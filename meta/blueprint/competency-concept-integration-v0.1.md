# Competency + Concept Registry Integration Proposal v0.1

**Status:** PROPOSAL — READY FOR ISSUE #9 INTEGRATION REVIEW; not canonical and not `VERIFIED`  
**Issue:** #13  
**Feeds:** Issue #9 reconciliation  
**Base:** `origin/main` at `271c44e18db98da0501bc3ab99046b1a98d7340d`  
**Scope:** Blueprint-level competency coverage, assessment evidence, Mini Cloud App/lab alignment, and the first bounded Concept Registry population for M00–M24.

## 1. Purpose and authority

This document proposes how the existing M00–M24 blueprint can produce observable capability rather than topic familiarity. It does not edit `meta/COMPETENCY_MATRIX.md`, `meta/CONCEPT_REGISTRY.md`, the Curriculum Map, or the dependency graph. Issue #9 should accept, revise, or reject these proposals while reconciling the parallel Issue #2, #3, and #4 outputs.

The proposal follows these rules:

- A module earns Core space only when it produces a new observable capability or applies an existing capability to a materially different mechanism.
- A competency claim requires evidence: an observation, prediction, explanation, diagnosis, correctness argument, estimate, judgment, or source-based learning artifact.
- A project hook is an integration surface, not a replacement for the mechanism-specific lab.
- A lab entry below is a candidate alignment to Issue #4, not final adoption. License, version, setup, safety, and provenance remain selection gates.
- A concept has one primary canonical teaching home. Later locations recap only what is needed for the new context and add application, failure, connection, or trade-off evidence.
- AI literacy, HCI/accessibility, applied foundations, and data-evolution decisions remain subject to the active Open Questions and are not silently promoted into the canonical Registry here.

## 2. Stage-level capability spine

| Stage | Modules | Capability transition | Evidence that must recur in the Stage | Integration risk for #9 |
|---|---|---|---|---|
| S1 Foundations | M00–M02 | From a whole-system question to reasoning about representations, algorithms, specifications, and costs. | One request/data trace; representation round-trip; size/complexity estimate; an explicit invariant and a judged data-structure choice. | Tool fluency and applied math can remain labels unless M00/M02 require source, measurement, and error evidence. |
| S2 Machine | M03–M05 | From source-level behavior to observable instruction, memory, locality, and translation mechanisms. | Disassembly/debugger evidence; controlled locality measurement; source-to-runtime trace; one explanation of what the tool cannot establish. | M05 has high vocabulary density; its exit condition must be a trace and a justified language/runtime claim, not parser terminology recall. |
| S3 OS and Persistence | M06–M09 | From a program to an isolated execution context whose data and durability behavior can be traced and challenged. | Syscall/process trace; address-space observation; file-I/O failure; durability/recovery claim with a bounded loss assumption and estimate. | Shell/Git/Linux environment must be an explicit lab prerequisite, not an unassessed M00 mention. |
| S4 Network and Web | M10–M12 | From local execution to an end-to-end request and browser integration case with protocol, cache, origin, and rendering evidence. | Packet/socket/request trace; timeout distinction; cache or proxy comparison; browser performance/security observation. | S4 remains a preferred narrative before S5, not a hard prerequisite for all S5 modules. |
| S5 Data and Concurrency | M13–M15 | From stored data to query cost and concurrent state transitions that can be specified, reproduced, and corrected. | Query plan and controlled benchmark; transaction anomaly; race/interleaving trace; invariant-preserving fix. | M14/M15 overlap intentionally, but the DB anomaly and thread interleaving must be separate evidence artifacts. |
| S6 Distributed and Infrastructure | M16–M20 | From single-system guarantees to partial failure, coordination, deployment, and evidence-driven operations across boundaries. | Timeout/retry trace; replica/consistency scenario; duplicate-delivery judgment; process/artifact comparison; controlled incident packet. | Consensus, queues, containers, and telemetry must remain mechanism cases, not product or implementation requirements. |
| S7 Security, Judgment, Defense | M21–M24 | From local trust/crypto/security mechanisms to transferable evaluation and a defended whole-system design. | Trust map; signature/certificate observation; safe-target regression; Technology Card; complete System Defense evidence packet. | Security and judgment must synthesize earlier evidence rather than become a vocabulary-heavy late exam. |

## 3. M00–M24 competency and evidence proposal

**Evidence vocabulary:** `Explain`, `Predict`, `Break`, `Judge`, `Recall`, `Connect`, `Transfer`, `Stage System Checkpoint`, and `Final System Defense` are used as assessment-pattern labels, not as full assessment specifications.

