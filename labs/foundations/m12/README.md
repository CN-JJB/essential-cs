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

# EXP-03 only: opt in to the public Chromium-source currentness probe
python tests/preflight_network_web.py --json --check-chromium-source
```

---

## L12-01 — Browser Systems Architecture & Process Topology

- **Live Observation:** When a real desktop browser GUI is available, record the exact browser/version/platform and compare its internal task/process view with the OS process monitor.
- **Inspection Focus:**
  - Record the process/service labels actually shown; do **not** require every build/platform to expose Browser/GPU/Network Service as one fixed set of OS processes;
  - compare observed process count/roles with tab/frame count without expecting a fixed ratio;
  - use EXP-03 source/current-practice evidence to interpret SiteInstance/Site Isolation. A task-manager screenshot alone does not prove the exact process-assignment policy.
- **Reference Mode:** If no GUI browser is available, record `NO LIVE BROWSER OBSERVATION` and proceed with EXP-03 source inspection.

---

## L12-02 — Document Rendering Pipeline Fixture

Start the pipeline demonstration server:

```bash
python labs/foundations/m12/rendering_fixture.py
```

- Binds to `http://127.0.0.1:<port>/`;
- Serves an HTML page containing external stylesheet, parser-blocking script (`/blocking.js?delay=0.3`), deferred script (`/deferred.js`), and async script (`/async.js`);
- In a **real browser**, use course event markers to observe parser-blocking classic-script vs classic `defer` relative ordering;
- DevTools Network/Performance observations are capability-gated and browser-version-specific. If no real browser runs the page, Python tests verify only asset/server structure and you must record `NO LIVE BROWSER PARSER-ORDER OBSERVATION` / `NO LIVE DEVTOOLS OBSERVATION`.

---

## L12-03 — Dual-Origin CORS & Web Security Model Fixture

Start the dual-origin CORS test suite:

```bash
python labs/foundations/m12/cors_fixture.py
```

- Spawns two independent servers on OS-assigned ports:
  - **Origin A:** `http://127.0.0.1:<portA>/` (Client Web Page)
  - **Origin B:** `http://127.0.0.1:<portB>/` (Target API)
- With a **real browser**, the page can demonstrate the simple-request / matching-ACAO / preflight paths. Record actual browser behavior; without one, use `NO LIVE BROWSER CORS OBSERVATION`.
- Raw automated tests prove only the course server's HTTP arrival and CORS-header policy; they do not execute browser enforcement.
- The authorized course response permits **only this run's dynamic Origin A**; the server does not reflect arbitrary Origin values.
- Non-browser `curl`/Python may receive the public course endpoint response because they do not enforce browser CORS response filtering; this is not a bypass of server authentication/authorization.

---

## L12-04 — Event Loop & Responsiveness Fixture

Start the event loop and long-task server:

```bash
python labs/foundations/m12/event_loop_fixture.py
```

- Binds to `http://127.0.0.1:<port>/`;
- **Ordering Test:** a real browser can record relative ordering: synchronous code &rarr; Promise/`queueMicrotask` reactions &rarr; later timer task. Static Python tests do not prove JS scheduling;
- **Long-Task & Jank:** course CPU loop is capped at 1500ms. Record main-thread delay in the actual browser; the CSS `transform` spinner is only a compositor-friendly candidate and may continue, stutter, or stop depending on implementation/runtime;
- **Chunked Yielding:** current fixture uses 20ms course work slices with `setTimeout` re-queueing. Compare observed responsiveness; do not treat 20ms as a universal smoothness threshold.

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
