# Mini Cloud App ↔ Curriculum Alignment v0.1

**Status:** PROPOSAL — READY FOR ISSUE #9 INTEGRATOR REVIEW (not `VERIFIED`)
**Scope:** Issue #11; alignment proposal only
**Inputs:** Issue #1 Core Stage/Module/Lesson map and dependency graph; Issue #2 external curriculum audit; Issue #3 Mini Cloud App evolution map; Issue #4 classic lab and Source Expedition candidates; repository invariants and decisions
**Date:** 2026-08-30

## 1. Purpose and governing decisions

This document maps the accepted Mini Cloud App milestones `P0`–`P9` onto the accepted proposal modules `M00`–`M24` without turning the project into a web-development, cloud-products, or infrastructure-accumulation curriculum. It is a reconciliation proposal for Issue #9. It does not modify the existing evolution map, curriculum map, dependency graph, competency matrix, or project code.

The following rules govern every mapping:

1. The Mini Cloud App is a recurring integration surface and final System Defense case, not the primary vehicle for teaching every mechanism.
2. A project milestone may appear as an early black-box observation or bounded integration checkpoint before the canonical mechanism is taught. That early appearance is a revisit or orientation, not a new hard prerequisite and not permission to teach the mechanism twice.
3. The Module DAG in `meta/blueprint/dependency-graph-v0.1.md` is authoritative. `H` edges constrain curriculum order; `S` edges are preferred only; `R` and `P` relationships do not create prerequisites.
4. `S4` Network/Web and `S5` Data/Concurrency are partially independent branches after `S3`. The default request-centric narrative may present S4 first, but the project sequence must not convert that preference into `S4 → S5` hard dependency.
5. Every checkpoint must expose a named invariant, controlled failure, observation or measurement, security/privacy decision, and simpler alternative. The evidence artifact is part of the competency outcome.
6. Products and frameworks are replaceable cases. Stable mechanisms, constraints, trade-offs, and failure modes are the canonical content.
7. Classic Labs and Source Expeditions teach mechanism-specific material first where Issue #4 identifies a suitable candidate. The project then revisits and composes it; it does not replace it.

### Reading the mapping fields

- **Earliest safe Module entry** means the first place a bounded project touch can occur without requiring the full later mechanism. It is not necessarily the canonical teaching home.
- **Primary Module/Stage home** means where the project milestone gets its strongest canonical integration and assessment. A milestone may revisit several earlier modules.
- **Prerequisite Modules** lists the minimum curriculum prerequisites for the stated project activity, not every module in the recommended learner narrative.
- **Mechanism ownership** distinguishes `Project integration`, `classic Lab`, and `Source Expedition`. “Combination” means the mechanism is taught elsewhere and the project composes or tests it.

## 2. Alignment overview

| Milestone | Earliest safe entry | Primary home | Stage relationship | Dominant competencies | Canonical mechanism ownership |
|---|---|---|---|---|---|
| P0 | M00, with bounded persistence after M01/M08 | M00 integration; M08/M09/M13 revisits | S1 orientation; S3/S5 mechanism revisits | Trace, Explain, Correctness, Estimate | Combination |
| P1 | M00 for CLI/interface; M10/M11 for network interface | M06 + M11, S3/S4 | Does not require Web before process boundary | Trace, Explain, Diagnose, Correctness | Combination |
| P2 | After P0 ownership state; bounded fixture from M00/M01 | M21/M22, S7, with M12 revisit | Security synthesis comes late; authorization can be integrated earlier | Judge, Correctness, Explain, Diagnose, Learn-New-Tech | Combination |
| P3 | M10 after process/socket foundations | M10/M11, S4 | May precede or follow S5 | Trace, Diagnose, Judge, Estimate, Correctness | Combination |
| P4 | M13 after storage and data-structure foundations | M13 plus M23 measurement revisit | S5 branch; no S4 hard dependency | Observe, Diagnose, Estimate, Judge, Correctness | Combination |
| P5 | M14/M15 after transaction or concurrency foundations | M14/M15, S5 | S5 remains independent of S4 after S3 | Correctness, Diagnose, Explain, Judge | Combination |
| P6 | M09 for durability; M13/M14 for schema/recovery | M09/M14 with M19 operational revisit | Can be integrated before distributed infrastructure | Observe, Correctness, Judge, Estimate | Combination |
| P7 | M06/M08 for reproducible native execution; M19 for container case | M19, S6 | Container checkpoint must not be pulled earlier by project order | Explain, Observe, Judge, Learn-New-Tech | Combination |
| P8 | M00/M04 for local timing; M20 for cross-layer observability | M20, S6 | Full observability follows M16/M19; minimal evidence can recur earlier | Observe, Diagnose, Judge, Correctness | Combination |
| P9 | M23; final defense at M24 | M23/M24, S7 | Requires complete shared chain for final defense, not for every scenario exercise | All eight | Project integration + Source Expedition/case analysis |

## 3. P0–P9 detailed mapping

### P0 — One process, one durable collection

**Earliest safe Module entry:** `M00` can introduce the domain, the transient-versus-durable state question, and a deliberately opaque baseline. The learner should not be expected to explain SQLite internals at M00. A meaningful persistence checkpoint is safe after `M01` (representation/serialization) and `M08`/`M09` (files, storage, durability). The query/index mechanism is revisited canonically at `M13` rather than pulled into P0.

**Primary Module/Stage home:** `M00` / `S1` for project orientation and the first whole-system trace; `M08`–`M09` / `S3` for file, durability, and recovery meaning; `M13` / `S5` for the database storage/indexing explanation. P0 is therefore a cross-stage baseline, not evidence that S5 must precede the rest of the course.

**Prerequisite Modules:** For the minimal build: `M00`; for representation-aware inspection: `M01`; for a truthful file/durability discussion: `M08`–`M09`. `M13` is a later canonical revisit, not a prerequisite for running the baseline. The project may use SQLite as a stable black-box dependency before the database module, provided the checkpoint labels its guarantees rather than teaching them prematurely.

**Concepts exposed:** Domain state; transient versus durable state; representation and serialization; stable identifiers; schema constraints; ownership; file/database boundary; commit and retrieval; interface versus implementation; size and storage cost.

**Competency purpose:** The learner traces one value from input through representation and process memory into durable state and back; explains what the baseline does and does not guarantee; states a schema invariant; estimates item size and storage growth; and learns to treat a database choice as a constrained decision rather than a default badge.

**Build opportunity:** Implement the smallest local CRUD path: one Python process, one SQLite database, parameterized SQL, explicit schema, stable item IDs, and a resettable fixture. Add one item, retrieve it, inspect the row and database file, and record the state locations.

**Observe opportunity:** Inspect SQLite rows/schema, filesystem metadata, process/file activity, serialized bytes, and before/after database size. Use a trace or state inspection appropriate to the current Module; do not require a database-engine implementation.

**Break opportunity:** Kill the process between operations; submit malformed or oversized input; attempt duplicate or invalid ownership; remove or replace the database fixture; compare an in-memory reset with a committed write. The break must be bounded and resettable.

**Explain / Judge requirement:** Explain where the item exists at input, in memory, in the database, and after process exit. Judge SQLite against an in-memory dictionary and append-only text for this workload, including what SQLite buys and what it moves to the library. State why parameterized SQL is a boundary correctness and security decision.

**Invariant:** Each item has exactly one owner and stable identifier; a successful committed write is readable as the same value; invalid ownership cannot be represented; external input is data, not SQL code.

**Failure mode:** Process exit, malformed serialization, duplicate identifier, constraint rejection, incomplete write, missing/corrupt database file, or confusing a returned acknowledgement with durable recovery evidence.

**Security/privacy decision:** Use fixture data only; parameterize SQL; do not log note contents or credentials; keep the database local and non-public; state that encryption at rest, authentication, backup policy, and multi-user exposure are postponed.

**Measurement/evidence artifact:** A baseline evidence packet containing schema, one request/data trace, row and file inspection, item/database size estimate, invariant, one controlled failure and result, and a comparison with the simpler in-memory alternative.

**Mechanism ownership:** **Combination.** Project integration owns the end-to-end state trace. Classic Labs/Source Expeditions should teach representation, files, storage, and database mechanisms; P0 must not replace them.

**Deliberately postponed:** HTTP; robust authentication; multiple processes; replication; migrations as a framework; full-text search; encryption at rest; production backups; PostgreSQL; cache; queue; container; deployment automation.

**Simpler alternative:** An in-memory dictionary for the first state/invariant exercise, or an append-only text file for a representation contrast. Neither is the canonical durable baseline when durability is the question.

**When NOT to add:** Do not add SQLite if the checkpoint is only about Python data structures, serialization, or a classic file mechanism. Do not add a database merely because later milestones are called “cloud.”

**Beyond-the-Project transfer case:** CLI configuration/state files, compiler output caches, notebook checkpoints, and batch-job restart state all separate transient representation from durable state.

### P1 — A process boundary and a narrow interface

**Earliest safe Module entry:** `M00` can expose the same operation through a function or CLI boundary and teach interface/implementation separation. A separate process and socket boundary first become safe after `M06` (processes/syscalls) and `M10` (sockets/transport). HTTP is deferred until `M11`/`M12` when HTTP and Web mechanisms are the learning target.

