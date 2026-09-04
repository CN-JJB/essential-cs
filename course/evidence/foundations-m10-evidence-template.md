# Foundations M10 Evidence Template: Networking I (IP, DNS & Transport)

This evidence template records empirical host execution results, claim boundaries, and architectural evaluations for **M10 — Networking I: IP, DNS & Transport**.

---

## A — Actual Environment / Python / Capability Preflight

- **Dispatch / Working Commit**: `63c382c0d6c4aa671d9492ec3fe18d2976fc5edc`
- **Assigned Branch**: `implementation/issue-74-m10-networking-ip-dns-transport`
- **Host Operating System (`platform.system()`, `release`, `version`)**: Windows 11 (10.0.26200)
- **Hardware Architecture (`platform.machine()`)**: AMD64
- **Python Implementation & Version (`platform.python_implementation()`, `python_version()`)**: CPython 3.13.1
- **Socket Support (`import socket`)**: YES
- **Loopback Bind Port 0 Capability (`can_bind_port_0`)**: YES (Empirically verified)
- **Loopback Connect Capability (`can_connect_loopback`)**: YES (Empirically verified)
- **Optional Linux `ss` Tool Disposition**: UNAVAILABLE (Non-Linux / Windows environment)
- **Optional Linux `ip route` Tool Disposition**: UNAVAILABLE (Non-Linux / Windows environment)
- **Traceroute Tool Disposition**: `tracert` available on Windows (`C:\WINDOWS\system32\tracert.EXE`); Linux `traceroute` UNAVAILABLE
- **Packet Capture Tool (`tcpdump` / `tshark`) Disposition**: UNAVAILABLE (`TOOL_UNAVAILABLE`)
- **Resolver Capability Disposition**: LIVE_DNS_FAILURE_OBSERVED (`gaierror` with Windows errno `11001`)
- **Preflight Verification Script Output**: `tests/preflight_network_web.py` -> `READY_M10_CORE`

---

## B — L10-01 Name / Address / Route / Socket Distinction

- **Six-Entity Architecture Matrix**:
  1. **Domain Name**: Human-readable hierarchical identifier; mapped by DNS to one or more IP addresses (one-to-many / many-to-one). Not a permanent physical identity.
  2. **IP Address**: Topological network-layer locator for interface; used by routers for hop-by-hop forwarding via longest prefix match. Not a fixed machine identity.
  3. **Next-Hop Interface**: Physical adjacent link-layer gateway (MAC address) for current local subnet hop; rewritten at every router hop.
  4. **Transport Port**: 16-bit integer demultiplexing tag within host OS kernel; assigned to sockets. Not an executable program file.
  5. **Socket**: File descriptor / handle managed by kernel representing communication endpoint.
  6. **Process**: OS execution context (M06) holding socket file descriptors.
- **Router Inspection Boundary**: Routers primarily forward by destination IP prefix, but modern middleboxes/firewalls can inspect L4 ports and higher metadata for QoS/filtering; routers are not universally constrained to L3 headers.

---

## C — Port-0 Local Endpoint + Bounded Loopback Exchange

- **Command Run**: `python labs/foundations/m10/endpoint_observer.py`
- **Process PID Recorded**: (Empirical host value recorded at runtime, e.g. `74360`)
- **Bind Address Requested**: `('127.0.0.1', 0)`
- **Kernel Allocated Port**: Dynamic non-zero port (Empirical value recorded at runtime, e.g. `63509`)
- **Client Dynamic Port**: Dynamic ephemeral port (Empirical value recorded, e.g. `63510`)
- **Payload Transmitted**: `CS-ESSENTIAL-M10` (16 bytes)
- **Payload Received**: `CS-ESSENTIAL-M10` (16 bytes)
- **Loopback Exchange Status**: `SUCCESS`
- **Post-Execution Teardown**: Server and client sockets cleanly closed; endpoint verified dormant.

---

## D — L10-02 TCP Byte-Stream Reconstruction + Actual recv() Partition

- **Command Run**: `python labs/foundations/m10/stream_framing.py`
- **Messages Sent Count**: 5 discrete messages
- **Total Logical Bytes Sent**: 113 bytes
- **Framing Protocol**: Length-prefixed binary framing (`!H` 2-byte unsigned short header + payload)
- **Actual `recv()` Chunk Partitions Observed**:
  - Sample partition sequence: `[16, 4, 16, 5, 7, 16, 16, 16, 9, 16, 2]`
  - *Invariant Confirmation*: Partitions reflect host OS buffer state and are recorded empirically; machine tests do not assert fixed chunk sizes.
- **Reconstructed Messages**:
  1. `PACKET_HEADER_DATA`
  2. `METRIC_SAMPLE_12345`
  3. `SHORT`
  4. `A_SOMEWHAT_LONGER_APPLICATION_PAYLOAD_BLOCK_FOR_TESTING`
  5. `FINAL_RECORD_END`
- **Exact Sequence Match**: `YES` (Reconstructed list matches sent list in byte content and order).

---

## E — ACK vs Application-Processing Explanation

