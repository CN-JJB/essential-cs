# LAB-REQ-01 Evidence Template — HTTP Interface, Origin & Intermediary Trace

Use this form for one **actual execution**. Do not copy example ports, versions, errors, or transcripts from another host.

## A — Execution identity and capability

- Dispatch base: `f82847e7b4a63ccbb0ab1e4b7ad0cdd0d786d4df`
- Execution commit/ref: `<actual>`
- OS / kernel / architecture: `<actual>`
- Python implementation/version: `<actual>`
- curl path: `<actual>`
- full `curl --version` evidence: `<actual>`
- preflight disposition: `<actual>`
- LAB-REQ-01 disposition: `PASS` / `ENVIRONMENT_BLOCKED_NOT_RUN`

If curl is missing or its version probe cannot execute, stop the Required-Lab trace and record:

```text
TOOL MISSING: curl is required for LAB-REQ-01
ENVIRONMENT_BLOCKED_NOT_RUN
```

Do not substitute Python-client evidence for a curl PASS.

## B — Readiness and dynamic endpoints

- Origin readiness line: `ORIGIN_READY_PORT=<actual>`
- Origin health check: `<actual>`
- Intermediary readiness line: `PROXY_READY_PORT=<actual>`
- Intermediary health check through origin: `<actual>`
- Both listeners bound only to `127.0.0.1`: `<evidence>`

## C — Step 1 direct curl trace

Command:

```bash
curl -sS -v -i --http1.1 http://127.0.0.1:<origin_port>/resource
```

Record:
- command argv/display: `<actual>`
- curl return code: `<actual>`
- **curl verbose stderr trace**: `<actual>`
- status line: `<actual>`
- ETag: `<actual>`
- body byte count: `<actual>`
- course Via present? expected **NO**: `<actual>`

## D — Step 2 forwarded curl trace

Command:

```bash
curl -sS -v -i --http1.1 http://127.0.0.1:<proxy_port>/resource
```

Record:
- curl verbose stderr trace: `<actual>`
- status: `<actual>`
- Via: `<actual>`
- ETag: `<actual>`
- body matches direct representation: `<actual>`

Intermediary audit:
- incoming `Connection` options parsed: `<test/evidence>`
- fields named by `Connection` removed: `<test/evidence>`
- known connection-specific fields handled: `<test/evidence>`
- Via received-protocol agrees with actual HTTP hop: `<evidence>`

## E — Step 3 conditional 304

Command:

```bash
curl -sS -v -i --http1.1 \
  -H 'If-None-Match: <actual ETag>' \
  http://127.0.0.1:<proxy_port>/resource
```

Record:
- curl verbose stderr trace: `<actual>`
- status: `304`
- Via / ETag metadata: `<actual>`
- response content/body byte count: **0**
- `Content-Length: 0` required? **NO**

## F — Step 4 course upstream failure

Record:
- harness process-stop record for origin: `<actual>`
- origin child reaped? `<actual>`
- old-origin endpoint connection established? expected **false**: `<actual raw probe>`
- actual host probe result/exception: `<actual; not a fixed acceptance value>`
- curl verbose stderr trace to intermediary: `<actual>`
- status: `502`
- Via: `<actual>`
- response body: `<actual course diagnostic>`

Boundary statement:
- This refusal/connect-failure → 502 mapping is a **LAB-REQ-01 course policy**, not a universal proxy law.

## G — Final cleanup

Record harness final cleanup:
- owned process records: `<actual>`
- all owned children reaped: `<actual>`
- old origin endpoint accepts new connection? expected **false**: `<actual>`
- old intermediary endpoint accepts new connection? expected **false**: `<actual>`
- cleanup escalation, if any: `<actual>`

No fixed POSIX signal, Windows status, errno, exception text, or latency is required.

## H — Standalone reset

Run twice:

```bash
python labs/lab_req_01/reset.py
python labs/lab_req_01/reset.py
```

Record outputs: `<actual>`.

`CLEAN_NO_PERSISTENT_ARTIFACTS` means only that no persistent course artifact requires deletion; lifecycle proof comes from Section G.

## I — Reviewer judgment

Explain:
- direct vs forwarded path;
- why Via is a hop trace rather than an application-business result;
- why connection-specific fields cannot be blindly forwarded;
- why 304 has no response content but does not require `Content-Length: 0`;
- where the course 502 was generated;
- why localhost trace timing/performance cannot be generalized to a CDN/WAN.
