#!/usr/bin/env python3
"""
CLI Runner for LAB-REQ-05: SQLite Transactions, Isolation & Recovery Boundary.
Executes the five canonical checkpoints and outputs structured or JSON evidence.
"""

import argparse
import json
import sys

try:
    from .harness import TransactionLabHarness
except ImportError:
    from harness import TransactionLabHarness


def main():
    parser = argparse.ArgumentParser(description="Run LAB-REQ-05 verification harness")
    parser.add_argument("--json", action="store_true", help="Output evidence in machine-readable JSON format")
    args = parser.parse_args()

    harness = TransactionLabHarness()
    results = harness.run_all(verbose=not args.json)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))

    sys.exit(0 if results["overall_passed"] else 1)


if __name__ == "__main__":
    main()
