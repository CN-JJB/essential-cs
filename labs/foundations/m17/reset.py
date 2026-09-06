#!/usr/bin/env python3
"""
Fail-closed, idempotent cleanup for M17 course-owned runtime artifacts.

Only removes files created under labs/foundations/m17/.scratch and the local
__pycache__ directory. Source files and any unrelated JSON are never globbed.
"""

import os
import shutil
import sys


M17_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(M17_DIR, ".scratch")
PYCACHE_DIR = os.path.join(M17_DIR, "__pycache__")


def reset_m17_environment() -> int:
    errors = []

    for owned_dir in (SCRATCH_DIR, PYCACHE_DIR):
        if not os.path.exists(owned_dir):
            continue
        try:
            shutil.rmtree(owned_dir)
        except OSError as exc:
            errors.append(f"{owned_dir}: {exc}")

    if errors:
        message = "M17 cleanup incomplete: " + "; ".join(errors)
        print(f"[RESET] {message}", file=sys.stderr)
        raise RuntimeError(message)

    print("[RESET] M17 course-owned scratch is clean.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(reset_m17_environment())
    except RuntimeError:
        sys.exit(1)
