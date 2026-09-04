#!/usr/bin/env python3
"""
M11 Lesson 2 Activity: HTTP Semantics & Uniform Interface Observer.

Demonstrates:
1. HTTP message structure (RFC 9110 / RFC 9112): Status line, headers, CRLF delimiter, payload.
2. Resource vs Representation distinction.
3. Method semantics: Safe (GET) vs Idempotent (PUT, DELETE) vs Non-idempotent (POST).
4. Protocol outcome vs Business outcome (HTTP 200 != business transaction success).
5. Unambiguous wire framing with Content-Length.
"""

import argparse
import http.server
import json
import socket
import sys
import threading
import urllib.request


class CourseHTTPHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # In-memory mock resource state
    resources = {
        "42": {"item_id": 42, "name": "Mechanical Keyboard", "stock": 10},
    }
    next_id = 43

    def log_message(self, format, *args):
        # Suppress default noisy stderr logging
        pass

    def send_framed_response(self, status_code, body_bytes, content_type="application/json", extra_headers=None):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body_bytes)))
        self.send_header("Connection", "close")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body_bytes)

    def do_GET(self):
        if self.path == "/items/42":
            data = json.dumps(self.resources["42"]).encode("utf-8")
            self.send_framed_response(200, data)
        elif self.path == "/business-failure":
            # Demonstrates 200 OK protocol status != business success
            data = json.dumps({
                "status": "FAILURE",
                "error_code": "INSUFFICIENT_FUNDS",
                "message": "Account balance below transaction threshold",
            }).encode("utf-8")
            self.send_framed_response(200, data)
        elif self.path == "/health":
            self.send_framed_response(200, b'{"status": "UP"}')
        else:
            self.send_framed_response(404, b'{"error": "not_found"}')

    def do_PUT(self):
        if self.path == "/items/42":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len) if content_len > 0 else b"{}"
            try:
                payload = json.loads(body.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("PUT representation must be a JSON object")
                # Course PUT contract: replace the selected resource representation
                # rather than applying a PATCH-like partial update.
                replacement = dict(payload)
                replacement["item_id"] = 42
                self.resources["42"] = replacement
                resp = json.dumps(self.resources["42"]).encode("utf-8")
                self.send_framed_response(200, resp)
            except Exception:
                self.send_framed_response(400, b'{"error": "invalid_json"}')
        else:
            self.send_framed_response(404, b'{"error": "not_found"}')

    def do_POST(self):
        if self.path == "/items":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len) if content_len > 0 else b"{}"
            try:
                payload = json.loads(body.decode("utf-8"))
                item_id = str(CourseHTTPHandler.next_id)
                CourseHTTPHandler.next_id += 1
                payload["item_id"] = int(item_id)
                self.resources[item_id] = payload
                resp = json.dumps(payload).encode("utf-8")
                self.send_framed_response(201, resp, extra_headers={"Location": f"/items/{item_id}"})
            except Exception:
                self.send_framed_response(400, b'{"error": "invalid_json"}')
        else:
            self.send_framed_response(404, b'{"error": "not_found"}')


