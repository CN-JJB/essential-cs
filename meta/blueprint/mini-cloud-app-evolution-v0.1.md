# Mini Cloud App Evolution Map v0.1

Status: **DRAFTED — READY FOR WEB LEAD REVIEW**

This is an Issue #3 proposal, not a final architecture or implementation plan. Milestones use stable `P` IDs and current macro Core IDs (`00`–`15`); they do not assume Issue #1's eventual Stage names or numbering.

## 1. Purpose and anti-goals

The Mini Cloud App is a recurring integration boundary: a deliberately boring multi-user service through which learners trace data, control, state, time, failure, and responsibility across the Core. It supplies continuity, not a second curriculum.

**Anti-goals**

- It is not a web-framework survey, frontend portfolio, SaaS product, or microservices exercise.
- It does not maximize features, traffic, cloud vendors, or deployment realism.
- It does not replace mechanism-specific classic labs.
- It does not require every “modern” component; rejection is an intended design outcome.
- It does not make security, reliability, or observability late-stage decorations.

## 2. Deliberately simple domain

The service stores short personal notes and bookmarks. A user can create, read, edit, delete, and list their own items; later, an item can be shared with another named user. An item has an owner, stable identifier, text or URL, creation/update times, and optional visibility. There is no recommendation engine, rich editor, file upload, billing, social graph, search ranking, or real-time collaboration.

The initial user-facing promise is: “I can save a small item locally and retrieve exactly the item I saved.” The initial implementation may be a Python process with SQLite, a small command-line client, and—only when the Web area requires it—a thin HTTP interface. The domain remains fixed while mechanisms change.

## 3. Milestone rules

- `P0` is the baseline; later milestones change one meaningful system constraint at a time.
- A milestone is earned only when a learner can predict, observe, break, explain, and judge the changed mechanism.
- The app should expose an explicit invariant and an evidence artifact (test, trace, measurement, log, or state inspection).
- “Add” means a teaching branch or experiment unless later Blueprint work explicitly promotes it to the canonical path.
- Each milestone must name what remains intentionally invisible or postponed.

## 4. Evolution map

### P0 — One process, one durable collection

- **Macro areas:** `00`, `01`, `02`, `05`, `06`.
- **Before:** None; the learner has a domain statement and a local Python/SQLite baseline.
- **New problem/constraint:** There is no useful system until an item survives process exit and can be retrieved without ambiguity.
- **Mechanism:** Representation, serialization, identifiers, files, process state, SQLite tables and constraints.
- **Proposed change:** Implement the smallest local CRUD path: one process, one SQLite database, parameterized SQL, explicit schema, stable item IDs, and a resettable fixture.
- **Competency purpose:** Trace a value from input to representation to storage and back; state a schema invariant; distinguish memory from durable state; estimate item size.
- **Build:** Add one item and inspect the row/database file.
- **Observe:** Use SQLite inspection, filesystem metadata, and process/file observations.
- **Break:** Kill the process between operations; submit malformed/oversized input; violate a uniqueness or ownership constraint.
- **Explain/Judge:** Where is the item at each point? Why is a database preferable to an ad-hoc JSON file here, and when is it not?
- **Correctness/invariant:** Every item has one owner and stable ID; a read after a successful write returns the same committed value; invalid ownership cannot be represented.
- **Ignore/postpone:** HTTP, authentication, multiple processes, replication, migrations, full-text search, encryption at rest, and production backup policy.
- **Complexity introduced:** Schema, SQL, serialization, and durable-state failure cases.
- **Complexity moved:** SQLite owns page layout, locking, recovery details, and query execution.
- **Simpler alternative:** In-memory dictionary or append-only text; useful as a contrast, not the durable baseline.
- **When NOT to add this:** Do not add a database if the exercise is only about Python data structures or if durability is not the question.
- **Beyond the Project:** CLI configuration/state files, compiler output caches, and a batch job checkpoint all separate transient from durable representation.

### P1 — A process boundary and a narrow interface

