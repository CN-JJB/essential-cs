#!/usr/bin/env python3
"""LAB-REQ-01 Intermediary Adapter (Reverse Proxy).

HTTP/1.1 Intermediary / Proxy Adapter:
- Binds to 127.0.0.1 with port 0 (dynamic allocation).
- Prints PROXY_READY_PORT=<port> to stdout immediately upon listening.
- Forwards incoming client requests to the configured origin server.
- Injects Via header: "1.1 essential-cs-intermediary".
- Correctly handles hop-by-hop headers (RFC 9110 Section 7.6.1).
- Maps upstream connection failure / refusal to 502 Bad Gateway.
"""

from __future__ import annotations

import argparse
import http.client
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}


def make_proxy_handler(origin_host: str, origin_port: int):
    class IntermediaryRequestHandler(BaseHTTPRequestHandler):
        """HTTP request handler forwarding to upstream origin."""

        protocol_version = "HTTP/1.1"

        def log_message(self, format: str, *args: object) -> None:
            """Suppress verbose server stderr logs during tests."""
            pass

        def _forward_request(self) -> None:
            # 1. Prepare upstream headers (strip hop-by-hop)
            upstream_headers: dict[str, str] = {}
            for k, v in self.headers.items():
                if k.lower() not in HOP_BY_HOP_HEADERS and k.lower() != "host":
                    upstream_headers[k] = v

            upstream_headers["Host"] = f"{origin_host}:{origin_port}"

            # 2. Inject / extend Via header
            client_via = self.headers.get("Via")
            if client_via:
                upstream_headers["Via"] = f"{client_via}, 1.1 essential-cs-intermediary"
            else:
                upstream_headers["Via"] = "1.1 essential-cs-intermediary"

            # 3. Read body if present
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # 4. Attempt upstream forward
            conn = None
            try:
                conn = http.client.HTTPConnection(origin_host, origin_port, timeout=3.0)
                conn.request(self.command, self.path, body=body, headers=upstream_headers)
                resp = conn.getresponse()
            except (OSError, http.client.HTTPException) as exc:
                # Upstream connection failed/refused -> 502 Bad Gateway
                if conn:
                    conn.close()
                err_body = json.dumps({
                    "error": "Bad Gateway",
                    "reason": "Origin server unreachable or connection refused",
                    "upstream": f"{origin_host}:{origin_port}",
                    "exception": type(exc).__name__,
                }).encode("utf-8")
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self.send_header("Via", "1.1 essential-cs-intermediary")
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(err_body)
                return

            # 5. Upstream responded: relay status and headers
            try:
                self.send_response(resp.status)
                resp_headers = resp.getheaders()
                via_seen = False
                for k, v in resp_headers:
                    if k.lower() in HOP_BY_HOP_HEADERS:
                        continue
                    if k.lower() == "via":
                        via_seen = True
                        self.send_header("Via", f"{v}, 1.1 essential-cs-intermediary")
                    else:
                        self.send_header(k, v)

                if not via_seen:
                    self.send_header("Via", "1.1 essential-cs-intermediary")
                self.send_header("Connection", "close")
                self.end_headers()

                # 6. Relay response body (unless 304, 204, or HEAD)
                if resp.status not in (204, 304) and self.command != "HEAD":
                    resp_body = resp.read()
                    self.wfile.write(resp_body)
            finally:
                conn.close()

        def do_GET(self) -> None:
            self._forward_request()

        def do_HEAD(self) -> None:
            self._forward_request()

        def do_POST(self) -> None:
            self._forward_request()

        def do_PUT(self) -> None:
            self._forward_request()

    return IntermediaryRequestHandler


def run_intermediary_adapter(
    origin_host: str, origin_port: int, host: str = "127.0.0.1", port: int = 0
) -> None:
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
    parser = argparse.ArgumentParser(description="LAB-REQ-01 Intermediary Adapter")
    parser.add_argument("--origin-host", default="127.0.0.1", help="Origin host (default: 127.0.0.1)")
    parser.add_argument("--origin-port", type=int, required=True, help="Origin port (required)")
    parser.add_argument("--host", default="127.0.0.1", help="Proxy bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=0, help="Proxy bind port (default: 0 for dynamic)")
    args = parser.parse_args()
    run_intermediary_adapter(args.origin_host, args.origin_port, args.host, args.port)
