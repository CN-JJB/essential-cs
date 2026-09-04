# LAB-REQ-01 — HTTP Interface, Origin & Intermediary Trace

LAB-REQ-01 is the required M11 localhost lab. It traces one HTTP request through an original Essential CS origin and bounded intermediary using the host's **real `curl -v`**.

## Safety and scope

- All listeners bind only `127.0.0.1`.
- All listeners request port `0`; record the actual OS-assigned ports.
- No public proxy, cloud account, credential, root/sudo, raw socket, packet injection, or system trust-store change is required.
- The intermediary accepts only the bounded course GET/HEAD subset. It is **not** an open proxy and does not support CONNECT/Upgrade tunneling.
- `502 Bad Gateway` for the stopped origin is a **course fixture policy**, not a universal mapping for every proxy/socket failure.

## Required components

```text
curl --HTTP/1.1--> IntermediaryAdapter --HTTP/1.1--> OriginServer
       |                   |                           |
       |                   +-- Connection-aware fields|
       |                   +-- truthful Via           +-- /resource: 200/304
       |                   +-- course 502 mapping      +-- /health: 200
```

- `origin_server.py`: localhost HTTP/1.1 origin, `/resource`, `/health`, ETag, conditional 304.
- `intermediary_adapter.py`: bounded GET/HEAD intermediary. Parses `Connection` options, removes nominated/known connection-specific fields, and appends `Via` using the protocol actually received.
- `harness.py`: owns the processes, waits for machine-readable readiness, performs health checks, runs the four real `curl -v` traces, stops/reaps children, and probes the old endpoints after cleanup.
- `test_lab.py`: unit/integration tests, including dynamic `Connection` token removal.
- `reset.py`: idempotent **no-persistent-artifact** reset. It does not claim to discover unknown old processes; lifecycle proof belongs to the harness.
- `course/evidence/lab-req-01-evidence-template.md`: reusable evidence form.

## curl is a Required-Lab gate

Run:

```bash
python tests/preflight_network_web.py --json
```

The lab requires a working `curl --version` result. If curl is missing or cannot execute, the lab disposition is:

```text
ENVIRONMENT_BLOCKED_NOT_RUN
TOOL MISSING: curl is required for LAB-REQ-01
```

A Python/manual HTTP client can be explanatory support only; it **cannot** satisfy LAB-REQ-01 in place of curl.

## Four-step trace

The harness runs curl with the bounded form:

```bash
curl -sS -v -i --http1.1 --max-time 5 ...
```

`-v` evidence is written by curl to stderr and is captured separately from the HTTP response in stdout.

### 1. Direct origin

```bash
curl -sS -v -i --http1.1 http://127.0.0.1:<origin_port>/resource
```

Expected relationship:
- HTTP/1.1 200;
- course ETag;
- non-empty representation;
- no course `Via`, because no course intermediary handled this hop.

### 2. Forwarded request

```bash
curl -sS -v -i --http1.1 http://127.0.0.1:<proxy_port>/resource
```

Expected relationship:
- HTTP/1.1 200;
- representation matches the direct course response;
- response contains a course `Via: 1.1 essential-cs-intermediary` entry because this fixture actually received HTTP/1.1 on the upstream hop.

The intermediary must not blindly forward `Connection` or fields named by its connection-options.

### 3. Conditional validation

```bash
curl -sS -v -i --http1.1 \
  -H 'If-None-Match: "<record actual course ETag>"' \
  http://127.0.0.1:<proxy_port>/resource
```

Expected relationship:
- 304 Not Modified;
- course Via and ETag metadata as applicable;
- **no response content/body**.

Do **not** require a `Content-Length: 0` field. The machine check is the absence of response content.

### 4. Controlled origin failure

The harness requests termination through its owned process handle, waits for the origin to be reaped, and checks that the old origin endpoint no longer accepts a new TCP connection. It then requests the still-running intermediary:

```bash
curl -sS -v -i --http1.1 http://127.0.0.1:<proxy_port>/resource
```

Expected relationship:
- course intermediary returns 502;
- response contains course Via;
- body identifies this as the course upstream-connection failure;
- no fixed OS errno, exception class, signal, or latency is an acceptance condition.

## Intermediary field rule

The course intermediary implements the essential RFC 9110 rule:

1. parse all values of the incoming `Connection` field;
2. remove `Connection` itself;
3. remove every field named by those connection-options;
4. remove known connection-specific fields handled by this bounded fixture;
5. reconstruct a clean next-hop message;
6. append a truthful `Via` entry for the protocol actually received.

Do not replace this algorithm with a static “hop-by-hop header list”.

## Lifecycle evidence

The harness records:
- origin/proxy readiness ports;
- health-check results;
- each child PID and whether it was reaped;
- whether escalation was required;
- the post-stop origin probe;
- post-final-cleanup probes for origin and intermediary endpoints.

Acceptance is semantic: old course endpoints must not accept a new connection. No specific refusal errno, exception text, signal, or millisecond threshold is required.

The standalone reset can be run twice:

```bash
python labs/lab_req_01/reset.py
python labs/lab_req_01/reset.py
```

It should report `CLEAN_NO_PERSISTENT_ARTIFACTS`; this only means no persistent course artifact needs deletion.

## Tests

```bash
python -m unittest discover -s labs/lab_req_01 -p "test_*.py" -v
```

If curl is unavailable, the full curl integration test is **skipped / NOT RUN**, while unit tests that do not require curl may still run. Do not relabel that skip as a Required-Lab PASS.