| Module | Primary competency | Secondary competencies | Observable capability by module end | Likely assessment evidence | Mini Cloud App evidence | Lab / Source Expedition evidence | First meaningful capability point |
|---|---|---|---|---|---|---|---|
| **M00** Map and system questions | **Trace** | Explain, Observe, Learn-New-Tech | Follow one local request from caller through interface, process, storage, and response; identify where data, state, time, and failure can reside. | `Trace + Explain + Break`: annotated request trace, one controlled service failure, evidence/source map, and a stated inference limit. | **P0:** identify the baseline process, durable collection, state locations, and one invariant without adding infrastructure. | Shell plus local HTTP observation; source-reading/toolchain orientation. This is a prerequisite pattern, not a final lab selection. | `L00-01`: the learner can trace one request and name one observation that would distinguish competing explanations. |
| **M01** Bits, Bytes, and Representation | **Explain** | Trace, Correctness, Estimate, Diagnose | Encode/decode a value or text, explain the representation boundary, estimate size, and detect a broken round trip or overflow. | `Predict + Explain + Break + Estimate`: hexdump/bytes evidence, malformed representation, round-trip check, and size estimate with assumptions. | **P0:** inspect an item’s identifier/text representation before and after storage; no new feature is required. | Adapted CS:APP Data Lab candidate, subject to license/access review; otherwise use original `struct`/hexdump exercises. | `L01-02/L01-04`: the learner predicts an overflow or round-trip failure and supports it with bytes and a test. |
| **M02** Computation and Complexity | **Correctness** | Explain, Estimate, Judge, Trace, Learn-New-Tech | State a specification/invariant, trace a data-structure operation, estimate growth, and choose among containers for a workload rather than by name. | `Predict + Judge + Transfer`: compare two representations, test scaling, state the invariant, and explain what the measurement does not prove. | **P0/P4:** justify the baseline collection and later query/index experiment; no index is added without a workload and baseline. | Small data-structure/scaling experiment; source reading of a standard/library contract. | `L02-02/L02-03`: the learner can reject an attractive data structure using a specification, workload, and cost argument. |
| **M03** ISA and Execution | **Trace** | Observe, Explain, Diagnose, Correctness | Trace a function call and memory access through registers/stack/instructions, use a debugger to locate a crash, and distinguish observed facts from guesses. | `Predict + Observe + Break + Explain`: predicted register/stack state, debugger/disassembly record, induced local crash, and causal explanation. | No required project change; P0 remains the simple baseline so machine evidence does not become web implementation. | Adapted offline CS:APP Bomb Lab or a course-owned debugger slice, subject to safety, architecture, and license review. | `L03-02/L03-03`: the learner locates the failing instruction or invalid access and explains the evidence chain. |
| **M04** Memory Hierarchy and Locality | **Observe** | Diagnose, Estimate, Explain, Judge | Design a fair comparison, observe locality effects, estimate latency orders, and diagnose whether a performance difference is plausibly memory-related. | `Predict + Observe + Diagnose + Estimate`: baseline/workload/warmup/repetitions, measured contrast, latency estimate, and alternative explanation. | **P4:** the project may expose a hot read only after a measured baseline; no cache layer is required. | Adapted CS:APP Cache Lab or a smaller locality benchmark; metadata and architecture constraints are mandatory. | `L04-02`: the learner changes data layout, measures the effect, and states the limits of causal attribution. |
| **M05** Languages, VM, and Compiler Pipeline | **Explain** | Trace, Judge, Learn-New-Tech, Correctness, Observe | Trace source through syntax/representation/runtime toward execution, explain one language/runtime behavior from primary documentation or source, and connect type/contract claims to correctness. | `Explain + Connect + Learn-New-Tech`: source-to-runtime map, one inspected bytecode/disassembly result, a documented language claim, and a counterexample or limit. | **P1 preparation:** keep the domain/service core separate from transport; explain which behavior belongs to the language/runtime and which to the interface. | Python `dis`/compiler observation or a small tokenizer/parser slice; full compiler construction remains Deep Dive. | `L05-01/L05-03`: the learner can explain one observed translation/runtime behavior and verify it against a source, not intuition. |
| **M06** Processes, Syscalls, and Execution Context | **Trace** | Observe, Explain, Diagnose, Correctness | Follow program-to-process startup, syscall entry/return, fork/exec, exit status, and a basic scheduling/blocking event. | `Trace + Observe + Break + Explain`: process/syscall trace, stopped child or failed exec, exit-status interpretation, and boundary contract. | **P1/P3:** show the app service and client as distinct execution contexts only when the process-boundary question is being assessed. | Adapted MIT xv6 utility path or native `strace`/`ps` exercise; exact source/license and toolchain review remains open. | `L06-01/L06-02`: the learner can trace one command through process creation and syscall evidence. |
| **M07** Virtual Memory and Isolation | **Explain** | Trace, Diagnose, Estimate, Correctness, Judge | Explain virtual-to-physical address translation at the intended abstraction, observe address-space boundaries, and diagnose an OOM, fault, or invalid access without confusing isolation with durability. | `Predict + Break + Diagnose + Judge`: address-space prediction, bounded memory failure, `/proc`/sanitizer evidence, and a resource estimate. | **P7 preparation:** compare process memory/state with later container limits; do not imply a container is automatically a security boundary. | Optional adapted xv6 page-table or memory observation; native `/proc`, sanitizer, and memory-limit path is the lower-load alternative. | `L07-01/L07-02`: the learner predicts what is private/shared and explains the evidence after a bounded memory failure. |
| **M08** Files, Filesystems, and System I/O | **Trace** | Explain, Observe, Diagnose, Correctness | Trace a file read/write from API through descriptor, page cache, filesystem metadata, and storage boundary; diagnose permission, missing-file, or full-disk behavior. | `Trace + Observe + Break + Explain`: `strace`/metadata record, induced I/O failure, file-state invariant, and distinction between buffered and durable state. | **P0/P6:** inspect item/database files and state what the baseline does and does not guarantee after interruption. | Adapted xv6 filesystem/utility slice or native `strace`/filesystem observation; no full filesystem implementation. | `L08-01/L08-03`: the learner traces a real file operation and identifies the first failing boundary. |
| **M09** Storage Engine and Durable Storage | **Judge** | Estimate, Explain, Diagnose, Correctness | State what durability means under a named failure bound, compare storage classes, and judge an `fsync`/backup/storage choice by loss, latency, and cost. | `Judge + Estimate + Break + Explain`: crash/recovery result, latency/cost estimate, explicit RPO-like loss bound, and rejected alternative. | **P6:** create/restore or inspect a backup fixture only after the learner states the baseline durability claim; do not promote object storage or replication by default. | Local `fsync`/interruption experiment and storage comparison; object-store case remains optional/current. | `L09-01`: the learner distinguishes “written,” “committed,” “backed up,” and “survives this failure” with evidence. |
| **M10** Networking I: IP, DNS, and Transport | **Trace** | Observe, Diagnose, Explain, Estimate | Trace application data to a socket and packet/transport exchange, distinguish refusal from timeout, and estimate RTT/bandwidth effects. | `Trace + Predict + Break + Diagnose`: local socket/packet evidence, stopped server, delayed response, and a bounded network estimate. | **P3:** run separate local client/service processes over a real loopback path; keep retries out until ambiguity is observable. | Local TCP/UDP and `ss`/`nc`/packet observation; CS144 receiver is an optional adapted Source Expedition, not a prerequisite. | `L10-02/L10-03`: the learner identifies whether the failure is connection, transport, application, or observation ambiguity. |
| **M11** Networking II: TLS, HTTP, CDN, and Proxies | **Explain** | Trace, Judge, Observe, Estimate, Correctness | Explain HTTP request/response semantics and TLS’s role, trace an intermediary/cache path, and judge an extra round trip or cache policy against freshness and privacy requirements. | `Trace + Predict + Judge + Observe`: `curl`/DevTools record, cache hit/miss or proxy comparison, certificate evidence, and latency estimate. | **P1/P3:** expose a minimal HTTP adapter only when the interface/network mechanism is the target; document the boundary and retry semantics. | Adopt/Adapt RFC 9110 plus local wire inspection; do not copy RFC text or make a CDN/product mandatory. | `L11-02/L11-03`: the learner can trace one request and explain which authority, state, and failure moved to an intermediary. |
| **M12** Web and Browser Integrated Case | **Observe** | Trace, Explain, Diagnose, Judge, Correctness | Observe a browser’s multi-process/request/render path, diagnose a render-blocking or origin-policy behavior, and explain why the browser case is not a single-process toy. | `Trace + Observe + Diagnose + Connect`: DevTools/process/timing evidence, broken CORS or render path, and a cross-layer explanation. | **P2/P3:** inspect the thin client and authorization/error behavior; do not turn the project into frontend framework training. | DevTools Performance/Network and local page; browser documentation is a current case whose process details require review. | `L12-01/L12-03`: the learner correlates one visible browser behavior with a process, network, or origin mechanism. |
| **M13** Databases: Storage and Indexing | **Observe** | Explain, Trace, Judge, Estimate, Correctness | Trace a query through a relational interface, plan, index, pages, and buffer/cache; judge an index only for a stated workload and preserve result correctness. | `Predict + Observe + Judge + Estimate`: plan before/after, controlled dataset, result equivalence, measured read/write/resource cost, and workload limits. | **P4:** add the query fixture and index experiment only after a scan baseline; a database replacement is not the learning outcome. | Adapted PostgreSQL `EXPLAIN`/SQLite comparison; PostgreSQL remains optional after the simple baseline and version review. | `L13-01/L13-03`: the learner reads one plan and connects its choice to measured workload evidence rather than memorizing B-tree vocabulary. |
| **M14** Databases: Transactions, Recovery, and Isolation | **Correctness** | Diagnose, Judge, Explain, Trace, Estimate | State transaction and ownership invariants, reproduce a permitted anomaly, explain the relevant isolation/recovery behavior, and justify the smallest fix. | `Predict + Break + Correctness + Diagnose`: concurrent transaction trace, anomaly reproduction, invariant matrix, rollback/recovery evidence, and throughput trade-off. | **P5/P6:** make one multi-step item mutation atomic and test crash/rollback behavior; migrations/backup scope requires #9 alignment. | Real SQLite/PostgreSQL isolation exercise; use controlled local transactions, not a mandatory production database. | `L14-01/L14-02`: the learner predicts an anomaly and distinguishes application-level locking from database guarantees. |
| **M15** Concurrency: Threads, Races, and Synchronization | **Diagnose** | Correctness, Trace, Explain, Judge, Estimate | Enumerate an interleaving, reproduce a race, fix it with an appropriate synchronization strategy, and explain the cost or boundary of the fix. | `Predict + Break + Diagnose + Correctness`: stress/reproduction trace, invariant, minimal fix, deadlock/progress observation, and thread-versus-async judgment. | **P5:** run the project race harness only after the independent mechanism exercise; require request IDs and final-state evidence. | Adapted OSTEP Threads (Semaphores) exercises, limited to one or two invariant-rich tasks and subject to license review. | `L15-01/L15-02`: the learner can make the race occur and explain why the correction changes the allowed interleavings. |
| **M16** Distributed Systems Foundations: Partial Failure and RPC | **Judge** | Trace, Explain, Estimate, Correctness, Diagnose | Distinguish slow, unavailable, and completed-but-unacknowledged remote work; choose bounded timeout/retry/idempotency behavior and trace the remote call. | `Trace + Break + Judge + Estimate`: delayed/disconnected RPC evidence, retry policy, idempotency invariant, availability estimate, and alternative design. | **P3/P9:** exercise a real two-process boundary with safe read/write retry policy; do not add service decomposition for appearance. | Local RPC with injected delay/partition; MIT 6.033 fault-tolerant case is an adapted reasoning supplement, not a required distributed implementation. | `L16-01/L16-02`: the learner states what cannot be known after a timeout and chooses a safe response. |
| **M17** Replication, Consistency, and Consensus | **Judge** | Explain, Correctness, Diagnose, Estimate, Trace | Compare replicated-state guarantees, explain what consensus buys, identify a stale/conflicting observation, and judge cost/availability/consistency consequences. | `Explain + Judge + Break + Estimate`: read/write scenario, replica-failure observation or trace, consistency claim with qualifier, and replication cost estimate. | **P9:** use a scenario card or bounded demonstration; adding replicas is not mandatory and must be justified by a failure/workload constraint. | Adopt/Adapt a small three-node observation or case analysis only after Issue #4 and #9 resolve the Core boundary; full Raft/Paxos implementation is Deep Dive. | `L17-01/L17-03`: the learner can state the guarantee being purchased and the behavior not guaranteed during a partition. |
| **M18** Distributed State and Coordination | **Judge** | Explain, Correctness, Diagnose, Trace, Learn-New-Tech | Choose between synchronous work, a durable job table, and a queue/broker for a stated constraint; explain duplicate delivery/order semantics and where complexity moves. | `Judge + Break + Explain + Transfer`: duplicate/out-of-order scenario, delivery invariant, rejected simpler alternative, and a transfer to a non-web workflow. | **P9:** queue remains scenario-only unless latency/work-duration or producer/consumer mismatch creates a measured need. | Local durable job-table or bounded queue case; no required Kafka/Redis/broker product. | `L18-01/L18-02`: the learner can explain why “exactly once” is a claim about end-to-end effects, not a magic broker setting. |
| **M19** Infrastructure: Containers, Virtualization, and Deployment | **Explain** | Observe, Judge, Estimate, Diagnose, Learn-New-Tech | Explain image/artifact versus running process, observe namespace/resource/configuration boundaries, and judge reproducibility separately from security isolation. | `Explain + Observe + Judge + Learn-New-Tech`: native/container comparison, missing dependency/config failure, resource estimate, and source/version map. | **P7:** compare the same app in the canonical Linux path and one optional container; preserve external state deliberately. | Adapted Docker/native-process comparison; container remains optional and vendor-neutral. | `L19-01/L19-03`: the learner can name what the container buys, what it moves to the host/runtime, and what it does not guarantee. |
| **M20** Observability and Reliability Engineering | **Diagnose** | Observe, Judge, Explain, Estimate, Correctness | Select a signal for a question, correlate a request across boundaries, distinguish symptom from cause, and state telemetry overhead/privacy/missingness limits. | `Observe + Diagnose + Explain + Judge`: controlled incident packet with logs/metrics/traces, injected fault, missing-signal analysis, redaction check, and impact estimate. | **P8:** add structured logs and timers first; add one trace only when it answers a named cross-boundary question. | Adapted OpenTelemetry signals/trace comparison; local logs/timers are the lower-complexity baseline. | `L20-01/L20-02`: the learner reaches a diagnosis with evidence and explicitly labels what remains unknown. |
| **M21** Security Synthesis I: Trust and Crypto Use | **Judge** | Explain, Diagnose, Learn-New-Tech, Correctness, Observe | Draw trust boundaries, select the role of a standard crypto primitive, inspect certificate/signature evidence, and reject unsafe “encryption solves everything” reasoning. | `Judge + Explain + Diagnose + Learn-New-Tech`: trust map, certificate/signature observation, failed-verification diagnosis, and source-backed API choice. | **P2/P9:** identify credential, authorization, and telemetry boundaries without introducing a real identity provider. | `openssl`/standard-library certificate and signing observation; Attack Lab is not a Core substitute. | `L21-01/L21-02`: the learner identifies an authority change and explains the property a chosen primitive does and does not provide. |
| **M22** Security Synthesis II: Authn/Authz and Secure Composition | **Diagnose** | Judge, Explain, Correctness, Learn-New-Tech, Observe | Trace identity to an authorization decision, reproduce a safe local composition failure, fix it, and verify the fix without exposing secrets or real targets. | `Break + Diagnose + Judge + Explain`: threat/authority map, safe-target failure, regression test, least-privilege decision, and dependency/source evidence. | **P2/P9:** two-user private/shared-item authorization and denial behavior; no public exposure or real credentials. | Course-owned safe target is a conditional Build gap; use only after a security dossier establishes reset, isolation, provenance, and license. | `L22-01/L22-02`: the learner demonstrates the denied operation and explains which boundary/enforcement point prevented it. |
| **M23** Systems Thinking and Judgment | **Learn-New-Tech** | Judge, Estimate, Diagnose, Explain, Correctness | Investigate an unfamiliar technology from authoritative sources, design a valid measurement, compare alternatives, and state the stable principle, uncertainty, and stopping point. | `Learn-New-Tech + Judge + Estimate + Transfer`: source map, benchmark design, Technology Card, cost/resource model, failure matrix, and explicit unknowns. | **P9:** evaluate an app evolution or defend rejection of one; no component is admitted merely because it is modern. | Adapted MIT 6.033 case-analysis method and measurement pattern; no copied final assignment. | `L23-01/L23-03`: the learner can make a defensible decision about an unfamiliar technology without treating documentation or AI output as authority. |
| **M24** Final System Defense | **Judge** | Explain, Diagnose, Estimate, Correctness, Trace, Observe, Learn-New-Tech | Defend the Mini Cloud App architecture under changed constraints, preserving invariants and naming assumptions, evidence, costs, failure behavior, privacy, accessibility, alternatives, and unknowns. | `Final System Defense`: request/data/control trace; state inventory; invariant/failure matrix; observations/measurements; trust/privacy/accessibility decisions; cost estimate; rejected alternatives; recovery evidence; source map. | **P9:** the app is the integration surface, but the learner may defend keeping the simple baseline rather than adding infrastructure. | Adapted system case/defense format; no separate implementation-heavy capstone is required. | `L24-01/L24-02`: the learner makes and defends a coherent claim under a changed constraint, not merely recites component names. |

