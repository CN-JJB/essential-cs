# Competency Matrix

Status: **Blueprint v0.1 — reconciled** (Issue #9 integration applied; Lead review pending)

The Curriculum Map records what is taught. This matrix records what learners must be able to do, where each competency grows, and which evidence gates prove it. It replaces the original scaffold with the integrated model from Issue #15 (accepted) plus the Issue #9 audit dispositions.

## Core competencies

| Competency | Meaning |
|---|---|
| Trace | Follow data/control/state across system layers |
| Explain | Build an accurate mental model and explain mechanism |
| Observe | Use real tools to inspect hidden behavior |
| Diagnose | Form hypotheses, measure, locate, and explain failures/performance |
| Correctness | State specifications/invariants and reason about violations |
| Judge | Compare alternatives, trade-offs, failure modes, and boundaries |
| Estimate | Back-of-envelope latency, throughput, storage, memory, bandwidth, cost |
| Learn-New-Tech | Investigate unfamiliar technology using docs/specs/source/evidence |

## Notation

| Symbol | Meaning |
|---|---|
| `I` | Introduce (first assessed teaching of the minimum capability, usually at the named Module/Lesson) |
| `P` | Practice (apply to a new mechanism/context — never a second canonical definition) |
| `A` | Assess / exit evidence (Stage exit evidence packet, Required Lab evidence, or System Defense item) |

A cell missing a competency means that Stage does **not** teach it — deliberately. Each competency has one real introduction, grows across the course, and is finally assessed at the System Defense.

## Stage × Competency growth matrix

| Stage | Trace | Explain | Observe | Diagnose | Correctness | Judge | Estimate | Learn-New-Tech |
|---|---|---|---|---|---|---|---|---|
| S1 Foundations | `I→A` M00 trace one request; M01–02 data-structure traces | `I→A` M00 mental model; M01 representation, M02 complexity | `I` M00 real tool orientation; M01 hexdump | `P` M02 first bug hunt (invariant violation) | `I→A` M02 spec/invariant/correctness (M01 application) | `I→A` M02 trade-off language (container choice) | `I→A` M01 sizes, M02 operations | `I` M00 tooling/source reading (evidence artifact) |
| S2 Machine | `I→A` M03 instruction/call-frame trace; M05 source→machine | `P→A` M03 machine evidence; M05 source-to-runtime claim | `I→A` M03 debugger/disassembly; M04 controlled measurement | `I→A` M03 crash; M04 measured perf diagnosis | `P` M05 types as invariants | `P` M04 cache/space trade-off | `I→A` M04 latency ladder | `I→A` M05 language/runtime claim verified from source/docs |
| S3 OS & Persistence | `I→A` M06 syscall path; M08 read path; M09 write path | `P` M06/M08 mechanism explanations | `I→A` M06 `strace`/`ps`; M08 file inspection | `I→A` M06 exit/block; M07 OOM/fault; M08 I/O failure | `P` M07 isolation; M08 file-state invariant | `I→A` M09 durability judgment | `P→A` M09 storage cost/latency | `P` M06/M08 source/tool reading |
| S4 Network & Web | `I→A` M10 packet/socket; M11 request through proxy/cache; M12 page load | `P→A` M10/M11 protocol semantics; `A` M12 browser integration | `P→A` M10 `ss`/`nc`; M11 `curl`/DevTools; M12 performance panel | `P` M10 timeout vs refused; M12 render-block/origin policy | `P` M11 cache/freshness; M12 origin/CORS mechanisms | `P` M11 cache vs no-cache, HTTP version | `P→A` M10 RTT/bandwidth; M11 extra round trips | `P` M12 browser documentation as current case |
| S5 Data & Concurrency | `I→A` M13 query→plan→page | `P→A` M13 engine; M14 isolation semantics; M15 locking | `I` M13 `EXPLAIN QUERY PLAN` (A via LAB-REQ-04); M14 connection timeline (A via LAB-REQ-05) | `P→A` M14 anomaly; M15 race (A via LAB-REQ-03/05) | `I→A` M14 transaction invariants; M15 thread-safety | `P` M13 index trade-off; M14 isolation trade-off; M15 lock vs async | `P→A` M13 page/IO cost; M14 throughput | `P` M13 SQL interface learning |
| S6 Distributed & Infra | `I→A` M16 remote call; M19 deployed request | `P` M16 ambiguity; M17 guarantees | `P→A` M19 process/artifact comparison; M20 instrumented signal | `P→A` M16 timeout/retry; M20 controlled incident packet | `P` M16 idempotency invariants; M19 reproducibility invariant | `I→A` M17 consistency choice; M18 delivery semantics; M19 cost | `P→A` M16 availability math (just-in-time); M17 replication cost; M19 resource cost | `P` M19 deployment reading; M20 tooling docs |
| S7 Judgment & Defense | `A` M24 data/request/control trace | `A` M24 articulated defense | `A` M24 evidence-based observation record | `A` M24 failure walkthrough | `A` M23/M24 stated invariants | `A` M23 Technology Card; M24 architecture defense | `A` M23 cost model; M24 scale analysis | `A` M23 systematic evaluation (stable principle, stopping point); M24 unknowns plan |

**Growth rule:** no competency becomes "mature" by recitation. `A` marks mean the learner has produced the named evidence artifact. `Judge`, `Estimate`, and `Learn-New-Tech` are introduced early and become systematic in S6/S7 — that is deliberate, not a late add-on.

## Module → primary competency and module-end capability

Compact form of the accepted #15 integration (full detail: `meta/blueprint/competency-concept-integration-v0.1.md` §3).

| Module | Primary | Capability by module end |
|---|---|---|
| M00 | Trace | Trace one local request through interface/process/storage/response; name where data/state/time/failure can reside |
| M01 | Explain | Encode/decode, explain representation boundary, estimate size, detect broken round-trip/overflow |
| M02 | Correctness | State spec/invariant, trace container ops, estimate growth, choose a container for a workload |
| M03 | Trace | Trace call/memory access through registers/stack; locate a crash; distinguish fact from guess |
| M04 | Observe | Fair measurement; locality effects; latency estimation; plausibility of a memory-related difference |
| M05 | Explain | Trace source→runtime; verify one language/runtime behavior from docs/source; type→correctness claim |
| M06 | Trace | Program→process startup; syscall entry/return; fork/exec; exit status; blocking/scheduling event |
| M07 | Explain | Translation at the intended abstraction; address-space boundaries; OOM/fault diagnosis without confusing isolation with durability |
| M08 | Trace | File read/write through API/descriptor/page cache/metadata/storage; diagnose permission/missing/full |
| M09 | Judge | Durability under a named failure bound; storage-class comparison; fsync/backup choice with loss/latency/cost |
| M10 | Trace | Data→socket→transport; refusal vs timeout; bounded RTT/bandwidth estimate |
| M11 | Explain | HTTP/TLS semantics; intermediary/cache path; extra round trip vs freshness/privacy |
| M12 | Observe | Multi-process browser + render path; render-blocking/origin-policy diagnosis |
| M13 | Observe | Query→plan→index→page; index judged for a stated workload; result correctness preserved |
| M14 | Correctness | Transaction/ownership invariants; permitted anomaly; isolation/recovery behavior; smallest fix |
| M15 | Diagnose | Enumerate an interleaving; reproduce a race; fix with synchronization; cost/boundary of the fix |
| M16 | Judge | Slow vs unavailable vs completed-but-unacknowledged; bounded timeout/retry/idempotency design |
| M17 | Judge | Replicated-state guarantees; what consensus buys; stale/conflicting observation; cost/availability consequences |
| M18 | Judge | Sync vs durable job table vs queue for a stated constraint; duplicate/order semantics; complexity destination |
| M19 | Explain | Image/artifact vs process; namespace/resource/config boundaries; reproducibility vs security isolation |
| M20 | Diagnose | Select a signal; correlate a request; symptom vs cause; overhead/privacy/missingness limits |
| M21 | Judge | Trust boundaries; crypto primitive role; certificate/signature evidence; reject "encryption solves everything" |
| M22 | Diagnose | Identity→authorization; reproduce a safe local composition failure; fix; verify without secrets/real targets |
| M23 | Learn-New-Tech | Investigate unfamiliar technology from authoritative sources; design a valid measurement; stable principle + stopping point |
| M24 | Judge | Defend architecture under changed constraints; preserve invariants; name assumptions/evidence/costs/failures/alternatives/unknowns |

**Guardrails kept from #15 §3.1:** M05 — trace + justified claim, not parser vocabulary; M18 — delivery semantics with a constrained choice, no broker product; M19 — process/artifact boundaries, not Docker/Kubernetes certification; M21/M22 — keep trust/crypto distinct from identity/authz/composition; M23 — real Technology Card, not a pros-cons essay; M24 — evidence-to-claim ratio and rejected alternatives, not architecture ornament.

## Required Labs → competencies (assessed)

| Lab | Location | Mechanism | Competencies assessed | Evidence pattern |
|---|---|---|---|---|
| LAB-REQ-01 | M11, revisit M12 | HTTP origin/intermediary/cache semantics | Trace, Explain, Observe, Correctness, Judge | Explain + Predict + Break + Judge: direct vs forwarded trace, controlled origin/cache failure, retry/cache judgment with limits, clean reset |
| LAB-REQ-02 | M06, short M08 revisit | User program → syscall route in xv6 | Trace, Explain, Observe, Diagnose, Learn-New-Tech | Trace + Predict + Break + Explain: source route, working `sleep`, failure-classification, reset evidence |
| LAB-REQ-03 | M15 | POSIX threads: defined lost update (C11 atomics), mutex, condition rendezvous, deadlock boundary | Correctness, Trace, Diagnose, Explain, Judge | Predict + Break + Diagnose + Correctness: observed interleaving, invariant, fix, held/reversed predicate break, fairness/limits statement |
| LAB-REQ-04 | M13, revisit M23 | SQLite plan, scan vs index, workload data, equivalence, read/write/space | Observe, Trace, Explain, Correctness, Diagnose, Estimate, Judge | Predict + Observe + Judge + Estimate: plan before/after, result equivalence, distribution/warmup/limits, write/space cost |
| LAB-REQ-05 | M14, revisits M09/M15 | SQLite transactions/isolation/rollback/process-interruption recovery/backup | Correctness, Trace, Observe, Diagnose, Explain, Judge, Estimate | Predict + Break + Correctness + Diagnose: invariant, timeline, anomaly/conflict, rollback + recovery record, backup/restore, guarantee-vs-application claim |

Every Required Lab begins with the mandatory **entry gate** (repository + preflight + baseline + evidence record) and applies the **measurement rule** (question, environment/version, workload, baseline, warmup, repetitions, distribution, causal limit — `lab-source-selection-map-v0.1.md` §1.2). Six competencies are represented across Labs; no Lab assesses a competency it does not also practice.

## Mini Cloud App milestones → competencies

| Milestone | Primary Core locations | Competency evidence | Project boundary |
|---|---|---|---|
| P0 | M00–M02, M08–M09, M13 | Trace input→representation→durable state→read; ownership/schema invariant; size estimate; simpler-alternative judgment | One process, one durable collection; no HTTP/auth/cache/replica |
| P1 | M05–M06, M10–M11 | Trace a boundary crossing; contract vs implementation; malformed/partial diagnosis | CLI first; minimal HTTP only when M11/M12 mechanism is the target |
| P2 | M12, M21–M22 | Identity→authorization trace; allowed/denied tests; privacy/logging decision | Course-owned fixture identities; no public exposure |
| P3 | M10–M11, M16 | Socket/protocol observation; timeout≠non-commit; safe retry/idempotency policy | Local processes; bounded delay/disconnect; no Internet inference from loopback |
| P4 | M02, M04, M13, M23 | Baseline/workload/plan/distribution/equivalence; write/space cost; inference limit | No index/cache without a measured query and stated workload |
| P5 | M14–M15 | Anomaly/race reproduction; invariant; app-lock vs DB guarantee; final-state verification | Independent concurrency lab stays separate from integration harness |
| P6 | M09, M14, M20, M23 | Backup/restore or recovery evidence; state version; loss bound; recovery runbook claim | Migrations only on real evolution need; backup before managed recovery |
| P7 | M05–M07, M19 | Native vs container artifact/process compare; config/state/resource boundaries; source/version map | Native Linux path canonical; container Optional |
| P8 | M04, M10–M11, M16, M20 | Correlate one request/failure; signal selection; redaction and missingness; overhead | Local structured logs/timers first; no vendor stack |
| P9 | M16–M24 | All eight competencies at whole-system scale | Scenario cards; **rejection of a component is a valid outcome** |

## Stage exit evidence (evidence-packet model)

A Stage System Checkpoint requires a compact evidence packet, not a topic quiz:

1. one prediction or stated specification;
2. one real observation or controlled break;
3. one explanation tied to mechanism and evidence;
4. one explicit invariant, failure bound, or uncertainty statement;
5. one judgment or estimate where the module makes a choice;
6. one transfer or connection prompt when the concept is a revisit.

`Recall` is legitimate only for a small set of interface facts and terms; it is never the sole evidence in a Stage. Each Stage exit additionally names its competency `A` cells from the matrix above (e.g., S2 exits when the learner produces the M04 measurement record with stated inference limits — the R1/R7 first-assessed home).

## Final System Defense (M24)

The defense reuses the packet at whole-system scale and requires: request/data/control trace; state inventory (transient/process/database/backup/telemetry/credential); invariant & failure matrix; measurements with environment/workload/repetitions/limits; security & privacy decisions; latency/resource/cost estimates; selected evolution or rejection; recovery evidence; three alternatives with moved complexity; explicit unknowns + learning plan. Passing requires a defensible evidence-to-claim relationship — **not** added infrastructure.

## Did the reconciliation change anything here?

No competency was renamed or added. `Introduce/Practice/Assess` and Stage/Module/Lab/Milestone mappings above are the same capability spine as Issue #15, with the #9 dispositions added as first-assessed homes (M04 measurement-uncertainty/experimental pattern; M13 schema-evolution; M00 toolchain outcomes + lab gate) and the "no module teaches everything" rule enforced by sparse cells.
