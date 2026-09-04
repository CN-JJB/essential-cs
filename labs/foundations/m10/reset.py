#!/usr/bin/env python3
"""
M10 Cleanup and Reset Utility.

Provides idempotent, course-scoped cleanup of M10 activity artifacts and endpoints.
Adheres strictly to Essential CS invariants:
- Harness owns process/socket handles.
- Cooperative and platform-appropriate termination.
- Post-reset checks confirm course endpoints are not serving without requiring exact refusal strings.
- Never wildcard-deletes learner files or unrelated temp data.
"""

import argparse
import json
import socket
import sys


def probe_endpoint_after_close(host="127.0.0.1", port=0, timeout_s=0.5):
    """
    Probe one previously known course endpoint after its owner has closed it.

    The acceptance invariant is semantic: a new TCP connection must not be
    established to the old course endpoint. The raw connect_ex() result is
    recorded as host evidence; no fixed errno, exception class, or latency is
    required.
    """
    if port == 0:
        return {
            "host": host,
            "port": port,
            "connection_established": False,
            "connect_ex_result": None,
            "disposition": "NO_ENDPOINT_PROVIDED",
        }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout_s)
    try:
        result = sock.connect_ex((host, port))
        established = result == 0
        return {
            "host": host,
            "port": port,
            "connection_established": established,
            "connect_ex_result": result,
            "disposition": (
                "UNEXPECTED_CONNECTION_ESTABLISHED"
                if established
                else "OLD_COURSE_ENDPOINT_NOT_ACCEPTING"
            ),
        }
    except Exception as exc:
        return {
            "host": host,
            "port": port,
            "connection_established": False,
            "connect_ex_result": None,
            "disposition": "PROBE_ERROR_NO_CONNECTION_ESTABLISHED",
            "exception_type": type(exc).__name__,
            "details": str(exc),
        }
    finally:
        sock.close()


def verify_endpoint_not_serving(host="127.0.0.1", port=0):
    """Compatibility wrapper returning only the semantic connection result."""
    return not probe_endpoint_after_close(host, port)["connection_established"]


def run_reset():
    """
    Execute idempotent course-scoped reset.

    M10 owns no persistent files, daemons, or externally managed listeners:
    each activity closes the sockets/threads it creates before returning.
    A standalone reset therefore has no unknown endpoint it can truthfully
    verify. Endpoint-specific teardown is verified by the activity/test while
    the assigned port is still known.
    """
    return {
        "status": "CLEAN_NO_PERSISTENT_ARTIFACTS",
        "actions_taken": [
            "No persistent M10 files or background services require deletion",
            "Endpoint-specific close probes run in the owning activity/test",
        ],
        "idempotent": True,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="M10 Reset Utility")
    parser.add_argument("--json", action="store_true", help="Output reset result in JSON format")
    args = parser.parse_args()

    result = run_reset()

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print("=" * 60)
    print(" M10 Reset & Teardown Verification")
    print("=" * 60)
    print(f" Status:        {result['status']}")
    print(f" Idempotent:    {result['idempotent']}")
    for action in result["actions_taken"]:
        print(f"  - {action}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
