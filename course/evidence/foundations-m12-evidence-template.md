# Foundations M12 Evidence Template — Web & Browser: The Integrated Case

Use this template for **actual execution and verification evidence**. Do not pre-fill another host's browser version, process counts, timings, or console messages.

---

## A — Actual Environment & Capability Preflight

Record empirical preflight data from `python tests/preflight_network_web.py --json`:
- Dispatch base: `8e271f8c827178b4a36b97c620a553ede34d467d`
- Execution commit / ref: `<actual>`
- OS / kernel / architecture: `<actual>`
- Python implementation / version: `<actual>`
- Loopback port 0 dynamic allocation: `<actual>`
- Browser binary detection: `<actual path / version or NONE>`
- GUI capability disposition: `NO LIVE BROWSER OBSERVATION` / `<actual>`
- Browser CORS observation disposition: `NO LIVE BROWSER CORS OBSERVATION` / `<actual>`
- DevTools observation disposition: `NO LIVE DEVTOOLS OBSERVATION` / `<actual>`
- Chromium source access disposition: `LIVE_CHROMIUM_SOURCE_ACCESSIBLE` / `NO LIVE CHROMIUM SOURCE RECHECK`
- curl path / version: `<actual>`
- OQ-BP-006 status: **OPEN**

---

## B — L12-01 Web Spec vs. Chromium Implementation Separation

Confirm the strict 4-layer evidence discipline:
1. **Web Platform specification**: Defines Document, Window, Browsing Context, Agent Cluster, Origin, and SOP rules.
2. **Chromium implementation / current practice**: Defines Browser process, Sandboxed Renderers, GPU process, Network Service, SiteInfo, SiteInstance, and Site Isolation process locks.
3. Explicit label in curriculum diagrams:
   `IMPLEMENTATION / CURRENT PRACTICE — NOT WEB PLATFORM SPEC`
4. Confirm negative guardrails:
   - No claim that "one tab = one process";
   - No claim that "one site = one process" is a universal cross-platform invariant;
   - No claim that all browsers share Chromium's multi-process architecture;
   - No claim that Site Isolation equals the Same-Origin Policy.

---

## C — Live Process Observation or Truthful Reference Mode

- If desktop browser GUI was available:
  - Browser name & exact version: `<actual>`
  - Internal Task Manager (`Shift+Esc`) observations: `<actual process rows>`
  - OS process monitor comparison: `<actual>`
- If running in headless/CI/non-interactive terminal:
  - Disposition: `NO LIVE BROWSER OBSERVATION`
  - Reference evidence mode: Course reference process topology and EXP-03 source inspection used.

---

## D — Site Isolation Platform & Current-Practice Boundary

Record understanding of Site Isolation boundaries:
- Desktop Chromium: Full Site Isolation defaults on, isolating cross-site iframes into Out-Of-Process Iframes (OOPIF).
- Mobile / low-memory devices: Full site isolation may be disabled or limited (e.g., password-triggered site isolation) due to OS process limits and RAM constraints.
- Motivation: Defense in depth against compromised renderers (UXSS) and microarchitectural speculative execution attacks (Spectre / Meltdown).

---

## E — L12-02 Conceptual Rendering Pipeline

Confirm tracing of the 6 conceptual stages:
1. HTML Parse &rarr; DOM Tree
2. CSS Parse &rarr; CSSOM Tree
3. Style Resolution &rarr; Render / Layout Tree (Computed Styles)
4. Layout / Reflow &rarr; Geometry Coordinates (Box Model)
5. Paint &rarr; Display Lists (Draw Commands)
6. Compositing &rarr; Layer Tiles to GPU Framebuffer

Marked explicitly as: **CONCEPTUAL PIPELINE**. Modern engines apply dirty-subtree invalidations, layer caching, and off-thread compositing.

---

## F — Parser-Blocking vs. Defer Structural Evidence

Record output from `labs/foundations/m12/rendering_fixture.py`:
- Server dynamic port: `<actual port>`
- Classical synchronous script (`/blocking.js?delay=0.3`):
  - Injected delay: `0.3s`
  - Parser observation: Later HTML parsing markers paused until script fetch and execution finished.
- Classical `defer` script (`/deferred.js`):
  - Fetched in parallel during parsing;
  - Executed strictly after DOM parsing completed and before `DOMContentLoaded`.
- Inference boundary: `defer` alters the critical path but does not provide an absolute machine guarantee that FCP occurs first.

---

## G — Live DevTools Evidence or Truthful Reference Mode

- If DevTools Performance panel was recorded:
  - Network waterfall & execution rows: `<actual trace>`
- If no GUI browser used:
  - Disposition: `NO LIVE DEVTOOLS OBSERVATION`
  - Structural ordering confirmed via fixture progress timestamps.

---

## H — Origin Tuple vs. Opaque-Origin Explanation

- Tuple Origin: `(scheme, host, port)`
- Opaque Origin: Internal unguessable identifier serialized as `"null"` (e.g., `data:` URLs, sandboxed `<iframe>` without `allow-same-origin`).
- Contrast with Site: Site is typically `scheme + eTLD+1` in Chromium desktop practice; not an origin synonym.

