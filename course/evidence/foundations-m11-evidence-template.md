# Foundations M11 Evidence Template — Networking II: TLS, HTTP, CDN & Proxies

Use this template for **actual execution evidence**. Do not pre-fill another host's cipher, exception, curl version, ports, timings, or tool availability.

## A — Execution identity / preflight

- Dispatch base: `f82847e7b4a63ccbb0ab1e4b7ad0cdd0d786d4df`
- Execution commit/ref: `<actual>`
- OS / kernel / architecture: `<actual>`
- Python implementation/version: `<actual>`
- Python `ssl.OPENSSL_VERSION` / TLS backend: `<actual>`
- TLS 1.3 capability: `<actual>`
- loopback port-0 bind/connect: `<actual>`
- curl path / `curl --version`: `<actual>`
- optional OpenSSL CLI: `<actual AVAILABLE / TOOL_UNAVAILABLE>`
- preflight disposition: `<actual>`
- OQ-BP-006: **OPEN**

## B — L11-01 TLS 1.3 course path

Normative/current anchors:
- RFC 9846 — current project TLS 1.3 authority; obsoletes RFC 8446.
- RFC 5280 — PKIX certificate-path validation.
- RFC 9525 — service identity; obsoletes RFC 6125.
- RFC 9849 — Encrypted Client Hello.

Course path:
- fresh certificate-authenticated TLS 1.3;
- DHE-based key establishment;
- dedicated course trust context;
- matching service identity.

Boundary:
- TLS 1.3 removed static RSA key exchange, but RSA can still be used for certificate signatures.
- DHE-based paths provide forward secrecy against later compromise of the long-term authentication key; PSK-only `psk_ke` does **not** have the same DHE forward-secrecy property.
- resumption / PSK / 0-RTT paths differ and are not collapsed into the fresh course handshake.

Record actual successful run:
- endpoint: `<actual loopback port>`
- negotiated TLS version: `<actual>`
- negotiated cipher: `<actual observation; not curriculum constant>`
- payload exchange: `<actual>`
- server worker reaped: `<actual>`

## C — Certificate path vs service identity

### Path / trust policy
Record:
- course CA loaded only into dedicated verification context: `<evidence>`
- system trust store modified? expected **NO**.
- certificate validity window: `<actual fixture>`
- relevant BasicConstraints / KeyUsage / EKU: `<actual fixture>`

### Service identity
Record:
- reference identity: `localhost`
- presented SAN identifiers: `<actual fixture>`
- RFC 9525 service-identity match result: `<actual>`

These are separate checks. A certificate path can be valid while the certificate belongs to a different service.

## D — Three controlled TLS cases

1. Trusted course CA + matching reference identity
   - disposition: success
   - actual runtime details: `<actual>`

2. Trusted course CA + deliberately mismatched reference identity
   - semantic disposition: service identity rejected
   - actual exception class/text: `<actual host evidence>`

3. Dedicated trust context that does not trust the course CA
   - semantic disposition: path/trust rejection
   - actual exception class/text: `<actual host evidence>`

Do **not** require one `SSLCertVerificationError` message/code across all Python/TLS backends.

## E — TLS trust boundary / ECH

Explain what the course observation supports:
- encrypted/authenticated TLS records protect application content according to the negotiated connection and verification policy;
- successful Web-PKI-style verification does not establish business legitimacy, authorization, endpoint-memory safety, or application correctness;
- normal non-ECH ClientHello SNI can expose a service name;
- successful ECH can protect the inner ClientHello/SNI, but IP endpoints, packet sizes/timing and provider/anonymity-set metadata remain outside that guarantee;
- ECH does not require one universal DoH/DoT deployment path.

No learner activity may disable certificate/service-identity verification.

## F — Course test PKI provenance

The committed `ca.key` and `server.key` are intentionally **public, non-secret localhost test fixtures**.

Record acknowledgement:
- never reuse these keys/certs for a real service;
- never install the course CA system-wide;
- learner Core uses committed fixture + Python stdlib `ssl`;
- `generate_certs.py` is optional maintenance tooling and can require third-party `cryptography`;
- the long fixture validity window is a maintenance choice, not a production/Web-PKI recommendation.

## G — L11-02 resource / representation / method semantics

Record one course HTTP observation:
- logical resource URI: `<actual>`
- representation media type/body: `<actual>`
- HTTP/1.1 protocol explicitly configured: `<evidence>`
- message content framing: `<actual>`

Method semantics:
- GET/HEAD are safe: the client does not request unsafe state change; incidental logging/accounting/cache work can still occur.
- PUT/DELETE are idempotent by RFC semantics: repeating the same request asks for the same **intended effect**; incidental side effects can differ.
- POST is not defined idempotent by default; the course POST endpoint specifically creates a new resource per submission.

