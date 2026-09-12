# Essential CS — Resource-First Learning Roadmap

Checked: **2026-09-12**

This is the learner-facing default route for Essential CS v1.0.

The repository is a map and guide. You do **not** need to complete every repo-owned lab or the Mini Cloud project to benefit from the curriculum. Prefer the strongest available external resource for a mechanism, use the repo Lessons for orientation and synthesis, and use repo Labs/Mini Cloud only when you want an extra guided exercise.

## How to use this roadmap

For each module:

1. Read the **Goal** first so you know what you are trying to understand.
2. Use the **Primary** resource as the main learning source.
3. Use **Reference / Deep Dive** only when the primary source leaves a gap or you want more depth.
4. Answer the **Checkpoint** in your own words or with a small observation. Do not optimize for finishing every exercise.
5. Stop when you can explain the mechanism and make one correct prediction. Move on; revisit depth later.

Resource labels:

- **PRIMARY** — recommended first route.
- **REFERENCE** — authoritative specification/docs; use to verify details.
- **DEEP DIVE** — valuable but not required for the first traversal.
- **CURRENT PRACTICE** — time-sensitive; periodically re-check.

---

## Stage 0 — Tooling bridge (optional)

Before M00, if shell/Git/editor/debugging friction is high:

- **PRIMARY:** [MIT — The Missing Semester of Your CS Education](https://missing.csail.mit.edu/) — command line, version control, debugging/tool fluency. The site has a current 2026 edition.

**Checkpoint:** clone a repository, inspect a diff, run a small program, redirect output, search files, and explain what Git is tracking.

---

## S1 — Foundations of Computation

### M00 — The Map

**Goal:** build a whole-system mental model: source code → runtime → OS → network/storage → service → database → response; distinguish abstraction, interface, state, indirection, and evidence.

- **PRIMARY:** this repository: `book/00-the-map/` and `meta/CURRICULUM_MAP.md`.
- **REFERENCE:** [The Missing Semester](https://missing.csail.mit.edu/) for practical tooling.

**Checkpoint:** take one everyday action such as loading a web page and draw the major layers involved. For each boundary ask: *what crosses this interface, who owns the state, and what evidence could prove my story?*

### M01 — Information & Representation

**Goal:** understand bits/bytes, integers, finite width, text/Unicode/UTF-8, endianness, serialization, and size reasoning.

- **PRIMARY:** [Nand2Tetris](https://www.nand2tetris.org/) — use the early Boolean/arithmetic/memory material for concrete representation intuition.
- **REFERENCE:** [The Unicode Standard](https://www.unicode.org/standard/standard.html) for text semantics and encoding references.

**Checkpoint:** predict byte length before measuring: encode several Unicode strings as UTF-8, serialize one small record, and explain the difference between character, code point, encoded bytes, and field boundaries.

### M02 — Computation, Algorithms & Data Structures

**Goal:** asymptotic reasoning, searching/sorting, hashing, trees, graphs, dynamic programming, and choosing a data structure based on operations rather than fashion.

- **PRIMARY:** [MIT 6.006 — Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/).
- **DEEP DIVE:** MIT 6.006 problem sets / lecture notes from the same course.

**Checkpoint:** for a small program, state the dominant operation, derive its time/space growth, then change the data structure and predict how the cost changes before benchmarking.

---

## S2 — The Machine

### M03 — ISA, Execution & Machine State

**Goal:** understand instructions, registers, stack frames, calls, branches, memory operands, compilation to machine code, and what a debugger/disassembler reveals.

- **PRIMARY:** [Nand2Tetris](https://www.nand2tetris.org/) — machine language / computer architecture sequence.
- **DEEP DIVE:** CMU 15-213 / CS:APP materials when available through the official course site.

**Checkpoint:** compile a tiny function, disassemble it, identify arguments/return value, single-step it in a debugger, and explain one source-level operation in terms of machine state.

### M04 — Memory Hierarchy, Locality & Measurement

**Goal:** caches, locality, latency hierarchy, benchmarking discipline, distributions/variation, and limits of performance inference.

- **PRIMARY:** CMU 15-213 / CS:APP memory-hierarchy and performance material.
- **REFERENCE:** current hardware/vendor documentation only when exact cache sizes or latency figures matter; treat those as **CURRENT**, not universal constants.

**Checkpoint:** write or reuse two equivalent traversals with different locality, predict which is faster and why, run repeated measurements, and report a bounded conclusion rather than a single timing number.

### M05 — Languages, Runtime & Compiler

**Goal:** connect source syntax, parsing/AST, bytecode or machine code, runtime representation, allocation, dispatch, exceptions, and garbage collection without trying to build an industrial compiler.

- **PRIMARY:** [Crafting Interpreters](https://craftinginterpreters.com/) — free online book; use selected chapters rather than treating the whole interpreter build as mandatory.
- **REFERENCE:** the official documentation for the language/runtime you actually use (for example Python's language/reference docs).

**Checkpoint:** trace one tiny expression from source text to parsed representation to runtime values; explain what the runtime, not the source language, must actually do.

---

## S3 — Operating Systems & Persistence

### M06 — Processes, Syscalls & Execution Context

**Goal:** process creation, execution, file descriptors, syscalls, privilege boundary, signals, exit/reaping, and the user/kernel transition.

- **PRIMARY:** [Operating Systems: Three Easy Pieces (OSTEP)](https://pages.cs.wisc.edu/~remzi/OSTEP/) — virtualization/process sections.
- **REFERENCE:** [Linux man-pages](https://man7.org/linux/man-pages/) for `fork`, `execve`, `wait`, `open`, `read`, `write`, signals, and `/proc` behavior.
- **OPTIONAL COMPANION:** repo LAB-REQ-02 / xv6 route when you want to see a syscall path in a teaching kernel.

**Checkpoint:** run a small program under `strace` (or equivalent), identify process/file syscalls, and explain what changed in user state versus kernel-managed state.

### M07 — Virtual Memory & Isolation

**Goal:** address spaces, pages, page tables, translation, faults, mapping, copy-on-write, protection, and why isolation is a mechanism rather than a guarantee of total security.

- **PRIMARY:** [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) — virtual-memory chapters.
- **REFERENCE:** Linux `mmap(2)`, `proc(5)`, and related man-pages.

**Checkpoint:** inspect a process memory map, identify code/heap/stack/shared-library regions, and explain what a page fault means without equating it with a program bug.

### M08 — Files, Filesystems & I/O

**Goal:** file descriptors, directories, inode-like metadata, buffering/page cache, filesystem namespace, crash boundaries, and deletion/retention semantics.

- **PRIMARY:** [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) — persistence/filesystem chapters.
- **REFERENCE:** Linux man-pages for `open`, `fsync`, `rename`, `unlink`, and filesystem interfaces.

**Checkpoint:** trace a read/write with OS tools and explain at which point data is in user memory, kernel cache, filesystem state, and durable media.

### M09 — Storage & Durability

**Goal:** block devices, SSD/HDD differences, caching, ordering, writeback, fsync, journaling/logging ideas, backup versus durability, and failure assumptions.

- **PRIMARY:** OSTEP persistence chapters plus the relevant filesystem documentation for your platform.
- **REFERENCE:** SQLite's durability/atomic-commit documentation is a useful concrete case: <https://www.sqlite.org/atomiccommit.html>.

**Checkpoint:** state what your program can and cannot claim after `write()`, after close, after `fsync`, and after a backup copy. Include the failure model in every durability claim.

---

## S4 — Networking, Web & Browser

### M10 — IP, DNS & Transport

**Goal:** addressing/routing, DNS, ports/sockets, UDP/TCP, reliability/order, congestion at a conceptual level, QUIC as modern transport, and end-to-end latency reasoning.

- **PRIMARY:** [Stanford CS144](https://cs144.github.io/) — use lectures/notes for networking mechanisms; projects are optional.
- **PRACTICAL REFERENCE:** [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/).
- **REFERENCE:** IETF RFCs for protocol truth when details matter.

**Checkpoint:** trace one connection from DNS lookup to socket endpoints; identify which guarantees come from IP, transport, application protocol, or your own code.

### M11 — TLS, HTTP, Caching & Intermediaries

**Goal:** TLS security properties, HTTP semantics, methods/status, representations, caching/validators, proxies, and the difference between application semantics and transport.

- **PRIMARY / REFERENCE:** [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
- **CURRENT REFERENCE:** [RFC 9846 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc9846.html) (2026; obsoletes RFC 8446).
- **PRACTICAL:** [MDN Web Security / TLS guidance](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/TLS).

**Checkpoint:** inspect one real HTTPS request and explain what TLS protects, what HTTP defines, what a cache validator means, and which metadata may still be observable.

### M12 — Browser as an Integrated System

**Goal:** URL/origin/site, navigation, parsing/rendering, event loop, storage, process model, sandbox/site isolation, and performance/security interactions.

- **PRIMARY:** MDN Web platform guides: <https://developer.mozilla.org/>.
- **REFERENCE / CURRENT PRACTICE:** [Chromium Site Isolation](https://www.chromium.org/Home/chromium-security/site-isolation/) and Chromium design documentation.
- **DEEP DIVE:** web.dev browser-rendering material, with process-model claims cross-checked against current Chromium docs.

**Checkpoint:** use browser DevTools to explain one page load across network, parser, DOM/layout/paint, script scheduling, storage, and process/security boundaries.

---

## S5 — Data & Concurrency

### M13 — Database Storage, Indexing & Query Execution

**Goal:** relational model, pages/records, indexes, query plans, declarative query versus physical execution, measurement, and space/write/read trade-offs.

- **PRIMARY:** [CMU 15-445/645 — Intro to Database Systems](https://15445.courses.cs.cmu.edu/) (use the current semester or archive appropriate to you).
- **REFERENCE:** [SQLite Query Planner](https://www.sqlite.org/queryplanner.html) and `EXPLAIN QUERY PLAN` docs.

**Checkpoint:** run the same query before/after an index on bounded data, verify result equivalence, inspect the actual plan, and explain why the planner is allowed to choose differently from your expectation.

### M14 — Transactions, Isolation, Recovery

**Goal:** transaction boundaries, atomicity, isolation/visibility, conflicts, rollback, logging/recovery, backup versus transaction semantics, and explicit failure models.

- **PRIMARY:** CMU 15-445 transaction/concurrency/recovery lectures.
- **REFERENCE:** [SQLite Transactions](https://www.sqlite.org/lang_transaction.html) and SQLite locking/journaling docs.

**Checkpoint:** use two database connections to produce a visibility/conflict scenario, predict the result, observe it, then explain which guarantee came from the DB and which came from your application protocol.

### M15 — Concurrency

**Goal:** interleavings, data races, atomicity, locks, condition variables, deadlock, threads/tasks, ownership, and invariants.

- **PRIMARY:** [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) — concurrency chapters.
- **REFERENCE:** POSIX/Linux pthread documentation or your language runtime's official concurrency docs.

**Checkpoint:** construct a small lost-update or ordering failure, write the invariant that failed, repair it, and explain why the repair works for all relevant interleavings rather than only the observed run.

---

## S6 — Distributed Systems & Modern Infrastructure

### M16 — Distributed Communication & Partial Failure

**Goal:** RPC/message boundaries, serialization, deadlines/timeouts, retry ambiguity, idempotency, backoff, partial failure, and why remote calls are not local calls.

- **PRIMARY:** [MIT 6.5840 / 6.824 Distributed Systems](https://pdos.csail.mit.edu/6.824/) — lectures/notes/readings; labs are optional.
- **DEEP DIVE:** *Designing Data-Intensive Applications* (Martin Kleppmann) for a durable conceptual synthesis.

**Checkpoint:** for one remote mutation, enumerate failures before send, after send/before response, duplicate delivery, and delayed response. Decide what the client can know in each case.

### M17 — Replication, Consistency & Consensus

**Goal:** replication, quorum reasoning, ordering/visibility models, linearizability, leader/term/log ideas, consensus purpose and limitations.

- **PRIMARY:** MIT 6.5840 replication/Raft/consistency material.
- **DEEP DIVE:** DDIA replication/consistency chapters.

**Checkpoint:** describe one read/write history and state exactly what guarantee you need. Do not use "consistent" without naming the ordering/visibility property.

### M18 — Coordination, Delivery & Distributed Transactions

**Goal:** duplicate delivery, queues, at-least-once implications, idempotency keys, leases/coordination, distributed transaction boundaries, 2PC trade-offs, and application-level invariants.

- **PRIMARY:** MIT 6.5840 transaction/sharding/coordination readings.
- **DEEP DIVE:** DDIA transactions and distributed-systems chapters.

**Checkpoint:** design one operation that remains correct under duplicate delivery and crash/retry. Identify the durable idempotency boundary and the business invariant it protects.

### M19 — Modern Infrastructure & Isolation

**Goal:** process/container boundary, namespaces, cgroups/resource control, deployment artifacts, reproducibility, supply-chain boundary, and when *not* to add orchestration.

- **PRIMARY / REFERENCE:** [Linux namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html).
- **REFERENCE:** [Linux kernel cgroup v2 documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html).
- **OPTIONAL CURRENT PRACTICE:** Docker/OCI/Kubernetes docs only after you understand the underlying process/namespace/resource mechanisms.

**Checkpoint:** inspect namespaces/cgroups for a process or container and explain which isolation/resource properties come from the kernel versus the container tool.

### M20 — Observability & Reliability Engineering

**Goal:** logs/metrics/traces, latency/error/saturation, instrumentation boundaries, correlation, SLI/SLO reasoning, incidents, and evidence without high-cardinality or sensitive-data mistakes.

- **PRIMARY:** [Google SRE Books](https://sre.google/books/) — Site Reliability Engineering and the SRE Workbook are readable online.
- **CURRENT REFERENCE:** [OpenTelemetry Documentation](https://opentelemetry.io/docs/) and [Signals](https://opentelemetry.io/docs/concepts/signals/).

**Checkpoint:** for one request, decide what belongs in a log, metric, and trace; then state one SLI and one failure that your chosen telemetry would miss.

---

## S7 — Security, Systems Judgment & Synthesis

### M21 — Trust, Cryptography & Secure Channels

**Goal:** threat model, trust boundary, hashing/MAC/signature/encryption distinctions, key material, randomness, certificates, secure channels, and "do not design your own crypto" judgment.

- **PRIMARY:** [Cryptopals](https://cryptopals.com/) as an optional experiential route for understanding why crypto misuse fails; do not treat implementing primitives as production guidance.
- **REFERENCE:** [RFC 9846 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc9846.html) and current NIST/IETF guidance for production claims.
- **SECURITY REFERENCE:** [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/).

**Checkpoint:** given a system claim such as "TLS makes this secure," name the protected property, trust anchor, key/identity assumption, and at least one property TLS does not provide.

### M22 — Authentication, Authorization & Secure Composition

**Goal:** AuthN versus AuthZ, session/token lifecycle, least privilege, deny-by-default, per-request authorization, enumeration, input/trust boundaries, and composition failures.

- **PRIMARY / CURRENT PRACTICE:** [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) and [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
- **CURRENT REFERENCE:** [RFC 9700 — OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700.html); for browser-based OAuth, also check the current IETF browser-app BCP.

**Checkpoint:** draw an authorization matrix for a small app. For every request ask: who is authenticated, what resource is addressed, what action is requested, and where the server enforces authorization.

### M23 — Systems Thinking & Technical Judgment

**Goal:** evaluate technologies using evidence, constraints, failure modes, cost, operational complexity, reversibility, and uncertainty rather than popularity.

- **PRIMARY:** [Google SRE Books](https://sre.google/books/) for reliability/operations trade-off reasoning.
- **DEEP DIVE:** DDIA for data-system trade-offs and failure-driven architecture reasoning.

**Checkpoint:** write a one-page Technology Card for a proposed component: problem, constraints, mechanism, failure modes, operational cost, measurement plan, alternatives, and a clear "when not to use it" section.

### M24 — Final System Synthesis / Defense

**Goal:** connect the entire stack and defend an architecture with evidence and bounded claims. A custom project is optional; you may analyze an existing system, external course project, work project (with confidential details removed), or the repo Mini Cloud.

- **PRIMARY:** revisit the strongest sources above for the actual system you choose.
- **SYNTHESIS REFERENCE:** Google SRE + OWASP + protocol/database/OS primary references relevant to your design.
- **OPTIONAL COMPANION:** repo Mini Cloud P0–P9 and M24 evidence templates.

**Checkpoint:** produce a system map that identifies state, interfaces, trust boundaries, failure boundaries, consistency/durability assumptions, observability, performance/cost risks, and one deliberate component you chose **not** to add. Every major claim should have evidence or an explicit uncertainty label.

---

# Recommended pacing

Do not optimize for finishing 25 modules quickly.

A good first traversal is:

- **S1:** learn enough representation/algorithms to reason precisely;
- **S2–S3:** spend extra time here if systems are new to you;
- **S4 and S5:** either order after S3 is acceptable;
- **S6:** only after networking + transaction/concurrency foundations feel concrete;
- **S7:** synthesis, not a bag of security buzzwords.

For each module, aim for roughly:

1. **Orientation** — 30–60 min: read the repo Lesson/module overview.
2. **Primary source** — several focused sessions; skip irrelevant assignments.
3. **One observation** — run or inspect something real.
4. **One explanation** — write the mechanism in your own words.
5. **One transfer question** — predict a related case you have not seen.

If you can explain the mechanism, make a useful prediction, and know where to look up exact details, move on.

# What not to do

- Do not finish an entire external university course just because it is linked.
- Do not implement a kernel, compiler, database, TCP stack, consensus system, or cloud platform unless that is your chosen deep dive.
- Do not memorize exact latency/version numbers as timeless facts.
- Do not treat AI output as authority; use it to generate hypotheses, comparisons, explanations, and search plans, then verify against primary sources.
- Do not confuse a green demo with understanding. Prefer a small experiment whose outcome you predicted.

# Existing repository exercises

The existing `labs/**`, `project/**`, and evidence templates remain valuable **optional companions**. They are especially useful when you want a ready-made bounded experiment instead of designing one yourself.

They are no longer a universal requirement for completing the resource-first roadmap.