### 3.1 Module capability guardrails

The following modules have the highest risk of increasing vocabulary without increasing capability. Issue #9 should preserve their evidence gates:

- **M05:** require one source-to-runtime explanation and one verified observation; do not assess lexer/AST/IR names in isolation.
- **M18:** assess delivery semantics and complexity placement using a constrained choice; do not require a broker product.
- **M19:** assess process/artifact/reproducibility boundaries; do not turn the module into Docker or Kubernetes certification.
- **M21–M22:** keep the two modules distinct: M21 owns trust boundaries and crypto roles; M22 owns identity/authorization and composition failures.
- **M23:** require a real Technology Card and measurement design; do not repeat a generic “name the pros and cons” essay.
- **M24:** grade evidence-to-claim relationships and rejected alternatives, not architecture ornament.

## 4. Mini Cloud App P0–P9 alignment

The P IDs remain Issue #3’s stable project milestones. The table below maps their competency purpose without making any component mandatory.

| Project milestone | Primary Core locations | Competency evidence | Required project boundary |
|---|---|---|---|
| **P0** One process, durable collection | M00–M02, M08–M09, M13 | Trace input → representation → durable state → read; state ownership/schema invariant; size and durability estimate; simpler-alternative judgment. | Keep one process and one durable collection. Do not add HTTP, auth, cache, replicas, or cloud deployment merely to make the baseline look modern. |
| **P1** Process boundary and narrow interface | M05–M06, M10–M11 | Trace a request across a process/interface boundary; explain contract versus implementation; diagnose malformed/partial input. | Retain a local CLI and add a minimal HTTP adapter only when the interface/network question is assessed. |
| **P2** Multiple users and trust boundaries | M12, M21–M22 | Trace identity to authorization; test allowed/denied operations; state privacy and logging decisions. | Use course-owned fixture identities; no real credentials or public exposure. |
| **P3** Real network path and bounded failure | M10–M11, M16 | Observe sockets/protocols; distinguish timeout from non-commit; define safe retry/idempotency policy. | Use local processes and controlled delay/disconnects; do not infer Internet behavior from loopback. |
| **P4** Query shape, indexes, and measurement | M02, M04, M13, M23 | Baseline, workload, plan, latency distribution, result equivalence, write/space cost, and limit of inference. | Do not add an index/cache without a measured query and stated workload. |
| **P5** Concurrent requests and transactional correctness | M14–M15 | Reproduce anomaly/race; state invariant; distinguish application lock from DB guarantee; verify final state. | Keep the independent concurrency lab separate from the project integration harness. |
| **P6** Durable recovery and operational evidence | M09, M14, M20, M23 | Backup/restore or recovery evidence; schema/state version; loss bound; recovery diagnosis and runbook claim. | Reconcile migration depth and privacy policy before making it canonical. |
| **P7** Deployment boundary and reproducible environment | M05–M07, M19 | Compare native/container artifact and process; identify configuration/state/resource boundaries; source/version map. | Native Linux path remains canonical; container is optional unless #9 decides otherwise. |
| **P8** Instrumentation before scaling | M04, M10–M11, M16, M20 | Correlate one request/failure; select useful signals; test redaction and missing telemetry; estimate overhead. | Start with local structured logs/timers; no vendor observability stack requirement. |
| **P9** System Defense candidate state | M16–M24 | All eight competencies through trace, explanation, observation, diagnosis, correctness, judgment, estimation, and source-backed learning. | Changed constraints are scenario cards. Rejection of a queue/cache/replica/cloud component is a valid result when evidence supports it. |