- **TCP ACK Definition**: TCP ACK confirms that specific sequence-space byte offsets arrived uncorrupted in the remote operating system's kernel TCP receive buffer.
- **What ACK Does NOT Prove**:
  - Does NOT prove remote application invoked `recv()` to consume bytes;
  - Does NOT prove application validated message syntax/schema;
  - Does NOT prove application executed business logic (e.g., balance deduction);
  - Does NOT prove state was synchronized to durable media (`fsync` / WAL, EC-CON-016).
- **Architectural Consequence**: End-to-end confirmation requires application-layer response protocols; transport ACK must never be used as business durability evidence.

---

## F — UDP Contrast + Checksum Boundary

- **Command Run**: `python labs/foundations/m10/stream_framing.py` (UDP component)
- **Datagrams Transmitted**: `[b"UDP_RECORD_ALPHA", b"UDP_RECORD_BRAVO", b"UDP_RECORD_CHARLIE"]` (3 datagrams)
- **Datagrams Received**: 3 individual `recvfrom()` calls
- **Boundary Preservation**: `YES` (Each `recvfrom()` returns exactly one sent datagram; datagram boundaries are preserved at transport interface).
- **Buffer Truncation Behavior**: If `recvfrom()` buffer is smaller than datagram, unread bytes are discarded by OS.
- **IPv4 vs IPv6 Checksum Normative Rule**:
  - **IPv4 (RFC 768 / RFC 791)**: UDP checksum is optional; a transmitted value of `0` indicates no checksum was computed.
  - **IPv6 (RFC 8200)**: UDP checksum is **mandatory** for standard unicast traffic; IPv6 header omits header checksum, so transport checksum validation is strictly enforced.

---

## G — Controlled Loopback Refusal Disposition

- **Command Run**: `python labs/foundations/m10/failure_fixture.py`
- **Target Endpoint**: `127.0.0.1:<unbound_port>` (Preconditioned unbound ephemeral port)
- **Disposition Observed**: `CONNECTION_REFUSED_OBSERVED`
- **Exception Class**: `ConnectionRefusedError` (inheriting from `OSError`)
- **Host Error Code (`errno`)**: `10061` on Windows (`WSAECONNREFUSED`); Linux hosts observe `111` (`ECONNREFUSED`).
- **Raw Elapsed Sample**: ~`2030 ms` on Windows loopback (SYN retry timer on unbound loopback port); Linux typically observes `< 1 ms`.
- **Inference Boundary**: Machine tests must never assert fixed errno `111`, fixed refusal time `< 5 ms`, or fixed refusal-to-timeout ratio.

---

## H — Accepted-but-Silent Read-Timeout Disposition + Raw Sample

- **Command Run**: `python labs/foundations/m10/failure_fixture.py`
- **Silent Server Endpoint**: `127.0.0.1:<dynamic_port>`
- **Server Behavior**: Accepts TCP 3-way handshake (connection established), then deliberately withholds application bytes.
- **Configured Client Read Deadline**: `0.25 s` (`250 ms`)
- **Harness Outer Watchdog**: `3.0 s` (Configured strictly to prevent CI hangs; not a curriculum timing constant)
- **Disposition Observed**: `READ_TIMEOUT_OBSERVED`
- **Exception Class**: `TimeoutError` (Python `socket.timeout`)
- **Raw Elapsed Sample**: ~`260 ms` (Elapsed time reflects client deadline expiration)
- **Inference Boundary**: Timeout proves only that the client's local read deadline expired; it provides no evidence of remote progress.

---

## I — DNS Capability and Live Observation or Truthful NO LIVE DNS FAILURE OBSERVATION

- **Tested Domain**: `m10-lookup-test.invalid` (RFC 2606 reserved TLD)
- **Resolver Disposition**: `LIVE_DNS_FAILURE_OBSERVED`
- **Exception Class**: `socket.gaierror`
- **Host Error Code (`errno`)**: `11001` on Windows (`WSAHOST_NOT_FOUND`); Linux hosts observe `EAI_NONAME` (`-2`).
- **Truthfulness Invariant**: If offline or environment-restricted, harness truthfully reports `NO LIVE DNS FAILURE OBSERVATION`; no error strings or NXDOMAIN traces are fabricated.

---

## J — Partial-Failure / Retry Judgment

- **The Partial Failure Dilemma**:
  - In a distributed system, a client timeout leaves remote execution state completely ambiguous.
  - Three indistinguishable scenarios: (1) Request lost before reaching server; (2) Request reached server and failed mid-execution; (3) Server processed request completely and response was lost in transit.
- **Idempotency & Retry Safety Policy**:
  - Natural idempotent operations (`GET`, `PUT`, `DELETE` per RFC 9110) are safe to retry.
  - Non-idempotent mutations (e.g. `POST /checkout`) must never be retried blindly.
  - Mitigation: Require client-generated Idempotency Keys (`UUID`) and server-side deduplication stores before enabling automatic retries.

---

## K — Bounded Estimate Task with Units / Assumptions / Inference Limits

