"""Minimal HTTP adapter (P1).

Standard library only: ``http.server`` plus a small explicit router. There is
deliberately no web framework. The adapter's whole job is to translate HTTP
bytes into service-core calls and back, and to make the *boundary* behaviour
visible: request IDs, bounded body size, honest status codes, and a single
error shape.

Every response carries ``X-Request-ID`` so a learner can correlate the HTTP
exchange with the structured log lines and the dependency call.
"""

from __future__ import annotations

import json
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .errors import (
    MiniCloudError,
    PayloadTooLargeError,
    ValidationError,
)
from .observability import Observability

#: (method, compiled pattern, route template, handler name)
_ROUTES = [
    ("GET", re.compile(r"^/health$"), "/health", "health"),
    ("GET", re.compile(r"^/metrics$"), "/metrics", "metrics"),
    ("POST", re.compile(r"^/v1/users$"), "/v1/users", "create_user"),
    ("POST", re.compile(r"^/v1/sessions$"), "/v1/sessions", "login"),
    ("DELETE", re.compile(r"^/v1/sessions$"), "/v1/sessions", "logout"),
    ("GET", re.compile(r"^/v1/items$"), "/v1/items", "list_items"),
    ("POST", re.compile(r"^/v1/items$"), "/v1/items", "create_item"),
    ("GET", re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})$"), "/v1/items/{id}", "get_item"),
    ("PATCH", re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})$"), "/v1/items/{id}", "update_item"),
    ("DELETE", re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})$"), "/v1/items/{id}", "delete_item"),
    ("GET", re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})/shares$"), "/v1/items/{id}/shares", "list_shares"),
    ("POST", re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})/shares$"), "/v1/items/{id}/shares", "share_item"),
    (
        "DELETE",
        re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})/shares/(?P<username>[A-Za-z0-9_-]{2,64})$"),
        "/v1/items/{id}/shares/{username}",
        "revoke_share",
    ),
    ("POST", re.compile(r"^/v1/items/(?P<item_id>[0-9a-f]{32})/reindex$"), "/v1/items/{id}/reindex", "reindex_item"),
]