## 5. Competency coverage audit

### 5.1 Recurrence and meaningful capability

| Competency | First introduction | First meaningful capability | Repeated observable evidence | Coverage judgment |
|---|---|---|---|---|
| **Trace** | M00 request/system map | M00 for one boundary; M06 for syscall/process evidence; M12 for cross-process browser trace | M01 representation; M03 machine; M08 file; M10 network; M11 HTTP; M13 query; M16 RPC; M19 deployment; M24 defense | Healthy if each trace names a boundary, state, and evidence source. Repeated request traces must become progressively cross-layer, not identical diagrams. |
| **Explain** | M00 mental model | M03 machine evidence and M08 system I/O make explanation mechanism-bound rather than purely verbal | Every Stage, with M05 source-to-runtime, M11 protocol semantics, M17 guarantees, M19 isolation/artifact, M21 security roles, M24 defense | Broadest competency. Risk of low-information repetition is controlled by requiring mechanism, evidence, assumptions, and limits. |
| **Observe** | M00 real tool orientation | M03 debugger/disassembly or M04 controlled performance observation | M06, M08, M10–M13, M17, M19–M22, M24 | Not a desert, but M00’s tool mention is not sufficient. Every observation must state the question, tool, captured evidence, and blind spot. |
| **Diagnose** | M00 failure question / M03 crash | M03 for a local crash; M04 for measured performance; M10 for network failure | M07–M08, M10–M12, M14–M16, M17–M20, M22–M24 | Introduced early enough. The main gap is experimental discipline: require hypothesis, competing explanation, controlled change, and conclusion from M03 onward. |
| **Correctness** | M01 round-trip evidence | M02 specification/invariant reasoning; M14 transaction correctness is the first complex-state capability | M05 types/contracts, M08 file state, M13 query equivalence, M14–M18, M21–M22, M24 | Current M01/M02 wording risks duplicate first homes. Canonical definition should be M02; M01 remains a representation correctness application. |
| **Judge** | M02 trade-off language | M09 storage durability and M11 cache/proxy choices; mature at M17/M23 | M04, M09, M11, M13–M19, M21–M24 | Risk of concentration in late S6/S7 and repeated generic pros/cons prompts. Use distinct decision scales: representation, resource, guarantee, failure, security, and architecture. |
| **Estimate** | M01 sizes | M04 latency/performance; M09 cost/durability; M13 query cost | M02, M04, M09–M11, M13, M16–M20, M23–M24 | Healthy recurrence. Applied statistics/uncertainty must be made explicit through OQ-BP-002; do not treat a single point estimate as an experiment. |
| **Learn-New-Tech** | M00 shell/source/tool question | M05 when a language/runtime claim is verified from documentation/source; systematic capability at M23 | M00, M02, M05, M11, M19, M21–M23, M24 | Currently named too lightly in early modules and concentrated as a mature skill late. Add a small source-map artifact at M00, M05, M11, and M19, then synthesize at M23. |

