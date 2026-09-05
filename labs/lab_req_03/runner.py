#!/usr/bin/env python3
"""
CLI runner for LAB-REQ-03: POSIX Threads Race, Rendezvous & Progress Boundaries.
Supports interactive terminal reporting and machine-readable JSON output.
"""

import argparse
import json
import sys

try:
    from .harness import ConcurrencyLabHarness
except ImportError:
    from harness import ConcurrencyLabHarness


def main():
    parser = argparse.ArgumentParser(description="LAB-REQ-03 Concurrency Lab Runner")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON report")
    parser.add_argument("--timeout", type=float, default=2.0, help="Deadlock watchdog timeout parameter in seconds")
    parser.add_argument("--iterations", type=int, default=10000, help="Iteration count for mutex and natural scheduler tests")
    args = parser.parse_args()

    harness = ConcurrencyLabHarness()
    report = harness.run_all(verbose=not args.json)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0 if report.get("overall_passed") else 1


if __name__ == "__main__":
    sys.exit(main())
