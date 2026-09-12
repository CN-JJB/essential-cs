"""The bounded loopback dependency service (P3/P6/P9).

This is a *real separate process* the Mini Cloud service depends on — the
"link indexer" that turns a saved bookmark into a short summary. It is small
on purpose: the point is not the indexing, it is that a dependency can be
slow, unavailable, or failing, and the caller must behave correctly.

It also exposes a control endpoint (``POST /control/fault``) so tests and the
P9 walkthrough can inject a fault deterministically instead of hoping for one.

Fault modes:

============  =========================================================
``ok``        normal behaviour
``unavailable``  returns HTTP 503 (simulates "dependency is down")
``slow``      sleeps past the caller's deadline (simulates a timeout)
``error``     returns HTTP 500 (simulates a buggy dependency)
============  =========================================================
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

FAULT_MODES = ("ok", "unavailable", "slow", "error")

#: How long ``slow`` mode sleeps. Comfortably beyond the default 1500 ms
#: application deadline so the caller's timeout path is genuinely exercised.
SLOW_DELAY_SECONDS = 3.0


def summarize(url: str, title: str) -> str:
    """Deterministic pseudo-summary so evidence is reproducible."""
    digest = hashlib.sha256(f"{url}\x00{title}".encode("utf-8")).hexdigest()[:12]
    host = ""
    if "://" in url:
        host = url.split("://", 1)[1].split("/", 1)[0]
    return f"indexed[{digest}] host={host or 'unknown'} title={title[:40]}"


class IndexerHandler(BaseHTTPRequestHandler):
    server_version = "MiniCloudIndexer/0.1"
    protocol_version = "HTTP/1.1"

    # -- helpers -----------------------------------------------------------
    def log_message(self, fmt, *args):  # noqa: A003 - silence default stderr spam
        return

    def handle_one_request(self):
        """A caller that gave up mid-request must not crash this dependency."""
        try:
            super().handle_one_request()
        except (ConnectionError, TimeoutError):
            self.close_connection = True

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}

    def _send(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @property
    def fault_mode(self) -> str:
        return self.server.fault_mode  # type: ignore[attr-defined]

    # -- routes ------------------------------------------------------------
    def do_GET(self):  # noqa: N802 - stdlib naming
        if self.path == "/health":
            self._send(200, {"status": "ok", "fault_mode": self.fault_mode})
        else:
            self._send(404, {"error": {"code": "not_found", "message": self.path}})

    def do_POST(self):  # noqa: N802 - stdlib naming
        if self.path == "/control/fault":
            body = self._read_json()
            mode = body.get("mode")
            if mode not in FAULT_MODES:
                self._send(400, {"error": {"code": "validation_error", "message": f"mode must be one of {FAULT_MODES}"}})
                return
            self.server.fault_mode = mode  # type: ignore[attr-defined]
            self._send(200, {"fault_mode": mode})
            return

        if self.path == "/index":
            mode = self.fault_mode
            if mode == "unavailable":
                self._send(503, {"error": {"code": "dependency_unavailable", "message": "indexer is down"}})
                return
            if mode == "error":
                self._send(500, {"error": {"code": "internal_error", "message": "indexer bug"}})
                return
            if mode == "slow":
                time.sleep(SLOW_DELAY_SECONDS)
            body = self._read_json()
            url = str(body.get("url") or "")
            title = str(body.get("title") or "")
            if not url:
                self._send(400, {"error": {"code": "validation_error", "message": "url is required"}})
                return
            self._send(200, {"summary": summarize(url, title), "provider": "mini-indexer"})
            return

        self._send(404, {"error": {"code": "not_found", "message": self.path}})


class IndexerServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, addr, handler, fault_mode: str = "ok") -> None:
        super().__init__(addr, handler)
        self.fault_mode = fault_mode


def create_server(host: str = "127.0.0.1", port: int = 0, fault_mode: str = "ok") -> IndexerServer:
    return IndexerServer((host, port), IndexerHandler, fault_mode=fault_mode)


def serve_in_thread(host: str = "127.0.0.1", fault_mode: str = "ok"):
    """Start the indexer in a background thread; return ``(server, thread, url)``."""
    server = create_server(host, 0, fault_mode)
    thread = threading.Thread(
        target=lambda: server.serve_forever(poll_interval=0.05), name="minicloud-indexer", daemon=True
    )
    thread.start()
    host, port = server.server_address[0], server.server_address[1]
    return server, thread, f"http://{host}:{port}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mini Cloud loopback indexer dependency")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--port-file", default=None, help="write the bound port here")
    parser.add_argument("--fault", default="ok", choices=FAULT_MODES)
    args = parser.parse_args(argv)

    server = create_server(args.host, args.port, args.fault)
    bound_port = server.server_address[1]
    if args.port_file:
        parent = os.path.dirname(os.path.abspath(args.port_file))
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(args.port_file, "w", encoding="utf-8") as handle:
            handle.write(str(bound_port))
    print(f"indexer listening on http://{args.host}:{bound_port} fault={args.fault}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