**Primary Module/Stage home:** `M06` / `S3` for process boundaries, execution contexts, and system interfaces; `M10`–`M11` / `S4` for sockets, HTTP messages, status codes, and protocol boundaries. `M00` remains the primary home for the general interface concept.

**Prerequisite Modules:** `M00` for interface and boundary language; `M06` for separate processes; `M10` for network sockets; `M11` for HTTP. `M12` is needed only for browser-facing integration. No `M12` prerequisite is created for the CLI or a local process boundary.

**Concepts exposed:** Process boundary; interface contract; framing; stdin/stdout or HTTP messages; serialization; status/error representation; timeout and partial-message boundary; validation location; transport versus service core.

**Competency purpose:** Trace a request across a boundary; explain interface versus implementation; diagnose malformed, partial, unsupported, and unavailable requests; specify bounded acknowledgements and errors; and judge whether a transport adds learning value.

**Build opportunity:** Keep the domain/service core independent of transport. Retain a CLI client and expose a documented narrow interface. Add a minimal HTTP adapter only at the Web checkpoint, without introducing a web framework or front-end application.

**Observe opportunity:** Capture request/response bytes or structured messages; inspect process creation and exit status; use socket/process tools; compare local function, pipe, and HTTP timing; inspect status codes and error classes.

**Break opportunity:** Close the client mid-request; send truncated or extra data; stop the service; send incompatible fields; cause a bounded timeout; submit a malformed request and verify it cannot reach SQL as code.

**Explain / Judge requirement:** State what the interface promises and deliberately does not promise. Explain where parsing, validation, authorization, and acknowledgement occur. Judge a local CLI, pipe, Unix-domain socket, and HTTP adapter for this learning objective, including complexity moved into libraries and the operating system.

**Invariant:** Each accepted request produces one specified response or bounded error; malformed external input is rejected at the boundary; a successful mutation has one defined acknowledgement semantics; the service core remains transport-independent.

**Failure mode:** Truncation, framing ambiguity, unsupported version/field, client disconnect, process crash, connection refusal, timeout, or duplicate acknowledgement interpretation.

**Security/privacy decision:** Bind only to a local interface for project work; validate at the service boundary; avoid secrets and private content in traces; do not expose the teaching service publicly; make transport security a later bounded case.

**Measurement/evidence artifact:** Interface contract plus example valid/invalid exchanges, one process/socket trace, latency comparison across the chosen boundary, one controlled disconnect/timeout trace, and a judgement of why the selected boundary is proportionate.

**Mechanism ownership:** **Combination.** Classic OS/network labs teach processes, sockets, streams, and HTTP semantics. The project integrates the same service operation across one boundary.

**Deliberately postponed:** Framework internals; HTTP/2 and HTTP/3 implementation; TLS certificate operations; browser JavaScript; service discovery; API version proliferation; public internet deployment.

**Simpler alternative:** Keep a local CLI, pipe, or Unix-domain socket when network semantics are not the target. A local process boundary is sufficient for the interface concept.

**When NOT to add:** Do not add HTTP merely to make the app look like a web app. Do not add a framework, router ecosystem, browser UI, or API versioning when a CLI or small standard-library adapter exposes the mechanism more clearly.

**Beyond-the-Project transfer case:** Unix pipelines, compiler command-line interfaces, file formats, database clients, and library APIs are contracts at boundaries with framing, validation, and failure semantics.

### P2 — Multiple users and explicit trust boundaries

**Earliest safe Module entry:** After P0 has established ownership and state invariants, a bounded local authorization fixture can be integrated as an early project revisit. The learner must first understand “who owns this item?” before adding authentication machinery. A complete security explanation belongs later at `M21`–`M22`; it is not a prerequisite for a small authorization-only experiment.

**Primary Module/Stage home:** `M21`–`M22` / `S7` for trust boundaries, crypto use, authentication versus authorization, sessions/tokens, secure composition, and privacy. `M12` / `S4` provides the browser-origin revisit when the project has an HTTP surface. `M13`/`M14` revisit ownership and transaction correctness.

**Prerequisite Modules:** `M01` for representation and input boundaries; `M00` and P0 for domain ownership; `M13` if authorization is integrated with database queries; `M11`/`M12` only for HTTP cookies, browser origins, or web attacks. `M21` is the hard prerequisite for the canonical M22 security sequence, but not for an early fixed-user authorization fixture.

**Concepts exposed:** Identity; authentication versus authorization; effective user; trust boundary; least privilege; sessions/tokens as state; private versus shared visibility; revocation; privacy minimization; denial behavior; untrusted client claims.

**Competency purpose:** Draw trust boundaries; trace identity to an authorization decision; distinguish confidentiality, privacy, and correctness; explain what the service trusts; diagnose an authorization bypass; judge what information a denial may reveal; and learn a security API from primary documentation rather than inventing cryptography.

**Build opportunity:** Add two course-owned fixture users, private and explicitly shared items, service-layer authorization checks, revocable sharing, and a deliberately simple credential/session mechanism. Never store plaintext passwords in the canonical path. Keep the fixture local, resettable, and non-public.

**Observe opportunity:** Record authorization decision inputs without secrets; inspect ownership and sharing rows; compare allowed and denied responses; inspect which fields enter logs, URLs, backups, and traces; map each trust boundary.

**Break opportunity:** Change an item ID; omit or alter identity; replay an expired fixture credential; attempt cross-user reads or writes; revoke sharing; try to infer another user’s item existence from status, timing, or error content.

**Explain / Judge requirement:** Identify the component authorized to decide access and why client claims are insufficient. Explain why authentication does not imply authorization. Judge a fixed local user ID, fixture credential, session, and real identity provider for this exercise; name the privacy and operational cost of each.

**Invariant:** Every private read/write is authorized for the effective user; unauthorized denial does not disclose whether another user’s private item exists; sharing is explicit, scoped, and revocable; secrets and private content are not emitted into evidence by default.

**Failure mode:** Missing identity, confused deputy, IDOR-style access, stale/replayed credential, non-revoked share, information leakage through errors/timing, or secret exposure in logs/URLs/backups.

**Security/privacy decision:** This milestone is itself a security/privacy decision. Use a local fixture, standard password hashing or a pre-generated non-secret credential fixture as appropriate to the teaching objective, no real identity provider, no internet exposure, minimal retained data, redacted telemetry, and a documented reset path.

**Measurement/evidence artifact:** Threat-boundary diagram, authorization matrix, allowed/denied test matrix, one failed access trace, redaction review of logs/evidence, revocation result, and a short explanation of what the fixture does not prove about production identity security.

**Mechanism ownership:** **Combination.** Classic/security Source Expedition work should teach trust boundaries, crypto use, authn/authz, and safe composition. The project supplies a meaningful ownership/privacy integration gap.

**Deliberately postponed:** OAuth providers; enterprise identity; password-reset email; WAFs; threat hunting; real-user data; public exposure; penetration-testing workflow; claims that a local fixture is production authentication.

**Simpler alternative:** Fixed local user IDs with an authorization matrix when authentication is not the learning target. This is preferable to a fragile homemade password system.

**When NOT to add:** Do not add authentication before the ownership invariant is understood. Do not connect a real identity provider, use real credentials, expose the app publicly, or add token products for résumé value.

**Beyond-the-Project transfer case:** File permissions, database roles, mobile capabilities, package signing, and operating-system privilege boundaries all separate identity, authority, and protected state.

### P3 — Real network path and bounded failure

**Earliest safe Module entry:** `M10` after process and socket foundations. A local pipe or Unix-domain socket may serve as an earlier process-boundary bridge; a real TCP/HTTP path should wait until networking concepts are introduced. P3 does not need to wait for the canonical security synthesis in P2 or for the S5 data branch.

**Primary Module/Stage home:** `M10`–`M11` / `S4` for sockets, TCP byte streams, HTTP semantics, timeouts, retries, and request identity. `M16` / `S6` later revisits the same ambiguity as distributed partial failure.

**Prerequisite Modules:** `M06` for processes; `M08` for I/O interface intuition; `M10` for sockets and transport; `M11` for HTTP if HTTP is used. `M15` is not required for a sequential client/server exercise, and `M14` is a soft contextual aid rather than a hard prerequisite. `M12` is not required.

**Concepts exposed:** Socket; client/server; DNS/name resolution as bounded local case; TCP byte stream; HTTP request/response; timeout; disconnect; retry; idempotency; request ID; partial failure; acknowledgement ambiguity.

**Competency purpose:** Trace application data through protocol layers; distinguish a timeout from proof that an operation did not happen; design safe retry behavior; estimate local network overhead without claiming loopback equals internet performance; and judge which guarantees belong to transport versus application logic.

**Build opportunity:** Run client and service as separate local processes over loopback or a controlled local network. Add explicit connect/read timeouts, bounded retry only for safe operations, request IDs, and a clear mutation acknowledgement policy. Preserve the same domain/service core.

**Observe opportunity:** Use socket/process tools, `curl` or equivalent wire inspection, local packet/request traces, latency measurements, and server logs keyed by request ID. Compare a successful response, timeout, refused connection, and disconnected client.

