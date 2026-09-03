#!/usr/bin/env python3
"""Cleanup and reset utility for M09 lab activities.

Removes temporary run directories, cache files, and generated artifacts in a scoped,
deterministic manner without wildcard-deleting arbitrary learner files.
"""

import shutil
import sys
from pathlib import Path


def reset_m09_workspace() -> int:
    current_dir = Path(__file__).parent.resolve()
    print(f"=== Resetting M09 Lab Workspace: {current_dir} ===")

    removed_count = 0

    # 1. Clean local temporary run directories and data files
    for item in current_dir.iterdir():
        if (
            item.name.startswith("_run_")
            or item.name.endswith(".tmp")
            or item.name.endswith(".dat")
            or item.name.startswith("temp_")
        ):
            if item.is_dir():
                shutil.rmtree(item)
                print(f"  [x] Removed directory: {item.name}")
            else:
                item.unlink()
                print(f"  [x] Removed file: {item.name}")
            removed_count += 1

    # 2. Clean __pycache__
    pycache = current_dir / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
        print("  [x] Removed __pycache__/")
        removed_count += 1

    print(f"Cleanup complete. Total artifacts removed: {removed_count}")
    return 0


if __name__ == "__main__":
    sys.exit(reset_m09_workspace())
