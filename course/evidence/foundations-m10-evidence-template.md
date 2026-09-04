# Foundations M10 Evidence Template: Networking I (IP, DNS & Transport)

This evidence template records empirical host execution results, claim boundaries, and architectural evaluations for **M10 — Networking I: IP, DNS & Transport**.

---

## A — Actual Environment / Python / Capability Preflight

- **Dispatch Base**: `63c382c0d6c4aa671d9492ec3fe18d2976fc5edc`
- **Execution / Working Commit**: `<record the exact commit actually executed>`
- **Execution Branch / Ref**: `<record the actual branch or detached ref>`
- **Host Operating System (`platform.system()`, `release`, `version`)**: `<record actual>`
- **Hardware Architecture (`platform.machine()`)**: `<record actual>`
- **Python Implementation & Version (`platform.python_implementation()`, `python_version()`)**: `<record actual>`
- **Socket Support (`import socket`)**: `<record actual PASS / BLOCKED + raw detail>`
- **Loopback Bind Port 0 Capability (`can_bind_port_0`)**: `<record actual>`
- **Loopback Connect Capability (`can_connect_loopback`)**: `<record actual>`
- **Optional `ss` Tool Disposition**: `<record actual AVAILABLE / TOOL_UNAVAILABLE / restricted>`
- **Optional `ip route` Tool Disposition**: `<record actual AVAILABLE / TOOL_UNAVAILABLE / restricted>`
- **Traceroute / tracert Tool Disposition**: `<record actual availability; do not imply live Internet use>`
- **Packet Capture Tool (`tcpdump` / `tshark`) Disposition**: `<record binary presence and capture capability separately>`
- **Resolver Capability Disposition**: `<record actual LIVE_DNS_FAILURE_OBSERVED / NO_LIVE_DNS_FAILURE_OBSERVATION / other handled disposition + raw host evidence>`
- **Preflight Verification Script Output**: `<paste or attach the actual current-run result; do not copy a reference transcript>`

> This is a reusable evidence template. Author/Lead environment observations belong in the PR Completion Report or filled evidence instance, **not** as canonical pre-populated learner evidence.

---

## B — L10-01 Name / Address / Route / Socket Distinction

- **Six-Entity Architecture Matrix**:
  1. **Domain Name**: Human-readable hierarchical identifier; mapped by DNS to one or more IP addresses (one-to-many / many-to-one). Not a permanent physical identity.
  2. **IP Address**: Network-layer address used by routing/forwarding policy; not a permanent machine identity and not guaranteed one-to-one with a host.
  3. **Route Result / Next Hop / Egress Interface**: Route lookup can yield a next-hop network-layer address plus an egress interface. If the link needs a neighbor address, IPv4 ARP or IPv6 Neighbor Discovery resolves it. A directly connected destination need not use a default gateway.
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
- **Post-Execution Teardown**: Server/client sockets are closed by the owning activity; while the assigned port is still known, the test probes that a fresh connection is not established and records the raw result.

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
  - Does NOT prove state was synchronized to durable media (`fsync` / WAL; durability was taught in M09).
- **Architectural Consequence**: End-to-end confirmation requires application-layer response protocols; transport ACK must never be used as business durability evidence.

---

## F — UDP Contrast + Checksum Boundary

- **Command Run**: `python labs/foundations/m10/stream_framing.py` (UDP component)
- **Datagrams Transmitted**: `[b"UDP_RECORD_ALPHA", b"UDP_RECORD_BRAVO", b"UDP_RECORD_CHARLIE"]` (3 datagrams)
- **Datagrams Received**: 3 individual `recvfrom()` calls
- **Boundary Observation**: In this bounded loopback run, each successful `recvfrom()` returned data from one datagram and all three small fixture datagrams were observed. This is **fixture evidence only**: UDP does not guarantee delivery or ordering; a too-small receive buffer can truncate a datagram.
- **Buffer Truncation Behavior**: If `recvfrom()` buffer is smaller than datagram, unread bytes are discarded by OS.
- **IPv4 vs IPv6 Checksum Normative Rule**:
  - **IPv4 (RFC 768 / RFC 791)**: UDP checksum is optional; a transmitted value of `0` indicates no checksum was computed.
  - **IPv6 (RFC 8200)**: Ordinary IPv6 UDP use requires a non-zero checksum; narrowly scoped tunnel exceptions are defined by later standards. Do not turn “mandatory in the ordinary case” into “zero checksum is impossible in every IPv6 context.”

---

## G — Controlled Loopback Refusal Disposition

- **Command Run**: `python labs/foundations/m10/failure_fixture.py`
- **Target Endpoint**: `127.0.0.1:<unbound_port>` (Preconditioned unbound ephemeral port)
- **Disposition Contract**: `UNBOUND_LOOPBACK_CONNECT_FAILURE_OBSERVED` or, if the runtime raises instead of returning a connect result, `UNBOUND_LOOPBACK_CONNECT_EXCEPTION_OBSERVED`.
- **Raw Host Evidence**: Record `connect_ex` result or exception type/errno/text (if any) plus elapsed sample from the actual run.
- **Inference Boundary**: Machine tests assert only that no new connection was established to the verified-unbound course endpoint. They do not require `ConnectionRefusedError`, one errno, one RST trace, or any latency threshold/ratio.

