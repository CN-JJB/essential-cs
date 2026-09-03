#!/usr/bin/env python3
"""Cleanup and reset utility for M08 lab activities.

Removes temporary run directories, cache files, and generated artifacts.
"""

import shutil
import sys
from pathlib import Path


def reset_m08_workspace() -> int:
    current_dir = Path(__file__).parent.resolve()
    print(f"=== Resetting M08 Lab Workspace: {current_dir} ===")

    removed_count = 0

    # 1. Clean only course-scoped generated directories.
    # Never wildcard-delete arbitrary *.dat or *.tmp files a learner may have created.
    generated_prefixes = ("_run_m08_", "_test_m08_", "_m08_generated_")
    for item in current_dir.iterdir():
        if item.name.startswith(generated_prefixes):
            if item.is_dir():
                shutil.rmtree(item)
                print(f"  [x] Removed course directory: {item.name}")
            elif item.is_file() or item.is_symlink():
                item.unlink()
                print(f"  [x] Removed course file: {item.name}")
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
    sys.exit(reset_m08_workspace())
