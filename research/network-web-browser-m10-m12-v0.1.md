# Networking & Web/Browser Platform (M10–M12) Research Dossier v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #68 — [Research] M10–M12 Networking & Web/Browser Research Dossier v0.1
Repository state researched: `main @ 278e0686d3b9bbaf420ecbe0637ed2075d305c38`
Checked date for current specifications, sources, and tools: **2026-09-03**
Role: Research Agent — Networking, Protocol, Browser Mechanism, Source, Provenance & Implementation-Feasibility Researcher
Scope: Research step only; no learner Lessons, runnable Lab implementation, Mini Cloud App feature work, Blueprint redesign, Concept Registry edits, or Open Question closure.

---

## Evidence-Layer Legend

This dossier strictly follows the repository source policy (`meta/RESEARCH_AND_SOURCE_POLICY.md`):

- **PRINCIPLE** — stable mechanism, theory, or reasoning pattern independent of a specific product or version.
- **SPECIFICATION** — normative or official contract from a formal standard, RFC, language specification, ABI, protocol, or platform interface definition.
- **IMPLEMENTATION** — actual tool, runtime, browser engine, or kernel behavior within a named environment.
- **CURRENT PRACTICE** — replaceable present-day convention, deployed version baseline, provider behavior, or operational pattern subject to periodic change.

Confidence and context labels:

- **ESTABLISHED** — strongly supported by stable primary/authoritative evidence and consensus systems practice.
- **IMPLEMENTATION-SPECIFIC** — valid only for the named implementation, toolchain, version, or environment.
- **CURRENT-PRACTICE** — useful at the checked date (2026-09-03) but expected to require scheduled review.
- **CONTESTED** — credible sources, specifications, or implementations disagree under comparable assumptions.
- **UNCERTAIN** — evidence is incomplete or the design choice requires empirical implementation testing.

---

## 1. Executive Recommendation / Readiness

**Recommendation: READY FOR DESIGN**

This Research Dossier establishes the technical, pedagogical, tooling, environment, Required-Lab, Optional-Lab, Source-Expedition, provenance, currentness, and claim-boundary evidence required to design the three Modules of Stage 4 (S4) without guessing:

$$\text{M10 (Networking I: IP, DNS, Transport)} \longrightarrow \text{M11 (Networking II: TLS, HTTP, CDN, Proxies)} \longrightarrow \text{M12 (Web & Browser: Integrated Case)}$$

### Key Findings and Invariant Alignment

1. **Architecture and Registry Integrity Preserved:**
   - **Zero new canonical concept first homes:** All 18 canonical concepts in `meta/CONCEPT_REGISTRY.md` remain at their accepted first homes.
   - **Strict future-home guardrails:** **EC-CON-014 Consistency** remains scheduled for its canonical first home in M14 (`L14-02`); **EC-CON-015 Concurrency** remains scheduled for its canonical first home in M15 (`L15-01`). M12's event loop is strictly a **preview** and application of concurrency in the browser context, not a canonical definition.
   - **Canonical concept revisits mapped cleanly:**
     - `EC-CON-005 Interface`: revisited in M11 (HTTP as a uniform protocol interface).
     - `EC-CON-010 Failure`: revisited in M10 (network failure taxonomy: timeout, connection refused, host unreachable, resolution failure) and M11 (HTTP status codes, TLS handshake failures, intermediary failures).
     - `EC-CON-011 Caching`: revisited in M11 (HTTP freshness, validators, conditional requests, shared vs. private caches, CDNs).
     - `EC-CON-012 Locality`: applied in M11/M12 performance reasoning (connection reuse, RTT bounds, edge termination).
     - `EC-CON-013 Isolation`: revisited in M12 (browser process isolation, renderer sandboxing, site isolation).
     - `EC-CON-017 Trust Boundary`: revisited in M11 (TLS certificate validation, public CA hierarchy) and M12 (Same-Origin Policy, CORS, CSP, browser-enforced site boundaries).
     - `EC-CON-018 Process`: revisited in M12 (browser architecture: browser process, renderer processes, utility processes, GPU process).
2. **LAB-REQ-01 Re-Audit Verified:**
   - The selected Required Lab — *HTTP interface, origin, and intermediary trace* (RFC 9110 + learner-owned localhost origin + bounded intermediary adapter + `curl`) — is technically feasible as a bounded localhost activity. Required tool availability and process cleanup still need implementation-time preflight/smoke; no one host result is a universal environment guarantee.
   - Evaluated against current normative RFC 9110 (HTTP Semantics, STD 97, June 2022) and RFC 9111 (HTTP Caching, STD 98, June 2022).
   - Uses standard Python libraries (`http.server`, `socket`, `urllib`) for the origin and forwarding adapter fixtures, ephemeral localhost port binding, and `curl` for inspection. No public traffic, no root/sudo privileges, no DNS manipulation, and no third-party services required.
   - Provenance and licensing: IETF Trust Legal Provisions govern RFC 9110/9111. All lab prose, test wrappers, and code fixtures will be original Essential CS creations (Apache-2.0 / CC BY-SA 4.0), referencing RFC sections without wholesale text copying.
3. **LAB-OPT-02 Rights and Currentness Recheck (Stanford CS144 Checkpoint 2):**
   - Stanford CS144 (Fall 2025 offering, Checkpoint 2 *The TCP Receiver*) checked at `https://cs144.github.io/assignments/check2.pdf`.
   - **Rights boundary:** The Minnow starter code repository (`cs144/minnow`) is frequently restricted/private during active academic terms, and public distribution terms for assignment text/tests are not explicitly granted.
   - **Architecture disposition:** LAB-OPT-02 **remains strictly Optional and link-only**. Essential CS will not bundle Stanford CS144 starter code or assignment text. Learners wishing to undertake this challenging implementation must obtain the materials independently.
4. **EXP-03 Chromium Source-Route Recheck:**
   - Primary route confirmed: Chromium design doc `docs/process_model_and_site_isolation.md` is active and authoritative for current practice on `chromium.googlesource.com`.
   - C++ source locations verified:
     - `content/browser/site_instance_impl.cc` (active, verified live).
     - `content/browser/security/cpsp/child_process_security_policy_impl.cc` (active, verified live at its updated location under `content/browser/security/cpsp/`).
   - Educational boundary: Source reading is strictly bounded to three specific inspection points. No Chromium compilation is required or permitted.
5. **Environment and OQ-BP-006 Baseline Feasible:**
   - Python 3 sockets provide the portable required observation spine; `curl` is a required LAB-REQ-01 tool subject to preflight, while Linux `ss`/`ip route` are useful environment-sensitive observations rather than universal prerequisites.
   - Raw packet capture (`tcpdump`) and network namespace operations are classified as **optional / capability-gated** because they require root/`CAP_NET_RAW` privileges that fail in restricted container and hosted environments.
   - System `openssl` CLI is environment-sensitive (often missing from Windows PATH); TLS inspection will use Python's standard `ssl` library and `curl` for core observation.
   - Browser environments: Desktop browsers (Chrome/Edge/Firefox) provide DevTools for visual inspection; headless environments rely on local HTML/JS fixtures with Python servers or deterministic static trace fallbacks. OQ-BP-006 remains open.
6. **Safety and Claim Boundaries Hardened:**
   - Strictly enforced localhost-only network safety posture: zero port scanning, zero external packet injection, zero DNS/ARP spoofing, zero certificate-bypass exercises against public entities, and zero production CDN manipulation.
   - Explicit claim boundaries established for TCP, DNS, TLS, HTTP, and Browsers to eradicate pervasive pedagogical fallacies (e.g., "TCP preserves message boundaries", "DNS lookup happens on every request", "valid cert = trustworthy business", "CORS is server authentication", "one tab = one process").

---

## 2. Scope and Canonical Constraints

### 2.1 Scope Chain and Module Definitions

| Module | Canonical Name | Preliminary Lessons | Hard Prereqs | Soft/Pref Prereqs | Canonical Concept First Home | Primary Competencies |
|---|---|---|---|---|---|---|
| **M10** | Networking I: IP, DNS & Transport | L10-01: How does a message cross the internet?<br>L10-02: How does 'reliable' work over unreliable links?<br>L10-03: Why is my request timing out? | M06 | M09, M08 | None (revisits Failure, Interface) | Trace, Explain, Diagnose, Judge, Estimate |
| **M11** | Networking II: TLS, HTTP, CDN & Proxies | L11-01: How do I talk securely to a server?<br>L11-02: What is HTTP, really?<br>L11-03: Why is my page slow to load? | M10 | None | None (revisits Interface, Failure, Caching, Locality, Trust Boundary) | Trace, Explain, Observe, Diagnose, Judge, Estimate |
| **M12** | Web & Browser: The Integrated Case | L12-01: What is a browser, architecturally?<br>L12-02: How does a page render?<br>L12-03: Why is the browser secure?<br>L12-04: Why does my page feel slow? | M11, M07 | M05, M02 | None (revisits Process, Isolation, Trust Boundary, Abstraction; **Concurrency preview only**) | Trace, Explain, Observe, Diagnose, Judge |

### 2.2 Canonical Concept Registry Constraints

There is **no new canonical concept first home** in M10–M12.

- **EC-CON-005 Interface (接口):** Revisit in M11 `L11-02` (HTTP uniform interface: methods, status codes, headers, representations).
- **EC-CON-010 Failure (故障):** Revisit in M10 `L10-03` (network failure taxonomy: connection refused vs. timeout vs. host unreachable vs. resolution failure) and M11 `L11-02`/`L11-03` (protocol status errors, TLS failures, proxy dropped connections).
- **EC-CON-011 Caching (缓存):** Revisit in M11 `L11-03` (HTTP caching: freshness vs. validation, conditional requests, ETag, private vs. shared caches, CDN edge caching).
- **EC-CON-012 Locality (局部性):** Applied in M11/M12 performance and latency reasoning (network RTT, edge termination, connection keep-alive/multiplexing).
- **EC-CON-013 Isolation (隔离):** Revisit in M12 `L12-01` and `L12-03` (multi-process browser architecture, renderer sandbox, site isolation).
- **EC-CON-017 Trust Boundary (信任边界):** Revisit in M11 `L11-01` (TLS authentication, CA hierarchy, public trust stores) and M12 `L12-03` (Same-Origin Policy, CORS, CSP).
- **EC-CON-018 Process (进程):** Revisit in M12 `L12-01` (browser process, renderer processes, GPU process, utility processes).

**Strict Future-Home Protections:**
- **EC-CON-014 Consistency (一致性):** Canonical first home is strictly M14 `L14-02`. M11 caching and M12 storage/DOM state must not define Consistency or use database/distributed consistency guarantees as established curriculum concepts.
- **EC-CON-015 Concurrency (并发):** Canonical first home is strictly M15 `L15-01`. M12 `L12-04` (event loop, render-blocking JS, task vs. microtask) is strictly a **preview** and application of concurrency in a browser runtime. It must not provide the canonical definition of Concurrency.

