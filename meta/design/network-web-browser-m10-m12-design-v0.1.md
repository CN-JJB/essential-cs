# Networking & Web/Browser Platform Design Dossier (M10–M12) v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #71 — [Post-Research] M10–M12 Networking & Web/Browser Design Dossier v0.1
Base: `06206f8178021794d8406d14e94865ba4b827602`
Branch: `design/issue-71-m10-m12-network-web-browser`
Role: Curriculum Design Agent — Module, Lesson, Activity, Required-Lab, Source-Expedition & Evidence Designer
Scope: Design step only for M10–M12. This document is an instructional design contract; it is not learner-facing Lesson prose, runnable Lab code, or a curriculum architecture modification.

---

## 1. Design Status & Executive Recommendation

**Recommendation: READY FOR LESSON / ACTIVITY IMPLEMENTATION**

This Design Dossier translates the Lead-accepted and verified Research Dossier (`research/network-web-browser-m10-m12-v0.1.md`) into a concrete, rigorous, implementation-ready architectural contract for the three Modules comprising Stage 4 (S4):

$$\text{M10 (Networking I: IP, DNS & Transport)} \longrightarrow \text{M11 (Networking II: TLS, HTTP, CDN & Proxies)} \longrightarrow \text{M12 (Web & Browser: Integrated Case)}$$

### Core Integrity & Boundary Confirmations

1. **Canonical Map Preserved:** All 3 Modules, all 10 preliminary Lessons, Required Lab LAB-REQ-01, Optional Lab LAB-OPT-02, and Source Expedition EXP-03 are preserved exactly without addition, deletion, or renaming.
2. **Concept Registry First Homes Preserved:**
   - Zero new canonical concept first homes are introduced in M10–M12.
   - All 7 referenced concepts are treated strictly as **revisits** under their primary canonical definitions:
     - `EC-CON-005` **Interface** (First home: M00 `L00-01`) $\rightarrow$ M10/M11 protocol and socket interfaces.
     - `EC-CON-010` **Failure** (First home: M03 `L03-03`) $\rightarrow$ M10 network failure taxonomy, M11 HTTP error codes.
     - `EC-CON-011` **Caching** (First home: M04 `L04-01`) $\rightarrow$ M11 HTTP caching (freshness vs. validation).
     - `EC-CON-012` **Locality** (First home: M04 `L04-02`) $\rightarrow$ M11 CDN edge distribution and connection reuse.
     - `EC-CON-013` **Isolation** (First home: M07 `L07-01`) $\rightarrow$ M12 multi-process browser and renderer sandboxing.
     - `EC-CON-017` **Trust Boundary** (First home: M07 `L07-01`) $\rightarrow$ M11 TLS/PKI trust anchors, M12 SOP/CORS/CSP.
     - `EC-CON-018` **Process** (First home: M06 `L06-01`) $\rightarrow$ M12 browser coordinator vs. sandboxed renderers.
3. **Strict Future-Home Guardrails:**
   - `EC-CON-014` **Consistency** remains scheduled for its canonical first home in **M14 `L14-02`**. M11 caching discusses freshness and validation; M12 discusses DOM and local storage state; neither module uses the term "consistent" as an invariant guarantee or borrows transactional/distributed consistency terminology.
   - `EC-CON-015` **Concurrency** remains scheduled for its canonical first home in **M15 `L15-01`**. M12 `L12-04` covers the JavaScript event loop, microtasks, and UI render blocking strictly as a domain-specific **preview** and execution model, explicitly avoiding canonical definitions of concurrency, OS threads, race conditions, or synchronization primitives.
4. **Inherited Research Corrections Fully Integrated:**
   - TLS 1.3 is specified using **RFC 9846** (July 2026), which formally obsoletes RFC 8446. Service identity follows **RFC 9525** (obsoleting RFC 6125). Encrypted Client Hello is specified per **RFC 9849**.
   - CSP Level 3 and Navigation Timing Level 2 are explicitly marked as **W3C Working Drafts** with check dates and implementation recheck gates.
   - HTTP caching specifies that strong ETags are opaque (not inherently hashes) and that `304 Not Modified` carries **no response body/content** (avoiding false requirements of `Content-Length: 0`).
   - M10 activities avoid brittle assumptions (no hardcoded errnos, no fixed latency constants, no TEST-NET guaranteed timeout, no fixed `recv()` partition sizes). Loopback port 0 dynamic allocation and semantic disposition checks are enforced.
   - M12 browser boundaries maintain a strict 4-layer separation: Web Platform specification vs. Chromium implementation vs. live DevTools observation vs. reference evidence.
5. **LAB-REQ-01 Feasibility & Lifecycle Contract:** Preserves the HTTP interface, origin, and intermediary trace using original Essential CS localhost fixtures. Dynamic port 0 binding, startup readiness, PID tracking, and deterministic listener cleanup are fully specified.
6. **LAB-OPT-02 Rights Discipline:** Stanford CS144 Checkpoint 2 rights remain **UNESTABLISHED**. It is maintained strictly as Optional and link-only; no starter code, assignment text, or tests are bundled.
7. **EXP-03 Bounded Route:** Preserves the verified 3-step Chromium inspection route (`docs/process_model_and_site_isolation.md` $\rightarrow$ `content/browser/site_instance_impl.cc` $\rightarrow$ `content/browser/security/cpsp/child_process_security_policy_impl.cc`) with a single bounded inspection card and no compilation requirement.
8. **OQ-BP-006 Dispatched Safely:** OQ-BP-006 remains **OPEN**. Tools and runtimes are classified into Required Core, LAB-REQ-01 Required, Optional, Environment-Sensitive, Browser/GUI-Dependent, and Privilege-Sensitive, with explicit truthful fallbacks.

---

## 2. Scope, Constraints & Inherited Research Corrections

This Design Dossier directly incorporates the normative corrections, evidence layers, and claim boundaries established in the accepted Research Dossier (`research/network-web-browser-m10-m12-v0.1.md`):

### 2.1 Normative Specification Currentness

1. **TLS 1.3 Specification (`RFC 9846`):**
   - RFC 9846 was published in July 2026 by the IETF, formally obsoleting RFC 8446. The curriculum references RFC 9846 as the current authoritative standard for TLS 1.3.
   - RFC 9525 (published November 2023) obsoletes RFC 6125 for TLS Service Identity verification in application protocols.
   - RFC 9849 (published March 2026) specifies Encrypted Client Hello (ECH).
   - *Negative Guardrails:*
     - Do NOT teach that all TLS 1.3 handshakes are an identical 1-RTT exchange (PSK resumption and 0-RTT early data have distinct handshake mechanisms and security trade-offs).
     - Do NOT teach that every PSK mode provides DHE forward secrecy (`psk_ke` does not; `psk_dhe_ke` does).
     - Do NOT teach that a valid TLS certificate implies the remote business or application is trustworthy.
     - Do NOT teach that SNI is universally plaintext (conditional on ECH deployment) or that ECH hides all metadata (IP endpoints, packet sizes, and traffic timing remain visible).

2. **Web Platform Specification Currentness & Draft Status:**
   - At Research acceptance:
     - **Content Security Policy Level 3:** W3C Working Draft (latest published 13 Aug 2026).
     - **Navigation Timing Level 2:** W3C Working Draft (latest published 25 Feb 2026).
   - *Draft Discipline:* The curriculum explicitly identifies CSP3 and Navigation Timing Level 2 as Working Drafts, avoiding claims that they are final W3C Recommendations, and requires implementation-time rechecking of normative text.

3. **HTTP Semantics & Caching Boundaries (RFC 9110 / RFC 9111):**
   - **Uniform Interface:** URIs identify resources; HTTP messages transfer representations of those resources.
   - **Safe Methods:** `GET`, `HEAD`, `OPTIONS`, `TRACE` are safe because the client does not request state-changing semantics. Incidental server operations (e.g., logging, metrics, cache population) do not violate safety.
   - **Idempotent Methods:** Multiple identical requests have the same intended effect as a single request (`GET`, `HEAD`, `PUT`, `DELETE`, `OPTIONS`, `TRACE`). Idempotency is a client-intended semantic property, not an absolute guarantee that automatic blind retries are universally safe under arbitrary partial failures.
   - **Status Codes:** `200 OK` establishes HTTP protocol success; it does not prove business-domain correctness.
   - **Entity Tags (ETags):** Strong ETags are opaque validators assigned by the origin; they are not required to be cryptographic hashes. Weak ETags (`W/"..."`) are valid only for weak comparison.
   - **304 Not Modified:** A 304 response to a conditional request transfers **no message content/body**. It may carry headers intended to update cached metadata, including `Content-Length` reflecting the representation size; tests must never assert `Content-Length: 0`.
   - **Wire Framing & Transport Evolution:**
     - HTTP/1.1 (RFC 9112) persistent connections are default; persistence is not "turned on" by the historical `Keep-Alive` header. Single-connection serialization causes application-layer head-of-line blocking.
     - HTTP/2 (RFC 9113) multiplexes concurrent binary streams over a single TCP connection. Because streams share one TCP connection, packet loss causes transport-layer head-of-line blocking across all multiplexed streams.
     - HTTP/3 (RFC 9114) over QUIC (RFC 9000) eliminates transport-layer head-of-line blocking between independent streams by running over UDP with per-stream loss recovery. However, HTTP/3 does not guarantee universal speedup; performance depends on RTT, loss rates, server/client CPU overhead, and network topology.

4. **M10 Deterministic Evidence Principles:**
   - Network tests must not assert fixed round-trip times, hardcoded errnos (e.g., assuming `111` or `ECONNREFUSED` string across all OSes), or arbitrary timeout ratios.
   - Port scanning, public malformed packets, and raw socket injection are strictly prohibited.
   - Port 0 allocation on `127.0.0.1` ensures collision-free loopback testing.
   - Deterministic localhost refusal is achieved by connecting to a verified unbound loopback port.
   - Deterministic read timeout is achieved using a course-owned accepted-but-silent server that accepts the TCP connection and withholds application bytes until the client's configured read deadline expires.
   - DNS failure testing uses the RFC 2606 reserved `.invalid` TLD and is capability-gated; if local resolver capability is unavailable, the harness records `NO LIVE DNS FAILURE OBSERVATION` rather than fabricating an output.

5. **Web & Browser Architecture Boundaries:**
   - Always maintain the strict 4-layer evidence separation:
     1. Web Platform specification (WHATWG HTML, WHATWG Fetch, W3C CSP).
     2. Chromium implementation / current practice (`content/browser/`, Site Isolation, `ChildProcessSecurityPolicy`).
     3. Live browser DevTools / console observation.
     4. Course-owned reference evidence (used strictly as fallback).
   - *Architecture Guardrails:*
     - Do NOT teach "one tab = one process"; Chromium assigns processes based on SiteInstance, browsing context groups, platform memory pressure, and Site Isolation mode.
     - Do NOT teach that Site Isolation is the Same-Origin Policy; Site Isolation is an OS-process level defense-in-depth mitigation against UXSS and Spectre-class microarchitectural leakage.
     - Do NOT teach that origins are always simple 3-tuples; HTML specifies tuple origins and opaque origins.
     - Do NOT teach that sites are universally `scheme + eTLD+1`; site computation accounts for special schemes, opaque hosts, and registrable domain rules.
     - Do NOT teach that CORS is server-side authentication or authorization; CORS is user-agent response read-access enforcement. Non-browser clients (`curl`, Python) are not constrained by CORS.
     - Do NOT teach that CSP is an absolute guarantee against XSS; CSP is defense-in-depth.
     - Do NOT teach that the browser is single-threaded; browsers are multi-process and multi-threaded; JavaScript Window/Document execution runs on an agent's main thread via an event loop.
     - Do NOT teach a rigid "one macrotask $\rightarrow$ one microtask $\rightarrow$ render" cycle or a fixed 16.7 ms frame budget; rendering opportunities occur conditionally.

---

## 3. Cross-Module Capability Chain

The three Modules of Stage 4 (S4) construct an integrated journey from low-level physical packet traversal up to the modern web browser as a secure operating environment for untrusted software:

```
[M10: Networking I — IP, DNS & Transport]
  L10-01: Name (DNS) vs Address (IP) vs Route (Hop) vs Endpoint (Socket/Port)
    |
    v
  L10-02: TCP Reliability Mechanics (Handshake, Sequence Space, Cumulative ACK, Byte Stream) vs UDP
    |
    v
  L10-03: Network Failure Spectrum (DNS Fail, Host Refusal, Read Timeout, Reset, Application Ambiguity)
    |
    | (Transport byte stream is established, but payloads lack security and application structure)
    v
[M11: Networking II — TLS, HTTP, CDN & Proxies]
  L11-01: Cryptographic Channel (TLS 1.3 RFC 9846, Trust Anchors RFC 9525, ECH RFC 9849)
    |
    v
  L11-02: Uniform Interface & Semantics (HTTP RFC 9110, Methods, Status Codes, Resource vs Representation)
    |
    v
  L11-03: Performance & Distribution (Caching RFC 9111, Freshness vs Validation, Intermediaries, H1/H2/H3)
    |
    +---> LAB-REQ-01: HTTP Interface, Origin & Intermediary Trace (Original localhost fixture + curl)
    |
    +---> LAB-OPT-02: Stanford CS144 Checkpoint 2 (The TCP Receiver — Optional, link-only)
    |
    | (Secure application protocol is established; now examine the ultimate client runtime)
    v
[M12: Web & Browser: The Integrated Case]
  L12-01: Browser Systems Architecture (Multi-Process, Sandboxing, Site Isolation Chromium Case)
    |
    v
  L12-02: Document Rendering Pipeline (HTML/CSS Parse -> DOM/CSSOM -> Style -> Layout -> Paint -> Composite)
    |
    v
  L12-03: Web Security Model (Same-Origin Policy, Fetch CORS, CSP Defense in Depth)
    |
    v
  L12-04: Execution & Responsiveness (Window Event Loop, Tasks, Microtasks, UI Jank — Concurrency Preview)
    |
    +---> EXP-03: Chromium Process Model & Site Isolation Source Expedition
```

This sequence equips the learner to understand exactly what happens under the hood when a user types a URL or an application issues an API call, connecting hardware packets to browser pixels without hand-waving or black-box abstractions.

---

## 4. Module M10 Design — Networking I: IP, DNS & Transport

### 4.1 Module-Level Specification
- **Title:** M10 — Networking I: IP, DNS & Transport (Area 08)
- **Primary Competency:** Trace
- **Growth Competencies:** Explain, Diagnose, Judge, Estimate
- **Module Prerequisites:** Hard: M06 (Processes, Syscalls), M08 (Files, File Descriptors & System I/O)
- **Capability Transition:** Transition from treating network communication as an abstract, magically reliable pipe (`requests.get("https://...")`) to understanding the layered, best-effort packet delivery mechanism of IP, the hierarchical indirection of DNS, and how transport protocols (TCP/UDP) construct distinct abstractions (ordered reliable stream vs. independent datagrams) over unreliable physical networks. Learners gain the ability to trace packet traversal and diagnose failure origins.

---

### 4.2 Lesson L10-01: “How does a message cross the internet?”

1. **Learner Question:** How does my computer send data across thousands of miles of physical cables and routers to reach a specific program on a remote server?
2. **Before / After Capability:**
   - *Before:* Assumes data moves through a direct, magic pipe connecting a program to a domain name; confuses IP address, port, route, and domain name.
   - *After:* Can trace a bounded packet path from a local application socket through host routing/forwarding decisions, distinguishing a DNS name from the network-layer address returned by resolution and distinguishing transport ports/sockets from process identity. IP addresses participate in forwarding and interface identification; they are not a universal permanent "topological identity" for a host.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Hard prerequisites: `M06` (processes and execution context) and `M08` (file descriptors and I/O abstractions).
   - Support: Port-number discipline: IANA divides the 16-bit port space into System Ports (0–1023), User Ports (1024–49151), and Dynamic/Private Ports (49152–65535). Binding to port `0` instructs the OS kernel to dynamically allocate an available port; the activity inspects the assigned port via `getsockname()` rather than hardcoding a port.
4. **Concepts:** Revisits **Interface** (EC-CON-005) and **Representation** (EC-CON-003). No new first homes.
5. **Mental Model:** Layered indirection. A name is resolved into one or more network-layer addresses; the host routing table chooses how to forward toward a destination; and the transport layer demultiplexes traffic to sockets/endpoints. Names, addresses, routes, ports, sockets, and processes are related but not interchangeable identifiers.
6. **Mechanism Sequence:**
   $$\text{Application Name} \xrightarrow{\text{getaddrinfo (DNS)}} \text{IP Address} \xrightarrow{\text{Route Table Lookup}} \text{Next-Hop Interface} \xrightarrow{\text{Packet Switching}} \text{Host Port Demux} \xrightarrow{} \text{Target Socket}$$
7. **Prediction-Before-Observation:** If two distinct Python programs both bind to port 0 on `127.0.0.1`, will the operating system assign them the same port number or distinct port numbers?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe:* Run a Python script that creates a TCP socket, binds to `('127.0.0.1', 0)`, and prints `getsockname()`. Observe that the operating system assigns a non-zero port number. If Linux `ss` is available, run `ss -tan` to observe the socket in the `LISTEN` state.
   - *Build:* Construct a client socket that connects to the dynamic server port and transmits a 16-byte payload; server reads and echoes the payload.
   - *Break:* Use the course-owned loopback fixture to connect to a verified unbound port and observe the transport failure disposition. A host-route/no-route observation is optional and environment-sensitive; Core must not depend on an arbitrary external or unroutable address.
   - *Explain:* Explain that the basic IP forwarding decision is made from network-layer destination/prefix information, while real routers/middleboxes may additionally inspect transport/application metadata for policy, filtering, QoS, telemetry, or load-balancing. Do not teach "routers can only see the IP header" as a universal law.
   - *Judge:* Evaluate the trade-off of decoupling names from addresses: why not route internet packets directly using human-readable domain names?
