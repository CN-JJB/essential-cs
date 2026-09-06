#!/usr/bin/env python3
"""
labs/foundations/m17/reset.py

Idempotent cleanup script for M17 activities and test artifacts.
Removes generated observation JSON files, logs, and temporary scratch data.
Safe to run repeatedly.
"""

import glob
import os
import shutil
import sys


def reset_m17_environment() -> int:
    m17_dir = os.path.dirname(os.path.abspath(__file__))
    patterns = [
        "*.json",
        "*.tmp",
        "*.log",
    ]

    removed_files = 0
    for pattern in patterns:
        for filepath in glob.glob(os.path.join(m17_dir, pattern)):
            try:
                os.remove(filepath)
                removed_files += 1
            except OSError as e:
                print(f"[WARN] Failed to remove {filepath}: {e}", file=sys.stderr)

    # Clean __pycache__ if present
    pycache_dir = os.path.join(m17_dir, "__pycache__")
    if os.path.exists(pycache_dir):
        try:
            shutil.rmtree(pycache_dir)
        except OSError as e:
            print(f"[WARN] Failed to remove {pycache_dir}: {e}", file=sys.stderr)

    print(f"[RESET] M17 workspace clean. Removed {removed_files} artifact(s).")
    return 0


if __name__ == "__main__":
    sys.exit(reset_m17_environment())
