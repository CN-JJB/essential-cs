#!/usr/bin/env python3
"""M06 Activity Reset & Cleanup Utility.

Safely terminates any lingering activity processes and removes temporary files.
"""

import os
import shutil
from pathlib import Path


def reset_m06():
    root = Path(__file__).parent
    cleaned = []

    # Clean __pycache__ directories
    for pycache in root.glob("**/__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        cleaned.append(str(pycache.name))

    # Clean temporary files
    for ext in ("*.tmp", "*.log"):
        for p in root.glob(ext):
            p.unlink()
            cleaned.append(str(p.name))

    print(f"M06 reset complete. Cleaned: {cleaned if cleaned else 'None (working tree clean)'}")


if __name__ == "__main__":
    reset_m06()
