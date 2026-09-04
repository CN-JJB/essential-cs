# M12 Activity Suite — Web & Browser: The Integrated Case

These course-owned laboratory fixtures support Module 12 on `127.0.0.1` localhost only.

## Safety & Environment Invariants

- **Loopback & Port 0:** All listener sockets bind `127.0.0.1` and request dynamic OS-assigned port `0`. Hardcoded ports (such as `8000` or `9000`) are strictly forbidden;
- **Privilege & Network Boundaries:** Zero root/administrator privileges required; no public listeners, no firewall weakening, no proxy or host-file mutations;
- **Zero Hidden Automation:** No undeclared `Playwright`, `Puppeteer`, `Selenium`, or `Node.js` dependencies. Testing runs cleanly using Python standard library tooling;
- **Observation Truthfulness:** If a desktop GUI browser is available, observations reflect actual browser version and runtime output. If no GUI browser is present, record `NO LIVE BROWSER OBSERVATION`, `NO LIVE BROWSER CORS OBSERVATION`, and `NO LIVE DEVTOOLS OBSERVATION` truthfully and rely on course reference traces.

---

## Preflight Verification

Before starting activities, verify host capability:

```bash
python tests/preflight_network_web.py --json
```

---

## L12-01 — Browser Systems Architecture & Process Topology

- **Live Observation:** When a supported browser (Chromium/Chrome or Firefox) is available, launch it and open its internal Task Manager (`Shift+Esc` in Chrome) alongside the operating system process monitor (`Task Manager` on Windows, `ps aux` or `top` on Linux/macOS).
- **Inspection Focus:**
  - Locate the Browser Coordinator process, GPU Process, Network Service, and Tab/Renderer processes;
  - Verify that process count does not equal tab count (demonstrating why "one tab = one process" is false);
  - Observe how Site Isolation groups browsing contexts by site rather than strictly per tab.
- **Reference Mode:** If no GUI browser is available, record `NO LIVE BROWSER OBSERVATION` and proceed with EXP-03 source inspection.

---

## L12-02 — Document Rendering Pipeline Fixture

Start the pipeline demonstration server:

```bash
python labs/foundations/m12/rendering_fixture.py
```

- Binds to `http://127.0.0.1:<port>/`;
- Serves an HTML page containing external stylesheet, parser-blocking script (`/blocking.js?delay=0.3`), deferred script (`/deferred.js`), and async script (`/async.js`);
- Observe the parser pause at the classic script execution point, while the deferred script executes after HTML parsing is complete;
- Open DevTools Network and Performance panels to record the conceptual pipeline stages.

---

## L12-03 — Dual-Origin CORS & Web Security Model Fixture

Start the dual-origin CORS test suite:

```bash
python labs/foundations/m12/cors_fixture.py
```

- Spawns two independent servers on OS-assigned ports:
  - **Origin A:** `http://127.0.0.1:<portA>/` (Client Web Page)
  - **Origin B:** `http://127.0.0.1:<portB>/` (Target API)
- Demonstrates:
  1. **Simple Cross-Origin Request Blocked:** Browser sends `fetch()` from Origin A to Origin B. The HTTP request arrives at Origin B (logged in server memory), but the browser user agent withholds the response from JavaScript because `Access-Control-Allow-Origin` is absent;
  2. **Authorized Request Allowed:** When Origin B includes matching `Access-Control-Allow-Origin`, page script successfully reads the payload;
  3. **Preflighted Request:** A request with custom headers triggers a browser `OPTIONS` preflight before the actual request;
  4. **Non-Browser Contrast:** Command-line clients (`curl` or Python `urllib`) receive the response directly from Origin B. This proves CORS is enforced by browser user agents to protect client browsing sessions, not a server-side authorization barrier.

---

## L12-04 — Event Loop & Responsiveness Fixture

Start the event loop and long-task server:

```bash
python labs/foundations/m12/event_loop_fixture.py
```

- Binds to `http://127.0.0.1:<port>/`;
- **Ordering Test:** Verifies relative execution ordering: Synchronous code &rarr; Microtask queue (Promises, `queueMicrotask`) &rarr; Next Task (`setTimeout`);
- **Long-Task & Jank:** Triggers a bounded CPU loop (strictly capped at 2000ms max). Observe that the main-thread counter freezes while the CSS `transform` spinner may continue smoothly on the compositor thread;
- **Chunked Yielding:** Breaks heavy work into smaller slices yielding to the event loop, maintaining UI responsiveness.

---

## Source Expedition EXP-03 — Chromium Process Model & Site Isolation

EXP-03 is link-and-inspection-first:
- Read `book/12-web-browser-integrated-case/EXP-03-chromium-process-model-site-isolation.md`;
- Inspect the 3 verified paths on `chromium.googlesource.com`:
  1. `docs/process_model_and_site_isolation.md`
  2. `content/browser/site_instance_impl.cc`
  3. `content/browser/security/cpsp/child_process_security_policy_impl.cc`
- Complete the 5-item Bounded Inspection Card.

---

## Automated Test Suite & Reset

Run all M12 fixture tests:

```bash
python -m unittest discover -s labs/foundations/m12 -p "test_*.py" -v
```

Execute idempotent reset:

```bash
python labs/foundations/m12/reset.py
```
