#!/usr/bin/env python3
"""
reset.py — Fail-Closed, Idempotent Cleanup for M22 Runtime Artifacts
===================================================================

Removes course-owned scratch artifacts under labs/foundations/m22/.scratch/ including:
- Observation records: *.json, *.jsonl, *.tmp, *.log
- Scratch notes: *.md
- Local Python cache: __pycache__/

Source files and code are never touched.
Fails closed if any deletion encounters an unrecoverable error.
"""

from __future__ import annotations

import glob
import os
import shutil
import sys

M22_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = os.path.join(M22_DIR, ".scratch")
PYCACHE_DIR = os.path.join(M22_DIR, "__pycache__")


def reset_m22_environment(verbose: bool = True) -> int:
    errors = []
    removed_count = 0

    # 1. Clean scratch directory files and directory
    if os.path.isdir(SCRATCH_DIR):
        patterns = ("*.json", "*.jsonl", "*.tmp", "*.log", "*.md")
        for pat in patterns:
            for file_path in glob.glob(os.path.join(SCRATCH_DIR, pat)):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_count += 1
                        if verbose:
                            print(f"[RESET] Removed scratch file: {file_path}")
                except OSError as exc:
                    errors.append(f"{file_path}: {exc}")

        try:
            shutil.rmtree(SCRATCH_DIR)
            if verbose:
                print(f"[RESET] Removed directory: {SCRATCH_DIR}")
        except OSError as exc:
            errors.append(f"{SCRATCH_DIR}: {exc}")

    # 2. Clean __pycache__ directory
    if os.path.isdir(PYCACHE_DIR):
        try:
            shutil.rmtree(PYCACHE_DIR)
            if verbose:
                print(f"[RESET] Removed directory: {PYCACHE_DIR}")
        except OSError as exc:
            errors.append(f"{PYCACHE_DIR}: {exc}")

    if errors:
        message = "M22 cleanup incomplete: " + "; ".join(errors)
        if verbose:
            print(f"[RESET ERROR] {message}", file=sys.stderr)
        raise RuntimeError(message)

    if verbose:
        print("[RESET] M22 course-owned scratch is clean.")
    return removed_count


if __name__ == "__main__":
    try:
        reset_m22_environment(verbose=True)
        sys.exit(0)
    except RuntimeError:
        sys.exit(1)
