#!/usr/bin/env python3
"""LAB-REQ-01 idempotent standalone reset.

The harness owns and verifies child-process/endpoint teardown while it still
knows the process handles and dynamically assigned ports. This standalone
reset only reports that LAB-REQ-01 creates no persistent course artifact that
requires deletion; it does not pretend to rediscover or verify unknown old
processes.
"""

from __future__ import annotations

import sys


def reset_lab_req_01() -> str:
    """Report the course-scoped no-persistent-artifact reset disposition."""
    return "CLEAN_NO_PERSISTENT_ARTIFACTS"


if __name__ == "__main__":
    result = reset_lab_req_01()
    print(f"LAB_REQ_01_RESET_OK: {result}")
    sys.exit(0)
