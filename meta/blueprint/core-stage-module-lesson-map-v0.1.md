# Core Stage / Module / Lesson Map v0.1

Status: **RECONCILED — Blueprint v0.1, Issue #9 integration applied (not VERIFIED; Lead review pending)**
Author: Local Agent (Curriculum Architecture Research & Design); Issue #9 integration applied by Curriculum Architecture Integrator
Date: 2026-08-30
Scope: Learner-visible Stages, Modules, and preliminary Lesson boundaries beneath the accepted macro Core spine (D-007). Original Issue #1 proposal content; the Issue #9 reconciliation outcomes (audit dispositions R1–R15, #14/#15/#16 accepted artifacts, hidden-prerequisite resolutions) have been applied on top. Still not a set of Lessons and not `VERIFIED`.

---

## 1. Design Principles

These principles are derived from the Curriculum Invariants and Decisions and applied consistently below:

**P1. Capability transitions, not topic counts.** Stage boundaries exist where the learner's ability to *do* something qualitatively changes (Trace / Explain / Observe / Diagnose / Correctness / Judge / Estimate / Learn-New-Tech), never where a conventional course happens to have a chapter boundary.

**P2. Bottom-up mechanism, top-down motivation.** The accepted spine mostly ascends the stack (bits → machine → OS → network → web → database → distributed). Each Module opens with the learner's real question ("why is my request slow?") so the mechanism has motivation, then descends to mechanism.

**P3. Teach once, revisit many times.** Every major concept has exactly one proposed primary teaching home (marked `FIRST-INTRO`). Later appearances are contextual revisits (`REVISIT`) that apply, connect, or break — never a duplicate full canonical explanation (Invariant 11, D-010).

**P4. Real mechanism over fake simulation (Invariant 5).** Where a real system can be observed safely, the default hands-on form is observation of a real system (strace, `perf`, `ss`, a real DB, a real browser). Simulations are only for mechanisms that cannot be observed cheaply (e.g., a CPU dataflow before hardware exists).

**P5. Horizontal threads recur, not late add-ons (Invariant 16, D-014).** Correctness, failure, debugging, measurement/performance, security, concurrency, cost, privacy, technical literacy, API/interface design, software engineering, napkin math are threaded through every Stage — never confined to a final "Security" Stage.

**P6. Complexity must justify itself (Invariant 8).** Each Module states what it buys for the shared world model. Tempting conventional-degree material that does not buy a capability is marked Deep Dive or Current Case, not Core.

**P7. Complete shared world model before specialization (Invariant 9).** The first Core traversal must let the learner connect the main modern computing chain (a request through a browser into a cache, a DB, a queue, an object store, and back) before Deep Dives specialize.

