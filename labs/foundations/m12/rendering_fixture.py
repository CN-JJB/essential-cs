#!/usr/bin/env python3
"""
Rendering Pipeline & Script Execution Fixture for M12 Lesson L12-02.
Demonstrates parser-blocking classic script vs. defer/async scheduling semantics.

Invariants:
- Dynamic port 0 binding on 127.0.0.1;
- Bounded delay safety cap (max 2.0s);
- Zero external dependencies (Python standard library only).
"""

import http.server
import socket
import socketserver
import sys
import threading
import time
import urllib.parse

SAFETY_DELAY_CAP_SECONDS = 2.0


class RenderingHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler serving pipeline demonstration assets."""

    def log_message(self, format, *args):
        # Suppress noisy request logs during testing unless debugging
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            self.send_index_html()
        elif path == "/style.css":
            self.send_css()
        elif path == "/blocking.js":
            delay = 0.3
            if "delay" in query:
                try:
                    delay = float(query["delay"][0])
                except ValueError:
                    delay = 0.3
            delay = max(0.0, min(delay, SAFETY_DELAY_CAP_SECONDS))
            self.send_blocking_js(delay)
        elif path == "/deferred.js":
            self.send_deferred_js()
        elif path == "/async.js":
            self.send_async_js()
        else:
            self.send_error(404, "Not Found")

    def send_index_html(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>L12-02 Document Rendering Pipeline Demonstration</title>
  <link rel="stylesheet" href="/style.css">
  <script>
    window.renderEvents = [];
    window.recordEvent = function(name) {
      const t = (performance && performance.now) ? performance.now() : Date.now();
      window.renderEvents.push({ event: name, timeMs: t });
      console.log("[L12-02 Event] " + name + " @ " + t.toFixed(2) + "ms");
    };
    recordEvent("head_start");
  </script>
  <!-- Parser-blocking classic script: parser pauses here until fetched & executed -->
  <script src="/blocking.js?delay=0.3"></script>
  <!-- Deferred classic script: fetched in parallel, executes after parsing completes -->
  <script defer src="/deferred.js"></script>
  <!-- Async script: executes when ready without waiting for parse completion -->
  <script async src="/async.js"></script>
  <script>
    recordEvent("head_end");
  </script>
</head>
<body>
  <h1>Essential CS L12-02: Document Rendering Pipeline</h1>
  <p id="content">This paragraph is part of the DOM constructed by the HTML parser.</p>
  <script>
    recordEvent("body_content_parsed");
  </script>
  <div id="status-box">Pipeline events logged. Open browser console or DevTools Performance panel.</div>
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      recordEvent("DOMContentLoaded");
    });
    window.addEventListener("load", function() {
      recordEvent("window_load");
    });
    recordEvent("body_end");
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

    def send_css(self):
        css = """/* Conceptual rendering pipeline style */
body {
  font-family: sans-serif;
  margin: 2rem;
  background: #f8f9fa;
  color: #212529;
}
#status-box {
  padding: 1rem;
  margin-top: 1.5rem;
  background: #e9ecef;
  border-left: 4px solid #0d6efd;
}
"""
        body = css.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/css; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_blocking_js(self, delay):
        if delay > 0:
            time.sleep(delay)
        code = f"""// [L12-02] Classic parser-blocking script (injected delay: {delay}s)
recordEvent("blocking_script_executed");
"""
        body = code.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Simulated-Delay", str(delay))
        self.end_headers()
        self.wfile.write(body)

    def send_deferred_js(self):
        code = """// [L12-02] Classic defer script (executes in document order after parse)
recordEvent("deferred_script_executed");
"""
        body = code.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_async_js(self):
        code = """// [L12-02] Async script (independent fetch/execution)
recordEvent("async_script_executed");
"""
        body = code.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/javascript; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class RenderingServerFixture:
    """Manages the lifecycle of a loopback rendering test server on port 0."""

    def __init__(self, host="127.0.0.1"):
        self.host = host
        self.server = None
        self.thread = None
        self.port = None

    def start(self):
        self.server = ThreadedHTTPServer((self.host, 0), RenderingHTTPHandler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self.port

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
            self.thread = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def main():
    fixture = RenderingServerFixture()
    port = fixture.start()
    print("=" * 60)
    print(" Essential CS L12-02: Document Rendering Pipeline Fixture")
    print("=" * 60)
    print(f" Listening on: http://127.0.0.1:{port}/")
    print(" Press Ctrl+C to stop.")
    print("-" * 60)
    print(" To observe in browser (when GUI is available):")
    print(f"   1. Open Chrome/Edge/Firefox to: http://127.0.0.1:{port}/")
    print("   2. Open DevTools -> Console to view recorded events.")
    print("   3. Open DevTools -> Performance to record timeline and observe script blocking.")
    print("-" * 60)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping fixture...")
    finally:
        fixture.stop()
        print("Stopped cleanly.")


if __name__ == "__main__":
    main()