For the PUT course fixture, record that identical full replacements produce the same resulting target state.

## H — HTTP status vs business outcome

Record the course `/business-failure` response:
- HTTP status: `<actual>`
- representation business status: `<actual>`

Explanation:
- `200 OK` reports success according to HTTP method semantics as represented by the server;
- it does not prove a domain/business invariant such as “funds transferred exactly once”.

## I — Partial failure / retry judgment

Explain:
- a communication timeout can leave remote application outcome ambiguous;
- idempotent methods have a stronger basis for automatic retry than non-idempotent methods, but this does not mean infinite/blind retry;
- application constraints such as versioning/concurrency, auth/quota, external side effects and retry budgets still matter;
- `If-Match`, stable operation IDs + deduplication, and query/reconciliation are possible mechanisms, not one universal required recipe.

## J — L11-03 freshness / validation

Record:
- course ETag: `<actual>`
- initial response status/body bytes: `<actual>`
- matching `If-None-Match` status: `304`
- 304 response content/body bytes: **0**
- mismatched validator status/body bytes: `<actual>`

Boundary:
- strong ETag is an opaque validator suitable for strong comparison, not inherently a hash;
- 304 has no response content; `Content-Length: 0` is **not required**;
- fresh stored responses can often be reused without revalidation when the full cache rules/request directives permit it; “fresh always means zero network work” is too broad.

## K — Intermediary / Via / failure

For LAB-REQ-01, record:
- `Connection` options parsed dynamically;
- fields named by `Connection` removed before forwarding;
- known connection-specific fields handled;
- `Via` received-protocol corresponds to the actual hop;
- stopped-origin connect failure maps to course `502`;
- actual host failure disposition recorded without fixed errno/exception/timing.

The 502 mapping is a **course policy**, not a universal proxy law.

## L — HTTP/1.1 / HTTP/2 / HTTP/3 judgment

Use mechanism language:
- HTTP/1.1 has no H2-style independent multiplexed streams; serial/pipelined/multi-connection behavior depends on client/server implementation.
- HTTP/2 multiplexes streams over one TCP connection; TCP loss/reordering can delay bytes needed by unrelated streams.
- HTTP/3 maps HTTP to QUIC streams; one stream's missing data need not block another stream's data delivery, while congestion control/path/CPU/resources remain shared factors.
- HTTPS HTTP/2 commonly uses TLS/ALPN, but HTTP/2 specification also defines a cleartext prior-knowledge path.
- no fixed browser connection count, packet-loss threshold, H3 CPU multiplier, or universal performance winner.

## M — Bounded Estimate

Illustrative assumptions only:
- origin RTT component = 100 ms;
- edge RTT component = 5 ms;
- representation size = 2 MiB;
- request rate = 10,000 req/s;
- cache hit ratio = 0.9.

Arithmetic:
- no-cache origin representation rate:
  `10,000 × 2 MiB/s = 20,000 MiB/s ≈ 19.53 GiB/s`
- 90%-hit origin representation rate:
  `10,000 × 0.1 × 2 MiB/s = 2,000 MiB/s ≈ 1.95 GiB/s`
- reduction in this simplified representation-egress model: 90%.
- weighted RTT component:
  `0.9 × 5 ms + 0.1 × (5 + 100) ms = 15 ms`.

Inference limits:
- these values are model inputs, **not observed Internet/CDN constants**;
- 15 ms is not full page latency or a TLS/HTTP handshake SLO;
- protocol overhead, object mix, cache fill/eviction, concurrency, origin fetch sharing and implementation are omitted;
- no hardware/cost reduction is inferred from the bandwidth ratio alone.

## N — Progressive support / visuals / safety

Record:
- each lesson has one collapsed `Question → Hint 1 → Hint 2 → Expected Observation → Full Explanation` ladder;
- no open-by-default details;
- all diagrams are original/editable;
- all runtime network endpoints are course-owned loopback;
- no public proxy/CDN/cloud account/root/sudo/raw-packet/system-trust-store mutation.

## O — Concepts / competencies / status

Canonical M11 revisits only:
- EC-CON-005 Interface
- EC-CON-010 Failure
- EC-CON-011 Caching
- EC-CON-012 Locality
- EC-CON-017 Trust Boundary

Future homes:
- EC-CON-014 Consistency remains M14/L14-02.
- EC-CON-015 Concurrency remains M15/L15-01.

M11 module primary competency: **Explain**.

Use only canonical competency names: Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, Learn-New-Tech.

This evidence does **not** constitute learner validation, VERIFIED, or RELEASED.
