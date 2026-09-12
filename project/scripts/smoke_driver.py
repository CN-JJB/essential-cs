#!/usr/bin/env python3
"""Smoke driver: real HTTP assertions against a *running* Mini Cloud service.

The shell smoke script owns process lifecycle and cleanup; this driver owns the
semantic assertions. It talks to the service over loopback exactly as a learner
would, and it writes machine-readable evidence plus explicit ``SMOKE_EVIDENCE``
lines that the shell script re-checks (so a silent no-op cannot look green).

Exit code is 0 only if every assertion passed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.dirname(_HERE)
if _PROJECT_DIR not in sys.path:
    sys.path.insert(0, _PROJECT_DIR)

from minicloud.client import MiniCloudClient  # noqa: E402

PASSWORD = "smoke-password"
ALICE = "smokealice"
BOB = "smokebob"


def _set_fault(indexer_url: str, mode: str) -> None:
    import urllib.request

    request = urllib.request.Request(
        f"{indexer_url}/control/fault",
        data=json.dumps({"mode": mode}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5):
        pass


class Checks:
    def __init__(self) -> None:
        self.results: list[dict] = []

    def check(self, name: str, ok: bool, **detail) -> None:
        self.results.append({"name": name, "ok": bool(ok), **detail})
        print(f"SMOKE_EVIDENCE: {'PASS' if ok else 'FAIL'} {name}", flush=True)

    @property
    def ok(self) -> bool:
        return all(r["ok"] for r in self.results)


def full_run(args) -> int:
    checks = Checks()
    client = MiniCloudClient(args.base_url, timeout_ms=5000)

    health = client.health()
    checks.check("health", health.status == 200 and health.body.get("status") == "ok")

    # Idempotent bootstrap so re-running against an existing database is fine.
    for username in (ALICE, BOB):
        created = client.create_user(username, PASSWORD)
        checks.check(f"user:{username}", created.status in (201, 400))

    alice = client.login(ALICE, PASSWORD)
    bob = client.login(BOB, PASSWORD)
    checks.check("login", alice.status == 201 and bob.status == 201)
    if not (alice.status == 201 and bob.status == 201):
        return _finish(checks, args, {})
    alice_token = alice.body["token"]
    bob_token = bob.body["token"]

    note = client.create_item(alice_token, kind="note", title="smoke-note", body="payload")
    checks.check("create", note.status == 201)
    item_id = note.body["item_id"] if note.status == 201 else None

    got = client.get_item(alice_token, item_id) if item_id else None
    checks.check("read-back", bool(got) and got.body["title"] == "smoke-note")

    listed = client.list_items(alice_token)
    checks.check("list", listed.status == 200 and listed.body["count"] >= 1)

    bad = client.request("POST", "/v1/items", body={"kind": "note"}, token=alice_token)
    checks.check("invalid-request-rejected", bad.status == 400)

    denied = client.get_item(bob_token, item_id) if item_id else None
    checks.check("cross-user-denied", bool(denied) and denied.status == 404)

    share = client.share_item(alice_token, item_id, BOB) if item_id else None
    checks.check("share", bool(share) and share.status == 201)
    shared = client.get_item(bob_token, item_id) if item_id else None
    checks.check("shared-read", bool(shared) and shared.status == 200)
    revoke = client.revoke_share(alice_token, item_id, BOB) if item_id else None
    checks.check("revoke", bool(revoke) and revoke.status == 200)
    after = client.get_item(bob_token, item_id) if item_id else None
    checks.check("revoked-denied", bool(after) and after.status == 404)

    bookmark = client.create_item(
        alice_token, kind="bookmark", title="smoke-bookmark", url="https://example.org"
    )
    checks.check(
        "dependency-indexed",
        bookmark.status == 201 and bookmark.body["index"]["status"] == "ready",
    )
    bookmark_id = bookmark.body["item_id"] if bookmark.status == 201 else None

    _set_fault(args.indexer_url, "unavailable")
    degraded = client.create_item(
        alice_token, kind="bookmark", title="smoke-degraded", url="https://example.net"
    )
    checks.check(
        "dependency-failure-degrades-index",
        degraded.status == 201 and degraded.body["index"]["status"] == "pending",
    )
    degraded_id = degraded.body["item_id"] if degraded.status == 201 else None
    durable = client.get_item(alice_token, degraded_id) if degraded_id else None
    checks.check("degraded-item-durable", bool(durable) and durable.status == 200)

    _set_fault(args.indexer_url, "ok")
    recovered = client.reindex_item(alice_token, degraded_id) if degraded_id else None
    checks.check(
        "recovery-reindex",
        bool(recovered) and recovered.status == 200 and recovered.body["index"]["status"] == "ready",
    )

    metrics = client.request("GET", "/metrics")
    checks.check(
        "observability-metrics",
        metrics.status == 200 and metrics.body["counters"].get("requests_total", 0) > 0,
    )

    return _finish(
        checks,
        args,
        {
            "item_id": item_id,
            "bookmark_id": bookmark_id,
            "degraded_id": degraded_id,
            "note_title": "smoke-note",
        },
    )


def verify_item(args) -> int:
    """Persistence check used by the shell script after a service restart."""
    checks = Checks()
    client = MiniCloudClient(args.base_url, timeout_ms=5000)
    login = client.login(ALICE, PASSWORD)
    checks.check("restart-login", login.status == 201)
    if login.status != 201:
        return _finish(checks, args, {})
    fetched = client.get_item(login.body["token"], args.verify_item)
    checks.check(
        "restart-persistence",
        fetched.status == 200 and fetched.body["title"] == args.expect_title,
        expected_title=args.expect_title,
        actual_title=fetched.body.get("title") if fetched.body else None,
    )
    return _finish(checks, args, {})


def _finish(checks: Checks, args, extra: dict) -> int:
    payload = {
        "result": "PASS" if checks.ok else "FAIL",
        "checks": checks.results,
        "failed": [r["name"] for r in checks.results if not r["ok"]],
        **extra,
    }
    if args.json_out:
        parent = os.path.dirname(os.path.abspath(args.json_out))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
    return 0 if checks.ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mini Cloud smoke driver")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--indexer-url", required=True)
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--verify-item", default=None, help="run the restart-persistence check instead")
    parser.add_argument("--expect-title", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.verify_item:
        return verify_item(args)
    return full_run(args)


if __name__ == "__main__":
    sys.exit(main())