### 5.2 Gaps and risks detected

- **Competencies introduced too late:** None of the eight is inherently late. `Judge`, `Estimate`, and `Learn-New-Tech` become mature late, which is appropriate, but their early forms must be assessed. `Diagnose` must not wait for M20; M03/M04 are its first real evidence homes.
- **Competencies named but not assessable:** M00 `Learn-New-Tech`, M05 runtime understanding, M21 source-backed crypto use, and M23 judgment are at risk unless each produces a source/evidence artifact. M19’s “learn a deployment” claim is not enough without a versioned environment/source map.
- **Competency deserts:** M18 has no strong native observation in the current map if the broker is kept scenario-only; its evidence must be a delivery trace or bounded case analysis. M21–M22 need explicit observation/regression evidence so security remains mechanism work rather than threat vocabulary. M05–M06 need an applied toolchain bridge so later labs do not depend on unassessed shell/Git fluency.
- **Duplicate assessments:** Request tracing recurs in M00, M10–M12, M16, M19, and M24; this is valid spiral reuse only if the boundary changes from local interface to transport, browser, remote failure, deployment, and defense. Generic “explain the architecture” prompts must not be reused. `Judge` appears frequently from M02 onward; each judgment must include a different constraint and the complexity moved elsewhere.
- **Excessive late concentration:** Security and distributed judgment should culminate in S7/S6, but their earlier mechanisms already need evidence in M07, M11, M12, M14, and M16. System Defense must synthesize prior artifacts rather than introduce all eight competencies for the first time.
- **Topic-vocabulary risk:** M05, M18, M19, M21–M22, and M23 have explicit capability gates in §3.1. If a module cannot produce the listed artifact, it should be merged, narrowed, or marked a Current Case/Deep Dive during #9 reconciliation.

### 5.3 Assessment architecture recommendation

For a Stage System Checkpoint, require a compact evidence packet rather than a topic quiz:

1. one prediction or stated specification;
2. one real observation or controlled break;
3. one explanation tied to mechanism and evidence;
4. one explicit invariant, failure bound, or uncertainty statement;
5. one judgment or estimate where the module makes a choice;
6. one transfer or connection prompt when the concept is a revisit.

`Recall` remains appropriate for a small set of terms and interface facts, but it must not be the only evidence in any module. `Final System Defense` should reuse the packet structure at whole-system scale.

## 6. Initial Concept Registry proposal

### 6.1 Bounded population

**Proposed size: 18 provisional concepts.** The first population includes the 15 initial Big Ideas already named by the canonical Registry plus three additions that recur across several modules and are at high risk of definition drift: `Process`, `Durability`, and `Trust Boundary`. It deliberately excludes product names, commands, individual protocols, framework terms, and every noun in a Lesson.

The IDs below are provisional and must not be copied into the canonical Registry until Issue #9 accepts the first homes and terminology.