- **Macro areas:** `04`, `05`, `07`, `08`.
- **Before:** P0 is called directly inside one process.
- **New problem/constraint:** A second client or process must use the service without importing its internals; boundaries create failure and serialization costs.
- **Mechanism:** Processes, stdin/stdout or HTTP messages, interfaces, framing, status/error representation.
- **Proposed change:** Expose the same operations through a small documented interface; retain a CLI client and add a minimal HTTP adapter only when Web concepts are taught. Keep the domain/service core independent of transport.
- **Competency purpose:** Trace a request across a boundary; explain interface versus implementation; diagnose malformed, partial, or unsupported requests.
- **Build:** Send valid and invalid requests through the interface.
- **Observe:** Capture bytes/messages, status codes, child process behavior, and timing.
- **Break:** Close the client mid-request, send truncated/extra data, stop the service, and use incompatible fields.
- **Explain/Judge:** What does the interface promise, and what does it deliberately not promise? Where should validation occur?
- **Correctness/invariant:** A request either produces one specified response or a bounded error; no malformed external input reaches SQL as code; successful mutation has one defined acknowledgement.
- **Ignore/postpone:** Framework internals, HTTP/2/3, TLS certificates, browser JavaScript, service discovery, and API version proliferation.
- **Complexity introduced:** Parsing, compatibility, boundary errors, and duplicated transport concerns.
- **Complexity moved:** The OS/runtime and protocol libraries handle sockets, buffering, and low-level parsing.
- **Simpler alternative:** Keep only a local CLI when network semantics are not the learning target.
- **When NOT to add this:** Do not add HTTP merely to make the app look like a web app.
- **Beyond the Project:** Unix pipes, compiler command-line interfaces, file formats, and library APIs are all contracts at boundaries.

### P2 — Multiple users and explicit trust boundaries

- **Macro areas:** `08`, `13`.
- **Before:** P1 accepts a caller but has no robust identity or authorization model.
- **New problem/constraint:** User A must not read or mutate User B’s private items; client claims cannot be trusted.
- **Mechanism:** Authentication versus authorization, sessions/tokens as state, least privilege, input validation, privacy minimization.
- **Proposed change:** Add a local, course-owned identity fixture and explicit authorization checks in the service layer. Use a deliberately simple credential/session mechanism suitable for teaching; never store plaintext passwords in the canonical path.
- **Competency purpose:** Draw trust boundaries, trace identity to an authorization decision, and distinguish confidentiality from correctness.
- **Build:** Create two users, create private/shared items, and exercise allowed/denied operations.
- **Observe:** Record the decision inputs without logging secrets; inspect database ownership and request outcomes.
- **Break:** Change an item ID, omit identity, replay an expired fixture credential, and attempt cross-user access.
- **Explain/Judge:** Which component is trusted to authorize? What data should never enter logs or URLs?
- **Correctness/invariant:** Every private read/write is authorized for the effective user; denial does not reveal whether another user’s item exists; sharing is explicit and revocable.
- **Ignore/postpone:** OAuth providers, enterprise identity, password-reset email, WAFs, threat hunting, and internet exposure.
- **Complexity introduced:** Identity state, secret handling, authorization paths, and privacy obligations.
- **Complexity moved:** Cryptographic primitives and secure transport are delegated to vetted libraries and later infrastructure cases.
- **Simpler alternative:** Fixed local user IDs for an authorization-only experiment.
- **When NOT to add this:** Do not add authentication before learners understand the data ownership invariant, and do not connect a real identity provider to a teaching app.
- **Beyond the Project:** File permissions, mobile app capabilities, database roles, and package signing all enforce authority at a boundary.

### P3 — Real network path and bounded failure

- **Macro areas:** `05`, `07`, `08`.
- **Before:** P2 is local or assumes a reliable call.
- **New problem/constraint:** A client and service communicate through a real network with delay, loss, disconnects, and independently failing processes.
- **Mechanism:** sockets, DNS/name resolution, TCP byte stream, HTTP semantics, timeouts, retries, idempotency, partial failure.
- **Proposed change:** Run client and service as separate local processes; use a real loopback/network path, explicit connect/read timeouts, bounded retry only for safe operations, and request IDs for diagnosis. Do not invent a new transport.
- **Competency purpose:** Trace application data through protocol layers; distinguish timeout from failure of the operation; design retry behavior.
- **Build:** Exercise GET/list and mutation calls over the network.
- **Observe:** Use packet/request traces, socket/process tools, and latency measurements.
- **Break:** Stop the server, delay responses, cut the connection after submission, and send duplicate requests.
- **Explain/Judge:** If the client times out after a write, did the write happen? Which operations are safe to retry?
- **Correctness/invariant:** Every mutation has a defined idempotency/retry policy; a timeout is not reported as “definitely not committed.”
- **Ignore/postpone:** Public DNS, global routing, QUIC implementation, CDN behavior, and multi-region deployment.
- **Complexity introduced:** Timeouts, ambiguity, retries, and operational test control.
- **Complexity moved:** TCP and HTTP libraries provide transport machinery but not application correctness.
- **Simpler alternative:** Unix-domain sockets or a local pipe for process-boundary teaching.
- **When NOT to add this:** Do not test against an uncontrolled public service or treat a loopback result as internet performance.
- **Beyond the Project:** Database clients, remote build executors, and message consumers all face acknowledgment ambiguity.

