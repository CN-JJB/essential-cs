#!/usr/bin/env python3
"""
Activity L14-02: Concurrent Access, Isolation Anomalies & Consistency First Home

Demonstrates:
1. Dual independent connections to a single SQLite database under DELETE rollback journal.
2. Committed-only visibility: Connection 2 cannot observe uncommitted mutations of Connection 1
   (absence of Dirty Reads under SQLite's declared committed-only visibility baseline).
3. Bounded second-writer conflict: Connection 2 attempting a concurrent write is blocked or
   receives a busy conflict (SQLITE_BUSY), without hardcoding fixed exception strings.
4. Canonical First Home of EC-CON-014 Consistency with mandatory named qualifier.
"""

import os
import sqlite3
import sys
from typing import Any, Dict, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "l14_02_concurrency.db")

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


EC_CON_014_DEFINITION = (
    "The relationship between allowed state transitions and what observers may see, "
    "according to a named ordering/visibility guarantee."
)

EC_CON_014_QUALIFIER = (
    "Qualifier: 'Consistent' must be qualified by a named ordering/visibility guarantee. "
    "Consistency is not automatically freshness; consistency is not automatically correctness in every sense; "
    "consistency is not durability; ACID 'C' is application invariant preservation rather than the whole systems-consistency concept; "
    "and single-node transaction isolation is not distributed consistency. "
    "SQLite's declared visibility behavior is SQLite committed-only visibility under the declared local locking/journal baseline, "
    "not generic ANSI Read Committed."
)


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
    cursor.execute("INSERT INTO accounts (id, balance) VALUES ('A', 600), ('B', 400);")
    conn.close()

    return {
        "sqlite_version": sqlite3.sqlite_version,
        "journal_mode": actual_journal_mode.upper(),
        "db_path": db_path,
    }


def run_activity_l14_02(db_path: str = DEFAULT_DB_PATH, verbose: bool = True) -> Dict[str, Any]:
    meta = init_database(db_path)

    # Establish two independent connections
    # Note: timeout=0 so concurrent write conflict fails immediately rather than waiting
    conn1 = sqlite3.connect(db_path, timeout=0.0, isolation_level=None)
    conn2 = sqlite3.connect(db_path, timeout=0.0, isolation_level=None)

    results: Dict[str, Any] = {
        "meta": meta,
        "ec_con_014_definition": EC_CON_014_DEFINITION,
        "ec_con_014_qualifier": EC_CON_014_QUALIFIER,
        "dirty_read_prevented": False,
        "conn1_uncommitted_value": None,
        "conn2_observed_value": None,
        "writer_conflict": {},
        "post_rollback_consistent": False,
    }

    try:
        if verbose:
            print("=" * 66)
            print(" Activity L14-02: Concurrent Visibility & EC-CON-014 Consistency")
            print("=" * 66)
            print(f" SQLite Version: {meta['sqlite_version']}, Journal Mode: {meta['journal_mode']}")

        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        # Step 1: Connection 1 mutates Account A inside an active transaction
        cur1.execute("BEGIN IMMEDIATE;")
        cur1.execute("UPDATE accounts SET balance = 500 WHERE id = 'A';")
        cur1.execute("SELECT balance FROM accounts WHERE id = 'A';")
        c1_val = cur1.fetchone()[0]
        results["conn1_uncommitted_value"] = c1_val
        if verbose:
            print(f" [Conn 1] Mutated Account A in uncommitted transaction: balance = {c1_val}")

        # Step 2: Connection 2 queries Account A
        # Under SQLite committed-only visibility, Conn 2 must observe the committed value (600)
        cur2.execute("SELECT balance FROM accounts WHERE id = 'A';")
        c2_val = cur2.fetchone()[0]
        results["conn2_observed_value"] = c2_val
        if verbose:
            print(f" [Conn 2] Read Account A: observed balance = {c2_val}")

        assert c2_val == 600, f"Dirty Read detected! Conn 2 saw {c2_val}, expected committed 600"
        results["dirty_read_prevented"] = True
        if verbose:
            print(" [Check] Dirty Read prevented: Conn 2 observes only committed state (600).")

        # Step 3: Connection 2 attempts a competing write transaction
        # Conn 1 owns the active write transaction; exact lock-state progression is engine-internal evidence.
        # Conn 2 should encounter a busy conflict.
        conflict_detected = False
        error_info: Dict[str, Any] = {
            "error_type": None,
            "error_message": None,
            "sqlite_errorcode": None,
            "sqlite_errorname": None,
            "disposition": None,
        }

        try:
            cur2.execute("BEGIN IMMEDIATE;")
            cur2.execute("UPDATE accounts SET balance = 999 WHERE id = 'B';")
        except sqlite3.OperationalError as e:
            error_info["error_type"] = type(e).__name__
            error_info["error_message"] = str(e)
            error_info["sqlite_errorcode"] = getattr(e, "sqlite_errorcode", None)
            error_info["sqlite_errorname"] = getattr(e, "sqlite_errorname", None)
            if _is_busy_conflict(e):
                conflict_detected = True
                error_info["disposition"] = "BUSY_CONFLICT_CAPTURED"
                if verbose:
                    print(f" [Conn 2 Write Conflict] Busy/locked result recorded: {type(e).__name__}: {e}")
                    if error_info["sqlite_errorname"]:
                        print(f"          SQLite Error: {error_info['sqlite_errorname']} (code {error_info['sqlite_errorcode']})")
            else:
                error_info["disposition"] = "UNEXPECTED_OPERATIONAL_ERROR"
                raise
        except sqlite3.Error:
            raise

        results["writer_conflict"] = {
            "conflict_detected": conflict_detected,
            "error_info": error_info,
        }
        assert conflict_detected, "Expected competing write transaction to encounter busy conflict!"

        # Step 4: Connection 1 aborts via ROLLBACK
        cur1.execute("ROLLBACK;")
        if verbose:
            print(" [Conn 1] Rolled back active transaction.")

        # Step 5: Verify post-rollback consistency across both connections
        cur1.execute("SELECT balance FROM accounts WHERE id = 'A';")
        r1_final = cur1.fetchone()[0]
        cur2.execute("SELECT balance FROM accounts WHERE id = 'A';")
        r2_final = cur2.fetchone()[0]

        assert r1_final == 600 and r2_final == 600, f"Balances inconsistent after rollback: c1={r1_final}, c2={r2_final}"
        results["post_rollback_consistent"] = True
        if verbose:
            print(f" [Verification] Both connections observe restored baseline: A={r1_final}")
            print("-" * 66)
            print(f" [EC-CON-014 Consistency Definition]")
            print(f"  \"{EC_CON_014_DEFINITION}\"")
            print(f" [EC-CON-014 Mandatory Qualifier]")
            print(f"  {EC_CON_014_QUALIFIER}")
            print("=" * 66)

    finally:
        conn1.close()
        conn2.close()

    return results


if __name__ == "__main__":
    run_activity_l14_02(verbose=True)