| Provisional ID | Chinese canonical name | English term and qualifiers | Definition boundary | Canonical first introduction | Meaningful revisits | Related concepts | Common confusions | Big Ideas |
|---|---|---|---|---|---|---|---|---|
| **EC-CON-001** | 状态 | State; process, durable, replicated qualifiers | Information that can affect future behavior or observations. It is not every piece of data, and storage is only one possible state location. | M00, `L00-01` | M02, M06, M08, M13, M14, M15, M17, M20, M23, M24; P0–P9 state inventory | Representation, Interface, Failure, Consistency | Variable vs system state; state vs storage; state vs configuration | State |
| **EC-CON-002** | 抽象 | Abstraction | A model or boundary that omits detail while preserving the behavior relevant to a stated purpose. It does not guarantee that omitted mechanisms are irrelevant. | M00, `L00-01` | M02, M05, M12, M16, M19, M23 | Interface, Indirection, Specification | Simplification vs guaranteed behavior; abstraction vs implementation | Abstraction |
| **EC-CON-003** | 表示 | Representation; in-memory, on-wire, on-disk qualifiers | A concrete encoding or structure used to carry information. The same information can have multiple representations with different costs and validity rules. | M01, `L01-01` | M03, M05, M08, M11, M13, M16; P0–P1 | State, Interface, Specification, Correctness | Information vs representation; serialization vs schema; encoding vs encryption | Representation |
| **EC-CON-004** | 间接 | Indirection; address, name, service, intermediary qualifiers | Reaching a resource through a reference, name, mapping, or intermediary so location or implementation can change without changing every caller. Indirection introduces lookup and failure points. | M00, `L00-01` | M05, M07, M11, M16, M19, M23 | Abstraction, Interface, State | Indirection vs abstraction; pointer/reference vs ownership; proxy vs authority | Indirection |
| **EC-CON-005** | 接口 | Interface; API, ABI, syscall, file, HTTP, SQL, RPC qualifiers | The externally visible contract for interaction: accepted forms, meaning, guarantees, errors, and boundaries. An interface is not its implementation or product wrapper. | M00, `L00-01` | M02, M03, M06, M08, M11, M13, M16, M19, M24 | Specification, Representation, Indirection | API vs implementation; protocol vs interface; user interface vs system interface | Interface |
| **EC-CON-006** | 权衡 | Trade-off; performance, reliability, security, privacy, cost qualifiers | A constrained choice where gaining one property changes cost, risk, complexity, or another property. A trade-off requires a stated constraint; it is not a synonym for compromise or preference. | M02, `L02-02` | M04, M09, M11, M13, M14, M17, M18, M19, M23, M24 | Estimate, Specification, Correctness | “Pros and cons” without a constraint; trade-off vs arbitrary compromise | Trade-off |
| **EC-CON-007** | 规格 | Specification | A testable statement of permitted behavior, required behavior, or guarantees under stated assumptions. It is not an implementation, an example, or an unbounded goal. | M02, `L02-03` | M05, M11, M14, M15, M16, M21, M22, M24 | Interface, Invariant, Correctness | Specification vs test case; desired feature vs guarantee; implementation detail | Specification |
| **EC-CON-008** | 不变量 | Invariant | A property that remains true across all permitted state transitions under a specified model. It may be temporarily absent during an internal operation if the specification does not expose that intermediate state. | M02, `L02-03` | M01, M05, M07, M08, M13, M14, M15, M16, M17, M21, M22, M24; P0–P9 | Specification, Correctness, Consistency | Invariant vs precondition; invariant vs consistency; “usually true” heuristic | Invariant |
| **EC-CON-009** | 正确性 | Correctness | Conformance of observable behavior to its specification under stated inputs, concurrency, failure, and trust assumptions. Correctness is not merely speed, security, or success on a sample. | M02, `L02-03` | M05, M07, M08, M13, M14, M15, M16, M17, M18, M21, M22, M24 | Specification, Invariant, Consistency | Correctness vs reliability; correctness vs performance; “it ran” vs conformance | Correctness |
| **EC-CON-010** | 故障 | Failure | A loss, deviation, or uncertainty relative to a specified capability or assumption, including crashes, wrong results, unavailability, and partial completion. Not every exception or unexpected event is a system failure. | M03, `L03-03`; M00 is preview only | M06–M20, M22, M23, M24; P3, P5, P6, P8, P9 | Correctness, State, Isolation, Consistency | Error vs bug vs failure; timeout vs known non-commit; incident vs root cause | Failure |
| **EC-CON-011** | 缓存 | Caching; hardware, page, HTTP, database, application qualifiers | Retaining a prior result or copy for reuse under a validity/freshness policy. A cache is not automatically durable, authoritative, private, or correct under mutation. | M04, `L04-01`; hardware-cache context | M08 page cache, M11 HTTP/cache/CDN, M13 buffer pool, M17 stale replica discussion, M19 resource case, M23 | Locality, State, Consistency, Trade-off | Cache vs buffer; cache vs replica; cache vs durable store; cache hit vs correctness | Caching |
| **EC-CON-012** | 局部性 | Locality; temporal, spatial, data, network qualifiers | The tendency for related accesses or communication to occur near one another in time, space, or placement, allowing lower resource cost. Locality can be exploited by a cache but is not itself a cache. | M04, `L04-02` | M08 disk/file access, M13 index/data layout, M17 replica placement, M23 | Caching, Estimate, Trade-off | Locality vs proximity alone; locality vs caching mechanism | Locality |
| **EC-CON-013** | 隔离 | Isolation; memory, process, browser, transaction, container qualifiers | Limiting interference or visibility between executions, identities, resources, or fault domains. Isolation can support security or correctness but does not alone establish either. | M07, `L07-01`; M06 process boundary is preview only | M12 browser/site boundary, M14 transaction isolation, M15 synchronization scope, M16–M17 fault domains, M19 containers, M21–M22 trust/authority | Trust Boundary, Concurrency, Consistency, State | Isolation vs encryption; process vs VM; transaction isolation vs distributed consistency | Isolation |
| **EC-CON-014** | 一致性 | Consistency; transaction and replicated-system qualifiers | The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee. It must be qualified; “consistent” does not mean merely fresh, durable, or correct in every sense. | M14, `L14-02`; M12/M14 may preview related problems but do not define distributed consistency | M17 replication/linearizability/eventual, M18 delivery/ordering, M23, M24 | Correctness, Invariant, Isolation, Durability | Consistency vs correctness; consistency vs durability; consistency vs consensus; database isolation vs replicated consistency | Consistency |
| **EC-CON-015** | 并发 | Concurrency; threads, processes, event loops, distributed operations qualifiers | Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations. | M15, `L15-01`; M12 event loop and M14 transaction overlap are previews only | M16–M18, M20, M23, M24 | State, Isolation, Correctness, Failure | Concurrency vs parallelism; async I/O vs no concurrency; distributed execution vs one thread | Concurrency |
| **EC-CON-016** | 持久性 | Durability; filesystem, database, object-storage qualifiers | A committed state survives a named restart or failure bound. Durability is a claim about a failure model, not a synonym for backup, replication, availability, or “written to a file.” | M09, `L09-01` | M14 WAL/commit, M17 replication, M18 durable handoff, M24; P0/P6 | State, Failure, Consistency, Trade-off | Durability vs persistence as mere storage; backup vs replication; commit vs survive power loss | Added Big Idea: stable cross-layer guarantee |
| **EC-CON-017** | 信任边界 | Trust Boundary; process, browser, service, user, data qualifiers | A boundary where authority, trust assumptions, or enforcement responsibility changes; inputs crossing it need explicit validation/authorization and outputs need bounded exposure. | M21, `L21-01` | M22 composition/authz, M23 technology judgment, M24; P2/P8/P9 | Interface, Isolation, Specification, Failure | Trust boundary vs network boundary; authentication alone; encryption alone; “internal” means trusted | Added Big Idea: stable security/judgment boundary |
| **EC-CON-018** | 进程 | Process; OS execution-context qualifier | A managed execution context with identity, resources, and normally an address-space boundary through which a program runs. It is not source code, a thread, a container image, or a virtual machine. | M06, `L06-01` | M07 address spaces, M12 browser processes, M16 remote process failure, M19 containers, M24 | State, Isolation, Concurrency, Interface | Program vs process; process vs thread; container vs VM; process state vs durable state | Added Big Idea: required bridge across OS, browser, and infrastructure |

