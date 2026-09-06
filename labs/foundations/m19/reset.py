#!/usr/bin/env python3
"""
Fail-closed, idempotent cleanup for M19 course-owned runtime artifacts.

Removes files created under labs/foundations/m19/.scratch/ including:
- Observation records: *.json, *.tmp, *.log
- Databases: *.db, *.db-journal, *.db-wal, *.db-shm
- Local Python cache: __pycache__/

Source files and code are never touched.
Fails closed (raises RuntimeError) if any deletion encounters an error.
Idempotent: passes when run multiple times in sequence.
"""

import glob
import os
import shutil
import sys
from typing import Optional

M19_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(M19_DIR, ".scratch")
PYCACHE_DIR = os.path.join(M19_DIR, "__pycache__")


def reset_m19_environment(
    verbose: bool = True,
    scratch_dir: Optional[str] = None,
    pycache_dir: Optional[str] = None,
) -> int:
    target_scratch = scratch_dir if scratch_dir is not None else SCRATCH_DIR
    target_pycache = pycache_dir if pycache_dir is not None else PYCACHE_DIR

    errors = []
    removed_count = 0

    # 1. Clean scratch directory files and directory
    if os.path.isdir(target_scratch):
        patterns = (
            "*.db",
            "*.db-journal",
            "*.db-wal",
            "*.db-shm",
            "*.json",
            "*.tmp",
            "*.log",
        )
        for pat in patterns:
            for file_path in glob.glob(os.path.join(target_scratch, pat)):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_count += 1
                        if verbose:
                            print(f"[RESET] Removed scratch file: {file_path}")
                except OSError as exc:
                    errors.append(f"{file_path}: {exc}")

        # Also remove scratch directory
        try:
            shutil.rmtree(target_scratch)
            if verbose:
                print(f"[RESET] Removed directory: {target_scratch}")
        except OSError as exc:
            errors.append(f"{target_scratch}: {exc}")

    # 2. Clean __pycache__ directory
    if os.path.isdir(target_pycache):
        try:
            shutil.rmtree(target_pycache)
            if verbose:
                print(f"[RESET] Removed directory: {target_pycache}")
        except OSError as exc:
            errors.append(f"{target_pycache}: {exc}")

    if errors:
        message = "M19 cleanup incomplete: " + "; ".join(errors)
        if verbose:
            print(f"[RESET ERROR] {message}", file=sys.stderr)
        raise RuntimeError(message)

    if verbose:
        print("[RESET] M19 course-owned scratch is clean.")
    return removed_count


if __name__ == "__main__":
    try:
        reset_m19_environment(verbose=True)
        sys.exit(0)
    except RuntimeError:
        sys.exit(1)
