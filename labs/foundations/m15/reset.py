#!/usr/bin/env python3
"""
Idempotent reset script for M15 Foundations activities.
Removes any temporary files, compiled binaries, and logs created by M15 activities.
"""

import os
import sys

TARGET_EXTENSIONS = {".o", ".exe", ".out", ".tmp", ".pyc"}
TARGET_BIN_NAMES = {
    "atomic_lost_update",
    "atomic_lost_update.exe",
}


def reset_m15_foundations(foundations_dir=None, verbose=True):
    target_dir = foundations_dir or os.path.dirname(os.path.abspath(__file__))
    removed_count = 0

    for fname in os.listdir(target_dir):
        fpath = os.path.join(target_dir, fname)
        if not os.path.isfile(fpath):
            continue

        _, ext = os.path.splitext(fname)
        if ext.lower() in TARGET_EXTENSIONS or fname in TARGET_BIN_NAMES:
            try:
                os.remove(fpath)
                removed_count += 1
                if verbose:
                    print(f"Removed artifact: {fname}")
            except OSError as exc:
                if verbose:
                    print(f"Warning: could not remove {fname}: {exc}")

    if verbose:
        print(f"M15 Foundations reset complete. {removed_count} artifacts removed.")
    return removed_count


if __name__ == "__main__":
    count = reset_m15_foundations(verbose=True)
    sys.exit(0)