---

## H — Accepted-but-Silent Read-Timeout Disposition + Raw Sample

- **Command Run**: `python labs/foundations/m10/failure_fixture.py`
- **Silent Server Endpoint**: `127.0.0.1:<dynamic_port>`
- **Server Behavior**: Accepts TCP 3-way handshake (connection established), then deliberately withholds application bytes.
- **Configured Client Read Deadline**: `0.25 s` (`250 ms`)
- **Harness Outer Watchdog**: `3.0 s` (Configured strictly to prevent CI hangs; not a curriculum timing constant)
- **Disposition Observed**: `READ_TIMEOUT_OBSERVED`
- **Runtime Disposition**: Record the actual timeout exception/type/text produced by the named Python runtime.
- **Raw Elapsed Sample**: Record the actual sample; do not require it to fall within a fixed percentage or millisecond threshold.
- **Inference Boundary**: Timeout proves only that the client's local read deadline expired; it provides no evidence of remote progress.

---

## I — DNS Capability and Live Observation or Truthful NO LIVE DNS FAILURE OBSERVATION

- **Tested Domain**: `m10-lookup-test.invalid` (RFC 2606 reserved TLD)
- **Resolver Disposition**: Record `LIVE_DNS_FAILURE_OBSERVED`, `NO_LIVE_DNS_FAILURE_OBSERVATION`, or another explicitly handled capability result from the actual host.
- **Raw Host Error Evidence**: If present, record exception class/code/text as host evidence only; do not require `gaierror`, `11001`, or `EAI_NONAME` for acceptance.
- **Truthfulness Invariant**: If offline or environment-restricted, harness truthfully reports `NO LIVE DNS FAILURE OBSERVATION`; no error strings or NXDOMAIN traces are fabricated.

---

## J — Partial-Failure / Retry Judgment

- **The Partial Failure Dilemma**:
  - In a distributed system, a client timeout leaves remote execution state completely ambiguous.
  - Three indistinguishable scenarios: (1) Request lost before reaching server; (2) Request reached server and failed mid-execution; (3) Server processed request completely and response was lost in transit.
- **Retry / Outcome Contract**:
  - A transport timeout never authorizes retry by itself.
  - Retry safety depends on application semantics and may use naturally idempotent business operations, a stable operation identifier with deduplication, or an explicit query/reconciliation path.
  - Idempotency-Key is one implementation pattern, not a universal requirement; HTTP method semantics are taught canonically in M11.

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
  - Record any loopback timing only as a host observation; do not embed one fixed loopback RTT in acceptance criteria.
  - Loopback measurements cannot be generalized to wide-area Internet paths. BDP here is an illustrative `bandwidth × RTT` model, not a physical upper bound on “bytes in fiber” or a TCP window constant.

---

## L — Visual / Progressive-Support Audit

- **Visual Diagrams Implemented**:
  1. `L10-01`: Layered Network Indirection (Domain Name -> network-layer address -> route result / next hop + egress interface -> link neighbor as needed -> Transport Endpoint/Socket -> Process) + distinction table.
  2. `L10-02`: TCP 3-Way Handshake + Sequence/ACK Timeline + Stream buffering vs UDP datagram boundary diagram.
  3. `L10-03`: Network Failure Spectrum diagram illustrating client-visible failure stages and observation ambiguity.
- **Progressive Support Audit**:
  - All 3 lessons (`L10-01`, `L10-02`, `L10-03`) implement the mandatory 5-step ladder:
    `Question -> Hint 1 -> Hint 2 -> Expected Observation -> Full Explanation`
  - Total `<details>` tags: 12 (4 per lesson: Hint 1, Hint 2, Expected Observation, Full Explanation).
  - Progressive details configured open-by-default: **0**.

---

## M — Safety / Cleanup / Optional-Tool Dispositions

- **Network Safety Checks**:
  - Default listeners bind strictly to `127.0.0.1:0`.
  - No public application endpoints targeted.
  - Zero port scanning; zero raw packet injection; zero ARP/DNS poisoning.
  - Zero sudo/root privilege requirements.
- **Cleanup & Reset Verification**:
  - M10 activities own and close their sockets/threads in-process; they create no persistent daemon or learner artifact requiring deletion.
  - Endpoint-specific tests probe the **known old port** after close and assert only that a new TCP connection is not established, while recording raw connect result.
  - Standalone `reset.py` truthfully reports `CLEAN_NO_PERSISTENT_ARTIFACTS`; running it twice demonstrates idempotency without pretending to know unknown old endpoints.
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
  - Verified-unbound loopback endpoint produced a non-success connect disposition; raw host result is recorded.
  - Accepted-but-silent server produced the runtime's timeout disposition after the configured local read deadline.
  - `.invalid` resolver observation records the actual host disposition; exact exception/errno is host-specific.
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
