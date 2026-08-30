# Curriculum Map

Status: **Blueprint v0.1 — reconciled, Lead-accepted** (Issue #9 integration; Blueprint remains ACTIVE until exit criteria are complete)

This is the canonical reference for what the Core teaches, in which Stage order,
through which Modules, Labs, Source Expeditions, and Mini Cloud App milestones.
It is not a lesson list. Detail lives in:

- `meta/blueprint/core-stage-module-lesson-map-v0.1.md` — Module/Lesson boundaries
- `meta/blueprint/dependency-graph-v0.1.md` — H/S/R/P prerequisite semantics
- `meta/blueprint/lab-source-selection-map-v0.1.md` — Lab & Source Expedition selection
- `meta/blueprint/final-reconciliation-v0.1.md` — issue #9 integration record, Mini Cloud App P0–P9 canonical Module mapping
- `meta/COMPETENCY_MATRIX.md` — capability growth and Stage exit evidence
- `meta/CONCEPT_REGISTRY.md` — canonical concept homes (EC-CON-001–018)

## Macro spine (D-007) and Stage mapping

The 16 macro areas below are mapped to 7 learner-visible Stages. Stage order is the
**default narrative**; hard prerequisites come from the Module DAG (see
`dependency-graph-v0.1.md`).

| Order | Area | Core role | Stage | Modules | Lesson status |
|---|---|---|---|---|---|
| 00 | The Map | Whole-system mental model; question set; Mini Cloud App surface | S1 | M00 | PLANNED |
| 01 | Information & Representation | Bits, numbers, text, serialization, size | S1 | M01 | PLANNED |
| 02 | Computation & Algorithms | Computation model, complexity, essential data structures | S1 | M02 | PLANNED |
| 03 | Machine | ISA, execution, memory hierarchy, locality | S2 | M03, M04 | PLANNED |
| 04 | Languages, Runtime & Compiler | Source → representation → runtime → machine | S2 | M05 | PLANNED |
| 05 | Operating Systems | Process, syscall, virtual memory, scheduling, files | S3 | M06, M07, M08 | PLANNED |
| 06 | Storage Systems | Filesystem → page cache → SSD → durability | S3 | M08, M09 | PLANNED |
| 07 | Networking | IP/DNS/TCP/UDP/QUIC/TLS/HTTP/proxies/timeouts | S4 | M10, M11 | PLANNED |
| 08 | Web & Browser Platform | Browser as integrated modern system case | S4 | M12 | PLANNED |
| 09 | Databases | Storage/index/query/transactions/recovery | S5 | M13, M14 | PLANNED |
| 10 | Concurrency | Race/atomicity/locks/async/isolation/idempotency | S5 | M15 | PLANNED |
| 11 | Distributed Systems | Partial failure, replication, consistency, queues, consensus | S6 | M16, M17, M18 | PLANNED |
| 12 | Modern Infrastructure | Containers/cloud/deployment/observability/supply chain | S6 | M19, M20 | PLANNED |
| 13 | Security Synthesis | Trust boundaries, crypto use, authn/authz, secure composition | S7 | M21, M22 | PLANNED |
| 14 | Systems Thinking & Judgment | Measurement, cost, failure, technology evaluation | S7 | M23 | PLANNED |
| 15 | Final System Defense | Integrated architecture and trade-off defense | S7 | M24 | PLANNED |

## Stages

| Stage | Name | Macro areas | Capability gained | Stage exit evidence |
|---|---|---|---|---|
| S1 | 计算的底座 — Foundations of Computation | 00–02 | Trace & Explain at representation level; structure, size, algorithm cost trade-offs | Representation round-trip; size/complexity estimate; invariant; one data-tool trace; toolchain evidence packet (L00-02) |
| S2 | 机器 — The Machine (ISA, Execution, Memory Hierarchy, Language→Machine) | 03–04 | Observe & Diagnose at machine level; disassembly/debugger; locality measurement | Disassembly/debugger record; controlled locality measurement; source-to-runtime trace; applied measurement-uncertainty pattern assessment (L04-02) |
| S3 | 操作系统与持久化 — OS: Processes, Memory, Files (+ Storage) | 05–06 | Trace & Diagnose across process/memory/files/storage boundary | Syscall/process trace; address-space observation; file-I/O and durability claims with loss-bound estimate |
| S4 | 网络与浏览器 — Networking, the Web, Browser as integrated case | 07–08 | Trace & Explain end-to-end request; estimate network cost | Packet/socket/request trace; timeout distinction; cache/intermediary or proxy comparison; browser performance/origin observation |
| S5 | 数据与并发 — Databases, Transactions, Concurrency | 09–10 | Correctness & Judge at data/concurrency level | Query plan + controlled benchmark; transaction anomaly; race/interleaving trace; invariant-preserving fix |
| S6 | 分布式与现代基础设施 — Distributed Systems, Cloud, Infrastructure | 11–12 | Judge & Estimate at scale; evidence-driven operations | Timeout/retry trace; replication/consistency scenario case; duplicate-delivery judgment; reproducible deployment comparison; controlled-incident packet |
| S7 | 安全综合·系统判断·最终答辩 — Security Synthesis, Systems Thinking, Final Defense | 13–15 | Judge & Learn-New-Tech at whole-system level | Trust map; certificate/signature observation; Technology Card + measurement design; complete System Defense evidence packet |

### Recommended first-time learner path vs hard prerequisites

```
S1 → S2 → S3
            ├─→ S4 ─┐
            └─→ S5 ─┴─→ S6 → S7
```

- **Default narrative** (pedagogical preference, not `H`): `S1 → S2 → S3 → S4 → S5 → S6 → S7` — a request-centric journey. A data/state-first learner may take `S3 → S5 → S4 → S6 → S7`; no Stage pair changes.
- **Hard structure:** `S1 → S2 → S3`; `S4` and `S5` are **partially independent after `S3`**; `S6` needs inputs from **both** the networking branch (`M10`) and the data/concurrency branch (`M14`, `M15`); `S7` requires a complete shared traversal.
- The Module DAG remains authoritative. Stage narrative is not dependency.

## Module dependency summary

- 25 Core Modules (`M00`–`M24`) under the DAG; **62 structured H/S edges** (40 `H`, 22 `S`) plus `R`/`P` relationships (see `dependency-graph-v0.1.md` §2).
- Corrected semantics preserved: no S4→S5 Stage edge; `M14 → M16` soft; `M14 → M17` hard; `M03/M12 → M15` soft.
- **Acyclic verified** after Issue #9 integration (method: topological ordering; all H/S edges point from earlier home regions to later dependent regions; `R`/`P` edges are non-ordering by definition).
- Hidden-prerequisite resolutions (Issue #9):
  - toolchain/shell/Git → first home `L00-02` with explicit learner outcomes + REQUIRED-lab entry gate (course discipline, not a DAG edge);
  - applied measurement-uncertainty → first home `L04-02` (M04), revisits M13/M16/M17/M20/M23; no standalone math Module;
  - clock semantics (wall vs monotonic) → resolved at `L20-01`/`L23-01`;
  - canonical environment repetition → environment preflight at M03/M06/M13 Stage boundaries + lab-entry gate.

## Horizontal threads

Correctness & Invariants; Failure; Debugging; Measurement & Performance; Security; Cost/Resource Economics; Technical Literacy; API/Interface Design; Software Engineering; Privacy/Data Responsibility; Napkin Math.

Reconciled additions (Issue #9, per accepted audit dispositions):

- **Applied measurement-uncertainty toolkit** (R1/R7) — sub-thread under Measurement & Performance: repeated measurements, distributions, median/percentiles when useful, uncertainty/variation, inference limits, order-of-magnitude reasoning. First assessed home: M04 `L04-02`; revisited at M13/M16/M17/M20/M23. Reliability/failure probability remains just-in-time inside M16/M17.
- **Experimental pattern** (R7) — question/hypothesis → baseline → controlled change → metric/environment/workload → repetitions/distribution when relevant → observation → competing explanation → bounded conclusion. First assessed home: M04 `L04-02`; revisited at M20 `L20-01`; consolidated at M23 `L23-01`.
- **Horizontal security/privacy evidence** (R8) — M07 `L07-01` is the first concrete **trust-boundary** home (while distinguishing trust from isolation); M11 TLS and M12 origin/site isolation revisit it; M19 adds deployment/supply-chain boundaries; synthesis at M21/M22; judgment at M23/M24. Evidence is required across P0–P9. Accessibility stays with OQ-BP-003, not resolved by security.

## Mini Cloud App (P0–P9)

A single-process, locally bounded, deliberately simple notes/bookmarks service used as the recurring integration surface and final System Defense case.

| Milestone | Constraint introduced | Primary Module home | Competency focus |
|---|---|---|---|
| P0 | One process, one durable collection | M00 (+M01/M08/M09/M13 revisits) | Trace, Explain, Correctness, Estimate |
| P1 | Process boundary, narrow interface | M06/M11 (M05/M10 support) | Trace, Explain, Diagnose, Correctness |
| P2 | Multiple users, explicit trust boundaries | M21/M22 (M12 revisit; early local fixture) | Judge, Correctness, Explain, Diagnose |
| P3 | Real local network path, bounded failure | M10/M11 (M16 revisit) | Trace, Diagnose, Judge, Estimate, Correctness |
| P4 | Query shape, indexes, measurement | M13 (M23 revisit) | Observe, Diagnose, Estimate, Judge, Correctness |
| P5 | Concurrent requests, transactional correctness | M14/M15 | Correctness, Diagnose, Explain, Judge |
| P6 | Durable recovery, operational evidence | M09/M14 (M19/M20 operational revisits) | Observe, Correctness, Judge, Estimate |
| P7 | Deployment boundary, reproducible environment | M19 (native path canonical; container Optional) | Explain, Observe, Judge, Learn-New-Tech |
| P8 | Instrumentation before scaling | M20 (M23/M24 revisits) | Observe, Diagnose, Judge, Correctness |
| P9 | System Defense under changed constraints | M23/M24 | All eight |

**Canonical per-milestone detail** (mechanism exposed, competency exercised, Module/Lesson dependency, first-intro vs application/revisit, deliberately-not-added, When-NOT-to-add, Beyond-the-Project companion case): `meta/blueprint/final-reconciliation-v0.1.md` §6.

**Guardrails** (accepted): native Linux path canonical; SQLite baseline; PostgreSQL Optional comparison; cache/queue/replica/container/proxy NOT mandatory; rejection ("do not add this component") is a passing P9 outcome; project never replaces mechanism Labs.

## Labs and Source Expeditions

Selection per `meta/blueprint/lab-source-selection-map-v0.1.md` (Adopt → Adapt → Build; no implementation in Blueprint).

### Required Labs (5)

| ID | Module/lab home | Canonical mechanism | Competencies assessed | Mini Cloud | Required before later Stage? | Environment prerequisite |
|---|---|---|---|---|---|---|
| LAB-REQ-01 | M11 (S4), revisit M12 | HTTP interface, origin, intermediary, conditional-cache semantics | Trace, Explain, Observe, Correctness, Judge | P1/P3 | Yes — completes S4 network/interface evidence needed by M12 and by S6 (M16 RPC framing); not a DAG edge | Canonical Linux shell; `curl`; localhost-only server; M00 evidence habits (lab-entry gate) |
| LAB-REQ-02 | M06 (S3), short M08 revisit | User program → syscall API → syscall dispatch → kernel route | Trace, Explain, Observe, Diagnose, Learn-New-Tech | P1/P3 (app process boundary) | Yes — completes S3 process/syscall evidence used across the spine | Canonical Linux; QEMU; RISC-V cross-toolchain (pinned); shell/Git gate |
| LAB-REQ-03 | M15 (S5) | POSIX thread interleaving, defined lost-update (C11 atomic load/store), mutex repair, condition-variable rendezvous, deadlock boundary | Correctness, Trace, Diagnose, Explain, Judge | P5 | Yes — M15 is an `H` input to M16 (S6) | Canonical Linux; `gcc -pthread`; user account; no network |
| LAB-REQ-04 | M13 (S5), revisit M23 | SQLite query shape, scan vs index, plan inspection, workload/data-size, write/space trade-offs, planner limits | Observe, Trace, Explain, Correctness, Diagnose, Estimate, Judge | P4 | Yes — M13 is `H` for M14 and the database branch must precede S6 | Canonical Linux; pinned `sqlite3` CLI; Python stdlib; synthetic fixture |
| LAB-REQ-05 | M14 (S5), revisits M09/M15 | SQLite transaction boundaries, isolation/committed-only visibility, rollback, process-interruption recovery, backup vs durability, journal mode | Correctness, Trace, Observe, Diagnose, Explain, Judge, Estimate | P5/P6 | Yes — M14 is `H` for M17; database correctness precedes S6/S7 evidence gates | Canonical Linux; `sqlite3`; two local connections; rollback-journal baseline; writable temp dir |

### Optional Labs (5)

| ID | Module home | Candidate | Status |
|---|---|---|---|
| LAB-OPT-01 | M01/M03 | CS:APP Data Lab narrow bit-representation slice | Adapt — rights-gated (link-only until cleared) |
| LAB-OPT-02 | M10/M16 | Stanford CS144 Checkpoint 2 TCP receiver slice | Adapt — rights-gated (link-only until cleared) |
| LAB-OPT-03 | M13/M14 | PostgreSQL 18 `EXPLAIN` + isolation comparison | Adapt — Optional after SQLite baseline |
| LAB-OPT-04 | M20 | Local OpenTelemetry trace vs logs/timers | Adapt — license-cleared in principle; pinned versions |
| LAB-OPT-05 | M15 | OSTEP v1.10 Threads/Semaphores rendezvous | Adopt — link-only (license unresolved) |

### Source Expeditions (5)

| ID | Module | Source route |
|---|---|---|
| EXP-01 | M06 | xv6 utility-to-kernel path (MIT-licensed software; page material CC BY 3.0 US as marked) |
| EXP-02 | M13 | PostgreSQL planner cost + buffer management (PostgreSQL License) |
| EXP-03 | M12 | Chromium process model & site isolation (BSD-style notices) |
| EXP-04 | M20 | OpenTelemetry span API vs SDK lifecycle (docs CC BY 4.0; code Apache-2.0) |
| EXP-05 | M17, revisits M23/M24 | MIT 6.033 replication/transactions/logging case (OCW CC BY-NC-SA 4.0; link/paraphrase only) |

No Required Lab bundles third-party material with unresolved reuse rights. OSTEP remains Optional/link-only. No full consensus implementation, full kernel/network-stack/compiler/DB-engine build is assigned to Core (Deep Dive boundaries per map §9).

## Concept Registry

Initial canonical population: 18 concepts `EC-CON-001`–`EC-CON-018` (the 15 Big Ideas as concepts + Process, Durability, Trust Boundary as concepts only). Big Ideas remain 15; no new Big Idea was created. Trust Boundary's first home is M07 `L07-01`; M21 is its security-synthesis revisit.

Deferred from first population (explicit): `Consensus` (concept is Core at M17 per R10; stable ID deferred), schema-evolution/provenance (application pattern over Representation/State/Interface/Invariant), AI-literacy/HCI concepts (OQ-BP-001 / OQ-BP-003 RFC-gated). No product names/commands/frameworks are concept IDs.

## Assessment

Per-milestone and per-Stage assessment follows the evidence-packet model in `meta/COMPETENCY_MATRIX.md` (predict/specify → observe/break → explain-to-mechanism → invariant/uncertainty → judge/estimate → transfer). Stage exits assess capability, not topic recall; the Final System Defense aggregates prior evidence.

## Scope rule

Core must preserve a complete shared modern computing worldview. Deep Dives may specialize beyond that baseline without consuming the first traversal. Complexity must justify itself; no compressed CS degree, no training for web development, no product/vendor syllabus.
