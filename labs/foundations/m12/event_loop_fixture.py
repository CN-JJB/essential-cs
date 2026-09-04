#!/usr/bin/env python3
"""
Event Loop, Task/Microtask Ordering & Long-Task Responsiveness Fixture for M12 Lesson L12-04.
Demonstrates:
1. Relative execution ordering of synchronous code -> Promise microtasks -> timer tasks;
2. Main-thread long-task UI jank under a strict harness safety cap (< 2.0s);
3. Compositor vs. main thread concurrency callout (CSS transforms may continue during main-thread lockup);
4. Chunked yielding to preserve responsiveness.

Invariants:
- Dynamic port 0 binding on 127.0.0.1;
- Strictly bounded long-task execution (capped at 2000ms, no infinite loops);
- Zero external dependencies.
"""

import http.server
import socket
import socketserver
import sys
import threading
import time
import urllib.parse


class EventLoopHTTPHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler serving event loop demonstration assets."""

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_index()
        else:
            self.send_error(404, "Not Found")

    def send_index(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>L12-04 Event Loop & Execution Ordering</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 2rem; background: #f8f9fa; color: #212529; line-height: 1.5; }
    .card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
    .btn { padding: 0.5rem 1rem; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9rem; font-weight: 600; margin-right: 0.5rem; margin-bottom: 0.5rem; }
    .btn-primary { background: #0d6efd; color: white; }
    .btn-danger { background: #dc3545; color: white; }
    .btn-success { background: #198754; color: white; }
    pre { background: #212529; color: #f8f9fa; padding: 1rem; border-radius: 6px; overflow-x: auto; font-size: 0.85rem; }

    /* Compositor-friendly spinning box */
    .spinner-box {
      width: 60px;
      height: 60px;
      background: linear-gradient(45deg, #0d6efd, #0dcaf0);
      border-radius: 12px;
      margin: 1rem 0;
      animation: spin 2s linear infinite;
      will-change: transform;
    }
    @keyframes spin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    .counter-display {
      font-size: 1.5rem;
      font-weight: bold;
      color: #0d6efd;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <h1>Essential CS L12-04: Event Loop & Responsiveness</h1>

  <div class="card">
    <h3>Demonstration 1: Task vs. Microtask Execution Ordering</h3>
    <p>Tests the deterministic relative ordering: Synchronous code &rarr; Microtask queue (Promises, queueMicrotask) &rarr; Next Task (setTimeout).</p>
    <button class="btn btn-primary" onclick="runOrderingTest()">Run Task/Microtask Test</button>
    <pre id="order-output">Click button to run test.</pre>
  </div>

  <div class="card">
    <h3>Demonstration 2: Main-Thread Long Task vs. Compositor Concurrency</h3>
    <p>The animated box below rotates using CSS <code>transform</code> (compositor thread). The counter updates via <code>requestAnimationFrame</code> on the main thread.</p>

    <div style="display: flex; gap: 2rem; align-items: center;">
      <div>
        <div class="spinner-box"></div>
        <small>Compositor Thread (CSS Transform)</small>
      </div>
      <div>
        <div class="counter-display" id="raf-counter">Frame: 0</div>
        <small>Main Thread rAF Counter</small>
      </div>
    </div>

    <div style="margin-top: 1.5rem;">
      <button class="btn btn-danger" onclick="triggerLongTask(500)">Block Main Thread (500ms Bounded Loop)</button>
      <button class="btn btn-success" onclick="triggerChunkedTask(500)">Run Chunked Yielding (500ms Sliced)</button>
      <div id="long-task-status" style="margin-top: 0.5rem; font-style: italic;">Status: Idle</div>
    </div>
  </div>

  <script>
    // Frame counter on main thread
    let frameCount = 0;
    function updateCounter() {
      frameCount++;
      document.getElementById("raf-counter").textContent = "Frame: " + frameCount;
      requestAnimationFrame(updateCounter);
    }
    requestAnimationFrame(updateCounter);

    // Demonstration 1: Ordering Test
    function runOrderingTest() {
      const out = document.getElementById("order-output");
      const logs = [];

      logs.push("1_sync_start");

      setTimeout(() => {
        logs.push("4_timer_task (setTimeout 0ms)");
        out.textContent = "Observed Execution Order:\n" + logs.map((l, i) => `  Step ${i+1}: ${l}`).join("\n");
      }, 0);

      Promise.resolve().then(() => {
        logs.push("3_microtask_promise_1");
      }).then(() => {
        logs.push("3b_microtask_promise_chained");
      });

      queueMicrotask(() => {
        logs.push("3c_microtask_queueMicrotask");
      });

      logs.push("2_sync_end");
    }

    // Demonstration 2: Bounded Long Task (safety capped to max 2000ms)
    function triggerLongTask(targetMs) {
      const status = document.getElementById("long-task-status");
      // Strict safety cap: never exceed 2000ms
      const cappedMs = Math.min(Math.max(targetMs, 50), 2000);
      status.textContent = "Status: Executing " + cappedMs + "ms synchronous blocking loop on main thread...";

      // Give UI one tick to show status before locking main thread
      setTimeout(() => {
        const start = performance.now();
        let iters = 0;
        while (performance.now() - start < cappedMs) {
          iters++;
          // Busy wait on main thread
        }
        const elapsed = (performance.now() - start).toFixed(1);
        status.textContent = "Status: Block completed in " + elapsed + "ms (" + iters + " iterations). Notice that the frame counter paused while the box may have kept spinning!";
      }, 20);
    }

    // Demonstration 2b: Chunked yielding task
    function triggerChunkedTask(totalMs) {
      const status = document.getElementById("long-task-status");
      const cappedTotal = Math.min(Math.max(totalMs, 50), 2000);
      const chunkSizeMs = 50;
      let remaining = cappedTotal;
      const startOverall = performance.now();

      status.textContent = "Status: Starting chunked execution (" + cappedTotal + "ms in 50ms slices)...";

      function doChunk() {
        const start = performance.now();
        while (performance.now() - start < chunkSizeMs) {
          // Busy work slice
        }
        remaining -= chunkSizeMs;
        if (remaining > 0) {
          status.textContent = "Status: Running chunk... " + remaining + "ms remaining (UI stays responsive!)";
          setTimeout(doChunk, 0); // Yield control to event loop
        } else {
          const totalElapsed = (performance.now() - startOverall).toFixed(1);
          status.textContent = "Status: Chunked execution finished in " + totalElapsed + "ms total without freezing UI counter!";
        }
      }

      setTimeout(doChunk, 0);
    }
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


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class EventLoopServerFixture:
    """Manages the lifecycle of a loopback event loop test server on port 0."""

    def __init__(self, host="127.0.0.1"):
        self.host = host
        self.server = None
        self.thread = None
        self.port = None

    def start(self):
        self.server = ThreadedHTTPServer((self.host, 0), EventLoopHTTPHandler)
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
    fixture = EventLoopServerFixture()
    port = fixture.start()
    print("=" * 60)
    print(" Essential CS L12-04: Event Loop & Responsiveness Fixture")
    print("=" * 60)
    print(f" Listening on: http://127.0.0.1:{port}/")
    print(" Press Ctrl+C to stop.")
    print("-" * 60)
    print(" To observe in browser:")
    print(f"   1. Open: http://127.0.0.1:{port}/")
    print("   2. Run Demonstration 1 to verify microtask queue draining before timer tasks.")
    print("   3. Run Demonstration 2 to observe main-thread lockup vs compositor thread animation.")
    print("=" * 60)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping event loop fixture...")
    finally:
        fixture.stop()
        print("Stopped cleanly.")


if __name__ == "__main__":
    main()
