#!/usr/bin/env python3
"""
Dual-Origin CORS & Security Boundary Fixture for M12 Lesson L12-03.
Demonstrates:
1. Origin A (http://127.0.0.1:<portA>) and Origin B (http://127.0.0.1:<portB>);
2. Simple cross-origin fetch arrival at Origin B vs. browser response-access enforcement;
3. Authorized CORS response with Access-Control-Allow-Origin;
4. Bounded deterministic preflighted request (OPTIONS);
5. Non-browser client contrast (curl/urllib receives response; does not mean curl bypasses server authn/authz).

Invariants:
- Dynamic port 0 binding on 127.0.0.1 for both Origin A and Origin B;
- Zero hardcoded ports (8000/9000 strictly forbidden);
- Zero external dependencies.
"""

import http.server
import json
import socketserver
import threading
import time
import urllib.parse
import urllib.request


class OriginARequestHandler(http.server.BaseHTTPRequestHandler):
    """Handler for Origin A serving the client testing web page."""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_index()
        else:
            self.send_error(404, "Not Found")

    def send_index(self):
        # Retrieve Origin B URL from server attributes
        origin_b_url = getattr(self.server, "origin_b_url", "http://127.0.0.1:0")
        origin_a_url = f"http://127.0.0.1:{self.server.server_address[1]}"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>L12-03 Origin A - CORS & Security Boundary Test</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 2rem; background: #f8f9fa; color: #212529; line-height: 1.5; }}
    .card {{ background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }}
    .btn {{ padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9rem; font-weight: 600; margin-right: 0.5rem; margin-bottom: 0.5rem; }}
    .btn-danger {{ background: #dc3545; color: white; }}
    .btn-success {{ background: #198754; color: white; }}
    .btn-primary {{ background: #0d6efd; color: white; }}
    pre {{ background: #212529; color: #f8f9fa; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; }}
    .badge {{ display: inline-block; padding: 0.25rem 0.5rem; font-size: 0.8rem; border-radius: 4px; font-weight: bold; }}
    .badge-origin {{ background: #e7f1ff; color: #0c63e4; }}
  </style>
</head>
<body>
  <h1>Essential CS L12-03: Web Security Model & CORS</h1>
  <div class="card">
    <p>Current Page Origin: <span class="badge badge-origin" id="page-origin">{origin_a_url}</span></p>
    <p>Target API Origin: <span class="badge badge-origin" id="target-origin">{origin_b_url}</span></p>
  </div>

  <div class="card">
    <h3>Action 1: Simple Cross-Origin Fetch without CORS Permission</h3>
    <p>Sends a simple GET request to Origin B. Origin B returns 200 OK without <code>Access-Control-Allow-Origin</code>.</p>
    <button class="btn btn-danger" onclick="runCase1()">Execute Fetch (Expect Browser CORS Block)</button>
    <div id="case1-result"></div>
  </div>

  <div class="card">
    <h3>Action 2: Authorized Cross-Origin Fetch</h3>
    <p>Sends a simple GET request with <code>?cors=1</code>. Origin B includes matching <code>Access-Control-Allow-Origin</code> header.</p>
    <button class="btn btn-success" onclick="runCase2()">Execute Fetch (Expect Success)</button>
    <div id="case2-result"></div>
  </div>

  <div class="card">
    <h3>Action 3: Preflighted Cross-Origin Request</h3>
    <p>Sends a request with a custom header <code>X-Course-Custom</code> triggering a browser preflight <code>OPTIONS</code> check.</p>
    <button class="btn btn-primary" onclick="runCase3()">Execute Preflighted Fetch</button>
    <div id="case3-result"></div>
  </div>

  <div class="card">
    <h3>Server-Side Arrival Inspection</h3>
    <p>Query Origin B for the list of HTTP requests that actually arrived at the server:</p>
    <button class="btn" style="background:#6c757d;color:white;" onclick="checkServerLogs()">Inspect Origin B Request Log</button>
    <pre id="log-output">No logs fetched yet.</pre>
  </div>

  <script>
    const TARGET_URL = "{origin_b_url}";

    async function runCase1() {{
      const out = document.getElementById("case1-result");
      out.innerHTML = "<em>Sending fetch...</em>";
      try {{
        const resp = await fetch(TARGET_URL + "/api/data?mode=unauthorized");
        const data = await resp.json();
        out.innerHTML = "<p style='color:green'>Unexpectedly accessed response: " + JSON.stringify(data) + "</p>";
      }} catch (err) {{
        out.innerHTML = "<p style='color:red'><strong>Browser Blocked Response:</strong> " + err.name + ": " + err.message + "<br><small>(Check DevTools Console for details: Cross-Origin Resource Sharing policy violation)</small></p>";
      }}
    }}

    async function runCase2() {{
      const out = document.getElementById("case2-result");
      out.innerHTML = "<em>Sending fetch...</em>";
      try {{
        const resp = await fetch(TARGET_URL + "/api/data?mode=authorized");
        const data = await resp.json();
        out.innerHTML = "<p style='color:green'><strong>Success! Response read:</strong> <pre>" + JSON.stringify(data, null, 2) + "</pre></p>";
      }} catch (err) {{
        out.innerHTML = "<p style='color:red'>Failed: " + err + "</p>";
      }}
    }}

    async function runCase3() {{
      const out = document.getElementById("case3-result");
      out.innerHTML = "<em>Sending preflighted fetch...</em>";
      try {{
        const resp = await fetch(TARGET_URL + "/api/preflighted", {{
          method: "POST",
          headers: {{
            "Content-Type": "application/json",
            "X-Course-Custom": "EssentialCS-Preflight-Check"
          }},
          body: JSON.stringify({{ action: "test-preflight" }})
        }});
        const data = await resp.json();
        out.innerHTML = "<p style='color:green'><strong>Preflight Success:</strong> <pre>" + JSON.stringify(data, null, 2) + "</pre></p>";
      }} catch (err) {{
        out.innerHTML = "<p style='color:red'>Preflight Failed: " + err + "</p>";
      }}
    }}

    async function checkServerLogs() {{
      const out = document.getElementById("log-output");
      try {{
        // Origin B provides an open inspection endpoint
        const resp = await fetch(TARGET_URL + "/api/requests?mode=open");
        const logs = await resp.json();
        out.textContent = JSON.stringify(logs, null, 2);
      }} catch (err) {{
        out.textContent = "Error fetching server logs: " + err;
      }}
    }}
  </script>
</body>
</html>
"""
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


class OriginBRequestHandler(http.server.BaseHTTPRequestHandler):
    """Handler for Origin B simulating backend API and recording requests."""

    def log_message(self, format, *args):
        pass

    def record_incoming_request(self):
        # Keep diagnostics course-scoped. Do not reflect arbitrary Cookie,
        # Authorization, or other ambient credential headers into Origin A.
        safe_header_names = (
            "Origin",
            "Access-Control-Request-Method",
            "Access-Control-Request-Headers",
            "Content-Type",
            "X-Course-Custom",
        )
        safe_headers = {
            name: self.headers.get(name)
            for name in safe_header_names
            if self.headers.get(name) is not None
        }
        log_entry = {
            "timestamp": time.time(),
            "method": self.command,
            "path": self.path,
            "headers": safe_headers,
        }
        with self.server.lock:
            self.server.received_requests.append(log_entry)

    def do_OPTIONS(self):
        self.record_incoming_request()
        parsed = urllib.parse.urlparse(self.path)
        origin_header = self.headers.get("Origin", "")

        if parsed.path == "/api/preflighted":
            allowed_origin = getattr(self.server, "allowed_origin", "")
            requested_method = self.headers.get("Access-Control-Request-Method", "")
            requested_headers = {
                item.strip().lower()
                for item in self.headers.get("Access-Control-Request-Headers", "").split(",")
                if item.strip()
            }
            allowed_headers = {"content-type", "x-course-custom"}
            if (
                origin_header != allowed_origin
                or requested_method != "POST"
                or not requested_headers.issubset(allowed_headers)
            ):
                self.send_response(403)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return

            # Course policy: authorize exactly this run's Origin A.
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Access-Control-Allow-Methods", "POST")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Course-Custom")
            self.send_header("Access-Control-Max-Age", "60")
            self.send_header("Vary", "Origin")
            self.end_headers()
        else:
            self.send_response(405)
            self.end_headers()

    def do_GET(self):
        self.record_incoming_request()
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        origin_header = self.headers.get("Origin", "")

        if parsed.path == "/api/data":
            mode = query.get("mode", ["unauthorized"])[0]
            data = {
                "source": "Origin B",
                "course_payload": "course-data-token-42",
                "received_origin": origin_header,
                "message": "Origin B generated this representation."
            }
            body = json.dumps(data, indent=2).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")

            # CORS Policy Decision
            allowed_origin = getattr(self.server, "allowed_origin", "")
            if mode == "authorized" and origin_header == allowed_origin:
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            elif mode == "wildcard":
                self.send_header("Access-Control-Allow-Origin", "*")
            # If mode == "unauthorized", omit Access-Control-Allow-Origin header completely

            self.end_headers()
            self.wfile.write(body)

        elif parsed.path == "/api/requests":
            # Diagnostic inspection endpoint
            with self.server.lock:
                logs = list(self.server.received_requests)
            body = json.dumps(logs, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")  # Open for inspection UI
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        self.record_incoming_request()
        parsed = urllib.parse.urlparse(self.path)
        origin_header = self.headers.get("Origin", "")

        if parsed.path == "/api/preflighted":
            content_length = int(self.headers.get("Content-Length", 0))
            payload = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

            response_data = {
                "status": "PREFLIGHTED_POST_SUCCESS",
                "received_custom_header": self.headers.get("X-Course-Custom"),
                "echo_payload": payload,
            }
            body = json.dumps(response_data).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            allowed_origin = getattr(self.server, "allowed_origin", "")
            if origin_header == allowed_origin:
                self.send_header("Access-Control-Allow-Origin", allowed_origin)
                self.send_header("Vary", "Origin")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not Found")


class DualOriginCORSFixture:
    """Manages two independent HTTP servers on dynamic ports to test CORS boundaries."""

    def __init__(self, host="127.0.0.1"):
        if host != "127.0.0.1":
            raise ValueError("M12 CORS fixture is localhost-only and must bind 127.0.0.1")
        self.host = host
        self.server_a = None
        self.server_b = None
        self.thread_a = None
        self.thread_b = None
        self.port_a = None
        self.port_b = None
        self.last_stop_record = None

    def start(self):
        # 1. Start Origin B (API Server)
        class OriginBServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
            daemon_threads = False
            allow_reuse_address = True

        self.server_b = OriginBServer((self.host, 0), OriginBRequestHandler)
        self.server_b.lock = threading.Lock()
        self.server_b.received_requests = []
        self.port_b = self.server_b.server_address[1]

        self.thread_b = threading.Thread(target=self.server_b.serve_forever, daemon=False)
        self.thread_b.start()

        # 2. Start Origin A (Client Web Page Server)
        class OriginAServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
            daemon_threads = True
            allow_reuse_address = True

        self.server_a = OriginAServer((self.host, 0), OriginARequestHandler)
        self.server_a.origin_b_url = f"http://{self.host}:{self.port_b}"
        self.port_a = self.server_a.server_address[1]
        self.server_b.allowed_origin = f"http://{self.host}:{self.port_a}"

        self.thread_a = threading.Thread(target=self.server_a.serve_forever, daemon=False)
        self.thread_a.start()

        return self.port_a, self.port_b

    def get_origin_b_requests(self):
        if self.server_b and hasattr(self.server_b, "received_requests"):
            with self.server_b.lock:
                return list(self.server_b.received_requests)
        return []

    def stop(self):
        threads = [("origin_a", self.thread_a), ("origin_b", self.thread_b)]
        if self.server_a:
            self.server_a.shutdown()
            self.server_a.server_close()
            self.server_a = None
        if self.server_b:
            self.server_b.shutdown()
            self.server_b.server_close()
            self.server_b = None

        record = {}
        for name, thread in threads:
            if thread:
                thread.join(timeout=2.0)
                record[name + "_thread_reaped"] = not thread.is_alive()
                if thread.is_alive():
                    raise RuntimeError(f"{name} server thread did not terminate cleanly")
        self.thread_a = None
        self.thread_b = None
        self.last_stop_record = record
        return record

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def fetch_from_non_browser_client(url):
    """
    Demonstrate that a non-browser HTTP client retrieves the response directly.
    Non-browser clients do not run untrusted scripts and do not enforce browser CORS response blocking.
    """
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=3.0) as response:
        status = response.status
        headers = dict(response.getheaders())
        body = response.read().decode("utf-8")
        return {
            "status_code": status,
            "headers": headers,
            "body": body,
            "has_cors_header": "access-control-allow-origin" in {k.lower(): v for k, v in headers.items()},
        }


def main():
    fixture = DualOriginCORSFixture()
    port_a, port_b = fixture.start()
    origin_a = f"http://127.0.0.1:{port_a}"
    origin_b = f"http://127.0.0.1:{port_b}"

    print("=" * 60)
    print(" Essential CS L12-03: Dual-Origin CORS Security Fixture")
    print("=" * 60)
    print(f" Origin A (Web Page): {origin_a}/")
    print(f" Origin B (API Server): {origin_b}/")
    print("-" * 60)
    print(" 1. Browser Test (when GUI browser available):")
    print(f"    Open {origin_a}/ in your browser.")
    print("    Click Action 1 to see the browser block cross-origin script access.")
    print("    Click Action 2 to see authorized cross-origin access with ACAO.")
    print("    Click Action 3 to observe preflight OPTIONS.")
    print("-" * 60)
    print(" 2. Non-Browser Client Contrast:")
    non_browser_res = fetch_from_non_browser_client(f"{origin_b}/api/data?mode=unauthorized")
    print(f"    curl / python client fetched {origin_b}/api/data?mode=unauthorized:")
    print(f"    Status: {non_browser_res['status_code']}, ACAO header present: {non_browser_res['has_cors_header']}")
    print(f"    Body received: {non_browser_res['body'].strip()}")
    print("    Notice: Non-browser client received the HTTP response body directly.")
    print("    This proves CORS is enforced by browser user agents, not the raw network layer.")
    print("=" * 60)
    print(" Press Ctrl+C to stop servers.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping CORS fixture...")
    finally:
        fixture.stop()
        print("Stopped cleanly.")


if __name__ == "__main__":
    main()