9. **Required Commands / Tools:** Python 3 standard library (`socket`), optional Linux CLI (`ss`, `ip route`).
10. **Machine-Checkable Evidence:** Test harness starts server on port 0, captures the assigned port from stdout/log, connects client, validates payload receipt, and asserts zero remaining open listeners after termination.
11. **Reviewer-Required Evidence:** Reviewer evaluates the learner's written explanation distinguishing the four network identifiers: Domain Name, IP Address, Next-Hop MAC/Interface, and Transport Port/Socket.
12. **Misconceptions Addressed:**
    - "A domain name connects directly to a running process." (DNS resolves names to IP addresses; ports and sockets demultiplex traffic to processes).
    - "One domain name maps to exactly one permanent IP address." (DNS routinely maps a single name to multiple dynamic IP addresses for load balancing, CDN edge steering, and Anycast).
    - "A port number belongs permanently to an executable file." (Ports are operating system kernel resources dynamically bound to sockets).
13. **What You Can Ignore—for Now:** BGP border routing algorithms, autonomous systems (AS) graph mathematics, link-layer Ethernet framing details, switch CAM tables.
14. **Progressive Support:**
    - *Question:* When you execute `socket.bind(('127.0.0.1', 0))`, what port is bound, and how do you find it?
    - *Hint 1:* Port 0 is a special sentinel value telling the OS kernel to allocate an available ephemeral port.
    - *Hint 2:* Inspect the socket object's local address using `sock.getsockname()`.
    - *Expected Observation:* `getsockname()` returns a tuple `('127.0.0.1', <port>)` where `<port>` is a non-zero integer.
    - *Full Explanation:* The OS network stack manages local port allocation. Passing 0 avoids hardcoded port collisions and asks the OS to select an available local port according to that host's policy; the learner records the actual assigned value rather than assuming one fixed ephemeral range.
15. **Visual Requirements:** Diagram illustrating the 4-layer indirection: Domain Name (Identity) $\rightarrow$ IP Address (Location) $\rightarrow$ Next-Hop Gateway (Route) $\rightarrow$ Transport Port (Process demultiplexing endpoint).
16. **Exit Criteria:** Learner executes a loopback socket exchange on port 0, inspects the assigned endpoint, and writes a clear trace of the name-to-port indirection path.
17. **Competency Mapping:** Trace (Primary: socket $\rightarrow$ route $\rightarrow$ packet), Explain (Growth: layered addressing).
18. **Provenance / Source Anchors:** RFC 791 (IPv4), RFC 8200 (IPv6), RFC 1034/1035 (DNS), Saltzer et al. (End-to-End Arguments in System Design, 1984).
19. **Failure / Inference Limits:** Loopback (`127.0.0.1`) bypasses physical network interface controllers (NICs), physical cables, and MTU fragmentation; host routing observed on loopback is internal kernel dispatch.

---

### 4.3 Lesson L10-02: “How does reliable work over unreliable links?”

1. **Learner Question:** If the underlying network can drop, reorder, or duplicate packets, how does TCP deliver an exact, in-order stream of bytes without missing a single character?
2. **Before / After Capability:**
   - *Before:* Thinks TCP magically prevents network packet loss, or that a TCP ACK means the remote program has finished processing the request; confuses packet boundaries with application message boundaries.
   - *After:* Can trace the TCP 3-way handshake, sequence/acknowledgment numbers, cumulative ACKs, sliding window flow control, and byte-stream accumulation, contrasting TCP streams with UDP datagrams.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L10-01` (Sockets, Ports, IP encapsulation).
   - Support: Introduce sequence number intuition as byte offsets in a continuous file-like stream rather than packet counters.
4. **Concepts:** Revisits **Interface** (EC-CON-005) and **Abstraction** (EC-CON-002).
5. **Mental Model:** Sequence space over an unreliable substrate. TCP assigns a sequence number to every individual payload byte, uses positive acknowledgments with retransmission timers to repair packet drops, and reconstructs an in-order byte stream independent of network packet boundaries.
6. **Mechanism Sequence:**
   $$\text{Client SYN (seq=x)} \xrightarrow{} \text{Server SYN-ACK (seq=y, ack=x+1)} \xrightarrow{} \text{Client ACK (ack=y+1)} \xrightarrow{} \text{ESTABLISHED}$$
   $$\text{Data Transfer: Byte Stream Segments with Sequence Numbers} \xrightarrow{\text{Cumulative ACK}} \text{Receiver Sliding Window Buffer}$$
7. **Prediction-Before-Observation:** If a client sends 3 separate messages of 100 bytes each using 3 `send()` calls, will the receiving server always receive them in exactly 3 `recv()` calls of 100 bytes each?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe:* Run a Python client that transmits 5 small chunks with brief pauses. The server calls `recv(4096)` and logs the byte count returned per call. Observe that TCP coalesces or partitions bytes arbitrarily based on OS buffering.
   - *Build:* Construct a stream reader loop that buffers incoming bytes from `recv()` until an explicit application delimiter (`\n` or length prefix) is found, correctly extracting complete application messages.
   - *Break:* Send data without application delimiters; demonstrate that the receiving application cannot determine message boundaries from TCP alone. Contrast this with UDP (`socket.SOCK_DGRAM`) where `recvfrom()` preserves datagram boundaries.
   - *Explain:* Explain why receiving a TCP ACK proves only that the peer operating system's TCP receive buffer accepted the bytes, not that the application process read, validated, or committed them.
   - *Judge:* Contrast TCP and UDP trade-offs: explain why real-time audio/video streaming or DNS lookups often choose UDP over TCP despite packet loss.
9. **Required Commands / Tools:** Python 3 standard library (`socket`).
10. **Machine-Checkable Evidence:** Test script verifies that the application framing parser reconstructs the exact original message sequence regardless of the partition sizes returned by `recv()`.
11. **Reviewer-Required Evidence:** Reviewer checks that learner explanations clearly distinguish TCP byte streams from UDP datagrams, correctly explain why TCP ACK does not equal application commit, and correctly state the IPv4 vs. IPv6 UDP checksum rules (RFC 8200: UDP checksum is mandatory in IPv6 with narrow tunnel exceptions, whereas in IPv4 it is optional).
12. **Misconceptions Addressed:**
    - "TCP preserves application message boundaries." (TCP is a continuous byte stream; application framing must be implemented by the application protocol).
    - "Receiving a TCP ACK proves the server executed my business transaction." (A TCP ACK confirms sequence-space delivery to the kernel buffer; application processing is completely separate).
    - "UDP has no error detection at all." (UDP includes an optional 16-bit checksum in IPv4, and mandatory checksum in IPv6 per RFC 8200).
13. **What You Can Ignore—for Now:** CUBIC/BBR congestion control mathematical curves, fast retransmit / SACK duplicate ACK heuristics, TCP SYN cookies, zero-window probing timers.
14. **Progressive Support:**
    - *Question:* Why does calling `recv(1024)` not guarantee that you get the exact 100 bytes sent by a single `send(b"hello...")` call?
    - *Hint 1:* TCP is a byte stream, not a packet or message transport.
    - *Hint 2:* TCP exposes an ordered byte stream, so neither TCP packet/segment boundaries nor the sender's `send()` call boundaries are part of the receiver's `recv()` interface contract.
    - *Expected Observation:* The byte count returned by `recv()` depends on network arrival and OS buffer state, not on the sender's `send()` call boundaries.
    - *Full Explanation:* TCP provides an ordered stream abstraction. To read discrete messages, the application layer must define its own framing, such as fixed lengths, length prefixes, or delimiter tokens.
15. **Visual Requirements:** Diagram contrasting (a) TCP packet encapsulation (IP Header $\rightarrow$ TCP Header $\rightarrow$ Payload), (b) the 3-way handshake sequence with sequence/ACK numbers, and (c) TCP byte-stream buffering vs. UDP discrete datagrams.
16. **Exit Criteria:** Learner builds a functioning stream framing parser and explains the fundamental difference between network transport acknowledgment and application-level commitment.
17. **Competency Mapping:** Trace (Primary: handshake and sequence progression), Explain (Growth: byte stream vs. datagram).
18. **Provenance / Source Anchors:** RFC 9293 (TCP, obsoleting RFC 793), RFC 768 (UDP), RFC 8200 (IPv6).
19. **Failure / Inference Limits:** Localhost socket pairs do not exhibit physical packet loss, duplicate packets, or out-of-order delivery; sequence numbers and sliding windows are observed through protocol structure rather than loss recovery.

---

### 4.4 Lesson L10-03: “Why is my request timing out?”

1. **Learner Question:** When I click a button or run a command and it hangs before printing "Connection timed out", what actually broke, where did it fail, and did my request execute on the server?
2. **Before / After Capability:**
   - *Before:* Thinks "Timeout" means the server is offline or dead, and assumes a timeout guarantees that nothing happened on the server.
   - *After:* Can systematically diagnose network failures across the taxonomy (name resolution failure, route unreachable, active connection refusal, read deadline timeout, connection reset), explain the fundamental partial-failure ambiguity of distributed systems, and determine when a retry is safe vs. dangerous.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisites: `L10-01` (Addressing & Sockets) and `L10-02` (Handshake & ACKs).
   - Support: Use monotonic timing (`time.perf_counter()`) to measure elapsed time, while noting that clock synchronization theory belongs to later modules (M20).
4. **Concepts:** Revisits **Failure** (EC-CON-010). No new first homes.
5. **Mental Model:** The network failure spectrum and partial failure ambiguity. A timeout is an expired local deadline, not a statement of where packets stopped. In a distributed network, the client cannot distinguish whether the request was lost before reaching the server, failed during server execution, or completed on the server while the response was lost on the return path.
6. **Mechanism Sequence:**
   $$\text{1. DNS Resolution} \xrightarrow{\text{Fail: Host Not Found}} \text{Abort (No IP)}$$
   $$\text{2. Connect (SYN)} \xrightarrow{\text{Fail: RST / ECONNREFUSED}} \text{Abort (Immediate Refusal)}$$
   $$\text{3. Connect (SYN)} \xrightarrow{\text{Fail: Silent Drop}} \text{Connect Timeout}$$
   $$\text{4. Connected (ESTABLISHED)} \xrightarrow{\text{Send Request}} \text{Server Delays / Network Drops Response} \xrightarrow{\text{Read Timeout}}$$
   $$\text{5. In-Flight Abruption} \xrightarrow{\text{Fail: RST / Peer Crash}} \text{Connection Reset (ECONNRESET)}$$
7. **Prediction-Before-Observation:** If a client sends an HTTP request to charge a credit card and receives a "Read Timeout" after 5 seconds, is it safe to automatically retry the request immediately?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe (Case 1: Refusal):* Attempt to connect to a course-selected verified-unbound port on `127.0.0.1`. Record the actual runtime/OS refusal disposition and elapsed sample. Do not require a fixed exception class, errno, text, or latency.
   - *Observe (Case 2: Read Timeout):* Connect to a course-owned accepted-but-silent server that accepts the TCP connection but deliberately withholds application bytes. Configure a bounded client read deadline. Record the actual timeout disposition and elapsed sample; use a separate generous harness watchdog only to prevent hangs, not as a timing invariant.
   - *Observe (Case 3: DNS Failure):* Attempt to resolve a domain name in the RFC 2606 reserved `.invalid` TLD (e.g., `test-target.invalid`). If resolver capability is present, record the resolution failure. If resolver capability is absent, record `NO LIVE DNS FAILURE OBSERVATION`.
   - *Explain:* Contrast the course-owned active-refusal path with expiry of a local read deadline on an established but silent connection. The two dispositions usually have different elapsed behavior in this fixture, but no fixed speed ratio or exact transport cause is a curriculum invariant.
   - *Judge:* Analyze why blindly retrying a timed-out request can duplicate application effects (for example, a payment mutation) when the remote outcome is unknown. Keep the lesson at partial-failure/retry ambiguity; do not introduce a formal Two Generals treatment.
9. **Required Commands / Tools:** Python 3 standard library (`socket`, `time`).
10. **Machine-Checkable Evidence:** Test script runs all three failure cases: asserts refusal on unbound port, asserts read timeout on silent server, verifies clean process cleanup, and records raw elapsed samples without asserting fixed numeric latency thresholds.
11. **Reviewer-Required Evidence:** Reviewer evaluates the learner's explanation of partial failure ambiguity: the learner must explain why a timeout leaves the remote server state uncertain, and why an ACK does not establish application-level execution.
12. **Misconceptions Addressed:**
    - "A request timeout means the server definitely did not receive or process the request." (The server may have received and executed the request, but the network failed before the client received the response).
    - "Connection refused means the server machine has crashed or is powered off." (In the course-owned loopback fixture, an unbound listener produces a refusal disposition. On arbitrary networks, hosts/firewalls/policy devices can reject or drop traffic differently, so refusal alone is not a universal proof of one root cause).
    - "Network failures always produce immediate, descriptive error codes." (Packet loss or server hangs produce silent delays that surface only when a local timer expires).
13. **What You Can Ignore—for Now:** Two-phase commit (2PC), Paxos/Raft consensus algorithms (reserved for S6/M16+), exponential backoff and jitter mathematical derivations.
14. **Progressive Support:**
    - *Question:* Why do the course-owned unbound-port and accepted-but-silent fixtures produce different failure dispositions and elapsed samples?
    - *Hint 1:* Look at what the operating system kernel does when a TCP SYN arrives on an unbound port.
    - *Hint 2:* Look at what happens when a connection is established but no bytes are sent back.
    - *Expected Observation:* The unbound-port fixture produces a refusal disposition, while the accepted-but-silent fixture remains connected until the configured read deadline expires. Record the actual exception classes/messages and elapsed samples without fixed thresholds.
    - *Full Explanation:* In the course loopback case, the OS reports that no listener accepted the selected endpoint; in the silent-server case the TCP connection is established but no application bytes arrive before the client's local read deadline. The lesson distinguishes these interface-level dispositions without universalizing an exact packet/error/timing path.
15. **Visual Requirements:** Diagram of the network failure spectrum showing the stage where each disposition becomes visible to the client (resolution, connect, established-stream read, peer close/reset) plus an explicit callout that the same client-visible timeout/error can have multiple underlying causes.
16. **Exit Criteria:** Learner diagnoses failure modes from command-line outputs and writes an architectural defense explaining why a timeout leaves remote state ambiguous.
17. **Competency Mapping:** Diagnose (Primary: network error classification), Judge (Growth: retry safety and partial failure), Estimate (Growth: timeout threshold trade-offs).
18. **Provenance / Source Anchors:** RFC 9293 (TCP failure handling), RFC 2606 (Reserved Top Level DNS Names), Saltzer, Reed, Clark (End-to-End Arguments in System Design).
19. **Failure / Inference Limits:** On arbitrary wide-area networks, middleboxes and firewalls can drop SYN packets silently, causing a connect timeout where a localhost system would report an immediate RST refusal; learners must not assume RST is universal.

---

## 5. Module M11 Design — Networking II: TLS, HTTP, CDN & Proxies

### 5.1 Module-Level Specification
- **Title:** M11 — Networking II: TLS, HTTP, CDN & Proxies (Area 08)
- **Primary Competency:** Explain
- **Growth Competencies:** Trace, Observe, Diagnose, Judge, Estimate
- **Module Prerequisites:** Hard: M10 (Networking I: IP, DNS & Transport)
- **Capability Transition:** Learners transition from raw transport streams to secure, structured application protocol interactions. They master the HTTP request-response model, uniform interface semantics, cache freshness and validation mechanisms, intermediary roles in distributed systems, and the transport evolution from HTTP/1.1 to HTTP/2 and HTTP/3/QUIC. They learn to separate protocol semantics from wire encoding and understand the cryptographic boundaries of TLS.

---

### 5.2 Lesson L11-01: “How do I talk securely to a server?”

1. **Learner Question:** When I connect to `https://`, how does my computer know it is actually talking to the intended server, and what prevents someone on the same Wi-Fi from reading or tampering with my data?
2. **Before / After Capability:**
   - *Before:* Thinks HTTPS just means "encrypted", assumes the green padlock proves a business is trustworthy, or believes TLS hides all traffic metadata from eavesdroppers.
   - *After:* Can explain how TLS 1.3 (RFC 9846) establishes confidentiality, integrity, and server authentication; trace X.509 certificate path verification using local trust anchors (RFC 9525); articulate forward secrecy boundaries; and describe the metadata visibility limits of SNI and Encrypted Client Hello (RFC 9849).
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Hard prerequisite: `L10-02` (TCP connections and streams).
   - Support: Dedicated course-owned certificate fixture and isolated verification context. The activity provides a local self-signed root CA and leaf certificate generated specifically for localhost testing, avoiding any need to touch the host operating system's system-wide trust store.
4. **Concepts:** Revisits **Trust Boundary** (EC-CON-017) and **Interface** (EC-CON-005). No new first homes.
5. **Mental Model:** Cryptographic channel and delegated identity verification. TLS constructs an encrypted pipe over TCP using negotiated ephemeral keys. Identity is verified by validating a digital certificate chain against pre-configured local trust anchors. A valid certificate proves cryptographic control of a domain name, not the business ethics or safety of the server application.
6. **Mechanism Sequence:**
   $$\text{ClientHello (Supported Ciphers, Key Share, SNI/ECH)} \xrightarrow{} \text{ServerHello (Chosen Cipher, Key Share)} \xrightarrow{} \text{Encrypted Extensions, Certificate, CertVerify, Finished}$$
   $$\text{Client validates Certificate Chain to Trust Anchor (RFC 9525)} \xrightarrow{} \text{Client Finished} \xrightarrow{} \text{Encrypted Application Data (AEAD)}$$
