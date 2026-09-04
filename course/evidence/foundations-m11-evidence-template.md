# Foundations M11 Evidence Template: Networking II (TLS, HTTP, CDN & Proxies)

This evidence template records empirical host execution results, claim boundaries, and architectural evaluations for **M11 — Networking II: TLS, HTTP, CDN & Proxies**.

---

## A — Actual Environment / Python / Capability Preflight

- **Dispatch Base**: `f82847e7b4a63ccbb0ab1e4b7ad0cdd0d786d4df`
- **Execution / Working Commit**: `<record the exact commit actually executed>`
- **Execution Branch / Ref**: `<record the actual branch or detached ref>`
- **Host Operating System (`platform.system()`, `release`, `version`)**: `<record actual>`
- **Hardware Architecture (`platform.machine()`)**: `<record actual>`
- **Python Implementation & Version (`platform.python_implementation()`, `python_version()`)**: `<record actual>`
- **OpenSSL Runtime Version (`ssl.OPENSSL_VERSION`)**: `<record actual>`
- **TLS 1.3 Protocol Support (`ssl.HAS_TLSv1_3`)**: `<record actual True / False>`
- **Loopback Bind Port 0 Capability (`can_bind_port_0`)**: `<record actual True / False>`
- **Loopback Connect Capability (`can_connect_loopback`)**: `<record actual True / False>`
- **`curl` Binary Availability (`which curl` / version)**: `<record actual path and version, e.g. curl 8.21.0>`
- **Preflight Verification Script Disposition**: `<record READY_M11_CORE_AND_LAB_REQ_01 or exact output>`

> This is a reusable evidence template. Author/Lead environment observations belong in the PR Completion Report or filled evidence instance, **not** as canonical pre-populated learner evidence.

---

## B — L11-01 TLS 1.3 Handshake & X.509 Dual-Pillar Verification

