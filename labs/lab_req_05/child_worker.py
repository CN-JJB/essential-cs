#!/usr/bin/env python3
"""
Child worker process for LAB-REQ-05 Checkpoint 4 (Owned Child Interruption).

Lifecycle:
1. Connects to the designated SQLite database.
2. Ensures DELETE journal mode.
3. Opens BEGIN IMMEDIATE transaction and mutates state.
4. Flushes 'CHILD_MUTATED' message to stdout.
5. Pauses execution until terminated abruptly by the parent process.
"""

import os
import sqlite3
import sys
import time


def main():
    if len(sys.argv) < 2:
        print("Usage: child_worker.py <db_path>", file=sys.stderr)
        sys.exit(1)

    db_path = sys.argv[1]
    conn = sqlite3.connect(db_path, isolation_level=None)
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA journal_mode = DELETE;")
        cursor.execute("BEGIN IMMEDIATE;")
        cursor.execute("UPDATE accounts SET balance = 100 WHERE id = 'A';")

        # Notify parent process that mutation has occurred
        print("CHILD_MUTATED", flush=True)

        # Sleep and await abrupt termination from parent watchdog
        while True:
            time.sleep(1.0)

    except Exception as e:
        print(f"CHILD_ERROR: {e}", flush=True)
        sys.exit(2)
    finally:
        # Note: In a real crash or SIGKILL/terminate, this finally block is bypassed.
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