### P4 — Query shape, indexes, and measurement

- **Macro areas:** `02`, `06`, `09`, `14`.
- **Before:** P3 stores a small set and scans it without evidence.
- **New problem/constraint:** Listing/filtering becomes slow as data grows; adding an index consumes space and changes write work.
- **Mechanism:** data structures, B-tree-like indexing, query plans, locality, cost estimates, benchmark discipline.
- **Proposed change:** Add a realistic fixture generator, one measured query, and an index only after a baseline. Compare plan, latency distribution, database size, and write cost.
- **Competency purpose:** Form a performance hypothesis, measure fairly, read a query plan, and judge an optimization by workload rather than fashion.
- **Build:** Add/query items with and without an index.
- **Observe:** Inspect `EXPLAIN`/plan output, page/cache behavior where available, and repeated timings.
- **Break:** Use a skewed dataset, cold versus warm runs, and a query that cannot use the index.
- **Explain/Judge:** What metric improved, for which data scale, and what did the index cost?
- **Correctness/invariant:** Results are identical before and after indexing; benchmark data, query, environment, warmup, repetitions, and distribution are recorded.
- **Ignore/postpone:** Distributed query planners, sharding, production SLOs, and premature cache layers.
- **Complexity introduced:** Fixture control, measurement noise, index maintenance, and plan interpretation.
- **Complexity moved:** The database planner and storage engine choose access paths.
- **Simpler alternative:** Improve an algorithm or query shape before adding an index.
- **When NOT to add this:** Do not add an index without a measured query and a stated workload.
- **Beyond the Project:** Compiler optimization, filesystem caches, build caches, and algorithmic data structures express the same space/time trade-off.

### P5 — Concurrent requests and transactional correctness

- **Macro areas:** `09`, `10`.
- **Before:** P4 assumes one request at a time.
- **New problem/constraint:** Two users update/share/delete simultaneously; a read-modify-write sequence can lose an update or violate ownership.
- **Mechanism:** interleavings, atomicity, locks, transactions, isolation, idempotency, deadlock/retry.
- **Proposed change:** Run concurrent clients against one database; define transactions around multi-step mutations; add a controlled race harness and explicit conflict behavior.
- **Competency purpose:** Enumerate interleavings, state a transaction invariant, reproduce a race, and distinguish application locks from database guarantees.
- **Build:** Concurrently edit/share the same item and inspect outcomes.
- **Observe:** Log request IDs, transaction boundaries, waits, commits, rollbacks, and final state.
- **Break:** Force delays between read and write; create lock contention and retryable conflicts.
- **Explain/Judge:** Which outcomes are allowed? Where should serialization happen, and what throughput does it cost?
- **Correctness/invariant:** No unauthorized mutation commits; each committed state satisfies schema and ownership invariants; a failed transaction leaves no partial mutation.
- **Ignore/postpone:** Distributed locks, global ordering, actor frameworks, and serializable-by-default claims across databases.
- **Complexity introduced:** Scheduling nondeterminism, locking, retries, and test flakiness.
- **Complexity moved:** SQLite/database transaction machinery handles local atomicity and recovery.
- **Simpler alternative:** Deterministic two-thread counter lab before app integration.
- **When NOT to add this:** Do not add threads merely to increase throughput if there is no observable correctness question.
- **Beyond the Project:** File updates, GUI event handlers, inventory systems, and build graphs have the same race/atomicity problem.

### P6 — Durable recovery and operational evidence

