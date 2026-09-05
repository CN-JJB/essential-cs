#!/usr/bin/env python3
"""
M13 Synthetic Fixture and Query Plan Helper.
Supports L13-01 (Access Paths & Indexing) and L13-02 (SQL Intent vs Engine Reality).

Safety:
- Operates on course-owned local SQLite files only.
- Deterministic pseudo-random generation with fixed seed.
- Bounded dataset sizes; zero external dependencies.
"""

import os
import random
import sqlite3
import time


def get_default_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "m13_foundations.db")


def generate_synthetic_data(db_path=None, user_count=200, order_count=2000, seed=42):
    """
    Deterministically populate users and orders tables.
    Bounded scale suitable for desktop execution and EQP demonstration.
    """
    target_path = db_path or get_default_db_path()
    if os.path.exists(target_path):
        os.remove(target_path)

    rng = random.Random(seed)
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    statuses = ["PENDING", "COMPLETED", "CANCELLED", "REFUNDED"]
    user_rows = []
    for uid in range(1, user_count + 1):
        uname = f"user_{uid}"
        mail = f"{uname}@example.com"
        st = statuses[uid % len(statuses)]
        dt = f"2026-01-{(uid % 28) + 1:02d}T10:00:00Z"
        user_rows.append((uid, uname, mail, st, dt))

    cur.executemany(
        "INSERT INTO users (id, username, email, status, created_at) VALUES (?, ?, ?, ?, ?);",
        user_rows,
    )

    order_rows = []
    for oid in range(1, order_count + 1):
        uid = rng.randint(1, user_count)
        amt = round(rng.uniform(5.0, 500.0), 2)
        st = statuses[rng.randint(0, len(statuses) - 1)]
        dt = f"2026-02-{(oid % 28) + 1:02d}T12:00:00Z"
        order_rows.append((oid, uid, amt, st, dt))

    cur.executemany(
        "INSERT INTO orders (id, user_id, amount, status, created_at) VALUES (?, ?, ?, ?, ?);",
        order_rows,
    )

    conn.commit()
    conn.close()
    return target_path


def inspect_eqp(conn, query, params=()):
    """
    Execute EXPLAIN QUERY PLAN and return parsed rows.
    """
    cur = conn.cursor()
    cur.execute(f"EXPLAIN QUERY PLAN {query}", params)
    rows = cur.fetchall()
    cur.close()
    return rows


def classify_eqp_detail(detail_str):
    """
    Semantically classify an EQP detail line without relying on exact string formatting.
    Identifies SCAN, SEARCH, and INDEX usage.
    """
    d_upper = detail_str.upper()
    has_scan = "SCAN " in d_upper or d_upper.startswith("SCAN")
    has_search = "SEARCH " in d_upper or d_upper.startswith("SEARCH")
    has_index = "INDEX" in d_upper
    has_covering = "COVERING INDEX" in d_upper

    if has_covering:
        return "COVERING_INDEX_SEARCH"
    elif has_search and has_index:
        return "INDEX_SEARCH"
    elif has_search:
        return "SEARCH_OTHER"
    elif has_scan:
        return "TABLE_SCAN"
    else:
        return "OTHER"


def compare_sargability(conn):
    """
    Demonstrate L13-02 sargability breakdown:
    - Sargable predicate: WHERE username = 'user_42' (can use index)
    - Non-sargable predicate: WHERE UPPER(username) = 'USER_42' (breaks index use)
    """
    q_sargable = "SELECT * FROM users WHERE username = 'user_42';"
    q_nonsargable = "SELECT * FROM users WHERE UPPER(username) = 'USER_42';"

    eqp_sargable = inspect_eqp(conn, q_sargable)
    eqp_nonsargable = inspect_eqp(conn, q_nonsargable)

    class_sargable = [classify_eqp_detail(r[3]) for r in eqp_sargable]
    class_nonsargable = [classify_eqp_detail(r[3]) for r in eqp_nonsargable]

    return {
        "sargable": {
            "query": q_sargable,
            "eqp_raw": [r[3] for r in eqp_sargable],
            "classifications": class_sargable,
        },
        "non_sargable": {
            "query": q_nonsargable,
            "eqp_raw": [r[3] for r in eqp_nonsargable],
            "classifications": class_nonsargable,
        },
    }


def main():
    print("Generating M13 synthetic dataset...")
    db_path = generate_synthetic_data()
    print(f"Database created at: {db_path} ({os.path.getsize(db_path)} bytes)")

    conn = sqlite3.connect(db_path)

    # 1. Unindexed vs Indexed on orders.user_id
    q_user = "SELECT * FROM orders WHERE user_id = 42;"
    eqp_before = inspect_eqp(conn, q_user)
    print("\n[L13-01] EQP on orders before secondary index:")
    for row in eqp_before:
        print(f"  detail: {row[3]} -> Classified: {classify_eqp_detail(row[3])}")

    conn.execute("CREATE INDEX idx_orders_user ON orders(user_id);")
    conn.commit()

    eqp_after = inspect_eqp(conn, q_user)
    print("\n[L13-01] EQP on orders after CREATE INDEX idx_orders_user:")
    for row in eqp_after:
        print(f"  detail: {row[3]} -> Classified: {classify_eqp_detail(row[3])}")

    # 2. Sargability on users.username
    sarg_res = compare_sargability(conn)
    print("\n[L13-02] Sargability comparison on users.username:")
    print("  Sargable query:", sarg_res["sargable"]["query"])
    print("    EQP detail:", sarg_res["sargable"]["eqp_raw"])
    print("    Classification:", sarg_res["sargable"]["classifications"])
    print("  Non-sargable query:", sarg_res["non_sargable"]["query"])
    print("    EQP detail:", sarg_res["non_sargable"]["eqp_raw"])
    print("    Classification:", sarg_res["non_sargable"]["classifications"])

    conn.close()


if __name__ == "__main__":
    main()
