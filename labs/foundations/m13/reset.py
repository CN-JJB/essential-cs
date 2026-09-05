#!/usr/bin/env python3
"""
Idempotent reset utility for M13 laboratory fixtures.
Cleans up all course-generated SQLite databases and sidecar files.
"""

import os
import sys


def reset_m13_fixtures():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    deleted_files = []
    patterns = (".db", ".db-journal", ".db-wal", ".db-shm")

    for entry in os.listdir(base_dir):
        if entry.endswith(patterns):
            target_path = os.path.join(base_dir, entry)
            try:
                os.remove(target_path)
                deleted_files.append(entry)
            except OSError as exc:
                print(f"Warning: Failed to delete {entry}: {exc}", file=sys.stderr)

    return deleted_files


def main():
    cleaned = reset_m13_fixtures()
    if cleaned:
        print(f"Reset complete. Removed {len(cleaned)} file(s): {', '.join(cleaned)}")
    else:
        print("Reset complete. Workspace clean; no lingering M13 database files found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