**Break opportunity:** Stop the server; delay responses; cut the connection after submission; duplicate a request; interrupt a response; send a request that reaches the service but whose acknowledgement is lost.

**Explain / Judge requirement:** If the client times out after a write, state the possible committed states and how the client can learn or safely recover. Judge retries by operation semantics, not by transport convenience. Explain why bounded retries do not make a non-idempotent mutation safe.

**Invariant:** Every mutation has a defined idempotency and retry policy; a timeout is not reported as “definitely not committed”; request IDs allow evidence correlation without becoming a security secret.

**Failure mode:** Connection refused, timeout, disconnect after commit, duplicate submission, partial message, DNS/name-resolution failure, server crash, or retry storm.

**Security/privacy decision:** Use local authorized endpoints; do not benchmark uncontrolled public services; keep credentials and note content out of packet captures/logs; treat HTTP without TLS as a local teaching boundary only; defer public trust and certificate operations.

**Measurement/evidence artifact:** One end-to-end request trace, timeout/duplicate trace, retry decision table, latency distribution with environment and repetitions, and a state reconciliation showing whether the mutation committed.

**Mechanism ownership:** **Combination.** Classic networking/HTTP work teaches byte streams, transport, request semantics, and measurement. The project integrates application acknowledgement and idempotency across the boundary.

**Deliberately postponed:** Public DNS; global routing; QUIC implementation; CDN behavior; multi-region deployment; service discovery; uncontrolled internet performance claims.

**Simpler alternative:** Unix-domain sockets or a local pipe for process-boundary teaching; direct local function calls for the interface contract before network failure is the target.

**When NOT to add:** Do not test against an uncontrolled public service or treat loopback measurements as internet performance. Do not add retries without a specified mutation policy and a way to distinguish ambiguous outcomes.

**Beyond-the-Project transfer case:** Database clients, remote build executors, package downloads, and message consumers all face delayed, duplicated, or ambiguous acknowledgements.

### P4 — Query shape, indexes, and measurement

**Earliest safe Module entry:** `M13` after the learner has the `M08`/`M09` storage model, `M02` data-structure vocabulary, and enough `M04` locality/measurement intuition. A simple query-shape comparison can be previewed earlier, but an index claim should wait for a baseline and query-plan evidence.

**Primary Module/Stage home:** `M13` / `S5` for relational storage, B-tree-like indexing, query plans, pages, and buffer behavior; `M23` / `S7` revisits experimental validity and technology judgement. P4 is a strong S5 branch checkpoint and does not depend on M12 Web/Browser.

**Prerequisite Modules:** Hard: `M08` and `M09` for file/storage and durability context; `M13` for the canonical database mechanism. Soft: `M02` for data structures and `M04` for locality/latency. `M10`/`M11`/`M12` are not prerequisites.

**Concepts exposed:** Query shape; scan versus index access; B-tree-like index; selectivity; query plan; page and I/O cost; locality; warm/cold state; workload; measurement noise; space/write trade-off; planner estimate versus observation.

**Competency purpose:** Form a performance hypothesis; create a controlled fixture; read a query plan; measure fairly; report uncertainty and limits; and judge an optimization by workload, correctness, and total cost rather than by fashion.

**Build opportunity:** Generate a realistic but bounded fixture; choose one query; establish a no-index baseline; add one index; compare results, plans, latency distribution, database size, and write cost. Keep the domain operation meaningful, such as listing a user’s items by owner/time.

**Observe opportunity:** Inspect `EXPLAIN` or equivalent plan output; measure repeated timings; inspect page/cache behavior where available; compare cold and warm runs; record dataset distribution and index size.

**Break opportunity:** Use a skewed dataset; run a query that cannot use the index; compare cold versus warm runs; change data scale; omit warmup/repetitions; or create a workload where write cost dominates. Verify that “faster” is not an artifact.

**Explain / Judge requirement:** State which metric improved, for which workload and scale, what the index costs, what the planner estimated, what was actually measured, and whether a query-shape or algorithm change would be simpler.

**Invariant:** Results are identical before and after indexing; the benchmark records environment, workload, warmup, repetitions, distribution, and limits; optimization does not weaken ownership or visibility constraints.

**Failure mode:** Incorrect result due to query change, stale/poor planner assumptions, index not selected, cold-cache confounding, write amplification, storage exhaustion, or benchmark overclaim.

**Security/privacy decision:** Use synthetic fixture content; avoid private note text in plans or logs; ensure query instrumentation does not expose credentials or user data; keep authorization predicates in the measured query so performance work cannot silently remove security checks.

**Measurement/evidence artifact:** Reproducible benchmark record with query, dataset generator, plan before/after, latency distribution, database size, write measurement, correctness comparison, and an explicit conclusion with inference limits.

**Mechanism ownership:** **Combination.** A classic database/indexing lab or Source Expedition should teach plans and index mechanics; the project supplies a domain-relevant workload and integration evidence.

**Deliberately postponed:** Distributed query planners; sharding; production SLOs; cache layers; generic benchmark dashboards; index catalogs beyond the one needed to answer the question.

**Simpler alternative:** Improve the algorithm, query shape, fixture, or schema before adding an index. A full scan is an acceptable baseline when the data set is small.

**When NOT to add:** Do not add an index without a measured query, stated workload, correctness comparison, and evidence that the index changes the relevant cost.

**Beyond-the-Project transfer case:** Compiler optimization, filesystem caches, build caches, and algorithmic data structures express the same space/time and invalidation trade-offs.

### P5 — Concurrent requests and transactional correctness

**Earliest safe Module entry:** The mechanism should be taught in classic `M14`/`M15` work before the project creates nondeterministic races. A deterministic project integration can begin after `M14` transaction/isolation or `M15` race/lock foundations, with the other module as contextual support.

**Primary Module/Stage home:** `M14`–`M15` / `S5` for transaction invariants, isolation, interleavings, locks, idempotency, and conflict behavior. P5 is a central S5 integration checkpoint and has no hard dependency on S4 after S3.

**Prerequisite Modules:** Hard: `M06` for process/execution context; `M13` for stored data if database transactions are tested. `M14` is the canonical transaction home; `M15` is the canonical thread/race home. Soft: `M03` for shared memory, `M12` for event-loop comparison. No `M10`–`M12` prerequisite is implied by the project’s earlier P3.

**Concepts exposed:** Interleaving; shared state; race condition; atomicity; transaction; isolation; lock; MVCC concept; deadlock; idempotency; conflict response; application lock versus database guarantee.

**Competency purpose:** Enumerate allowed interleavings; state a transaction invariant; reproduce a race; distinguish application synchronization from database guarantees; diagnose a lost update or unauthorized mutation; and judge serialization cost against correctness.

**Build opportunity:** Run concurrent clients against one database; define transactions around multi-step edit/share/delete operations; add a controlled race harness; introduce deliberate delays; specify conflict and retry behavior; inspect final state.

**Observe opportunity:** Log request IDs, transaction boundaries, waits, commits, rollbacks, and final state; inspect database locking or isolation behavior; compare sequential and concurrent traces.

**Break opportunity:** Force a delay between read and write; concurrently edit/share/delete the same item; create lock contention; induce a deadlock or retryable conflict; terminate one transaction; verify no partial unauthorized mutation remains.

**Explain / Judge requirement:** State which outcomes are allowed, where serialization occurs, why a lock or transaction is needed, what throughput it costs, and which guarantees come from SQLite/database semantics versus application code. Explain why “it passed once” is not race evidence.

**Invariant:** No unauthorized mutation commits; every committed state satisfies schema and ownership invariants; a failed transaction leaves no partial mutation; the retry policy does not duplicate a non-idempotent effect.

**Failure mode:** Lost update; stale read; partial multi-step mutation; deadlock; starvation; duplicate retry; lock timeout; race-test flakiness mistaken for correctness.

**Security/privacy decision:** Authorization checks must remain inside the correctness boundary; do not log private content while correlating concurrent requests; ensure error traces do not expose other users’ state; use synthetic fixtures.

**Measurement/evidence artifact:** Interleaving diagram, deterministic race or transaction test, request/transaction trace, final-state invariant check, conflict/deadlock result, and throughput/latency comparison with the simpler sequential path.

**Mechanism ownership:** **Combination.** OSTEP semaphore/concurrency work and database isolation experiments should teach the mechanisms first. The project fills the genuine integration gap by exercising ownership and domain state under concurrent operations.

**Deliberately postponed:** Distributed locks; global ordering; actor frameworks; serializable-by-default claims across databases; sharded transactions; queue-based coordination.

**Simpler alternative:** A deterministic two-thread counter or database transaction lab before introducing concurrent app requests.

**When NOT to add:** Do not add threads merely to increase throughput. Do not claim correctness from a stress test without an explicit invariant, controlled schedule or repetitions, and a mechanism explanation.

**Beyond-the-Project transfer case:** File updates, GUI event handlers, inventory systems, booking, accounting, and build graphs share the same race and atomicity problem.

### P6 — Durable recovery and operational evidence

**Earliest safe Module entry:** `M09` can teach durability, `fsync`, crash loss, and backup-versus-replication distinctions. A project recovery checkpoint with schema migration belongs after `M13`/`M14`, when the learner can state the data and transaction invariants. Operational evidence can later revisit `M19`/`M20`.