def run_http_semantics_observation():
    # Reset bounded fixture state so repeated runs remain deterministic.
    CourseHTTPHandler.resources = {
        "42": {"item_id": 42, "name": "Mechanical Keyboard", "stock": 10},
    }
    CourseHTTPHandler.next_id = 43

    # Start server on 127.0.0.1:0
    server = http.server.HTTPServer(("127.0.0.1", 0), CourseHTTPHandler)
    bound_host, bound_port = server.server_address

    srv_thread = threading.Thread(target=server.serve_forever, daemon=False)
    srv_thread.start()

    base_url = f"http://{bound_host}:{bound_port}"

    results = {
        "endpoint": f"{bound_host}:{bound_port}",
        "step1_safe_get": {},
        "step2_idempotent_put": {},
        "step3_non_idempotent_post": {},
        "step4_protocol_vs_business_status": {},
        "step5_raw_wire_trace": {},
    }

    try:
        # Step 1: Safe GET
        req = urllib.request.Request(f"{base_url}/items/42", method="GET")
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            results["step1_safe_get"] = {
                "method": "GET",
                "semantic": "SAFE (client does not request an unsafe state change; incidental effects may exist)",
                "status_code": resp.status,
                "headers": dict(resp.headers),
                "representation": body,
            }

        # Step 2: Idempotent PUT
        put_payload = json.dumps({
            "item_id": 42,
            "name": "Custom Mechanical Keyboard",
            "stock": 10,
        }).encode("utf-8")
        req_put1 = urllib.request.Request(
            f"{base_url}/items/42",
            data=put_payload,
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req_put1, timeout=3.0) as resp1:
            body1 = json.loads(resp1.read().decode("utf-8"))

        req_put2 = urllib.request.Request(
            f"{base_url}/items/42",
            data=put_payload,
            headers={"Content-Type": "application/json"},
            method="PUT",
        )
        with urllib.request.urlopen(req_put2, timeout=3.0) as resp2:
            body2 = json.loads(resp2.read().decode("utf-8"))

        results["step2_idempotent_put"] = {
            "method": "PUT",
            "semantic": "IDEMPOTENT (repeating the same request asks for the same intended target-resource effect)",
            "status_code": resp2.status,
            "idempotency_verified": (body1 == body2),
            "resulting_state": body2,
        }

        # Step 3: Non-idempotent POST
        post_payload = json.dumps({"name": "Wireless Mouse", "stock": 5}).encode("utf-8")
        req_post = urllib.request.Request(
            f"{base_url}/items",
            data=post_payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req_post, timeout=3.0) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            results["step3_non_idempotent_post"] = {
                "method": "POST",
                "semantic": "POST is not defined idempotent by default; this course endpoint creates a new resource per submission",
                "status_code": resp.status,
                "location_header": resp.headers.get("Location"),
                "created_item": body,
            }

        # Step 4: Protocol 200 OK vs Business Failure
        req_err = urllib.request.Request(f"{base_url}/business-failure", method="GET")
        with urllib.request.urlopen(req_err, timeout=3.0) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            results["step4_protocol_vs_business_status"] = {
                "http_status_code": resp.status,
                "http_status_meaning": "200 OK: this course request succeeded according to GET semantics as reported by the server",
                "business_status": body.get("status"),
                "business_error_code": body.get("error_code"),
                "lesson_takeaway": "HTTP 200 OK does not establish a domain/business invariant",
            }

        # Step 5: Raw wire-level HTTP/1.1 message inspection over raw socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0)
        s.connect((bound_host, bound_port))
        raw_request = (
            f"GET /items/42 HTTP/1.1\r\n"
            f"Host: {bound_host}:{bound_port}\r\n"
            f"User-Agent: EssentialCS-RawTrace/1.0\r\n"
            f"Accept: application/json\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        ).encode("utf-8")
        s.sendall(raw_request)

        raw_response = bytearray()
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            raw_response.extend(chunk)
        s.close()

        wire_text = raw_response.decode("utf-8", errors="replace")
        header_part, _, body_part = wire_text.partition("\r\n\r\n")

        results["step5_raw_wire_trace"] = {
            "raw_request_sent": raw_request.decode("utf-8"),
            "response_headers": header_part.split("\r\n"),
            "response_body": body_part,
            "crlf_delimiter_found": "\r\n\r\n" in wire_text,
        }

    finally:
        server.shutdown()
        server.server_close()
        srv_thread.join(timeout=2.0)
        results["server_thread_reaped"] = not srv_thread.is_alive()

    return results


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="M11 HTTP Semantics Observer")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = run_http_semantics_observation()

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    print("=" * 60)
    print(" M11-02 HTTP Semantics & Uniform Interface Observer")
    print("=" * 60)
    print(f" Target Endpoint:   {results['endpoint']}")
    print("-" * 60)
    print(" [Step 1: Safe Method Semantics (GET)]")
    s1 = results["step1_safe_get"]
    print(f"   Status Code:     {s1['status_code']}")
    print(f"   Semantics:       {s1['semantic']}")
    print(f"   Representation:  {s1['representation']}")
    print("-" * 60)
    print(" [Step 2: Idempotent Method Semantics (PUT)]")
    s2 = results["step2_idempotent_put"]
    print(f"   Status Code:     {s2['status_code']}")
    print(f"   Semantics:       {s2['semantic']}")
    print(f"   State Unchanged on Re-execution: {'YES' if s2['idempotency_verified'] else 'NO'}")
    print("-" * 60)
    print(" [Step 3: Non-Idempotent Semantics (POST)]")
    s3 = results["step3_non_idempotent_post"]
    print(f"   Status Code:     {s3['status_code']}")
    print(f"   Location:        {s3['location_header']}")
    print(f"   Created Item:    {s3['created_item']}")
    print("-" * 60)
    print(" [Step 4: Protocol Status vs Business Outcome]")
    s4 = results["step4_protocol_vs_business_status"]
    print(f"   HTTP Status:     {s4['http_status_code']} OK")
    print(f"   Business Status: {s4['business_status']} ({s4['business_error_code']})")
    print(f"   Core Boundary:   {s4['lesson_takeaway']}")
    print("-" * 60)
    print(" [Step 5: Wire Framing]")
    s5 = results["step5_raw_wire_trace"]
    print(f"   Status Line:     {s5['response_headers'][0]}")
    print(f"   Header/Body CRLF Delimiter: {'PRESENT' if s5['crlf_delimiter_found'] else 'MISSING'}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