**P8. Mini Cloud App integration hooks only.** This proposal states *where* the Mini Cloud App can naturally integrate (as a recurring hands-on surface for observing mechanisms), but does not design its feature sequence (Issue #3 owns that).

**P9. Chinese canonical, English terms introduced with the concept (D-005).** Every canonical concept is introduced in Chinese with its English term. Since Issue #9, the canonical concept IDs live in `meta/CONCEPT_REGISTRY.md` (`EC-CON-001`–`EC-CON-018`); the §8 first-introduction table below uses those Registry IDs.

---

## 2. Research / Source Summary

The following sources were used to test sequencing and prerequisite assumptions. They are cited with the architectural claim each supports. All were fetched/verified in 2026-08.

| # | Source | Institution / Author, date | Architectural claim it supports |
|---|---|---|---|
| R1 | CMU 15-213 *Introduction to Computer Systems* — [official schedule](https://www.cs.cmu.edu/~213/schedule.html) | Carnegie Mellon Univ., current (~2025-26) | The canonical systems-sequence: bits/ints → machine code → linking → memory hierarchy/caches → virtual memory → dynamic memory → processes/exceptional control flow → files → networking → concurrency/synchronization. Validates: (a) bits before assembly; (b) caches/virtual memory before OS processes; (c) processes & files before networking; (d) concurrency near the end, after files/network. |
| R2 | OSTEP — *Operating Systems: Three Easy Pieces*, v1.10, [chapter index](https://pages.cs.wisc.edu/~remzi/OSTEP/) | Arpaci-Dusseau (UW-Madison), Nov 2023 | OS = virtualization (CPU, memory) → concurrency → persistence. Confirms that memory virtualization precedes files/persistence in the standard OS teaching order. Also that OS courses place distributed systems (NFS/AFS) *after* persistence, and security chapters last. |
| R3 | MIT 6.5840 (formerly 6.824) — [schedule](https://pdos.csail.mit.edu/6.824/schedule.html) | MIT PDOS, Spring 2026 | Distributed-systems sequence: threads/RPC first → replication (GFS) → consensus (Paxos, Raft) → consistency (linearizability) → transactions/2PC → sharding (Spanner, chain replication, OCC, memcached) → verification → security. Confirms: (a) concurrency & RPC are *hard prerequisites* to distribution; (b) consensus follows replication; (c) transaction consistency follows consensus; (d) distributed security is a later synthesis. |
| R4 | Nand2Tetris / *The Elements of Computing Systems* — [project sequence](https://www.nand2tetris.org/course) | Noam Nisan & Shimon Schocken, current | Bottom-up construction: Boolean logic → arithmetic → memory → machine language → computer architecture → assembler → VM → parsing → compiler → OS. Confirms: (a) gates & arithmetic precede machine language; (b) machine language precedes assembler/compiler; (c) VM/JVM-style intermediate representations precede high-level language semantic understanding. |
| R5 | Berkeley CS61A→61B→61C — [course descriptions](https://www2.eecs.berkeley.edu/Courses/CS61B/), [prerequisite notes](https://hkn.eecs.berkeley.edu/courseguides/CS/61C) | UC Berkeley | CS61A (programming) is a prerequisite for CS61B (data structures), which is a prerequisite for CS61C (architecture). Supports the claim that data structures & algorithmic thinking are best *before* architecture if the learner must write assembly/C against data structures — but the hard prerequisite is programming ability, not deep algorithms. |
| R6 | CMU 15-445 *Intro to Database Systems* — [schedule & topic list](https://www.cs.cmu.edu/csd/course/15445/s24) | CMU, current | DBMS topics: data models → storage → indexing → query processing → transactions/ACID → recovery/logging → concurrency control. Confirms storage/indexing precedes transactions, and transactions precede recovery in the canonical DB teaching order; and that DBMS internals (buffer pool, B+ trees) are directly downstream of OS virtual memory / storage. |
| R7 | *Designing Data-Intensive Applications* — [full chapter list](https://synchronium.github.io/software-architecture-wiki/sources/designing-data-intensive-applications.html) | Martin Kleppmann, O'Reilly, 2017 | The data-intensiveness order: reliability → data models/queries → storage engines → encoding → replication → partitioning → transactions → distributed systems problems → consistency → batch/stream. Validates: single-node DB (storage, indexing, transactions) before replication/partitioning; and replication/consistency before distributed-system failure models. |
| R8 | Chromium — *Process Model and Site Isolation* (current source doc, [process_model_and_site_isolation.md](https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md)) | Chromium Project, current | A modern browser is a multi-process *OS-for-web-content*: browser process + sandboxed renderer processes + site isolation. This is the canonical case that Web/Browser is the integration point of OS processes + networking + storage + languages/runtime + security confinement. |
| R9 | *How Browsers Work* — [web.dev article](https://web.dev/articles/howbrowserswork) | Tali Garsiel & Paul Irish (Google), last updated 2011 (still primary for parsing/rendering pipeline) | Browser request→DOM→render tree→layout→paint pipeline; HTML parser error-tolerance; CSS cascade/specificity; and the single-threaded main-thread event loop. The 2011 document is explicitly marked partially outdated for current process models (see R8 for the modern multi-process model), so the course must use R8 for process architecture and treat R9's main-flow as a simplified mental model with a stated expiration. |
| R10 | RFC 9000 (QUIC) — [RFC Editor](https://www.rfc-editor.org/rfc/rfc9000.html) | IETF, May 2021 | QUIC is a UDP-based multiplexed and secure transport; HTTP/3 (RFC 9114) maps HTTP semantics over it. Supports positioning QUIC/HTTP-3 as STABLE modern transport reality (not FRONTIER), taught as the current end-state of the transport evolution after TCP/TLS. |
| R11 | Latency numbers (Jeff Dean's list & continuations) — [canonical gist](https://gist.github.com/jboner/2841832) & [2026 interactive update](https://philbogle.github.io/interactive-latency-numbers/) | Jeff Dean (Google), maintained community update 2026 | `L1 ~1ns; L2 ~4ns; L3 ~15ns; RAM ~100ns; NVMe ~100µs; HDD seek ~10ms; network RTT ~10-100ms`. These approximate orders-of-magnitude support the Napkin Math / Estimate competency across the whole course. They are marked **CURRENT** (hardware-dependent) and must be re-verified at review time. |
| R12 | Berkeley CS61C [course notes](https://notes.cs61c.org/) | UC Berkeley, 2026 | Machine architecture as the lens connecting high-level languages, memory hierarchy, and OS support (I/O, interrupts, memory management, process switching). Reinforces the Machine area's role as the bridge between computation and OS. |

**Source limitations stated explicitly:**

- R1, R6, R8, R12 are *current course/document sheets* rather than formal curricula studies; they evidence typical ordering but not pedagogical effect sizes.
- R9 is explicitly self-declared partially out of date (2011) for process architecture. The course must not present its single-process/main-thread model as the current browser architecture (R8 supersedes). The *rendering pipeline* (parse → DOM → render tree → layout → paint) remains essentially stable as of 2026 and is used for that.
- R11's latency numbers are hardware- and workload-dependent. The course teaches them as order-of-magnitude intuition, not exact constants.
- No source was found that establishes the *best* Stage boundary for a part-time adult learner; that remains a learner-validation question (Open Question OQ-1).
- This research validates the *sequence spine* but does not validate the choice of Stage count/names — that is a design judgment, intentionally left for Lead reconciliation.

---

## 3. Proposed Stages

Stage IDs are stable proposal labels (`S1`..`S7`). Each Stage maps the accepted macro areas `00`–`15` (D-007) and is defined by a qualitative capability transition.

### Stage 1 — S1: Foundations of Computation (`00`–`02`)

- **Proposed name:** 计算的底座 — Foundations of Computation
- **Rationale:** The learner already programs; this Stage gives them the representational substrate (what a bit, a byte, an integer really is) and the formal lens (what computation means), before any machine is introduced. This is what makes later "the CPU executes instructions" land as mechanism rather than as assertion.
- **Included macro areas:** 00 The Map; 01 Information & Representation; 02 Computation & Algorithms.
- **Entry assumptions:** Basic programming (variables, loops, functions, can run Python/JS); high-school math (D-002). No formal CS background.
- **Major capability gained:** **Trace & Explain** at the representation level — the learner can state what a number/text/serialized object *is* in memory, estimate sizes, and explain what "big-O" and a data structure really do rather than recite.
- **Stage System Checkpoint idea:** Given a file (e.g., a PNG, a JSON, a UTF-8 text), ask the learner to estimate its byte size, then explain how many bits/bytes a `uint64` or a Unicode code point occupies; then predict/count how many comparisons a given loop performs and justify its complexity. A "representation↔size" and "algorithm cost" checkpoint combined.
- **Exit criteria:** Can (a) convert between representations and explain two's-complement/UTF-8/endianness; (b) estimate sizes and compute time complexity of a simple program; (c) use hashtable/list/tree and state the trade-off; (d) observe a debugger/`gdb`-style state and explain where a variable lives. (No requirement to write a compiler or build a CPU yet.)
- **Why educationally useful:** This Stage removes the biggest hidden-precondition of the whole course: the learner's program has *some* meaning in memory. After it, "the machine interprets instructions" is a logical step, not a new religion.

### Stage 2 — S2: The Machine (`03`–`04`)

- **Proposed name:** 机器 — The Machine (ISA, Execution, Memory Hierarchy, Language→Machine)
- **Rationale:** The machine is the pivot. Here the learner watches source become instructions, an instruction become data movement, and memory become a multi-level hierarchy. This is the canonical "CSAPP moment" (R1): what the CPU actually does with your program.
- **Included macro areas:** 03 Machine; 04 Languages, Runtime & Compiler.
- **Entry assumptions:** Completion of S1 (or equivalent: representation, complexity, data structures) plus basic ability to run a shell (introduced in S1's observe phase) and to read tiny amounts of C/assembly (introduced inside this Stage).
- **Major capability gained:** **Observe & Diagnose** at machine level — the learner can use `objdump`/`gdb`/`strace`-adjacent tools to see what a compiled program does, identify where a variable lives, and diagnose what a segfault/stack overflow actually is.
- **Stage System Checkpoint idea:** Take the learner's small program; have them disassemble a function, predict register/memory behavior, then use `gdb` to confirm; then predict the effect of a cache-locality change on runtime and measure it with `perf stat`/timing.
- **Exit criteria:** Can (a) read simple assembly and explain register/memory/stack/wall-clock; (b) explain the memory hierarchy (levels, sizes, latency) and why cache matters (estimate: one cache miss = ~100 arithmetic ops-scale); (c) explain what a compiler does in broad terms and run a simple disassembly; (d) explain the distinction between stack vs heap lifetime and what a leak/overflow means.
- **Why educationally useful:** Once the learner can predict machine behavior, every higher level (OS, network, DB, browser) becomes a *policy* question over a known mechanism instead of a new black box.

### Stage 3 — S3: The Operating System & Persistence (`05`–`06`)

- **Proposed name:** 操作系统与持久化 — OS: Processes, Memory, Files (with Storage Systems as a direct extension)
- **Rationale:** The OS is the multiplexer that makes one machine serve many programs; storage is what makes data survive. The learner's "program" is finally embedded in an environment with a scheduler, a page table, file descriptors, and a filesystem.
- **Included macro areas:** 05 Operating Systems; 06 Storage Systems.
- **Entry assumptions:** S2, plus enough multi-file/programming maturity to write small C/Python programs that use syscalls (open/read/write/fork/exec). No requirement to write a full kernel.
- **Major capability gained:** **Trace & Diagnose** across the process/memory/files boundary — the learner can follow a syscall, explain process vs thread, read a page table conceptually, and diagnose a file I/O or memory issue with real tools.
- **Stage System Checkpoint idea:** Use `strace`, `pstree`/`ps`, `/proc`, and filesystem tools to answer: "when my Python program reads a file, what syscalls happen, where does the data live at each step (page cache → filesystem → block device), and what happens if I lose power?"
- **Exit criteria:** Can (a) explain process vs thread, virtual memory, page table, and why isolation matters; (b) explain filesystems (directories, inode-like structure, POSIX-like API) at a mechanism level and trace a read; (c) explain why an SSD differs from an HDD and what durability means; (d) use `strace`/`dmesg`-family tools to *diagnose* a real system-level issue; (e) estimate storage/IO latency and cost.
- **Why educationally useful:** This Stage answers the "where is the data going?" question for a single machine. Without it, the later "which machine / what network" questions have no baseline.

### Stage 4 — S4: Networking & the Web (`07`–`08`)

- **Proposed name:** 网络与浏览器 — Networking, the Web, and the Browser as an Integrated System Case
- **Rationale:** A request from a browser to a server is the canonical modern end-to-end trace. With OS + storage under the belt, the learner can now attribute each delay/hop to a real mechanism (DNS, TCP handshake, TLS, cache hit/miss, web proxy, CDN), and the Browser becomes the case that *integrates* the previous pieces.
- **Included macro areas:** 07 Networking; 08 Web & Browser Platform.
- **Entry assumptions:** S3 (processes, files, syscalls) and S1/S2 fundamentals. Ability to run a shell, a simple HTTP server, and read tiny HTTP headers.
- **Major capability gained:** **Trace & Explain** an end-to-end request; **Estimate** network latency/bandwidth/cost.
- **Stage System Checkpoint idea:** The learner instruments a real browser page load (Chrome DevTools/network panel + `curl` + a local server), traces `DNS → TCP → TLS → HTTP → render`, and explains/measures where time goes; then quantifies the cost of a cache miss / extra round trip / too-large asset.
- **Exit criteria:** Can (a) explain IP/DNS/TCP or QUIC/TLS/HTTP and their failure modes; (b) run a real HTTP request through a proxy and trace it; (c) explain what a browser does on load (parse, DOM, render, lay out, paint) and the modern multi-process/site-isolation reality (R8); (d) explain request/response caching, CSP, CORS as interactive mechanisms; (e) estimate end-to-end latency from components.
- **Why educationally useful:** The browser is where the majority of learners meet all prior concepts *at once* — it is the highest-value integration case available without leaving the single-system world. It must not become web-development training (D-006): the goal is mechanism literacy, not framework fluency.

### Stage 5 — S5: Data, Consistency & Concurrency (`09`–`10`)

- **Proposed name:** 数据与并发 — Databases, Transactions, and Concurrency
- **Rationale:** With network + browser complete, persistence and concurrency become the two hard mysteries: "why is my data in two places inconsistent?" and "why does my program sometimes do the wrong thing?" Both are answered with a shared toolbox (atomicity, isolation, ordering, locks, invariants) that the later distributed Stage will reuse.
- **Included macro areas:** 09 Databases; 10 Concurrency.
- **Entry assumptions:** S4 (or S3 if the learner takes the DB-before-browser branch — see Dependency Graph note). Filesystem/OS model from S3 is required.
- **Major capability gained:** **Correctness & Judge** at the data/concurrency level — the learner can state a transaction's invariants, explain an isolation level, and diagnose a data race.
- **Stage System Checkpoint idea:** The learner operates a real DB (SQLite/Postgres) and a real concurrent Python program: predicts an anomaly (dirty read / lost update / race), makes it happen, then explains the isolation mechanism that fixes it; then uses `strace`/`pg_stat`-style tools to see where locking happens.
- **Exit criteria:** Can (a) explain B-tree indexes, storage engine basics, query planning in broad strokes, and write structured SQL; (b) state ACID, explain isolation levels and their trade-off with performance; (c) explain threads vs processes, a lock, an atomic operation, and what idempotency means; (d) diagnose a race in a small program and justify the fix; (e) estimate storage/DB cost at different scales.
- **Why educationally useful:** Concurrency and consistency are the *single most common source of production bugs* and the bridge from single-system to distributed. Teaching them here (with a real DB) gives the later distributed Stage a concrete, owned set of concepts to reuse.

### Stage 6 — S6: Distributed Systems & Modern Infrastructure (`11`–`12`)

- **Proposed name:** 分布式系统与现代基础设施 — Distributed Systems, Cloud, and Infrastructure Engineering
- **Rationale:** The learner now has the single-system and the concurrency/transaction tools. This Stage extends them across machines: partial failure, replication, consensus, consistency, queues, and the container/cloud/deployment layer that makes modern operation real.
- **Included macro areas:** 11 Distributed Systems; 12 Modern Infrastructure.
- **Entry assumptions:** S5. Also a comfortable base in S3 (processes) and S4 (network) applied across machines.
- **Major capability gained:** **Judge & Estimate** at scale — the learner can reason about partial failure, choose between replication/consistency models, and explain why a cloud deployment fails the way it does.
- **Stage System Checkpoint idea:** The learner runs a small replicated service (e.g., a demo KV store with 3 replicas via a course-provided lab, or an adapted classic), kills a replica/partition, and explains the consistency state they observe; then estimates the cost/availability trade-off of a chosen replication factor.
- **Exit criteria:** Can (a) explain partial failure, retries, idempotency, and chaos-style failure intuition; (b) explain replication (async/sync), consensus (Raft/Paxos), consistency models (linearizability ↔ eventual), and the CAP-style trade-off; (c) explain queues, message brokers, and at-least/at-most/exactly-once semantics; (d) explain containers/virtualization/cloud deployment and observability (metrics/traces/logs) well enough to diagnose an infrastructure-level problem; (e) estimate availability, cost, and performance of a distributed design.
- **Why educationally useful:** This is where "the internet" stops being a black box and becomes a composition of policies with failure modes — the core of modern systems judgment (D-001).

### Stage 7 — S7: Security Synthesis, Systems Thinking & Final Defense (`13`–`15`)

- **Proposed name:** 安全综合与系统判断 — Security Synthesis, Systems Thinking & Judgment, Final Defense
- **Rationale:** The final Stage deliberately *revisits* the whole spine through the security lens (trust boundaries, crypto *use*, authn/authz, secure composition), then synthesizes the entire curriculum into judgment questions (measurement, cost, failure, technology evaluation) and the System Defense.
- **Included macro areas:** 13 Security Synthesis; 14 Systems Thinking & Judgment; 15 Final System Defense.
- **Entry assumptions:** S6 (or S4/S5-complete in a compressed path — see Dependency Graph). The learner must be able to connect the full chain before specializing.
- **Major capability gained:** **Judge & Learn-New-Tech** at the whole-system level — the learner can evaluate a technology/architecture against the Technology Evaluation Framework (D-015) and defend a real design decision.
- **Stage System Checkpoint idea:** A "technology evaluation case" exercise: given a real (possibly unreal) system scenario, the learner uses the Technology Card structure (Problem → Mechanism → Gains → Costs → Failure → When-not-to-use → Stable Principle) to evaluate and defend a choice; plus a security *review* of a small course-owned vulnerable app (safe target).
- **Exit criteria:** Can (a) identify a trust boundary and state what must be true for the system to remain secure; (b) explain where/when to use crypto primitives (not implement them); (c) explain authn/authz and common composition failures (SQL-i, XSS, SSRF, CSRF, insecure deserialization, supply chain); (d) run the Technology Evaluation Framework on a familiar technology and defend the judgment; (e) produce a coherent System Defense of a Mini Cloud App architecture with trade-off reasoning.
- **Why educationally useful:** The curriculum's highest goal is *judgment* (Invariant 1). This Stage converts accumulated mechanism knowledge into a defensible, transferable judgment capability and explicitly re-teaches nothing — it reuses everything.

**Stage mapping table (Macro areas → Stages):**

| Macro area (D-007) | Stage |
|---|---|
| 00 The Map | S1 |
| 01 Information & Representation | S1 |
| 02 Computation & Algorithms | S1 |
| 03 Machine | S2 |
| 04 Languages, Runtime & Compiler | S2 |
| 05 Operating Systems | S3 |
| 06 Storage Systems | S3 |
| 07 Networking | S4 |
| 08 Web & Browser Platform | S4 |
| 09 Databases | S5 |
| 10 Concurrency | S5 |
| 11 Distributed Systems | S6 |
| 12 Modern Infrastructure | S6 |
| 13 Security Synthesis | S7 |
| 14 Systems Thinking & Judgment | S7 |
| 15 Final System Defense | S7 |

**Stage dependency (corrected — Issue #9 keeps the Lead-fixed semantics):**

```
S1 → S2 → S3
           ├─→ S4 ─┐
           └─→ S5 ─┴─→ S6 → S7
```

- **Hard prerequisites:** `S1 → S2 → S3`; `S3 → S4` and `S3 → S5` (each Stage's capability is a genuine prerequisite for the next Stage it must feed); `S4 & S5 → S6` (distributed systems needs both the networking path and the data/concurrency path); `S6 → S7`.
- **S4 / S5 are partially independent after S3.** There is **no hard `S4 → S5` Stage edge**.
- **Default first-time learner narrative (pedagogical preference, not `H`):** `S1 → S2 → S3 → S4 → S5 → S6 → S7` (request-centric journey). A state-centric learner may run `S1 → S2 → S3 → S5 → S4 → S6 → S7`; a compressed branch may not skip S4 or S5 entirely before S6.
- The **Module DAG** (`dependency-graph-v0.1.md`) remains authoritative for actual prerequisite semantics; the narrative choice is recorded under OQ-BP-004 as resolved (preference, not dependency).

---

## 4. Detailed Module Map

Module IDs are proposal labels (`M00`..`M30`), each mapped to a macro area and a Stage. Within a Stage, Modules are ordered; cross-Stage ordering follows the dependency chain.

### S1 · M00 — The Map & How Computing Systems Connect (Area 00)
- **Purpose / mental-model contribution:** The learner's first whole-system map: a request goes through layers (client → network → server → storage), and abstractions hide mechanisms. Establish the "where is the time going / data going / state / failure" question set (Technology Evaluation Framework course questions).
- **Prerequisites:** Entry-level programming; none of this course.
- **Key concepts:** system map (whole system mental model); abstraction; interface; indirection; state; Mini Cloud App as recurring integration surface (placeholder only).
- **Competencies:** Trace (first), Explain (first), Observe (first use of a real tool).
- **Horizontal threads first introduced/revisited:** Technical Literacy (FIRST-INTRO); API/Interface Design (FIRST-INTRO); Napkin Math (FIRST-INTRO — order of magnitude); Failure (FIRST-INTRO — "systems fail"); Debugging (FIRST-INTRO — what debugging is).
- **Reconciled explicit learner outcomes (R2 toolchain, Issue #9):** `L00-02` must produce observable outcomes — shell/task execution; reading an unfamiliar code/file; debugger-light investigation; Git evidence; reproducibility/version/environment record; running a baseline and preserving evidence. The minimal form is one reproducible investigation: read an unfamiliar file → run a command → controlled change → record it in Git → run it → save an environment/version/evidence record. Not a command encyclopedia. A REQUIRED-lab entry gate (get repository, run documented preflight check, reproduce baseline, save evidence record; environment preflight repeated at M03/M06/M13) may reference these abilities but is course discipline, **not** a DAG edge and not a new Module.
- **Likely hands-on mechanism class:** Observe a real HTTP request against a local demo service; use a shell; break the service and observe the failure.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any production system reading.
- **Core vs Deep Dive boundary:** Deep Dive: system-design interview prep, architecture pattern catalogs.

### S1 · M01 — Bits, Bytes & Representation (Area 01)
- **Purpose / mental-model contribution:** What a `1` and a `0` are; how integers, text (UTF-8), and binary files are represented; endianness; serialization; size estimation. This is the substrate of everything later.
- **Prerequisites:** M00.
- **Key concepts:** bit, byte, binary, two's-complement, unsigned/signed, character encoding (UTF-8), serialization, endianness, base conversion; size in bytes.
- **Competencies:** Trace (bits through representation), Explain (representation), Estimate (byte sizes), Correctness (invariant: representation must be unambiguous).
- **Horizontal threads:** Correctness & Invariants (FIRST-INTRO — representation must round-trip); Technical Literacy (revisit); Napkin Math (revisit — size estimates).
- **Likely hands-on mechanism class:** Use Python (`struct`, `bytes`, `int.to_bytes`) and real binary files; observe hexdump; break a serialization and watch it fail.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** data formats, wire protocols, file parsing, security (integer overflow).
- **Core vs Deep Dive:** Deep Dive: floating-point deep dive, arbitrary precision, compression theory (LZ/entropy).

### S1 · M02 — Computation & Complexity (Area 02)
- **Purpose / mental-model contribution:** What "computation" is conceptually (a function/algorithm), abstraction of operations, complexity as *growth*, and the standard containers (array/list/hash/stack/queue/tree) with their trade-offs.
- **Prerequisites:** M01 (or at least integer/representation basics).
- **Key concepts:** algorithm, complexity, big-O, data structures (array, hash table, linked list, stack/queue, tree), recursion; state/specification; intuitive model of computation; tractability/limits intuition.
- **Competencies:** Trace (data structure operations), Explain, Estimate (operation counts), Correctness (invariants of a data structure).
- **Reconciled outcomes (R1 + R9, Issue #9):** `L02-01` explicitly owns the just-in-time applied discrete/asymptotic toolkit — counting, asymptotic growth, order-of-magnitude scheduling — and `L02-03` protects the **intuitive** model of computation (what a computation/algorithm is), **expression limits** (what "expressible/representable" means), **tractability** (why some problems are hard), and a **decidability intuition** (some questions are not answerable this way). The algorithm ↔ language/runtime connection is established here and confirmed at M05 (`L05-01..03`): representing a problem correctly then stating how a representation or language choice changes cost or expressibility. Formal automata theory, reductions, computability proofs stay Deep Dive. No math prerequisite gate before M01.
- **Horizontal threads:** Correctness & Invariants (revisit — loop invariants); Napkin Math (revisit); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** Implement a small data structure or measure a sort on inputs of different sizes; observe scaling behavior; use a profiler-light timing.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any programming, algorithm choice, interview/fundamentals.
- **Core vs Deep Dive:** Deep Dive: graph algorithms, advanced algorithmic design (DP, NP-completeness theory).

### S2 · M03 — Machine: ISA & Execution (Area 03)
- **Purpose / mental-model contribution:** The CPU executes instructions; registers, stack, heap, call frame; memory addressing; the fetch-decode-execute loop conceptually; what `main`→`call`→`return` really does.
- **Prerequisites:** M01 (representation), M02 (basic complexity), and the ability to read tiny C (introduced here; D-008 minimal C).
- **Key concepts:** ISA; register; instruction; stack frame; program counter; memory/address; assembly (basic); `objdump`; syscall (preview); endianness (revisit).
- **Competencies:** Trace (instruction/control flow), Observe (`objdump`/`gdb`), Explain, Diagnose (segfault/stack overflow).
- **Horizontal threads:** Failure (revisit — crash as signal); Debugging (FIRST-INTRO — using gdb); Technical Literacy (revisit); API/Interface Design (revisit — ABI as interface).
- **Likely hands-on mechanism class:** Disassemble a tiny C function (real); `gdb` step-through; induce a stack overflow and observe; optional CPU simulator only where hardware is unavailable.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** debugging, crash analysis, performance, security (buffer overflow).
- **Core vs Deep Dive:** Deep Dive: logic gates → ALU → Verilog-level CPU design; branch prediction; pipelining. (Nand2Tetris optional core-adjacent excursion.)

### S2 · M04 — Memory Hierarchy & Locality (Area 03)
- **Purpose / mental-model contribution:** Memory isn't one thing: cache (L1/L2/L3) → RAM → disk; latency ladder; locality; why a reordered loop or a contiguous array is dramatically faster.
- **Prerequisites:** M03 (machine basics), M01 (sizes/units).
- **Key concepts:** memory hierarchy, cache, locality, cache line, latency ladder, RAM vs storage, spatial/temporal locality, performance measurement; measured variation: repeated measurements, distributions, median/percentiles when useful, uncertainty/variation, inference limits.
- **Competencies:** Observe (perf stat / timing), Diagnose (cache-miss-bound performance), Estimate (hierarchy latency trade-off), Explain (why cache works).
- **Reconciled first home (R1 + R7, Issue #9):** `L04-02` is the canonical first assessed home of the **applied measurement-uncertainty toolkit** (repeated measurements; distributions; median; percentiles when useful; uncertainty/variation; inference limits; order-of-magnitude reasoning) and of the **experimental pattern**: question/hypothesis → baseline → controlled change → metric/environment/workload → repetitions/distribution when relevant → observation → competing explanation → bounded conclusion. Reliability/failure probability stays just-in-time (M16/M17) where a mechanism requires it. No standalone mathematics Module; no statistics sequence; no math gate.
- **Horizontal threads:** Measurement & Performance (FIRST-INTRO — a real measured difference); Napkin Math (revisit — 100 ns vs 1 ms); Correctness (revisit — cache coherence intuition); Cost/Resource Economics (revisit).
- **Likely hands-on mechanism class:** Cache-blocking / array-of-structs vs struct-of-arrays timing measurement; `perf` if available; memory-latency microbenchmark.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any performance work, data layout, system design.
- **Core vs Deep Dive:** Deep Dive: cache coherence protocols, cache-set-associativity math, SIMD/vectorization.

### S2 · M05 — Languages, VM & Compiler Pipeline (Area 04)
- **Purpose / mental-model contribution:** Source → tokens → AST → IR → machine code; what an interpreter/runtime (Python/JVM/JS engine) actually does; the gap between "language" and "machine". Establish that a language is a *convention for an interface*, and a compiler/runtime is a *translation* with choices.
- **Prerequisites:** M03 (machine), M04 (memory), M02 (basic).
- **Key concepts:** lexer/parser/AST (per R9/R4), intermediate representation, compiler, interpreter, runtime (GC, JIT, event loop), ABI, source mapping; closure (concept-level).
- **Competencies:** Trace (source → machine), Explain (compilation), Learn-New-Tech (read a language/compiler behavior), Observe (disassembly of a higher-level language).
- **Reconciled outcome (R9, Issue #9):** the algorithm ↔ language/runtime connection established in M02 is confirmed here — how a source-level construct becomes a representation, a runtime mechanism, and a machine instruction; a language construct's cost/expressibility consequences. Exit evidence is a source-to-runtime trace and one verified language/runtime claim (from documentation or source), not parser vocabulary recall. Formal type theory, GC internals, and compiler construction remain Deep Dive. Guardrail: no vocabulary-only assessment (matches #15 §3.1).
- **Horizontal threads:** API/Interface Design (revisit — language/runtime interface); Correctness (revisit — type systems as invariants); Debugging (revisit — stack traces, symbols); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** Compile (or use a real compiler for) a tiny program and inspect the pipeline; use Python `dis` or a small interpreter-writing exercise; optional simple tokenizer/parser with a course skeleton.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any language choice, JIT/GC behavior, framework internals.
- **Core vs Deep Dive:** Deep Dive: full compiler design (Nand2Tetris Part II), type-system theory, GC internals, JIT compilation.

### S3 · M06 — Processes, Syscalls & Execution Context (Area 05)
- **Purpose / mental-model contribution:** The OS is the multiplexer. What a process is, how a program becomes a running process, syscalls as the OS API, fork/exec, process isolation, and simple scheduling intuition.
- **Prerequisites:** M03, M05 (or at least M03) + ability to compile tiny C.
- **Key concepts:** process; syscall; kernel/user mode; process table; fork/exec; PCB; exit status; scheduling (round-robin priority intuition); signals (light).
- **Competencies:** Trace (syscall path), Observe (strace/ps/pstree), Diagnose (zombie/exit/block), Explain.
- **Horizontal threads:** Failure (revisit — crash, exit codes); Debugging (revisit — strace); API/Interface Design (revisit — syscall as interface); Software Engineering (FIRST-INTRO — process structuring); Correctness (revisit).
- **Likely hands-on mechanism class:** `fork()`/`exec()` demo; `strace` a real command; `ps`/`/proc` observation.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** server management, containerization, debugging.
- **Core vs Deep Dive:** Deep Dive: scheduler internals, kernel module development, real-time scheduling.

### S3 · M07 — Virtual Memory & Isolation (Area 05)
- **Purpose / mental-model contribution:** Every process has its own address space; the page table is the mechanism; virtual memory is why isolation, sharing, and memory-mapped files work; plus dynamic memory (heap) and allocation failure.
- **Prerequisites:** M04 (memory hierarchy), M06 (processes), M03 (machine).
- **Key concepts:** virtual memory, address space, page table, page fault, TLB, memory-mapped file, malloc/heap, out-of-memory, copy-on-write (light); **trust boundary** as the first concrete security-boundary concept, explicitly distinguished from isolation.
- **Competencies:** Trace (address → physical), Explain (isolation/security of memory), Diagnose (OOM/segfault), Estimate (memory needs).
- **Horizontal threads:** Security (FIRST-INTRO — memory isolation as the first concrete protection boundary; define **trust boundary** here and state that isolation boundary ≠ trust boundary by default); Correctness (revisit); Debugging (revisit); Cost (revisit — memory as resource).
- **Likely hands-on mechanism class:** `/proc/<pid>/maps`; observe a growing process; `valgrind`/ASan for heap errors; memory-limit demo.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** memory tuning, container limits, security exploits.
- **Core vs Deep Dive:** Deep Dive: full page-table implementation, swap/paging policies, hardware TLB details.

### S3 · M08 — Files, Filesystems & System I/O (Area 05/06)
- **Purpose / mental-model contribution:** The file interface (POSIX-like: open/read/write/close, directory, inode), how a filesystem organizes blocks, and how syscalls meet storage.
- **Prerequisites:** M06 (processes/syscalls), M07 (memory).
- **Key concepts:** file; fd; directory; inode; path; mount; metadata; permissions; buffered I/O; page cache; block device (mechanism-level); special files (/dev, pipes).
- **Competencies:** Trace (read path), Explain (filesystem), Diagnose (I/O error, permission, disk full), Observe (strace file ops).
- **Horizontal threads:** API/Interface Design (revisit — file interface); Correctness (revisit — file state invariant); Failure (revisit — I/O failure); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** `strace` a file read; create a small filesystem image or inspect `dd`/`debugfs`-style structures; observe page cache with `vmstat`.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any file-backed code, config management, containers.
- **Core vs Deep Dive:** Deep Dive: journaling internals, FFS/ext4 on-disk structures, FUSE.

### S3 · M09 — Storage Engine & Durable Storage (Area 06)
- **Purpose / mental-model contribution:** What "durable" means; the mechanics of HDD vs SSD vs object storage; write amplification; filesystem journaling/durability trade-off; and why crashes lose data.
- **Prerequisites:** M08 (files), M04 (memory hierarchy, re-used for latency ladder), M01.
- **Key concepts:** durability, fsync/barrier, write-ahead log (concept), HDD vs SSD (seek/erase, wear leveling), storage cost/latency ladder; object storage vs block vs file; RAID concept (brief).
- **Competencies:** Judge (durability trade-off), Estimate (storage latency/cost), Explain, Diagnose (data-loss scenario).
- **Horizontal threads:** Failure (revisit — data-loss failure model); Cost / Resource Economics (FIRST-INTRO — storage cost per GB); Correctness (revisit — durability invariant); Measurement (revisit).
- **Likely hands-on mechanism class:** measure fsync vs no-fsync under a kill/power-loss simulation (safe, local); compare SSD vs HDD-like behavior on the course VM; inspect an object store endpoint.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** backups, database durability, cloud storage costs.
- **Core vs Deep Dive:** Deep Dive: RAID internals, FTL/switching (SSD), erasure coding, log-structured storage.

### S4 · M10 — Networking I: IP, DNS & Transport (Area 07)
- **Purpose / mental-model contribution:** How packets cross the world; IP addressing/routing; DNS; TCP (reliability, handshake, congestion intuition) and UDP; TCP vs UDP trade-off; sockets API.
- **Prerequisites:** M06 (processes), M08 (I/O), M09 (storage — used for latency ladder), basic network literacy from everyday use.
- **Key concepts:** IP; subnet (light); routing; DNS; packet; port; TCP (3-way handshake, segments, retransmission, flow/congestion light); UDP; socket; LOCALHOST.
- **Competencies:** Trace (request → socket → network), Observe (`ss`/`tcpdump`-light/`nc`), Diagnose (timeout/connection-refused), Estimate (RTT, bandwidth-delay product light).
- **Horizontal threads:** Failure (revisit — network failure modes); Measurement (revisit — RTT); API/Interface Design (revisit — sockets); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** run a local TCP/UDP server/client; `ss`, `nc`, `traceroute`; observe TCP handshake in a packet trace (local).
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any client/server, debugging, firewall/DNS issues.
- **Core vs Deep Dive:** Deep Dive: congestion control, network QoS, BGP/global routing, packet-sniffing tools beyond `tcpdump` basics.

### S4 · M11 — Networking II: TLS, HTTP, CDN & Proxies (Area 07)
- **Purpose / mental-model contribution:** What makes a network channel *authenticated/encrypted*; the HTTP request-response model; caching; proxies/CDNs; headers; and the transport evolution TCP → TLS → QUIC/HTTP-3.
- **Prerequisites:** M10 (transport), M05 (runtime), M07 (isolation).
- **Key concepts:** TLS (handshake concept, cert/CA, encryption-in- transit), HTTP request/response (methods, status, headers), caching (ETag/Last-Modified), proxy, CDN, HTTP/2 vs HTTP/3 (QUIC), WebSocket (brief).
- **Competencies:** Trace (request through proxy/cache), Judge (cache vs no-cache, HTTP version choice), Explain, Observe (`curl -v`, browser network panel).
- **Horizontal threads:** Security (revisit — TLS as transport security, cert verification); Measurement (revisit — time-to-first-byte); API/Interface Design (revisit — HTTP as API surface); Privacy/Data Responsibility (FIRST-INTRO — data in transit, cookies).
- **Likely hands-on mechanism class:** `curl -v` and browser DevTools trace a real page; run a local proxy or use an HTTPS endpoint; observe caching headers with a local cache; break an HTTPS handshake (course-safe, local).
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** web APIs, debugging 40x/50x, front-end performance.
- **Core vs Deep Dive:** Deep Dive: TLS 1.3 internals, certificate pinning, CDN internals, HTTP/3 stream scheduling.

### S4 · M12 — Web & Browser: The Integrated Case (Area 08)
- **Purpose / mental-model contribution:** A browser is a multi-process OS-for-web-content (R8): browser process, sandboxed renderers, networking, storage, rendering pipeline (parse→DOM→render→layout→paint per R9), JS runtime/event loop, and the security model (origin, CORS, CSP, same-origin policy). This is the integration case — never web-dev training (D-006).
- **Prerequisites:** M10/M11 (network), M05 (runtime), M07 (isolation), M02 (data structures).
- **Key concepts:** browser process architecture; renderer/site isolation; DOM; rendering pipeline; event loop; origin/same-origin policy; CORS; CSP; cookies/storage (localStorage, IndexedDB); performance API (navigation timing).
- **Competencies:** Trace (a page load across processes), Observe (DevTools, performance panel), Diagnose (render-blocking JS, script order), Explain (browser security model), Judge (web platform trade-offs).
- **Horizontal threads:** Security (revisit — same-origin, CORS, CSP); Concurrency (FIRST-INTRO preview — event loop); Observability/Measurement (revisit — navigation timing); Software Engineering (revisit — JS module practices light); Privacy (revisit — third-party cookies).
- **Likely hands-on mechanism class:** DevTools Performance/Network panels; run a local page and observe render blocking; inspect `chrome://process-internals` behavior conceptually; simple JS event-loop demo; break a CORS request and explain.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any web app work, browser debugging, web security.
- **Core vs Deep Dive:** Deep Dive: CSS layout internals (Flex/Grid), web performance budgets, rendering engine source expeditions.

### S5 · M13 — Databases: Storage & Indexing (Area 09)
- **Purpose / mental-model contribution:** What a database actually is under the hood: pages, B-tree indexes, heap/log storage, buffer pool; the relational model and SQL; why indexes speed reads and slow writes.
- **Prerequisites:** M08/M09 (files/storage), M04 (memory hierarchy), M02 (data structures).
- **Key concepts:** DBMS; relational model; SQL; page; heap; B-tree/B+ tree; hash index; buffer pool; query planner (concept); storage engine (row vs column); schema invariant; source-of-truth vs derived data.
- **Competencies:** Explain (index mechanism), Observe (`EXPLAIN`/`EXPLAIN QUERY PLAN`), Judge (index trade-off), Estimate (page/IO cost), Trace (query → index → page).
- **Reconciled first home (R6, Issue #9):** `L13-03` extends the schema-invariant lesson to protect: **schema evolution** (changing fields/constraints over time), **reader/writer compatibility** (old readers vs new writers and vice versa), **migration/backfill trade-offs** (delay, downtime, complexity — migrate only when there is a real evolution need), **source-of-truth vs derived data** (one authoritative copy; derived data is recomputable), and **lightweight provenance** (where the value came from, which version/assumptions shaped it — PROV-DM as conceptual vocabulary only). Representation/model distinction rides on M01 `L01-04` + M13 `L13-02`; compatibility revisits at M16 `L16-02`; derived data at M18; provenance at M19/M23. Bounded carefully: one evolving schema, one derived view, one provenance record — **not** schema-registry operations, not Data Engineering, no PROV ontology, no lineage platform, no NoSQL family survey.
- **Horizontal threads:** Measurement (revisit — query timing); Correctness (revisit — schema invariants); API/Interface Design (revisit — SQL as interface); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** operate a real Postgres/SQLite; `EXPLAIN` a query; create/drop indexes and measure; observe buffer cache activity.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any data work, ORM debugging, schema design.
- **Core vs Deep Dive:** Deep Dive: custom B-tree implementation, columnar/LSM engines, vector indexing.

### S5 · M14 — Databases: Transactions, Recovery & Isolation (Area 09)
- **Purpose / mental-model contribution:** ACID; atomicity via write-ahead log; isolation levels and which anomalies each prevents; locking vs MVCC; what "durable" commits; and the trade-off between isolation and concurrency.
- **Prerequisites:** M13 (storage/indexing), M09 (durability), M15-concurrency preview (or taught with it).
- **Key concepts:** transaction; ACID; WAL; commit; isolation levels (read uncommitted → serializable); anomaly (dirty read, lost update, skew); MVCC (concept); locks; deadlock (light); idempotency (preview).
- **Competencies:** Correctness (state transaction invariants), Judge (isolation trade-off), Diagnose (anomaly in a concurrent run), Explain.
- **Horizontal threads:** Correctness & Invariants (revisit — transaction invariants); Concurrency (FIRST-INTRO — as DB isolation); Failure (revisit — crash recovery); Measurement (revisit — isolation vs throughput).
- **Likely hands-on mechanism class:** run concurrent transactions in Postgres/SQLite; cause a lost update / dirty read; observe locking; kill a transaction mid-flight and recover; map to WAL.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** payment/booking systems, any multi-step write, accounting.
- **Core vs Deep Dive:** Deep Dive: MVCC internals, serializable snapshot isolation, distributed transactions.

### S5 · M15 — Concurrency: Threads, Races & Synchronization (Area 10)
- **Purpose / mental-model contribution:** Why parallel code is hard: threads, shared state, races, atomicity, locks, condition variables, deadlock; and the async/event-loop alternative (from M12's event loop).
- **Prerequisites:** M06 (processes), M03 (machine), M14 (as motivating case: DB isolation), M05 (runtime).
- **Key concepts:** thread; race condition; atomicity; mutex; condition variable; deadlock (light); semaphore (concept); shared vs concurrent; GIL (as Python reality); async/await/event loop (revisit).
- **Competencies:** Correctness (specify a thread-safe invariant), Diagnose (find a race), Explain (locking semantics), Judge (lock vs async).
- **Horizontal threads:** Concurrency (FIRST-INTRO as a *coherent* topic — with M14); Correctness (revisit); Failure (revisit — race as deadly subtle bug); Measurement (revisit — scaling); Debugging (revisit — race detectors, `pytest`-with-threads stress).
- **Likely hands-on mechanism class:** write a threaded counter with a race, observe it misbehave, fix with a lock, then use a race detector / stress test; compare to an async solution.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any backend, any multi-threaded service, async code.
- **Core vs Deep Dive:** Deep Dive: lock-free programming, memory models, transactional memory, futex internals.

### S6 · M16 — Distributed Systems Foundations: Partial Failure & RPC (Area 11)
- **Purpose / mental-model contribution:** The defining constraint: machines fail independently; you cannot know both "is it done?" and "did it succeed?" — hence retries, timeouts, idempotency, at-least-once. RPC as the distributed function-call abstraction.
- **Prerequisites:** M15 (concurrency), M10/M11 (network), M05 (runtime), M14 (transactions as motivating case).
- **Key concepts:** partial failure; timeout; retry; idempotency; distributed semantics; RPC (concept + a real framework); network partition; ambiguity of failure (unavailable vs slow).
- **Competencies:** Trace (a distributed call), Judge (retry/idempotency design), Explain (why failure is fundamental), Estimate (availability math).
- **Horizontal threads:** Failure (FIRST-INTRO at scale — partial failure); Correctness (revisit — idempotency as invariant); Debugging (revisit — distributed tracing); Measurement (revisit — timeouts); Software Engineering (revisit).
- **Likely hands-on mechanism class:** run a two-process RPC (gRPC/Thrift or Python) with an injected network delay/partition; observe retries/timeouts; explain idempotency with a course-safe demo.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** microservices, API calls, third-party service failures.
- **Core vs Deep Dive:** Deep Dive: distributed consensus detail, fault-tolerant RPC research.

### S6 · M17 — Replication, Consistency & Consensus (Area 11)
- **Purpose / mental-model contribution:** Replication for availability/durability; consistency models (strong ↔ eventual, linearizability); consensus (Raft/Paxos intuitive); why "CAP" is a trade-off framing, not a law (R3, R7).
- **Prerequisites:** M16 (partial failure/RPC), M14 (transactions), M09 (durability).
- **Key concepts:** replication (sync/async, leader/follower); consistency (linearizability ↔ eventual); quorum; consensus (Raft/Paxos intuitive); split brain; availability vs consistency trade-off.
- **Competencies:** Judge (choose consistency model), Explain (consensus mechanism), Diagnose (a replication anomaly), Estimate (availability/cost).
- **Reconciled boundary (R10/R11, Issue #9):** consensus **concept** is Core here: why coordination is hard, what consensus buys/costs, when replication/consistency choices apply. No full Raft/Paxos implementation is required for M17 exit. The accepted hands-on boundary is **bounded observation/case** — Source Expedition EXP-05 (replication/transactions/logging case) and the SQLite transaction/recovery evidence (LAB-REQ-05) as the local-scale analogue; full consensus implementation/proofs are Deep Dive (R11). No Registry ID for Consensus in the first population (deferred explicitly; concept stays Core at M17).
- **Horizontal threads:** Correctness (revisit — replicated invariants); Failure (revisit — partition); Concurrency (revisit — ordering); Cost (revisit — replication cost).
- **Likely hands-on mechanism class:** bounded state/message/failure traces plus the accepted `EXP-05` Source Expedition; optionally observe a rights-cleared/local replication case later if a Module Dossier justifies it. No required 3-node service and no Raft/Paxos implementation in Core.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** etcd/ZooKeeper/consensus-based stores; databases.
- **Core vs Deep Dive:** Deep Dive: full Raft implementation, Byzantine fault tolerance, distributed storage research.

### S6 · M18 — Distributed State & Coordination (Area 11)
- **Purpose / mental-model contribution:** Queues, brokers, and coordination services; exactly-once semantics and their limits; distributed transactions/2PC (concept) and why they are used sparingly; event sourcing/streams as a consistency pattern.
- **Prerequisites:** M17 (consensus/consistency), M14 (transactions), M16.
- **Key concepts:** queue; broker; at-least/at-most/exactly-once; saga (light); 2PC (concept); distributed lock (light); stream/event log; ordering.
- **Competencies:** Judge (choose sync call vs durable job table vs queue), Explain (delivery-semantics limits), Diagnose (duplicate/out-of-order processing), Observe (bounded local delivery evidence without requiring a specific broker product).
- **Horizontal threads:** Concurrency (revisit — ordering), Failure (revisit — duplicate delivery), Cost (revisit — broker cost), Software Engineering (revisit).
- **Likely hands-on mechanism class:** bounded local duplicate-delivery/idempotency case using the simplest mechanism that preserves the lesson (for example a course-owned durable job-table/queue fixture). A broker may appear only as a replaceable Current Case; Kafka/Redis or any specific broker is not a Core prerequisite.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** event-driven systems, workflows, outbox patterns.
- **Core vs Deep Dive:** Deep Dive: exactly-once frameworks, event sourcing internals, consensus protocols beyond RAFT.

### S6 · M19 — Infrastructure: Containers, Virtualization & Deployment (Area 12)
- **Purpose / mental-model contribution:** The modern runtime environment of production code: containers as OS-level virtualization (namespaces + cgroups), VMs, images, registries, and the deployment/CI/CD pipeline; what "the cloud" actually does and what it costs.
- **Prerequisites:** M06/M07 (processes/memory), M08 (files), M16 (partial failure) — infra needs the failure model.
- **Key concepts:** container; image; namespaces; cgroups; Docker/OCI (as case); VM vs container; cloud/region/AZ/availability zone; deployment (rolling, blue-green, canary); CI/CD (concept); IaC (concept); observability (metrics/logs/traces).
- **Competencies:** Explain (container mechanism), Trace (a deployed request), Diagnose (deployment failure), Estimate (cost of an infra choice), Learn-New-Tech (read a deployment).
- **Horizontal threads:** Cost / Resource Economics (revisit — cloud cost); Failure (revisit — deployment failures); Technical Literacy (revisit); Software Engineering (revisit); API/Interface Design (revisit — infra config as interface).
- **Likely hands-on mechanism class:** build a small container locally; observe namespaces/cgroups in the course VM; deploy a two-container service; break the network path and observe.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any production deployment, DevOps, platform engineering.
- **Core vs Deep Dive:** Deep Dive: Kubernetes internals, service mesh, real IaC design complex.

### S6 · M20 — Observability & Reliability Engineering (Area 12)
- **Purpose / mental-model contribution:** How to know a production system is healthy: metrics, logs, traces, alerts, SLOs, incident response, postmortems. This is the "how would I know?" question made systematic (D-014 Diagnostics).
- **Prerequisites:** M18/M19 (state/infra), M16, M11 (measurement/tracing).
- **Key concepts:** metric; log; trace; correlation; SLO; alerting (concept); instrumentation; red-teaming light; postmortem; budgeting; clock semantics (monotonic vs wall clock).
- **Competencies:** Diagnose (from signal to cause), Observe (a dashboard), Judge (SLO choice), Estimate (business cost of outage).
- **Reconciled outcome (R7, Issue #9):** the experimental pattern first assessed at M04 `L04-02` is **revisited** as production-signal diagnosis at `L20-01/L20-02` (and consolidated at M23 `L23-01`). The DAG-hidden-prerequisite flag for **clock semantics** is resolved here: measuring durations requires a monotonic clock; wall-clock readings cannot time spans (Python docs: `time()` wall vs `time.monotonic()`/`perf_counter`); one light bridge, no statistics prerequisite.
- **Horizontal threads:** Measurement & Performance (revisit — the "how long/where time" question formalized); Failure (revisit — incident); Software Engineering (revisit); Cost (revisit).
- **Likely hands-on mechanism class:** instrument a small service with metrics/logs/traces; create an alert; run a controlled failure; read a real postmortem (course-owned or classic).
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** SRE, any production debugging.
- **Core vs Deep Dive:** Deep Dive: distributed tracing internals, alert tuning, chaos engineering.

### S7 · M21 — Security Synthesis I: Trust & Crypto Use (Area 13)
- **Purpose / mental-model contribution:** Security is a *system property of boundaries*, not a feature. Trust boundaries; what to do, not how to implement: symmetric/asymmetric crypto use, hashing, signatures, certificates; where "don't roll your own" applies.
- **Prerequisites:** M11 (TLS — the crypto case already visited), M07 (isolation), M12 (same-origin).
- **Key concepts:** trust-boundary **synthesis/revisit**; threat model; hash; MAC; symmetric/asymmetric; signature; cert/CA; nonce; random; secret management; defense in depth (light).
- **Competencies:** Judge (boundary design), Explain (crypto role: confidentiality/integrity/auth), Diagnose (a misuse), Learn-New-Tech (read a crypto API).
- **Horizontal threads:** Security (**SYNTHESIS** — M07/M11/M12/M19 boundary cases are consolidated into an explicit threat model and crypto-use judgment); Correctness (revisit — crypto invariants); Privacy (revisit — encryption ≠ anonymity).
- **Likely hands-on mechanism class:** use a standard library (Python `cryptography`) for signing/verifying and encrypting; observe a failed verification; inspect a TLS certificate with `openssl`.
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any security review, password handling, API auth.
- **Core vs Deep Dive:** Deep Dive: crypto implementation, side-channel attacks, post-quantum.

### S7 · M22 — Security Synthesis II: Authn/Authz & Secure Composition (Area 13)
- **Purpose / mental-model contribution:** Authentication vs authorization; session/token (JWT) mechanics; injection-style vulnerabilities; composition failures (insecure deserialization, SSRF, supply chain); the safety-first defense mindset (D-012 security labs).
- **Prerequisites:** M21, M11 (HTTP headers), M12 (browser security model), M19 (supply chain context).
- **Key concepts:** authn vs authz; password hashing; session vs token; JWT (claims/signature); OAuth (concept); SQL injection; XSS; CSRF; SSRF; deserialization; CSP (revisit); least privilege; dependency/supply chain.
- **Competencies:** Judge (secure design), Diagnose (a vulnerable app), Explain (attack → mechanism → fix), Learn-New-Tech (read a security doc).
- **Horizontal threads:** Security (revisit/synthesis); Correctness (revisit — inputs as untrusted); Software Engineering (revisit); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** use a course-owned vulnerable app (safe target, D-012) to observe an injection/XSS; then fix it; then write a threat-model card. **No penetration-testing training.**
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any app development, security reviews, OWASP awareness.
- **Core vs Deep Dive:** Deep Dive: formal security proofs, binary exploitation beyond intro, red-team training (rejected as Core).

### S7 · M23 — Systems Thinking & Judgment (Area 14)
- **Purpose / mental-model contribution:** Synthesize everything into judgment tools: measurement discipline, cost/resource economics, failure-mode reasoning, the Technology Evaluation Framework (D-015), and the systems questions (where is time/data/state going; where can it fail; how would I know; what must always be true; what are we paying for; at what scale does this become a problem).
- **Prerequisites:** S6-complete (or M18/M20 if compressed path), plus M21/M22 or concurrent.
- **Key concepts:** judgment; measurement methodology; cost model; failure taxonomy; technology admission (D-015 card); napkin math (consolidated); judgment under uncertainty; trade-off language; applied measurement-uncertainty toolkit (consolidated).
- **Competencies:** Judge (the capstone competency), Estimate (consolidated), Learn-New-Tech (systematically evaluate), Explain (defend).
- **Reconciled outcome (R1/R7, Issue #9):** `L23-01` **consolidates** the experimental pattern (first assessed at M04 `L04-02`, production-mode at M20) and the applied measurement-uncertainty toolkit — distributions/median/percentiles/uncertainty/inference limits — into one measurement methodology; clock-semantics bridge applies here as well (monotonic vs wall clock). `L23-02` evaluates technology via the Technology Evaluation Framework and (per R5) treats AI-generated claims as untrusted hypotheses verified by source/test/measurement (Current Case), without an AI module.
- **Horizontal threads:** ALL threads converge here (synthesis); Measurement & Performance (revisit — methodology); Cost (revisit — models); Failure (revisit — taxonomy); Technical Literacy (revisit).
- **Likely hands-on mechanism class:** a technology evaluation case study (write a full Technology Card on a real/current technology); a measurement methodology exercise (design a benchmark that answers a question).
- **Mini Cloud App integration:** Use the accepted P0–P9 mapping in `meta/blueprint/final-reconciliation-v0.1.md` §6. This Module is a project application/revisit only where that mapping names it; project milestone order is not a curriculum DAG edge.
- **Beyond-the-Project relevance:** any engineering leadership, architecture reviews, technology selection.
- **Core vs Deep Dive:** Deep Dive: formal architecture-role studies, research-style measurement.

### S7 · M24 — Final System Defense (Area 15)
- **Purpose / mental-model contribution:** A capstone not of *new* material but of *integration and articulation*: the learner defends the architecture of the Mini Cloud App using mechanisms, trade-offs, failure modes, measurement, cost, and the Technology Evaluation Framework. It is the final assessment of judgment (D-006, Invariant 1).
- **Prerequisites:** M23 (judgment synthesis) and the complete S1–S6 chain.
- **Key concepts:** architecture review; trade-off defense; failure/risk walkthrough; cost/scale analysis; evidence-based claims; identifying what *should* be measured.
- **Competencies:** Judge (defended), Estimate (under uncertainty), Explain (articulate), Correctness (stated invariants), Diagnose (anticipate failures).
- **Horizontal threads:** ALL — final synthesis (Judge + all threads).
- **Likely hands-on mechanism class:** a structured architecture defense session; possibly a written design doc + oral defense (this is the Mini Cloud App by then, Issue #3).
- **Mini Cloud App integration:** the app *is* this capstone.
- **Beyond-the-Project relevance:** any architecture/technical-leadership review.
- **Core vs Deep Dive:** Core terminal; no deeper extension expected in the first traversal.

---

## 5. Preliminary Lesson Map

**Purpose:** dependency reasoning only. IDs are proposal labels (per-Module `Lxx-yy`). Each entry is intentionally compact. **This is not lesson drafting**; no teaching prose here.

Legend: `FI` = would be canonical first-introduction; `RV` = contextual revisit. Mechanism classes assume the canonical Linux env (D-008).

| Lesson ID | Module | Learner question | Primary mechanism/concept | Hard prerequisites | FI / RV | Competency gain | Active observe/build/break? |
|---|---|---|---|---|---|---|---|
| L00-01 | M00 | "When I open a webpage, what actually happens?" | Whole-system map; abstraction/interface/indirection; the question set | programming basics | FI: system map, abstraction, question set | Trace, Explain, Observe | Y (observe a request, break it) |
| L00-02 | M00 | "How do I investigate something I don't understand?" | Tooling: shell/task execution; reading unfamiliar code/file; debugger-light investigation; Git evidence; reproducibility/version/environment record; run baseline + preserve evidence (R2); AI-generated output = untrusted hypothesis (R5) | L00-01 | FI: Technical Literacy basics; Debugging intro; source-verification habit | Observe, Learn-New-Tech, Explain, Diagnose | Y (use shell, git; reproducible investigation) |
| L01-01 | M01 | "What is a bit, really?" | Bit/byte/binary; counting | L00-01 | FI: representation | Trace, Explain, Estimate | Y (hexdump) |
| L01-02 | M01 | "Why is my number wrong?" (overflow) | Two's-complement, signed/unsigned, overflow | L01-01 | FI: integer representation | Correctness, Trace, Diagnose | Y (overflow demo) |
| L01-03 | M01 | "Why does my text look broken?" | UTF-8/encoding; endianness | L01-01 | FI: text encoding | Trace, Explain, Diagnose | Y (decode/encode, break) |
| L01-04 | M01 | "How big is this file?" | Size estimation; serialization; round-trip invariant | L01-01 | FI: size/no-serialization round-trip; RV: representational correctness | Estimate, Correctness | Y (compress/parse) |
| L02-01 | M02 | "What does 'fast' mean for an algorithm?" | Complexity as growth; applied discrete/asymptotic toolkit: counting, order-of-magnitude scheduling (R1) | L01-01 or prior | FI: complexity; FI: asymptotic/counting toolkit (R1) | Estimate, Explain, Trace | Y (measure growth) |
| L02-02 | M02 | "Why is my lookup slow?" | Hash table vs list vs tree; trade-off | L02-01 | FI: standard data structures; FI: trade-off language | Judge, Explain | Y (implement/measure) |
| L02-03 | M02 | "What is abstraction doing for me?" | Abstraction layers; interface vs implementation; **intuitive model of computation; expressibility; tractability; decidability intuition** (R9); specification + invariant + correctness canonical home | L02-02 | RV: abstraction; FI: interface/contract; FI: spec/invariant/correctness; FI: limits intuition (R9) | Explain, Judge, Correctness | Y (design a small interface) |
| L03-01 | M03 | "What does my code actually run on?" | ISA, registers, instruction fetch-execute | L01-01, L02-02 | FI: machine model | Trace, Explain | Y (disassembly) |
| L03-02 | M03 | "How does a function call work?" | Stack frame, call/return, stack overflow | L03-01 | FI: stack/heap/call frame | Trace, Diagnose | Y (gdb, overflow) |
| L03-03 | M03 | "Why does my program crash?" (segfault) | Memory access; address validity | L03-02 | FI: crash as signal; RV: failure | Diagnose, Observe | Y (induce crash) |
| L04-01 | M04 | "Why is my slow loop slow?" | Memory hierarchy; cache; latency ladder | L03-01, M01 | FI: hierarchy, locality | Observe, Diagnose, Estimate | Y (measure blocking) |
| L04-02 | M04 | "Why does order matter?" | Locality (spatial/temporal); layout; **applied measurement-uncertainty toolkit + experimental pattern — canonical first home (R1/R7)**: baseline → controlled change → metric/environment/workload → repetitions/distribution → observation → competing explanation → bounded conclusion; repeated measurements, median/percentiles when useful, uncertainty, inference limits | L04-01 | RV: locality; FI: measurement-uncertainty toolkit (R1); FI: experimental pattern (R7); RV: measurement methodology | Diagnose, Measure, Judge, Estimate | Y (benchmark, reorder; distribution of runs) |
| L05-01 | M05 | "How does my Python become an instruction?" | Compiler/interpreter pipeline; source→machine | L03-02, L04-01 | FI: translation/interpretation; RV: abstraction | Trace, Explain, Learn-New-Tech | Y (read bytecode/dis) |
| L05-02 | M05 | "What is a language really?" | AST/grammar (lexer/parser concept); IR; runtime (GC/JIT) | L05-01 | FI: grammar/AST; RV: interface | Explain, Judge | Y (tiny parser) |
| L05-03 | M05 | "Why are types useful?" | Type systems as invariants; dynamic vs static | L05-02 | FI: type as invariant | Correctness, Judge | Y (mismatch bug) |
| L06-01 | M06 | "What is a process?" | Process; program→process; syscalls | L03-02, L05-02 | FI: process, syscall, kernel/user | Trace, Explain, Observe | Y (ps/strace) |
| L06-02 | M06 | "How does a program start another?" | fork/exec; exit/status; shell | L06-01 | FI: fork/exec; RV: interface | Trace, Diagnose | Y (fork demo, strace) |
| L06-03 | M06 | "How does the CPU get shared?" | Scheduling intuition; isolation | L06-02 | FI: scheduling (intuition), isolation | Explain, Judge | Y (CPU-bound vs IO) |
| L07-01 | M07 | "How do two programs both use memory?" | Virtual memory; address space; paging concept; first concrete trust/protection boundary | L04-01, L06-01 | FI: VM concept; FI: trust boundary (distinguish from isolation); RV: isolation | Trace, Explain, Judge | Y (/proc/maps) |
| L07-02 | M07 | "Why is my program out of memory?" | Heap/malloc; OOM; leak | L07-01 | FI: heap/OOM; RV: failure | Diagnose, Estimate | Y (memory stress) |
| L07-03 | M07 | "What happens when I touch a bad address?" | Page fault; faults; fault handler intuition | L07-01 | RV: failure; FI: page fault | Trace, Explain, Diagnose | Y (fault observ. via tools) |
| L08-01 | M08 | "What is a file, underneath?" | File API; fd; inode (concept); directory | L06-01, L07-01 | FI: file/dir/inode; RV: interface | Trace, Explain | Y (stat/strace) |
| L08-02 | M08 | "Where does my file's data actually live?" | Page cache; block device; buffered I/O | L08-01, L04-01 | FI: page cache; RV: hierarchy | Trace, Explain, Measure | Y (vmstat, read timing) |
| L08-03 | M08 | "Why is my file I/O slow?" | I/O error, permission, disk-full; buffering | L08-02 | RV: failure; FI: I/O failure | Diagnose, Judge | Y (induce errors) |
| L09-01 | M09 | "What does 'durable' mean?" | Durability; fsync; WAL concept | L08-02 | FI: durability; RV: reliability | Judge, Explain | Y (kill/power-loss simulation) |
| L09-02 | M09 | "Why is my disk fast sometimes and slow later?" | SSD vs HDD; write amplification; wear leveling | L09-01 | FI: SSD/HDD mechanism; RV: cost | Estimate, Explain, Judge | Y (latency measurement) |
| L09-03 | M09 | "Where should my company's files live?" | Object vs block vs file; storage cost model | L09-02 | FI: storage classes; FI: cost economics | Estimate, Judge, Learn-New-Tech | Y (cost calc; inspect object storage) |
| L10-01 | M10 | "How does a message cross the internet?" | IP; routing; packet; port | L06-01 | FI: network basics | Trace, Explain | Y (traceroute, nc) |
| L10-02 | M10 | "How does 'reliable' work over unreliable links?" | TCP handshake, segments, retransmission; UDP | L10-01 | FI: TCP/UDP; RV: reliability | Explain, Trace, Diagnose | Y (ss, local socket) |
| L10-03 | M10 | "Why is my request timing out?" | Failure modes; timeout vs refused | L10-02 | RV: failure; FI: network diagnosis | Diagnose, Judge | Y (kill a server, observe) |
| L11-01 | M11 | "How do I talk securely to a server?" | TLS handshake concept; CA/cert | L10-02, M07 | FI: TLS; RV: crypto primer | Trace, Explain, Judge | Y (curl -v, openssl) |
| L11-02 | M11 | "What is HTTP, really?" | Request/response, methods, status, headers | L11-01 | FI: HTTP; RV: API/interface | Trace, Explain, Observe | Y (curl, DevTools) |
| L11-03 | M11 | "Why is my page slow to load?" | Caching; ETag; proxies/CDN; HTTP/2/3 | L11-02 | FI: HTTP caching; FI: QUIC/HTTP3 (STABLE, R10); RV: performance | Diagnose, Judge, Estimate | Y (cache headers, local proxy) |
| L12-01 | M12 | "What is a browser, architecturally?" | Multi-process; renderer; browser process; site isolation | L10-02, L11-02, L07 | FI: browser architecture (R8); RV: process model | Trace, Explain, Judge | Y (DevTools/task manager) |
| L12-02 | M12 | "How does a page render?" | Rendering pipeline: parse→DOM→render→layout→paint | L12-01 | FI: rendering (R9); RV: parsing | Trace, Explain, Observe | Y (DevTools performance) |
| L12-03 | M12 | "Why is the browser secure?" | Origin; same-origin; CORS; CSP; sandbox | L12-02, L11-02 | FI: origin/security model; RV: security | Explain, Judge, Diagnose | Y (break CORS, fix) |
| L12-04 | M12 | "Why does my page feel slow?" | Event loop; render-blocking; JS runtime | L12-02 | FI: event loop preview; RV: concurrency | Diagnose, Measure | Y (block the main thread) |
| L13-01 | M13 | "Why is my query fast/slow?" | B-tree; index; page/IO; EXPLAIN | L08-02, L09-02, L04 | FI: indexing/engine; RV: data structures | Explain, Observe, Estimate | Y (EXPLAIN, index measure) |
| L13-02 | M13 | "What is SQL doing?" | Relational model; query plan concept; storage engine | L13-01 | FI: relational/SQL semantics | Trace, Explain, Judge | Y (query a real DB) |
| L13-03 | M13 | "Why do my schema choices matter?" | Schema design & invariant; **schema evolution; reader/writer compatibility; migration/backfill trade-offs; source-of-truth vs derived data; lightweight provenance (R6)** | L13-02 | RV: trade-off; FI: schema invariant; FI: schema-evolution/provenance pattern (R6, application pattern — no new concept ID) | Correctness, Judge, Diagnose, Learn-New-Tech | Y (design schema, evolve it, measure) |
| L14-01 | M14 | "What is a transaction?" | ACID; atomicity; WAL; commit | L13-02, L09-01 | FI: transaction/ACID/WAL | Correctness, Trace, Explain | Y (transaction, crash) |
| L14-02 | M14 | "Why does concurrent access corrupt data?" | Anomalies; isolation levels; locks; MVCC | L14-01, M15-preview | FI: isolation; RV: concurrency | Diagnose, Judge, Correctness | Y (reproduce anomaly) |
| L14-03 | M14 | "How do I design an atomic write?" | Idempotency; multi-step writes; deadlock (light) | L14-02 | FI: idempotency preview; RV: invariant | Judge, Correctness | Y (write + crash test) |
| L15-01 | M15 | "Why is my threaded code wrong?" | Threads; races; interleaving | L06-01, M14 (or L14-02) | FI: threads/race | Trace, Diagnose, Correctness | Y (race repro, stress) |
| L15-02 | M15 | "How do I make it right?" | Mutex; atomicity; conditions; deadlock | L15-01 | FI: locks; RV: correctness | Explain, Correctness, Judge | Y (fix race; deadlock observe) |
| L15-03 | M15 | "Thread or async?" | Event loop (revisit); async/await; GIL reality | L15-02, L12-04 | FI: async/event loop synthesis; RV: concurrency | Judge, Explain | Y (async vs thread measure) |
| L16-01 | M16 | "What is different about many machines?" | Partial failure; the fundamental ambiguity | L15-01, L10-02 | FI: partial failure; RV: failure | Judge, Explain, Trace | Y (inject partition) |
| L16-02 | M16 | "How do I call a remote function safely?" | RPC; serialization; timeout; retry; idempotency | L16-01 | FI: RPC; RV: interface/indirection | Trace, Judge, Explain | Y (RPC with injected delay) |
| L17-01 | M17 | "How do I keep data safe across machines?" | Replication; quorum; durability | L16-01, L09-01 | FI: replication; RV: durability | Judge, Explain | Y (bounded state/message/failure trace + EXP-05 source case; no required 3-node implementation) |
| L17-02 | M17 | "How do machines agree?" | Consensus concept (Raft/Paxos intuitive): what it buys/costs, leader election, bounded worked trace (R10) | L17-01 | FI: consensus (concept; Registry ID deferred); RV: correctness | Explain, Trace, Judge | Y (worked trace / failure scenario; no implementation) |
| L17-03 | M17 | "How consistent is 'strong enough'?" | Consistency models; linearizability ↔ eventual; CAP framing | L17-02 | FI: consistency models; RV: trade-off | Judge, Explain | Y (observe read-your-writes) |
| L18-01 | M18 | "How do services delegate work?" | Queue; durable handoff; at-least/at-most/exactly-once claims and limits | L17-03, L16-02 | FI: delivery/queue semantics; RV: failure | Judge, Explain, Trace | Y (bounded duplicate-delivery case; no broker product required) |
| L18-02 | M18 | "Do I need a distributor?" | Distributed transactions/2PC concept; saga; ordering | L18-01, M14 | FI: 2PC concept; FI: saga/ordering; RV: trade-off | Judge, Explain | Y (workshop scenario) |
| L19-01 | M19 | "What is a container?" | Container; namespaces; cgroups; image | L06-01, L07-01, L08-01 | FI: container mechanism; RV: isolation | Trace, Explain, Judge | Y (build/run container) |
| L19-02 | M19 | "What does 'the cloud' actually mean?" | VM vs container; region/AZ; cloud pricing | L19-01 | FI: cloud model; FI: cost | Explain, Judge, Estimate | Y (deploy + cost calc) |
| L19-03 | M19 | "How does code get to production?" | CI/CD; deployment strategies; IaC | L19-02, L16 (failure model) | FI: deployment/CI-CD; RV: failure | Explain, Judge, Diagnose | Y (pipeline demo; rollback) |
| L20-01 | M20 | "How do I know the system is OK?" | Metrics/logs/traces; SLO; alerting; **clock semantics — monotonic vs wall clock bridge (resolves DAG §6 flag)** | L19-02, L16 | FI: observability; RV: measurement; RV: experimental pattern (R7, from M04) | Observe, Diagnose, Judge | Y (instrument, alert) |
| L20-02 | M20 | "How do I debug a production incident?" | Incident response; postmortem; correlation | L20-01 | RV: debugging (elevated); FI: SRE/incident | Diagnose, Observe, Explain | Y (controlled incident) |
| L21-01 | M21 | "Where are the boundaries I must protect?" | Trust-boundary synthesis; threat model; defense in depth | L11-01, L07-01, L12-03 | FI: threat model/defense-in-depth synthesis; RV: trust boundary + isolation/TLS/origin cases | Judge, Explain, Diagnose | Y (threat map exercise) |
| L21-02 | M21 | "What do I use crypto for?" | Hash/MAC/signature/symmetric; cert lifecycle | L21-01 | FI: crypto *use*; RV: TLS | Explain, Judge, Learn-New-Tech | Y (openssl, signing) |
| L22-01 | M22 | "How do I know who is calling?" | Authn vs authz; password hashing; session/token/JWT | L21-02, L11-02 | FI: authn/authz; RV: identity | Judge, Explain | Y (token verify/forge-safe demo) |
| L22-02 | M22 | "Why is my web app vulnerable?" | Injection; XSS; CSRF; SSRF; deserialization | L22-01, L12-03 | FI: injection/OWASP-style; RV: security composition | Diagnose, Judge, Explain | Y (safe vulnerable app, fix) |
| L22-03 | M22 | "Why do I trust my dependencies?" | Supply chain; pinning; provenance light | L22-02, L19 | FI: supply chain; RV: trust | Learn-New-Tech, Judge | Y (dependency audit) |
| L23-01 | M23 | "How do I measure honestly?" | Measurement methodology; benchmarking rules; **consolidation of experimental pattern + measurement-uncertainty toolkit (R1/R7)** | L20-01, L04-02 (performance foundations) | RV: measurement methodology (consolidation); RV: uncertainty toolkit | Estimate, Judge, Diagnose | Y (design benchmark) |
| L23-02 | M23 | "How do I pick a technology?" | Technology Evaluation Framework (D-015); stable principle | L23-01, S6 foundations | FI: tech evaluation; RV: judgment | Judge, Learn-New-Tech, Explain | Y (write a Technology Card) |
| L23-03 | M23 | "What is the cost of my design?" | Cost/resource economics synthesis; napkin math at scale | L23-02 | FI: cost synthesis; RV: estimate | Estimate, Judge | Y (cost model) |
| L24-01 | M24 | "Can I defend an architecture?" | System Defense; trade-off reasoning; failure walkthrough | L23-02 | RV: all synthesis | Judge, Explain, Diagnose, Estimate | Y (defense session) |
| L24-02 | M24 | "What should I measure before I ship?" | Evidence-based claims; what to measure | L24-01 | RV: measurement; FI: evidence discipline | Judge, Diagnose | Y (design a pre-ship check) |

**Lesson count (reconciled):** 70 entries (S1: 9, S2: 8, S3: 12, S4: 10, S5: 9, S6: 12, S7: 10). This is an intentionally preliminary granularity — the Lead may merge/split at module-dossier time. The map is for dependency reasoning, not a locked lesson list.

**Course-discipline annotation (not a lesson row):** all REQUIRED Labs carry a **lab-entry gate** (obtain repository → run documented preflight check → reproduce baseline → save an environment/version/evidence record; environment preflight repeated at M03/M06/M13). This is course discipline, **not** a Module `H` edge and not a new lesson; R2/Issue #9 integration.

---

## 6. Competency Relationships

Every Module below names at least one competency it improves. The following shows the *dominant* competency per Module and where each competency first becomes a *strong* capability (not merely introduced):

| Competency | First **strong** capability | Modules that keep it strong |
|---|---|---|
| Trace | M00 (system map), mature by M12 (cross-process load) | M01, M03, M06, M08, M12, M16 |
| Explain | M00–M02 (representation/mechanism), mature by M08 | continuously all modules |
| Observe | M00 (tooling), mature by M04/M06 (perf/proc tools) | M03, M04, M06, M08, M13, M20 |
| Diagnose | M03/M04 (crash/perf), mature by M15/M20 (races/incidents) | M03, M04, M07, M08, M12, M14, M15, M20 |
| Correctness | M02 (invariants), mature by M14 (transaction invariants) | M01, M02, M05, M14, M15, M17 |
| Judge | M02 (trade-off language), matures M17/M23 | M09, M11, M12, M14, M17, M18, M22, M23 |
| Estimate | M01 (sizes), mature by L09-03/M19 (cost models) | M01, M02, M04, M09, M13, M19, M23 |
| Learn-New-Tech | M00 (tooling), matures M21–M23 (systematic evaluation) | M02, M05, M12, M19, M22, M23 |

**Design rule applied:** no Module exists that only adds terminology. Every Module above either (a) introduces a new mechanism observable with a real tool, or (b) extends an existing competency in a new context.

---

## 7. Horizontal Thread Map

D-014 names the threads; the Curriculum Map adds API/Interface Design, Software Engineering, and Napkin Math. Each thread is traced below. Format: **First meaningful / Recurs in / Synthesis**.

### Correctness & Invariants
- **First:** M01 (representation round-trip invariant), M02 (loop/data-structure invariants).
- **Recurs:** M05 (type systems), M07 (isolation), M13 (schema), M14 (transaction invariants), M15 (thread-safety), M16 (idempotency), M17 (replicated invariants), M21–M22 (crypto/security invariants).
- **Synthesis:** M23 (state invariants as the "what must always remain true?" question), M24 (defend invariants).

### Failure
- **First:** M00 (systems fail), M03 (crash as signal).
- **Recurs:** M06 (exit code/block), M07 (OOM/fault), M08 (I/O error), M09 (durability), M10 (network), M11 (TLS/HTTP errors), M14 (crash recovery), M15 (race), M16 (partial failure — the *defining* failure), M17 (partition), M18 (duplicate delivery), M19 (deployment), M20 (incident).
- **Synthesis:** M23 (failure taxonomy), M24 (failure walkthrough).

### Debugging
- **First:** M00 (debugging discipline), M02 (a first bug hunt).
- **Recurs:** M03 (gdb), M04 (perf measurement), M06 (strace), M07 (memory debuggers), M10/M11 (network tools), M13 (EXPLAIN), M14 (anomaly), M15 (race detectors), M16/M18 (tracing), M20 (production incident).
- **Synthesis:** M20 (SRE-style debugging), M24 (evidence discipline).

### Measurement & Performance
- **First:** M04 (real measurement: cache locality), M01 (estimation).
- **Recurs:** M08 (I/O measurement), M09 (storage latency), M10/M11 (RTT/TTFB), M12 (page load), M13 (query timing), M15 (scaling), M20 (SLO/metrics).
- **Synthesis:** M23 (measurement methodology), M24 (what to measure).

### Security
- **First meaningful:** M07 (memory isolation as security boundary), M11 (TLS), M12 (same-origin/CORS/CSP).
- **Recurs:** M17 (replication/partition security intuition), M19 (supply chain), M21 (trust/crypto), M22 (authn/authz/composition).
- **Synthesis:** M21–M22 (Security Synthesis), M23–M24 (secure judgment in defense).

### Concurrency
- **First meaningful:** M12 (event loop preview), M14 (DB isolation), M15 (threads/races — the coherent topic).
- **Recurs:** M16 (RPC/partial failure), M17 (ordering/consensus), M18 (queues/ordering), M20 (concurrent incident).
- **Synthesis:** M23 (concurrency in judgment), M24.

### Cost / Resource Economics
- **First:** M01 (size = resource), M04 (cache as cost trade-off), M09 (storage cost per GB — explicit), M10 (bandwidth).
- **Recurs:** M11 (CDN/cache cost), M13 (index write cost), M17 (replication cost), M18 (broker cost), M19 (cloud cost), M20 (downtime cost).
- **Synthesis:** M23 (cost model; "what are we paying for?"), M24.

### Technical Literacy
- **First:** M00 (shell/git/tooling), M01 (data formats).
- **Recurs:** M03 (assembly/ABI), M05 (language internals), M08 (filesystems), M10 (protocols), M12 (browser), M19 (infra), M22 (security docs).
- **Synthesis:** M23 (evaluating technology = literacy applied).

### API / Interface Design
- **First:** M00 (interface concept), M02 (contracts).
- **Recurs:** M03 (ABI), M05 (language/runtime interface), M06 (syscall API), M08 (file API), M11 (HTTP as API), M13 (SQL as interface), M16 (RPC interface), M19 (infra config as interface).
- **Synthesis:** M23–M24 (interface judgment in defense).

### Software Engineering
- **First:** M02 or M05 (structure matters), M06 (process structuring).
- **Recurs:** M12 (JS module practices light), M15 (testing/race stress), M16 (service decomposition), M19 (CI/CD).
- **Synthesis:** M23 (engineering judgment), M24.

### Privacy / Data Responsibility
- **First:** M11 (data in transit, cookies), M12 (third-party storage).
- **Recurs:** M07 (memory isolation), M19 (data residency/cloud), M21–M22 (encryption ≠ anonymity; least privilege).
- **Synthesis:** M23–M24 (privacy as part of judgment).

### Napkin Math / Estimation
- **First:** M01 (byte sizes), M02 (complexity), M04 (latency ladder).
- **Recurs:** M09 (storage), M10 (bandwidth), M11 (cache), M13 (IO cost), M17 (availability math), M19 (cloud cost).
- **Synthesis:** M23 (napkin math consolidated), M24.

---

## 8. Canonical First-Introductions & Revisits

This is the "teach once" table (Invariant 11, D-010). The stable definitions/canonical explanations live in `meta/CONCEPT_REGISTRY.md` (IDs `EC-CON-001`–`EC-CON-018`); this table is the locations table reconciled in Issue #9.

| Concept (EN; CN canonical) | Registry ID | Primary home (FI) | Subsequent revisits (RV) |
|---|---|---|---|
| Abstraction 抽象 | EC-CON-002 | M00 | M02, M05, M12, M16, M19, M23 |
| Interface 接口 | EC-CON-005 | M00 | M02, M06, M08, M11, M13, M16, M19 |
| Indirection 间接 | EC-CON-004 | M00 | M05, M07, M11, M16, M23 |
| Representation 表示 | EC-CON-003 | M01 | M03 (instructions), M05 (IR), M13 (tuples), M16 (serialization) |
| State 状态 | EC-CON-001 | M00 | M02, M06, M13, M14, M15, M17, M23 |
| Invariant 不变量 | EC-CON-008 | M02 (`L02-03`; M01 is application only) | M05 (types), M07 (isolation), M13–M15, M17, M21–M22, M23 |
| Specification 规格 | EC-CON-007 | M02 (`L02-03`) | M14 (transactions), M15 (thread safety), M21 (threat model) |
| Correctness 正确性 | EC-CON-009 | M02 (`L02-03`; M01 supplies evidence) | M07, M13–M17, M21–M23 |
| Caching 缓存 | EC-CON-011 | M04 | M08 (page cache), M11 (HTTP cache, CDN), M13 (buffer pool), M17 (consistency), M19 |
| Locality 局部性 | EC-CON-012 | M04 | M08 (disk locality), M13 (index locality), M23 |
| Trade-off 权衡 | EC-CON-006 | M02 (`L02-02`) | M04, M09, M11, M13, M14, M17, M18, M19, M23 |
| Failure 故障 | EC-CON-010 | M03 (`L03-03`; M00 is preview) | M06–M20 (everywhere), M23–M24 |
| Isolation 隔离 | EC-CON-013 | M07 (`L07-01`; M06 process boundary is preview) | M12 (browser), M14 (transactions), M15 (threads), M16–M17, M21, M22 |
| Concurrency 并发 | EC-CON-015 | M15 (`L15-01`; M12 event loop / M14 overlap are previews) | M16–M18, M20, M23 |
| Consistency 一致性 | EC-CON-014 | M14 (`L14-02`) | M17 (replicated, changed guarantee), M18, M23 |
| Trust boundary 信任边界 | EC-CON-017 | M07 (`L07-01`; first concrete protection/trust boundary, not identical to isolation) | M11, M12, M19, M21 (synthesis), M22, M23, M24 |
| Durability 持久性/耐久性 | EC-CON-016 | M09 (`L09-01`) | M14 (WAL), M17 (replication), M24 |
| Process 进程 | EC-CON-018 | M06 (`L06-01`) | M07 (address spaces), M12 (browser processes), M16–M17, M19 (containers), M24 |

**Issue #9 additions (concepts without new Registry IDs; patterns or thread-level homes):**

| Pattern / thread | Home (FI) | Revisits |
|---|---|---|
| Applied measurement-uncertainty toolkit (R1) | M04 `L04-02` | M13 (selectivity/cost), M16/M17 (availability math, just-in-time), M19 (cloud cost), M20 (latency distributions), M23 (consolidation) |
| Experimental measurement pattern (R7) | M04 `L04-02` (first assessed) | M20 (`L20-01` production signals), M23 `L23-01` (consolidation) |
| Schema evolution / provenance (R6, application pattern over State/Representation/Interface/Invariant) | M13 `L13-03` | M16 (serialization compatibility), M18 (derived/event data), M19/M23 (supply/source provenance), P0/P4/P6/P9 |
| Toolchain investigative loop (R2) | M00 `L00-02` | every REQUIRED lab (entry gate), M03/M06/M13 env preflight, M19 `L19-03` packaging, M23 `L23-02` source verification |
| Consensus concept (R10; Registry ID deferred) | M17 `L17-02` | M18, M23, M24 |

**Harmful-duplication note:** The same concept (e.g., Caching, Isolation, Failure) must never get a *second* full canonical explanation. Every later location uses one-sentence recap + context-specific application.

---

## 9. Core / Deep Dive Boundary Notes

The following are **tempting conventional-degree items that should probably remain OUT of Core** (or be marked Deep Dive / Current Case):

| Topic | Boundary | Rationale |
|---|---|---|
| Logic gates → ALU → full CPU design (Nand2Tetris Part I / digital logic) | Deep Dive (optional Core-adjacent excursion) | R4 shows it's a complete construction but the Core learner needs the *mechanism* (there is an ISA), not the *construction*. It adds a lot of hours without a new shared-world capability. |
| Compiler construction (full; Dragon-book) | Deep Dive | M05 gives the pipeline lens; full compiler is a specialization. |
| Data structures beyond core (graphs, DP, NP-completeness) | Deep Dive | Core needs the standard containers & complexity; graph/DP theory is its own field. |
| Kernel internals / driver development | Deep Dive | M06/M07 give mechanism understanding; writing a kernel is specialization. |
| Full database implementation (B-tree from scratch, MVCC internals) | Deep Dive | M13/M14 teach mechanism + judgment; implementation internals beyond that is a DB course. |
| Congestion control detail, BGP, global routing | Deep Dive | M10/M11 teach the mechanism and evaluation; deep protocol internals is networking specialization. |
| Web development practice (frameworks, SPA architecture, CSS mastery) | NOT Core (Current Case / Deep Dive) | D-006 forbids web-dev training. M12 teaches the *platform*, not frameworks. |
| Crypto implementation / side-channel / post-quantum | Deep Dive | M21/M22 teach *use* and boundary design, never implementation. |
| Penetration testing / exploitation | REJECTED as Core (Current Case only for awareness) | D-012 security labs are defense-first, safe-target, mechanism-aware. |
| Kubernetes/service-mesh ops mastery | Current Case / Deep Dive | M19 gives container/cloud mechanism; Kubernetes specifics are a specialization with fast decay (FRONTIER). |
| Type-system theory / PL research | Deep Dive | M05 teaches why types matter as invariants; theory is specialization. |
| Full storage-engine implementation (LSM, erasure coding) | Deep Dive | M09/M13 teach judgment; implementation is specialization. |
| ML/AI **content** (introducing models) | NOT Core (Current Case only; OQ-BP-001 escalation) | R4 disposition: bounded AI literacy is an RFC-gated architecture question. Safe interim: AI-generated output = untrusted hypothesis verified by source/test/measurement (R5 Current Case at M00 `L00-02` / M23 `L23-02`). No ML math, no LLM architecture, no prompt-engineering catalog, no vendor survey. |
| Applied probability/statistics/math sequences (discrete-math course, calculus, inferential-statistics course) | NOT Core (just-in-time toolkit) | R1 disposition: only the M04 `L04-02` applied-uncertainty toolkit + in-context estimation; no math gate before M01. |
| Full consensus implementation (Raft/Paxos build, proofs) | Deep Dive | R11 disposition: concept stays Core at M17; implementation/proofs after a complete shared model; EXP-05 explores the case. |
| Schema-registry operations / Data Engineering / lineage platforms | NOT Core | R6 disposition: bounded M13 `L13-03` application pattern; no PROV ontology, no data-platform training. |
| Front-end performance budgets | Deep Dive | M12 covers measurement; budgets are practice. |

**Core boundary test applied:** a topic is Core only if removing it would break the learner's ability to connect the main modern chain (a request through a browser, into a web server, a cache, a DB, a queue, object storage, and back) with accurate mechanism + judgment. Everything else is either a Current Case (reality-aware reference) or Deep Dive.

---

## 10. Reconciliation With #2/#3/#4 — RESOLVED (Issue #9)

### With Issue #2 (External Curriculum Coverage Audit) — resolved via #10 disposition matrix (PR #17) + this map
- Audit recommendations R1–R15 were given one disposition each in `audit-to-architecture-disposition-v0.1.md` (5 integrate-existing, 2 bounded additions, 2 current case, 3 deep dive, 1 reject, 2 escalations). The non-escalated outcomes are integrated above: R1 (§ M04), R2 (§ M00), R6 (§ M13), R7 (§ M04), R8 (§ horizontal threads), R9 (§ M02/M05), R10 (§ M17); R5/R13 are Current Case discipline; R11/R12/R14 Deep Dive; R15 rejected. R3/R4 remain architecture escalations (OQ-BP-003 / OQ-BP-001, RFC candidates in `meta/rfcs/`).

### With Issue #3 (Mini Cloud App Evolution) — resolved via #14 alignment (PR #14) + §6 of `final-reconciliation-v0.1.md`
- The app surfaces at M00 intro, every Stage checkpoint, and the M24 capstone; P0–P9 milestones are anchored to macro area IDs and Module IDs (not Stage names); the app is the recurring *observation surface* and final capstone, never the lesson (D-006). Canonical per-milestone mapping: `final-reconciliation-v0.1.md` §6.

### With Issue #4 (Classic labs / Source Expedition research) — resolved via #16 selection map (PR #16)
- Mechanism *classes* above became the accepted selection: **5 Required Labs, 5 Optional Labs, 5 Source Expeditions** (Adopt → Adapt → Build) per `lab-source-selection-map-v0.1.md`. No Lab is implemented in Blueprint. Every Module not represented by a selected Lab keeps its mechanism class, project checkpoint, or Source Expedition.

---

## 11. Proposal-Level Open Questions — RESOLVED (Issue #9)

The original Issue #1 proposal-level questions were answered by the reconciliation wave:

| OQ | Question | Resolution |
|---|---|---|
| OQ-1 | Stage boundaries/names | 7 Stages confirmed; corrections only to dependency semantics, not Stage count/names. S4/S5 remain separate; Concurrency stays inside S5 (M14/M15 parallel, both soft/partial, no `H` either way). Learner validation may still refine names post-construction. |
| OQ-2 | Lesson granularity | 70 preliminary Lesson entries (S1: 9, S2: 8, S3: 12, S4: 10, S5: 9, S6: 12, S7: 10); granularity is blueprint-level for dependency reasoning; final merge/split decisions happen at module-dossier time, not in Blueprint. |
| OQ-3 | First Concept Registry population | Resolved: 18 concepts (`EC-CON-001`–`EC-CON-018`; see `meta/CONCEPT_REGISTRY.md`); M00 question set is a tool/thread, not a concept. |
| OQ-4 | Where specific hands-on experiences belong | Resolved: 5 Required / 5 Optional / 5 Source Expeditions (`lab-source-selection-map-v0.1.md`); no Lab implemented in Blueprint. |
| OQ-5 | Mini Cloud checkpoint granularity | Resolved: #14 anchors P0–P9 to Module IDs and macro areas (not Stage names); canonical mapping in `final-reconciliation-v0.1.md` §6. |
| OQ-6 | Audit findings | Resolved: `audit-to-architecture-disposition-v0.1.md` + this map §10 (above). |
| OQ-7 | S4/S5 order (browser vs DB first) | Resolved: request-centric default narrative is pedagogical preference (OQ-BP-004); no `H` edge; learner may follow either branch. |
| OQ-8 | Compression of S5/S6 | Not compressed as a separate track; S4/S5 partial independence exists, but a complete shared traversal still requires both before S6 synthesis (DAG facts, not a time budget). |
| OQ-9 | Napkin-math constants | **Resolved as a separate question:** hardware-dependent latency/cost constants are implementation-time baselines governed by OQ-BP-006, module Research Dossiers, and Living Curriculum review. Do not maintain a second Open Question for them. |

**Remaining architecture-level Open Questions** are tracked in `meta/OPEN_QUESTIONS.md` (OQ-BP-001 bounded AI literacy; OQ-BP-003 human-facing/accessibility boundary; OQ-BP-006 environment versions).

---

## 12. Verification Record (for this deliverable)

See `dependency-graph-v0.1.md` §§5–9 for graph-specific checks and the Completion Report in the PR. Summary:

- All macro areas `00`–`15` accounted for (Stage mapping table, §3).
- Every Stage has a named capability gain + checkpoint + exit criteria.
- Every Module names ≥1 competency improved.
- Every horizontal thread from D-014 + Curriculum Map has first/recur/synthesis.
- No Module is a pure terminology catalog.
- No web-development sequence emerges (M12 is platform-mechanism, not framework practice).
- No single traditional field is over-weighted: 16 Macro areas split across 7 Stages; no Module set duplicates a conventional course wholesale.
- Lesson entries remain Blueprint-level (compact IDs/questions/mechanism — no teaching prose).
- External factual claims verified against R1–R12 (fetched 2026-08-30).
- `book/`, `course/`, `labs/`, `project/`, canonical meta files: **unchanged** (only the two new proposal files created).

**What was NOT verified (original proposal):** (a) real learner validation (not yet possible); (b) external audit findings (#2 parallel); (c) Mini Cloud App feature sequence (#3); (d) labs (#4); (e) final Concept Registry IDs.

**Issue #9 re-verification (2026-08-30):** (b) resolved via PR #17 dispositions and integrated in §§4/9/10 above; (c) resolved via PR #14 and canonical mapping in `final-reconciliation-v0.1.md` §6; (d) resolved via PR #16 selection map (5/5/5; no code implemented); (e) resolved via `meta/CONCEPT_REGISTRY.md` first population (18 IDs). Items (a) learner validation, plus environment/version pinning and napkin-math constants, remain post-Blueprint/implementation work.
