#!/usr/bin/env python3
"""
M12 Cleanup and Reset Utility.

Reports the idempotent no-persistent-artifact disposition for M12 lesson activities.

Listener/thread teardown is verified by each owning activity/test while it still
has the actual handles. This standalone command does not claim to rediscover or
probe arbitrary old endpoints.
"""

import argparse
import json
import sys


def run_reset():
    """
    M12 activities own no persistent daemon or learner artifact.

    Listener/thread lifecycle is verified by the owning activity/test while the
    actual endpoint and worker handle are still known. A standalone reset
    cannot truthfully rediscover arbitrary old ports or prove process cleanup.
    """
    return {
        "status": "CLEAN_NO_PERSISTENT_ARTIFACTS",
        "actions_taken": [
            "No persistent M12 course daemon or learner artifact requires deletion",
            "Endpoint/thread teardown is verified by the owning activity/test",
        ],
        "idempotent": True,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="M12 Reset Utility")
    parser.add_argument("--json", action="store_true", help="Output reset result in JSON format")
    args = parser.parse_args()

    result = run_reset()

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("=" * 60)
    print(" M12 Reset & Teardown Verification")
    print("=" * 60)
    print(f" Status:        {result['status']}")
    print(f" Idempotent:    {result['idempotent']}")
    for action in result["actions_taken"]:
        print(f"  - {action}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