- **Macro areas:** `06`, `09`, `12`, `14`.
- **Before:** P5 has transactions but no stated recovery/backup story.
- **New problem/constraint:** Crashes, full disks, corrupt/missing database files, and bad migrations threaten durable user data.
- **Mechanism:** write-ahead/recovery concepts, backups, restore tests, schema migration, resource exhaustion, runbooks.
- **Proposed change:** Add versioned migrations, a documented backup/restore exercise, disk/resource limits in a local sandbox, and a recovery checklist. Preserve SQLite unless a concrete teaching constraint requires a server database.
- **Competency purpose:** Locate durable state, test a recovery claim, distinguish backup from replication, and reason about RPO/RTO.
- **Build:** Apply a migration, create a backup, restore into a clean instance.
- **Observe:** Inspect files, migration history, disk usage, and recovery logs.
- **Break:** Interrupt migration, restore an old backup, fill a bounded filesystem, and start with a missing/corrupt file.
- **Explain/Judge:** What data can be lost, how would we know, and who owns recovery complexity?
- **Correctness/invariant:** A completed migration has a known schema version; restore produces a readable database with declared loss bounds; failed migration does not silently claim success.
- **Ignore/postpone:** Managed backups, multi-region disaster recovery, object-store semantics, and compliance certification.
- **Complexity introduced:** Operations, version compatibility, runbooks, and recovery testing.
- **Complexity moved:** SQLite handles local journaling; operators still own backup correctness and restore evidence.
- **Simpler alternative:** Copy/restore a static fixture to teach state location before migrations.
- **When NOT to add this:** Do not add a migration framework before schema evolution is an actual problem.
- **Beyond the Project:** Package-lock updates, VM snapshots, notebook checkpoints, and build artifacts all require versioned recovery thinking.

### P7 — Deployment boundary and reproducible environment

- **Macro areas:** `04`, `05`, `12`.
- **Before:** P6 runs from a manually configured host.
- **New problem/constraint:** “Works on my machine” makes a process, dependency, and configuration claim hard to reproduce.
- **Mechanism:** executable artifacts, namespaces/isolation, environment configuration, build provenance, resource limits.
- **Proposed change:** Provide one canonical Linux run path and one optional container image for comparison. Inspect the process and filesystem; do not split the app into services.
- **Competency purpose:** Explain image versus running process, identify configuration/state boundaries, and distinguish reproducibility from security isolation.
- **Build:** Build/run the same app from a pinned environment.
- **Observe:** Compare processes, mounts, ports, environment, image layers, and startup logs.
- **Break:** Remove a dependency, use missing configuration, cap memory/CPU, and delete the container while preserving or losing external state deliberately.
- **Explain/Judge:** What does the container buy in this course, and what does it not guarantee?
- **Ignore/postpone:** Kubernetes, service mesh, orchestration, cloud IAM, autoscaling, and image supply-chain policy beyond a bounded introduction.
- **Complexity introduced:** Image builds, configuration, platform prerequisites, and state-volume confusion.
- **Complexity moved:** Container runtime owns namespaces/cgroups and image assembly; host/kernel remain part of the model.
- **Simpler alternative:** A reproducible shell script or virtual environment.
- **When NOT to add this:** Do not require Docker when it hides the OS process model or harms canonical Linux reproducibility.
- **Beyond the Project:** Hermetic builds, package managers, virtual machines, and mobile app sandboxes make similar artifact/isolation trade-offs.

### P8 — Instrumentation before scaling

- **Macro areas:** `05`, `07`, `10`, `12`, `14`.
- **Before:** P7 can run reproducibly but failures and latency are inferred from guesswork.
- **New problem/constraint:** A request is slow or wrong, and aggregate uptime cannot explain why.
- **Mechanism:** logs, metrics, traces, correlation IDs, cardinality, sampling, causal evidence, privacy-aware telemetry.
- **Proposed change:** Add structured logs and basic request/database duration metrics; optionally add OpenTelemetry-compatible traces as a bounded comparison, not a mandatory backend stack.
- **Competency purpose:** Observe hidden behavior, distinguish symptom from cause, correlate one request across layers, and state measurement limits.
- **Build:** Instrument one request path and one failure path.
- **Observe:** Compare logs, metrics, and trace spans; inspect overhead and sensitive-field handling.
- **Break:** Inject latency/error, lose telemetry, create high-cardinality labels, and sample away the interesting request.
- **Explain/Judge:** Which signal answers which question? What evidence is missing?
- **Correctness/invariant:** Telemetry must not change user-visible correctness; secret/private content is excluded or redacted; every sampled request retains a correlation path.
- **Ignore/postpone:** Vendor dashboards, full SRE platform, anomaly AI, and “observability” without a question.
- **Complexity introduced:** Instrumentation code, data volume, overhead, retention, and privacy risk.
- **Complexity moved:** Collectors/backends process telemetry; operators still choose useful signals and controls.
- **Simpler alternative:** Structured local logs plus timing around known boundaries.
- **When NOT to add this:** Do not add a tracing backend before learners can formulate a failure/performance question.
- **Beyond the Project:** Compiler profiling, OS tracing, database query plans, and batch job counters are observability for non-web systems.

