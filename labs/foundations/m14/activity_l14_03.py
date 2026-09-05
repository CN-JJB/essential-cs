#!/usr/bin/env python3
"""
Activity L14-03: Atomic Write Design, Lock-Upgrade Collisions & Boundary Retries

Demonstrates:
1. The lock-upgrade hazard: concurrent connections reading with BEGIN DEFERRED and then
   attempting to upgrade to write locks encounter SQLITE_BUSY under rollback-journal locking.
2. The architectural fix: BEGIN IMMEDIATE acquires write intent at transaction start,
   serializing write intent and eliminating read-to-write upgrade collisions.
3. Transaction-boundary retry loop: transient conflict handling with ROLLBACK,
   bounded exponential backoff, and an idempotency token check preventing duplicate execution.
4. Essential guardrails: non-transient errors (syntax, constraints) must fail fast, not retry.
"""

import os
import sqlite3
import sys
import time
from typing import Any, Dict, List, Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "l14_03_atomic_write.db")


def _is_busy_conflict(exc: sqlite3.Error) -> bool:
    """Classify SQLite BUSY/LOCKED structurally, without matching driver message text."""
    code = getattr(exc, "sqlite_errorcode", None)
    name = getattr(exc, "sqlite_errorname", None)
    primary_codes = {
        getattr(sqlite3, "SQLITE_BUSY", 5),
        getattr(sqlite3, "SQLITE_LOCKED", 6),
    }
    if isinstance(code, int) and (code & 0xFF) in primary_codes:
        return True
    if isinstance(name, str) and (name.startswith("SQLITE_BUSY") or name.startswith("SQLITE_LOCKED")):
        return True
    return False


