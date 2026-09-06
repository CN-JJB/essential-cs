#!/usr/bin/env python3
"""
Reset script for M16 Foundations activities.
Idempotently cleans only course-owned M16 scratch artifacts.
Cleanup failures are surfaced instead of being silently converted to success.
"""

import glob
import os
import sys

LAB_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(LAB_DIR, ".scratch")


def reset_m16_foundations(verbose: bool = True) -> int:
    roots = [LAB_DIR, SCRATCH_DIR]
    suffix_patterns = (
        "*.db",
        "*.db-journal",
        "*.db-wal",
        "*.db-shm",
        "*.tmp",
        "*.log",
    )
    removed_count = 0
    errors = []

    for root in roots:
        if not os.path.isdir(root):
            continue
        for suffix in suffix_patterns:
            for file_path in glob.glob(os.path.join(root, suffix)):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_count += 1
                        if verbose:
                            print(f"[RESET] Removed: {file_path}")
                except OSError as e:
                    errors.append(f"{file_path}: {e}")

    if errors:
        message = "M16 cleanup incomplete: " + "; ".join(errors)
        if verbose:
            print(f"[RESET] {message}", file=sys.stderr)
        raise RuntimeError(message)

    if os.path.isdir(SCRATCH_DIR):
        try:
            if not os.listdir(SCRATCH_DIR):
                os.rmdir(SCRATCH_DIR)
        except OSError:
            # Directory removal is best-effort only after all tracked artifacts are gone.
            pass

    if verbose:
        print(f"[RESET] M16 Foundations reset complete. ({removed_count} files removed)")
    return removed_count


if __name__ == "__main__":
    try:
        reset_m16_foundations(verbose=True)
    except RuntimeError:
        sys.exit(1)