### 6.2 Registry boundedness test

The 18 proposed concepts pass the initial boundedness test because each has a clear first home, at least two meaningful later contexts, and a predictable definition-drift risk. The following are intentionally **not** provisional Registry entries:

- product names, commands, frameworks, and vendor services;
- individual protocols such as TCP, HTTP, TLS, DNS, QUIC, or OAuth — these are mechanism/interface cases that use the canonical concepts;
- individual data structures, database index families, and telemetry signal names;
- `Queue`, `Replication`, `Consensus`, `Transaction`, `RPC`, `Container`, and `Observability` as initial Big-Thing IDs. They remain important module-level mechanisms, but their exact Core scope and canonical boundary require #9/#4 reconciliation; premature IDs would harden an architecture decision;
- AI model/training/evaluation concepts, HCI/accessibility concepts, schema evolution/provenance, and applied statistics concepts until their Core placement is resolved through the active Open Questions.

## 7. Teach Once → Revisit Many audit

### 7.1 First-introduction conflicts in the current blueprint

| Concept | Current ambiguity | Proposal | Dependency-order result |
|---|---|---|---|
| **Invariant** | Current map says `M01/M02`; M01 also uses a representation round-trip invariant. | Canonical definition at M02 `L02-03`. M01 is an application: “this representation round-trips.” | M02 is after representation and before machine/data reasoning; valid. |
| **Correctness** | Current map says `M01/M02`. | Canonical definition at M02 alongside specification/invariant. M01 supplies evidence, not a second definition. | Valid; correctness can be applied to representation before its general definition only if M01 uses the phrase as a local test condition. |
| **Failure** | Current map says `M00/M03`. | M00 asks where failure could occur and observes a stopped service; canonical definition/mechanism at M03 through a real crash/invalid access. | Valid; M00 is a preview, not a premature failure taxonomy. |
| **Isolation** | Current map says `M06/M07`. | M06 introduces process boundaries; M07 owns the canonical explanation of address-space isolation. | Valid; M06 does not define browser, transaction, or security isolation. |
| **Concurrency** | Current map says `M12` preview and `M14–M15`. | M12 event loop and M14 concurrent transactions are contextual previews; M15 owns the canonical concurrency definition and interleaving mechanism. | Valid; M15 has M06 and optional M14 support, not a browser hard dependency. |
| **Consistency** | Current map says `M14/M17`. | M14 owns the qualified consistency/visibility definition for transaction state; M17 revisits it for replicated systems and names the changed guarantee. | Valid; M17 depends on M14 as specified by the graph. |
| **Caching** | M04, M08, M11, M13, and M17 all describe a cache-like mechanism. | M04 owns the general “reused copy under a validity policy” concept. Later modules use explicit qualifiers and never redefine it from scratch. | Valid; hardware cache precedes page/HTTP/database contexts. |
| **Interface** | M00 introduces interfaces; M02 also calls contracts/interfaces first. | M00 owns the canonical interface boundary. M02 teaches specification/contract as a revisit and applies it to a data structure. | Valid; no second interface definition. |
| **State** | M00 introduces state; later project and data modules use it heavily. | M00 owns the broad state distinction; later modules classify state as process, durable, transactional, replicated, telemetry, or credential state. | Valid; this is the necessary top-level concept for the project map. |
| **Durability** | M09 first introduces it, but M14 WAL and M17 replication can appear to redefine it. | M09 owns the failure-bound definition; M14/M17 state which durability mechanism or replication guarantee is being revisited. | Valid; M09 precedes both. |
| **Trust Boundary** | M07, M11, M12, and M19 contain boundary/security material before M21. | Early modules may show boundaries as cases; M21 owns the canonical authority-change definition and synthesis. | Valid if early lessons use “boundary” descriptively and do not duplicate the threat-model explanation. |

### 7.2 Per-concept acceptance questions

For every proposed entry, #9 should confirm:

- **One home:** the `Canonical first introduction` column is the only full definition/mechanism home.
- **Later use:** each revisit has a changed mechanism, failure mode, scale, guarantee, or judgment question; it is not a glossary repetition.
- **Graph order:** every home occurs after the dependencies named in `dependency-graph-v0.1.md`. The only early appearances before a canonical home are explicitly marked preview/application.
- **No premature convenience:** later lessons must not introduce a concept early merely to shorten their own explanation. If a preview is necessary, it should name the question without teaching the canonical boundary.
- **Version/context:** overloaded concepts must carry the context qualifier in the lesson and assessment evidence, especially Caching, Isolation, Consistency, Interface, State, Failure, and Concurrency.

## 8. Deferred concepts and architecture questions

These are not omissions hidden inside the proposal. They are explicit reconciliation inputs:

1. **Bounded AI literacy — OQ-BP-001.** No canonical AI/model/evaluation concepts are assigned. #9 must decide whether the stable capability is a Core thread, a bounded Current Case, or another placement before adding a first home. The safe interim assessment pattern is source/test/measurement verification of an AI-generated claim, not a product lesson.
2. **Human-facing boundary — OQ-BP-003.** No canonical `User Mental Model`, `Accessibility`, or `Consent` entries are assigned. The proposal requires M12/M22/P2 evidence to include user-visible error recovery and privacy decisions only if the architecture decision establishes their Core location.
3. **Applied mathematical/statistical toolkit — OQ-BP-002.** No separate Registry IDs are proposed for probability, uncertainty, or statistics. #9 must choose whether the applied bridge first appears in M04, M16, M20, M23, or a cross-module tool pattern; the competency requirement is already represented by Estimate/Diagnose evidence.
4. **Data modeling, schema evolution, provenance, and derived data — Issue #2 R6.** M13/P6 need a reconciliation decision about whether schema evolution receives an explicit Core lesson. No ID is assigned until a first home and revisit path exists.
5. **Consensus/replication/queue architecture.** These mechanisms are important in M17–M18, but the Core boundary between conceptual case, trace, and implementation remains an Issue #4/#9 decision. No canonical IDs are added to avoid turning a proposed mechanism into a mandatory architecture.
6. **Observability as a Registry concept.** M20 is required as a competency surface, but “observability” is an umbrella practice whose signal/tool boundary and current dependencies need a dossier. The first proposal uses the existing concepts State, Failure, Interface, Estimate, and Correctness instead of adding a broad umbrella ID.
7. **S4/S5 narrative.** The module evidence assumes the default request-centric narrative S4 before S5, while preserving the graph’s partial independence. Reordering the visible narrative must not change the proposed first homes unless the graph is deliberately revised.
8. **Canonical environment and versions — OQ-BP-006.** Tool and version names are intentionally not Registry concepts. Exact environment choices belong in later Research Dossiers and lab selection.