- **TLS 1.3 Architectural Redesign**:
  1. **Mandatory Forward Secrecy**: Static RSA key exchange is completely abolished in TLS 1.3; ephemeral Diffie-Hellman ((EC)DHE) is strictly enforced.
  2. **Handshake Latency**: 1-RTT standard handshake (reduced from TLS 1.2's 2-RTT); 0-RTT PSK is optional with explicit replay vulnerability boundaries.
  3. **Metadata Confidentiality**: Server certificate, extensions, and handshake transcript signatures are encrypted over the wire; only initial `ClientHello` remains plaintext (unless ECH is active).
- **Dual-Pillar X.509 Verification State Machine**:
  - **Pillar 1: Path / Chain Validation**: Validates signature chain backwards from leaf certificate to local trusted Root CA anchor in client trust store; checks validity dates and RFC 5280 extensions (`BasicConstraints`, `KeyUsage`, `ExtendedKeyUsage`).
  - **Pillar 2: Subject Alternative Name (SAN) Identity Matching**: RFC 6125 requires matching expected request host against SAN extension entries (`DNS:` or `IP:`). Common Name (CN) is obsolete.
  - *Invariant*: Both pillars must pass simultaneously. A valid CA signature on an unrelated host certificate (`attacker.com`) must be rejected when accessing `bank.example.com`.

---

## C — Controlled Test PKI Endpoint Observations (3 Discrete Cases)

- **Command Run**: `python labs/foundations/m11/tls_fixture.py`
- **PKI Parameters**: Course-owned test Root CA (`ca.pem`), Leaf Server Certificate (`server.pem` with SAN `DNS:localhost, IP:127.0.0.1`), Untrusted Test CA (`untrusted_ca.pem`). All certs generated with 10-year validity (RFC 5280 conformant).
- **Case 1 (Trusted Root CA + Matching SAN `localhost`)**:
  - Disposition: `TLS_HANDSHAKE_SUCCESS`
  - Negotiated Protocol: `TLSv1.3`
  - Negotiated Cipher Suite: `<record empirical suite, e.g. TLS_AES_256_GCM_SHA384>`
  - Bypass Flags: **ZERO** (`verify_mode=CERT_REQUIRED`, `check_hostname=True`).
- **Case 2 (Trusted Root CA + Mismatched SAN `wrong.example.internal`)**:
  - Disposition: `HOSTNAME_MISMATCH_REJECTED`
  - Observed Exception: `ssl.SSLCertVerificationError` (Certificate hostname mismatch)
  - Connection State: Terminated immediately; no application bytes sent.
- **Case 3 (Untrusted Root CA + Matching SAN `localhost`)**:
  - Disposition: `UNTRUSTED_ROOT_REJECTED`
  - Observed Exception: `ssl.SSLCertVerificationError` (Self-signed certificate in certificate chain / untrusted issuer)
  - Connection State: Terminated immediately; no application bytes sent.

---

## D — Trust Boundary Demarcation (EC-CON-017)

- **What TLS Guarantees**:
  - Confidentiality of data transmitted across untrusted network links against passive eavesdropping.
  - Integrity of in-flight records against active tampering and packet injection (via AEAD ciphers).
  - Authenticity of the server endpoint identity (under strict dual-pillar validation).
- **What TLS Does NOT Guarantee**:
  - Does NOT guarantee application software security (SQL injection, XSS, unauthorized API access).
  - Does NOT guarantee host memory integrity or endpoint defense against compromise/malware.
  - Does NOT protect against an attacker possessing a compromised or rogue root certificate installed in the client's local OS trust store.
  - Does NOT hide SNI destination host from network eavesdroppers unless Encrypted Client Hello (ECH) is deployed.
- **Bypass Prohibition**:
  - Flags such as `verify=False`, `check_hostname=False`, and `curl -k` strip both verification pillars, completely abolishing the system's trust boundary.

---

## E — L11-02 HTTP Uniform Interface: Resource vs Representation

- **Decoupling Matrix**:
  - **Resource**: Conceptual entity identified by URI (e.g. `/api/v1/accounts/101`).
  - **Representation**: Byte serialization of the resource's current state transmitted with specific media metadata (`Content-Type: application/json` or `text/csv`).
- **Architectural Value**:
  - Uniform interface allows servers to re-architect internal storage engines or database schemas without altering client interaction contracts.

---

## F — HTTP Method Semantics Matrix (Safe vs Idempotent)

| Method | Safe (RFC 9110) | Idempotent (RFC 9110) | State Machine Semantic |
|---|---|---|---|
| `GET` | **YES** | **YES** | Read-only representation retrieval; promises zero server state change. |
| `HEAD` | **YES** | **YES** | Identical to GET but transfers no response body bytes. |
| `PUT` | **NO** | **YES** | Replaces/creates target resource state with provided representation. |
| `DELETE` | **NO** | **YES** | Removes resource identified by request URI. |
| `POST` | **NO** | **NO** | Submits representation for arbitrary target processing (creates child, mutates). |

---

## G — Idempotence vs Blind Retry Safety (Partial Failure Reality)

- **Fundamental Distributed Systems Axiom (EC-CON-010)**:
  - Idempotence guarantees that multiple identical successful requests have the same net server state effect as a single request.
  - **Idempotent != Retry-Safe after Timeout**: A client-side socket read timeout leaves server state fundamentally ambiguous (request lost, server processing slow, or response lost in transit).
  - Blindly re-issuing a `PUT` after timeout can trigger non-idempotent downstream side effects (e.g. audit log duplication, notification triggers, or overwriting newer concurrent mutations).
- **Remediation Contract**:
  - Requires conditional concurrency controls (optimistic locking via `If-Match: <ETag>`) or dedicated reconciliation queries (`GET`) before retry.

---

## H — Protocol Status vs Business Outcome Decoupling

- **Protocol Layer (`200 OK`)**:
  - Confirms the HTTP transport request was received, parsed, and answered by the HTTP stack.
- **Business Layer (`ERR_INSUFFICIENT_FUNDS`)**:
  - The business domain logic failed to execute (e.g. account balance insufficient).
- **Empirical Observation**:
  - In `labs/foundations/m11/http_semantics_observer.py`, the observer records:
    - HTTP Status: `200 OK`
    - Payload JSON: `{"success": false, "code": "ERR_INSUFFICIENT_FUNDS", "message": "Transaction failed..."}`
- **Architectural Rule**:
  - Applications must never treat HTTP 200 as business execution proof.

---

## I — HTTP/1.1 Wire Framing Observation (CRLF Demarcation)

- **Framing Invariant**:
  - Header lines delimited strictly by CRLF (`\r\n`, hex `0x0D 0x0A`).
  - Header block terminates upon encountering an empty line (`\r\n\r\n`).
- **Empirical Host Evidence**:
  - Directly verified by raw TCP socket byte exchange in `labs/foundations/m11/http_semantics_observer.py`.

---

## J — L11-03 Caching Architecture: Freshness vs Validation

- **Pillar 1: Freshness Lifetime (`Cache-Control: max-age`)**:
  - Evaluated locally by client/cache without initiating any network exchange. Zero latency overhead.
- **Pillar 2: Conditional Validation (`ETag` / `If-None-Match`)**:
  - Executed when stale; initiates lightweight round-trip to verify whether cached representation remains authoritative.

---

## K — Strong ETag Opaque Validator & 304 Zero Body Bytes

- **Opaque Validator Principle**:
  - RFC 9110 specifies that an Entity Tag (`ETag`) is an opaque string token. It is not universally required to be a cryptographic hash.
- **304 Not Modified Body Constraint (RFC 9111 Section 4.1)**:
  - The 304 response **MUST NOT** contain a message body.
  - Empirical verification in `labs/foundations/m11/caching_observer.py`:
    - Received bytes following double CRLF: strictly **0 bytes**.
    - Notice: RFC 9111 does not mandate `Content-Length: 0` in 304; representation headers may be present, but body transmission is 0.

---

## L — Intermediary Adapter, Header Transformation & Upstream Outage

- **Hop-by-hop Headers Stripping**:
  - Headers `Connection`, `Keep-Alive`, `Proxy-Authenticate`, `Proxy-Authorization`, `TE`, `Trailers`, `Transfer-Encoding`, `Upgrade` are stripped before forwarding.
- **Via Header Injection**:
  - Appends `Via: 1.1 essential-cs-intermediary` on request and response hops.
- **Upstream Failure Mapping (EC-CON-010)**:
  - When upstream origin server is terminated or connection refused, intermediary catches `ConnectionRefusedError` and returns `502 Bad Gateway` with diagnostic JSON.

---

## M — Transport Generational Evolution & Trade-offs (No Universal Winner)

| Protocol | Transport Base | Head-of-Line (HOL) Blocking | Core Architectural Trade-off |
|---|---|---|---|
| **HTTP/1.1** | TCP (Text / CRLF) | Severe Application-layer HOL | Simple & transparent; requires multiple concurrent TCP connections. |
| **HTTP/2** | TCP (Binary Framing) | Solves App-layer HOL; suffers TCP-layer HOL | Single-connection multiplexing; high packet loss drops throughput for all streams. |
| **HTTP/3** | QUIC (UDP + Integrated TLS 1.3) | Eliminates Transport HOL; per-stream independent loss recovery | High user-space CPU load; susceptible to network UDP QoS rate-limiting/filtering. |

- *Conclusion*: **No Universal Transport Winner**. System selection depends on packet loss profile, CPU budget, and middlebox network constraints.

---

## N — Bounded Estimate Task: Bandwidth & Latency Savings

- **Illustrative Parameters**:
  - Origin RTT: $\text{RTT}_{\text{origin}} = 100\text{ ms}$
  - Edge Cache RTT: $\text{RTT}_{\text{edge}} = 5\text{ ms}$
  - Static Resource Bundle Size: $S = 2\text{ MiB}$
  - Concurrency: $N = 10{,}000\text{ req/s}$
  - Cache Hit Ratio: $H = 90\%$ ($0.9$)
- **Calculations**:
  - Uncached Origin Egress Bandwidth: $B_{\text{nocache}} = 10{,}000 \times 2\text{ MiB/s} = 20\text{ GiB/s} = 160\text{ Gbps}$
  - Cached Origin Egress Bandwidth: $B_{\text{cached}} = 10{,}000 \times (1 - 0.9) \times 2\text{ MiB/s} = 2\text{ GiB/s} = 16\text{ Gbps}$ ($90\%$ bandwidth reduction).
  - Average User Latency: $T_{\text{avg}} = 0.9 \times 5\text{ ms} + 0.1 \times (5 + 100)\text{ ms} = 4.5\text{ ms} + 10.5\text{ ms} = 15\text{ ms}$ ($85\%$ latency reduction).
- **Inference Limits**:
  - Assumes uniform static cacheability. Dynamic uncacheable API endpoints do not realize these gains. Cache invalidation spikes can induce severe cache stampedes.

---

## O — Concept Audit & Verification Boundaries

- **Canonical Concept Revisits**:
  - `EC-CON-005 Interface`: Revisits in L11-01 (TLS/socket boundary), L11-02 (HTTP uniform interface), L11-03 (proxy/hop-by-hop headers).
  - `EC-CON-010 Failure`: Revisits in L11-01 (handshake rejection), L11-02 (partial failure/timeout), L11-03 (502 Bad Gateway mapping).
  - `EC-CON-011 Caching`: Revisits in L11-03 (freshness vs validation, 304, CDN caching).
  - `EC-CON-012 Locality`: Revisits in L11-03 (CDN edge caching proximity).
  - `EC-CON-017 Trust Boundary`: Revisits in L11-01 (TLS 1.3 trust boundary, X.509 dual pillars, zero bypass flags).
- **Concept Governance Audit**:
  - Total new concepts introduced: **0** [AUDIT: CONFIRMED]
  - Future concepts `EC-CON-014 Consistency` and `EC-CON-015 Concurrency` NOT defined [AUDIT: CONFIRMED]
- **Progressive Support Details Audit**:
  - Zero open-by-default details tags (`<details open>` count: **0**) [AUDIT: CONFIRMED]
- **Learner Validation Status**:
  - Module M11 status: `READY FOR LEAD REVIEW` (v0.1).
  - Author does not self-promote to `VERIFIED` or `RELEASED`.
