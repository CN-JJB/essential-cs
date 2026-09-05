#!/usr/bin/env python3
"""
Deterministic synthetic dataset generator for LAB-REQ-04.
Generates an unindexed orders table with bounded size for indexing & plan experiments.

Safety:
- Course-owned local file only.
- Deterministic pseudo-random generation with fixed seed.
- Bounded row count; zero external dependencies.
"""

import os
import random
import sqlite3


def get_default_lab_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "lab_orders.db")


def generate_lab_dataset(db_path=None, row_count=5000, seed=42):
    """
    Populate lab_orders database with deterministic rows.
    """
    target_path = db_path or get_default_lab_db_path()
    if os.path.exists(target_path):
        os.remove(target_path)

    rng = random.Random(seed)
    conn = sqlite3.connect(target_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        region TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    statuses = ["PENDING", "PROCESSING", "COMPLETED", "CANCELLED", "REFUNDED"]
    regions = ["US_EAST", "US_WEST", "EU_CENTRAL", "AP_EAST"]

    rows = []
    for oid in range(1, row_count + 1):
        # user_id distribution: skewed so some users have many orders, some few
        uid = rng.randint(1, 250)
        amt = round(rng.uniform(1.0, 1000.0), 2)
        st = statuses[rng.randint(0, len(statuses) - 1)]
        reg = regions[rng.randint(0, len(regions) - 1)]
        dt = f"2026-03-{(oid % 28) + 1:02d}T{(oid % 24):02d}:00:00Z"
        rows.append((oid, uid, amt, st, reg, dt))

    cur.executemany(
        "INSERT INTO orders (id, user_id, amount, status, region, created_at) VALUES (?, ?, ?, ?, ?, ?);",
        rows,
    )

    conn.commit()
    conn.close()
    return target_path


if __name__ == "__main__":
    path = generate_lab_dataset()
    print(f"LAB-REQ-04 dataset generated at: {path} ({os.path.getsize(path)} bytes)")
