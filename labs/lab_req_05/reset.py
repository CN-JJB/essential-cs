#!/usr/bin/env python3
"""
Reset script for LAB-REQ-05: SQLite Transactions & Recovery.
Idempotently removes all test databases, rollback journals, WAL files, and backups.
"""

import glob
import os
import sys

LAB_DIR = os.path.dirname(os.path.abspath(__file__))


def reset_lab_req_05(verbose: bool = True) -> int:
    patterns = [
        os.path.join(LAB_DIR, "*.db"),
        os.path.join(LAB_DIR, "*.db-journal"),
        os.path.join(LAB_DIR, "*.db-wal"),
        os.path.join(LAB_DIR, "*.db-shm"),
        os.path.join(LAB_DIR, "*.bak"),
    ]
    removed_count = 0
    for pattern in patterns:
        for file_path in glob.glob(pattern):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    removed_count += 1
                    if verbose:
                        print(f"[RESET] Removed: {os.path.basename(file_path)}")
            except OSError as e:
                if verbose:
                    print(f"[RESET] Error removing {file_path}: {e}", file=sys.stderr)
    if verbose:
        print(f"[RESET] LAB-REQ-05 reset complete. ({removed_count} files removed)")
    return removed_count


if __name__ == "__main__":
    reset_lab_req_05(verbose=True)
