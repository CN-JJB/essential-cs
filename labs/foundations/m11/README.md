# M11 Activity Suite — TLS, HTTP, Caching & Intermediaries

These course-owned activities support M11 on localhost only.

## Safety / environment

- listeners bind `127.0.0.1` and request port `0`;
- no public endpoint, proxy, cloud account, root/sudo, raw packet, or system trust-store modification;
- exact Python/TLS/curl versions are recorded at runtime; OQ-BP-006 remains OPEN;
- the external `openssl` CLI is optional;
- the `cryptography` package is used only by the optional certificate **regeneration** utility, not learner Core execution.

Run preflight:

```bash
python tests/preflight_network_web.py --json
```

M11 Core requires Python socket/ssl + TLS 1.3 capability. LAB-REQ-01 separately requires a working curl version probe.

## L11-01 — TLS fixture

```bash
python labs/foundations/m11/tls_fixture.py
```

The committed cert/key files are **public localhost test fixtures**, not secrets. Never reuse them for a real service and never install the course CA into a system-wide trust store.

The fixture pins this activity to TLS 1.3 and records:
1. trusted course CA + matching `localhost` service identity → success;
2. trusted course CA + mismatched reference identity → TLS client rejects;
3. dedicated trust context without course CA → TLS client rejects.

The actual negotiated cipher and actual runtime verification errors are observations, not curriculum constants.

Normative boundary:
- RFC 9846 current TLS 1.3 authority;
- RFC 5280 path validation;
- RFC 9525 service identity;
- RFC 9849 ECH.
- DHE-based TLS 1.3 paths provide the course forward-secrecy example; PSK-only `psk_ke` is a distinct boundary.

Certificate maintenance details are in `certs/README.md`.

## L11-02 — HTTP semantics observer

```bash
python labs/foundations/m11/http_semantics_observer.py
```

Observe:
- GET safe semantics: the client does not request unsafe state change; incidental effects can exist;
- course PUT performs a **full target-resource replacement** and repeating the same PUT requests the same intended effect;
- POST is not defined idempotent by default; this course POST endpoint creates a new resource per submission;
- `200 OK` does not establish business/domain correctness;
- HTTP/1.1 CRLF/header-section framing in a raw course trace.

## L11-03 — caching observer

```bash
python labs/foundations/m11/caching_observer.py
```

Observe:
- course ETag as opaque validator;
- matching conditional request → 304 with **no response content/body**;
- no requirement for `Content-Length: 0`;
- mismatched validator → representation transfer;
- H1/H2/H3 mechanism differences without a universal performance winner.

## Reset / tests

```bash
python -m unittest discover -s labs/foundations/m11 -p "test_*.py" -v
python labs/foundations/m11/reset.py
python labs/foundations/m11/reset.py
```

`reset.py` reports `CLEAN_NO_PERSISTENT_ARTIFACTS` because these in-process lesson fixtures create no persistent course artifact. Worker/listener teardown is checked by the activity/test while the handles are known; reset does not fabricate endpoint evidence.

LAB-REQ-01 has a separate required curl harness under `labs/lab_req_01/`.