**Primary Module/Stage home:** `M09` / `S3` for durable storage and loss models; `M13`–`M14` / `S5` for database schema, transactions, recovery, and migration correctness; `M23` for RPO/RTO and judgement. P6 does not require S6 distributed infrastructure.

**Prerequisite Modules:** Hard for durability: `M08` and `M09`. Hard for database recovery/migrations: `M13` and `M14`. `M19`/`M20` are later operational revisits, not prerequisites for a local backup/restore exercise.

**Concepts exposed:** Durability; crash recovery; WAL concept; schema version; migration; backup; restore; RPO/RTO; disk/resource exhaustion; recovery evidence; local state versus replicated state.

**Competency purpose:** Locate durable state; test a recovery claim; distinguish backup from replication; state loss bounds; diagnose a failed or incomplete migration; estimate recovery cost; and judge operational complexity against the small baseline.

**Build opportunity:** Add a minimal versioned schema change only when the domain has an actual evolution need; create a documented backup; restore into a clean instance; run a recovery checklist; use bounded disk/resource limits in a local sandbox.

**Observe opportunity:** Inspect database files, schema/migration history, disk usage, backup/restore logs, timestamps, and restored state. Compare a clean restore with a missing or stale backup.

**Break opportunity:** Interrupt a migration; restore an old backup; fill a bounded filesystem; start with a missing/corrupt file; kill a process during a write; verify what can be recovered and what cannot.

**Explain / Judge requirement:** Explain what “committed,” “backed up,” and “replicated” each mean. State RPO/RTO assumptions and who owns recovery complexity. Judge a copied fixture, SQLite backup, migration, replica, and managed backup without treating any one as automatically superior.

**Invariant:** A completed migration has a known schema version; restore produces a readable database with declared loss bounds; failed migration does not claim success; restored data still satisfies ownership and visibility invariants.

**Failure mode:** Partial migration; backup taken at the wrong point; corrupt or missing backup; disk full; data loss after crash; restore that starts but violates application invariants.

**Security/privacy decision:** Backups contain private data and require the same fixture/redaction discipline as the live database; protect backup permissions; do not upload real learner or user data; document retention and deletion of test backups.

**Measurement/evidence artifact:** Recovery runbook, migration history, backup/restore transcript, state diff against declared RPO, bounded resource-failure trace, and a cost/complexity comparison with the static-fixture alternative.

**Mechanism ownership:** **Combination.** Classic storage/database Labs teach durability, WAL, recovery, and isolation. The project integrates backup, restore, migration state, and user-data invariants.

**Deliberately postponed:** Managed backups; multi-region disaster recovery; object-store guarantees; compliance certification; high-availability databases; automatic migration orchestration.

**Simpler alternative:** Copy and restore a static fixture to teach state location and recovery evidence before introducing schema migration.

**When NOT to add:** Do not add a migration framework before schema evolution is an actual problem. Do not confuse a second copy, a backup, and a tested restore; do not add cloud backup products to create realism.

**Beyond-the-Project transfer case:** Package-lock updates, VM snapshots, notebook checkpoints, generated build artifacts, and data-pipeline checkpoints all require versioned recovery thinking.

### P7 — Deployment boundary and reproducible environment

**Earliest safe Module entry:** Native reproducibility can begin at `M00`/`M06`/`M08` with a documented Linux run path, virtual environment, shell script, and pinned dependency set. The container mechanism belongs at `M19` after OS process/memory/files foundations and the distributed failure context required by the Module DAG.

**Primary Module/Stage home:** `M19` / `S6` for containers, namespaces, cgroups, images, deployment boundaries, and cloud/resource reasoning. P7 should be a native-versus-container comparison, not a container-first project requirement.

**Prerequisite Modules:** Native reproducibility: `M00`, `M06`, `M08`. Container mechanism: hard `M06`, `M07`, `M08`, and `M16` per the current DAG; `M19` supplies the canonical teaching home. `M20` is not required, and no Kubernetes knowledge is required.

**Concepts exposed:** Executable artifact; environment; dependency; process versus image; namespace; cgroup; filesystem/mount; port; configuration/state boundary; reproducibility versus isolation; build provenance; resource limit.

**Competency purpose:** Explain image versus running process; identify configuration, executable, and durable-state boundaries; reproduce a run; distinguish reproducibility from security isolation; diagnose missing dependency/configuration/resource failure; and learn a deployment description from authoritative sources.

**Build opportunity:** First provide one canonical native Linux run path. Later, optionally build/run one container containing the same single service and compare it with the native process. Preserve one process and one database unless a separate constraint is justified.

**Observe opportunity:** Compare processes, mounts, ports, environment, image layers, startup logs, resource limits, and external state. Inspect what is isolated and what still depends on the host kernel.

**Break opportunity:** Remove a dependency; omit configuration; cap memory/CPU; delete the container while preserving or losing external state deliberately; use an incompatible image/runtime; make the service unavailable during startup.

**Explain / Judge requirement:** State what the container buys for this course and what it does not guarantee. Judge a virtual environment, reproducible shell script, VM, native process, and container for the stated constraint. Explain which complexity moved into the runtime, host, image, or volume.

**Invariant:** The same declared input and environment produces the same specified service behavior within stated limits; durable state is not accidentally hidden inside an ephemeral image; containerization does not weaken authorization or data ownership.

**Failure mode:** “Works on my machine”; missing dependency; image/runtime mismatch; inaccessible volume; memory or CPU exhaustion; hidden host dependency; false security confidence; lost state on container deletion.

**Security/privacy decision:** Use local images and synthetic data; pin or record provenance for dependencies; bind only to local interfaces by default; do not treat a container as a security boundary against a hostile host; avoid registry credentials and public image pulls unless an explicit Source Expedition requires them.

**Measurement/evidence artifact:** Native/container comparison sheet, reproducibility record, process/mount/port inspection, one resource or configuration failure trace, image/dependency provenance note, and a judgement of whether the container is worth its setup cost.

**Mechanism ownership:** **Combination.** OS Labs teach process, memory, and filesystem mechanisms; the Docker/container Source Expedition is optional and bounded. The project integrates reproducibility and state-boundary judgement.

**Deliberately postponed:** Kubernetes; service mesh; orchestration; cloud IAM; autoscaling; registry operations; multi-container decomposition; image supply-chain policy beyond the bounded provenance question.

**Simpler alternative:** A reproducible shell script, Python virtual environment, or native Linux process is the canonical path when environment mismatch is the only constraint.

**When NOT to add:** Do not require Docker when it hides process/syscall teaching, requires unsupported host setup, or makes the canonical Linux path less reproducible. Do not split the app into services to justify containers.

**Beyond-the-Project transfer case:** Hermetic builds, package managers, virtual machines, CI runners, and mobile sandboxes make similar artifact, dependency, and isolation trade-offs.

### P8 — Instrumentation before scaling

**Earliest safe Module entry:** Basic explicit timers and structured local logs can recur from `M00`, `M04`, `M10`, and P3. The canonical cross-layer observability checkpoint belongs at `M20`, after the learner has a failure question and the `M16`/`M19` context needed for distributed and infrastructure signals.

**Primary Module/Stage home:** `M20` / `S6` for metrics, logs, traces, correlation, SLOs, incident evidence, and privacy-aware telemetry. `M23`/`M24` revisit measurement methodology and evidence-based claims.

**Prerequisite Modules:** Basic timing/logging: `M00` and `M04` or `M10`. Full observability integration: hard `M16` and `M19` through `M20`; `M11` is a soft aid for HTTP/navigation metrics. No tracing backend is required before the diagnostic question exists.

**Concepts exposed:** Structured log; metric; duration; trace; span; correlation ID; cardinality; sampling; missing signal; causal evidence; overhead; retention; SLO/SLI concept; privacy-aware telemetry.

**Competency purpose:** Observe hidden behavior; distinguish symptom from cause; correlate one request across process/database boundaries; state what the evidence cannot prove; diagnose an injected failure; and judge telemetry value against overhead, storage, and privacy cost.

**Build opportunity:** Instrument one request path and one failure path with structured local logs and basic request/database duration metrics. Add one local trace or OpenTelemetry-compatible comparison only when it answers a named question; do not require a vendor backend.

**Observe opportunity:** Compare logs, metrics, and trace spans; follow a request ID; inspect missing or sampled signals; measure instrumentation overhead; inspect redaction and high-cardinality behavior.

**Break opportunity:** Inject latency or an error; lose telemetry; create a high-cardinality label; sample away the interesting request; log a private field in a controlled fixture; compare a signal that shows symptom with one that helps locate cause.

**Explain / Judge requirement:** State which signal answers which question, what causal link is supported, what evidence is missing, and whether a backend or trace is justified. Explain why a dashboard is not itself observability and why telemetry can create a privacy/security failure.

**Invariant:** Telemetry does not change user-visible correctness; secrets/private content are excluded or redacted; each selected request retains a documented correlation path; instrumentation overhead and missingness are stated.

