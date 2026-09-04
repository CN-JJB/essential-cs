#!/usr/bin/env python3
"""LAB-REQ-01 bounded HTTP/1.1 intermediary.

Course contract:
- localhost only, dynamic port 0;
- GET/HEAD only;
- parse Connection options and remove nominated connection-specific fields;
- append a truthful Via entry using the protocol actually received on each hop;
- map the course-owned upstream connect failure to 502;
- never act as an open/public proxy.
"""

from __future__ import annotations

import argparse
import http.client
import json
from email.message import Message
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Iterable

# Fields this bounded intermediary always consumes rather than blindly forwarding.
# This combines current/legacy connection-control fields with proxy-only
# authentication fields that the course reverse-proxy fixture refuses to relay.
# Fields named dynamically by Connection are handled separately below.
COURSE_ALWAYS_REMOVE_FIELDS = {
    "connection",
    "proxy-connection",  # legacy/non-standard but common enough to reject here
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "transfer-encoding",
    "upgrade",
}


def _connection_tokens_from_values(values: Iterable[str]) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        for item in value.split(","):
            token = item.strip().lower()
            if token:
                tokens.add(token)
    return tokens


def _request_connection_tokens(headers: Message) -> set[str]:
    return _connection_tokens_from_values(headers.get_all("Connection", []) or [])


def _response_connection_tokens(headers: list[tuple[str, str]]) -> set[str]:
    return _connection_tokens_from_values(
        value for name, value in headers if name.lower() == "connection"
    )


def _remove_for_forwarding(name: str, connection_tokens: set[str]) -> bool:
    lower = name.lower()
    return lower in COURSE_ALWAYS_REMOVE_FIELDS or lower in connection_tokens


def _http_version_token(version: str | int) -> str:
    """Return the Via received-protocol token for the versions this lab supports."""
    if isinstance(version, int):
        if version == 11:
            return "1.1"
        if version == 10:
            return "1.0"
        return f"unknown-{version}"

    text = version.upper()
    if text.startswith("HTTP/"):
        return text.split("/", 1)[1]
    return text


def _append_via(existing: str | None, received_protocol: str) -> str:
    course_entry = f"{received_protocol} essential-cs-intermediary"
    return f"{existing}, {course_entry}" if existing else course_entry


def make_proxy_handler(origin_host: str, origin_port: int):
    class IntermediaryRequestHandler(BaseHTTPRequestHandler):
        """Forward the bounded course GET/HEAD subset to one configured origin."""

        protocol_version = "HTTP/1.1"

        def log_message(self, format: str, *args: object) -> None:
            pass

        def _send_course_error(self, status: int, payload: dict[str, object]) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header(
                "Via",
                _append_via(None, _http_version_token(self.request_version)),
            )
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _method_not_allowed(self) -> None:
            body = json.dumps(
                {
                    "error": "Method Not Allowed",
                    "allowed": ["GET", "HEAD"],
                    "course_scope": "LAB-REQ-01 bounded intermediary",
                }
            ).encode("utf-8")
            self.send_response(405)
            self.send_header("Allow", "GET, HEAD")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)

        def _forward_request(self) -> None:
            request_connection_tokens = _request_connection_tokens(self.headers)

            upstream_headers: dict[str, str] = {}
            for name, value in self.headers.items():
                lower = name.lower()
                if lower == "host":
                    continue
                if _remove_for_forwarding(name, request_connection_tokens):
                    continue
                upstream_headers[name] = value

            upstream_headers["Host"] = f"{origin_host}:{origin_port}"
            upstream_headers["Via"] = _append_via(
                self.headers.get("Via"),
                _http_version_token(self.request_version),
            )

            conn = http.client.HTTPConnection(origin_host, origin_port, timeout=3.0)
            try:
                conn.request(self.command, self.path, headers=upstream_headers)
                resp = conn.getresponse()
            except (OSError, http.client.HTTPException) as exc:
                conn.close()
                self._send_course_error(
                    502,
                    {
                        "error": "Bad Gateway",
                        "reason": "Course origin connection failed",
                        "upstream": f"{origin_host}:{origin_port}",
                        "host_disposition": type(exc).__name__,
                    },
                )
                return

            try:
                response_headers = resp.getheaders()
                response_connection_tokens = _response_connection_tokens(response_headers)
                response_via_values = [
                    value for name, value in response_headers if name.lower() == "via"
                ]
                existing_response_via = ", ".join(response_via_values) or None
                upstream_received_protocol = _http_version_token(resp.version)

                # Forward the upstream status line without letting
                # BaseHTTPRequestHandler inject a second Server/Date pair.
                self.send_response_only(resp.status)
                for name, value in response_headers:
                    lower = name.lower()
                    if lower == "via":
                        continue
                    if _remove_for_forwarding(name, response_connection_tokens):
                        continue
                    self.send_header(name, value)

                self.send_header(
                    "Via",
                    _append_via(existing_response_via, upstream_received_protocol),
                )
                # The course intermediary deliberately closes each downstream response.
                self.send_header("Connection", "close")
                self.end_headers()

                if resp.status not in (204, 304) and self.command != "HEAD":
                    self.wfile.write(resp.read())
            finally:
                conn.close()

        def do_GET(self) -> None:
            self._forward_request()

        def do_HEAD(self) -> None:
            self._forward_request()

        def do_POST(self) -> None:
            self._method_not_allowed()

        def do_PUT(self) -> None:
            self._method_not_allowed()

        def do_DELETE(self) -> None:
            self._method_not_allowed()

        def do_CONNECT(self) -> None:
            self._method_not_allowed()

    return IntermediaryRequestHandler


def run_intermediary_adapter(
    origin_host: str, origin_port: int, host: str = "127.0.0.1", port: int = 0
) -> None:
    if host != "127.0.0.1" or origin_host != "127.0.0.1":
        raise ValueError("LAB-REQ-01 is localhost-only: both bind and origin host must be 127.0.0.1")

    handler_class = make_proxy_handler(origin_host, origin_port)
    server = ThreadingHTTPServer((host, port), handler_class)
    actual_port = server.server_port
    print(f"PROXY_READY_PORT={actual_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LAB-REQ-01 bounded intermediary")
    parser.add_argument("--origin-host", default="127.0.0.1")
    parser.add_argument("--origin-port", type=int, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args()
    run_intermediary_adapter(args.origin_host, args.origin_port, args.host, args.port)
