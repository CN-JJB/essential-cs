# Classic Lab and Source Expedition Candidates v0.1

Status: **DRAFTED — READY FOR WEB LEAD REVIEW**

This inventory supports later Lab Map and Research Dossier work. It does not select final Labs, implement experiments, or lock lesson placement. Suggested placement uses current macro areas `00`–`15`, not Issue #1 Stage names.

## 1. Research method

I searched authoritative university course pages, official lab handouts, standards, and official project documentation. A candidate was serious only when the primary source exposed an actual learner task or inspectable mechanism. I evaluated mechanism fit, transfer value, learner cognitive load, canonical Linux feasibility, setup/resource burden, failure observability, safety, maintenance, and provenance.

The decision rule is **Adopt → Adapt → Build**:

- **Adopt:** the mechanism and environment fit with little change.
- **Adapt:** retain the mechanism but narrow scope, update environment, improve safety, or reduce accidental load.
- **Reject:** valuable in its origin but unsuitable for this learner/profile/environment/scope, or not sufficiently verifiable.
- **Build:** allowed only after a documented gap; “AI can generate it” is not evidence.

Current claims were checked against primary sources on 2026-08-30. “Current” means current at that check, not permanent truth.

## 2. Source and provenance policy applied

- Standards/specifications outrank product summaries for protocol and guarantee claims.
- Official course/project pages establish what the exercise actually asks; search snippets do not.
- License is recorded from the authoritative page when visible. A course page’s educational availability is not assumed to grant redistribution or adaptation rights.
- Essential CS should summarize and link rather than copy third-party lab text/code. Adapted material needs origin, retained scope, changes/deletions, and license review.
- Where a page did not establish license, version, or reproducibility, I mark it **UNCERTAIN** rather than infer it.
- Current repositories and toolchains require a pre-release recheck; the inventory does not freeze versions.

## 3. Lab candidate inventory