7. **Prediction-Before-Observation:** If a malicious actor creates a valid, cryptographically signed TLS certificate for their own domain (`evil.example`), can they use that certificate to impersonate `bank.example` without triggering a browser or TLS client warning?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe:* Run a local Python TLS server on `127.0.0.1` (port 0) using a course-provided test certificate and dedicated local CA. Connect using Python's `ssl` module configured with the dedicated CA context. Verify successful handshake and inspect negotiated protocol (`TLSv1.3`) and cipher suite.
   - *Break (Case 1: Hostname Mismatch):* Connect to the server using an incorrect server hostname (e.g., configuring verification for `mismatch.invalid`). Observe that the TLS handshake fails with a hostname verification error (`CertificateError` / `IP address mismatch` per RFC 9525).
   - *Break (Case 2: Untrusted Anchor):* Connect to the server using an empty or default CA context that does not contain the course test CA. Observe that the handshake fails with a certificate verification failure (`SSLCertVerificationError`).
   - *Strict Safety Rule:* The exercise strictly prohibits teaching verification bypasses (`curl -k`, `verify=False`, or disabling check_hostname).
   - *Explain:* Explain why a valid certificate proves only that the private key holder controls the domain name listed in `subjectAltName`, and why TLS does not authenticate application authorization or protect against application-level fraud.
   - *Judge:* Evaluate forward secrecy: explain why ephemeral Diffie-Hellman key exchange (`(EC)DHE`) ensures that future disclosure of a server's long-term private key cannot decrypt previously recorded network traffic, whereas static PSK-only modes (`psk_ke`) do not provide this guarantee.
9. **Required Commands / Tools:** Python 3 standard library (`ssl`, `socket`). OpenSSL CLI is optional and environment-sensitive; the core activity remains fully functional without an external `openssl` binary.
10. **Machine-Checkable Evidence:** Test harness runs three automated checks: (1) valid handshake succeeds and exchanges data, (2) hostname mismatch is rejected, and (3) untrusted CA is rejected. Asserts zero bypass flags.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner explains the difference between identity verification and business trustworthiness, correctly identifies what metadata is visible during a TLS exchange (IP endpoints, packet sizes, timing; SNI visible unless RFC 9849 ECH is negotiated), and articulates why forward secrecy depends on ephemeral key shares.
12. **Misconceptions Addressed:**
    - "HTTPS encryption proves the website is safe and not a scam." (TLS validates domain control, not business honesty or application security; phishing sites regularly use valid TLS certificates).
    - "TLS hides all metadata on the wire." (IP addresses, packet sizes, timing, and unencrypted SNI remain observable to network observers; RFC 9849 ECH protects SNI only when specifically deployed and supported).
    - "All TLS 1.3 handshakes are identical 1-RTT exchanges." (PSK resumption and 0-RTT early data use different message flows and carry replay attack risks).
13. **What You Can Ignore—for Now:** Elliptic curve point multiplication mathematics, ASN.1 DER binary decoding details, OCSP stapling protocol mechanics, Certificate Transparency Merkle tree proofs.
14. **Progressive Support:**
    - *Question:* Why does connecting to our local test server fail if we don't pass the custom CA certificate file to the client context?
    - *Hint 1:* Where does your computer store the list of certificate authorities it trusts?
    - *Hint 2:* Our test certificate was issued by a course-created CA, which is not part of the standard system trust store.
    - *Expected Observation:* The client throws an `SSLCertVerificationError` stating that the certificate issuer is unknown or untrusted.
    - *Full Explanation:* TLS authentication is anchor-based. A client validates a certificate by building a chain to a trusted root anchor in its local store. Since our course CA is private, the client must explicitly specify that anchor in its verification context.