def init_database(db_path: str = DEFAULT_DB_PATH) -> Dict[str, str]:
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode = DELETE;")
    actual_journal_mode = cursor.fetchone()[0]
    cursor.execute("PRAGMA synchronous = NORMAL;")

    cursor.execute("""
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY,
            balance INTEGER NOT NULL CHECK (balance >= 0)
        );
    """)
    cursor.execute("""
        CREATE TABLE processed_tokens (
            token TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('A', 600), ('B', 400);")
    conn.close()

    return {
        "sqlite_version": sqlite3.sqlite_version,
        "journal_mode": actual_journal_mode.upper(),
        "db_path": db_path,
    }


def demonstrate_upgrade_collision(db_path: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Demonstrates a read-to-write upgrade conflict under SQLite rollback-journal mode:
    both connections establish read transactions; connection 1 then becomes the writer,
    and connection 2's later upgrade fails with a BUSY/LOCKED-class result because
    another writer already exists.
    """
    conn1 = sqlite3.connect(db_path, timeout=0.0, isolation_level=None)
    conn2 = sqlite3.connect(db_path, timeout=0.0, isolation_level=None)

    cur1 = conn1.cursor()
    cur2 = conn2.cursor()

    collision_info: Dict[str, Any] = {
        "collision_observed": False,
        "error_type": None,
        "error_message": None,
        "sqlite_errorcode": None,
        "sqlite_errorname": None,
    }

    try:
        # Both start deferred transactions
        cur1.execute("BEGIN DEFERRED;")
        cur1.execute("SELECT balance FROM accounts WHERE id = 'A';")
        _ = cur1.fetchone()[0]

        cur2.execute("BEGIN DEFERRED;")
        cur2.execute("SELECT balance FROM accounts WHERE id = 'A';")
        _ = cur2.fetchone()[0]

        # Conn 1 attempts write
        cur1.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 'A';")

        # Conn 2 attempts write while Conn 1 has reserved lock -> Lock Upgrade Collision!
        try:
            cur2.execute("UPDATE accounts SET balance = balance - 10 WHERE id = 'A';")
        except sqlite3.OperationalError as e:
            collision_info["error_type"] = type(e).__name__
            collision_info["error_message"] = str(e)
            collision_info["sqlite_errorcode"] = getattr(e, "sqlite_errorcode", None)
            collision_info["sqlite_errorname"] = getattr(e, "sqlite_errorname", None)
            if _is_busy_conflict(e):
                collision_info["collision_observed"] = True
                if verbose:
                    print(" [Upgrade Collision] Conn 2 could not upgrade while Conn 1 is the writer:")
                    print(f"                     {type(e).__name__}: {e}")
            else:
                raise

        # Cleanup active transactions
        try:
            cur1.execute("ROLLBACK;")
        except sqlite3.Error:
            pass
        try:
            cur2.execute("ROLLBACK;")
        except sqlite3.Error:
            pass

    finally:
        conn1.close()
        conn2.close()

    return collision_info


def execute_with_boundary_retry(
    db_path: str,
    from_id: str,
    to_id: str,
    amount: int,
    idempotency_token: str,
    max_retries: int = 5,
    base_backoff_sec: float = 0.01,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Executes a transfer using BEGIN IMMEDIATE, full rollback on conflict,
    exponential backoff, and an idempotency token check.
    """
    attempts = 0
    start_time = time.time()

    conn = sqlite3.connect(db_path, timeout=0.1, isolation_level=None)
    cursor = conn.cursor()

    try:
        while attempts < max_retries:
            attempts += 1
            try:
                # 1. Begin immediate to acquire write intent upfront
                cursor.execute("BEGIN IMMEDIATE;")

                # 2. Idempotency check: has this token already been processed?
                cursor.execute("SELECT 1 FROM processed_tokens WHERE token = ?;", (idempotency_token,))
                if cursor.fetchone():
                    # Token already applied! Idempotent no-op
                    cursor.execute("ROLLBACK;")
                    if verbose:
                        print(f" [Idempotency] Token '{idempotency_token}' already applied. Skipping duplicate mutation.")
                    return {
                        "status": "ALREADY_PROCESSED",
                        "attempts": attempts,
                        "token": idempotency_token,
                    }

                # 3. Read current balance under write lock
                cursor.execute("SELECT balance FROM accounts WHERE id = ?;", (from_id,))
                row = cursor.fetchone()
                if not row or row[0] < amount:
                    cursor.execute("ROLLBACK;")
                    return {
                        "status": "INSUFFICIENT_FUNDS",
                        "attempts": attempts,
                        "token": idempotency_token,
                    }

                # 4. Perform mutations
                cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?;", (amount, from_id))
                cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?;", (amount, to_id))

                # 5. Record idempotency token
                cursor.execute("INSERT INTO processed_tokens (token) VALUES (?);", (idempotency_token,))

                # 6. Commit
                cursor.execute("COMMIT;")
                if verbose:
                    print(f" [Success] Transfer of {amount} from {from_id} to {to_id} committed (attempt {attempts}).")
                return {
                    "status": "COMMITTED",
                    "attempts": attempts,
                    "token": idempotency_token,
                }

            except sqlite3.OperationalError as e:
                # BEGIN IMMEDIATE itself can fail before a transaction begins.
                if conn.in_transaction:
                    try:
                        cursor.execute("ROLLBACK;")
                    except sqlite3.Error:
                        pass

                if _is_busy_conflict(e) and attempts < max_retries:
                    backoff = base_backoff_sec * (2 ** (attempts - 1))
                    if verbose:
                        print(f" [Conflict] Attempt {attempts} failed with busy/locked result. Backing off {backoff:.3f}s...")
                    time.sleep(backoff)
                    continue

                # Unknown operational errors and exhausted retry budgets remain failures.
                raise

            except sqlite3.IntegrityError:
                # Non-transient constraint error: rollback an active transaction and fail fast.
                if conn.in_transaction:
                    cursor.execute("ROLLBACK;")
                raise

        return {"status": "MAX_RETRIES_EXCEEDED", "attempts": attempts, "token": idempotency_token}

    finally:
        conn.close()


def run_activity_l14_03(db_path: str = DEFAULT_DB_PATH, verbose: bool = True) -> Dict[str, Any]:
    meta = init_database(db_path)

    if verbose:
        print("=" * 66)
        print(" Activity L14-03: Atomic Write Design & Boundary Retries")
        print("=" * 66)
        print(f" SQLite Version: {meta['sqlite_version']}, Journal Mode: {meta['journal_mode']}")

    # Part 1: Demonstrate deferred upgrade collision
    collision_result = demonstrate_upgrade_collision(db_path, verbose=verbose)

    # Part 2: Transaction-boundary retry with idempotency
    token = "tx-req-transfer-001"
    res1 = execute_with_boundary_retry(db_path, "A", "B", 50, token, verbose=verbose)
    assert res1["status"] == "COMMITTED", f"First execution failed: {res1}"

    # Verify idempotency: re-executing with the exact same token does not double-spend
    res2 = execute_with_boundary_retry(db_path, "A", "B", 50, token, verbose=verbose)
    assert res2["status"] == "ALREADY_PROCESSED", f"Idempotency check failed: {res2}"

    # Check balances: A was 600, should now be 550; B was 400, should now be 450; sum = 1000
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
    final_balances = dict(cur.fetchall())
    conn.close()

    assert final_balances == {"A": 550, "B": 450}, f"Unexpected final balances: {final_balances}"
    total = sum(final_balances.values())
    assert total == 1000, f"Invariant sum violation: total is {total}"

    if verbose:
        print(f" [Final State] Balances: {final_balances}, Invariant Total = {total}")
        print("-" * 66)
        print(" [Guardrail Summary]")
        print(" 1. BEGIN IMMEDIATE serializes write intent upfront, avoiding upgrade collisions.")
        print(" 2. Transient conflicts (SQLITE_BUSY) trigger ROLLBACK + bounded backoff + retry.")
        print(" 3. Non-transient errors (syntax, constraint, application logic) FAIL FAST without retry.")
        print(" 4. Idempotency tokens ensure retried executions do not duplicate mutations.")
        print("=" * 66)

    return {
        "meta": meta,
        "collision_result": collision_result,
        "first_execution": res1,
        "idempotent_execution": res2,
        "final_balances": final_balances,
    }


if __name__ == "__main__":
    run_activity_l14_03(verbose=True)