| Area | Source and exact exercise | Mechanism / outcome | Suggested location | Decision and adaptation | Prerequisites / cognitive load | Linux, setup, runtime, safety | Provenance / license risk | Mini Cloud App relevance / Build need |
|---|---|---|---|---|---|---|---|---|
| `01` Information | CMU CS:APP3e **Data Lab** | Restricted C bit operations, two’s complement, floating representation; predicts representation consequences. | `01` | **Adapt**: retain restrictions and prediction; remove broad grading dependency and narrow function set. | Basic C and binary arithmetic; medium-high. | Linux/C compiler; self-contained tar but access may be required; low runtime, safe. | Official page says student handouts exist; exact redistribution/adaptation license not established; legal review before bundling. | Helps explain serialized IDs/bytes; custom project lab not necessary for core bit mechanisms. |
| `03` Machine / `04` Runtime | CMU CS:APP3e **Bomb Lab** | Disassembly, calling convention, debugger, control flow and data representation. | `03`/`04` | **Adapt**: use offline, non-networking bomb only; no grading server; focus on 1–2 phases and debugger evidence. | Assembly reading and debugger basics; high if full lab. | Linux x86-64; official page notes a runnable offline bomb; architecture mismatch for ARM hosts possible. Safe if local; do not use exploit targets. | Page identifies authorship and distribution, but redistribution rights for course bundle need review. | Strong Source Expedition after machine/runtime; not necessary to build project feature. |
| `03` Machine | CS:APP3e **Cache Lab** | Cache simulator plus locality-driven matrix transpose; measures misses and software/hardware interaction. | `03` | **Adapt**: retain trace/simulator and one transpose; require metric/environment/data disclosure. | C, arrays, basic cache model; high. | Linux x86-64 and Valgrind per official page; setup and architecture constraints; safe. | Official handouts/tar access; license/redistribution uncertain. | Supports project performance reasoning, but project should use DB/query measurements instead. |
| `05` OS | MIT 6.1810 **xv6 and Unix utilities** | System calls, file descriptors, processes, fork/exec/wait, directories and user/kernel boundary. | `05` | **Adapt**: choose `sleep`, `find`, and `exec` slices; retain xv6’s small real kernel; do not require full lab sequence. | Basic C, shell, pointers; medium-high. | RISC-V cross compiler, QEMU, 128MB sample VM; setup nontrivial, but official tools exist. Safe local emulator. | 2025 lab page displays CC BY 3.0 US; source repository and xv6 book attribution still need recorded before adaptation. | Directly illuminates P1/P3 process boundaries; no custom OS toy needed. |
| `05`/`06` OS/Storage | MIT 6.1810 **xv6 system calls / file system / threads labs** | Kernel entry, virtual memory, file systems, locks and scheduling. | `05`/`06`/`10` | **Adapt**: one inspect-and-change slice after a mental model; do not assign a full teaching OS. | C, pointers, prior xv6 orientation; high. | QEMU/cross toolchain; compile/runtime burden medium-high; safe. | Same CC/source review requirement; exact lab-version maintenance risk. | Explains where app syscalls/files/locks go; project need is a Source Expedition, not another implementation. |
| `07` Networking | Stanford CS144 **Checkpoints 0–3: byte stream, TCP receiver, TCP sender** | Encapsulation, reliable byte stream, sequence/acknowledgment, retransmission and flow/congestion concepts. | `07` | **Adapt**: one checkpoint or receiver core; retain packet traces and invariants; omit full semester pacing and large framework. | C++ and networking basics; high. | Linux toolchain; current site lists Fall 2025; compile/setup and debugging burden high, safe local. | Site’s licensing/redistribution terms for handouts/code not established; do not copy. | Strong foundation for P3 timeout/retry reasoning; no custom TCP implementation in project. |
| `07`/`08` Web | IETF **RFC 9110 HTTP semantics** plus `curl`/local server inspection | Request/response, statelessness, representations, intermediaries, caches, origins and status semantics. | `07`/`08` | **Adapt**: source expedition/measurement lab rather than implementing HTTP; retain wire inspection and semantic predictions. | P1 process/interface and basic networking; medium. | Linux `curl`/packet tools; minimal setup; safe local targets only. | RFC copyright/license permits reading/linking but extracted text/code requires IETF terms; summarize rather than copy. | Directly supports P1/P3; custom web framework lab unnecessary. |
| `09` Databases | PostgreSQL official **EXPLAIN** and transaction isolation exercises | Plans, estimates versus actuals, buffers, MVCC/isolation, serialization failures and retry. | `09`/`10` | **Adapt**: use a small local PostgreSQL instance only as an optional comparison after SQLite; retain controlled datasets and rollback. | SQL and transactions; medium. | Linux packages/container possible; server setup medium; safe local data. | Official docs are authoritative; license for documentation is not a redistribution assumption. Current version is 18 at check date; recheck. | Directly supports P4–P6; PostgreSQL should not replace the baseline without a constraint. |
| `10` Concurrency | OSTEP v1.10 **Threads (Semaphores) — Homework (Code)**, backed by the official OSTEP homework repository | Real semaphore exercises covering ordering/synchronization problems (including fork/join, rendezvous, barriers, reader-writer and starvation); exposes interleavings, blocking, invariants and progress. | `10` | **Adapt**: select 1–2 bounded exercises after race/lock mental models; require prediction + trace + invariant explanation; do not assign the whole set. | Threads/shared state and basic C; medium. | Native POSIX semaphores on Linux; small local programs, low runtime, safe. | Official OSTEP homework page identifies the code homework and links the maintained homework repository; redistribution/adaptation license still needs per-repo verification, so link/attribute rather than bundle until cleared. | Strong mechanism candidate before P5; the project race harness remains an integration exercise, not the canonical concurrency lab. |
| `11` Distributed | MIT 6.033 **Computer System Engineering** written/project cases | Modularity, naming, performance, security/privacy, fault tolerance, atomicity, recovery and coordination. | `11`/`14` | **Adapt**: adopt case-analysis method and one bounded fault-tolerant transaction case; do not copy full assignments. | Prior system models and writing judgment; high conceptual, low setup. | PDFs/readings; no runtime; safe. | MIT OCW page provides course resources; individual assignment licensing/adaptation must be checked before reuse. | Best companion to P9/System Defense; no distributed service implementation required. |
| `12` Infrastructure | Docker official **What is a container?** hands-on | Container as isolated process, image/filesystem/port boundary, contrast with VM. | `12` | **Adapt**: local comparison of native process and one container; inspect namespaces/files/ports; avoid Docker Desktop dependency. | OS process model; low-medium. | Docker/engine prerequisite and host support; resource burden low-medium; safe local image only. | Official docs link/source license not recorded here; summarize/link, do not copy screenshots/text. | Directly supports P7; container remains optional, not canonical prerequisite. |
| `12`/`14` Observability | OpenTelemetry official **Observability primer** plus local logs/metrics/traces | Signals, spans/traces, reliability, SLI/SLO vocabulary, correlation and diagnostic limits. | `12`/`14` | **Adapt**: start with structured logs/timers; add one local trace only for a question; avoid backend vendor stack. | P3 boundary and P4 measurement; medium. | Python instrumentation and local collector optional; data/CPU burden medium; redact secrets/private content. | OpenTelemetry project/docs provenance is clear; exact reuse license and dependency versions need recheck. | Directly supports P8; project’s minimal telemetry is a natural integration case. |
| `13` Security | CS:APP3e **Attack Lab** | Stack discipline and memory corruption mechanics. | `13` | **Reject for Core**; retain only as a safety-reviewed historical case or controlled course-owned sandbox. | High; offensive framing and exploit construction. | Official targets are local but exploit material creates safety/maintenance burden; architecture/toolchain drift. | Redistribution/adaptation and target provenance need legal review. | Does not fit defense-first scope; use secure coding and authorization boundary cases instead. |
| `13` Security | Local OWASP-style **course-owned vulnerable app** (future candidate family) | Real vulnerable mechanism against authorized local target, followed by fix and regression test. | `13` | **Build only if dossier finds no suitable adoptable safe target**; require local sandbox, reset, non-public binding and defense-first framing. | Web/security basics; medium-high. | Linux reproducible, but maintenance and safe-default burden high. | Must be original/Apache-2.0 or license-cleared; provenance open until selected. | Could exercise P2 auth/authorization; custom Build gap remains conditional. |
| `14` Measurement | Stanford CS144 **Checkpoint 4: measuring the real world** | Measurement design, real-world network behavior and limits of causal claims. | `07`/`14` | **Adapt**: local controlled network measurements plus explicit environment/warmup/repetition/distribution record. | Networking basics; medium. | Linux tools; network variability; safe. | Current assignment page confirms checkpoint; handout license/adaptation rights not established. | Strongly supports P3/P4; no fake benchmark should be built. |
| `15` System judgment | MIT 6.033 case discussions and design/project prompts | Defend alternatives, requirements, failure assumptions and trade-offs. | `14`/`15` | **Adapt**: use as a defense rubric input, not a copied final assessment. | Full Core traversal; high reasoning, low setup. | No runtime; safe. | Assignment-specific reuse/license needs review. | Directly supports P9; project defense should remain Essential CS-owned. |

