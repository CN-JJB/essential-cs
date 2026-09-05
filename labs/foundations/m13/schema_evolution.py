#!/usr/bin/env python3
"""
M13 Schema Evolution and Provenance Fixture.
Supports L13-03 (Schema Choices, Invariants, Expand-Contract, Source of Truth vs Derived Views).

Demonstrates:
1. Controlled Break: Attempting to add a NOT NULL column without DEFAULT to populated table fails.
2. Expand-Contract Pattern:
   - Expand: Add nullable or defaulted new column; dual-version reader compatibility.
   - Backfill: Bounded batch migration of historical records.
   - Contract: Transition reader queries and verify state invariants.
3. Source of Truth vs Intentionally Recomputable Derived View:
   - Primary operational records in `orders` (Source of Truth).
   - Recomputable aggregate in `user_order_summary` with explicit provenance metadata.
"""

import datetime
import json
import os
import sqlite3


def get_evolution_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "m13_evolution.db")


def setup_initial_database(db_path=None):
    """
    Initialize schema v1.0 with initial rows.
    """
    target_path = db_path or get_evolution_db_path()
    if os.path.exists(target_path):
        os.remove(target_path)

    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    # Populate initial records
    users_data = [
        (1, "alice", "alice@example.com", "2026-01-01T00:00:00Z"),
        (2, "bob", "bob@example.com", "2026-01-02T00:00:00Z"),
        (3, "charlie", "charlie@example.com", "2026-01-03T00:00:00Z"),
    ]
    cur.executemany("INSERT INTO users VALUES (?, ?, ?, ?);", users_data)

    orders_data = [
        (101, 1, 45.50, "2026-01-05T12:00:00Z"),
        (102, 1, 15.00, "2026-01-06T12:00:00Z"),
        (103, 2, 99.00, "2026-01-07T12:00:00Z"),
        (104, 3, 12.50, "2026-01-08T12:00:00Z"),
        (105, 1, 100.00, "2026-01-09T12:00:00Z"),
    ]
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?);", orders_data)

    conn.commit()
    conn.close()
    return target_path


def demonstrate_controlled_break(db_path=None):
    """
    Controlled Break:
    Adding a NOT NULL column without DEFAULT to an already populated table
    violates SQLite schema invariants and raises OperationalError.
    """
    target_path = db_path or get_evolution_db_path()
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    break_succeeded = False
    error_message = None
    try:
        # This statement must fail on populated table in SQLite
        cur.execute("ALTER TABLE users ADD COLUMN phone_number TEXT NOT NULL;")
        conn.commit()
    except sqlite3.OperationalError as exc:
        break_succeeded = True
        error_message = str(exc)
    finally:
        conn.close()

    return {
        "attempted_statement": "ALTER TABLE users ADD COLUMN phone_number TEXT NOT NULL;",
        "break_observed": break_succeeded,
        "error_message": error_message,
    }


def execute_expand_phase(db_path=None):
    """
    Expand Phase:
    Safely add new column with DEFAULT value to preserve backward compatibility for readers.
    """
    target_path = db_path or get_evolution_db_path()
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    # Expand: add column with safe default
    cur.execute("ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'PENDING_VERIFICATION';")
    conn.commit()

    # Verify both old and new columns are accessible
    cur.execute("SELECT id, username, status FROM users ORDER BY id;")
    rows = cur.fetchall()
    conn.close()

    return {
        "status": "EXPAND_COMPLETE",
        "rows": rows,
    }


def execute_backfill_phase(db_path=None):
    """
    Backfill Phase:
    Update existing records in controlled fashion.
    """
    target_path = db_path or get_evolution_db_path()
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    # Bounded migration update
    cur.execute("UPDATE users SET status = 'ACTIVE' WHERE created_at < '2026-01-03T00:00:00Z';")
    updated_count = cur.rowcount
    conn.commit()

    cur.execute("SELECT id, username, status FROM users ORDER BY id;")
    rows = cur.fetchall()
    conn.close()

    return {
        "status": "BACKFILL_COMPLETE",
        "updated_count": updated_count,
        "rows": rows,
    }


def recompute_derived_view(db_path=None):
    """
    Single Source of Truth vs Intentionally Recomputable Derived View:
    Computes user order totals from `orders` (Source of Truth) into `user_order_summary`
    with explicit provenance metadata.
    """
    target_path = db_path or get_evolution_db_path()
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    # Recreate derived summary table
    cur.execute("DROP TABLE IF EXISTS user_order_summary;")
    cur.execute("""
    CREATE TABLE user_order_summary (
        user_id INTEGER PRIMARY KEY,
        order_count INTEGER NOT NULL,
        total_spent REAL NOT NULL,
        provenance_metadata TEXT NOT NULL
    );
    """)

    # Aggregate from Source of Truth
    cur.execute("""
    SELECT user_id, COUNT(*) as cnt, SUM(amount) as total
    FROM orders
    GROUP BY user_id;
    """)
    aggregates = cur.fetchall()

    now_ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    summary_rows = []
    for uid, cnt, total in aggregates:
        prov = json.dumps({
            "source_tables": ["orders"],
            "recomputed_at": now_ts,
            "engine": "sqlite_m13_derived_view",
            "schema_version": "v1.1",
        })
        summary_rows.append((uid, cnt, round(total, 2), prov))

    cur.executemany("INSERT INTO user_order_summary VALUES (?, ?, ?, ?);", summary_rows)
    conn.commit()

    cur.execute("SELECT user_id, order_count, total_spent, provenance_metadata FROM user_order_summary ORDER BY user_id;")
    derived_rows = cur.fetchall()
    conn.close()

    return {
        "recomputed_count": len(derived_rows),
        "rows": derived_rows,
    }


def main():
    print("Initializing initial database (v1.0)...")
    db_path = setup_initial_database()
    print(f"Database at: {db_path}")

    print("\n[Controlled Break] Attempting naive NOT NULL column addition without DEFAULT:")
    break_res = demonstrate_controlled_break(db_path)
    print(f"  Attempt: {break_res['attempted_statement']}")
    print(f"  Expected Break Observed: {break_res['break_observed']}")
    print(f"  Captured Error: {break_res['error_message']}")

    print("\n[Expand Phase] Adding status column with safe DEFAULT:")
    expand_res = execute_expand_phase(db_path)
    print(f"  Status: {expand_res['status']}")
    for r in expand_res["rows"]:
        print(f"    user {r[0]} ({r[1]}): status={r[2]}")

    print("\n[Backfill Phase] Updating legacy user statuses:")
    backfill_res = execute_backfill_phase(db_path)
    print(f"  Updated rows: {backfill_res['updated_count']}")
    for r in backfill_res["rows"]:
        print(f"    user {r[0]} ({r[1]}): status={r[2]}")

    print("\n[Derived View] Recomputing user_order_summary from Source of Truth (orders):")
    deriv_res = recompute_derived_view(db_path)
    for r in deriv_res["rows"]:
        print(f"    user {r[0]}: orders={r[1]}, total=${r[2]:.2f}, prov={r[3]}")


if __name__ == "__main__":
    main()
