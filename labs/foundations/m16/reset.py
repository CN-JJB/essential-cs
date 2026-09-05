#!/usr/bin/env python3
"""
Reset script for M16 Foundations activities.
Idempotently cleans up database, journal, WAL, SHM, temporary, and log files.
Must be idempotent and pass cleanly when executed repeatedly.
"""

import glob
import os
import sys

LAB_DIR = os.path.dirname(os.path.abspath(__file__))


def reset_m16_foundations(verbose: bool = True) -> int:
    patterns = [
        os.path.join(LAB_DIR, "*.db"),
        os.path.join(LAB_DIR, "*.db-journal"),
        os.path.join(LAB_DIR, "*.db-wal"),
        os.path.join(LAB_DIR, "*.db-shm"),
        os.path.join(LAB_DIR, "*.tmp"),
        os.path.join(LAB_DIR, "*.log"),
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
        print(f"[RESET] M16 Foundations reset complete. ({removed_count} files removed)")
    return removed_count


if __name__ == "__main__":
    reset_m16_foundations(verbose=True)
