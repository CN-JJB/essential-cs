"""P9 — the integrated system walkthrough.

This is the checkpoint that separates "nine demos" from "one system". A single
scripted run drives a real HTTP request through every layer and proves the chain
holds end to end:

    request → application → durable state → dependency → observability
            → failure → recovery

It also demonstrates the P3 lesson the hard way: the client is given a deadline
so short that it gives up on a write, and the walkthrough then *reconciles* —
showing that the item was committed anyway. A timeout is not a rollback.

Everything runs on loopback against a temporary database. The result is a
structured evidence packet, not a wall of prose.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time

from . import httpd, indexer
from .client import MiniCloudClient
from .config import Config
from .dependency import IndexerClient
from .observability import Observability
from .service import MiniCloudService
from .store import Store

PASSWORD = "walkthrough-password"
ALICE = "alice"
BOB = "bob"


def _set_fault(base_url: str, mode: str) -> dict:
    import urllib.request

    request = urllib.request.Request(
        f"{base_url}/control/fault",
        data=json.dumps({"mode": mode}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read())


class _Recorder:
    def __init__(self) -> None:
        self.checkpoints: list[dict] = []

    def check(self, name: str, ok: bool, **detail) -> bool:
        self.checkpoints.append({"step": name, "ok": bool(ok), **detail})
        return bool(ok)


def run_walkthrough(*, workdir: str | None = None, log_path: str | None = None) -> dict:
    own_workdir = workdir is None
    workdir = workdir or tempfile.mkdtemp(prefix="minicloud-walkthrough-")
    log_path = log_path or os.path.join(workdir, "minicloud.log")
    db_path = os.path.join(workdir, "minicloud.db")
    rec = _Recorder()

    iserver = None
    server = None
    try:
        # ---- P7: materialize the environment from configuration only -------
        iserver, _ithread, indexer_url = indexer.serve_in_thread(fault_mode="ok")
        cfg = Config.from_env(
            {
                "MINICLOUD_DB_PATH": db_path,
                "MINICLOUD_PBKDF2_ITERATIONS": "10000",
                "MINICLOUD_INDEXER_URL": indexer_url,
                "MINICLOUD_DEP_TIMEOUT_MS": "1500",
                "MINICLOUD_DEP_MAX_ATTEMPTS": "2",
                "MINICLOUD_LOG_PATH": log_path,
            }
        )
        obs = Observability(log_path=log_path)
        store = Store(cfg.db_path)
        dep = IndexerClient(
            cfg.indexer_url,
            timeout_ms=cfg.dep_timeout_ms,
            max_attempts=cfg.dep_max_attempts,
            observability=obs,
        )
        service = MiniCloudService(store=store, config=cfg, observability=obs, dependency=dep)
        service.initialize()

        # ---- P0/P1: the service is reachable through a real boundary -------
        server, _thread, base = httpd.serve_in_thread(service)
        client = MiniCloudClient(base, timeout_ms=3000)
        health = client.health()
        rec.check(
            "P0/P1 health over HTTP",
            health.status == 200 and health.body.get("status") == "ok",
            status=health.status,
            schema_version=health.body.get("schema_version") if health.body else None,
        )

        # ---- P2: identity and authorization ---------------------------------
        assert client.create_user(ALICE, PASSWORD).status == 201
        assert client.create_user(BOB, PASSWORD).status == 201
        alice = client.login(ALICE, PASSWORD).body["token"]
        bob = client.login(BOB, PASSWORD).body["token"]
        rec.check("P2 login issues sessions", bool(alice) and bool(bob))

        created = client.create_item(alice, kind="note", title="shopping list", body="milk")
        item_id = created.body["item_id"]
        rec.check("P0 create + read back", client.get_item(alice, item_id).body["title"] == "shopping list")
        listed = client.list_items(alice)
        rec.check("P0 list own items", listed.body["count"] == 1, count=listed.body["count"])

        # ---- P1/P2: malformed input is rejected at the boundary -------------
        bad = client.request("POST", "/v1/items", body={"kind": "note"}, token=alice)
        rec.check(
            "P1 malformed request rejected",
            bad.status == 400 and bad.body["error"]["code"] == "validation_error",
            status=bad.status,
        )

        # ---- P2: no existence leak ------------------------------------------
        peek = client.get_item(bob, item_id)
        rec.check(
            "P2 cross-user read denied without leaking existence",
            peek.status == 404 and peek.body["error"]["code"] == "not_found",
            status=peek.status,
        )

        client.share_item(alice, item_id, BOB)
        shared_read = client.get_item(bob, item_id)
        rec.check("P2 explicit share grants read", shared_read.status == 200 and not shared_read.body["is_owner"])
        client.revoke_share(alice, item_id, BOB)
        after_revoke = client.get_item(bob, item_id)
        rec.check("P2 revocation removes access", after_revoke.status == 404)

        # ---- P3/P8: correlated request across layers ------------------------
        correlated = obs.new_request_id()
        bookmark = client.request(
            "POST",
            "/v1/items",
            body={"kind": "bookmark", "title": "Python", "url": "https://python.org"},
            token=alice,
            request_id=correlated,
        )
        rec.check(
            "P3/P9 dependency indexed a bookmark",
            bookmark.status == 201 and bookmark.body["index"]["status"] == "ready",
            index=bookmark.body["index"],
        )

        # ---- P6/P9: dependency down; the item is still durable --------------
        _set_fault(indexer_url, "unavailable")
        degraded = client.create_item(alice, kind="bookmark", title="Rust", url="https://rust-lang.org")
        degraded_id = degraded.body["item_id"]
        rec.check(
            "P9 dependency failure degrades only the index",
            degraded.status == 201 and degraded.body["index"]["status"] == "pending",
            index=degraded.body["index"],
        )
        rec.check(
            "P9 degraded item is still readable (state survived dependency failure)",
            client.get_item(alice, degraded_id).status == 200,
        )

        # ---- P3: a client timeout is NOT proof the write did not happen -----
        _set_fault(indexer_url, "slow")
        impatient = MiniCloudClient(base, timeout_ms=200)
        ambiguous = impatient.create_item(
            alice, kind="bookmark", title="Go", url="https://go.dev", idempotency_key="walkthrough-go"
        )
        rec.check(
            "P3 client timeout reported as ambiguous (not failure)",
            ambiguous.status is None and ambiguous.ambiguous,
            ambiguous=ambiguous.ambiguous,
            error=ambiguous.error,
        )
        reconciled = _poll_for_title(client, alice, "Go", timeout_s=8.0)
        rec.check(
            "P3 reconciliation: the timed-out write DID commit",
            reconciled is not None,
            item_id=reconciled["item_id"] if reconciled else None,
        )
        timed_out_id = reconciled["item_id"] if reconciled else None

        # ---- P3/P5: idempotent replay of the same key -----------------------
        if timed_out_id is not None:
            replay = client.create_item(
                alice, kind="bookmark", title="Go", url="https://go.dev", idempotency_key="walkthrough-go"
            )
            rec.check(
                "P3 idempotency key prevents a duplicate effect",
                replay.status == 201 and replay.body.get("idempotent_replay") is True,
            )

        # ---- P9 recovery: dependency returns, index completes ---------------
        _set_fault(indexer_url, "ok")
        recovered = client.reindex_item(alice, degraded_id)
        rec.check(
            "P9 recovery completes the pending index",
            recovered.status == 200 and recovered.body["index"]["status"] == "ready",
            index=recovered.body["index"],
        )

        # ---- P5: concurrent writers cannot both win --------------------------
        current = client.get_item(alice, item_id).body
        first = client.update_item(alice, item_id, expected_version=current["version"], title="A")
        second = client.update_item(alice, item_id, expected_version=current["version"], title="B")
        rec.check(
            "P5 optimistic concurrency rejects the stale writer",
            first.status == 200 and second.status == 409,
            first=first.status,
            second=second.status,
        )

        # ---- P6: durable state survives a service restart --------------------
        server.shutdown()
        server.server_close()
        store2 = Store(cfg.db_path)
        service2 = MiniCloudService(store=store2, config=cfg, observability=obs, dependency=dep)
        service2.initialize()
        server, _thread, base = httpd.serve_in_thread(service2)
        client = MiniCloudClient(base, timeout_ms=3000)
        alice2 = client.login(ALICE, PASSWORD).body["token"]
        survived = client.get_item(alice2, item_id)
        rec.check(
            "P6 durable state survives a full service restart",
            survived.status == 200 and survived.body["title"] == "A",
            title=survived.body.get("title") if survived.body else None,
        )

        # ---- P8: observability evidence --------------------------------------
        correlation = _correlate(log_path, correlated)
        rec.check(
            "P8 one request_id correlates HTTP → service → dependency",
            correlation["correlated"],
            events=correlation["events"],
        )
        metrics = service2.metrics_snapshot()
        rec.check(
            "P8 metrics recorded with bounded labels",
            metrics["counters"].get("requests_total", 0) > 0
            and "item_id" in metrics["labels"]["excluded"],
            counters=metrics["counters"],
        )
        redaction_ok = _redaction_ok(log_path)
        rec.check("P8 secrets redacted from logs", redaction_ok)

        # ---- shutdown ---------------------------------------------------------
        server.shutdown()
        server.server_close()
        server = None
        iserver.shutdown()
        iserver.server_close()
        iserver = None
        import threading as _threading

        live = [t.name for t in _threading.enumerate() if t.name in ("minicloud-http", "minicloud-indexer") and t.is_alive()]
        rec.check("clean shutdown (no live server or indexer thread)", not live, live_threads=live)

        disposition = "PASS" if all(c["ok"] for c in rec.checkpoints) else "FAIL"
        return {
            "disposition": disposition,
            "checkpoints": rec.checkpoints,
            "chain": "request → application → state → dependency → observability → failure → recovery",
            "evidence": {
                "db_path": db_path,
                "log_path": log_path,
                "indexer_url": indexer_url,
            },
            "inference_limits": [
                "loopback only; this is a local teaching boundary, not internet behaviour",
                "single-node SQLite; not a distributed or multi-region claim",
                "the timeout demonstration uses an injected slow dependency, not real packet loss",
            ],
        }
    finally:
        if server is not None:
            try:
                server.shutdown()
                server.server_close()
            except Exception:  # noqa: BLE001
                pass
        if iserver is not None:
            try:
                iserver.shutdown()
                iserver.server_close()
            except Exception:  # noqa: BLE001
                pass
        if own_workdir:
            shutil.rmtree(workdir, ignore_errors=True)


def _poll_for_title(client: MiniCloudClient, token: str, title: str, *, timeout_s: float) -> dict | None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        listing = client.list_items(token, limit=200)
        if listing.ok and listing.body:
            for item in listing.body["items"]:
                if item["title"] == title:
                    return item
        time.sleep(0.2)
    return None


def _correlate(log_path: str, request_id: str) -> dict:
    events: list[str] = []
    if not os.path.exists(log_path):
        return {"correlated": False, "events": events}
    with open(log_path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("request_id") == request_id:
                events.append(record.get("event", "?"))
    correlated = (
        "http.request" in events
        and "item.created" in events
        and any(e.startswith("dependency.index") for e in events)
    )
    return {"correlated": correlated, "events": sorted(set(events))}


def _redaction_ok(log_path: str) -> bool:
    if not os.path.exists(log_path):
        return False
    with open(log_path, encoding="utf-8") as handle:
        blob = handle.read()
    # The walkthrough password must never appear in the log.
    return PASSWORD not in blob