### P9 — System Defense candidate state

- **Macro areas:** `11`, `12`, `13`, `14`, `15`.
- **Before:** P8 is one instrumented service with local durable state.
- **New problem/constraint:** The learner must defend a design under changed constraints without adding components by reflex.
- **Mechanism:** partial failure, consistency, queues/replicas as alternatives, threat boundaries, cost/resource economics, evidence-based judgment.
- **Proposed change:** No required production component. Give scenario cards: tenfold read load, intermittent storage, asynchronous export, stricter privacy, regional latency, or a restore deadline. Learner proposes the smallest justified evolution and tests a representative claim.
- **Competency purpose:** Integrate Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, and Learn-New-Tech.
- **Build:** Implement only the selected narrow change in a branch or design exercise.
- **Observe:** Produce an evidence packet: architecture/state diagram, measurements, failure trace, invariant list, cost/resource estimate, and rejected alternatives.
- **Break:** Defend behavior under timeout, duplicate submission, stale read, failed replica, lost telemetry, and compromised credential scenarios.
- **Explain/Judge:** Where is state? Where does time go? Where can it fail? How would we know? What are we paying for? When is the simpler design better?
- **Correctness/invariant:** The defense names assumptions and preserves user/data invariants under the chosen failure model.
- **Ignore/postpone:** No mandatory queue, cache, replica, PostgreSQL cluster, reverse proxy, service mesh, or cloud deployment.
- **Complexity introduced:** Scenario analysis and architectural judgment rather than baseline runtime complexity.
- **Complexity moved:** Any selected abstraction moves failure, operations, and cost; the learner must name that destination.
- **Simpler alternative:** Keep P8 and defend rejection of the proposed technology.
- **When NOT to add this:** Do not turn the final defense into a feature-build contest.
- **Beyond the Project:** Defend a build cache, local database, data pipeline, or messaging workflow under the same constraints.

## 5. Cross-cutting competency and concern matrix

| Milestones | Main competencies | Recurrent concerns |
|---|---|---|
| P0–P1 | Trace, Explain, Correctness | representation, interfaces, state, malformed input |
| P2–P3 | Trace, Explain, Judge, Correctness | trust, privacy, authorization, timeout ambiguity |
| P4 | Observe, Diagnose, Estimate, Judge | workload, cache/locality, measurement validity, cost |
| P5 | Diagnose, Correctness, Explain | interleavings, atomicity, isolation, retry |
| P6 | Observe, Correctness, Judge, Estimate | durability, recovery, resource exhaustion, data responsibility |
| P7 | Explain, Observe, Judge, Learn-New-Tech | process/artifact boundary, reproducibility, isolation, supply chain |
| P8 | Observe, Diagnose, Judge, Correctness | causal evidence, telemetry cost, redaction, missing signals |
| P9 | All eight | partial failure, alternatives, cost, security, evidence, rejection |

Every project checkpoint should require at least one invariant, one controlled failure, one measurement or observation, one security/privacy decision, and one simpler alternative.

## 6. Major-component justification cards

These are proposals for case branches, not admissions to the Core project.

### PostgreSQL — **Adapt / likely optional case, not baseline**

- **Problem/constraints:** A server database may be justified by concurrent clients, richer query workloads, operational separation, or a need to study MVCC and isolation beyond SQLite.
- **Mechanism/gains:** client/server database, indexes, query planner, MVCC, transactions, isolation, server-managed concurrency.
- **Costs/failures:** setup and version burden, connection/configuration complexity, new backup/authentication surface, misleading assumption that “bigger database” fixes a bad invariant or query.
- **Alternatives/when not:** SQLite is better for a small single-node durable service; do not add PostgreSQL for fashion, résumé value, or an unmeasured workload.
- **Scale threshold:** No universal number; add only when the pedagogical constraint is concurrent server-managed state or a measured workload exceeds the simple baseline. Record dataset, concurrency, latency, and durability requirements.
- **Evidence:** PostgreSQL 18 current documentation describes isolation levels, serialization failures/retry, MVCC behavior, and `EXPLAIN` plans; see Sources.
- **Evolution/stable principle:** SQLite single-process state → constraint from concurrency/operations → server database → stronger separation and tooling but more operational state. Stable principle: storage guarantees must match workload and invariant.

