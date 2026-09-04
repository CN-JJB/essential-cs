#!/usr/bin/env python3
"""LAB-REQ-01 Origin Server.

HTTP/1.1 Origin server for LAB-REQ-01:
- Binds to 127.0.0.1 with port 0 (dynamic allocation).
- Prints ORIGIN_READY_PORT=<port> to stdout immediately upon listening.
- Serves /resource with ETag and supports conditional If-None-Match requests (304 with zero body).
- Serves /health for liveness probes.
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ETAG_RESOURCE = '"strong-v1"'
RESOURCE_PAYLOAD = {
    "message": "Hello from origin server",
    "version": 1,
    "status": "active",
    "authoritative": True,
}


class OriginRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for LAB-REQ-01 origin server."""

    protocol_version = "HTTP/1.1"

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default stderr logging during normal operation."""
        # Un-comment below for verbose local debugging:
        # sys.stderr.write(f"[ORIGIN] {format % args}\n")
        pass

    def do_GET(self) -> None:
        """Handle GET requests."""
        if self.path == "/health":
            body = json.dumps({"status": "ok", "service": "origin"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/resource":
            inm = self.headers.get("If-None-Match", "").strip()
            # Conditional request validation
            if inm == ETAG_RESOURCE:
                # 304 Not Modified: RFC 9111 Section 4.1:
                # The 304 status code MUST NOT contain a message body.
                self.send_response(304)
                self.send_header("ETag", ETAG_RESOURCE)
                self.send_header("Cache-Control", "max-age=60, must-revalidate")
                self.send_header("Connection", "close")
                self.end_headers()
                # Crucial: write NO body bytes
                return

            body = json.dumps(RESOURCE_PAYLOAD).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("ETag", ETAG_RESOURCE)
            self.send_header("Cache-Control", "max-age=60, must-revalidate")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            return

        # Fallback 404
        body = json.dumps({"error": "Not Found", "path": self.path}).encode("utf-8")
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)


def run_origin_server(host: str = "127.0.0.1", port: int = 0) -> None:
    """Run origin server until interrupted."""
    server = ThreadingHTTPServer((host, port), OriginRequestHandler)
    actual_port = server.server_port
    # Print machine-readable handshake for harness / learners
    print(f"ORIGIN_READY_PORT={actual_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LAB-REQ-01 Origin Server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=0, help="Bind port (default: 0 for dynamic)")
    args = parser.parse_args()
    run_origin_server(args.host, args.port)