- **Task**: Estimate serialization delay, propagation delay, and Bandwidth-Delay Product (BDP) for transferring a payload across a wide-area network vs local loopback.
- **Explicit Illustrative Parameters**:
  - Payload Size ($S$): $10\text{ MiB} = 10 \times 1024 \times 1024 \text{ bytes} = 83{,}886{,}080 \text{ bits}$
  - Bottleneck Link Bandwidth ($B$): $100\text{ Mbps} = 10^8 \text{ bits/s} = 12.5\text{ MB/s}$
  - Fiber Route Distance ($d$): $9{,}000\text{ km}$
  - Propagation Speed in Fiber ($v$): $200{,}000\text{ km/s} = 200\text{ km/ms}$
- **Calculations**:
  - Serialization Delay: $T_{\text{tx}} = \frac{S}{B} = \frac{83{,}886{,}080}{100{,}000{,}000} \approx 0.839\text{ s} = 839\text{ ms}$
  - One-way Propagation Delay: $T_{\text{prop}} = \frac{9{,}000\text{ km}}{200\text{ km/ms}} = 45\text{ ms}$
  - Minimum Round-Trip Time: $\text{RTT}_{\text{min}} = 2 \times T_{\text{prop}} = 90\text{ ms}$
  - Bandwidth-Delay Product: $\text{BDP} = B \times \text{RTT}_{\text{min}} = 100\text{ Mbps} \times 0.09\text{ s} = 9\text{ Mbits} = 1{,}125{,}000\text{ bytes} \approx 1.07\text{ MiB}$
- **Inference Limits**:
  - Loopback measured RTT (~$0.05\text{ ms}$) is constrained by memory speed and internal kernel context switching.
  - Loopback measurements cannot be generalized to wide-area Internet connections governed by fiber propagation physics and queueing delays.

---

## L — Visual / Progressive-Support Audit

- **Visual Diagrams Implemented**:
  1. `L10-01`: Layered Network Indirection (Domain Name -> IP Address -> Next-Hop Gateway -> Transport Port -> Process) + 6-entity distinction table.
  2. `L10-02`: TCP 3-Way Handshake + Sequence/ACK Timeline + Stream buffering vs UDP datagram boundary diagram.
  3. `L10-03`: Network Failure Spectrum diagram illustrating client-visible failure stages and observation ambiguity.
- **Progressive Support Audit**:
  - All 3 lessons (`L10-01`, `L10-02`, `L10-03`) implement the mandatory 5-step ladder:
    `Question -> Hint 1 -> Hint 2 -> Expected Observation -> Full Explanation`
  - Total `<details>` tags: 12 (4 per lesson: Hint 1, Hint 2, Expected Observation, Full Explanation).
  - Total `<details open>` tags: **0** (Zero occurrences across all files).

---

## M — Safety / Cleanup / Optional-Tool Dispositions

- **Network Safety Checks**:
  - Default listeners bind strictly to `127.0.0.1:0`.
  - No public application endpoints targeted.
  - Zero port scanning; zero raw packet injection; zero ARP/DNS poisoning.
  - Zero sudo/root privilege requirements.
- **Cleanup & Reset Verification**:
  - Script: `labs/foundations/m10/reset.py`
  - Post-execution verification confirms course endpoints are dormant.
  - Executed twice in automated tests to confirm idempotency.
  - Zero wildcard deletions of learner files.
- **Optional Tools Disposition**:
  - `ss`: Truthfully reported as `TOOL UNAVAILABLE` on Windows/minimal environments.
  - `ip route`: Truthfully reported as `TOOL UNAVAILABLE` on Windows/minimal environments.
  - `tcpdump`: Truthfully reported as `TOOL UNAVAILABLE`.

---

## N — Fact vs Inference / Concept / Future-Home Audit

- **Facts (Empirically Observed on Host)**:
  - Dynamic port 0 bound to non-zero ephemeral port.
  - TCP stream partitioned across multiple `recv()` calls and reconstructed via framing loop.
  - Unbound port produced `ConnectionRefusedError`.
  - Silent server produced `TimeoutError` after client read deadline.
  - `.invalid` TLD produced `gaierror` with Windows errno 11001.
- **Inferences & Architectural Models**:
  - BDP calculation is an idealized model based on explicit propagation parameters.
  - Network failure taxonomy models client-visible stages across distributed links.
- **Canonical Concept Audit**:
  - `EC-CON-005 Interface`: Revisits in `L10-01` and `L10-02` (socket API and protocol boundaries) [AUDIT: CONFIRMED]
  - `EC-CON-010 Failure`: Revisit in `L10-03` (network failure taxonomy and partial failure) [AUDIT: CONFIRMED]
  - Zero new concept IDs introduced in M10 [AUDIT: CONFIRMED]
  - No improper canonical definition of `EC-CON-014 Consistency` (M14) or `EC-CON-015 Concurrency` (M15) [AUDIT: CONFIRMED]
- **Learner Validation Status**:
  - M10 is implementation v0.1: `READY FOR LEAD REVIEW`.
  - No unauthorized claims of `VERIFIED` or `RELEASED`.