**Failure mode:** Missing logs; misleading aggregate metric; trace sampling gap; high-cardinality cost; telemetry outage; sensitive data leakage; instrumentation changing timing or behavior.

**Security/privacy decision:** Define fields, redaction, retention, access, and deletion before collecting telemetry. Never use note content, credentials, or raw tokens as labels. Keep telemetry local and synthetic; state whether evidence is suitable for sharing.

**Measurement/evidence artifact:** Diagnostic question, instrumented trace/log/metric packet, injected-failure trace, redaction review, overhead measurement, missingness/limits statement, and decision on whether additional tooling is warranted.

**Mechanism ownership:** **Combination.** Measurement and observability Source Expeditions teach signals and limits; the project provides a natural cross-layer failure path and privacy-sensitive telemetry gap.

**Deliberately postponed:** Vendor dashboards; full SRE platform; anomaly-detection AI; collector internals; long-term production retention; observability added without a diagnostic question.

**Simpler alternative:** Structured local logs plus explicit timers around known boundaries. This is the canonical first signal set.

**When NOT to add:** Do not add a tracing backend, collector, or dashboard before a learner can formulate a failure/performance question that the simpler evidence cannot answer.

**Beyond-the-Project transfer case:** Compiler profiling, OS tracing, database query plans, batch-job counters, and build telemetry are observability for non-web systems.

### P9 — System Defense candidate state

**Earliest safe Module entry:** Scenario cards and rejection judgements can appear in `M23` once the learner has enough mechanisms to compare alternatives. The final System Defense belongs at `M24` after the shared S1–S6 chain and `M23` judgement toolkit. A learner may practice one constrained case earlier, but that is not the final defense.

**Primary Module/Stage home:** `M23`–`M24` / `S7` for systems judgement, security/privacy, cost, measurement, failure analysis, and defended architecture. P9 is the capstone integration surface, not a requirement to add infrastructure.

**Prerequisite Modules:** Final defense: `M23`, complete shared `S1`–`S6` traversal, and the security synthesis material required by the current architecture. Specific scenario cards may use a smaller subset, but their scope must be stated. `M17`/`M18`/`M19` are concepts to judge, not automatically project dependencies.

**Concepts exposed:** Partial failure; consistency; queue and replica alternatives; trust boundaries; privacy; cost/resource economics; evidence; assumptions; scale thresholds; complexity moved elsewhere; rejection as an engineering decision.

**Competency purpose:** Integrate Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, and Learn-New-Tech. The learner must defend the smallest justified evolution or defend keeping the simpler design, under changed constraints.

**Build opportunity:** No required production component. Given a scenario—tenfold read load, intermittent storage, asynchronous export, stricter privacy, regional latency, or a restore deadline—the learner may implement one narrow change in a branch or produce a design experiment. Rejection is equally valid when evidence supports it.

**Observe opportunity:** Produce an architecture/state diagram, request/data/control trace, measurements, failure trace, invariant list, cost/resource estimate, security/privacy boundary, recovery evidence, and rejected alternatives.

**Break opportunity:** Defend behavior under timeout, duplicate submission, stale read, failed replica, lost telemetry, compromised credential, restore failure, or privacy leak. The scenarios must remain bounded and authorized; no public attack target is required.

**Explain / Judge requirement:** Answer: Where is state? Where does time go? Where can it fail? How would we know? What must remain true? What are we paying for? At what scale does the proposed change become worthwhile? Why is the simpler design better or worse?

**Invariant:** The defense names assumptions and preserves user/data/security invariants under the chosen failure model; evidence supports claims; uncertainty and unknowns are explicit; no component is admitted merely because it is common in production.

**Failure mode:** Adding infrastructure without a constraint; confusing availability with durability; ignoring stale or duplicate state; relying on missing telemetry; accepting an unbounded threat or cost claim; defending architecture vocabulary without mechanism evidence.

**Security/privacy decision:** Include trust boundaries, credential/data handling, privacy retention, telemetry redaction, accessibility/user impact where relevant, and the security consequences of each proposed alternative. Encryption is not treated as anonymity, and a cloud provider is not treated as a trust boundary explanation.

**Measurement/evidence artifact:** The final evidence packet: request/data/control trace; transient/process/database/backup/telemetry/credential state inventory; invariant/failure matrix; measurements with workload and limits; security/privacy decisions; latency/resource/cost estimates; selected evolution or rejection; recovery evidence; three alternatives and moved complexity; explicit unknowns and source-learning plan.

**Mechanism ownership:** **Project integration + Source Expedition/case analysis.** Classic Labs remain responsible for component mechanisms. The project owns the cross-layer defence and the genuine integration question: what is the smallest justified change?

**Deliberately postponed:** Mandatory queue; cache; replica; PostgreSQL cluster; reverse proxy; service mesh; cloud deployment; microservice decomposition; feature-building contest; public production launch.

**Simpler alternative:** Keep P8 and defend rejection of the proposed technology, or improve measurement/runbook/schema/query before adding a component.

**When NOT to add:** Do not turn the final defense into a feature-build contest, infrastructure checklist, or vendor certification exercise. Do not pass a design because it has more components.

**Beyond-the-Project transfer case:** Defend a build cache, local database, data pipeline, compiler service, batch workflow, or messaging system under the same requirements, guarantees, failure, cost, privacy, and evidence questions.

## 4. Project order versus curriculum dependency integrity

### 4.1 The project sequence is not a curriculum DAG

`P0 → P1 → ... → P9` is a deliberate project evolution narrative: each milestone changes one meaningful system constraint. It is not a list of hard curriculum prerequisites. A learner may meet a project milestone as a bounded integration revisit before its canonical mechanism is taught, or the curriculum may teach a mechanism before the project needs it. The project must record which of those situations applies.

The corrected module graph remains:

```text
S1 → S2 → S3
           ├─→ S4 ─┐
           └─→ S5 ─┴─→ S6 → S7
```

In particular:

- `S4` Network/Web and `S5` Data/Concurrency are partially independent after `S3`.
- The recommended request-centric narrative may show S4 before S5, but there is no hard `S4 → S5` Stage edge.
- `M10` and `M14`/`M15` both feed `M16`; a project’s P3-before-P5 ordering does not make network knowledge a hard prerequisite for all data/concurrency work.
- `M14 → M16` remains soft. `M14 → M17` remains hard because distributed consistency needs the single-node consistency model.
- A `P` relationship is project integration, not a curriculum prerequisite.

### 4.2 Potential false prerequisites and resolution

| Apparent conflict | Why it would be false | Alignment resolution |
|---|---|---|
| P1 must wait for the full Web module because it may use HTTP | The process/interface idea precedes HTTP; HTTP is only one transport case | Introduce function/CLI/process boundaries at M00/M06; defer HTTP to M11/M12 |
| P2 must be taught in S7 before P3 can use the network | A local authorization fixture is not the full security synthesis | Permit bounded ownership/authorization integration early; teach canonical security at M21/M22; keep P3 local and non-public |
| P3 must wait for P2’s canonical authn/authz | Network timeout/idempotency is a distinct S4 mechanism | Use synthetic/fixed local identity or no auth for the P3 network experiment; do not expose the service publicly |
| P4 must wait for P3 and therefore for S4 | Project narrative order is not module dependency; DB storage/indexing follows S3 directly | Place P4 on the S5 branch after M08/M09/M13; do not require M10–M12 |
| P5 must wait for all of S4 because the project did P3 first | Transactions and concurrency have direct S3/M13/M14/M15 foundations | Teach P5 on the S5 branch; P3 is only a prior project state, not an H edge |
| P6 must wait for P5 to teach durability | Durability is first introduced at M09 and revisited in M14 | Use P6 after the P5 project state if desired, but do not add a curriculum edge P5 → M09 |
| P7 should introduce containers immediately after P6 | The current M19 DAG requires process/memory/files and M16 failure context; containers are not a beginner prerequisite | Use a native reproducible run path earlier; place optional container comparison at M19 |
| P8 should require a tracing backend before any diagnosis | Observability begins with measurement, logs, and timers; M20 formalizes it later | Start with local signals; add a trace only for a named cross-boundary question |
| P9 requires every distributed component to have been built | System Defense tests judgement, not infrastructure accumulation | Permit design, evidence, or rejection; full implementations remain Lab/Deep Dive material |

### 4.3 Default learner narrative

The default narrative may still present `S4` before `S5` because a browser request is a motivating whole-system journey. That is a pedagogical preference, not a hard prerequisite. A data-first path may teach `M13`–`M15` after `S3`, then return to `M10`–`M12`; the Mini Cloud App can be used in either order as long as the checkpoint identifies whether it is an orientation, revisit, or canonical mechanism application.

The project sequence therefore needs a small annotation in future implementation materials: **project order**, **canonical mechanism home**, and **required curriculum prerequisites** must be separate fields. No change to the existing evolution file is made by this proposal.

## 5. Technology admission review

The default result is deliberately conservative: no listed component is required in the canonical Mini Cloud App path merely because it is common in production. Each component must clear a named constraint, stable mechanism, educational gain, evidence plan, and complexity threshold. A component can be a bounded classic Lab, Source Expedition, or optional project branch without being admitted to the canonical project.