### 2.3 Competency Progression Constraints

Only the 8 canonical competencies (`meta/COMPETENCY_MATRIX.md`) are used:

- **M10:** Primary: **Trace** (packet hop, DNS query, socket write, 3-way handshake). Growth: **Explain** (reliability mechanisms, UDP vs. TCP trade-offs), **Diagnose** (connection refused vs. timeout vs. resolution failure), **Judge** (transport protocol choice), **Estimate** (RTT and bandwidth-delay product).
- **M11:** Primary: **Trace** (request through client, intermediary, cache, and origin; TLS handshake). Growth: **Explain** (HTTP semantics, certificate chain validation), **Observe** (`curl -v`, HTTP response headers, status codes), **Diagnose** (stale cache, proxy error 502/504, TLS certificate mismatch), **Judge** (caching policies, HTTP method idempotency, retry safety), **Estimate** (handshake round-trips, transfer latency).
- **M12:** Primary: **Trace** (page load lifecycle across browser processes: parse $\rightarrow$ DOM $\rightarrow$ CSSOM $\rightarrow$ layout $\rightarrow$ paint $\rightarrow$ composite). Growth: **Observe** (DevTools Performance and Network panels, task manager), **Diagnose** (render-blocking scripts, CORS violations, event loop starvation), **Explain** (browser security model: SOP, CORS, CSP, sandbox), **Judge** (web platform security and architectural trade-offs).

---

## 3. Cross-Module Mechanism Chain M10 $\rightarrow$ M11 $\rightarrow$ M12

The three modules form a continuous, cohesive systems journey tracing a network request from raw packets and sockets up through secure transport, application protocol semantics, and finally into the integrated browser operating environment:

```
+-------------------------------------------------------------------------------+
| M10: Networking I — IP, DNS & Transport                                       |
| Host naming -> DNS resolution (A/AAAA) -> IP packet routing (best effort)     |
| Transport layer: UDP datagrams vs. TCP reliable byte stream                   |
| Sockets (endpoints: IP + Port) -> 3-way handshake -> Sequence numbers & ACKs  |
| Network failure spectrum: DNS failure | Connection Refused (RST) | Timeout    |
+---------------------------------------+---------------------------------------+
                                        | Byte stream carries secure protocol
                                        v
+---------------------------------------+---------------------------------------+
| M11: Networking II — TLS, HTTP, CDN & Proxies                                 |
| TLS 1.3 Handshake: Server certificate verification, PKI trust store, Ephemeral|
| Diffie-Hellman key exchange -> Encrypted, authenticated, tamper-proof channel |
| HTTP Semantics (RFC 9110): Uniform interface, Methods (Safe/Idempotent), URI   |
| Representations & Headers -> HTTP Wire Evolution: HTTP/1.1 -> H2 -> H3/QUIC   |
| Intermediaries & Caching (RFC 9111): Gateways, Proxies, CDNs, Freshness, ETags|
+---------------------------------------+---------------------------------------+
                                        | Browser issues requests & renders doc
                                        v
+---------------------------------------+---------------------------------------+
| M12: Web & Browser — The Integrated Case                                      |
| Multi-Process Architecture: Browser Process (privileged) vs. Renderers        |
| Site Isolation (Process-per-site-instance) & OS Sandboxing                    |
| Document Pipeline: Parse HTML -> DOM -> CSSOM -> Layout -> Paint -> Composite |
| Security Model: Origin (Scheme+Host+Port), Same-Origin Policy, CORS, CSP      |
| Execution Mechanics: Single-threaded JS event loop (Tasks & Microtasks)      |
+-------------------------------------------------------------------------------+
```

---

## 4. M10 Research — Networking I: IP, DNS & Transport

### 4.1 Capability Transition
Learners transition from viewing network communication as an abstract, magically reliable pipe (`requests.get("https://...")`) to understanding the layered, best-effort packet delivery mechanism of IP, the hierarchical indirection of DNS, and how transport protocols (TCP/UDP) construct distinct abstractions (ordered reliable stream vs. independent datagrams) over unreliable physical networks. Learners gain the ability to pinpoint whether a failure is a name resolution failure, an unreachable route, an active rejection (`RST`), or a silent loss/timeout.

### 4.2 Minimum Mechanism Model
1. **Network Layer (IP — Internet Protocol):**
   - Best-effort, connectionless packet switching (RFC 791 / RFC 8200). Packets may be delayed, lost, duplicated, reordered, or corrupted.
   - Addressing: IPv4 (32-bit) and IPv6 (128-bit) identify host network interfaces. Subnets, netmasks, and CIDR notation (`/24`).
   - Routing: Hop-by-hop forwarding based on destination IP and local routing tables (longest prefix match). Routers do not maintain end-to-end connection state.
2. **Name Resolution (DNS — Domain Name System):**
   - Hierarchical distributed database mapping human-readable names to network resources (RFC 1034, RFC 1035, RFC 2181).
   - Hierarchy: Root zone (`.`), Top-Level Domains (`.com`, `.org`), Authoritative Name Servers.
   - Resolution Mechanics: Stub resolver (`getaddrinfo` via libc) queries a recursive resolver; recursive resolver traverses the hierarchy using referrals.
   - Record Types: `A` (IPv4 address), `AAAA` (IPv6 address), `CNAME` (canonical name alias).
   - Caching & TTL: Responses carry a Time-To-Live (TTL) indicating maximum cache validity. Resolvers and operating systems cache records locally.
3. **Transport Layer (UDP vs. TCP):**
   - **Ports and Sockets:** A connected transport flow can be identified by protocol plus local/remote addresses and ports. Port numbers participate in demultiplexing to transport endpoints/sockets; they do **not** map one-to-one to operating-system processes because one process may own many sockets and multiple sockets/processes can share a local port under defined reuse/listening rules.
   - **UDP (User Datagram Protocol — RFC 768):** Minimal datagram transport with source/destination ports and a checksum field. Datagram boundaries are preserved. UDP itself adds no handshake, acknowledgment, ordering, retransmission, flow control, or congestion control. Checksum rules depend on the network layer: a zero checksum is permitted for IPv4 UDP, while IPv6 requires the UDP checksum by default with narrow tunnel exceptions (RFC 8200 / RFC 8085).
   - **TCP (Transmission Control Protocol — RFC 9293, obsoleting RFC 793):**
     - Reliable, connection-oriented, full-duplex, ordered **byte stream**.
     - Connection lifecycle: 3-way handshake (`SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK`), graceful connection termination (`FIN`/`ACK`), abortive termination (`RST`).
     - Byte stream vs. packets: TCP assigns a sequence number to every byte, not to application messages. TCP does not preserve application message boundaries.
     - Reliability mechanics: Positive acknowledgment (`ACK`), retransmission timers, cumulative acknowledgments, sliding window flow control.
4. **Network Failure Taxonomy:**
   - **Resolution Failure:** DNS name cannot be resolved (`NXDOMAIN`, resolver timeout, `getaddrinfo` returns `EAI_NONAME`). No packets reach any server.
   - **Route Unreachable:** Gateway/router returns ICMP Destination Unreachable (`EHOSTUNREACH`, `ENETUNREACH`), or packets silently drop en route.
   - **Connection Refused:** In the deterministic localhost case, connecting to an unbound TCP port normally produces an active refusal surfaced as `ECONNREFUSED`/the runtime's connection-refused exception. On arbitrary networks, policy devices and host firewalls can drop or reject traffic differently, so `RST = no process listening` is not a universal diagnosis.
   - **Timeout:** A configured operation deadline expires before the required progress occurs. Depending on the API this can be a connect timeout, read timeout, or higher-level request timeout; it does not by itself identify where packets were lost or whether remote application work occurred.
   - **Connection Reset / Abrupt Termination:** Established connection is terminated abruptly by a peer crash, firewall state timeout, or explicit `RST` (`ECONNRESET`).
   - **Application-Level Silence / Hang:** TCP connection is successfully established (`ESTABLISHED`), request bytes are sent, but the server application hangs, deadlocks, or is overloaded, sending no application response (`read timeout`).

### 4.3 Explicit Non-Goals
- Global BGP routing policies, autonomous systems (AS) graph algorithms, or routing protocol implementations (OSPF, RIP).
- Implementing a full TCP stack from scratch for Core (reserved for optional study via LAB-OPT-02).
- Low-level congestion control mathematical proofs (BIC, CUBIC, BBR derivations).
- Packet sniffing / promiscuous raw socket packet crafting exercises.
- Public network scanning, penetration testing, or DDoS simulation tools (`nmap`, `scapy`, `hping3`).
- Enterprise hardware router/switch administration.

