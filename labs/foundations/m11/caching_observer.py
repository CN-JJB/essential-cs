#!/usr/bin/env python3
"""
M11 Lesson 3 Activity: HTTP Caching, Validation & Intermediary Observer.

Demonstrates:
1. HTTP Cache Freshness vs Validation (RFC 9111).
2. Strong ETag as an opaque entity validator (not inherently a hash).
3. Conditional request with If-None-Match yielding 304 Not Modified.
4. Proof of zero message body content transferred on 304 (without requiring Content-Length: 0).
5. Architectural trade-offs across HTTP/1.1, HTTP/2, and HTTP/3.
"""

import argparse
import http.server
import json
import socket
import sys
import threading
import time
import urllib.request


class CachingHTTPHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    current_etag = '"course-m11-v1"'
    resource_payload = json.dumps({
        "course": "Essential CS",
        "module": "M11",
        "data": "Large representation payload simulating network transfer savings",
    }).encode("utf-8")

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/resource":
            inm = self.headers.get("If-None-Match")

            # Check conditional validator
            if inm and inm.strip() == self.current_etag:
                # 304 Not Modified: transfers NO message body
                self.send_response(304)
                self.send_header("ETag", self.current_etag)
                self.send_header("Cache-Control", "max-age=60")
                self.send_header("Connection", "close")
                self.end_headers()
                # Crucial invariant: write ZERO body bytes
                return

            # Full 200 representation
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(self.resource_payload)))
            self.send_header("ETag", self.current_etag)
            self.send_header("Cache-Control", "max-age=60")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(self.resource_payload)
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()


def run_caching_observation():
    server = http.server.HTTPServer(("127.0.0.1", 0), CachingHTTPHandler)
    bound_host, bound_port = server.server_address

    srv_thread = threading.Thread(target=server.serve_forever, daemon=True)
    srv_thread.start()

    base_url = f"http://{bound_host}:{bound_port}"

    results = {
        "endpoint": f"{bound_host}:{bound_port}",
        "step1_initial_fetch": {},
        "step2_conditional_matching_etag": {},
        "step3_conditional_mismatched_etag": {},
        "transport_evolution_tradeoffs": {
            "http1": "Serial requests per connection by default, or multiple connections. Application-level HOL blocking.",
            "http2": "Multiplexes concurrent binary streams over one TCP connection. Packet drop on TCP causes transport-level HOL blocking across all streams.",
            "http3": "Independent streams over QUIC / UDP. Eliminates transport-level HOL blocking between streams, but higher CPU overhead and UDP routing sensitivity.",
            "winner_verdict": "NO UNIVERSAL PERFORMANCE WINNER; depends on RTT, loss rates, CPU capacity, and middlebox topologies.",
        },
    }

    try:
        # Step 1: Initial fetch (200 OK)
        req1 = urllib.request.Request(f"{base_url}/resource", method="GET")
        with urllib.request.urlopen(req1, timeout=3.0) as resp1:
            body1 = resp1.read()
            etag1 = resp1.headers.get("ETag")
            cache_control1 = resp1.headers.get("Cache-Control")
            results["step1_initial_fetch"] = {
                "status_code": resp1.status,
                "etag_received": etag1,
                "cache_control": cache_control1,
                "body_bytes_transferred": len(body1),
            }

        # Step 2: Conditional request with matching ETag (via raw socket to verify wire body bytes)
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.settimeout(3.0)
        raw_sock.connect((bound_host, bound_port))
        raw_cond_req = (
            f"GET /resource HTTP/1.1\r\n"
            f"Host: {bound_host}:{bound_port}\r\n"
            f"If-None-Match: {etag1}\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode("utf-8")
        raw_sock.sendall(raw_cond_req)

        raw_304_resp = bytearray()
        while True:
            chunk = raw_sock.recv(1024)
            if not chunk:
                break
            raw_304_resp.extend(chunk)
        raw_sock.close()

        wire_304_text = raw_304_resp.decode("utf-8", errors="replace")
        headers_part, sep, body_part = wire_304_text.partition("\r\n\r\n")
        status_line = headers_part.splitlines()[0] if headers_part else ""

        results["step2_conditional_matching_etag"] = {
            "status_line": status_line,
            "status_code": 304,
            "wire_body_bytes_transferred": len(body_part.encode("utf-8")),
            "zero_body_verified": (len(body_part) == 0),
            "bandwidth_saved_bytes": len(body1),
            "rule_confirmation": "RFC 9111 specifies 304 transfers NO message content; Content-Length: 0 is NOT required",
        }

        # Step 3: Conditional request with mismatched ETag (200 OK + full body)
        req3 = urllib.request.Request(
            f"{base_url}/resource",
            headers={"If-None-Match": '"v0.9-stale"'},
            method="GET",
        )
        with urllib.request.urlopen(req3, timeout=3.0) as resp3:
            body3 = resp3.read()
            results["step3_conditional_mismatched_etag"] = {
                "status_code": resp3.status,
                "body_bytes_transferred": len(body3),
                "revalidated": False,
                "full_body_sent": (len(body3) == len(body1)),
            }

    finally:
        server.shutdown()
        server.server_close()
        srv_thread.join(timeout=1.0)

    return results


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="M11 Caching and Validation Observer")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = run_caching_observation()

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    print("=" * 60)
    print(" M11-03 HTTP Caching & Validation Observer")
    print("=" * 60)
    print(f" Target Endpoint:   {results['endpoint']}")
    print("-" * 60)
    print(" [Step 1: Initial Representation Fetch]")
    s1 = results["step1_initial_fetch"]
    print(f"   Status Code:     {s1['status_code']}")
    print(f"   ETag Received:   {s1['etag_received']} (Opaque entity validator)")
    print(f"   Body Transferred:{s1['body_bytes_transferred']} bytes")
    print("-" * 60)
    print(" [Step 2: Conditional Request with Matching If-None-Match]")
    s2 = results["step2_conditional_matching_etag"]
    print(f"   Status Line:     {s2['status_line']}")
    print(f"   Body Transferred:{s2['wire_body_bytes_transferred']} bytes")
    print(f"   Zero Body Verified: {'YES' if s2['zero_body_verified'] else 'NO'}")
    print(f"   Bandwidth Saved: {s2['bandwidth_saved_bytes']} payload bytes")
    print("-" * 60)
    print(" [Step 3: Conditional Request with Mismatched ETag]")
    s3 = results["step3_conditional_mismatched_etag"]
    print(f"   Status Code:     {s3['status_code']} (Stale validator triggers representation transfer)")
    print(f"   Body Transferred:{s3['body_bytes_transferred']} bytes")
    print("-" * 60)
    print(" [Transport Evolution & Invariants]")
    t = results["transport_evolution_tradeoffs"]
    print(f"   HTTP/1.1:        {t['http1']}")
    print(f"   HTTP/2:          {t['http2']}")
    print(f"   HTTP/3:          {t['http3']}")
    print(f"   Verdict:         {t['winner_verdict']}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