### Cache — **Do not add to canonical path; teach as a bounded branch**

- **Problem/constraints:** Repeated equivalent reads consume measurable latency/bandwidth; responses are safe to reuse with explicit freshness semantics.
- **Mechanism/gains:** local/shared copy, keying, eviction, freshness and invalidation; lower repeated-read cost.
- **Costs/failures:** stale data, invalidation, memory cost, cache stampede, privacy/key leaks, false performance conclusions.
- **Alternatives/when not:** query/index improvement, database/page cache, HTTP caching, or no cache. Do not add before measuring a repeated-read problem and defining correctness under staleness.
- **Scale threshold:** Only after a repeatable read workload and acceptable staleness bound are stated.
- **Evidence/evolution/stable principle:** RFC 9110 describes caches as stores of prior responses that shorten the request chain, with constraints on cacheability; stable principle: a copy requires a validity policy.

### Queue — **Reject as a required project component; scenario-only**

- **Problem/constraints:** Work can be delayed, retried, smoothed, or decoupled from a user request.
- **Mechanism/gains:** durable/asynchronous handoff, buffering, consumer concurrency.
- **Costs/failures:** duplicate delivery, ordering ambiguity, poison messages, visibility/ack semantics, another durable state and operator.
- **Alternatives/when not:** synchronous call, local batch, database outbox only when a concrete atomic handoff problem exists. Do not add for one small export.
- **Scale threshold:** A queue becomes educationally justified when bounded request latency conflicts with work duration or producer/consumer rates measurably differ.
- **Evidence/evolution/stable principle:** Teach from a local durable job table before any broker; stable principle: asynchronous work trades immediate certainty for buffering and delivery semantics.

### Container — **Optional P7 comparison**

- **Problem/constraints:** Reproduce dependencies and isolate process/filesystem assumptions.
- **Mechanism/gains:** isolated processes sharing a host kernel, image/artifact packaging, resource controls.
- **Costs/failures:** host-kernel dependence, image size/provenance, volume/state confusion, extra setup, false security confidence.
- **Alternatives/when not:** virtual environment, shell script, VM, or native Linux process. Do not require it when it obscures process/syscall teaching.
- **Scale threshold:** Educational threshold is environment mismatch, not user traffic.
- **Evidence:** Docker’s current documentation defines containers as isolated processes and distinguishes them from VMs; see Sources.
- **Stable principle:** Reproducible artifacts do not eliminate dependencies on the underlying system.

### Reverse proxy / TLS termination — **Optional infrastructure/security case, not baseline**

- **Problem/constraints:** One public entry point may route to an origin, centralize policy, or terminate TLS; certificate identity and hop boundaries matter.
- **Mechanism/gains:** intermediary/gateway, connection termination, routing, policy boundary, TLS authentication/confidentiality.
- **Costs/failures:** new trust boundary, forwarded-header mistakes, double termination, origin exposure, certificate/renewal operations, confusing client-to-proxy with end-to-end security.
- **Alternatives/when not:** direct localhost service or direct TLS in the app for a bounded case. Do not add a proxy just to imitate production.
- **Scale threshold:** Public multi-process routing or a clearly stated certificate/policy boundary.
- **Evidence:** RFC 9110 defines gateways/reverse proxies and HTTP origins; HTTPS authority depends on certificate verification and trust anchors; see Sources.
- **Stable principle:** Intermediaries alter where protocol, authority, and failure are located.

### Observability tooling — **Adapt, minimal signals first**

- **Problem/constraints:** Need to ask why behavior occurred across boundaries.
- **Mechanism/gains:** correlated logs, metrics, spans and traces; improved diagnosis of novel failures.
- **Costs/failures:** overhead, cardinality, storage/retention, privacy leakage, missing/sampled evidence.
- **Alternatives/when not:** structured logs and explicit timers. Do not add a vendor backend before defining a diagnostic question.
- **Scale threshold:** The first threshold is a cross-boundary failure that local logs cannot explain, not a request count.
- **Evidence:** OpenTelemetry’s current primer defines observability, telemetry signals, spans, traces, reliability, and privacy-relevant attributes; see Sources.
- **Stable principle:** Instrumentation is an evidence design problem, not a dashboard purchase.