| Component | Problem / constraint | Stable mechanism | Educational gain | Cost / complexity moved elsewhere | Failure modes | Simpler alternative | When NOT | Admission threshold |
|---|---|---|---|---|---|---|---|---|
| **PostgreSQL** | A server database may be needed for concurrent clients, richer workload, server-managed MVCC/isolation, or an explicit client/server database comparison. | Client/server DB; pages/indexes/planner; MVCC; transactions/isolation; server-managed concurrency. | Makes database process boundaries, `EXPLAIN`, MVCC, serialization failures, and operational state observable after SQLite fundamentals. | Setup/version/package burden; connections/configuration; database auth and backup surface; more moving state; danger of mistaking a larger product for a better invariant. | Connection exhaustion; isolation anomalies; serialization failures; misconfiguration; version drift; misleading plan/benchmark comparison. | SQLite for one-process durable state; a local SQLite transaction/index exercise. | Do not add for fashion, résumé value, or an unmeasured workload; do not replace the SQLite baseline. | **Optional Adapt/Source Expedition, not canonical baseline.** Require a stated concurrent/server-managed constraint, dataset/concurrency/latency evidence, and version/provenance record. |
| **Cache** | Repeated equivalent reads measurably consume latency/bandwidth and have a valid freshness policy. | Reusable copy; keying; eviction; freshness/invalidation; hit/miss measurement. | Teaches that a copy requires a validity policy and exposes locality, latency, staleness, privacy, and cost trade-offs. | Invalidation and stampede logic; memory; key design; observability; privacy leaks; more state to recover; false performance conclusions. | Stale private data; wrong key scope; cache stampede; unbounded memory; invalidation race; warm-cache benchmark bias. | Better query/index shape; database/page cache; HTTP cache case; no cache. | Do not add before a repeated-read workload and acceptable staleness bound are stated; do not add to make P4 faster by assumption. | **Do not add to canonical path.** Admit only as a bounded branch after baseline measurement, explicit freshness/correctness invariant, privacy keying review, and hit/miss evidence. |
| **Queue** | Work is too slow or bursty for the request path, or producer/consumer rates measurably differ; asynchronous completion is acceptable. | Durable/asynchronous handoff; buffering; consumer concurrency; acknowledgement and delivery semantics. | Teaches delivery guarantees, buffering, duplicate processing, ordering, idempotency, and the trade between immediate certainty and decoupling. | Another durable state, consumer lifecycle, retries, poison-message handling, visibility/ack semantics, operations, and debugging surface. | Duplicate delivery; lost/poison message; reordering; stuck consumer; unbounded backlog; false exactly-once claim. | Synchronous call; local batch; durable job table/outbox only when atomic handoff is the question. | Do not add for one small export, “cloud realism,” or to hide a slow operation without measuring it. | **Reject as required project component; scenario-only.** Admit a local queue/broker case only after a bounded latency/backlog constraint, delivery invariant, duplicate test, and retry policy are specified. |
| **Container** | Dependencies/environment are not reproducible, or process/filesystem/resource boundaries are the explicit learning target. | OS-level process isolation via namespaces/cgroups; image/artifact packaging; host-kernel sharing. | Makes artifact versus process, resource limits, host dependence, and reproducibility visible. | Image builds, host/runtime setup, volume/state confusion, provenance, platform support, extra debugging, false security confidence. | Missing volume; lost ephemeral state; resource OOM; host-kernel mismatch; image drift; exposed port; dependency omission. | Native Linux process; virtual environment; reproducible shell script; VM when isolation is the target. | Do not require it when it hides syscalls/processes, blocks learners on host setup, or makes the native path less reproducible. | **Optional P7 comparison, not canonical prerequisite.** Admit when a reproducibility/isolation question is explicit, native baseline exists, and process/memory/files mechanisms have been taught. |
| **Reverse proxy / TLS termination** | A public entry point must route to an origin, centralize policy, or terminate TLS; the hop/trust boundary itself is the learning target. | Intermediary/gateway; connection termination; routing; forwarded identity; TLS authentication/confidentiality boundary. | Shows how intermediaries relocate authority, protocol, failure, certificate operations, and end-to-end guarantees. | New trust boundary; forwarding-header policy; certificate issuance/renewal; origin exposure; double termination; more ports/processes; operational config. | Header spoofing; origin bypass; incorrect client-IP/auth assumptions; certificate failure; plaintext internal hop mistaken for end-to-end security. | Direct local service; direct TLS in a bounded local case; no intermediary. | Do not add to imitate production or before direct HTTP/TLS semantics are understood; do not expose a teaching origin publicly. | **Optional infrastructure/security case, not baseline.** Require a clearly stated routing/certificate/policy boundary and evidence that direct service cannot expose the mechanism as clearly. |
| **TLS termination as a separate concern** | The learner must distinguish transport authentication/confidentiality from proxy routing and understand where encryption ends. | TLS handshake/certificate verification at a selected endpoint; encrypted client-proxy and possibly proxy-origin hops. | Clarifies trust anchors, certificate identity, hop-by-hop versus end-to-end protection, and privacy claims. | Certificate lifecycle, secrets, renewal, local CA setup, proxy configuration, and risk of teaching an invalid production posture. | Expired/wrong certificate; untrusted CA; plaintext origin; forwarded-secret leakage; false end-to-end claim. | `curl`/`openssl` against a local HTTPS endpoint without a proxy; RFC/Source Expedition. | Do not terminate TLS in the project solely to obtain a padlock or cloud-like appearance; do not use real credentials/data. | **Bounded Source Expedition or optional case.** Require a named certificate/trust-boundary question, local safe target, redaction, and explicit hop guarantee. |
| **Observability tooling** | A cross-boundary failure/performance question cannot be answered by local logs/timers alone. | Correlated logs; metrics; spans/traces; sampling; cardinality; retention and missingness. | Turns “how would I know?” into evidence design; exposes causal limits, overhead, privacy, and operational judgement. | Instrumentation code; signal volume; collector/backend; retention; access controls; privacy review; false confidence in dashboards. | Missing/sampled signal; high-cardinality explosion; telemetry outage; sensitive field leakage; overhead changes behavior. | Structured local logs and explicit timers. | Do not add a vendor backend, collector, or dashboard before a named diagnostic question. | **Minimal signals are admitted at P8/M20; backend tooling is optional.** Require diagnostic question, redaction policy, evidence artifact, overhead/retention estimate, and local reset path. |
| **Replicas** | Availability, read locality, or durability needs multiple copies under a stated failure model and SLO/RPO/RTO. | Synchronous/asynchronous replication; leader/follower; quorum; consistency lag; failover. | Makes copies, consistency, failover, and cost visible; supports a distributed judgement case. | Coordination, stale reads, split brain, failover operations, credentials, storage/compute cost, debugging complexity. | Read-your-writes failure; divergence; split brain; lost acknowledged write; failover loop; stale private data. | One process/database; tested backups; restart/runbook; read optimization before replication. | Do not add without a failure model, workload, SLO/RPO/RTO, consistency invariant, and evidence simpler operation is insufficient. | **Do not add to Core baseline.** Admit only as an M17/P9 scenario or bounded replica experiment after M16/M17 concepts and a controlled local failure plan. |
| **Distributed components** | Independent scaling, partial-failure isolation, asynchronous ownership, or a real cross-machine constraint requires more than one service/component. | Remote call/RPC; partial failure; coordination; independent state; message or service boundary. | Makes distribution, failure ambiguity, ownership, and coordination concrete when a single process no longer answers the question. | Network and deployment topology; version compatibility; retries; identity; tracing; operational and cost surface; more invariants. | Partial failure; retry storm; split-brain ownership; duplicate effects; incompatible versions; missing telemetry. | One process with modules; one database; local function/CLI/process boundary; scenario analysis. | Do not decompose for architecture fashion, microservice vocabulary, or to create more deployables. | **Reject as canonical project default.** Admit only when a named constraint cannot be observed with a single process and the learner can state cross-component invariants and evidence. |
| **Deployment automation** | Repeated deployment is error-prone, rollback/verification needs evidence, or a controlled pipeline mechanism is the learning target. | Build artifact; provenance; repeatable steps; verification gate; rollback/roll-forward; environment configuration. | Connects reproducibility, supply chain, operational failure, and evidence without requiring a vendor platform. | CI platform/version churn; credentials; secret management; pipeline debugging; hidden remote state; maintenance and cost. | Deploy wrong artifact; secret leakage; partial rollout; unverified migration; failed rollback; environment drift. | Documented shell script and manual checklist with evidence; local one-command run. | Do not add automation before a repeatable manual path exists or merely to appear production-like. | **Optional bounded P7/P9 case, not canonical baseline.** Require repeated manual failure/evidence, pinned artifact/provenance, safe local credentials, rollback or verification claim, and a clear complexity ledger. |

### Technology admission conclusion

The canonical Mini Cloud App remains a single-process, local/safely bounded service with one durable collection and minimal evidence instrumentation. PostgreSQL, cache, queue, container, reverse proxy/TLS termination, replicas, distributed components, and deployment automation are not mandatory project components in v0.1. Minimal observability—structured logs and explicit timing—is admitted because evidence is a horizontal competency, not because a dashboard is modern. Optional cases must be removable without breaking the shared system journey.