15. **Visual Requirements:** Diagram showing: (a) TLS 1.3 handshake exchange with ephemeral key share generation, (b) Certificate chain verification from leaf through intermediate to local trust anchor, and (c) Encrypted payload boundary vs. visible network metadata (IP, size, timing, SNI/ECH).
16. **Exit Criteria:** Learner successfully executes the 3-state TLS verification suite, explains certificate path validation, and articulates why TLS identity does not imply application correctness.
17. **Competency Mapping:** Explain (Primary: TLS trust and encryption properties), Observe (Growth: certificate error inspection).
18. **Provenance / Source Anchors:** RFC 9846 (TLS 1.3, July 2026, obsoleting RFC 8446), RFC 9525 (Service Identity in TLS, November 2023, obsoleting RFC 6125), RFC 9849 (Encrypted Client Hello, March 2026), RFC 5280 (PKIX Certificate and CRL Profile).
19. **Failure / Inference Limits:** Localhost TLS fixtures verify cryptographic logic and certificate parsing without interacting with public CA infrastructure (Let's Encrypt), revocation checking (CRLs/OCSP), or public DNS TXT records.

---

### 5.3 Lesson L11-02: “What is HTTP, really?”

1. **Learner Question:** What actually happens when an HTTP request is made, what do methods like GET and POST really mean, and why is HTTP called a "uniform interface"?
2. **Before / After Capability:**
   - *Before:* Views HTTP as an arbitrary function call or URL string; assumes `200 OK` means the business operation succeeded; confuses HTTP methods with backend database operations.
   - *After:* Can break down an HTTP message into request/response lines, headers, and body; explain the uniform interface principles (RFC 9110); distinguish resource from representation; classify methods by safety and idempotency; and correctly interpret status code classes ($1\text{xx}$ to $5\text{xx}$).
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L10-02` (TCP byte streams).
   - Support: Understand CRLF line terminators (`\r\n`) and header parsing conventions. Use `curl -v` against localhost to expose raw protocol bytes.
4. **Concepts:** Revisits **Interface** (EC-CON-005) and **Failure** (EC-CON-010). No new first homes.
5. **Mental Model:** A standardized application interface over a reliable byte stream. URIs identify abstract conceptual resources; HTTP methods express standardized client intentions; HTTP headers convey message metadata; status codes report protocol outcomes; and the message body carries a concrete representation (e.g., JSON, HTML, binary) of the resource state.
6. **Mechanism Sequence:**
   $$\text{Client Request: Method + Target URI + HTTP/1.1} \xrightarrow{\text{CRLF}} \text{Headers (Host, Accept, Content-Type)} \xrightarrow{\text{CRLF CRLF}} \text{[Optional Body]}$$
   $$\text{Server Response: HTTP/1.1 + Status Code + Reason} \xrightarrow{\text{CRLF}} \text{Headers (Content-Type, Content-Length)} \xrightarrow{\text{CRLF CRLF}} \text{[Response Body]}$$
7. **Prediction-Before-Observation:** If a server returns an HTTP response with status code `200 OK` and a body containing `{"error": "insufficient_funds"}`, did the HTTP request succeed or fail according to the HTTP protocol specification?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe:* Start a minimal Python HTTP server on `127.0.0.1` (port 0). Issue a request using `curl -v http://127.0.0.1:<port>/items/1`. Inspect the verbatim output: `>` lines (outgoing request), `<` lines (incoming response), status line, headers, and payload.
   - *Build:* Construct a Python handler that implements `GET` (returns resource representation), `PUT` (idempotent replacement), and `POST` (non-idempotent submission).
   - *Break:* Send a malformed HTTP request missing the `Host` header (in HTTP/1.1) or with invalid CRLF formatting; observe that the server returns `400 Bad Request`.
   - *Explain:* Contrast Safe methods (`GET`, `HEAD`) with Idempotent methods (`PUT`, `DELETE`). Explain why "safe" means the client requests no state change (incidental server logging is allowed), while "idempotent" means repeated identical requests have the same intended effect as a single request.
   - *Judge:* Analyze why returning `200 OK` for application errors (e.g., in naive GraphQL or REST APIs) breaks standard intermediaries, caches, and monitoring systems, violating the uniform interface contract.
9. **Required Commands / Tools:** Python 3 standard library (`http.server`), `curl`.
10. **Machine-Checkable Evidence:** Test script sends structured requests via `curl` (or Python client if curl is preflighted absent), validates status codes ($200, 400, 404, 405$), and parses response header fields.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner explains the distinction between a resource and its representation, clearly defines safety vs. idempotency, and articulates why `200 OK` does not prove business-level correctness.
12. **Misconceptions Addressed:**
    - "A GET request can never cause any side effects on the server." (The RFC specifies that GET has safe semantics, but broken server implementations can mutate state; incidental logging and caching are not violations of safety).
    - "Idempotent means a request is always safe to retry automatically under any circumstances." (Idempotency defines intended effect; network failures during partial writes may still require application-level reconciliation before retrying).
    - "Status 200 proves the business operation succeeded." (`200 OK` means the HTTP server processed the request according to HTTP semantics; the representation body may still report domain-level business failures).
13. **What You Can Ignore—for Now:** WebDAV extended methods (`PROPFIND`, `LOCK`), HTTP/1.1 pipelining history, MIME multipart body boundary parsing internals.
14. **Progressive Support:**
    - *Question:* Why does `curl -v` print lines starting with `>` and `<`?
    - *Hint 1:* Look at the direction of communication between the client and the server.
    - *Hint 2:* Lines starting with `>` represent bytes sent by curl; lines starting with `<` represent bytes received from the server.
    - *Expected Observation:* The transcript shows the complete HTTP request sent over the TCP connection followed by the complete HTTP response received.
    - *Full Explanation:* `curl -v` provides a literal transcript of the application protocol exchange, allowing you to see the exact text lines and headers traversing the socket.
15. **Visual Requirements:** Diagram of the HTTP message format, highlighting: (1) Request line / Status line, (2) Header block separated by CRLF, (3) Empty line delimiter (`\r\n\r\n`), and (4) Message body.
16. **Exit Criteria:** Learner produces a verbatim `curl -v` trace, analyzes each header and status code, and writes a concise defense of method safety and idempotency.
17. **Competency Mapping:** Trace (Primary: HTTP message exchange), Explain (Growth: uniform interface and method semantics).
18. **Provenance / Source Anchors:** IETF STD 97 / RFC 9110 (HTTP Semantics, June 2022).
19. **Failure / Inference Limits:** Testing on localhost HTTP servers bypasses network middleboxes, carrier-grade NATs, and wide-area proxy rewrites; header parsing is observed on standard CPython `http.server`.

---

### 5.4 Lesson L11-03: “Why is my page slow to load?”

1. **Learner Question:** When a website takes seconds to load, why does subsequent loading feel instantaneous, what do proxies and CDNs actually do, and why did the internet need HTTP/2 and HTTP/3?
2. **Before / After Capability:**
   - *Before:* Believes browsers re-download everything on every click, assumes caching is just "saving files locally", or believes HTTP/3 is unconditionally faster than HTTP/1.1 in all situations.
   - *After:* Can explain HTTP caching mechanics (freshness vs. validation per RFC 9111), trace conditional requests with ETags and `304 Not Modified`, explain the role of intermediaries (reverse proxies, CDNs) in optimizing network locality, and evaluate the architectural trade-offs between HTTP/1.1, HTTP/2, and HTTP/3/QUIC.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisites: `L11-02` (HTTP Semantics) and `L10-02` (TCP byte streams).
   - Support: Review concept **Caching** (EC-CON-011) and **Locality** (EC-CON-012) from M04.
4. **Concepts:** Revisits **Caching** (EC-CON-011), **Locality** (EC-CON-012), and **Interface** (EC-CON-005). No new first homes.
5. **Mental Model:** Hierarchical caching and transport multiplexing. Caching avoids redundant network round trips by reusing fresh representations or validating stale ones using lightweight conditional headers (`If-None-Match`). Intermediaries position caches close to users (network locality). Protocol evolution resolves head-of-line blocking: HTTP/2 multiplexes streams over one TCP connection; HTTP/3/QUIC runs independent streams over UDP.
6. **Mechanism Sequence:**
   $$\text{Initial GET} \xrightarrow{} \text{200 OK with ETag: \"xyz\" and Cache-Control: max-age=60}$$
   $$\text{Subsequent Request (Fresh)} \xrightarrow{} \text{Cache Hit (Zero Network Round Trips)}$$
   $$\text{Subsequent Request (Stale)} \xrightarrow{\text{GET with If-None-Match: \"xyz\"}} \text{Server Validates} \xrightarrow{} \text{304 Not Modified (No Response Body)}$$
   $$\text{Transport Evolution: H1 (Serial/HOLB) } \longrightarrow \text{ H2 (Stream Multiplexing over TCP) } \longrightarrow \text{ H3 (QUIC/UDP Independent Streams)}$$
7. **Prediction-Before-Observation:** When a server responds with `304 Not Modified` to a conditional request, will the network transfer include the original HTML/image file payload?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe:* Start a local Python server serving a static resource with `ETag: "v1.0"` and `Cache-Control: max-age=1`. Use `curl -v` to fetch the resource; note headers. Then issue a conditional request: `curl -v -H 'If-None-Match: "v1.0"' http://127.0.0.1:<port>/resource`. Observe response status `304 Not Modified` and verify that the response body is completely empty.
   - *Build:* Construct a simple caching proxy adapter that intercepts client requests, stores the response along with its ETag, and serves subsequent requests conditionally.
   - *Break:* Mutate the server resource content (updating the ETag to `"v1.1"`); issue the same conditional request with `If-None-Match: "v1.0"`. Observe that validation fails and the server returns `200 OK` with the new representation body.
   - *Explain:* Explain why a strong ETag is an opaque entity validator, not inherently a cryptographic hash (it can be an internal version number or timestamp, as long as it satisfies RFC 9111 comparison rules).
   - *Judge:* Evaluate HTTP/2 vs. HTTP/3: explain why HTTP/2 suffers from transport-layer head-of-line blocking on lossy wireless networks (because all streams share a single TCP sequence space), and analyze why HTTP/3 does not guarantee universal speedup on stable, low-latency, high-bandwidth wired networks.
9. **Required Commands / Tools:** Python 3 standard library (`http.server`), `curl`.
10. **Machine-Checkable Evidence:** Test script issues an initial request, records ETag, issues conditional request with `If-None-Match`, and asserts: (1) status is `304 Not Modified`, (2) response body length is 0 bytes, and (3) cached metadata is preserved.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner's explanation distinguishes cache freshness (`max-age`) from cache validation (`ETag` / `304`), explains why `304` carries no message content, and compares H1, H2, and H3 mechanisms without claiming a universal performance winner.
12. **Misconceptions Addressed:**
    - "A strong ETag must be an MD5 or SHA-256 hash of the file content." (ETags are opaque strings defined by the origin; any format satisfying uniqueness/comparison requirements is valid).
    - "Status 304 responses must include Content-Length: 0." (A 304 response transfers no body, but RFC 9111 permits it to send the `Content-Length` of the representation that would have been sent in a 200 response).
    - "HTTP/3 is always faster than HTTP/2." (HTTP/3 eliminates transport head-of-line blocking on lossy connections, but has higher CPU encryption/UDP handling overhead and may perform identically to HTTP/2 on reliable low-latency networks).
13. **What You Can Ignore—for Now:** HPACK/QPACK Huffman static table encoding algorithms, QUIC connection ID routing and load balancer tokens, CDN Anycast BGP route flap management.
14. **Progressive Support:**
    - *Question:* Why does a `304 Not Modified` response save network bandwidth if the client still has to send an HTTP request to the server?
    - *Hint 1:* Look at what is in the response body of a 304 compared to a 200.
    - *Hint 2:* The round trip checks validation, but the heavy payload (e.g., a 5 MB image or script) is not retransmitted.
    - *Expected Observation:* The 304 response contains only headers and zero payload bytes, completing much faster and using minimal network transfer.
    - *Full Explanation:* Conditional requests trade a small header exchange for the transmission of large payload bodies. If the representation has not changed, the server sends 304 with no content, and the client reuses its stored representation.
15. **Visual Requirements:** Diagram contrasting: (1) Fresh cache hit (zero network round trips), (2) Stale cache conditional validation with ETag $\rightarrow$ 304 Not Modified, and (3) Head-of-line blocking comparison between HTTP/1.1 (serial connection wait), HTTP/2 (TCP stream block on drop), and HTTP/3 (independent QUIC streams).
16. **Exit Criteria:** Learner executes a conditional HTTP cache validation trace, proves zero body transfer on 304, and explains the architectural trade-offs across H1, H2, and H3.
17. **Competency Mapping:** Observe (Primary: cache trace and header inspection), Diagnose (Growth: cache invalidation bugs), Judge (Growth: protocol version selection), Estimate (Growth: bandwidth savings).
18. **Provenance / Source Anchors:** IETF STD 98 / RFC 9111 (HTTP Caching), RFC 9112 (HTTP/1.1), RFC 9113 (HTTP/2), RFC 9114 (HTTP/3), RFC 9000 (QUIC).
19. **Failure / Inference Limits:** Localhost measurements do not capture wide-area network latency (RTT), packet loss rate variations, or CDN geographical edge distance; performance benefits are evaluated conceptually and structurally rather than via physical internet benchmarks.

---

## 6. Required Lab LAB-REQ-01 Design — HTTP Interface, Origin & Intermediary Trace

### 6.1 Lab Overview & Normative Alignment
- **Identity:** `LAB-REQ-01` — HTTP Interface, Origin & Intermediary Trace
- **Module Home:** M11 (Networking II: TLS, HTTP, CDN & Proxies)
- **Primary Competency:** Trace
- **Growth Competencies:** Observe, Diagnose, Judge
- **Normative Foundation:**
  - IETF STD 97 / RFC 9110 (*HTTP Semantics*, June 2022)
  - IETF STD 98 / RFC 9111 (*HTTP Caching*, June 2022)
- **Pedagogical Purpose:** Demystify how web traffic traverses the internet by implementing and tracing an end-to-end HTTP communication path involving a client, a forwarding intermediary (proxy/gateway), and an origin server on `127.0.0.1`. The learner directly observes header transformations, hop-by-hop vs. end-to-end headers, the `Via` protocol tracking contract, conditional cache validation yielding `304 Not Modified` with zero body transfer, and controlled upstream failure mapping.

---

### 6.2 Pedagogical Contract & Scope Boundary

1. **Original Essential CS Implementation:** All server and intermediary code components are 100% original Essential CS Python scripts (licensed Apache-2.0). No third-party proxy packages (`nginx`, `squid`, `traefik`, `mitmproxy`) or RFC code snippets are bundled.
2. **Localhost & Privilege Boundary:** All listeners bind strictly to `127.0.0.1`. The lab requires zero elevated privileges (no `sudo`, no `root`, no raw socket capabilities). It touches zero public endpoints and does not touch system trust stores.
3. **No Brittle Assumptions:** Tests and evidence rubrics must not assume fixed port numbers, fixed process IDs (PIDs), hardcoded header ordering, or fixed round-trip execution timings.
4. **Tool Contract:** The lab requires `curl` for client interactions to expose verbatim protocol framing. If `curl` is preflighted as absent, the lab provides an explicit environment block with an approved fallback strategy, but does not silently substitute a Python `urllib` script while claiming curl evidence.

---

### 6.3 Technical Architecture & Component Specifications

The lab consists of three bounded components executing on loopback:

```
+-------------------------------------------------------------------------------+
|                                   LOCALHOST (127.0.0.1)                       |
|                                                                               |
|  [ Client (curl) ]                                                            |
|          |                                                                    |
|          | Direct Trace: curl -v http://127.0.0.1:<origin_port>/resource      |
|          +--------------------------------------------+                       |
|          |                                            |                       |
|          | Forwarded Trace                            v                       |
|          | curl -v http://127.0.0.1:<proxy_port>/...  [ OriginServer ]        |
|          v                                            * Binds port 0          |
|  [ IntermediaryAdapter ]                              * Serves representations|
|  * Binds port 0                                       * Computes strong ETag  |
|  * Injects "Via: 1.1 essential-cs-proxy"              * Validates conditional |
|  * Forwards upstream to OriginServer                  | requests (If-None-    |
|  * Maps socket refusal -> 502 Bad Gateway             | Match -> 304)         |
|          |                                            ^                       |
|          +--------------------------------------------+                       |
|                     Forwarded upstream connection                             |
+-------------------------------------------------------------------------------+
```

#### Component 1: `OriginServer` (`labs/lab_req_01/origin_server.py`)
- **Network Interface:** Binds to `127.0.0.1` on port `0` (dynamic OS allocation). Upon successful bind, immediately prints an unbuffered readiness line to stdout: `ORIGIN_READY_PORT=<port>`.
- **Endpoints:**
  - `GET /resource`: Returns `200 OK`, `Content-Type: application/json`, `ETag: "v1-canonical"`, `Cache-Control: max-age=60`, and body `{"service": "origin", "data": "payload-v1"}`.
  - `GET /resource` with `If-None-Match: "v1-canonical"`: Validates conditional request per RFC 9111. Returns `304 Not Modified` with **zero message body/content**.
  - `GET /resource` with mismatched ETag: Returns `200 OK` with the full representation body.
  - `GET /health`: Returns `200 OK`, body `OK`.
- **Termination:** Handles `SIGTERM` and `SIGINT` cleanly, closing listeners and active connections within 1.0 second.

#### Component 2: `IntermediaryAdapter` (`labs/lab_req_01/intermediary_adapter.py`)
- **Network Interface:** Binds to `127.0.0.1` on port `0`. Takes the origin port as a command-line argument (`--origin-port=<port>`). Prints readiness line: `PROXY_READY_PORT=<port>`.
- **Forwarding Protocol Mechanics:**
  - Receives incoming HTTP client request.
  - Forwards the request line and end-to-end headers to `OriginServer`.
  - Removes hop-by-hop headers (`Connection`, `Keep-Alive`, `Transfer-Encoding`).
  - Appends intermediary tracking header: `Via: 1.1 essential-cs-proxy` per RFC 9110 §7.6.3.
  - Receives response from `OriginServer` and streams response line, headers, and body back to client.
- **Controlled Upstream Failure Mapping:**
  - If the connection to `OriginServer` fails due to an active refusal (`ECONNREFUSED` / `ConnectionRefusedError`), the intermediary catches the error and returns:
    `HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/plain\r\nVia: 1.1 essential-cs-proxy\r\n\r\nUpstream origin connection refused.\n`
  - *Optional Distinct Deadline Fixture:* If an upstream read deadline expires, the intermediary returns `504 Gateway Timeout`.
  - *Pedagogical Boundary:* The lesson explicitly instructs learners that this mapping is a **course fixture policy** chosen to illustrate gateway error semantics, not an immutable law of physics.

---

### 6.4 Preflight, Toolchain & Truthful Fallback Strategy

1. **Preflight Step:** Before starting the lab, the harness runs `preflight_lab_req_01.py`:
   - Checks Python standard library (`socket`, `http.server`, `subprocess`).
   - Checks `curl` binary availability: executes `curl --version`.
   - Records the exact curl version and TLS backend string (e.g., `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13`).
2. **Truthful Fallback Strategy:**
   - If `curl` is missing, the lab harness issues an explicit warning: `TOOL MISSING: curl is required for the interactive trace of LAB-REQ-01`.
   - The learner may install `curl` using standard package managers (`apt install curl`, `winget install curl`, `brew install curl`).
   - If in a restricted environment where `curl` cannot be installed, the learner runs an approved, standalone Python trace client (`python -m labs.lab_req_01.raw_http_client`) that transmits raw HTTP text over raw sockets and prints formatted `>` and `<` traces identical to curl. The transcript must be explicitly labeled `EVIDENCE GENERATED VIA STANDALONE RAW SOCKET CLIENT (CURL FALLBACK)`.

---

### 6.5 Process Lifecycle, Deterministic Port Allocation & Cleanup

To prevent orphan processes, hung background listeners, or port collisions:

1. **Startup Readiness Protocol:**
   - Harness launches `OriginServer` via `subprocess.Popen`.
   - Harness reads stdout pipe line-by-line with a 5.0-second timeout until it matches `ORIGIN_READY_PORT=(\d+)`. It extracts `<origin_port>`.
   - Harness launches `IntermediaryAdapter` passing `--origin-port=<origin_port>`.
   - Harness reads stdout pipe until matching `PROXY_READY_PORT=(\d+)` to extract `<proxy_port>`.
   - A quick TCP connect check verifies both endpoints accept connections before any tests run.
2. **Deterministic Teardown & Listener Check:**
   - At lab conclusion (or upon any failure/exception), the teardown fixture executes:
     1. Sends `SIGTERM` to `IntermediaryAdapter` PID; waits up to 2.0s with `proc.wait()`.
     2. Sends `SIGTERM` to `OriginServer` PID; waits up to 2.0s with `proc.wait()`.
     3. If either process fails to exit within 2.0s, sends `SIGKILL`.
     4. Executes a post-reset listener check: attempts a non-blocking TCP connect to both assigned ports on `127.0.0.1`. Asserts that both ports immediately yield `ConnectionRefusedError`, proving no background processes or sockets were leaked.

---

### 6.6 Step-by-Step Lab Execution & Failure Injection

The lab proceeds through four sequential investigative steps:

- **Step 1: Direct Origin Trace**
  - Execute: `curl -v http://127.0.0.1:<origin_port>/resource`
  - Learner observes direct connection to origin, `200 OK`, `ETag: "v1-canonical"`, and JSON payload. Note that no `Via` header is present.
- **Step 2: Forwarded Intermediary Trace**
  - Execute: `curl -v http://127.0.0.1:<proxy_port>/resource`
  - Learner observes connection to intermediary, forwarded response from origin, and presence of `Via: 1.1 essential-cs-proxy`.
  - Compare headers between Step 1 and Step 2 in an inspection table (identifying hop-by-hop vs. end-to-end fields).
- **Step 3: Conditional Validation Trace (304 Not Modified)**
  - Execute: `curl -v -H 'If-None-Match: "v1-canonical"' http://127.0.0.1:<proxy_port>/resource`
  - Learner observes status line `HTTP/1.1 304 Not Modified`.
  - Learner verifies that the response carries **zero payload bytes** (response body is empty).
  - Learner notes that headers may still report metadata (e.g., representation `Content-Length`), confirming that RFC 9111 does not require `Content-Length: 0`.
- **Step 4: Controlled Origin Failure Injection**
  - Learner (or harness) terminates `OriginServer` (`kill -TERM <origin_pid>`).
  - Execute: `curl -v http://127.0.0.1:<proxy_port>/resource`
  - Intermediary fails to connect to origin and returns `HTTP/1.1 502 Bad Gateway`.
  - Learner verifies status `502` and presence of intermediary `Via` header, confirming the error was generated by the gateway rather than the origin.

---

### 6.7 Evidence Rubric: Machine-Checkable vs. Reviewer-Required

| Assessment Dimension | Machine-Checkable Invariant | Reviewer-Required Pedagogical Invariant |
|---|---|---|
| **Step 1: Direct Trace** | HTTP status == 200; `ETag` header present; `Via` header absent. | Verifies learner correctly identifies request line, header block, and CRLF separation. |
| **Step 2: Forwarded Trace** | HTTP status == 200; `Via` header present and contains `essential-cs-proxy`. | Verifies header comparison table correctly separates hop-by-hop from end-to-end headers. |
| **Step 3: Conditional 304** | HTTP status == 304; response body length == 0 bytes. | Verifies learner explains bandwidth savings without falsely claiming `Content-Length: 0` is required. |
| **Step 4: Failure Injection** | HTTP status == 502; response generated by intermediary while origin is offline. | Verifies learner explains why `502 Bad Gateway` originates from the intermediary, not the origin. |
| **Lifecycle & Teardown** | Post-reset port check proves both ports actively refuse connections (zero socket leaks). | Verifies learner followed unprivileged localhost safety rules and recorded tool versions. |

---

## 7. Optional Lab LAB-OPT-02 Design Disposition — Stanford CS144 Checkpoint 2 (The TCP Receiver)

### 7.1 Lab Role & Scope
- **Identity:** `LAB-OPT-02` — Stanford CS144 Checkpoint 2: *The TCP Receiver*
- **Module Home:** M10 / M11 Optional Extension
- **Selected Assignment offering:** Stanford CS144 *Introduction to Computer Networking*, Fall 2025 (`https://cs144.github.io/assignments/check2.pdf`)
- **Technical Scope:** Implementation in modern C++ of:
  - 32-bit sequence number wrapping and unwrapping (`Wrap32` class) to handle sequence number rollover in a 4 GB space.
  - `TCPReceiver` class: receives incoming TCP segments, reassembles bytes into a contiguous `ByteStream`, computes the cumulative acknowledgment number (`ackno`), and computes advertised receive window capacity (`window_size`).
- **Pedagogical Value:** Exceptional hands-on exploration of transport-layer state machine invariants: handling out-of-order segments, duplicate bytes, overlapping segments, and sequence wrapping without relying on high-level language abstractions.

---

### 7.2 Rights & Redistribution Disposition

1. **Rights Finding:** At Research and Design time (September 2026), the assignment PDF and syllabus for Stanford CS144 Fall 2025 were publicly accessible on the web. However, the course materials do **not** carry an open, permissive license authorizing Essential CS to vendor, redistribute, or adapt the assignment text, starter code, or test harnesses.
2. **License Status:** Reuse rights are classified as **UNESTABLISHED**.
3. **Mandatory Repository Policy:**
   - **MUST REMAIN STRICTLY OPTIONAL AND LINK-ONLY.**
   - Essential CS **will not bundle, vendor, fork, or mirror** the Minnow starter repository, assignment PDF text, or grading scripts into this repository.
   - Third-party GitHub mirrors or unofficial forks are strictly rejected as provenance authorities.
   - **DO NOT PROMOTE TO REQUIRED.** Promoting LAB-OPT-02 to a Required Lab would introduce an unverified external dependency and violate curriculum invariant 15 (Vendor-neutral and open-first) and invariant 20 (Self-contained teachable course).

---

### 7.3 Pedagogical Guidance & Learner Support Strategy

For learners electing to pursue LAB-OPT-02 independently:

1. **Self-Contained Conceptual Guide:** Essential CS provides an original, self-contained conceptual bridge document (`labs/lab_opt_02/README.md`) written entirely by Essential CS authors (CC BY-SA 4.0).
2. **External Link Routing:** Directs learners to obtain official assignment specifications directly from the canonical Stanford CS144 course portal.
3. **Cognitive Load Warning:** The guide explicitly warns learners that LAB-OPT-02 involves significant cognitive and environment setup overhead (modern C++20 toolchain, CMake, Linux build environment) and is not required to complete the Core computing-system world model or proceed to M11/M12.

---

## 8. Module M12 Design — Web & Browser: The Integrated Case

### 8.1 Module-Level Specification
- **Title:** M12 — Web & Browser: The Integrated Case (Area 08)
- **Primary Competency:** Observe
- **Growth Competencies:** Trace, Explain, Diagnose, Judge
- **Module Prerequisites:** Hard: M11 (Networking II: TLS, HTTP, CDN & Proxies)
- **Capability Transition:** Learners transition from viewing the browser as a simple document reader to understanding it as an integrated computing system for safely executing untrusted code. They separate Web Platform specifications from named browser implementations (Chromium case), trace a conceptual rendering pipeline, explain origin-based security boundaries (SOP, CORS, CSP), and observe how the Window/Document event loop schedules tasks, microtasks, and rendering opportunities without canonically defining Concurrency.

---

### 8.2 Lesson L12-01: “What is a browser, architecturally?”

1. **Learner Question:** What actually runs on my computer when I launch a browser, and why does a single browser window spawn dozens of operating system processes?
2. **Before / After Capability:**
   - *Before:* Assumes a browser is a monolithic single process, or believes the simplified myth that "every browser tab equals exactly one OS process".
   - *After:* Can explain modern browser multi-process architecture using Chromium as a concrete case study; distinguish the browser coordinator process, sandboxed renderers, GPU services, and network/utility services; articulate how Site Isolation groups browsing contexts by site; and separate Web Platform requirements from implementation-specific process topology.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Hard prerequisites: `M06` (Process isolation, OS boundaries) and `M07` (Virtual memory, address space isolation).
   - Support: Review concept **Process** (EC-CON-018) and **Isolation** (EC-CON-013).
4. **Concepts:** Revisits **Process** (EC-CON-018) and **Isolation** (EC-CON-013). No new first homes.
5. **Mental Model:** A multi-process sandboxed operating environment for untrusted web content. The browser coordinator process holds operating-system privileges and coordinates UI, navigation, and persistent storage. Untrusted web scripts run inside restricted, sandboxed renderer processes. Site Isolation enforces OS-level memory boundaries between cross-site documents as defense in depth against UXSS and Spectre-class attacks.
6. **Mechanism Sequence:**
   $$\text{User Enters URL} \xrightarrow{} \text{Browser Coordinator Process (Network Service)} \xrightarrow{\text{Determine Site & Origin}} \text{SiteInstance Selection}$$
   $$\text{Assign / Reuse Sandboxed Renderer Process} \xrightarrow{\text{Spawn / IPC Channel}} \text{Renderer Parses & Renders} \xrightarrow{\text{Shared Memory / GPU IPC}} \text{GPU Process Composites Pixels}$$
7. **Prediction-Before-Observation:** If you open three tabs pointing to `a.example.com`, `b.example.com`, and a blank `about:blank` tab, will the operating system process table always show exactly three renderer processes?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe (Live Browser or Reference):* Open a supported desktop browser (Chromium/Chrome or Firefox). Open the internal process task manager (`Shift+Esc` in Chrome) and system process table (`ps aux` / Task Manager). Record the running processes: Browser process, GPU Process, Network Service, and Tab/Frame Renderers. Note that the process count does not equal the tab count.
   - *Break:* Open multiple subframes across different domains (e.g., embedding an iframe from a different site). Observe whether an Out-Of-Process Iframe (OOPIF) spawns a distinct renderer process (subject to the platform's Site Isolation mode).
   - *Explain:* Contrast Web Platform specifications (which define browsing contexts, origins, and document objects) with Chromium implementation choices (which map browsing contexts to `SiteInstance` and OS processes).
   - *Judge:* Evaluate process isolation trade-offs: what are the security gains of isolating cross-site iframes into separate OS processes vs. the memory overhead on mobile devices with limited RAM?
9. **Required Commands / Tools:** Real desktop browser (Chromium/Chrome preferred; Firefox optional) with DevTools / Task Manager. If no GUI/browser environment is available, record `NO LIVE BROWSER OBSERVATION` and inspect course reference process traces.
10. **Machine-Checkable Evidence:** EXP-03 source inspection answers verifying exact Chromium source locations (`docs/process_model_and_site_isolation.md`, `site_instance_impl.cc`, `child_process_security_policy_impl.cc`).
11. **Reviewer-Required Evidence:** Reviewer checks that the learner explains why "one tab = one process" is false, distinguishes Web Platform specs from Chromium implementation, and explains the defense-in-depth role of OS-level process sandboxing.
12. **Misconceptions Addressed:**
    - "One browser tab equals one operating system process." (Chromium assigns processes based on SiteInstance, browsing context groups, memory limits, and platform-specific isolation policies; tabs sharing a site or subframes from different sites may share or split processes).
    - "Site Isolation is a synonym for the Same-Origin Policy." (SOP is a Web Platform logical access-control policy; Site Isolation is an OS process-level memory boundary implementation designed to mitigate hardware speculative execution attacks and renderer compromises).
    - "All browsers share the same internal process architecture." (Process topologies differ significantly between Chromium, Firefox Gecko, and WebKit Safari, and evolve across versions).
13. **What You Can Ignore—for Now:** Chromium Mojo IPC binary message serialization protocols, Mach port / Windows token sandbox capability internals, GPU driver GL context management.
14. **Progressive Support:**
    - *Question:* Why does opening Chrome's Task Manager reveal processes named "GPU Process" and "Network Service" even if you only have one tab open?
    - *Hint 1:* Look at the principle of least privilege and fault isolation from M06.
    - *Hint 2:* If the graphics driver crashes or a network connection hangs, should that bring down the entire browser UI?
    - *Expected Observation:* The browser decomposes functionalities into specialized helper processes rather than running everything inside the UI process.
    - *Full Explanation:* Chromium utilizes a modular service architecture. Isolating GPU operations and networking into dedicated processes prevents device driver instability from crashing the browser and restricts network permissions.
15. **Visual Requirements:** Architectural diagram contrasting: (a) Web Platform specification entities (Browsing Contexts, Windows, Iframes, Origins) with (b) Chromium implementation entities (Browser Process, Network Service, Sandboxed Renderer Processes, GPU Process, SiteInstances).
16. **Exit Criteria:** Learner identifies the primary processes in a live or reference browser trace and explains how Site Isolation isolates untrusted web content.
17. **Competency Mapping:** Explain (Primary: multi-process architecture and isolation boundaries), Observe (Growth: browser process inspection).
18. **Provenance / Source Anchors:** Chromium Project: *Process Model and Site Isolation* (`docs/process_model_and_site_isolation.md`), Reis and Gribble: *Isolating Web Programs in Modern Browser Architectures* (ACM EuroSys 2009).
19. **Failure / Inference Limits:** Process count and memory footprint vary dynamically based on OS RAM pressure, hardware acceleration availability, and browser build flags; observed process structures reflect current Chromium desktop practice, not a standardized Web specification.

---

### 8.3 Lesson L12-02: “How does a page render?”

1. **Learner Question:** When HTML, CSS, and JavaScript arrive over the network, how does the browser turn raw text into interactive, smooth visual pixels on my screen?
2. **Before / After Capability:**
   - *Before:* Thinks the browser immediately displays HTML tags as it downloads them, or views the rendering engine as an instantaneous black box; does not understand why scripts can freeze visual rendering.
   - *After:* Can trace the conceptual document rendering pipeline: HTML parse $\rightarrow$ DOM, CSS parse $\rightarrow$ CSSOM, Style resolution $\rightarrow$ Render Tree, Layout (Reflow) $\rightarrow$ Geometry, Paint $\rightarrow$ Display Lists, and Compositing $\rightarrow$ Screen Pixels; and explain the render-blocking implications of synchronous scripts vs. `async` and `defer`.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L11-02` (HTTP representations) and `L12-01` (Renderer processes).
   - Support: Minimal HTML/CSS/JS fixture served on loopback port 0.
4. **Concepts:** Revisits **Representation** (EC-CON-003) and **Interface** (EC-CON-005). No new first homes.
5. **Mental Model:** A multi-stage transformation pipeline from structured document text to GPU pixel tiles. Each stage produces intermediate structural data. Real browser rendering engines (Blink, Gecko, WebKit) optimize this conceptual pipeline by caching results, skipping un-invalidated stages, performing incremental updates, and offloading layer compositing to GPU threads.
6. **Mechanism Sequence:**
   $$\text{HTML Bytes} \xrightarrow{\text{Tokenizer/Parser}} \text{DOM Tree}$$
   $$\text{CSS Bytes} \xrightarrow{\text{CSS Parser}} \text{CSSOM Tree}$$
   $$\text{DOM + CSSOM} \xrightarrow{\text{Selector Matching}} \text{Render/Layout Tree (Computed Styles)}$$
   $$\text{Render Tree} \xrightarrow{\text{Layout (Reflow)}} \text{Geometry Coordinates (X, Y, Width, Height)}$$
   $$\text{Geometry} \xrightarrow{\text{Paint}} \text{Display Lists (Draw Commands)}$$
   $$\text{Display Lists} \xrightarrow{\text{Compositing (Compositor Thread)}} \text{Tiles / GPU Textures} \xrightarrow{} \text{Screen Framebuffer}$$
7. **Prediction-Before-Observation:** If an external `<script src="...">` tag without `async` or `defer` is placed in the middle of the `<head>` tag, what does the HTML parser do while the script is fetching over the network?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe (Live or Reference):* Serve a minimal course HTML fixture containing an external stylesheet, an image, and a synchronous script. Open DevTools **Network** and **Performance** panels. Record the phases actually displayed (note that on localhost, DNS/connect/TLS phases may be zero or folded).
   - *Break:* Insert a heavy synchronous script in `<head>` that blocks execution for 500 ms. Observe in the Performance timeline that the First Contentful Paint (FCP) is delayed until the script completes, because synchronous scripts block HTML parsing.
   - *Fix:* Modify the script tag to include `defer`. Re-run the Performance trace and observe that HTML parsing completes and initial DOM construction finishes before the deferred script executes.
   - *Explain:* Explain why classic `<script defer>` and `<script type="module">` avoid parser blocking, and contrast their execution timing with `<script async>`.
   - *Judge:* Evaluate the architectural separation between the Renderer Main Thread (which handles DOM, style, layout, and JavaScript) and the Compositor Thread: explain why smooth scrolling and CSS transforms can continue even when the main thread is busy.
9. **Required Commands / Tools:** Real browser with DevTools (Network & Performance panels), local Python HTTP server. If GUI browser is unavailable, mark `NO LIVE BROWSER OBSERVATION` and provide course reference waterfall traces.
10. **Machine-Checkable Evidence:** Automated test serving the HTML fixture asserts that the server receives requests in expected structural order and confirms HTTP response headers.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner traces the 6 pipeline stages, explains why synchronous scripts block parsing, and notes that modern engines incrementally update and composite rather than recalculating the entire tree on every tiny change.
12. **Misconceptions Addressed:**
    - "The browser redraws the entire page from scratch on every single mouse move or style update." (Engines invalidate and recompute only affected subtrees and composite cached layer tiles on the GPU).
    - "DOM and CSSOM are merged directly into pixels in one step." (Style resolution produces a render tree, which must go through layout/geometry and painting before compositing).
    - "All network waterfalls display DNS, TLS, and connect rows." (On localhost or persistent reused connections, those phases are absent or zero; test rubrics must not require them).
13. **What You Can Ignore—for Now:** HarfBuzz font shaping internals, Skia graphics library draw call opcodes, Subpixel anti-aliasing algorithms.
14. **Progressive Support:**
    - *Question:* Why does placing a slow script tag in `<head>` make the entire page stay blank?
    - *Hint 1:* What might a JavaScript script do to the HTML document while it is loading?
    - *Hint 2:* JavaScript can call `document.write()` or inspect elements, so the parser must pause until the script runs.
    - *Expected Observation:* The browser pauses HTML parsing, delaying DOM construction and layout until the external script finishes downloading and executing.
    - *Full Explanation:* By default, scripts are parser-blocking. The parser cannot know in advance whether the script will modify the DOM tree, so it must halt parsing until execution concludes. Using `defer` or `async` signals that parsing can continue safely.
15. **Visual Requirements:** Diagram of the conceptual rendering pipeline: HTML $\rightarrow$ DOM, CSS $\rightarrow$ CSSOM, Style Resolution $\rightarrow$ Layout/Reflow $\rightarrow$ Paint $\rightarrow$ Compositing $\rightarrow$ Screen Pixels, with callouts indicating where synchronous scripts block parsing.
16. **Exit Criteria:** Learner traces the stages of the rendering pipeline and demonstrates parser-blocking mitigation using `defer`.
17. **Competency Mapping:** Observe (Primary: DevTools Performance panel timeline), Trace (Growth: script execution and render pipeline stages).
18. **Provenance / Source Anchors:** WHATWG HTML Living Standard (*Parsing HTML documents*, *Scripting*), W3C Navigation Timing Level 2 (Working Draft, Feb 2026).
19. **Failure / Inference Limits:** DevTools Performance panel row names, recording metrics, and timeline layouts vary across browser versions and platforms; observations verify structural pipeline phases, not identical milliseconds or row labels.

---

### 8.4 Lesson L12-03: “Why is the browser secure?”

1. **Learner Question:** How can my browser safely load and run untrusted code from completely unknown websites without letting them steal my emails or bank session tokens?
2. **Before / After Capability:**
   - *Before:* Thinks websites are completely isolated like VMs, or conversely believes cross-origin requests are completely impossible; confuses CORS with server-side authentication; assumes CSP prevents all XSS attacks.
   - *After:* Can explain the Web Platform security model; define tuple vs. opaque origins; articulate Same-Origin Policy (SOP) boundaries across DOM, cookies, and network access; explain Fetch CORS preflight and safelisting mechanics as user-agent enforcement; and evaluate Content Security Policy (CSP) as defense in depth.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisites: `L11-02` (HTTP headers & methods) and `L12-01` (Browser process boundaries).
   - Support: Start two distinct local HTTP servers on OS-assigned ports on `127.0.0.1` (e.g., Origin A: `http://127.0.0.1:<portA>` and Origin B: `http://127.0.0.1:<portB>`).
4. **Concepts:** Revisits **Trust Boundary** (EC-CON-017) and **Isolation** (EC-CON-013). No new first homes.
5. **Mental Model:** Origin-based compartmentalization with controlled, user-agent enforced relaxation. An origin is the fundamental trust boundary of the Web Platform. Browsers prevent scripts from one origin from reading data from another origin (SOP). CORS allows a target origin to explicitly grant response read access to client scripts via HTTP headers. Non-browser clients are not subject to CORS filtering, proving that CORS is user-agent enforcement, not server-side authorization.
6. **Mechanism Sequence:**
   $$\text{Page at Origin A runs: fetch('http://127.0.0.1:<portB>/api')}$$
   $$\text{Browser sends HTTP Request (with Origin: http://127.0.0.1:<portA>)}$$
   $$\text{Server B Responds: Status 200 OK}$$
   $$\text{Browser checks Access-Control-Allow-Origin:}$$
   $$\text{  - If Missing / Mismatch } \longrightarrow \text{ Browser blocks JS access; logs CORS error in Console}$$
   $$\text{  - If Matches Origin A } \longrightarrow \text{ Browser passes response payload to JS Promise}$$
7. **Prediction-Before-Observation:** If Origin B does not return any CORS headers, did the HTTP request actually arrive at Origin B's server, or was it blocked by the browser before leaving your computer?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe (Case 1: CORS Error in Browser):* Open a page hosted on Origin A (`127.0.0.1:<portA>`). Script issues `fetch('http://127.0.0.1:<portB>/data')`. Origin B returns standard `200 OK` without CORS headers. Observe in the browser console that the request completed at the network level, but the browser blocked JavaScript from reading the response.
   - *Observe (Case 2: The Non-Browser Contrast):* Execute the exact same request using `curl -v http://127.0.0.1:<portB>/data`. Observe that `curl` receives and prints the response body with zero restrictions.
   - *Observe (Case 3: Authorized CORS):* Configure Origin B to include `Access-Control-Allow-Origin: http://127.0.0.1:<portA>`. Re-run the browser fetch; observe that JavaScript successfully resolves the Promise and accesses the data.
   - *Explain:* Explain why CORS does **not** protect backend databases from unauthorized writes sent by non-browser clients (`curl`, scripts), and why server APIs must authenticate requests independently.
   - *Judge:* Evaluate Content Security Policy (CSP Level 3): explain why adding `Content-Security-Policy: default-src 'self'` provides defense in depth by restricting where scripts can execute from and where data can be exfiltrated.
9. **Required Commands / Tools:** Real browser with developer console, `curl`, Python 3 standard library (`http.server`). If a real browser user-agent context is unavailable, record `NO LIVE BROWSER CORS OBSERVATION` and evaluate reference transcripts; do not add an undeclared Playwright/Node dependency.
10. **Machine-Checkable Evidence:** Test script asserts that Origin B returns expected data over raw HTTP, while browser-context test (when browser capability is present) records the CORS block exception.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner explains the difference between browser SOP enforcement and server-side authorization, clearly identifies what an origin tuple consists of, and articulates why CSP is defense-in-depth rather than an absolute XSS proof.
12. **Misconceptions Addressed:**
    - "CORS is a security feature that protects backend servers from attackers." (CORS protects web users and origins from unauthorized script access within the browser; attackers can easily bypass CORS using `curl` or non-browser HTTP clients).
    - "A CORS error means the request never reached the server." (For simple requests without preflight, the request reaches the server, executes, and returns; the browser merely hides the response from client JavaScript).
    - "Origin and domain mean the exact same thing." (An origin includes scheme, host, and port; `http://example.com:80` and `https://example.com:443` are completely distinct origins).
13. **What You Can Ignore—for Now:** WebCrypto subtle cryptographic algorithms, Cross-Origin Opener Policy (COOP) and Cross-Origin Embedder Policy (COEP) memory-sharing details, Trusted Types API implementations.
14. **Progressive Support:**
    - *Question:* If your browser blocks a cross-origin fetch request with a CORS error, why does running the same URL in `curl` succeed completely?
    - *Hint 1:* Who enforces the Cross-Origin Resource Sharing policy?
    - *Hint 2:* Is `curl` a web browser running untrusted JavaScript from other websites?
    - *Expected Observation:* The browser console shows a CORS denial, but curl prints the full response payload immediately.
    - *Full Explanation:* CORS is an agreement enforced by user agents (browsers) to protect users from malicious scripts running in their browsing context. Command-line clients like curl do not execute untrusted third-party web scripts, so they do not enforce CORS response restrictions.
15. **Visual Requirements:** Diagram contrasting: (1) Same-Origin Policy boundary between Origin A and Origin B, (2) The CORS validation checkpoint inside the browser user agent, and (3) Non-browser client (`curl`) communicating directly with Origin B without browser mediation.
16. **Exit Criteria:** Learner produces a browser CORS denial trace alongside a matching successful curl trace and writes an architectural explanation of the user-agent enforcement boundary.
17. **Competency Mapping:** Judge (Primary: security boundary analysis), Diagnose (Growth: CORS error troubleshooting).
18. **Provenance / Source Anchors:** WHATWG Fetch Living Standard (*CORS Protocol*), WHATWG HTML Living Standard (*Origin computation*), W3C Content Security Policy Level 3 (Working Draft, Aug 2026).
19. **Failure / Inference Limits:** Live CORS enforcement can be truthfully demonstrated only within a real browser or headless-browser user-agent context; non-browser tools (Python, curl) demonstrate the absence of enforcement.

---

### 8.5 Lesson L12-04: “Why does my page feel slow?”

1. **Learner Question:** Why does clicking a button or scrolling sometimes freeze completely even on a multi-core computer, and how does the browser decide when to run my JavaScript versus updating the screen?
2. **Before / After Capability:**
   - *Before:* Assumes JavaScript runs across multiple background threads automatically, or thinks the browser executes a rigid "one macrotask $\rightarrow$ one microtask $\rightarrow$ render" cycle with a fixed 16.7 ms frame clock.
   - *After:* Can trace how an agent's Window/Document event loop processes tasks from multiple task queues, drains the microtask queue at defined checkpoints (Promises), and schedules rendering opportunities; and explain how long-running main-thread tasks cause UI jank (**Concurrency preview only**).
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisites: `L12-01` (Renderer main thread) and `L12-02` (Rendering pipeline).
   - Support: JavaScript Promise and `queueMicrotask()` intuition.
4. **Concepts:** Previews concurrency concepts strictly in the browser agent domain. Does **not** define `EC-CON-015` Concurrency (reserved for M15 `L15-01`).
5. **Mental Model:** An agent-scoped event loop managing cooperative execution and rendering opportunities. JavaScript execution, DOM updates, and layout calculations on a page share the renderer main thread. Tasks are dispatched from task queues; microtasks are drained to completion after tasks; and rendering opportunities are scheduled periodically by the browser engine. Heavy synchronous computation starves the event loop, delaying input events and rendering opportunities, causing visible jank.
6. **Mechanism Sequence:**
   $$\text{1. Select & Execute One Task from a Task Queue (e.g., Timer, User Input)}$$
   $$\text{2. Perform Microtask Checkpoint: Drain Microtask Queue completely (Promises, queueMicrotask)}$$
   $$\text{3. Check if Rendering Opportunity exists (e.g., VSync / Display refresh alignment)}$$
   $$\text{    - If Yes: Run RequestAnimationFrame } \longrightarrow \text{ Style } \longrightarrow \text{ Layout } \longrightarrow \text{ Paint}$$
   $$\text{4. Repeat Loop}$$
7. **Prediction-Before-Observation:** If a button click triggers an infinite `while(true) {}` loop in JavaScript, will the browser still update the text on the page or allow you to select text with your mouse?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Observe:* Load a local test page with an animated CSS spinner or an incrementing numerical counter. Observe smooth 60 Hz animation.
   - *Break:* Click a button that executes a synchronous 1.5-second blocking computation (`const start = performance.now(); while (performance.now() - start < 1500) {}`). Observe that the CSS animation/counter freezes solid and input clicks are unresponsive during those 1.5 seconds.
   - *Fix:* Refactor the heavy computation into smaller chunked tasks using `setTimeout()` or `requestAnimationFrame()`, or explain how background Web Workers can move CPU work off the main thread. Observe that the UI remains interactive.
   - *Explain:* Trace the difference in execution order between tasks (`setTimeout`), microtasks (`Promise.resolve().then()`), and animation callbacks (`requestAnimationFrame`). Explain why microtasks run before the next rendering opportunity.
   - *Judge:* Evaluate frame budgets: explain why 60 Hz displays suggest an illustrative period of ~16.7 ms, but why modern displays (120 Hz, variable refresh) and power-saving modes mean the browser engine does not operate on a single hardcoded frame threshold.
9. **Required Commands / Tools:** Real browser with interactive UI and DevTools Performance panel.
10. **Machine-Checkable Evidence:** Test script asserts task queue order using a standardized JavaScript test snippet logging sequence numbers across Task, Microtask, and Animation frames.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner explains the main-thread event loop without claiming JavaScript is globally single-threaded (noting Web Workers and multi-process architecture), explains why microtasks drain before rendering, and treats concurrency strictly as a preview.
12. **Misconceptions Addressed:**
    - "JavaScript and browsers are single-threaded." (Browsers are multi-process and multi-threaded; an individual Window/Document script runs within its agent's main-thread event loop, but workers and browser subsystems run on separate threads/processes).
    - "The event loop executes a rigid, fixed cycle of exactly one task, one microtask, and one screen render." (Engines drain multiple microtasks until the queue is empty; rendering opportunities occur conditionally based on refresh timing and document visibility).
    - "Every display requires a fixed 16.7 ms frame budget." (Displays feature varying refresh rates, such as 90 Hz, 120 Hz, or 240 Hz, or dynamic variable refresh rates; 16.7 ms is illustrative for 60 Hz, not an invariant law).
13. **What You Can Ignore—for Now:** WebAssembly multi-threaded shared memory atomics (`Atomics.wait`), Web Workers transferable `ArrayBuffer` internals, Chrome scheduler task prioritization internal heuristics.
14. **Progressive Support:**
    - *Question:* Why does a `Promise.resolve().then(...)` callback execute before a `setTimeout(..., 0)` callback even if the timer timeout is 0 ms?
    - *Hint 1:* Check which queue promises belong to vs. timers.
    - *Hint 2:* Microtasks are drained immediately after the current task finishes, before the next task is picked from a task queue.
    - *Expected Observation:* The Promise callback executes immediately after the current script block, while the timer callback waits for the next event loop turn.
    - *Full Explanation:* Timers schedule tasks in a general task queue. Promises schedule callbacks in the microtask queue. The HTML specification requires the event loop to perform a microtask checkpoint and completely drain the microtask queue before picking the next task or rendering.
15. **Visual Requirements:** Diagram of the Window/Document Event Loop: Task Queues (Timers, I/O, UI Events) $\rightarrow$ Execution $\rightarrow$ Microtask Checkpoint (Draining Promise reactions) $\rightarrow$ Conditional Rendering Opportunity (rAF $\rightarrow$ Style $\rightarrow$ Layout $\rightarrow$ Paint) $\rightarrow$ Next Iteration.
16. **Exit Criteria:** Learner traces the execution sequence of tasks and microtasks, demonstrates main-thread UI jank, and explains why synchronous work blocks rendering.
17. **Competency Mapping:** Observe (Primary: UI freeze and event loop trace), Diagnose (Growth: main-thread bottleneck analysis), Estimate (Growth: frame budget trade-offs).
18. **Provenance / Source Anchors:** WHATWG HTML Living Standard (*Event loops*, *Processing model*), W3C Navigation Timing Level 2.
19. **Failure / Inference Limits:** Microtask execution timing is deterministic per spec; however, exact rendering opportunity frequency and task prioritization between different task sources (e.g., user input vs. timer) are browser-implementation dependent.

---

## 9. Source Expedition EXP-03 Design — Chromium Process Model & Site Isolation

### 9.1 Expedition Overview & Pedagogical Purpose
- **Identity:** `EXP-03` — Chromium Process Model & Site Isolation Source Expedition
- **Module Home:** M12 (Web & Browser: The Integrated Case)
- **Primary Competency:** Observe
- **Growth Competencies:** Trace, Explain
- **Pedagogical Purpose:** Bridge conceptual browser architecture with production systems code by guiding the learner through three verified anchor points in the official Chromium open-source codebase. The learner directly inspects how production software implements process assignment, Site Isolation policies, and browser-side security enforcement.

---

### 9.2 Source Route & Verification Status

All three inspection targets have been rechecked and verified active on `chromium.googlesource.com` as of 2026-09-03:

1. **Design Documentation Anchor:**
   - **Path:** `docs/process_model_and_site_isolation.md`
   - **URL:** `https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md`
   - **Key Content:** Details Chromium's multi-process design, the motivation for Site Isolation (mitigating UXSS vulnerabilities and Spectre speculative execution leakage), browsing context groups, and process reuse limits.
2. **Process Selection Logic Anchor:**
   - **Path:** `content/browser/site_instance_impl.cc`
   - **URL:** `https://chromium.googlesource.com/chromium/src/+/main/content/browser/site_instance_impl.cc`
   - **Key Content:** Implements `SiteInstanceImpl::GetProcess()`, `SiteInfo`, and logic determining whether a new navigation shares an existing renderer process or requires allocating a separate process.
3. **Browser Policy Enforcement Anchor:**
   - **Path:** `content/browser/security/cpsp/child_process_security_policy_impl.cc`
   - **URL:** `https://chromium.googlesource.com/chromium/src/+/main/content/browser/security/cpsp/child_process_security_policy_impl.cc`
   - **Path Currentness Note:** Formerly located at `content/browser/child_process_security_policy_impl.cc`, the file was relocated into the `content/browser/security/cpsp/` subdirectory in recent Chromium refactorings.
   - **Key Content:** Implements centralized browser-side security policy (`ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin`), ensuring that compromised renderer processes cannot access cross-site cookies, local files, or unauthorized origins.

---

### 9.3 Bounded Inspection Card & Stopping Points

To ensure high educational value without overwhelming learners in Chromium's vast codebase (~35 million lines of code), the expedition specifies a single bounded inspection card:

```markdown
### EXP-03 Inspection Card: Chromium Process Model & Site Isolation

- [ ] **Target 1 (Architecture Claim):** In `docs/process_model_and_site_isolation.md`, locate the section describing "Site Isolation". What specific hardware vulnerability class motivated isolating cross-site iframes into separate OS processes?
      *Stopping Point:* Stop after reading the introduction and Site Isolation motivation sections. Do not read Android-specific WebView embedder details.
- [ ] **Target 2 (Process Assignment):** In `content/browser/site_instance_impl.cc`, locate the method `SiteInstanceImpl::GetProcess()`. What check does Chromium make before deciding to reuse an existing renderer process?
      *Stopping Point:* Inspect the entry conditions of `GetProcess()`. Do not trace internal IPC channel allocation or RenderProcessHost initialization.
- [ ] **Target 3 (Security Policy Enforcement):** In `content/browser/security/cpsp/child_process_security_policy_impl.cc`, locate the method `CanAccessDataForOrigin()`. What parameters does it evaluate to verify if a process is authorized to access an origin's data?
      *Stopping Point:* Stop at the origin validation assertion. Do not trace file scheme or blob URL legacy compatibility helpers.
- [ ] **Target 4 (Nuance / Reflection):** Identify one difference between the conceptual "one site = one process" model and the real-world logic in `site_instance_impl.cc` (e.g., process limits, spare renderers, or memory pressure fallbacks).
- [ ] **Target 5 (Provenance Record):** Record the exact Git commit hash or date of the Chromium source tree inspected.
```

---

### 9.4 Licensing, Rights & Non-Compilation Boundaries

1. **Zero Compilation Requirement:** Learners do **not** download the 100 GB Chromium repository or compile Chromium from source. Inspection is conducted entirely via the official web-based Gitiles source browser (`chromium.googlesource.com`).
2. **Licensing & Copyright Discipline:**
   - Chromium source code is licensed under BSD-style terms with third-party components under distinct licenses.
   - EXP-03 is link-and-inspection-only. Essential CS does not vendor, mirror, or redistribute Chromium source code.
   - Any educational quotes or code snippets included in learner guides are bounded to minimal functional lines (fair use) with clear copyright attribution to The Chromium Authors.

---

## 10. Shared Environment & Preflight Contract

### 10.1 Status of OQ-BP-006
**OQ-BP-006 remains explicitly OPEN.**
This Design Dossier deliberately does **not** hardcode a single pinned operating system version, Python minor version (e.g., locking strictly to 3.12 or 3.13), `curl` version, or browser version as a permanent curriculum invariant.

Instead, the design classifies runtime capabilities and establishes an empirical preflight verification script (`tests/preflight_network_web.py`) that probes host capabilities, records actual runtime versions and TLS backends, and enables truthful fallbacks or graceful skips when optional or GUI tools are absent.

---

### 10.2 Preflight Capabilities Matrix

| Tool / Capability | Module Placement | Role in Curriculum | Classification | Environment Constraints & Sensitivity | Truthful Fallback / Skip Strategy | Checked Baseline at Design |
|---|---|---|---|---|---|---|
| **Python 3 `socket`** | M10, M11, LAB-REQ-01 | Required for Core | Standard Library / Unprivileged | Available in standard CPython; exact errno strings and timing vary by OS. | Hard prerequisite; if sockets are unavailable, Core networking is blocked. | CPython 3.12 / 3.13; OQ-BP-006 OPEN |
| **Python 3 `http.server`** | M11, M12, LAB-REQ-01 | Required for Core | Standard Library / Unprivileged | Binds to `127.0.0.1` on port 0; handles standard HTTP/1.1 requests. | Hard prerequisite for local HTTP server fixtures. | CPython 3.12 / 3.13; OQ-BP-006 OPEN |
| **Python 3 `ssl`** | M11 | Required for Core | Standard Library / Unprivileged | Uses host OpenSSL / LibreSSL library; supports TLS 1.3 on modern OSes. | Dedicated local verification context; no external CA dependency. | OpenSSL 3.x backend |
| **`curl` CLI** | M11, LAB-REQ-01 | Required for LAB-REQ-01 | External Binary / Unprivileged | Common on Linux, macOS, and modern Windows; TLS backend varies. | If missing, record `TOOL MISSING`; allow installation or run approved standalone raw socket client. | curl 8.x (tested on 8.5.0); OQ-BP-006 OPEN |
| **Linux `ss`** | M10 | Optional Observation | Environment-Sensitive (Linux) | Part of `iproute2`; omitted from minimal Docker images and non-Linux. | If missing, record `TOOL UNAVAILABLE`; preserve Python endpoint evidence. | iproute2 `ss -tan` |
| **Linux `ip route`** | M10 | Optional Observation | Environment-Sensitive (Linux) | Part of `iproute2`; container routing tables may be restricted. | If missing, record `TOOL UNAVAILABLE`; do not synthesize host routes. | iproute2 |
| **Netcat (`nc`)** | M10 | Optional / Illustrative | Environment-Sensitive | Syntax fragmentation (OpenBSD vs. GNU flags). | Do not rely on netcat flags; use Python socket one-liners instead. | Netcat OpenBSD / GNU |
| **`openssl` CLI** | M11 | Optional / Auxiliary | Environment-Sensitive | Missing by default on many Windows installations. | Core TLS verification uses Python `ssl`; OpenSSL CLI is optional. | OpenSSL 3.x CLI |
| **`traceroute`** | M10 | Optional / Capability-gated | Privilege-Sensitive | Raw socket / ICMP permissions vary; often blocked in containers. | If unavailable or blocked, report `SKIP`; reference traces are labeled reference-only. | traceroute / mtr |
| **`tcpdump` / Wireshark** | M10 | Optional / Capability-gated | Privilege-Sensitive | Requires `CAP_NET_RAW` / `sudo` or packet-capture helper permissions. | Strictly Optional; never required for Core. Pre-captured PCAP files are reference evidence. | tcpdump 4.99+ |
| **Desktop Browser (Chromium / Chrome)** | M12 | Preferred Browser Observation | Browser/GUI-Dependent / Current Practice | Requires graphical desktop environment (X11/Wayland/Windows/macOS). | If running in headless container/WSL, record `NO LIVE BROWSER OBSERVATION`; use reference traces. | Chromium 120+ / Chrome |
| **Alternative Browser (Firefox)** | M12 | Optional Browser Observation | Browser/GUI-Dependent / Current Practice | Process model differs from Chromium; Gecko rendering engine. | Optional comparison; do not use Firefox to validate Chromium internal claims. | Firefox ESR / Release |
| **Local HTML/JS Fixtures** | M12 | Required for Core | Course-owned / Unprivileged | Static files served on loopback port 0; standard modern JavaScript. | Browser capability is gated separately from static file serving. | Modern ECMAScript (fetch, Promises) |

---

### 10.3 Preflight Verification Script Contract

Before running any network or web module tests, the environment must execute the preflight verification script (`tests/preflight_network_web.py`), which outputs a structured JSON report and human-readable summary:

```json
{
  "timestamp": "2026-09-03T09:30:00Z",
  "os": {
    "system": "Linux",
    "release": "6.8.0-generic",
    "architecture": "x86_64"
  },
  "python": {
    "version": "3.12.3",
    "has_socket": true,
    "has_ssl": true,
    "ssl_version": "OpenSSL 3.0.13 30 Jan 2024",
    "tls1_3_supported": true
  },
  "tools": {
    "curl": {
      "available": true,
      "version": "8.5.0",
      "tls_backend": "OpenSSL/3.0.13"
    },
    "ss": { "available": true },
    "ip_route": { "available": true },
    "openssl_cli": { "available": true },
    "traceroute": { "available": false },
    "tcpdump": { "available": false, "reason": "non-root environment" }
  },
  "browser": {
    "gui_available": true,
    "chromium_detected": true,
    "chromium_version": "128.0.6613.119",
    "firefox_detected": true
  },
  "preflight_status": "READY_CORE_AND_LAB_REQ_01"
}
```

---

## 11. Evidence & Assessment Matrix

| Lesson / Lab | Primary Competency | Candidate Machine-Checkable Evidence | Reviewer-Required Pedagogical & Architectural Evidence |
|---|---|---|---|
| **L10-01** (Message Across Internet) | Trace | Server binds port 0; client connects and exchanges 16-byte payload; asserts port is non-zero; clean teardown. | Reviewer checks learner's written distinction of Name vs. Address vs. Route vs. Port/Socket. |
| **L10-02** (TCP Reliability) | Trace | Stream reader reconstructs multi-chunk payload across arbitrary `recv()` partition boundaries; UDP datagram test confirms message boundary preservation. | Reviewer checks explanation of why TCP ACK does not equal application commit; verifies IPv4 vs. IPv6 UDP checksum rules. |
| **L10-03** (Request Timeout) | Diagnose | Unbound port yields refusal disposition; silent server triggers client `TimeoutError` after configured deadline; `.invalid` resolver failure is recorded or marked `NO LIVE DNS FAILURE`. | Reviewer checks explanation of partial failure ambiguity and why blindly retrying timed-out requests can duplicate mutations. |
| **L11-01** (Secure Server / TLS) | Explain | Automated test verifies 3 handshake cases: (1) valid local cert succeeds, (2) hostname mismatch rejected, (3) untrusted root CA rejected. Asserts zero verification bypasses. | Reviewer checks explanation of why TLS validates domain identity rather than business safety; explains forward secrecy boundary. |
| **L11-02** (HTTP Semantics) | Trace | Raw HTTP requests parse status codes ($200, 400, 404$), headers, and CRLF line breaks; validates uniform interface. | Reviewer checks learner's explanation of Resource vs. Representation, Safe vs. Idempotent methods, and why $200\text{ OK}$ != business correctness. |
| **L11-03** (Caching & Speed) | Observe | Conditional request with matching `If-None-Match` returns $304\text{ Not Modified}$ with 0 body bytes; mismatched ETag returns $200\text{ OK}$ with full body. | Reviewer checks explanation of Freshness vs. Validation, opaque strong ETags, and balanced evaluation of H1, H2, and H3 trade-offs. |
| **LAB-REQ-01** (HTTP Interface Lab) | Trace | 4-step trace: Direct trace ($200$), Forwarded trace (`Via: 1.1 essential-cs-proxy`), Conditional trace ($304$, 0 body), Upstream refusal ($502$). Post-reset listener check confirms zero open sockets. | Reviewer evaluates complete `curl -v` transcripts, header comparison table, and explanation of gateway failure mapping. |
| **LAB-OPT-02** (CS144 Checkpoint 2) | Trace (Optional) | (Learner-owned independent C++ test suite if pursued). | Reviewer verifies lab is treated strictly as Optional and link-only; zero bundled Stanford code. |
| **L12-01** (Browser Architecture) | Explain | Verification of EXP-03 source inspection answers matching current Chromium repository files. | Reviewer checks learner's refutation of "one tab = one process", separation of Web spec vs. Chromium implementation, and sandboxing explanation. |
| **L12-02** (Rendering Pipeline) | Observe | Test fixture serves HTML/CSS/JS in structured order; DevTools trace records phases actually present. | Reviewer checks learner's trace of the 6 pipeline stages and explanation of why synchronous scripts block HTML parsing while `defer` does not. |
| **L12-03** (Browser Security) | Judge | Localhost dual-origin test: non-browser client (`curl`) succeeds unconditionally; browser console records CORS block; matching allow header unblocks JS. | Reviewer checks explanation of CORS as user-agent enforcement vs. server-side authorization; explains CSP defense in depth. |
| **L12-04** (Event Loop & Jank) | Observe | JavaScript task vs. microtask execution ordering test verifies Promise reactions drain before timer tasks. | Reviewer checks explanation of UI jank caused by main-thread blocking; verifies Concurrency is treated strictly as a preview. |
| **EXP-03** (Chromium Expedition) | Observe | Verification of 5 inspection card answers identifying lines and mechanisms in Chromium source. | Reviewer checks that learner correctly identified stopping points without arbitrary source-tree wandering. |

---

## 12. Canonical Concept First-Home & Revisit Audit

### 12.1 Revisit Discipline Audit

The table below confirms that no concept is re-defined, and all references across M10–M12 strictly follow the canonical definition established in their primary homes:

| Concept ID | Canonical Name | First Home | M10–M12 Revisit Role & Context | Strict Boundary Guardrail |
|---|---|---|---|---|
| **EC-CON-005** | 接口 (Interface) | M00 `L00-01` | M10 socket APIs; M11 HTTP as uniform interface contract (methods, status codes, headers, representations). | Do not treat HTTP as a programming language framework API; interface is the external protocol contract. |
| **EC-CON-010** | 故障 (Failure) | M03 `L03-03` | M10 `L10-03` network failure taxonomy; M11 `L11-02` HTTP error status codes ($4\text{xx}, 5\text{xx}$); LAB-REQ-01 gateway errors ($502$). | Maintain clear distinction between transport-level rejection, protocol errors, and application domain failures. |
| **EC-CON-011** | 缓存 (Caching) | M04 `L04-01` | M11 `L11-03` HTTP caching (freshness vs. validation, ETag, 304, private/shared caches, CDNs). | Retaining prior results under a validity policy. A cache is not an authoritative store and does not guarantee durability. |
| **EC-CON-012** | 局部性 (Locality) | M04 `L04-02` | M11/M12 network locality (CDN edge caching, connection reuse, RTT minimization). | Locality is the tendency of references to cluster; it motivates caching and CDN placement, but is not identical to caching. |
| **EC-CON-013** | 隔离 (Isolation) | M07 `L07-01` | M12 `L12-01` / `L12-03` browser multi-process architecture, renderer sandboxing, Site Isolation. | Limiting visibility and interference. Isolation supports security defense in depth, but does not equal authorization. |
| **EC-CON-017** | 信任边界 (Trust Boundary) | M07 `L07-01` | M11 `L11-01` TLS/PKI trust anchors; M12 `L12-03` Same-Origin Policy, Fetch CORS, CSP. | Boundary where authority or enforcement changes. Inputs crossing the boundary require validation. |
| **EC-CON-018** | 进程 (Process) | M06 `L06-01` | M12 `L12-01` Browser coordinator process vs. sandboxed renderer processes vs. GPU process. | Managed OS execution context with address space and privileges. Not a tab, thread, or script. |

### 12.2 Future-First-Home Guardrails

1. **EC-CON-014 一致性 (Consistency):**
   - Scheduled First Home: **M14 `L14-02`** (Database Transactions & Consistency Models).
   - *Audit Confirmation:* PASS. M11 caching discusses "freshness", "stateness", and "validation". M12 discusses DOM updates and storage. Neither module uses the word "consistent" as a formal guarantee or borrows ACID / distributed consistency terminology.
2. **EC-CON-015 并发 (Concurrency):**
   - Scheduled First Home: **M15 `L15-01`** (Concurrency Foundations, Threads & Race Conditions).
   - *Audit Confirmation:* PASS. M12 `L12-04` covers the JavaScript event loop, task queues, microtasks, and UI render blocking strictly as a **preview** and domain-specific execution model. It does not canonically define Concurrency, OS threads, race conditions, or synchronization primitives.

---

## 13. Visual System Requirements

In accordance with curriculum invariants and the visual policy, all diagrams in M10–M12 must be original, editable vector/ASCII/Mermaid assets. No diagrams may be copied verbatim from RFCs, W3C specifications, or Chromium project documentation.

### Visual 1 (M10 `L10-01`): Layered Network Indirection
```
+-------------------------------------------------------------------------+
| [1. Host Identity] Domain Name: api.example.com                         |
+-------------------------------------------------------------------------+
                                    | getaddrinfo() / DNS Resolution
                                    v
+-------------------------------------------------------------------------+
| [2. Topological Location] IP Address: 93.184.216.34 (IPv4)              |
+-------------------------------------------------------------------------+
                                    | Route Table Lookup (Longest Prefix)
                                    v
+-------------------------------------------------------------------------+
| [3. Physical Transit] Next-Hop Gateway / Interface: eth0 -> Router R1   |
+-------------------------------------------------------------------------+
                                    | Hop-by-Hop Packet Switching
                                    v
+-------------------------------------------------------------------------+
| [4. Endpoint Demux] Transport Port: TCP Port 443 -> Target Socket       |
+-------------------------------------------------------------------------+
```

### Visual 2 (M10 `L10-02`): TCP Reliability & Handshake
```
Client Endpoint                                           Server Endpoint
       |                                                         |
       |------------------- SYN (seq=100) ---------------------->|
       |<---------------- SYN-ACK (seq=500, ack=101) ------------|  3-Way Handshake
       |------------------- ACK (ack=501) ---------------------->|  (Establishes Connection)
       |                                                         |
 [ESTABLISHED]                                             [ESTABLISHED]
       |                                                         |
       |===== Data Segment 1: Bytes 101-200 (100 bytes) ========>|
       |===== Data Segment 2: Bytes 201-300 (100 bytes) ========>|
       |<==== Cumulative ACK (ack=301, win=65535) ===============|  Sequence Space & Flow Control
       |                                                         |
```

### Visual 3 (M10 `L10-03`): Network Failure Spectrum
```
[Client App] ---> (1) DNS Resolution Fail ---> [Localhost Abort: No IP]
     |
     +----------> (2) Connect (SYN) -> RST ---> [Localhost Abort: Active Refusal (ECONNREFUSED)]
     |
     +----------> (3) Connect (SYN) -> Silent Drop en route ---> [Connect Timeout]
     |
 [Connected] ---> (4) Request Sent -> Server Execution / Drop -> [Read Timeout (Ambiguous State)]
     |
     +----------> (5) Peer Crash / Firewall State Drop --------> [Connection Reset (ECONNRESET)]
```

### Visual 4 (M11 `L11-01`): TLS 1.3 Handshake & Trust Boundary
```
Client                                                         Server
  |                                                              |
  |-- ClientHello [Key Share (DHE), Ciphers, SNI/ECH] ---------->|
  |<-- ServerHello [Key Share (DHE), Chosen Cipher] -------------|
  |                                                              |
  |   [Encrypted with Handshake Keys]                            |
  |<-- EncryptedExtensions, Certificate Chain, CertVerify, Finished -|
  |                                                              |
  * Client verifies Certificate Chain against Local Trust Anchors
  |                                                              |
  |-- Finished ------------------------------------------------->|
  |                                                              |
[Application Data Encrypted with AEAD Traffic Keys]
  |<============================================================>|
```

### Visual 5 (M11 `L11-02`): HTTP Message Anatomy
```
HTTP Request:
+-------------------------------------------------------------------------+
| GET /items/42 HTTP/1.1                                  [Request Line]  |
| Host: api.example.com                                   [Headers]       |
| Accept: application/json                                                |
| \r\n                                                    [Empty Line]    |
| [Optional Payload / Request Body]                       [Message Body]  |
+-------------------------------------------------------------------------+

HTTP Response:
+-------------------------------------------------------------------------+
| HTTP/1.1 200 OK                                         [Status Line]   |
| Content-Type: application/json                          [Headers]       |
| Content-Length: 32                                                      |
| ETag: "v1.0"                                                            |
| \r\n                                                    [Empty Line]    |
| {"id": 42, "status": "active"}                          [Response Body] |
+-------------------------------------------------------------------------+
```

### Visual 6 (M11 `L11-03`): Caching & Intermediary Topology
```
Client (Browser / App)       Intermediary (Proxy / CDN)             Origin Server
      |                                  |                                |
      |--- GET /data ------------------->|--- GET /data ----------------->|
      |<-- 200 OK (ETag: "v1") ----------|<-- 200 OK (ETag: "v1") --------| (Origin computes)
      |    (Stored in client cache)      |    (Stored in edge cache)      |
      |                                  |                                |
      |=== Conditional Validation ====== |                                |
      |--- GET /data (If-None-Match: "v1")>|                              |
      |                                  |--- GET /data (If-None-Match: "v1")>|
      |                                  |<-- 304 Not Modified -----------| (Zero Body)
      |<-- 304 Not Modified (Zero Body) -|    (Metadata revalidated)      |
```

### Visual 7 (M12 `L12-01`): Chromium Multi-Process Architecture (Current Practice Case)
```
+-------------------------------------------------------------------------+
|                         Browser Process (Coordinator)                   |
|  - UI & Window Management                                               |
|  - Navigation Dispatch & Process Selection (SiteInstance)               |
|  - Centralized Security Policy (ChildProcessSecurityPolicy)             |
+-------------------------------------------------------------------------+
        | (Mojo IPC)                    | (Mojo IPC)              | (Mojo IPC)
        v                               v                         v
+-----------------------+     +-----------------------+     +-------------+
| Sandboxed Renderer A  |     | Sandboxed Renderer B  |     | GPU Process |
| (Site: site-a.com)    |     | (Site: site-b.com)    |     | Composites  |
| - Blink / DOM / Style |     | - Blink / DOM / Style |     | layer tiles |
| - V8 JavaScript Engine|     | - V8 JavaScript Engine|     | to screen   |
| - OOPIF for site-a    |     | - OOPIF for site-b    |     +-------------+
+-----------------------+     +-----------------------+
```

### Visual 8 (M12 `L12-02`): Document Rendering Pipeline
```
[HTML] ---> Tokenize/Parse ---> [DOM Tree] ----+
                                               |
                                               v
[CSS]  ---> Tokenize/Parse ---> [CSSOM Tree] -> [Render Tree] (Style Resolution)
                                                       |
                                                       v
                                               [Layout / Reflow] (Geometry Box Model)
                                                       |
                                                       v
                                               [Paint] (Display Lists / Draw Commands)
                                                       |
                                                       v
                                               [Compositing] (Layer Tiles -> GPU Screen)
```

### Visual 9 (M12 `L12-03`): Web Platform Security Boundaries
```
+-------------------------------------------------------------------------+
|                               USER AGENT (Browser)                      |
|                                                                         |
|  [ Origin A: http://127.0.0.1:8000 ]                                    |
|      |                                                                  |
|      | fetch('http://127.0.0.1:9000/data')                              |
|      v                                                                  |
|  [ CORS Enforcement Gate ]                                              |
|      | - Checks Access-Control-Allow-Origin against Origin A            |
|      | - If missing: BLOCKS JavaScript access; logs error to console    |
|      | - If matching: EXPOSES response payload to Promise               |
+------|------------------------------------------------------------------+
       |                                       ^
       | HTTP Request (Origin: 8000)           | HTTP Response (200 OK)
       v                                       |
+-------------------------------------------------------------------------+
|  [ Origin B: http://127.0.0.1:9000 ] (Target API Server)                |
+-------------------------------------------------------------------------+
       ^                                       ^
       |                                       |
       +--- curl http://127.0.0.1:9000/data ---+  (Non-browser client:
            (Succeeds unconditionally!)            Bypasses browser gate!)
```

### Visual 10 (M12 `L12-04`): Window/Document Event Loop Execution
```
+-------------------------------------------------------------------------+
|                           RENDERER MAIN THREAD                          |
|                                                                         |
|  [ Task Queues ]                                                        |
|  (Timers, User Input, Network Events)                                   |
|         |                                                               |
|         v                                                               |
|  [ Pick & Execute 1 Task ] ------------------------------------+        |
|                                                                |        |
|                                                                v        |
|  [ Microtask Checkpoint ] <------------------------------------+        |
|  (Drain Promise reactions, queueMicrotask until EMPTY)                  |
|         |                                                               |
|         v                                                               |
|  [ Rendering Opportunity? ] (VSync / Display Refresh Check)             |
|         |                                                               |
|         +--- YES ---> [ Run rAF ] -> [ Style ] -> [ Layout ] -> [ Paint]|
|         |                                                               |
|         +--- NO  ---> (Skip render; immediately process next task)      |
|         |                                                               |
|         v                                                               |
|  (Repeat Event Loop Turn)                                               |
+-------------------------------------------------------------------------+
```

---

## 14. Progressive-Support Requirements

Every Lesson across M10–M12 must implement the mandatory 5-step progressive-support ladder without `details-open` elements. Expected observations must describe structural relationships and patterns rather than hardcoding errnos, ports, PIDs, or execution milliseconds:

### Checkpoint Support Ladder: L10-01 (Message Across Internet)
- **Question:** How do you determine the dynamic port assigned by the operating system when binding a Python TCP socket to port 0?
- **Hint 1:** Look at the methods available on the Python `socket` object for retrieving local address information.
- **Hint 2:** The method returns a tuple `(host, port)` containing the bound interface and port.
- **Expected Observation:** Calling `sock.getsockname()` returns a tuple where the second element is an integer greater than 0, reflecting the kernel's ephemeral port assignment.
- **Full Explanation:** Port 0 is a standardized API sentinel. Passing port 0 signals the OS transport layer to allocate an unassigned port from the dynamic range. `getsockname()` queries the kernel for the socket's bound address structure.

### Checkpoint Support Ladder: L10-02 (TCP Reliability & Handshake)
- **Question:** If the sender transmits 1000 bytes with a single `send()` call, why might the receiver require multiple `recv()` calls to read the full data?
- **Hint 1:** What is the fundamental abstraction provided by TCP compared to UDP?
- **Hint 2:** Does TCP track individual `send()` calls, or does it track a continuous stream of byte offsets?
- **Expected Observation:** The receiver's first `recv()` call returns a byte count smaller than 1000, requiring a loop that repeatedly calls `recv()` and appends chunks until 1000 bytes are accumulated.
- **Full Explanation:** TCP is an unstructured byte stream. Network packet fragmentation (MTU limits) and OS buffer draining mean transport segments do not preserve application call boundaries. Applications must implement their own message framing.

### Checkpoint Support Ladder: L10-03 (Request Timeout & Partial Failure)
- **Question:** Why does a client connecting to an unbound localhost port fail immediately with a refusal error, while connecting to a silent server hangs until a timeout expires?
- **Hint 1:** Contrast active rejection generated by the operating system kernel with the absence of application data.
- **Hint 2:** What packet does a host send when a TCP SYN hits a port with no listening process?
- **Expected Observation:** The unbound port raises `ConnectionRefusedError` immediately; the silent server raises `TimeoutError` only after the configured client deadline expires.
- **Full Explanation:** An unbound port triggers an active TCP `RST` from the host kernel, terminating the handshake immediately. A silent server completes the 3-way handshake (`ESTABLISHED`), so the client waits for application response bytes until its local read deadline elapses.

### Checkpoint Support Ladder: L11-01 (Secure Server / TLS)
- **Question:** Why does connecting to a TLS server with an untrusted certificate cause a handshake failure, and why should you never bypass it with `verify=False`?
- **Hint 1:** How does a TLS client determine whether a server's public key actually belongs to the claimed hostname?
- **Hint 2:** If any unsigned certificate were accepted, what could an attacker on the same network do to your traffic?
- **Expected Observation:** The TLS library raises a certificate verification error indicating the issuer is untrusted or the hostname does not match `subjectAltName`.
- **Full Explanation:** TLS relies on a chain of trust anchored in trusted root certificates. Disabling certificate verification allows a man-in-the-middle attacker to present their own certificate and intercept all encrypted data, completely neutralizing the security guarantees of TLS.

### Checkpoint Support Ladder: L11-02 (HTTP Semantics & Uniform Interface)
- **Question:** If an API endpoint modifies database records when receiving an HTTP `GET` request, why is this an architectural defect even if the code runs without errors?
- **Hint 1:** What does RFC 9110 define as the contract for "safe" HTTP methods?
- **Hint 2:** How do web crawlers, browser prefetchers, and intermediary caches treat `GET` requests?
- **Expected Observation:** Intermediaries or browser prefetch engines may automatically issue `GET` requests in the background, inadvertently triggering unauthorized database mutations.
- **Full Explanation:** HTTP methods establish a uniform interface contract. `GET` is normatively defined as safe (requesting no state mutation). Violating this contract breaks automated tooling, caches, and search indexing engines that rely on method semantics.

### Checkpoint Support Ladder: L11-03 (Caching & Transport Evolution)
- **Question:** When a server responds with `304 Not Modified`, why does the browser re-render the page correctly without downloading the HTML or image payload?
- **Hint 1:** What did the client send in the `If-None-Match` request header?
- **Hint 2:** Where does the client get the representation content if the server sends zero body bytes?
- **Expected Observation:** The HTTP response status line is `304 Not Modified`, the response body has a length of 0 bytes, and the client displays the representation stored in its local cache.
- **Full Explanation:** A conditional request asks the server to validate cached state. If the server's current representation matches the validator (`ETag`), the server sends 304 with no body, instructing the client to reuse its locally cached representation.

### Checkpoint Support Ladder: L12-01 (Browser Architecture & Process Model)
- **Question:** In Chrome, why does closing a single tab with an unresponsive, crashing script not crash the other open tabs?
- **Hint 1:** How does the operating system isolate distinct running programs?
- **Hint 2:** Does each site or browsing context execute in the same OS address space as the browser UI?
- **Expected Observation:** The crashed tab displays a crash error screen ("Aw, Snap!"), but the browser window, URL bar, and other open tabs remain fully functional.
- **Full Explanation:** Modern browsers isolate untrusted web content in separate OS renderer processes with restricted privileges (sandboxing). A crash in one renderer process is contained by the operating system kernel and does not corrupt the memory space of the browser coordinator process or other renderers.

### Checkpoint Support Ladder: L12-02 (Document Rendering Pipeline)
- **Question:** Why does adding the `defer` attribute to an external `<script>` tag in `<head>` make the page appear faster than using a synchronous script?
- **Hint 1:** What does the HTML parser do when it encounters `<script src="...">` without `defer` or `async`?
- **Hint 2:** Can the parser construct the DOM and trigger the initial paint while downloading a synchronous script?
- **Expected Observation:** In the DevTools Performance trace, the First Contentful Paint (FCP) occurs before the deferred script executes, whereas the synchronous script delays FCP until after download and execution.
- **Full Explanation:** Synchronous scripts block the HTML parser because the script might call `document.write()` or modify the DOM. The `defer` attribute tells the browser to download the script in parallel in the background and execute it only after HTML parsing completes, allowing the page to render without delay.

### Checkpoint Support Ladder: L12-03 (Browser Security & CORS)
- **Question:** If your browser blocks a cross-origin `fetch()` call with a CORS error, why can you successfully fetch the exact same URL using `curl` from your terminal?
- **Hint 1:** Who enforces the Cross-Origin Resource Sharing policy: the server or the client?
- **Hint 2:** What threat does CORS protect against, and does that threat exist in a command-line script?
- **Expected Observation:** The browser console displays a CORS policy denial error, but `curl` immediately prints the complete JSON or HTML response from the server.
- **Full Explanation:** CORS is a security mechanism enforced by browser user agents to prevent malicious scripts on one website from reading private data from another site using your authenticated session. Command-line tools like `curl` do not execute untrusted third-party web scripts, so they do not enforce browser CORS restrictions. Servers must implement independent authorization.

### Checkpoint Support Ladder: L12-04 (Event Loop & UI Responsiveness)
- **Question:** Why does a long-running JavaScript `while` loop on a web page freeze button clicks and CSS animations completely?
- **Hint 1:** What thread does JavaScript execution run on in a browser renderer process?
- **Hint 2:** What else shares that same thread?
- **Expected Observation:** While the JavaScript loop executes, button clicks do not register, text cannot be selected, and CSS animations stop moving until the loop terminates.
- **Full Explanation:** In a browser renderer, JavaScript execution, DOM event dispatching, and rendering opportunity updates (style, layout, paint) share the single renderer main thread via an event loop. A synchronous long task starves the event loop, preventing user input processing and rendering opportunities.

---

## 15. Source & Provenance Rules

### 15.1 Authoritative Specification Register

All architectural claims, protocol models, and evidence invariants in M10–M12 are derived directly from the authoritative specifications listed below:

1. **Transport & Network Layer:**
   - **RFC 9293:** *Transmission Control Protocol (TCP)*, August 2022 (Normative Internet Standard, STD 7; obsoletes RFC 793).
   - **RFC 768:** *User Datagram Protocol (UDP)*, August 1980 (STD 6).
   - **RFC 791:** *Internet Protocol (IPv4)*, September 1981 (STD 5).
   - **RFC 8200:** *Internet Protocol, Version 6 (IPv6) Specification*, July 2017 (STD 86).
   - **RFC 1034 / RFC 1035:** *Domain Names - Concepts and Facilities / Implementation and Specification*, November 1987 (STD 13).
   - **RFC 2606:** *Reserved Top Level DNS Names*, June 1999 (BCP 32; defines `.invalid`).
2. **Security & Cryptography Layer:**
   - **RFC 9846:** *The Transport Layer Security (TLS) Protocol Version 1.3*, July 2026 (Authoritative TLS 1.3 standard; formally obsoletes RFC 8446).
   - **RFC 9525:** *Service Identity in TLS*, November 2023 (Authoritative service identity standard; formally obsoletes RFC 6125).
   - **RFC 9849:** *TLS Encrypted Client Hello*, March 2026 (ECH privacy extension).
   - **RFC 5280:** *Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile*, May 2008.
3. **Application & Web Layer:**
   - **RFC 9110:** *HTTP Semantics*, June 2022 (STD 97).
   - **RFC 9111:** *HTTP Caching*, June 2022 (STD 98).
   - **RFC 9112:** *HTTP/1.1*, June 2022 (STD 99).
   - **RFC 9113:** *HTTP/2*, June 2022.
   - **RFC 9114:** *HTTP/3*, June 2022.
   - **RFC 9000:** *QUIC: A UDP-Based Multiplexed and Secure Transport*, May 2021.
   - **WHATWG HTML Living Standard:** *Event loops, processing model, and navigation* (Continuously updated).
   - **WHATWG Fetch Living Standard:** *CORS protocol, origin, and response filtering* (Continuously updated).
   - **W3C Content Security Policy Level 3:** *Working Draft*, 13 August 2026.
   - **W3C Navigation Timing Level 2:** *Working Draft*, 25 February 2026.
4. **Implementation Systems Reference:**
   - **Chromium Project:** *Process Model and Site Isolation* (`docs/process_model_and_site_isolation.md`).
   - **Chromium Source Code:** `content/browser/site_instance_impl.cc` and `content/browser/security/cpsp/child_process_security_policy_impl.cc` (The Chromium Authors, BSD-style license).
   - **Saltzer, Reed, Clark:** *End-to-End Arguments in System Design*, ACM TOCS, November 1984.

---

### 15.2 Licensing & Attribution Governance

1. **Original Educational Content:** All lesson prose, explanatory text, original diagrams, and conceptual walkthroughs are licensed under **CC BY-SA 4.0**.
2. **Original Code & Fixtures:** All Python server fixtures, proxy adapters, preflight scripts, and test harnesses created for M10–M12 and LAB-REQ-01 are licensed under **Apache-2.0**.
3. **Third-Party Provenance:**
   - RFC citations are referenced under fair use / IETF Trust Legal Provisions (TLP 4.0). No RFC text or diagrams are bundled verbatim.
   - Chromium source inspection references and brief quote excerpts in EXP-03 comply with BSD-3-Clause attribution requirements, acknowledging The Chromium Authors.
   - Stanford CS144 Checkpoint 2 is strictly link-only; zero Stanford code or PDF text is bundled.

---

## 16. Cross-Module Handoffs & Mini Cloud App Hooks

### 16.1 Curriculum Handoff Chain

```
[M09: Durable Storage & Storage Engines]
  Handoff: Learner understands durable writes, page caches, WAL, and physical media boundaries.
    |
    v
[M10: Networking I — IP, DNS & Transport]
  Intake: Uses OS process (M06) and I/O file descriptors (M08) to establish raw network sockets.
  Exit: Understands packet routing, TCP sequence spaces, and the partial failure spectrum.
    |
    v
[M11: Networking II — TLS, HTTP, CDN & Proxies]
  Intake: Takes raw transport streams from M10 and wraps them in cryptographic identity (TLS).
  Core Activity: LAB-REQ-01 traces HTTP interfaces, proxies, and conditional cache validation.
  Exit: Understands uniform interfaces, caching semantics, and transport multiplexing.
    |
    v
[M12: Web & Browser: The Integrated Case]
  Intake: Takes secure HTTP protocols from M11 to construct the client execution runtime.
  Core Activity: EXP-03 inspects Chromium source code for process sandboxing and Site Isolation.
  Exit: Understands the browser as a secure operating system for untrusted web software.
    |
    v
[M13: Relational Model, Storage Engine & Indexing]
  Handoff: Now that client-server communication and browser runtimes are established, the curriculum
  dives into the core stateful backend tier: relational databases, indexing, and transactional storage.
```

---

### 16.2 Mini Cloud App Evolution Hooks (Milestone P3 & P4)

1. **Milestone P3 — Real Network Path & Bounded Failure (`M10`–`M11` Integration):**
   - **Scope:** Replaces local in-memory or pipe communication with real TCP/HTTP socket endpoints running on localhost.
   - **Mechanisms Applied:**
     - Client connects to the Mini Cloud App backend over TCP.
     - HTTP API endpoints enforce method semantics (GET for reading notes/tasks; POST for creating items; PUT/DELETE for updates).
     - Client and server implement explicit timeout deadlines (`socket.settimeout()`).
     - Client handles partial failure ambiguity: implements idempotency keys for mutative requests to ensure retries do not create duplicate records.
     - Server sends `ETag` and `Cache-Control` headers for item representations; client uses `If-None-Match` to avoid re-fetching unchanged representations (`304 Not Modified`).
2. **Milestone P4 Preview — Query Shape & Web Frontend Integration (`M12` Context):**
   - **Scope:** In M12, the Mini Cloud App exposes a minimal web frontend that issues `fetch()` calls to the backend API from a distinct origin, requiring configuration of CORS headers (`Access-Control-Allow-Origin`).
   - **Event Loop & UI:** The web UI implements asynchronous background fetching (`fetch()`), demonstrating how non-blocking I/O keeps the user interface responsive and prevents main-thread jank.

---

## 17. Explicit Non-Goals & Later-Module Boundaries

To preserve curriculum focus and prevent cognitive overload, the following topics are explicitly excluded from M10–M12 and reserved for later modules:

- **BGP / Autonomous System Routing:** No global routing policy algorithms (reserved for Deep Dives / M20+).
- **Writing a TCP Stack from Scratch in Core:** Reserved for optional self-study via LAB-OPT-02; Core focuses on transport abstractions and socket boundaries.
- **Congestion Control Derivations:** No mathematical proofs of BIC, CUBIC, or BBR (reserved for M20+).
- **Public Packet Sniffing / Scanning:** No `nmap`, `scapy`, or raw socket packet injection against public networks.
- **Frontend Frameworks:** No React, Vue, Svelte, Angular, or CSS grid layout trivia in M12; M12 teaches browser systems architecture, not web development.
- **Compiling Chromium:** EXP-03 is source inspection only; no local Chromium builds.
- **Canonical Consistency:** `EC-CON-014` Consistency is strictly reserved for **M14 `L14-02`**.
- **Canonical Concurrency:** `EC-CON-015` Concurrency is strictly reserved for **M15 `L15-01`**.
- **Distributed Consensus Algorithms:** Paxos, Raft, and two-phase commit are strictly reserved for Stage 6 (M16+).

---

## 18. Implementation Handoff

Subsequent Lesson and Lab implementation agents must adhere to the following contracts:

1. **Strict File Structure:**
   - Lessons reside in `book/m10_networking_i/`, `book/m11_networking_ii/`, and `book/m12_web_browser/`.
   - LAB-REQ-01 code resides in `labs/lab_req_01/`.
   - EXP-03 inspection materials reside in `labs/exp_03/`.
   - Preflight scripts reside in `tests/preflight_network_web.py`.
2. **Port Allocation Contract:** Every socket listener created in tests or activities must bind to `127.0.0.1` on port `0`. Hardcoded ports (e.g., 80, 443, 8080, 3000) are strictly prohibited.
3. **No Fabricated Evidence:** If an optional tool (`ss`, `ip route`, `traceroute`, desktop browser) is absent, tests and logs must truthfully output `TOOL UNAVAILABLE` or `NO LIVE BROWSER OBSERVATION` and record fallback evidence. Never fabricate terminal outputs.
4. **Process Cleanup Discipline:** All test fixtures launching background processes (`OriginServer`, `IntermediaryAdapter`) must track PIDs, implement graceful `SIGTERM` teardown, enforce join deadlines, and execute a post-reset listener verification asserting that target ports actively refuse connections.
5. **No Verification Bypass:** Never instruct learners or write scripts using `curl -k`, `verify=False`, or disabled certificate hostname validation.

---

## 19. Risks & Design Blockers

| Risk / Item | Severity | Classification | Mitigation Strategy |
|---|---|---|---|
| **OQ-BP-006 (Version Pinning)** | Low | OPEN / Managed | Classified tools into capability tiers; preflight script records actual host versions empirically without brittle hardcoding. |
| **GUI / Browser Dependency** | Medium | Managed | M12 activities provide a dual track: live DevTools inspection when a graphical browser is present, and course-owned reference traces when running in headless containers. |
| **W3C Draft Currentness** | Low | Managed | CSP Level 3 and Navigation Timing Level 2 are explicitly marked as Working Drafts with checked dates (Aug/Feb 2026) and implementation recheck gates. |
| **Stanford CS144 Rights** | Low | Resolved | LAB-OPT-02 rights remain UNESTABLISHED; strictly maintained as Optional and link-only with zero bundled code. |
| **Chromium Source Drift** | Low | Managed | EXP-03 verified against current Gitiles paths on 2026-09-03, with historical path migration noted for `child_process_security_policy_impl.cc`. |

---

## 20. Final Recommendation

The M10–M12 design is technically sound, fully aligned with all curriculum invariants, strictly respectful of canonical concept first homes and future guardrails, and supported by verified normative sources (RFC 9846, RFC 9525, RFC 9849, RFC 9110, RFC 9111, WHATWG HTML/Fetch) and empirical localhost toolchain feasibility.

**READY FOR LESSON / ACTIVITY IMPLEMENTATION**

---

## 21. Completion Report

### Status
READY FOR LEAD REVIEW

### Exact Dispatch Base
`06206f8178021794d8406d14e94865ba4b827602`

### Exact Files Changed
- `meta/design/network-web-browser-m10-m12-design-v0.1.md` (Primary deliverable created)

### Accepted Research Dependency
Issue #68 / PR #69 (`research/network-web-browser-m10-m12-v0.1.md` merged at `d10d0c6e9bd031bab49763d5e0e4fd8baf621400`).

### 10-Lesson Audit
All 10 canonical Lessons across M10, M11, and M12 are preserved without addition, deletion, or renaming:
- M10: `L10-01`, `L10-02`, `L10-03`
- M11: `L11-01`, `L11-02`, `L11-03`
- M12: `L12-01`, `L12-02`, `L12-03`, `L12-04`

### Concept Audit
- Zero new canonical concept first homes in M10–M12.
- 7 canonical concepts revisited strictly under their primary homes: `EC-CON-005` (Interface), `EC-CON-010` (Failure), `EC-CON-011` (Caching), `EC-CON-012` (Locality), `EC-CON-013` (Isolation), `EC-CON-017` (Trust Boundary), `EC-CON-018` (Process).
- Strict future-home guardrails enforced: `EC-CON-014` Consistency remains M14 (`L14-02`); `EC-CON-015` Concurrency remains M15 (`L15-01`).

### Protocol Currentness
- TLS 1.3 specified per **RFC 9846** (July 2026, obsoleting RFC 8446).
- Service Identity specified per **RFC 9525** (obsoleting RFC 6125).
- Encrypted Client Hello specified per **RFC 9849**.
- CSP Level 3 and Navigation Timing Level 2 labeled as W3C Working Drafts with recheck gates.

### M10 Evidence Design
- Dynamic port 0 allocation on `127.0.0.1`.
- Deterministic loopback refusal and accepted-but-silent read deadline timeout.
- Capability-gated `.invalid` DNS resolution.
- Zero brittle assumptions: no hardcoded errnos, no fixed latency thresholds, no fixed `recv()` partition sizes.

### LAB-REQ-01 Design
- Complete 4-step trace using original Essential CS localhost origin and intermediary adapter.
- `curl -v` preflight with version and TLS backend logging.
- `Via: 1.1 essential-cs-proxy` tracking header.
- Conditional ETag request yielding `304 Not Modified` with zero body transfer.
- Controlled upstream refusal mapped to `502 Bad Gateway`.
- Strict PID lifecycle and post-reset listener verification asserting active refusal.

### LAB-OPT-02 Rights Disposition
- Stanford CS144 Checkpoint 2 rights remain UNESTABLISHED.
- Maintained strictly as Optional and link-only; zero bundled code, assignment text, or grading scripts; do not promote to Required.

### M12 Browser & Spec Evidence Design
- Strict 4-layer separation: Web Platform specification vs. Chromium implementation vs. DevTools observation vs. reference evidence.
- Refutation of "one tab = one process" myth.
- CORS specified as user-agent response read-access enforcement, contrasted with non-browser client (`curl`).
- Truthful fallback: `NO LIVE BROWSER CORS OBSERVATION` when running without a real browser; no undeclared Playwright/Node dependency.

### EXP-03 Route
- Verified 3-step inspection on `chromium.googlesource.com`:
  1. `docs/process_model_and_site_isolation.md`
  2. `content/browser/site_instance_impl.cc`
  3. `content/browser/security/cpsp/child_process_security_policy_impl.cc`
- Bounded 5-item inspection card; zero local compilation required.

### Environment & Preflight (OQ-BP-006)
- OQ-BP-006 remains explicitly OPEN.
- Tools categorized into Required Core, LAB-REQ-01 Required, Optional, Environment-Sensitive, Browser/GUI-Dependent, and Privilege-Sensitive.
- Preflight verification script contract (`tests/preflight_network_web.py`).

### Progressive Support & Visuals
- All 10 lessons equipped with 5-step support ladders (Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation); zero `details-open`.
- Original editable diagrams specified for all 10 lessons; zero copied RFC/W3C/Chromium figures.

### Provenance & Licensing
- Essential CS content licensed under CC BY-SA 4.0 (text) and Apache-2.0 (code).
- Third-party sources cited with formal attribution; BSD-3-Clause notices respected for Chromium; IETF fair use.

### Risks / Blockers Classification
- No critical design blockers; all identified risks managed through capability matrices and truthful fallbacks.

### Recommended Lead Focus
- Verify LAB-REQ-01 process lifecycle and failure mapping contract.
- Review M12 4-layer evidence separation and CORS user-agent enforcement boundaries.
- Confirm that future concept guardrails for M14 Consistency and M15 Concurrency are airtight.

### Final Dossier Recommendation
READY FOR LESSON / ACTIVITY IMPLEMENTATION