## 9. Verification and completion report

### 9.1 Verification performed

- Read the repository instructions and required canonical/Blueprint inputs from `origin/main` at dispatch `271c44e18db98da0501bc3ab99046b1a98d7340d`.
- Confirmed M00–M24 are each represented once in the module competency table.
- Confirmed all eight competencies have an introduction, a meaningful capability point, and repeated evidence locations.
- Mapped the assessment vocabulary across every module; `Recall` is deliberately limited to supporting facts, while mechanism evidence uses `Explain`, `Predict`, `Break`, `Judge`, `Connect`, `Transfer`, Stage Checkpoints, and the Final System Defense.
- Mapped P0–P9 to Core module evidence without making cache, queue, replica, container, proxy, PostgreSQL, or cloud products mandatory.
- Distinguished likely Adopt/Adapt/source-expedition alignments from final lab selection; preserved Issue #4’s license and provenance gates.
- Proposed one canonical first home for each of 18 concepts and listed later revisits, qualifiers, related concepts, common confusions, and Big Ideas.
- Audited current first-introduction conflicts for Invariant, Correctness, Failure, Isolation, Concurrency, Consistency, Caching, Interface, State, Durability, and Trust Boundary.
- Checked the proposed homes against the authoritative hard-prerequisite direction in the dependency graph; previews are marked as non-canonical applications.
- Kept architecture-dependent areas as explicit Open Questions rather than silently deciding them.

### 9.2 Completion report

**Files changed**

- `meta/blueprint/competency-concept-integration-v0.1.md` — created.
- No canonical Matrix, Registry, Curriculum Map, dependency proposal, status, decision, lesson, lab, or project files were edited.

**Competency gap findings**

- The eight competencies are structurally present, but M00 tool/source literacy, M05 runtime learning, M19 deployment learning, M21 crypto-source judgment, and M23 technology evaluation need explicit evidence artifacts.
- Diagnose is not a late-only S6/S7 capability; M03/M04/M10 must remain real diagnosis homes with controlled hypotheses and measurement limits.
- Judge is introduced in M02 but risks generic repetition and late concentration; its evidence must vary by scale, guarantee, failure, security, and cost constraint.
- Correctness has a current M01/M02 first-home collision; this proposal assigns the canonical explanation to M02 and keeps M01 as a representation application.
- M18, M21, and M22 need observation or regression evidence so scenario/security vocabulary does not replace capability.

**Assessment gap findings**

- Repeated traces and failure exercises are valuable only when each moves to a new boundary or failure model; duplicate generic architecture prompts should be removed.
- Every Stage Checkpoint should require prediction/specification, observation or controlled break, mechanism explanation, invariant/failure/uncertainty statement, and a choice/estimate where applicable.
- Final System Defense should aggregate prior evidence rather than be the first place all eight competencies appear.
- Experimental validity, source verification, and explicit limits of inference are currently under-specified in the canonical Matrix and should be carried into #9’s reconciliation.

**Proposed Registry size**

- 18 provisional concepts: the 15 existing initial Big Ideas plus Process, Durability, and Trust Boundary.
- This is intentionally bounded. Protocols, products, commands, frameworks, mechanism nouns, and architecture-dependent concepts remain outside the first population.

**First-introduction conflicts**

- Resolved provisionally through one-home/preview/revisit rules for Invariant, Correctness, Failure, Isolation, Concurrency, Consistency, Caching, Interface, State, Durability, and Trust Boundary.
- No dependency-order conflict remains if early appearances are kept as previews/applications rather than duplicate canonical explanations.
- #9 must confirm whether adding the three proposed concepts expands the Registry’s intended scope beyond the initial Big Ideas.

**Concepts deferred**

- AI/model/evaluation concepts;
- HCI/accessibility/user mental model/consent concepts;
- applied probability/statistics/uncertainty concepts;
- schema evolution/provenance/derived-data concepts;
- Queue, Replication, Consensus, Transaction, RPC, Container, and Observability as canonical IDs;
- exact environment/version concepts.

**Architecture questions discovered**

- OQ-BP-001: bounded AI literacy placement and stable boundary;
- OQ-BP-002: first home and minimum depth for applied foundations, toolchain, source verification, and statistics;
- OQ-BP-003: bounded human-facing/accessibility boundary;
- OQ-BP-004: default S4/S5 narrative versus hard dependency;
- OQ-BP-005: final lab adoption, adaptation, licensing, and provenance;
- OQ-BP-006: canonical environment/version set;
- whether schema evolution/provenance needs an explicit Core lesson;
- whether Process, Durability, and Trust Boundary should be admitted in the first canonical Registry population.

**Assumptions**

- M00–M24 and the current dependency graph remain proposal inputs; this document does not settle Stage names, lesson count, or exact project implementation.
- The default learner-visible narrative remains S1 → S2 → S3 → S4 → S5 → S6 → S7, while S4/S5 hard-dependency semantics remain partially independent.
- “Meaningful capability” means a learner can produce evidence under a stated task and constraint, not that the learner has mastered a full specialist field.
- Issue #4 candidates remain unbundled until licenses, versions, setup, safety, and provenance are verified.

**Prompt deviations**

- None in the requested deliverable content.
- Commit, push, and PR actions were not performed in this session; the proposal remains local on the dedicated Issue #13 branch pending explicit integration/review authorization.

**Out-of-scope necessary fixes**

- None. The observed need for Matrix/Registry updates is recorded as an Issue #9 integration action, not applied here.

**Recommended #9 Integrator review focus**

1. Decide whether the 18-concept population, especially Process/Durability/Trust Boundary, is the right first canonical boundary.
2. Confirm the M02 canonical home for Specification/Invariant/Correctness and enforce preview language in M01.
3. Verify that M00/M05/M19/M21/M23 source-learning artifacts make Learn-New-Tech assessable rather than nominal.
4. Resolve the M18 queue evidence strategy and the M17 consensus Core boundary without turning products or full implementations into requirements.
5. Reconcile R1–R8 and R6 from Issue #2: applied foundations, toolchain/reproducibility, HCI/accessibility, AI literacy, data evolution/provenance, experimental diagnosis, and horizontal security/privacy.
6. Ensure P0–P9 project evidence remains a mechanism-integration surface and that simpler rejection is accepted as a valid System Defense outcome.
7. Before promoting any concept or assessment rule to canonical files, run a duplicate-definition audit against the final Stage/Lesson and lab selections.
