#!/usr/bin/env python3
"""
Idempotent reset script for LAB-REQ-03.
Removes compiled test binaries, object files, and temporary execution artifacts.
"""

import os
import sys

TARGET_EXTENSIONS = {".o", ".exe", ".out", ".tmp", ".pyc"}
TARGET_BIN_NAMES = {
    "broken_counter",
    "mutex_counter",
    "cond_rendezvous",
    "deadlock_preconditions",
    "broken_counter.exe",
    "mutex_counter.exe",
    "cond_rendezvous.exe",
    "deadlock_preconditions.exe",
}


def reset_lab_req_03(lab_dir=None, verbose=True):
    target_dir = lab_dir or os.path.dirname(os.path.abspath(__file__))
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
        print(f"Reset complete. {removed_count} artifacts removed.")
    return removed_count


if __name__ == "__main__":
    count = reset_lab_req_03(verbose=True)
    sys.exit(0)
