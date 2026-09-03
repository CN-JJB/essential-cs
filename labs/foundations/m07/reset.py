#!/usr/bin/env python3
"""reset.py - Essential CS M07 Lab State Cleanup.

Restores the M07 lab directory to a clean initial state by removing
compiled binaries, object files, and bytecode caches.
"""

from __future__ import annotations

import shutil
from pathlib import Path


def clean_lab_artifacts() -> None:
    lab_dir = Path(__file__).resolve().parent

    # Binary and object files to remove
    artifacts = [
        lab_dir / "bad_address",
        lab_dir / "bad_address.exe",
    ]

    for p in artifacts:
        if p.exists():
            p.unlink()
            print(f"Removed: {p.name}")

    # Remove glob patterns: *.o, core, core.*
    for pattern in ["*.o", "core", "core.*"]:
        for p in lab_dir.glob(pattern):
            if p.is_file():
                p.unlink()
                print(f"Removed: {p.name}")

    # Remove __pycache__
    for pycache in lab_dir.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            print(f"Removed cache directory: {pycache.name}")

    print("M07 lab directory cleaned successfully.")


if __name__ == "__main__":
    clean_lab_artifacts()
