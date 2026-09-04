# LAB-REQ-01 Evidence Template: HTTP Intermediary Adapter, Conditional Caching & Upstream Failure Mapping

This evidence template records empirical host execution transcripts, protocol validation results, and lifecycle evaluations for **LAB-REQ-01**.

---

## A — Environment & Tooling Verification

- **Dispatch Base**: `f82847e7b4a63ccbb0ab1e4b7ad0cdd0d786d4df`
- **Execution Commit**: `<record exact commit>`
- **Execution Branch**: `<record exact branch>`
- **Host Operating System (`platform.system()`, `release`, `version`)**: `<record actual>`
- **Hardware Architecture (`platform.machine()`)**: `<record actual>`
- **Python Version (`platform.python_version()`)**: `<record actual>`
- **`curl` Binary Path**: `<record actual path, e.g. C:\WINDOWS\system32\curl.EXE or /usr/bin/curl>`
- **`curl` Version & Protocols**: `<record actual curl -V output, e.g. curl 8.21.0 with HTTP, HTTPS>`
- **Preflight Verification Disposition**: `<record READY_M11_CORE_AND_LAB_REQ_01>`

> This is a reusable evidence template. Author/Lead environment observations belong in the PR Completion Report or filled evidence instance, **not** as canonical pre-populated learner evidence.

---

## B — Component Dynamic Port Allocation

- **Origin Server**:
  - Bound Address: `127.0.0.1:0`
  - Allocated Port Observed: `<record empirical port, e.g. 62669>`
  - Readiness Handshake Output: `ORIGIN_READY_PORT=<port>`
- **Intermediary Adapter (Reverse Proxy)**:
  - Bound Address: `127.0.0.1:0`
  - Target Upstream: `127.0.0.1:<origin_port>`
  - Allocated Port Observed: `<record empirical port, e.g. 62670>`
  - Readiness Handshake Output: `PROXY_READY_PORT=<port>`
- **Zero Port Conflict Invariant**:
  - Both components dynamically bind port `0`. Zero hardcoded ports.

---

## C — Step 1: Direct Request to Origin Server (Uncached Baseline)

- **Execution Command**:
  ```bash
  curl -s -i http://127.0.0.1:<origin_port>/resource
  ```
- **Observed HTTP Status Line**: `HTTP/1.1 200 OK`
- **Observed Headers**:
  - `Content-Type: application/json`
  - `ETag: "strong-v1"`
  - `Cache-Control: max-age=60, must-revalidate`
- **Observed Response Body**:
  - Body Byte Count: `96` bytes
  - Content Excerpt: `{"message": "Hello from origin server", "version": 1, "status": "active", "authoritative": true}`
- **Disposition**: `STEP_1_DIRECT_ORIGIN_PASS`

---

## D — Step 2: Forwarded Request via Intermediary Adapter

- **Execution Command**:
  ```bash
  curl -s -i http://127.0.0.1:<proxy_port>/resource
  ```
- **Observed HTTP Status Line**: `HTTP/1.1 200 OK`
- **Observed Injected Headers**:
  - `Via: 1.1 essential-cs-intermediary`
  - `ETag: "strong-v1"`
- **Hop-by-hop Header Compliance (RFC 9110 Section 7.6.1)**:
  - Headers `Connection`, `Keep-Alive`, `Upgrade`, `Transfer-Encoding` are stripped before forwarding.
- **Payload Verification**:
  - Body matches Step 1 byte-for-byte (`96` bytes).
- **Disposition**: `STEP_2_PROXY_FORWARD_PASS`

---

## E — Step 3: Conditional Request via Intermediary Adapter

- **Execution Command**:
  ```bash
  curl -s -i -H 'If-None-Match: "strong-v1"' http://127.0.0.1:<proxy_port>/resource
  ```
- **Observed HTTP Status Line**: `HTTP/1.1 304 Not Modified`
- **Observed Headers**:
  - `Via: 1.1 essential-cs-intermediary`
  - `ETag: "strong-v1"`
- **Zero Body Bytes Verification (RFC 9111 Section 4.1)**:
  - Observed Body Byte Count: **`0` bytes** (strictly zero payload bytes following header demarcation `\r\n\r\n`).
- **Disposition**: `STEP_3_CONDITIONAL_304_PASS`

---

## F — Step 4: Upstream Failure Mapping (Origin Terminated)

- **Origin Termination Action**:
  - Origin process sent `SIGTERM` / `.terminate()` and reaped.
  - Verified process terminated: `origin_proc.poll() is not None`.
- **Execution Command**:
  ```bash
  curl -s -i http://127.0.0.1:<proxy_port>/resource
  ```
- **Observed HTTP Status Line**: `HTTP/1.1 502 Bad Gateway`
- **Observed Headers**:
  - `Via: 1.1 essential-cs-intermediary`
  - `Content-Type: application/json`
- **Observed Error Body**:
  - Contains structured failure diagnostic: `{"error": "Bad Gateway", "reason": "Origin server unreachable...", "upstream": "127.0.0.1:<origin_port>"}`
- **Disposition**: `STEP_4_UPSTREAM_FAILURE_502_PASS`

---

## G — Process Lifecycle & Orphan Cleanup

- **Process Tracking**: All child subprocesses (origin server, proxy adapter) tracked in `ProcessManager`.
- **Cleanup Guarantee**: `finally:` block executes `terminate()` followed by `kill()` watchdog.
- **Post-Run Process Audit**: Zero lingering origin or proxy listener processes.

---

## H — Reset Script Verification

- **Command Run**: `python labs/lab_req_01/reset.py`
- **First Invocation Output**: `LAB_REQ_01_RESET_OK: CLEAN_NO_PERSISTENT_ARTIFACTS`
- **Second Invocation Output (Idempotency)**: `LAB_REQ_01_RESET_OK: CLEAN_NO_PERSISTENT_ARTIFACTS`
- **Exit Code**: `0`