A technology admission record must name: the problem, constraints, stable mechanism, competency gain, new failure modes, complexity moved, simpler alternative, When-NOT case, evidence artifact, and qualitative threshold. No universal request-count threshold is asserted.

## 6. Lab separation and project-specific gaps

### 6.1 Mechanisms better taught by a classic Lab or Source Expedition first

| Mechanism | Primary non-project teaching location | Project checkpoint that may revisit it | Boundary |
|---|---|---|---|
| Bits, encodings, serialization, and size | M01 classic representation experiment; CS:APP Data Lab or local hexdump/bytes adaptation | P0 serialized item and size evidence | P0 uses representation; it does not replace bit/encoding teaching |
| Algorithms, data structures, and complexity | M02 classic data-structure/scaling exercise | P4 query shape/index workload | The app supplies a workload, not a general algorithms course |
| ISA, call frames, memory, locality | M03/M04 CS:APP disassembly/cache adaptation or equivalent | Optional P0/P4 timing/state observation | The project must not become a machine/cache implementation lab |
| Processes, syscalls, files, and virtual memory | M06–M09 xv6/OSTEP slice, `strace`, `/proc`, filesystem inspection | P1 process boundary; P0/P6 state and file inspection | Teach OS mechanisms before asking the project to diagnose them |
| TCP byte stream, reliability, and HTTP semantics | M10/M11 RFC + `curl`/local server; bounded CS144 adaptation | P1/P3 request boundary and timeout | Do not build a TCP stack or framework syllabus in the project |
| Browser process/render/origin model | M12 browser/DevTools mechanism case | Optional thin browser-facing revisit after P1/P2 | P1/P2 do not require front-end development |
| Database pages, indexes, plans, transactions, and recovery | M13/M14 SQLite/PostgreSQL bounded experiment; EXPLAIN/isolation Source Expedition | P0/P4/P5/P6 | PostgreSQL remains optional comparison after SQLite |
| Thread interleavings, semaphores, locks, and deadlock | M15 OSTEP v1.10 Threads (Semaphores) adaptation | P5 controlled application race harness | The project does not replace the mechanism lab with stress tests |
| Partial failure, replication, consensus, and queue semantics | M16–M18 classic case/Source Expedition; bounded local experiment | P9 scenario or selected narrow branch | No required Raft implementation, broker, or replica |
| Containers and resource isolation | M19 native process versus optional container Source Expedition | P7 comparison | Native Linux path remains canonical |
| Observability signals and measurement validity | M20/M23 logs/timers/trace comparison and measurement case | P8 cross-layer failure evidence | Start with a question and local signals, not a vendor platform |
| Trust, crypto use, authn/authz, secure composition | M21/M22 safe defensive lab/Source Expedition | P2 authorization/privacy integration; P9 security defense | The project is not an exploit-training target |

### 6.2 Project checkpoints that should only revisit/integrate mechanisms

- **P0** revisits representation, files, durability, and database state as one trace; it does not teach SQLite internals or replace a storage lab.
- **P1/P3** integrate process, interface, socket, and HTTP boundaries; they do not replace OS/network mechanism experiments.
- **P2** integrates ownership, trust, privacy, and authorization; it does not replace a canonical crypto/authn/authz explanation or authorize real identity-provider work.
- **P4** integrates query workload, index judgement, and measurement validity; it does not replace a general data-structure or database engine lab.
- **P5** integrates transaction/concurrency mechanisms with domain ownership; it does not replace deterministic race, semaphore, or isolation labs.
- **P6** integrates migration, backup, restore, and user-data invariants; it does not replace a storage recovery experiment.
- **P7** integrates reproducibility and state boundaries; it does not replace process/memory/files teaching or require orchestration.
- **P8** integrates evidence across one request path; it does not replace measurement methodology or observability signal teaching.
- **P9** integrates and judges mechanisms; it does not require every learner to implement a distributed component.

### 6.3 Genuine project-specific Build gaps

Build is justified only where a proven mechanism activity does not supply the intended cross-layer integration:

1. **Integrated boundary experiment:** A small original harness may be needed to carry one domain operation from client/interface through process, storage, failure, and evidence. This is a project checkpoint, not a replacement for any classic mechanism lab.
2. **Authorization/privacy experiment:** If no license-cleared, safe, resettable defensive target fits the P2 outcome, a small course-owned fixture may be built. It must bind locally, use synthetic data, omit offensive workflows, and include regression tests.
3. **Cross-layer failure/observability fixture:** If adapted logs/timers/traces cannot correlate one injected timeout, latency, or storage failure across layers, a small original fixture may be built for P8.
4. **Concurrency-to-application integration:** A controlled P5 race harness may be built after a proven concurrency/isolation lab, because classic exercises do not necessarily preserve the app’s ownership and sharing invariants.
5. **Evidence packet scaffolding:** A project-owned evidence template and resettable fixture may be necessary so learners can submit traces, measurements, invariant checks, privacy decisions, and rejected alternatives consistently.

No custom final Lab, OS, network stack, database engine, queue platform, or distributed service is justified by this alignment artifact.

## 7. Audit and Issue #9 reconciliation

The Issue #2 recommendations are reconciled here without importing CS2023 hours or expanding the project domain.

| Audit recommendation | Outcome for this alignment | P0–P9 / Module implication | Remaining architecture action |
|---|---|---|---|
| R1 applied discrete/probability/statistics/scale reasoning | Integrate as a just-in-time horizontal toolkit, not a standalone prerequisite sequence | Size in P0; complexity and workload in P4; failure/availability estimates in P3/P9; measurement uncertainty in P4/P8/M23 | #9 should make the applied toolkit and assessment pattern explicit without adding a separate degree-style math track |
| R2 shell/debugging/Git/testing/reproducibility | Integrate into M00 and every evidence packet; strengthen as lab prerequisites | All milestones require reset, test, trace, or evidence discipline; P7 makes reproducibility visible | #9 should define minimum toolchain/SDF outcomes and lab entry criteria |
| R3 HCI/accessibility/user boundary | Architecture question remains open; add bounded user-facing checks to P2/P9 rather than inventing a Web syllabus | P2 denial/error/privacy interaction; P9 affected users, accessibility, consent, and recovery where relevant | Preserve `OQ-BP-003`; resolve by RFC/Decision if it changes Core scope |
| R4 bounded AI literacy | Do not silently decide Core placement in this project artifact; treat AI-assisted claims as a Current Case for evidence verification | P9 may require judging an AI-related proposal, cost, privacy, and evaluation; no AI feature is added to the app | Preserve `OQ-BP-001`; #9 must use RFC/Decision for Core thread/module versus Current Case |
| R5 AI-output verification | Bounded Current Case | Any generated code/config/claim is an untrusted hypothesis checked by source, test, measurement, and security review | Integrate into tool/source-verification policy, not project business scope |
| R6 data modeling/encoding/evolution/provenance/derived data | Integrate into existing M01, M13, M14, M16, and P0/P4/P6/P9 | P0 schema/serialization; P4 query workload; P6 schema evolution; P9 provenance and alternatives | #9 should protect these outcomes without broadening database product coverage |
| R7 experimental measurement/diagnosis | Integrate as a required evidence pattern across all milestones | Every card includes prediction, baseline or stated observation, controlled failure/change, measurement, limit, and conclusion | #9 should make this pattern part of competency assessment and lab DoD |
| R8 security/privacy/SEP horizontal evidence | Integrate horizontally; not only in S7 | P0 data minimization; P2 authorization/privacy; P3 local exposure; P4 query privacy; P6 backups; P7 provenance; P8 telemetry; P9 threat/impact judgement | #9 should verify evidence occurs before final synthesis |
| R9 computational models and limits | Integrate into M02/M05; project uses the practical representation/algorithm/runtime connection | P0/P4 judge representation/query choices; no project compiler is added | #9 should confirm M02/M05 outcomes and avoid project-driven theory expansion |
| R10 consensus as concept | Keep as Core concept/case, not project implementation requirement | P9 can judge replication/coordination alternatives; M17 owns canonical concept | Final Lab/Source Expedition selection remains Issue #4 + Lead review |
| R11 consensus/replicated-service implementation | Deep Dive/optional Source Expedition | No mandatory P9 replica or Raft build | Preserve the boundary in #9’s lab map |
| R12 physical/embedded/real-time case | Deep Dive pending evidence | No P0–P9 dependency or feature | Keep as architecture question, not a project addition |
| R13 cloud/orchestration products | Stable mechanisms Core, replaceable products Current Case/Deep Dive | P7/P9 explicitly reject mandatory orchestration; container is optional | #9 should retain vendor-neutral infrastructure boundary |
| R14 full kernel/protocol/compiler/DB implementation | Deep Dive; small Adopt/Adapt slices only | Project checkpoints integrate, never replace, classic Labs | #9 should preserve Adopt → Adapt → Build and license gates |
| R15 quantum/specialist topic inventory | Reject from v0.1 Core/project path | No milestone dependency or feature | No action unless a later RFC demonstrates a cross-cutting dependency |

## 8. Proposed changes to the existing P0–P9 proposal

These are proposed reconciliations for Issue #9. They are not edits to `mini-cloud-app-evolution-v0.1.md` in this task.