## 4. Source Expedition inventory

| Expedition | Principle already taught | Inspect only | Reality added | Ignore / stopping point | Load / maturity / suitability |
|---|---|---|---|---|---|
| **xv6 utility path** — MIT 6.1810 2025 | Process, syscall, file descriptor, fork/exec | `user/find.c`, syscall declaration/entry path, one kernel implementation such as `sys_pause` | The “simple” Unix interface crosses generated/user/kernel code and a real file system. | Ignore scheduler internals and unrelated labs; stop after tracing one utility end-to-end and one controlled change. | Medium-high; maintained annual course source, current 2025 page. **Adapt.** |
| **CS:APP malloc driver** | Address space, pointers, allocation, throughput/utilization | `mdriver` trace loop and allocator interface; do not inspect instructor solution | Evaluation itself encodes a space/time trade-off and workload assumptions. | Ignore allocator optimizations not needed to explain traces; stop after one trace and two metrics. | High; official material exists but license/access risk. **Adapt/possibly reject if redistribution blocked.** |
| **CS:APP proxy lab** | Sockets, HTTP, concurrency, caching | Proxy request path, cache key/eviction location, worker synchronization | A “small” proxy combines byte ordering, file I/O, process/thread control, cache correctness and synchronization. | Ignore full web compatibility and internet target; local authorized origin only; stop at one request and one cache-hit/miss trace. | High; official page describes a concurrent caching proxy; license/setup risk. **Adapt.** |
| **CS144 TCP receiver** | Byte streams, sequence numbers, invariants | Reassembler and acknowledgment decision locations | TCP segments do not preserve application write boundaries; receiver correctness is an invariant over gaps/duplicates. | Ignore congestion control and full sender; stop after one out-of-order/duplicate trace. | High; current course, C++ burden. **Adapt.** |
| **PostgreSQL EXPLAIN** | Query cost and indexing hypothesis | One plan node showing sequential versus index scan; compare estimated/actual rows | A planner is an estimator with workload statistics, not an oracle; instrumentation has overhead. | Ignore every planner knob and production tuning; stop after one query, one dataset scale, and one changed plan. | Medium; maintained official docs, version-sensitive. **Adopt as a bounded source expedition.** |
| **HTTP origin/intermediary path** — RFC 9110 | Layering, interfaces, stateless request/response | Sections on origin, gateway, cache, and one local `curl -v` exchange | HTTP semantics survive across versions; intermediaries relocate authority, state and failure. | Ignore full ABNF and browser implementation; stop after mapping one request/response and one cache/proxy distinction. | Medium; stable standard. **Adopt/Adapt.** |
| **OpenTelemetry trace path** | Observation, timing, causality | One instrumentation call, one span creation/export boundary, one trace viewer representation | Telemetry is data with cost, missingness, cardinality and privacy constraints; a trace is not proof of cause by itself. | Ignore collector internals/vendors; stop after one request and one injected delay. | Medium; actively maintained current docs, version-sensitive. **Adapt.** |
| **MIT 6.033 fault-tolerant transaction case** | Atomicity, failure, recovery | One diagram/request path from coordinator to primary/backup | A design can preserve an invariant while exposing availability, recovery and coordination costs. | Ignore the full assignment and unrelated system; stop at one failure trace and one alternative. | High conceptual; mature OCW 2018 source. **Adapt.** |

