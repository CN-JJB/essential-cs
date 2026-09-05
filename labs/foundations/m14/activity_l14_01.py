#!/usr/bin/env python3
"""
Activity L14-01: Transaction Boundaries, Invariants & Rollback Mechanics

Demonstrates:
1. Multi-step state transition (S0 -> S1) preserving declared invariant (sum = 1000).
2. Simulated failure mid-transaction followed by explicit ROLLBACK, restoring S0.
3. Successful multi-step transition followed by COMMIT to S1.
4. Rollback journal observation under declared DELETE journal mode.
5. Critical inference limit: application rollback != power-loss durability.
"""

import os
import sqlite3
import sys
from typing import Dict, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "l14_01_transactions.db")


def init_database(db_path: str = DEFAULT_DB_PATH) -> Tuple[sqlite3.Connection, Dict[str, str]]:
    if os.path.exists(db_path):
        os.remove(db_path)

    # isolation_level=None allows manual transaction control (BEGIN/COMMIT/ROLLBACK)
    # and prevents implicit transactions during PRAGMA execution
    conn = sqlite3.connect(db_path, isolation_level=None)
    cursor = conn.cursor()

    # Explicitly set and verify rollback journal DELETE mode
    cursor.execute("PRAGMA journal_mode = DELETE;")
    actual_journal_mode = cursor.fetchone()[0]

    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.execute("PRAGMA synchronous;")
    actual_synchronous = cursor.fetchone()[0]

    cursor.execute("""
        CREATE TABLE accounts (
            id TEXT PRIMARY KEY,
            balance INTEGER NOT NULL CHECK (balance >= 0)
        );
    """)
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('A', 600), ('B', 400);")
    conn.commit()

    meta = {
        "sqlite_version": sqlite3.sqlite_version,
        "journal_mode": actual_journal_mode.upper(),
        "synchronous": str(actual_synchronous),
        "db_path": db_path,
    }
    return conn, meta


def get_balances(conn: sqlite3.Connection) -> Dict[str, int]:
    cursor = conn.cursor()
    cursor.execute("SELECT id, balance FROM accounts ORDER BY id ASC;")
    return {row[0]: row[1] for row in cursor.fetchall()}


def verify_invariant(balances: Dict[str, int], expected_total: int = 1000) -> bool:
    total = sum(balances.values())
    return total == expected_total


def run_activity_l14_01(db_path: str = DEFAULT_DB_PATH, verbose: bool = True) -> Dict[str, object]:
    conn, meta = init_database(db_path)
    cursor = conn.cursor()

    results = {
        "meta": meta,
        "baseline": {},
        "failed_transfer": {},
        "post_rollback": {},
        "successful_transfer": {},
        "post_commit": {},
        "journal_observed": False,
        "inference_limit_acknowledged": True,
    }

    try:
        # Step 1: Baseline inspection (S0)
        baseline = get_balances(conn)
        results["baseline"] = baseline
        if verbose:
            print("=" * 60)
            print(" Activity L14-01: Transactions, Invariants & Rollback")
            print("=" * 60)
            print(f" SQLite Version: {meta['sqlite_version']}, Journal Mode: {meta['journal_mode']}")
            print(f" [S0 Baseline] Balances: {baseline}, Total = {sum(baseline.values())}")
        assert verify_invariant(baseline, 1000), "Baseline invariant violated!"

        # Step 2: Simulated failure mid-transaction
        # Transfer 100 from A to B, but crash before crediting B
        journal_path = db_path + "-journal"
        cursor.execute("BEGIN IMMEDIATE;")
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 'A';")

        # In-transaction partial state
        in_trans_balances = get_balances(conn)
        results["failed_transfer"]["in_transaction"] = in_trans_balances
        if verbose:
            print(f" [In-Transaction] Debited A: {in_trans_balances}, Total = {sum(in_trans_balances.values())}")
            print(f" [Check] Invariant temporarily broken in active tx: sum is {sum(in_trans_balances.values())} (expected 1000)")

        # Observe journal side-file
        journal_exists = os.path.exists(journal_path)
        results["journal_observed"] = journal_exists
        if verbose:
            print(f" [Observation] Rollback journal exists on disk: {journal_exists} ({journal_path})")

        # Simulate failure: an exception occurs
        if verbose:
            print(" [Failure Injection] Simulating network/application fault before crediting B...")
        cursor.execute("ROLLBACK;")
        if verbose:
            print(" [ROLLBACK] Explicit ROLLBACK executed.")

        # Step 3: Verify post-rollback state (restored S0)
        post_rollback = get_balances(conn)
        results["post_rollback"] = post_rollback
        if verbose:
            print(f" [Post-Rollback] Balances: {post_rollback}, Total = {sum(post_rollback.values())}")
        assert post_rollback == baseline, "Rollback failed to restore baseline state!"
        assert verify_invariant(post_rollback, 1000), "Post-rollback invariant violated!"

        # Step 4: Successful complete transaction (S0 -> S1)
        cursor.execute("BEGIN IMMEDIATE;")
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 'A';")
        cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 'B';")
        cursor.execute("COMMIT;")
        if verbose:
            print(" [COMMIT] Multi-step transfer committed successfully.")

        post_commit = get_balances(conn)
        results["post_commit"] = post_commit
        if verbose:
            print(f" [S1 Committed] Balances: {post_commit}, Total = {sum(post_commit.values())}")
            print(f" [Check] Invariant holds in S1: sum = {sum(post_commit.values())}")
        assert post_commit == {"A": 500, "B": 500}, "Committed state unexpected!"
        assert verify_invariant(post_commit, 1000), "Post-commit invariant violated!"

        if verbose:
            print("-" * 60)
            print(" [Inference Limit Reminder]")
            print(" Demonstrating explicit rollback proves transaction atomicity and rollback capability,")
            print(" but does NOT prove physical power-loss durability against un-flushed disk caches.")
            print("=" * 60)

    finally:
        conn.close()

    return results


if __name__ == "__main__":
    run_activity_l14_01(verbose=True)
