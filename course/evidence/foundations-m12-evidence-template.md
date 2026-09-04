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
- Default local preflight Chromium-source disposition: `NO LIVE CHROMIUM SOURCE RECHECK` / reason `NOT_REQUESTED`
- EXP-03 opt-in command: `python tests/preflight_network_web.py --json --check-chromium-source`
- Opt-in Chromium source access disposition: `LIVE_CHROMIUM_SOURCE_ACCESSIBLE` / `NO LIVE CHROMIUM SOURCE RECHECK`
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
- **Chromium current-practice evidence:** desktop builds use Full Site Isolation in the current process-model documentation; Chrome for Android has Partial/No Site Isolation modes depending on current platform/resource policy. Record the exact source revision/date rather than turning a current threshold into curriculum law.
- OOPIF/process assignment is implementation evidence, not a Web Platform guarantee.
- Motivation: defense in depth against compromised renderers and Spectre-like speculative-execution threats. Do not claim Site Isolation eliminates every side channel.

---

## E — L12-02 Conceptual Rendering Pipeline

Confirm tracing of the 6 conceptual stages:
1. HTML parse &rarr; DOM
2. CSS parse &rarr; style rules / CSSOM conceptual data
3. Style resolution &rarr; styled boxes / implementation-specific layout structures
4. Layout &rarr; geometry
5. Paint &rarr; implementation-specific drawing records
6. Compositing / rasterization &rarr; displayable pixels

Marked explicitly as: **CONCEPTUAL PIPELINE**. Incremental invalidation, caching, thread assignment, layer structure, software/GPU rasterization and DevTools labels are implementation/runtime evidence.

---

## F — Parser-Blocking vs. Defer Structural Evidence

Record the course fixture structure:
- Server dynamic port: `<actual port>`
- parser-blocking classic script URL/delay parameter: `<actual fixture config>`
- classic `defer` asset present: `<actual fixture config>`

If a **real browser** was used, separately record actual browser event-marker evidence supporting parser-blocking / defer ordering. If no real browser executed the page, record `NO LIVE BROWSER PARSER-ORDER OBSERVATION`; Python HTTP tests verify only the served asset/header structure, not JavaScript parser scheduling.

Inference boundary: `defer` changes parser interaction but does not guarantee FCP ordering or milliseconds.

---

## G — Live DevTools Evidence or Truthful Reference Mode

- If DevTools Performance panel was recorded:
  - Network waterfall & execution rows: `<actual trace>`
- If no GUI browser used:
  - Disposition: `NO LIVE DEVTOOLS OBSERVATION`
  - No DevTools/parser/rendering timing is claimed. Course fixture structure and specification/reference material remain separate evidence.

---

## H — Origin Tuple vs. Opaque-Origin Explanation

- Tuple Origin: `(scheme, host, port)`
- Opaque Origin: an implementation-internal opaque value with serialization commonly `null` in relevant serialization contexts; distinct opaque origins are not made equal merely because they serialize alike.
- Contrast with Site: in Chromium Full Site Isolation current process-model context, site locks commonly use scheme + eTLD+1; this is not a universal Web-wide definition and is not an origin synonym.

---

## I — Same-Origin Policy vs. Cookie Rule Separation

- SOP governs: DOM tree access, `localStorage`, `sessionStorage`, `indexedDB`, and JavaScript read access to HTTP responses.
- Cookie rules govern storage/transmission under their own host/domain/path/Secure/SameSite/etc. rules.
  - Port is not a Cookie domain/path matching key, so different ports on the same host are not independently cookie-scoped.
  - Actual sending still depends on host-only/Domain, Path, Secure, SameSite, expiry and request context.
  - `HttpOnly` restricts script access; it is not part of the network-domain matching rule.

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
  - Automated tests establish only that the raw HTTP course request reached Origin B and whether ACAO/preflight headers were present. They **do not** prove browser CORS enforcement.

---

## K — Authorized CORS Evidence

If a real browser was used:
- record whether JavaScript could read the matching-ACAO response;
- record actual preflight/actual-request behavior without fixed console wording.

Without a real browser:
- record `NO LIVE BROWSER CORS OBSERVATION`;
- raw tests may verify the course server's matching ACAO policy and bounded `OPTIONS` response shape, but must not label that a browser CORS PASS.

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
- Long Tasks API document status (if referenced for the 50 ms reporting threshold): **W3C Working Draft (19 March 2026)**.
- Defense in depth: Restricts script sources and fetch destinations; mitigates XSS data exfiltration.
- Does not replace input validation or secure coding.

---

## N — L12-04 Task/Microtask Relative Ordering Evidence

If a real browser executes `labs/foundations/m12/event_loop_fixture.py`, record the actual relative log order. For the committed fixture, the expected relation is synchronous start/end → first Promise reaction → already-queued `queueMicrotask` callback → chained Promise reaction (enqueued only after the first reaction resolves) → later timer task. Record the browser's actual output; do not add milliseconds as acceptance criteria.

If no real browser executes the JavaScript, record `NO LIVE BROWSER EVENT-LOOP OBSERVATION`; Python/static tests can verify that the fixture contains the intended code but cannot prove browser scheduling.

---

## O — Long-Main-Thread-Task Observation & Compositor Caveat

- Course long-task fixture is bounded below 2 seconds (current cap 1500 ms).
- With a real browser, record the actual delay in same-window main-thread handlers/rAF updates.
- Record whether the CSS transform candidate continued, stuttered, or stopped; compositor promotion is browser/runtime evidence and is **not guaranteed**.
- Without a real browser: `NO LIVE BROWSER LONG-TASK/COMPOSITOR OBSERVATION`.

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