## 5. Adopt shortlist

These are the strongest low-copy, high-transfer candidates, subject to final license/environment review:

1. **RFC 9110 + local wire inspection** for HTTP semantics, origins, intermediaries and caching.
2. **PostgreSQL `EXPLAIN`/isolation reading and controlled query exercise** after SQLite fundamentals.
3. **MIT xv6 one-utility trace** after process/syscall concepts, narrowed to one end-to-end path.
4. **OpenTelemetry signals/trace comparison** after learners formulate a diagnostic question.
5. **MIT 6.033 bounded case analysis** for failure, atomicity, privacy and system judgment.

“Adopt” means adopt the mechanism and activity pattern; it does not mean copy third-party prose, code, screenshots, or grading infrastructure.

## 6. Adapt shortlist

- CS:APP Data Lab, Cache Lab, Malloc Lab, and Proxy Lab: valuable but high C/toolchain/load or license burden.
- MIT xv6 syscall/file-system/thread labs: powerful real mechanism, but select one slice rather than a whole OS course.
- Stanford CS144 checkpoints: excellent network mechanisms, but C++ and assignment scale exceed early Essential CS needs.
- Docker container exercise: use native Linux process comparison and optional container branch, not Docker Desktop as a hidden prerequisite.
- OpenTelemetry: logs/timers first, trace backend second; retain the diagnostic question.
- CS:APP Bomb Lab: offline and narrow only; avoid grading server, exploit framing, and architecture assumptions.
- Stanford measurement checkpoint: adapt to controlled local conditions and require benchmark metadata.

## 7. Reject examples

- **CS:APP Attack Lab as a Core security lab:** mechanism is real, but exploit construction is not necessary for defense-first scope; safety, architecture, target and license burden are high. A later authorized security dossier may reconsider a tightly bounded variant.
- **Full xv6 implementation sequence:** excellent university OS course, but reproducing the complete sequence would turn the project into an OS implementation course and overwhelm the shared world model.
- **Full CS144 semester checkpoint sequence:** excellent but too much C++/network-stack implementation for a first traversal; use one invariant-rich checkpoint.
- **Generic “build a web app” or “add Redis/Kubernetes” demos:** no classic mechanism evidence, high accidental complexity, and product/framework tunnel vision.
- **Uncontrolled public benchmark or penetration target:** fails reproducibility/safety and confounds observation with causal claim.
- **Custom fake distributed-system simulator before real mechanisms:** violates real-mechanism preference when local process/database/network failure can be observed directly.

## 8. Remaining Build gaps

Build is currently justified only conditionally:

1. **Integrated Mini Cloud App boundary experiment:** Existing classic labs teach pieces, not the deliberate P0–P9 evolution. A small original integration harness may be required later, but it must be a project checkpoint, not a replacement for classic labs.
2. **Safe authorization/privacy experiment:** Existing security labs inspected here either over-index on exploitation or have uncertain redistribution/safety boundaries. Build a course-owned target only after a security dossier defines safe defaults, reset, scope, and license.
3. **Cross-layer failure/observability exercise:** Existing candidates cover either distributed case reasoning or telemetry tooling. A small original fixture may be needed to inject one timeout/latency/storage failure and correlate it across logs, metrics, and state—only if P8 cannot be achieved by adapting the Mini Cloud App itself.
4. **Concurrency-to-application integration:** OSTEP's semaphore/concurrency exercises and database isolation materials teach mechanisms separately. A project-specific race harness may still be needed for P5, but only as an integration checkpoint after adopting/adapting a proven concurrency lab.

