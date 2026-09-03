#!/usr/bin/env python3
"""M05 Activity Reset & Cleanup Script.

Removes any generated build artifacts, object files, and __pycache__ directories.
"""

import shutil
from pathlib import Path


def reset_m05():
    root = Path(__file__).parent
    cleaned = []

    # Clean compiled C object files and executables
    for ext in ("*.o", "*.obj", "*.exe"):
        for p in root.glob(ext):
            p.unlink()
            cleaned.append(str(p.name))

    # Clean __pycache__ directories
    for pycache in root.glob("**/__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        cleaned.append(str(pycache.name))

    print(f"M05 reset complete. Cleaned: {cleaned if cleaned else 'None (working tree clean)'}")


if __name__ == "__main__":
    reset_m05()