---

## I — Same-Origin Policy vs. Cookie Rule Separation

- SOP governs: DOM tree access, `localStorage`, `sessionStorage`, `indexedDB`, and JavaScript read access to HTTP responses.
- Cookie rules govern: Browser cookie transmission.
  - **Ignores port by default**: A cookie set for `example.com` is sent to `http://example.com:8080` and `http://example.com:9000`.
  - Scoped by: `Domain`, `Path`, `SameSite`, `HttpOnly`, `Secure`.

---

## J — CORS Simple-Request Browser Evidence or Truthful Mode

- Using `labs/foundations/m12/cors_fixture.py`:
  - Origin A: `http://127.0.0.1:<portA>`
  - Origin B: `http://127.0.0.1:<portB>`
- If live browser was used:
  - Simple `fetch()` from Origin A to Origin B without ACAO;
  - Browser console recorded CORS violation exception;
  - Origin B request log proved the HTTP request **arrived and executed** on the server.
- If no live browser used:
  - Disposition: `NO LIVE BROWSER CORS OBSERVATION`
  - Proven via course automated test suite asserting server request arrival and header absence.

---

## K — Authorized CORS Browser Evidence

- When Origin B returned `Access-Control-Allow-Origin: http://127.0.0.1:<portA>`:
  - Browser JavaScript successfully resolved Promise and read response JSON.
- Deterministic preflight:
  - Request with `X-Course-Custom` sent `OPTIONS` probe;
  - Origin B returned 204 with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`.

---

## L — Non-Browser Course-Endpoint Contrast

- Terminal / Python client executed against `http://127.0.0.1:<portB>/api/data?mode=unauthorized`:
  - HTTP Status: `200 OK`
  - Response body: Received directly without browser CORS filtering.
- Boundary confirmed:
  - Non-browser clients are not executing untrusted web scripts;
  - "curl does not enforce browser CORS response blocking" does NOT mean "curl bypasses all server security";
  - Server authentication and authorization remain completely independent.

---

## M — CSP Defense-in-Depth Judgment & Document Status

- CSP Level 3 document status: **W3C Working Draft (13 August 2026)**.
- Defense in depth: Restricts script sources and fetch destinations; mitigates XSS data exfiltration.
- Does not replace input validation or secure coding.

---

## N — L12-04 Task/Microtask Relative Ordering Evidence

Record relative ordering from `labs/foundations/m12/event_loop_fixture.py`:
- `1_sync_start`
- `2_sync_end`
- `3_microtask_promise_1`
- `3b_microtask_promise_chained`
- `3c_microtask_queueMicrotask`
- `4_timer_task`
- Microtask queue drained completely at microtask checkpoint before timer task ran.

---

## O — Long-Main-Thread-Task Observation & Compositor Caveat

- Configurable long task executed under strict safety cap (< 2.0s):
  - Main-thread rAF counter froze during execution;
  - User interaction delayed;
  - GPU-accelerated CSS `transform` spinner on Compositor thread continued rotating smoothly.
- Invariant confirmed: Do NOT claim all CSS animations freeze; Compositor thread concurrency handles independent transform layers.

---

## P — Frame-Budget Estimate with Explicit Assumptions

- At 60 Hz display refresh: Frame interval $\approx 1000/60 \approx 16.7\text{ ms}$.
- At 120 Hz display refresh: Frame interval $\approx 1000/120 \approx 8.3\text{ ms}$.
- Frame budget is an illustrative Estimate under specific hardware assumptions; modern browsers do not operate on a hardcoded global 16.7 ms law.

---

## Q — Concept, Future-Home & Competency Audit

- Canonical Concept Revisits:
  - `EC-CON-018` Process (First home: M06 L06-01) &rarr; Revisit in L12-01.
  - `EC-CON-013` Isolation (First home: M07 L07-01) &rarr; Revisit in L12-01, L12-03.
  - `EC-CON-005` Interface (First home: M00 L00-01) &rarr; Revisit in L12-02.
  - `EC-CON-017` Trust Boundary (First home: M07 L07-01) &rarr; Revisit in L12-03.
- Future-Home Guardrails:
  - `EC-CON-014` Consistency: **NOT DEFINED** (reserved for M14 L14-02).
  - `EC-CON-015` Concurrency: **NOT DEFINED** (reserved for M15 L15-01; L12-04 is Concurrency preview only).
- Module Primary Competency: **Observe**.
- Canonical Competencies used: Observe, Trace, Explain, Judge, Diagnose, Estimate.

---

## R — Progressive-Support, Visual, Source & Safety Audit

- Progressive Support:
  - L12-01: 5-step ladder present; 0 `open` attributes.
  - L12-02: 5-step ladder present; 0 `open` attributes.
  - L12-03: 5-step ladder present; 0 `open` attributes.
  - L12-04: 5-step ladder present; 0 `open` attributes.
- Visuals: Original ASCII/Markdown diagrams with explicit boundary disclaimers.
- Safety: All sockets bind `127.0.0.1:0`; no root; no host-file or firewall modifications; no hidden browser automation dependencies.
