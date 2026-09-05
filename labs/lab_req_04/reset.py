#!/usr/bin/env python3
"""
Idempotent reset utility for LAB-REQ-04.
Cleans up all lab database files, sidecars, and generated execution traces.
"""

import os
import sys


def reset_lab_req_04():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    deleted = []
    patterns = (".db", ".db-journal", ".db-wal", ".db-shm", ".sql")

    for entry in os.listdir(base_dir):
        if entry.endswith(patterns):
            target_path = os.path.join(base_dir, entry)
            try:
                os.remove(target_path)
                deleted.append(entry)
            except OSError as exc:
                print(f"Warning: Failed to delete {entry}: {exc}", file=sys.stderr)

    return deleted


def main():
    cleaned = reset_lab_req_04()
    if cleaned:
        print(f"LAB-REQ-04 reset complete. Removed {len(cleaned)} file(s): {', '.join(cleaned)}")
    else:
        print("LAB-REQ-04 reset complete. Workspace clean; zero lingering files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