### 4.4 Hidden Prerequisites / Just-In-Time Support
- Basic socket abstraction: Python `socket` module provides direct exposure to POSIX socket syscalls (`socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `send()`, `recv()`, `close()`).
- Port-number discipline: IANA divides the 16-bit space into System Ports (0–1023), User Ports (1024–49151), and Dynamic/Private Ports (49152–65535). Whether a process needs privilege to bind a low port is an OS policy, not an IANA property. Binding a socket to local port `0` asks the OS to choose an available port; the activity records the actual assigned port instead of assuming a fixed range.
- Timing-tool choice: if an activity records elapsed time, use a monotonic elapsed-time API such as `time.perf_counter()`/`time.monotonic()`. M10 uses this operationally without canonically teaching clock semantics, whose accepted later home remains M20.

### 4.5 Candidate Real Observation / Activity
- **Activity M10-A (Local Socket Mechanics & State Observation):**
  - Launch a minimal Python TCP server on `127.0.0.1` binding to port 0 (ephemeral).
  - If available, inspect orchestrated socket states using Linux `ss -tan` (or a platform-native equivalent). `LISTEN` and a held-open `ESTABLISHED` connection can be made deterministic; transient states such as `SYN_SENT`, `TIME_WAIT`, and `CLOSE_WAIT` are optional observations and must not be required on every host.
  - Connect with a Python client and send several application chunks. The receiver accumulates bytes until the expected logical payload length is reached and records the actual `recv()` partition observed. Tests assert byte content/order, **not** that one `recv()` coalesces or preserves the sender's call boundaries.
- **Activity M10-B (Controlled Network Failure Injection on Localhost):**
  - Case 1: Connect to a course-selected currently unused port on `127.0.0.1` and record the runtime's connection-refused disposition. Do not assert a fixed errno or latency.
  - Case 2: For a deterministic timeout, use a course-owned localhost server that accepts a connection but deliberately withholds the expected application response until the client's configured **read** deadline expires. This demonstrates timeout semantics without depending on external routing/firewall behavior. A true connect-timeout observation is optional/environment-sensitive and must not target TEST-NET as though silence were guaranteed.
  - Case 3: If resolver capability is available, resolve a name under the reserved `.invalid` TLD and record the actual resolver failure. If name service is unavailable/restricted, report `NO LIVE DNS FAILURE OBSERVATION` rather than fabricating an `NXDOMAIN` transcript.
  - Compare semantic dispositions and actual elapsed samples only as host evidence; no fixed timing ratio is a curriculum invariant.

### 4.6 Required Learner Evidence
- Transcript recording the deterministic localhost connection-refused and application read-timeout dispositions, plus a truthful DNS-failure disposition when resolver capability exists.
- Raw elapsed-time samples may be recorded, but no `<N ms`, `±N%`, or fixed refused-vs-timeout ratio is required.
- If `ss` is available, preserve a snapshot of the orchestrated `LISTEN`/`ESTABLISHED` sockets; otherwise record a truthful tool-unavailable disposition and preserve the Python endpoint evidence.
- Written explanation demonstrating why receiving an ACK does not prove the remote application has processed the business request.

### 4.7 Evidence-Layer Classification
- **PRINCIPLE:** End-to-end argument; layered communication model; byte-stream abstraction vs. datagram; sequence space wrapping; two-generals problem / failure ambiguity.
- **SPECIFICATION:** RFC 9293 (TCP); RFC 768 (UDP); RFC 791 (IPv4); RFC 8200 (IPv6); RFC 1034/1035 (DNS); POSIX.1-2017 socket interface.
- **IMPLEMENTATION:** Linux TCP/IP stack (tcp(7), ip(7), socket(2)); `ss` (iproute2); glibc `getaddrinfo()`; CPython `socket` module.
- **CURRENT PRACTICE:** Named resolver implementation behavior (for example systemd-resolved) and platform socket/tool defaults, but only when the exact implementation/version is recorded. No TCP initial-window constant is a curriculum invariant.

### 4.8 Authoritative Sources
- IETF STD 7 / RFC 9293: *Transmission Control Protocol (TCP)*, August 2022 (Normative current TCP spec).
- IETF STD 6 / RFC 768: *User Datagram Protocol (UDP)*, August 1980.
- IETF STD 86 / RFC 8200: *Internet Protocol, Version 6 (IPv6) Specification*, July 2017.
- IETF STD 13 / RFC 1034 & RFC 1035: *Domain Names - Concepts and Facilities / Implementation and Specification*, November 1987.
- Saltzer, Reed, Clark: *End-to-End Arguments in System Design*, ACM TOCS 1984.

### 4.9 Likely Misconceptions
1. *"TCP preserves application message boundaries."* (TCP is a continuous byte stream; application framing must be implemented via delimiters or length prefixes).
2. *"Receiving an ACK means the remote application executed the command."* (A TCP ACK acknowledges sequence-space receipt by the peer TCP endpoint; it does not establish that the remote application consumed, validated, or committed the bytes).
3. *"A request timeout means the server definitely did not perform the write."* (The request could have been received and committed by the server, but the network failed before the client received the acknowledgment).
4. *"One domain name maps to exactly one permanent IP address."* (DNS frequently maps one name to multiple dynamic IPs for load balancing, CDN edge steering, and multi-homing).
5. *"DNS lookups happen before every single HTTP request."* (Browsers, operating systems, and HTTP client connection pools maintain internal caches and reuse existing TCP/TLS connections).

### 4.10 Environment / Tool Constraints
- Cross-platform Python 3 standard library `socket` works reliably on Linux, macOS, and Windows.
- `ss` is Linux-specific (from `iproute2`) and must be capability-checked. Other platforms may expose different native socket tables; the required activity remains functional using Python endpoint state/evidence without adding an undeclared third-party `psutil` dependency.
- `nc` (netcat) has syntax variations between OpenBSD netcat and GNU netcat (`-z`, `-l -p`); avoid relying on netcat CLI options; prefer Python socket scripts.
- `traceroute` availability and privilege requirements vary by platform and probe mode (ICMP/UDP/TCP). Keep it optional/capability-gated; lack of the tool or raw-socket capability is a truthful `SKIP`, not a Core failure.
- Raw packet capture (`tcpdump`, Wireshark) requires elevated privileges (`CAP_NET_RAW` / root) and is classified as Optional / Capability-gated.

### 4.11 Provenance / License Risk
- All primary M10 lab scripts and diagnostic exercises are original Essential CS implementations (Apache-2.0).
- RFC text is referenced by section under fair use / IETF Trust provisions; no RFC text or figures will be bundled verbatim.

### 4.12 Implementation-Time Smoke Requirements
- Python socket smoke: bind to port 0, connect, exchange a bounded payload, and close cleanly under a harness deadline used only to prevent hangs (not as learner timing evidence).
- Failure smoke: reproduce the course-owned localhost refusal and read-timeout paths, capability-gate DNS failure, and verify no hanging processes or socket leaks.

---

## 5. M11 Research — Networking II: TLS, HTTP, CDN & Proxies

### 5.1 Capability Transition
Learners transition from raw transport streams to secure, structured application protocol interactions. They master the HTTP request-response model, uniform interface semantics, cache freshness and validation mechanisms, intermediary role in distributed systems, and the transport evolution from HTTP/1.1 to HTTP/2 and HTTP/3/QUIC. They learn to separate the protocol's semantics from its wire encoding and understand the cryptographic boundaries of TLS.

### 5.2 Minimum Mechanism Model
1. **Transport Layer Security (TLS 1.3 — RFC 8446):**
   - **Security Properties:** TLS 1.3 uses authenticated encryption (AEAD) for record confidentiality/integrity and can authenticate peers through certificate- or PSK-based handshakes. In the common Web PKI server-authentication case, the server proves possession of a key bound to a validated certificate identity; TLS does not establish application authorization or business trustworthiness.
   - **Handshake Mechanics:** A fresh certificate-based TLS 1.3 handshake can establish application-data keys after one network round trip, typically using an (EC)DHE key share selected from negotiated groups (X25519 is one common group, not a universal constant). PSK resumption and optional 0-RTT early data follow different paths and carry replay/security trade-offs that must not be collapsed into the fresh-handshake model.
   - **Forward Secrecy Boundary:** When TLS 1.3 uses (EC)DHE key establishment (including `psk_dhe_ke`), compromise of a long-term authentication key does not by itself reveal past session traffic keys. TLS 1.3 also defines PSK-only `psk_ke`; therefore, “TLS 1.3 always provides forward secrecy” is too broad.
   - **PKI & Certificate Path:** X.509/PKIX certificate validation follows RFC 5280 plus application-specific identity rules and a local trust-anchor policy. Web PKI deployments commonly use root trust anchors, intermediates, and end-entity certificates, but chain shape and trust-store contents are platform/current-practice details.
   - **Service Identity Verification (RFC 9525):** RFC 9525 (2023) obsoletes RFC 6125. Clients compare the reference service identity with presented `subjectAltName` identifiers according to the application protocol's rules; a successful certificate/path check is not a statement about the service's ethics or business correctness.
2. **HTTP Semantics (RFC 9110 — STD 97):**
   - **Uniform Interface:** Resources identified by URIs; representations carried in messages.
   - **Message Format:** Request (Method, Target, Version, Headers, Payload) and Response (Version, Status Code, Reason, Headers, Payload).
   - **Method Taxonomy:**
     - *Safe Methods:* `GET`, `HEAD`, `OPTIONS`, `TRACE` (read-only semantics, no server state mutation intended).
     - *Idempotent Methods:* `GET`, `HEAD`, `PUT`, `DELETE`, `OPTIONS`, `TRACE` (multiple identical requests have the same intended effect as a single request).
     - *Non-Idempotent Methods:* `POST`, `PATCH` (each request may produce an independent mutation).
   - **Status Code Classes:** 1xx (Informational), 2xx (Success: 200, 201, 204), 3xx (Redirection: 301, 302, 304), 4xx (Client Error: 400, 401, 403, 404, 405), 5xx (Server Error: 500, 502, 503, 504).
3. **HTTP Caching & Intermediaries (RFC 9111 — STD 98):**
   - **Intermediaries:** Forward proxies (client-selected), reverse proxies / gateways (origin-facing, transparent to client), and CDNs (geographically distributed reverse proxy caches).
   - **Freshness vs. Validation:**
     - *Freshness:* Controlled by `Cache-Control: max-age=N` or `Expires`. Fresh responses are served directly from cache without contacting the origin.
     - *Validation:* When a cached representation becomes stale, the cache or client performs a conditional request using validators:
       - Strong entity-tag: an opaque `ETag` value eligible for strong comparison when the origin assigns it according to strong-validator requirements; it is **not required to be a hash**.
       - Weak entity-tag: `ETag: W/"v1"`, suitable only for weak comparison.
       - Date validator: `Last-Modified`, whose validator strength depends on the RFC 9110 conditions.
       - Conditional headers: `If-None-Match`, `If-Modified-Since`.
     - *304 Not Modified:* A 304 response to a conditional GET carries **no message content/body**. It may still carry a `Content-Length` field whose value corresponds to the selected 200 representation, so tests must not require `Content-Length: 0`.
4. **HTTP Wire Framing & Evolution:**
   - **HTTP/1.1 (RFC 9112):** Uses a textual message syntax with field lines and supports transfer codings such as chunked encoding. Connections are persistent by default unless closure is indicated; the historical/optional `Keep-Alive` field is not what makes HTTP/1.1 persistence work. Serial request/response use on one connection can create application-layer head-of-line waiting.
   - **HTTP/2 (RFC 9113):** Adds binary framing, HPACK field compression, and concurrent streams over one TCP connection, removing HTTP/1.1's need to serialize exchanges on that connection. Because all streams still share TCP's ordered byte stream, loss/reordering of TCP data can delay progress for otherwise unrelated HTTP/2 streams.
   - **HTTP/3 (RFC 9114) over QUIC (RFC 9000):** Maps HTTP semantics onto QUIC streams. QUIC uses TLS 1.3 key establishment (RFC 9001) and avoids TCP's connection-wide byte-stream ordering between application streams: missing stream data need not block delivery of data on another stream. Congestion control, packet loss, and shared connection resources can still affect the whole connection. Connection IDs support path migration subject to QUIC's validation rules.

### 5.3 Explicit Non-Goals
- Cryptographic algorithm implementation (writing AES, RSA, or ECC math).
- PKI administration, CA root issuance, or OCSP stapling operations.
- Decrypting TLS packet captures in Wireshark using extracted session keys.
- CDN vendor configuration (Cloudflare, Fastly, AWS CloudFront dashboard training).
- Web framework API development (Django, Flask, Express).
- Running public proxy relays or scraping third-party websites.

### 5.4 Hidden Prerequisites / Just-In-Time Support
- HTTP message parsing intuition: Header lines terminated by `\r\n` (`CRLF`), empty line separating headers from body.
- TLS fixture on localhost: use a course-owned test CA/certificate (or another explicitly trusted local fixture) and a dedicated verification context so the learner can observe **successful verification**, hostname mismatch, and trust failure without contacting a public CA or teaching verification bypass.
- Safe port allocation: bind localhost listeners to port `0` and record the OS-assigned port. Do not hard-code 80/443 or assume the assigned port belongs to one universal “ephemeral >1024” range.

### 5.5 Candidate Real Observation / Activity
- **Activity M11-A (HTTP Request/Response & Header Inspection via `curl`):**
  - Run a local Python HTTP server on `127.0.0.1`.
  - Issue requests using `curl -v http://127.0.0.1:<port>/resource`.
  - Trace the raw HTTP exchange: request line (`GET /resource HTTP/1.1`), request headers (`Host`, `User-Agent`, `Accept`), blank line, response line (`HTTP/1.1 200 OK`), response headers (`Content-Type`, `Content-Length`), and response body.
- **Activity M11-B (LAB-REQ-01 HTTP Interface, Origin & Intermediary Trace):**
  - Setup: Start a local origin server (`OriginServer`) that serves content with `ETag` and `Cache-Control`.
  - Step 1 (Direct trace): Request directly from origin with `curl -v`. Observe origin processing.
  - Step 2 (Forwarded trace): Start a bounded local forwarding adapter (`IntermediaryAdapter`). Request through adapter. Observe `Via` header injection and socket connection hops: Client $\rightarrow$ Intermediary, Intermediary $\rightarrow$ Origin.
  - Step 3 (Conditional Cache Validation): Issue a second request through the intermediary with `If-None-Match: "etag"`. Intermediary or origin returns `304 Not Modified`. Trace shows zero response body payload transferred.
  - Step 4 (Controlled Failure): stop the origin server. The **course fixture policy** maps an upstream connection refusal to `502 Bad Gateway`; a separately modeled upstream deadline may map to `504 Gateway Timeout`. Learners must distinguish this fixture mapping from a universal law that every intermediary maps socket errors identically.

### 5.6 Required Learner Evidence
- Complete, verbatim `curl -v` transcripts of direct, forwarded, and conditional requests.
- Header analysis table comparing headers present at client vs. headers received at origin (identifying hop-by-hop vs. end-to-end headers).
- Verification of status `304 Not Modified` with the expected validator and **no response body/content**. Do not assert `Content-Length: 0`.
- Error trace for origin failure demonstrating proxy response with `502 Bad Gateway`.
- Clean reset verification proving all local processes terminated and ports released.

### 5.7 Evidence-Layer Classification
- **PRINCIPLE:** Uniform interface; resource vs. representation; safe vs. idempotent methods; cache freshness vs. validation; end-to-end vs. hop-by-hop boundaries; trust delegation via PKI.
- **SPECIFICATION:** RFC 9110 (HTTP Semantics, STD 97); RFC 9111 (HTTP Caching, STD 98); RFC 9112 (HTTP/1.1, STD 99); RFC 9113 (HTTP/2); RFC 9114 (HTTP/3); RFC 9000 (QUIC); RFC 8446 (TLS 1.3); RFC 5280 (X.509 PKI).
- **IMPLEMENTATION:** `curl` (libcurl CLI behavior); Python standard library `http.server`, `urllib.request`, `ssl`; OpenSSL / Schannel / SecureTransport backend differences in `curl`.
- **CURRENT PRACTICE:** Named browser/client ALPN preferences, deployed TLS/HTTP version support, certificate lifetimes, and connection-pool limits only when tied to an exact implementation/version/date. None of these values belongs in the curriculum as a permanent constant.

### 5.8 Authoritative Sources
- IETF STD 97 / RFC 9110: *HTTP Semantics*, June 2022.
- IETF STD 98 / RFC 9111: *HTTP Caching*, June 2022.
- IETF STD 99 / RFC 9112: *HTTP/1.1*, June 2022.
- IETF RFC 9113: *HTTP/2*, June 2022.
- IETF RFC 9000: *QUIC: A UDP-Based Multiplexed and Secure Transport*, May 2021.
- IETF RFC 9114: *HTTP/3*, June 2022.
- IETF RFC 8446: *The Transport Layer Security (TLS) Protocol Version 1.3*, August 2018.

### 5.9 Likely Misconceptions
1. *"HTTPS encrypts data, so the website is trustworthy and safe to send money to."* (Successful Web PKI verification establishes a cryptographic channel to a service identity validated under the client's trust policy; it does not establish the service's business legitimacy, authorization policy, or application correctness).
2. *"TLS hides all metadata on the wire."* (TLS does not hide IP-layer endpoints, packet timing, or packet sizes. Server-name exposure is now conditional: ordinary ClientHello SNI can be visible, while RFC 9849 Encrypted Client Hello (ECH) can protect the real ClientHello/SNI when successfully configured and negotiated. Do not teach either “SNI is always plaintext” or “ECH hides all metadata.”)
3. *"An idempotent method is always safe to retry automatically under all conditions."* (RFC 9110 defines idempotency in terms of the **intended effect requested by the client**. Idempotent methods are retry-friendly when a communication failure occurs before a response is read, but clients still need application-specific limits, authentication/replay considerations, and knowledge of semantics outside the method contract.)
4. *"A 200 OK response means the business transaction succeeded."* (`200 OK` means the request succeeded according to HTTP method semantics as reported by the server; it does not prove a domain/business invariant. The representation can still describe an application-level failure or partial outcome.)
5. *"HTTP/3 is always faster than HTTP/2 and HTTP/1.1."* (Performance depends on RTT, loss/reordering, connection reuse, implementation, CPU, congestion control, server/client behavior, and workload. The Research does not assign a universal winner or fixed speedup.)

### 5.10 Environment / Tool Constraints
- `curl` is common across the target platforms but must be preflighted; do not infer availability or a particular TLS backend/version from the OS name alone.
- `openssl` CLI is missing by default from many Windows installations; therefore, TLS verification must be supported via Python's standard `ssl` library or pre-bundled test fixtures rather than mandating an external `openssl` binary.
- All HTTP fixtures must bind to loopback and request OS-assigned ports (`bind(..., 0)` where supported). This reduces collision risk and avoids fixed privileged ports; the actual port is recorded as evidence.

### 5.11 Provenance / License Risk
- LAB-REQ-01 uses original Essential CS code for the server and intermediary adapter (Apache-2.0).
- RFC 9110 and RFC 9111 are referenced by section number; no text or diagrams from RFCs are copied into the curriculum.

### 5.12 Implementation-Time Smoke Requirements
- Start the local origin and intermediary adapter, issue direct/forwarded/conditional requests, verify the fixture's `Via`, 304-with-no-body, and refusal→502 policies, then terminate all processes cleanly. Use a bounded harness deadline only to prevent hangs; do not make a fixed total runtime an acceptance invariant.

---

## 6. M12 Research — Web & Browser: The Integrated Case

### 6.1 Capability Transition
Learners transition from treating the web browser as an opaque document viewer to understanding it as an integrated systems case for untrusted web content. They separate Web Platform contracts from a named browser implementation, trace a **conceptual** rendering pipeline, explain browser-enforced origin/security boundaries, and observe how a window/document event loop can make main-thread work interfere with responsiveness without canonically defining Concurrency.

### 6.2 Minimum Mechanism Model
1. **Multi-Process Architecture (Chromium Case Model):**
   - **Browser Process (Chromium case):** A privileged coordinator for browser UI, navigation/process assignment, permissions/security policy, and other browser-level services. Networking, storage, GPU, media, and utility work can live in dedicated processes/services depending on Chromium platform/version; do not teach one fixed process allocation as the browser architecture contract.
   - **Renderer Processes (Chromium case):** Sandboxed processes host web-content execution and rendering work for assigned frames/sites. Blink/V8 participate in parsing, DOM/style/layout/paint and JavaScript execution, but exact thread/process placement and scheduling are implementation details.
   - **GPU / compositor services (Chromium case):** GPU/compositor work is separated from renderer main-thread work in current Chromium, but exact service/process topology is implementation/current-practice evidence rather than a Web Platform requirement.
   - **Utility / Network services:** Current Chromium may isolate networking, media decoding, storage-related, and other services in dedicated processes. The lesson should use the current EXP-03 source/document as a case study rather than asserting every browser uses this topology.
2. **Site Isolation & Process Sandboxing:**
   - **Site vs. Origin:**
     - *Origin:* WHATWG HTML can produce a **tuple origin** (scheme, host, port, domain) or an opaque origin. For ordinary HTTP(S) tuple origins, same-origin comparison is based on scheme/host/port; do not teach every origin as a permanent 3-tuple.
     - *Site:* WHATWG site computation is based on the origin's scheme plus a registrable-domain-derived host when available, with opaque/special-host cases. Chromium's Site Isolation uses its own documented site/process concepts. “scheme + eTLD+1” is a useful common Web case, not a universal formula.
   - **Site Isolation (Chromium current-practice case):** Full Site Isolation on supported desktop configurations attempts to keep cross-site documents in separate renderer processes and combines this with renderer sandboxing/browser-side policy checks. Chromium's own documentation describes platform/resource-dependent modes, including more limited isolation on some mobile/embedder configurations. Do not make “every different site always has its own process” a browser invariant.
   - **Defense-in-depth boundary:** Site Isolation, renderer sandboxing, and browser-side `ChildProcessSecurityPolicy` checks reduce what a compromised renderer can directly access and are important mitigations for UXSS/Spectre-class risk. They do **not** prove that arbitrary renderer compromise can never disclose cross-site data; Chromium documents remaining gaps and platform-dependent protections.
   - **Out-Of-Process Iframes (OOPIF, Chromium case):** Under configurations with cross-site process isolation, a cross-site child frame can be hosted in another renderer process and composited into the page. This is implementation/current-practice evidence, not a universal rule for every browser/platform/frame.
3. **Conceptual Rendering Pipeline:**
   $$\text{HTML} \xrightarrow{\text{Parser}} \text{DOM Tree}$$
   $$\text{CSS} \xrightarrow{\text{Parser}} \text{CSSOM Tree}$$
   $$\text{DOM} + \text{CSSOM} \xrightarrow{\text{Style Resolution}} \text{Render Tree}$$
   $$\text{Render Tree} \xrightarrow{\text{Layout (Reflow)}} \text{Geometry (Box Model, Coordinates)}$$
   $$\text{Geometry} \xrightarrow{\text{Paint}} \text{Display Lists (Draw Operations)}$$
   $\text{Display Lists} \xrightarrow{\text{Compositing}} \text{Tiles / Layers} \xrightarrow{\text{GPU}} \text{Screen Pixels}$
   - This diagram is a learner-facing **mechanism model**, not a normative total ordering for every frame. Browsers can cache prior work, skip stages, perform style/layout/paint incrementally, and schedule/composite work across threads/processes.
   - **Script Execution & Render Blocking:**
     - Synchronous `<script>` blocks HTML parsing while fetching and executing.
     - `<script async>` fetches in background, executes immediately upon arrival (interrupts parsing).
     - Classic `<script defer>` and module scripts have different specification rules but both avoid the simple “parser blocks until this external script fetches and runs” model. Design should follow current HTML script-processing semantics rather than teach one identical timing rule for `defer` and `type="module"`.
4. **Web Platform Security Model:**
   - **Same-Origin Policy family:** Same-origin restrictions limit many cross-origin DOM/API interactions and origin-keyed storage access. Cookies have their **own** domain/path/SameSite/HttpOnly rules and must not be taught as simply governed by the origin tuple. Cross-origin embedding, navigation, messaging, and reading have API-specific rules; “cross-origin means no interaction” is too broad.
   - **Cross-Origin Resource Sharing (CORS — WHATWG Fetch):**
     - Browser-enforced relaxation of SOP for network requests (`fetch()`, `XMLHttpRequest`).
     - Server responds with `Access-Control-Allow-Origin: <origin>` to grant read access to client JavaScript.
     - *Preflight Request:* The Fetch standard defines **CORS-safelisted** methods/headers/content types. Requests outside the safelisted conditions generally require a CORS preflight (`OPTIONS`) before the CORS request, subject to the specification's cache/redirect/credentials rules. Avoid the incomplete shortcut “anything except GET/POST/HEAD or any custom header.”
     - *Crucial Boundary:* CORS is enforced by participating user agents around cross-origin fetch access. It is **not** server-side authentication/authorization and does not constrain a non-browser HTTP client in the same way. Phrase this as an interface/enforcement boundary, not as instructions to “bypass” browser security.
   - **Content Security Policy (CSP — W3C):**
     - HTTP response header (`Content-Security-Policy`) allowing a site to declare approved sources for scripts, styles, images, and network connections (`default-src`, `script-src`, `connect-src`).
     - Whether inline script or string-to-code execution is allowed depends on the actual policy. A sufficiently restrictive `script-src` can block those paths; directives such as `'unsafe-inline'`/`'unsafe-eval'`, nonce/hash sources, and other policy details change the result. CSP is defense in depth, not an automatic XSS proof.
5. **Event Loop Mechanics (Concurrency Preview):**
   - A Window/Document runs script through an event loop associated with its agent; browsers also have workers and many internal threads/processes. “JavaScript/browser is single-threaded” is not a valid global statement.
   - **Task queues:** HTML defines one or more task queues for an event loop and task sources; selecting which runnable task queue supplies the next task is partly implementation-defined.
   - **Microtask queue:** Promise reactions and `queueMicrotask()` use the microtask machinery; microtask checkpoints occur at specified points rather than forming a universal learner formula of “one macrotask then render.”
   - **Rendering opportunities:** Window event loops may perform rendering-update steps at rendering opportunities, but a render is not guaranteed after every task/microtask cycle.
   - A deliberately bounded long-running main-thread task can delay input/rendering opportunities and create observable jank. This is a preview of scheduling/interleaving concerns; EC-CON-015 Concurrency remains M15.

### 6.3 Explicit Non-Goals
- Web frontend framework programming (React, Vue, Svelte, Angular).
- CSS layout trivia, grid/flexbox edge cases, or responsive design styling.
- Compiling Chromium from source code.
- Exploitation/malware analysis or offensive XSS attack payload generation.
- Canonical definition of Concurrency (reserved for M15).
- Canonical definition of Consistency (reserved for M14).

### 6.4 Hidden Prerequisites / Just-In-Time Support
- Minimal HTML/DOM literacy: Basic tags (`<html>`, `<head>`, `<body>`, `<div>`, `<script>`).
- Modern JavaScript basics: `fetch()`, `Promise`, `console.log`.
- Local HTTP file serving: Ability to run Python `http.server` to serve static test HTML/JS fixtures.

### 6.5 Candidate Real Observation / Activity
- **Activity M12-A (DevTools Rendering & Network Waterfall Trace):**
  - Serve a minimal course-owned HTML page with a stylesheet, an image, and a synchronous vs. deferred script.
  - Open an available supported desktop browser's DevTools Network/Performance tooling.
  - Record **the phases actually shown** for the selected request. On localhost or reused connections, DNS/connect/TLS rows may be absent, zero-like, cached, or folded differently; do not require every waterfall to display all phases.
  - Observe parser-blocking: compare timeline with synchronous `<script>` vs. `<script defer>`.
- **Activity M12-B (Localhost CORS & Origin Failure Exploration):**
  - Start two loopback Python HTTP servers on OS-assigned distinct ports and record both resulting origins.
  - Origin A serves an HTML page with JavaScript issuing a `fetch()` to Origin B.
  - Case 1: Origin B sends no CORS headers $\rightarrow$ browser console shows CORS error; request reached server, but client JS is denied access to the response.
  - Case 2: issue the same HTTP request with a non-browser client such as `curl`; it is not subject to browser CORS response filtering. This demonstrates the enforcement boundary without framing the exercise as a security bypass.
  - Case 3: Origin B returns an `Access-Control-Allow-Origin` value matching the **actual dynamically assigned Origin A**; a real browser context can then expose the response to the page when the rest of the CORS rules are satisfied.
- **Activity M12-C (Source Expedition EXP-03 — Chromium Process & Site Isolation):**
  - Inspect Chromium design document: `docs/process_model_and_site_isolation.md`.
  - Inspect `content/browser/site_instance_impl.cc` to locate how `SiteInstance` determines process reuse.
  - Inspect `content/browser/security/cpsp/child_process_security_policy_impl.cc` to locate browser-side process permission enforcement.

### 6.6 Required Learner Evidence
- Network panel screenshot/export showing the phases the selected browser actually reports for the request, with absent/reused/cached phases interpreted truthfully rather than treated as test failures.
- Browser console error log demonstrating a CORS failure, paired with a matching successful `curl` transcript to prove the difference between browser SOP enforcement and server authorization.
- Performance panel trace identifying main-thread blocking during a long-running JavaScript loop.
- Completed EXP-03 inspection card identifying the exact lines and mechanisms in Chromium source.

### 6.7 Evidence-Layer Classification
- **PRINCIPLE:** Process isolation as one defense-in-depth boundary; separation of parsing/style/layout/paint/compositing concerns; event-loop scheduling and main-thread responsiveness; least privilege.
- **SPECIFICATION:** WHATWG HTML Living Standard (Event loop, DOM, script processing); WHATWG Fetch Living Standard (CORS, origin computation); W3C Content Security Policy Level 3; W3C Navigation Timing Level 2.
- **IMPLEMENTATION:** Chromium multi-process implementation (`content/browser/`, Blink rendering engine, V8 JavaScript engine); Firefox Gecko/SpiderMonkey process architecture.
- **CURRENT PRACTICE:** Named browser/platform Site Isolation modes and diagnostic surfaces such as Chromium process internals/DevTools. A 60 Hz display has an illustrative period of about 16.7 ms, but this is not a universal browser “frame budget” or acceptance threshold.

### 6.8 Authoritative Sources
- WHATWG HTML Living Standard: *Event loops, processing model, and navigation*, continuously updated.
- WHATWG Fetch Living Standard: *CORS protocol, origin, and response filtering*, continuously updated.
- W3C *Content Security Policy Level 3*, **Working Draft** (latest published 13 Aug 2026 at review time); treat its status/current text as review-sensitive.
- Chromium Project: *Process Model and Site Isolation*, `https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md`.
- Reis and Gribble: *Isolating Web Programs in Modern Browser Architectures*, ACM EuroSys 2009.

### 6.9 Likely Misconceptions
1. *"One browser tab equals one operating system process."* (Chromium process assignment depends on SiteInstance/browsing-context relationships, platform, isolation mode, resource pressure, and process reuse. Under full Site Isolation, cross-site frames can use OOPIFs, but this is not a universal tab/process equation.)
2. *"Origin, Site, and Host mean the same thing."* (For ordinary HTTPS tuple origins, `https://shop.example.com:8080` and `https://api.example.com:8080` differ by host and therefore origin; a common registrable-domain site computation can group them under the same schemeful site. Opaque origins and special hosts mean the rule is not simply “site = eTLD+1.”)
3. *"CORS is an authentication/authorization mechanism that protects the server from unauthorized requests."* (CORS controls how a browser exposes cross-origin responses to requesting script. Server authentication/authorization must stand independently because non-browser HTTP clients are not governed by browser CORS enforcement.)
4. *"Adding a Content Security Policy (CSP) completely eliminates all XSS vulnerabilities."* (CSP is defense-in-depth; misconfigurations, unsafe nonces, or DOM-based script gadgets can still permit code execution).
5. *"The browser is single-threaded because JavaScript has an event loop."* (Browsers are multi-process/multi-threaded; Window/Document script commonly executes on a renderer main thread, while workers and browser internals have other agents/threads. The event-loop model is scoped to its agent, not the entire browser.)

### 6.10 Environment / Tool Constraints
- Interactive DevTools inspection requires a compatible browser/GUI environment; exact browser/tool availability must be preflighted rather than inferred from OS.
- In headless container / Codespace / WSL-without-GUI environments, learners cannot interactively inspect DevTools panels.
  - **Fallback:** if a real browser context is unavailable, retain course-owned reference traces/screenshots as **REFERENCE EVIDENCE ONLY** and mark live browser-specific observations `NO LIVE BROWSER OBSERVATION`. Do not introduce Playwright/Node as an undeclared Core dependency merely to manufacture live evidence.
- OQ-BP-006 baseline for browser versions remains open; no specific browser version is canonically locked.

### 6.11 Provenance / License Risk
- Chromium source code is licensed under a BSD-style license with copyright notices. Inspection via EXP-03 requires no code redistribution; linking and reading online source repositories is safe and royalty-free.

### 6.12 Implementation-Time Smoke Requirements
- With a real supported browser/headless-browser capability present, start two loopback origins on OS-assigned ports and verify the course CORS denial/allow cases. Without that capability, report `NO LIVE BROWSER CORS OBSERVATION`. Use harness deadlines only to prevent hangs; no fixed runtime is a curriculum invariant.

---

## 7. Protocol / Browser Specification Map

| Protocol / System Component | Governing Standards Body | Primary Normative Specification | Status as of 2026-09-03 | Obsoleted Prior Standards |
|---|---|---|---|---|
| **TCP** | IETF | **RFC 9293** (STD 7) | Normative Current Standard | RFC 793, RFC 879, RFC 2873, RFC 6093, RFC 6429, RFC 6528, RFC 6691 |
| **UDP** | IETF | **RFC 768** (STD 6) | Normative Current Standard | None |
| **IPv4** | IETF | **RFC 791** (STD 5) | Normative Current Standard | None |
| **IPv6** | IETF | **RFC 8200** (STD 86) | Normative Current Standard | RFC 2460 |
| **DNS** | IETF | **RFC 1034 / RFC 1035** (STD 13) | Normative Current Standard | None (updated by RFC 2181, 8484, etc.) |
| **TLS 1.3** | IETF | **RFC 8446** | Proposed Standard (Current) | RFC 5246 (TLS 1.2 obsoleted in practice) |
| **HTTP Semantics** | IETF | **RFC 9110** (STD 97) | Normative Current Standard | RFC 7230, 7231, 7232, 7233, 7234, 7235 |
| **HTTP Caching** | IETF | **RFC 9111** (STD 98) | Normative Current Standard | RFC 7234 |
| **HTTP/1.1 Framing** | IETF | **RFC 9112** (STD 99) | Normative Current Standard | RFC 7230 |
| **HTTP/2** | IETF | **RFC 9113** | Proposed Standard (Current) | RFC 7540 |
| **QUIC Transport** | IETF | **RFC 9000** | Proposed Standard (Current) | None |
| **QUIC TLS** | IETF | **RFC 9001** | Proposed Standard (Current) | None |
| **HTTP/3** | IETF | **RFC 9114** | Proposed Standard (Current) | None |
| **Web Platform / DOM** | WHATWG | **HTML Living Standard** | Living Standard | W3C HTML5 |
| **Fetch / CORS** | WHATWG | **Fetch Living Standard** | Living Standard | W3C CORS |
| **Content Security Policy** | W3C | **CSP Level 3** | **Working Draft** (13 Aug 2026 latest published at review) | CSP Level 1, CSP Level 2 |
| **Navigation Timing** | W3C | **Navigation Timing Level 2** | **Working Draft** (25 Feb 2026 latest published at review) | Navigation Timing Level 1 |

---

## 8. Canonical Concept Revisit & Future-First-Home Audit

### 8.1 Revisit Discipline Audit
The table below verifies that no concept is re-defined, and every mention in M10–M12 adheres strictly to the canonical definition established in its primary home:

| Concept ID | Canonical Name | First Home | M10–M12 Revisit Role & Context | Boundary Guardrail |
|---|---|---|---|---|
| **EC-CON-005** | 接口 (Interface) | M00 `L00-01` | M11 `L11-02`: HTTP as a uniform interface contract (methods, status codes, headers, representations). | Do not treat HTTP as a framework API or library implementation. Interface is the externally visible protocol contract. |
| **EC-CON-010** | 故障 (Failure) | M03 `L03-03` | M10 `L10-03`: Network failure taxonomy (DNS, route, timeout, refused). M11 `L11-02`: HTTP error statuses ($4\text{xx}, 5\text{xx}$) and proxy drops. | Maintain clear distinction between network transport failure, protocol rejection, and application error. |
| **EC-CON-011** | 缓存 (Caching) | M04 `L04-01` | M11 `L11-03`: HTTP caching (freshness, validation, ETag, 304, private/shared, CDNs). | Retaining prior results under a validity policy. A cache is not an authoritative store and does not guarantee durability. |
| **EC-CON-012** | 局部性 (Locality) | M04 `L04-02` | M11/M12: Network locality (CDN edge caching, keep-alive connection reuse, RTT minimization). | Locality is the tendency of accesses to occur near one another; it motivates caching but is not identical to caching. |
| **EC-CON-013** | 隔离 (Isolation) | M07 `L07-01` | M12 `L12-01` / `L12-03`: Multi-process browser architecture, renderer sandbox, site isolation. | Limiting interference/visibility. Isolation supports security but does not equal authorization. |
| **EC-CON-017** | 信任边界 (Trust Boundary) | M07 `L07-01` | M11 `L11-01`: TLS/PKI certificate trust stores. M12 `L12-03`: Same-Origin Policy, CORS, CSP. | Boundary where authority or enforcement changes. Inputs crossing it require validation. |
| **EC-CON-018** | 进程 (Process) | M06 `L06-01` | M12 `L12-01`: Browser process vs. renderer processes vs. GPU process. | Managed OS execution context with identity and address-space boundary. Not a tab, thread, or script. |

### 8.2 Future-First-Home Guardrails
1. **EC-CON-014 一致性 (Consistency):**
   - Scheduled First Home: **M14 `L14-02`**.
   - Audit Result: PASS. M11 caching discusses "freshness" and "validation"; M12 discusses "DOM and local storage updates". Neither module defines Consistency, uses the word "consistent" as a formal guarantee, or borrows transactional ACID / distributed consistency terminology.
2. **EC-CON-015 并发 (Concurrency):**
   - Scheduled First Home: **M15 `L15-01`**.
   - Audit Result: PASS. M12 `L12-04` covers the JavaScript event loop, microtask/task scheduling, and UI render blocking strictly as a **preview** and domain-specific execution model. It does not canonically define Concurrency, threads, race conditions, or synchronization primitives.

---

## 9. LAB-REQ-01 Re-Audit: HTTP Interface, Origin & Intermediary Trace

### 9.1 Feasibility and Normative Foundation
- **Selected Exercise:** Adapt RFC 9110 (HTTP Semantics) and RFC 9111 (HTTP Caching) into a learner-owned localhost HTTP origin + forwarding adapter + `curl` inspection lab.
- **Specification Status:** RFC 9110 (STD 97) and RFC 9111 (STD 98) are current, fully published Internet Standards (June 2022).
- **Core Feasibility:** the bounded fixture design is feasible with Python standard-library networking on loopback; implementation still must preflight `curl`, exercise process cleanup, and record actual host/runtime versions. This Research result does not close OQ-BP-006.

### 9.2 Controlled Failure and Trace Mechanics
1. **Direct Trace:** Client issues `curl -v http://127.0.0.1:<origin_port>/resource`. Inspects request headers, response headers, `ETag: "test-v1"`, and status `200 OK`.
2. **Forwarded Trace:** Client issues `curl -v http://127.0.0.1:<proxy_port>/resource`. Intermediary forwards to origin, appends `Via: 1.1 essential-cs-proxy`, and returns response. Client compares direct vs. forwarded headers.
3. **Conditional Validation Trace:** Client issues `curl -v -H 'If-None-Match: "test-v1"' http://127.0.0.1:<proxy_port>/resource`. Server returns `304 Not Modified` with no response content/body. The learner may compare transferred bytes on this fixture, but the lesson must not universalize a fixed bandwidth saving.
4. **Controlled Origin Failure:** Learner terminates `OriginServer`. The course intermediary maps the resulting upstream refusal to `502 Bad Gateway`. A distinct upstream-deadline fixture may demonstrate `504 Gateway Timeout`; neither mapping is generalized to every proxy implementation.

### 9.3 Safety and Environment Discipline
- **Localhost Only:** Strictly bound to `127.0.0.1`. No external network calls, no public proxying, no public internet dependencies.
- **Unprivileged:** Requires no `sudo`, no `root`, and no raw socket capabilities.
- **Deterministic Cleanup:** explicit ownership/PID tracking, shutdown/join logic, and a post-reset listener check establish cleanup. Port `0` allocation by itself does not guarantee that processes or sockets were cleaned up.

### 9.4 Licensing and Provenance Boundary
- RFC 9110/9111 are IETF publications under the IETF Trust Legal Provisions (TLP 4.0). Code components extracted from RFCs carry a 3-clause BSD license; text is copyrighted by IETF Trust.
- Essential CS will **not** bundle or reproduce RFC text or code. All server scripts, adapter code, test harnesses, and lesson text are **original Essential CS implementations** (Apache-2.0 / CC BY-SA 4.0). The RFCs are cited and linked by section number.

---

## 10. LAB-OPT-02 Rights & Currentness Recheck: Stanford CS144 Checkpoint 2

### 10.1 Assignment Inspection
- **Source Examined:** Stanford CS144 *Introduction to Computer Networking*, Fall 2025 offering. Checkpoint 2: *The TCP Receiver* (`https://cs144.github.io/assignments/check2.pdf`).
- **Technical Scope:** Implementing 32-bit sequence number wrapping (`Wrap32`) and the `TCPReceiver` class, which receives segments, reassembles bytes into a `ByteStream`, tracks acknowledgment numbers (`ackno`), and advertises receive window capacity (`window_size`).
- **Educational Value:** Outstanding demonstration of transport sequence space, sliding windows, out-of-order reassembly invariants, and flow control.

### 10.2 Rights and Redistribution Disposition
- **Repository Access:** The official course starter repository (`cs144/minnow`) is frequently kept private by Stanford instructors during active academic quarters.
- **License Status:** The course PDF and assignments do not grant a public license for downstream redistribution, adaptation, or inclusion in external educational curricula.
- **Recommendation:** LAB-OPT-02 **MUST REMAIN OPTIONAL AND LINK-ONLY**. Essential CS will **not** vendor, bundle, or distribute Minnow starter code, tests, or assignment PDFs. The curriculum provides an optional checkpoint guide with original conceptual prompts, directing learners to obtain the official materials independently.

---

## 11. EXP-03 Chromium Source-Route Recheck

### 11.1 Document and Source Route Verification
All three primary inspection targets have been rechecked and verified active on `chromium.googlesource.com` as of 2026-09-03:

1. **Design Document:**
   - Path: `docs/process_model_and_site_isolation.md`
   - URL: `https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md`
   - Key Content: Describes Chromium's multi-process model, Site Isolation goals (mitigating UXSS and Spectre), process reuse policies, and browsing context groups.
2. **Process Selection Implementation:**
   - Path: `content/browser/site_instance_impl.cc`
   - URL: `https://chromium.googlesource.com/chromium/src/+/main/content/browser/site_instance_impl.cc`
   - Key Content: Implements `SiteInstanceImpl::GetProcess()`, `SiteInfo`, and process assignment logic determining whether a navigation stays in an existing renderer or spawns a new process.
3. **Browser Policy Enforcement:**
   - Path: `content/browser/security/cpsp/child_process_security_policy_impl.cc`
   - URL: `https://chromium.googlesource.com/chromium/src/+/main/content/browser/security/cpsp/child_process_security_policy_impl.cc`
   - *Note on Path Relocation:* Formerly at `content/browser/child_process_security_policy_impl.cc`, the implementation was relocated into the `content/browser/security/cpsp/` subdirectory in recent Chromium refactorings.
   - Key Content: Implements the central browser-side security policy enforcing which renderer process is allowed to access specific origins, schemes, and files.

### 11.2 Bounded Learner Stopping Point
- Learners inspect only the documented sections and the designated entry functions (`SiteInstanceImpl::GetProcess` and `ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin`).
- Learners do not follow deeper internal helper methods, IPC bindings, or Blink rendering code.
- No local compilation of Chromium is required or permitted. Inspection is performed via web source viewers (Gitiles / GitHub mirrors).

---

## 12. Environment / Tool / Browser Capability Matrix

| Tool / Capability | Module Placement | Role in Curriculum | Classification | Environment Sensitivity & Constraints | Truthful Fallback / Skip Disposition | Checked Version / Source |
|---|---|---|---|---|---|---|
| **Python 3 `socket`** | M10 | Required for Core | Standard-library / Unprivileged | Available in supported CPython environments; exact exception types/errno/timing remain platform-specific. | Required preflight; if the runtime lacks sockets, Core network activity is blocked truthfully. | Author tested CPython 3.12/3.13; OQ-BP-006 remains open |
| **Linux `ss`** | M10 | Optional observation on Linux | Environment-Sensitive | Part of iproute2 when installed; many minimal images omit it. Read-only socket-table use is ordinarily unprivileged, subject to environment restrictions. | `TOOL UNAVAILABLE` is acceptable; preserve Python endpoint evidence instead. | Exact binary/version must be recorded by implementation preflight |
| **`ip route`** | M10 | Optional observation on Linux | Environment-Sensitive | Available when iproute2 is installed; route visibility can differ in containers/namespaces. | `TOOL UNAVAILABLE` / environment-limited is acceptable; do not synthesize host routing evidence. | Exact binary/version must be recorded by implementation preflight |
| **`nc` (netcat)** | M10 | Optional / Illustrative | Environment-Sensitive | Dialect fragmentation (OpenBSD vs. GNU flags). | Use Python socket one-liners instead of shell netcat. | OpenBSD netcat / nmap-ncat |
| **`traceroute`** | M10 | Optional / Capability-gated | Environment-Sensitive | Tool presence and privilege needs vary with implementation and ICMP/UDP/TCP probe mode. | `SKIP` if unavailable/restricted; course-owned reference traces must be labeled reference-only. | No canonical implementation/version pinned |
| **`tcpdump`** | M10 | Optional / Capability-gated | Privilege/Capability-Sensitive | Live capture commonly needs capture privileges/capabilities and may be blocked in hosted/container environments. | Never required for Core; `SKIP` is valid. Course-owned pre-captured traces are reference evidence, not live learner observation. | No canonical version pinned |
| **`curl`** | M11 / LAB-REQ-01 | Required tool for the selected Lab | Environment-Sensitive / Unprivileged | Common but not guaranteed installed; features/TLS backend/output vary by build. | Preflight exact `curl --version`; if absent, LAB-REQ-01 is environment-blocked unless Design explicitly provides an approved equivalent without changing the lab contract. | No canonical `curl 8.x` pin while OQ-BP-006 is open |
| **Python `http.server`** | M11, M12 | Candidate Core fixture | Standard-library / Unprivileged | Bind loopback to port `0` and record the assigned port; behavior/version belongs to the named Python implementation. | Preflight/runtime smoke required. | Author tested CPython 3.12/3.13; no canonical pin |
| **`openssl` CLI** | M11 | Optional / Auxiliary | Environment-Sensitive | Presence/version/provider configuration varies across distributions and Windows setups. | Use the course-owned Python `ssl`/trusted-local-certificate route when CLI is absent; do not require verification bypass. | No canonical version pinned |
| **Chromium / Chrome** | M12 | Preferred browser observation | Browser/GUI-Dependent / CURRENT PRACTICE | Availability, DevTools UI, process model and Site Isolation mode vary by version/platform. | If unavailable, record `NO LIVE BROWSER OBSERVATION`; course reference traces remain reference-only. | Record actual browser version at implementation; no `120+` baseline |
| **Firefox** | M12 | Optional alternative observation | Browser/GUI-Dependent / CURRENT PRACTICE | DevTools/process behavior differs from Chromium and by version/platform. | Optional; do not use Firefox observation as evidence for Chromium implementation claims. | Record actual version if used; no `120+` baseline |
| **Local HTML/JS Fixtures** | M12 | Required Core fixture content | Course-owned / Unprivileged | Use the minimal current HTML + ECMAScript features needed by the activity (`fetch`, Promise/microtask examples), served on loopback. | Browser capability remains separately gated. | Web Platform contracts from current WHATWG HTML/Fetch; no “HTML5/ES6” version pin |

---

## 13. Source Authority Register

| Topic / Mechanism | Primary Source | Authority Class | Source Status / Version Checked | Pedagogical Role |
|---|---|---|---|---|
| **TCP Protocol & State Machine** | RFC 9293 (STD 7) | SPECIFICATION | Normative Current Standard (Aug 2022) | Authoritative contract for 3-way handshake, state transitions, sequence numbers, and reset semantics. |
| **UDP Datagram Transport** | RFC 768 (STD 6) | SPECIFICATION | Normative Current Standard (Aug 1980) | Authoritative contract for minimal transport service and datagram boundary preservation. |
| **End-to-End Systems Principle** | Saltzer, Reed, Clark (1984) | PRINCIPLE | Foundational Systems Paper | Foundational rationale for transport vs. application reliability boundaries. |
| **IP Routing & Addressing** | RFC 791 / RFC 8200 | SPECIFICATION | Normative Current Standards | Packet switching, best-effort delivery, hop-by-hop forwarding. |
| **DNS Architecture & Records** | RFC 1034 / 1035 / 2181 | SPECIFICATION | Normative Current Standards | Hierarchical naming, authoritative delegation, caching, TTL. |
| **TLS 1.3 Security & Handshake** | RFC 8446 + RFC 9525 identity rules; RFC 9849 ECH where metadata privacy is discussed | SPECIFICATION | Standards Track / Proposed Standard as applicable | Fresh-handshake, PSK/0-RTT, service-identity and ECH boundaries; do not compress these into universal “1-RTT + forward secrecy + plaintext SNI” claims. |
| **HTTP Semantics** | RFC 9110 (STD 97) | SPECIFICATION | Normative Current Standard (Jun 2022) | Uniform interface, URI authority, method safety/idempotency, headers, status codes. |
| **HTTP Caching & Validation** | RFC 9111 (STD 98) | SPECIFICATION | Normative Current Standard (Jun 2022) | Cache keys, freshness lifetimes, conditional validation (ETag, 304). |
| **HTTP/2 & HTTP/3 Protocols** | RFC 9113 / RFC 9114 + RFC 9000/9001 | SPECIFICATION | **Proposed Standards** | Multiplexed stream/framing and QUIC integration; performance remains workload/implementation-specific. |
| **Browser Process Model & Site Isolation** | Chromium Design Docs & Reis et al. | IMPLEMENTATION / CURRENT PRACTICE | Current Chromium Source (Sep 2026) | Real-world multi-process browser architecture, sandboxing, and site isolation. |
| **HTML Event Loop & Document Lifecycle** | WHATWG HTML Living Standard | SPECIFICATION | Living Standard (Checked Sep 2026) | Normative web platform contract for DOM parsing, script execution, and event loop. |
| **Fetch & CORS Protocol** | WHATWG Fetch Living Standard | SPECIFICATION | Living Standard (Checked Sep 2026) | Normative platform contract for Same-Origin Policy and CORS headers. |
| **Content Security Policy** | W3C CSP Level 3 | SPECIFICATION (draft status) | **Working Draft, 13 Aug 2026** | Current draft contract for content restrictions; review-sensitive until later W3C maturity. |

---

## 14. Licensing, Redistribution & Adaptation Constraints

1. **Essential CS Original Artifacts (Apache-2.0 & CC BY-SA 4.0):**
   - All Python scripts, local HTTP servers, forwarding adapters, failure injection harnesses, HTML/JS test pages, and curriculum markdown prose are original works owned by Essential CS.
2. **IETF Specifications (RFC 9110, 9111, 9293, etc.):**
   - Copyright owned by IETF Trust under the Trust Legal Provisions (TLP 4.0).
   - Essential CS adapts only the *ideas and specifications* by citation and link. No large blocks of RFC text, diagrams, or ABNF grammar are copied verbatim.
3. **Stanford CS144 (LAB-OPT-02):**
   - The Fall 2025 Checkpoint 2 page/PDF is publicly accessible, but this review did not establish a permissive license granting Essential CS redistribution/adaptation rights for the assignment text, starter repository, or tests.
   - Therefore Essential CS keeps the activity **Optional + link-only** and does not bundle the assignment PDF, starter code, or tests unless rights are separately established.
4. **Chromium Source Code (EXP-03):**
   - Chromium source is distributed under BSD-style licensing plus third-party notices in the repository.
   - EXP-03 should remain link/source-inspection-first. Do not bundle snippets merely because they are short; if later Design wants to redistribute source excerpts, review the applicable file/header/license notices for that exact excerpt.

---

## 15. Misconceptions & Inference Boundaries

### 15.1 TCP Hotspots
- **DO NOT TEACH:** "TCP preserves application message boundaries."
  - *Reality:* TCP is a byte stream. The receiver cannot determine whether the sender made one `send()` of 100 bytes or 100 `send()`s of 1 byte. Applications must provide their own framing.
- **DO NOT TEACH:** "ACK means the remote application has processed the data."
  - *Reality:* A TCP ACK acknowledges sequence-space receipt at the peer TCP endpoint; it does not establish application consumption, validation, persistence, or business commit.
- **DO NOT TEACH:** "TCP guarantees delivery under every possible failure."
  - *Reality:* TCP provides an ordered reliable byte-stream abstraction while the connection can make progress; failures are surfaced according to the implementation/API and may leave application outcome ambiguous. Do not teach a fixed errno or one universal retransmission/failure path.
- **DO NOT TEACH:** "A request timeout proves the request did not take effect on the server."
  - *Reality:* The request may have been received and fully committed by the server, but the network failed before the response reached the client (the fundamental partial-failure ambiguity).

### 15.2 DNS Hotspots
- **DO NOT TEACH:** "One hostname maps to one permanent IP address."
  - *Reality:* DNS names routinely resolve to pools of rotating IP addresses for load balancing, Anycast routing, and CDN edge distribution.
- **DO NOT TEACH:** "TTL guarantees exact cache eviction timing across the entire internet."
  - *Reality:* Intermediate resolvers may clamp TTLs to arbitrary minimums or maximums, or evict records early under memory pressure.
- **DO NOT TEACH:** "A DNS lookup happens before every single HTTP request."
  - *Reality:* Operating systems, resolvers, and browsers cache DNS responses, and HTTP client connection pools reuse existing established TCP/TLS connections without re-resolving DNS.

### 15.3 TLS Hotspots
- **DO NOT TEACH:** "Encryption equals authorization or authenticity of application truth."
  - *Reality:* TLS encrypts the wire and authenticates the domain holder. It does not authenticate the end user, nor does it verify that the application logic is trustworthy or secure.
- **DO NOT TEACH:** "A valid green padlock / TLS certificate proves the website is not a scam."
  - *Reality:* A valid certificate proves only that the owner of the private key controls the specified domain name. Phishing sites routinely obtain valid TLS certificates.
- **DO NOT TEACH:** "TLS hides all metadata from eavesdroppers."
  - *Reality:* IP-layer endpoints, packet timing and sizes remain observable. Server-name exposure depends on deployment: ordinary ClientHello SNI can be visible, while RFC 9849 ECH can protect the inner ClientHello/SNI when configured and negotiated.

### 15.4 HTTP Hotspots
- **DO NOT TEACH:** "GET is always side-effect-free in every server implementation."
  - *Reality:* Safe semantics are a normative requirement of the specification; broken or naive applications frequently perform database mutations or state changes inside GET handlers.
- **DO NOT TEACH:** "An idempotent request is safe to retry blindly under any application semantics."
  - *Reality:* If a server API incorrectly models a state mutation as non-idempotent, or if partial execution occurred before failure, automatic retries can duplicate business operations.
- **DO NOT TEACH:** "Status 200 proves business correctness."
  - *Reality:* `200 OK` reports HTTP-level success for the method semantics; it does not establish a domain/business invariant, transaction commit, or correctness of the representation's meaning.
- **DO NOT TEACH:** "HTTP/2 or HTTP/3 is unconditionally faster than HTTP/1.1."
  - *Reality:* Relative performance depends on connection reuse, RTT, loss/reordering, CPU, implementation, congestion control and workload. No fixed version winner is a curriculum claim.

### 15.5 Browser Hotspots
- **DO NOT TEACH:** "One browser tab equals one operating system process."
  - *Reality:* In Chromium, process assignment depends on SiteInstance/browsing-context relationships, Site Isolation mode, platform, process reuse and resource constraints. Cross-site OOPIF separation is a current Chromium case under applicable isolation modes, not a browser invariant.
- **DO NOT TEACH:** "Origin, site, and host mean the same thing."
  - *Reality:* Ordinary HTTP(S) tuple-origin comparisons use scheme/host/port, but origins can be opaque. Site computation is schemeful and registrable-domain-derived when available, with special/opaque-host cases; it is not universally `scheme + eTLD+1`.
- **DO NOT TEACH:** "CORS is server-side security authentication."
  - *Reality:* CORS is user-agent enforcement controlling script access to cross-origin responses. Non-browser clients are not governed by that browser enforcement, so server authn/authz must be independent.
- **DO NOT TEACH:** "CSP fully prevents Cross-Site Scripting (XSS)."
  - *Reality:* CSP is a mitigation layer. Weak policies, unsafe inline directives, script gadgets, and non-script injection can bypass CSP.
- **DO NOT TEACH:** "The browser is single-threaded."
  - *Reality:* Browsers are multi-process/multi-threaded. Window/Document script commonly runs through an event loop on a renderer main thread, while workers and browser internals have separate agents/threads; scope the claim to the observed context.

---

## 16. Candidate Machine-Checkable vs. Reviewer-Required Evidence

### 16.1 Machine-Checkable Evidence Candidates
- **M10:**
  - Python test verifying `ConnectionRefusedError` (errno 111 / WSAECONNREFUSED) occurs within $< 50\text{ms}$ when connecting to an unused localhost port.
  - Python test verifying `TimeoutError` fires after approximately the configured socket timeout ($\pm 10\%$).
  - Python test verifying `socket.gaierror` when resolving `nonexistent.invalid`.
  - Byte-stream test verifying multiple small `send()` calls can be read by a single `recv()` call.
- **M11:**
  - Direct `curl` execution returning status 200 and expected `ETag`.
  - Forwarded `curl` execution returning status 200 and asserting the presence of the `Via` header.
  - Conditional `curl` execution with `If-None-Match` returning exactly status `304 Not Modified` and zero content length.
  - Proxy failure test verifying that stopping the origin server causes the intermediary to return status `502 Bad Gateway`.
- **M12:**
  - Automated Node.js / Python script verifying that a cross-origin fetch without CORS headers fails with a client-side type error, while a fetch with `Access-Control-Allow-Origin` succeeds.
  - Performance timing test measuring execution time of a synchronous blocking script loop.

### 16.2 Reviewer-Required Pedagogical & Architectural Evidence
- Verification that learner prose does not confuse TCP acknowledgment with application-level commitment.
- Verification that learner diagrams accurately trace trust boundaries and intermediary hops.
- Verification that learner explains why CORS does not prevent backend server abuse by non-browser clients.
- Verification that learner correctly identifies the three inspection points in Chromium source code (EXP-03).

---

## 17. Localhost / Browser Safety Model

All activities across M10–M12 strictly adhere to the following safety boundaries:

1. **Localhost Only by Default:** All server listeners, client connections, proxies, and test endpoints must bind exclusively to `127.0.0.1` or `::1`.
2. **No Port Scanning:** No automated scanning of ranges of ports. All tests communicate with specific, dynamically bound ephemeral ports.
3. **No Public Packet Injection:** No generation of raw, malformed, or spoofed packets to the public internet or local network.
4. **No ARP / DNS Spoofing:** No manipulation of local system resolver caches, hosts files, or ARP tables. Invalid domain testing must use RFC-reserved invalid TLDs (`.invalid` per RFC 2606).
5. **No Certificate-Bypass Training:** No teaching learners to disable TLS certificate verification (`curl -k` / `verify=False`) against third-party public websites. Local TLS testing uses self-contained test certificates with dedicated local verification contexts.
6. **No Production CDN / Cache Mutation:** No tests targeting external commercial CDNs or production websites.
7. **No Root / Sudo Requirement:** Core labs and activities must run entirely within standard user permissions. Any tool requiring elevated privileges (`tcpdump`, raw sockets) is classified as Optional / Capability-gated.

---

## 18. Design Handoff Requirements

The subsequent Design task (covering M10, M11, and M12) must implement the following structural and pedagogical specifications:

1. **Lesson Plan Architecture:**
   - **M10 (3 Lessons):**
     - `L10-01`: IP routing, packet switching, ports, sockets. Hands-on: Local socket creation, ephemeral ports, `ss` inspection.
     - `L10-02`: TCP reliability, 3-way handshake, sequence numbers, ACKs, byte stream vs. message boundary, UDP contrast. Hands-on: Observing byte-stream accumulation.
     - `L10-03`: Network failure modes. Hands-on: Controlled injection of DNS failure, connection refused (RST), and timeout.
   - **M11 (3 Lessons + LAB-REQ-01):**
     - `L11-01`: TLS 1.3 handshake, encryption, server authentication, PKI, certificate validation. Hands-on: TLS connection inspection.
     - `L11-02`: HTTP semantics (RFC 9110), uniform interface, methods, safe/idempotent properties, status codes, headers. Hands-on: Raw HTTP request/response with `curl -v`.
     - `L11-03`: Caching (RFC 9111), ETag, conditional requests, 304, intermediaries, CDNs, HTTP/1.1 vs. H2 vs. H3/QUIC. Hands-on: Cache validation trace.
     - `LAB-REQ-01`: HTTP interface, origin, and intermediary trace lab.
   - **M12 (4 Lessons + EXP-03):**
     - `L12-01`: Browser multi-process architecture, browser process, renderers, Site Isolation, sandboxing. Hands-on: DevTools process inspection / EXP-03 inspection.
     - `L12-02`: Document rendering pipeline (parse $\rightarrow$ DOM $\rightarrow$ CSSOM $\rightarrow$ layout $\rightarrow$ paint $\rightarrow$ composite), render-blocking scripts. Hands-on: Performance panel timeline.
     - `L12-03`: Web platform security model: Same-Origin Policy, CORS, CSP. Hands-on: Controlled localhost CORS failure and resolution.
     - `L12-04`: Event loop execution mechanics, tasks, microtasks, UI jank (**Concurrency preview only**). Hands-on: Blocking the main thread and observing UI freeze.
     - `EXP-03`: Chromium process model and Site Isolation source expedition.
2. **Visual Asset Requirements:**
   - M10: Diagram showing packet encapsulation (IP Header $\rightarrow$ TCP Header $\rightarrow$ Payload) and the 3-way handshake sequence with sequence/ACK numbers.
   - M10: Diagram illustrating the network failure spectrum (where in the path each error originates).
   - M11: Diagram showing direct vs. intermediary HTTP communication path, illustrating hop-by-hop vs. end-to-end headers.
   - M11: Diagram illustrating HTTP caching flow: fresh cache hit vs. conditional request with ETag yielding 304 Not Modified.
   - M12: Architectural diagram of Chromium's multi-process model (Browser Process, Renderers, GPU, Utility).
   - M12: Pipeline diagram of the rendering flow (Parse $\rightarrow$ DOM/CSSOM $\rightarrow$ Render Tree $\rightarrow$ Layout $\rightarrow$ Paint $\rightarrow$ Composite).
3. **Lab & Activity Specifications:**
   - Full implementation of LAB-REQ-01 starter and test harnesses in pure Python.
   - Explicit cleanup routines to kill all spawned child processes and free ports.

---

## 19. Open Risks / Open Question Interactions

- **OQ-BP-006 (Canonical Environment & Tool Version Pinning):**
  - Remains **OPEN**. This dossier provides concrete evidence that Python 3.12/3.13, `curl 8.x`, and standard Linux `iproute2` (`ss`) are sufficient for Core. Specific browser version pinning is avoided because browser architectures maintain stable platform contracts while internal versions advance rapidly.
- **OQ-BP-001 (AI Literacy) & OQ-BP-003 (Human-Facing Systems Boundary):**
  - Remain **OPEN / RFC-GATED**. S4 does not incorporate generative AI or formal HCI curriculum modules; M12 strictly teaches browser systems architecture and platform security models.
- **GDB Debt (from M03):**
  - Fully decoupled. M10–M12 requires zero GDB execution.
- **xv6 Grader Status (from M06):**
  - Fully decoupled. S4 does not depend on xv6 grading.

---

## 20. Final Recommendation

### **READY FOR DESIGN**

The research confirms that Stage 4 (M10–M12) is completely sound, technically feasible, safe, and aligned with all curriculum invariants. All primary sources, standards, and code routes have been independently verified against current 2026 specifications. The subsequent Design task can proceed immediately to develop the detailed Module Design Dossier for M10–M12.