1. **Add an explicit three-way label to each milestone:** project entry point; canonical mechanism home; and curriculum prerequisites. This prevents an early black-box integration from becoming a false hard dependency.
2. **Clarify P0:** SQLite is a bounded baseline and state surface, not a demand to teach database internals before M13. The evidence packet must distinguish a library guarantee from an observed application result.
3. **Clarify P1:** A local CLI/process boundary is the default. HTTP is conditional on M11/M12 and must not create a web-framework syllabus.
4. **Clarify P2:** Ownership and authorization may be integrated with a course-owned local fixture after P0, while full authn/authz and crypto use remain canonical M21/M22 material. Real identity providers remain out of scope.
5. **Clarify P3:** Network failure work follows M10/M11 and need not wait for canonical P2 security synthesis or S5. A local safe identity fixture may be used, and public exposure is prohibited.
6. **Strengthen P4:** Require benchmark metadata, correctness comparison, distribution, warmup/repetitions, and query-plan evidence before an index is admitted.
7. **Strengthen P5:** Require a classic concurrency/isolation mechanism exercise first, then use the app for ownership-aware integration and deterministic failure control.
8. **Narrow P6:** Add migrations only when schema evolution is an actual problem; teach backup/restore evidence before managed or multi-region recovery.
9. **Narrow P7:** Make native Linux reproducibility canonical and container comparison optional. Do not let the project force a container before M19’s DAG prerequisites.
10. **Strengthen P8:** Make structured local logs and timers the first path; traces/backends require a diagnostic question and privacy/overhead evidence.
11. **Strengthen P9:** Make rejection a passing engineering outcome. Scenario cards should ask for the smallest justified change, not a component checklist.
12. **Add a horizontal evidence rule:** every milestone submission includes an invariant, controlled failure, security/privacy decision, observation/measurement, simpler alternative, and limit of inference.

## 9. Completion report

### Deliverable

- `meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md`
- Maps every `P0`–`P9` milestone to earliest entry, primary Module/Stage home, prerequisites, concepts, competencies, Build/Observe/Break/Explain/Judge activities, invariant, failure, security/privacy, measurement/evidence, mechanism ownership, postponements, simpler alternative, When-NOT guidance, and transfer case.
- Re-evaluates PostgreSQL, cache, queue, container, reverse proxy/TLS termination, observability tooling, replicas, distributed components, and deployment automation.
- Separates classic mechanism teaching, project integration, Source Expeditions, and conditional Build gaps.
- Reconciles the alignment with Issues #2, #4, and #9 while preserving unresolved architecture questions.

### Files changed

- Created only `meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md`.
- Did not modify the existing Mini Cloud App evolution map, Curriculum Map, Dependency Graph, Competency Matrix, canonical project code, status, decisions, or open-question files.

### P0–P9 mapping summary

- **P0:** Single-process durable baseline; SQLite is a bounded state surface; canonical storage/database mechanisms remain in M08/M09/M13.
- **P1:** Narrow process/interface boundary; CLI first, HTTP only when M11/M12 make it educationally relevant.
- **P2:** Local multi-user ownership and explicit authorization/privacy; full security synthesis remains M21/M22.
- **P3:** Real local network path, timeout ambiguity, retry/idempotency; S4 branch, independent of S5.
- **P4:** Measured query/index trade-off; S5 M13 integration, no premature cache.
- **P5:** Transactional and concurrent correctness under controlled races; S5 M14/M15 integration after classic mechanism teaching.
- **P6:** Recovery, migration, backup/restore, and RPO/RTO evidence; durability is not replication.
- **P7:** Native reproducibility first; optional container comparison at M19.
- **P8:** Local logs/timers first; cross-layer observability at M20 only for a diagnostic question.
- **P9:** System Defense under changed constraints; no required infrastructure and rejection is valid.

### Proposed changes to existing P0–P9

- Add project-entry versus canonical-home versus curriculum-prerequisite labels.
- Make CLI/native/simple baselines explicit and conditionalize HTTP, migrations, containers, traces, and all distributed components.
- Require benchmark metadata, classic-lab-first separation, privacy-aware evidence, and explicit rejection paths.
- Preserve stable P IDs and the one-constraint-at-a-time evolution rule.

### Dependency conflicts found

- No actual conflict with the corrected Module DAG was found after separating project order from curriculum order.
- The main risk was interpreting P2-before-P3, P3-before-P4/P5, P6-before-P7, or P7-before-P8 as hard curriculum edges. The proposal explicitly rejects those interpretations.
- `S4` and `S5` remain partially independent after `S3`; P4/P5 use the S5 branch without manufacturing a Web prerequisite, while P3 uses S4 without manufacturing a database/concurrency prerequisite.
- P7’s optional container case respects the current M19 prerequisites, including the M16 partial-failure context; a native reproducible path remains available earlier.

### Lab/project separation findings

- Representation, algorithms, machine/cache, OS/filesystem, network/TCP/HTTP, database, concurrency, distributed coordination, container, observability, and security mechanisms are better taught first through the classic Lab or Source Expedition candidates in Issue #4.
- The project’s genuine gaps are cross-layer state/boundary integration, ownership-aware concurrency, safe authorization/privacy evidence, cross-layer failure telemetry, and a reusable evidence packet.
- No project milestone justifies replacing a proven lab with a framework demo, full OS/network/database implementation, broker platform, or distributed service.

### Component admissions/rejections

- **PostgreSQL:** optional bounded comparison after SQLite; not canonical baseline.
- **Cache:** not canonical; bounded branch only after measured repeated-read problem and freshness invariant.
- **Queue:** reject as required component; scenario-only unless latency/backlog and delivery semantics justify it.
- **Container:** optional P7 comparison; native Linux path is canonical.
- **Reverse proxy:** optional infrastructure/security case; no proxy for production appearance.
- **TLS termination:** optional bounded Source Expedition; direct local TLS is simpler for the mechanism.
- **Observability tooling:** minimal structured logs/timers admitted; vendor backends not required.
- **Replicas:** no Core baseline; bounded M17/P9 scenario only with failure and consistency evidence.
- **Distributed components:** reject as canonical default; admit only for a specific non-single-process constraint.
- **Deployment automation:** optional bounded case after a reproducible manual path; no CI/CD product syllabus.

### Assumptions

- The latest fetched `origin/main` at dispatch reference `271c44e18db98da0501bc3ab99046b1a98d7340d` is authoritative for this proposal.
- The accepted P0–P9 evolution and M00–M24 map remain proposals subject to Lead/#9 reconciliation, not final released curriculum.
- SQLite remains an acceptable baseline black box for a small local durable service; using it before M13 is an integration choice, not a claim that database internals have already been taught.
- Exact lab adoption, license clearance, environment versions, and final competency rubric remain outside this parallel-safe artifact.
- No universal numerical scale threshold is asserted for technology admission; thresholds are constraint/evidence based.

### Open questions

- `OQ-BP-001`: bounded AI literacy remains an explicit Core-scope/RFC decision; this artifact does not silently place it in the project.
- `OQ-BP-003`: bounded HCI/accessibility/user-boundary treatment remains an architecture question; P2/P9 identify where evidence can be collected without inventing a Web syllabus.
- `OQ-BP-004`: S4/S5 default narrative remains a pedagogical choice; this document preserves S4-first as a recommended request-centric path, not an H edge.
- `OQ-BP-005`: final classic Lab and Source Expedition adoption still requires Lead selection, license/provenance review, setup validation, and DoD.
- `OQ-BP-006`: Python/SQLite/browser/container/observability versions remain to be pinned after Blueprint reconciliation.
- Exact identity fixture, project privacy/retention policy, final System Defense rubric, and project-versus-lab measurement placement remain for #9/Lead review.

### Prompt deviations

- None. The requested single deliverable was created, and protected files were not modified.

### Out-of-scope necessary fixes

- None identified. The proposal records follow-up questions instead of changing canonical architecture files or making unresolved decisions.

### Recommended Issue #9 Integrator review focus

1. Verify that the three-way distinction—project entry, canonical mechanism home, and hard curriculum prerequisite—survives integration into the reconciled maps.
2. Check P4/P5 placement against the parallel S4/S5 DAG and ensure no project-order annotation creates an accidental H edge.
3. Confirm whether the proposed early P2 authorization fixture fits the final security/privacy teaching ownership and does not duplicate M21/M22.
4. Decide the final classic Lab/Source Expedition boundary for P0–P8, especially database isolation, OSTEP concurrency, RFC/HTTP, xv6, and observability candidates.
5. Review whether applied MSF/statistics, HCI/accessibility, and AI-output verification have enough explicit competency/evidence treatment without expanding the app domain.
6. Recheck technology admission cards for constraint, stable mechanism, failure, cost, simpler alternative, When-NOT, evidence, and qualitative threshold.
7. Confirm that rejecting infrastructure is an assessable System Defense outcome and that no mandatory PostgreSQL, cache, queue, container, proxy, replica, distributed component, or deployment automation has entered the canonical path.
8. Before any promotion, rerun technical versions, licenses/provenance, local reproducibility, privacy policy, and learner validation against the final integrated Blueprint.