No custom final Lab is implemented by this artifact.

## 9. Licensing, provenance, and maintenance risks

| Candidate family | Risk | Required follow-up |
|---|---|---|
| CS:APP labs | Official pages provide handouts/tars and authorship, but redistribution/adaptation terms are not established in the inspected pages; instructor account may be required. | Obtain permission/license before bundling; otherwise link and summarize only. |
| MIT xv6 / 6.1810 | 2025 lab page displays CC BY 3.0 US; source/book and exact current repository terms still need attribution review. | Record exact repository commit, license files, retained/changed files, and current toolchain. |
| Stanford CS144 | Current 2025 course and assignments are visible; handout/source redistribution/adaptation terms were not established in inspected pages. | Ask/verify rights; do not copy assignment text/code. |
| MIT OCW 6.033 | Course page and resources are available; individual assignment reuse terms may differ. | Verify OCW/material license per item before adaptation. |
| RFCs | IETF Trust terms govern documents; extracted code components have specific license requirements. | Link and paraphrase; include required notice if any text/code is extracted. |
| PostgreSQL/Docker/OpenTelemetry docs | Current official docs are maintained and version-sensitive; documentation/code licenses were not fully audited in this pass. | Verify repository/docs license and pin versions in the later dossier. |
| Security targets | Target provenance and safe defaults are critical. | Prefer original Apache-2.0 course-owned code or a clearly licensed educational target; isolate locally. |

## 10. Reconciliation notes

- **Issue #1:** Use macro placement now; reconcile exact Stage/Lesson location after the dependency graph settles.
- **Issue #2:** Add candidates only for verified external coverage gaps; do not inflate this inventory for symmetry.
- **Issue #3:** P0–P9 project opportunities are not final Labs. Select classic candidates that illuminate the same mechanism, then decide whether an integration checkpoint remains necessary.
- **Later Research Dossiers:** Recheck licenses, versions, architecture prerequisites, canonical Linux reproducibility, learner load, and current source status before final selection.
- **Final Lab Map:** Must decide required versus optional, Adopt versus Adapt, and whether each activity has a smoke test, cleanup/reset, controlled failure, exit criteria, and provenance record.

## 11. Evidence checked

- OSTEP, [Homework](https://pages.cs.wisc.edu/~remzi/OSTEP/Homework/homework.html), especially **Threads (Semaphores) — Homework (Code)** and the linked maintained homework repository: exact concurrency coding source for synchronization/invariant exercises; adaptation/redistribution license still requires per-repository verification.
- MIT, [6.1810 Fall 2025 overview](https://pdos.csail.mit.edu/6.1810/2025/overview.html), and [xv6 Unix utilities lab](https://pdos.csail.mit.edu/6.1810/2025/labs/util.html): current course scope, xv6 rationale, actual exercises, QEMU/toolchain and CC BY 3.0 US notice.
- Stanford, [CS 144 Fall 2025 course and checkpoints](https://cs144.github.io/): actual checkpoints 0–7, including TCP, measurement, router and creative project work.
- CMU, [CS:APP3e lab assignments](https://csapp.cs.cmu.edu/3e/labs.html), and [Malloc Lab instructor README](https://csapp.cs.cmu.edu/3e/README-malloclab): actual Data/Bomb/Cache/Shell/Malloc/Proxy tasks, Linux/architecture notes and author attribution.
- MIT OpenCourseWare, [6.033 Computer System Engineering](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/): current page for course scope and resource types.
- PostgreSQL, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) and [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html): current PostgreSQL 18 behavior, plans, estimates, buffers, and instrumentation caveats.
- Docker, [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container.md): current process/container/VM explanation.
- OpenTelemetry, [Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/): current telemetry, reliability, spans and traces guidance; page reports last modified 2026-04-23.
- IETF, [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) and [RFC 9293 TCP](https://www.rfc-editor.org/rfc/rfc9293.html): standards for HTTP semantics/intermediaries/caches and TCP byte-stream/reliability/failure mechanisms.

## 12. Review focus

The highest-risk decisions for Lead review are: whether any CS:APP/Stanford materials can legally be adapted; whether xv6/CS144 setup is proportionate to Essential CS load; whether security Build gaps can be made safe and reproducible; and whether the Mini Cloud App should carry integration experiments that no classic lab can provide.