### Replicas / distributed components / deployment automation — **Do not add to the Core baseline**

- **Problem/constraints:** Availability, read locality, rollout safety, or independent scaling may justify multiple copies/components.
- **Mechanism/gains:** replication, failover, independent deployment, partial-failure isolation.
- **Costs/failures:** consistency lag, split brain, coordination, rollout/rollback complexity, credentials, cost, and much larger debugging surface.
- **Alternatives/when not:** one process, one database, tested backups, and a restart/runbook. Do not add without a failure model, workload, SLO/RPO/RTO, and evidence that simpler operations are insufficient.
- **Scale threshold:** Constraint-driven only; no generic traffic threshold admits them.
- **Stable principle:** Distributed state creates coordination and partial-failure obligations.

## 7. Final System Defense preparation

The final defense should require a baseline diagram and a changed-constraint response. The learner must submit:

1. request/data/control trace from client to durable state;
2. state inventory: transient, process, database, backup, telemetry, and credential state;
3. invariant and failure matrix;
4. observations and measurements with environment, workload, warmup/repetitions, and limits;
5. security/privacy boundaries and data-retention decisions;
6. latency/resource/cost estimates;
7. selected evolution or reason for rejection;
8. recovery and operational evidence;
9. three plausible alternatives and what complexity each moves;
10. explicit unknowns and a plan to learn them from authoritative sources.

A passing defense does not require adding infrastructure. It requires a defensible relationship between requirements, mechanisms, evidence, guarantees, failures, and cost.

## 8. Reconciliation points

- **Issue #1:** Map each `P` milestone to final learner-visible stages only after the Core architecture and dependency graph settle. Preserve P IDs; do not rename them to stage numbers.
- **Issue #2:** Incorporate external coverage gaps only if they improve a mechanism or competency; do not expand the app’s business domain to satisfy symmetry.
- **Issue #4:** Select proven experiments independently. Project opportunities here are invitations for lab research, not final lab choices.
- **Research dossiers:** Re-check versions, security practices, database behavior, container details, and current observability guidance before lessons are drafted.
- **Technology admission:** Any promotion of PostgreSQL, queues, replicas, or deployment automation requires an explicit constraint/evidence record and Lead review.

## 9. Unresolved architecture questions

1. Is the canonical baseline CLI-only until `08`, or should a minimal HTTP adapter exist earlier as a stable interface case?
2. Which Python/SQLite versions and Linux environment are canonical for the first runnable slice?
3. What is the smallest safe identity fixture for P2, and where is its primary security explanation owned?
4. Should P7 container work be required, optional, or a Source Expedition after native Linux process teaching?
5. Which P4/P5 measurements belong in the Core project versus Issue #4’s classic lab inventory?
6. What exact System Defense rubric and evidence format will Issue #1/assessment architecture define?
7. What privacy policy governs fixture data, logs, traces, backups, and learner-submitted defenses?

## 10. Evidence and provenance

**Repository sources:** `meta/CURRICULUM_MAP.md`, `meta/COMPETENCY_MATRIX.md`, `meta/TECHNOLOGY_EVALUATION_FRAMEWORK.md`, `meta/RESEARCH_AND_SOURCE_POLICY.md`, `meta/LAB_DESIGN_POLICY.md`, and `meta/DECISIONS.md` (accessed 2026-08-30).

**Authoritative technical sources checked 2026-08-30:**

- IETF, [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html): HTTP stateless semantics, intermediaries, caches, origins, HTTPS identity.
- IETF, [RFC 9293 — Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293.html): byte streams, sequencing, retransmission, timeout/failure, connection state.
- PostgreSQL, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) and [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html): current PostgreSQL 18 behavior and measurement caveats.
- Docker, [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container.md): current container/process and VM distinction.
- OpenTelemetry, [Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/): telemetry signals, reliability, traces and spans; page reports last modification 2026-04-23.
- MIT 6.1810, [Fall 2025 overview](https://pdos.csail.mit.edu/6.1810/2025/overview.html): teaching-OS scope and xv6 size/complexity rationale.

Claims about scale thresholds are intentionally qualitative: no universal traffic number is asserted. Product versions and current practices must be rechecked during Lead review.