class MiniCloudHTTPRequestHandler(BaseHTTPRequestHandler):
    server_version = "MiniCloud/0.1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # noqa: A003 - default stderr logging is replaced by structured logs
        return

    def handle_one_request(self):
        """Safety net: a dropped client must not print a traceback or crash the worker."""
        try:
            super().handle_one_request()
        except (ConnectionError, TimeoutError):
            self.close_connection = True

    # -- infrastructure ----------------------------------------------------
    @property
    def service(self):
        return self.server.service  # type: ignore[attr-defined]

    @property
    def obs(self) -> Observability:
        return self.server.obs  # type: ignore[attr-defined]

    @property
    def max_body(self) -> int:
        return self.server.max_body  # type: ignore[attr-defined]

    def _read_body(self) -> dict:
        length_header = self.headers.get("Content-Length")
        if length_header is None:
            return {}
        try:
            length = int(length_header)
        except ValueError as exc:
            raise ValidationError("invalid Content-Length") from exc
        if length > self.max_body:
            raise PayloadTooLargeError(
                f"request body exceeds {self.max_body} bytes", details={"declared_bytes": length}
            )
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValidationError("request body must be valid UTF-8 JSON") from exc
        if not isinstance(parsed, dict):
            raise ValidationError("request body must be a JSON object")
        return parsed

    def _send(self, status: int, payload: dict | None, request_id: str) -> None:
        body = b"" if payload is None else json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        if body:
            self.wfile.write(body)

    @staticmethod
    def _bearer_token(headers) -> str | None:
        raw = headers.get("Authorization")
        if not raw:
            return None
        parts = raw.split(None, 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        return parts[1].strip()

    # -- dispatch ----------------------------------------------------------
    def _handle(self, method: str) -> None:
        started = time.perf_counter()
        request_id = self.headers.get("X-Request-ID") or self.obs.new_request_id()
        matched_route = "unmatched"
        status = 500
        try:
            path = self.path.split("?", 1)[0]
            for route_method, pattern, template, name in _ROUTES:
                match = pattern.match(path)
                if not match:
                    continue
                if route_method != method:
                    continue
                matched_route = template
                status, payload = self._invoke(name, match, request_id)
                self._send(status, payload, request_id)
                return
            # Distinguish "wrong method" from "unknown path" honestly.
            if any(p.match(path) for _, p, _, _ in _ROUTES):
                status = 405
                self._send(405, {"error": {"code": "method_not_allowed", "message": f"{method} {path}"}}, request_id)
            else:
                status = 404
                self._send(404, {"error": {"code": "not_found", "message": path}}, request_id)
        except (ConnectionError, TimeoutError) as exc:
            # The caller went away mid-response (reset/abort/timeout). This is a
            # client-side event, not a server fault: record it honestly and do
            # not attempt to send a 5xx down a dead socket.
            status = 499
            self.obs.log(
                "http.client_disconnected", request_id=request_id, level="warning", error=type(exc).__name__
            )
        except MiniCloudError as exc:
            status = exc.http_status
            self._send(status, exc.to_payload(request_id), request_id)
        except Exception as exc:  # noqa: BLE001 - boundary must never leak a stack trace
            status = 500
            self.obs.log(
                "http.unhandled_error", request_id=request_id, level="error", error=type(exc).__name__
            )
            self._send(500, {"error": {"code": "internal_error", "message": "internal error", "request_id": request_id}}, request_id)
        finally:
            duration_ms = (time.perf_counter() - started) * 1000.0
            self.obs.observe_request(matched_route, status, duration_ms)
            self.obs.log(
                "http.request",
                request_id=request_id,
                method=method,
                route=matched_route,
                status=status,
                duration_ms=round(duration_ms, 3),
            )

    def _invoke(self, name: str, match: re.Match, request_id: str) -> tuple[int, dict]:
        service = self.service
        groups = match.groupdict()
        token = self._bearer_token(self.headers)

        if name == "health":
            return 200, service.health()
        if name == "metrics":
            return 200, service.metrics_snapshot()
        if name == "create_user":
            body = self._read_body()
            return 201, service.create_user(body.get("username"), body.get("password"), request_id=request_id)
        if name == "login":
            body = self._read_body()
            return 201, service.login(body.get("username"), body.get("password"), request_id=request_id)
        if name == "logout":
            return 200, service.logout(token or "", request_id=request_id)

        identity = service.authenticate(token)
        if name == "list_items":
            body = self._read_body()
            limit = body.get("limit")
            return 200, service.list_items(identity, limit=limit, request_id=request_id)
        if name == "create_item":
            body = self._read_body()
            idem = self.headers.get("Idempotency-Key")
            return 201, service.create_item(
                identity,
                kind=body.get("kind", "note"),
                title=body.get("title", ""),
                body=body.get("body", ""),
                url=body.get("url"),
                visibility=body.get("visibility", "private"),
                idempotency_key=idem,
                request_id=request_id,
            )
        if name == "get_item":
            return 200, service.get_item(identity, groups["item_id"], request_id=request_id)
        if name == "update_item":
            body = self._read_body()
            expected = body.pop("expected_version", None)
            return 200, service.update_item(
                identity, groups["item_id"], expected_version=expected, fields=body, request_id=request_id
            )
        if name == "delete_item":
            service.delete_item(identity, groups["item_id"], request_id=request_id)
            return 204, {}
        if name == "list_shares":
            return 200, service.list_shares(identity, groups["item_id"], request_id=request_id)
        if name == "share_item":
            body = self._read_body()
            return 201, service.share_item(
                identity, groups["item_id"], body.get("grantee", ""), request_id=request_id
            )
        if name == "revoke_share":
            return 200, service.revoke_share(
                identity, groups["item_id"], groups["username"], request_id=request_id
            )
        if name == "reindex_item":
            return 200, service.reindex_item(identity, groups["item_id"], request_id=request_id)
        raise AssertionError(f"unrouted handler {name}")  # pragma: no cover

    # -- verbs -------------------------------------------------------------
    def do_GET(self):  # noqa: N802
        self._handle("GET")

    def do_POST(self):  # noqa: N802
        self._handle("POST")

    def do_PATCH(self):  # noqa: N802
        self._handle("PATCH")

    def do_DELETE(self):  # noqa: N802
        self._handle("DELETE")


class MiniCloudHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, addr, handler, service, obs: Observability, max_body: int) -> None:
        super().__init__(addr, handler)
        self.service = service
        self.obs = obs
        self.max_body = max_body


def create_server(service, *, host: str = "127.0.0.1", port: int = 0) -> MiniCloudHTTPServer:
    obs = service.obs
    return MiniCloudHTTPServer(
        (host, port), MiniCloudHTTPRequestHandler, service, obs, service.config.max_body_bytes
    )


def serve_in_thread(service, *, host: str = "127.0.0.1", port: int = 0):
    server = create_server(service, host=host, port=port)
    # A short poll interval keeps test/teardown latency low; it does not change
    # request handling, which is already per-connection threaded.
    thread = threading.Thread(
        target=lambda: server.serve_forever(poll_interval=0.05), name="minicloud-http", daemon=True
    )
    thread.start()
    bound_host, bound_port = server.server_address[0], server.server_address[1]
    return server, thread, f"http://{bound_host}:{bound_port}"
