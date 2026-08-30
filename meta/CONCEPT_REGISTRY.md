# Concept Registry

Status: **Blueprint v0.1 — initial canonical population, Lead-accepted** (Issue #9 integration; concept boundaries remain revisable through formal review)

The Concept Registry is stricter than a glossary. It prevents canonical definitions from drifting across modules. **Teach once, revisit many times.**
A concept's core definition/mechanism has one primary teaching home. Other lessons/labs/projects include a short recap and context-specific application, but never a second full canonical explanation.

## Entry schema

Each canonical entry records:

- `id`
- canonical Chinese name
- canonical English name (with qualifiers where the same English word is overloaded)
- canonical definition
- canonical first home
- revisits
- related concepts
- common confusions
- Big Ideas relation

## Initial Big Ideas (unchanged — 15)

State; Abstraction; Representation; Indirection; Caching; Concurrency; Isolation; Consistency; Failure; Interface; Locality; Trade-off; Correctness; Invariant; Specification.

`Process`, `Durability`, and `Trust Boundary` are **concepts, not Big Ideas** — the initial population admits them below without promoting them. Big Idea changes require separate architecture review and were **not** made by Issue #9.

## Initial canonical population (18)

### EC-CON-001 状态 — State

- **Definition:** Information that can affect future behavior or observations. Not every piece of data is state; storage is only one possible state location.
- **First home:** M00, `L00-01`.
- **Revisits:** M02, M06, M08, M13, M14, M15, M17, M20, M23, M24; P0–P9 state inventory.
- **Related:** Representation, Interface, Failure, Consistency.
- **Common confusions:** variable vs system state; state vs storage; state vs configuration.
- **Big Ideas:** State.

### EC-CON-002 抽象 — Abstraction

- **Definition:** A model or boundary that omits detail while preserving the behavior relevant to a stated purpose. It does not guarantee that omitted mechanisms are irrelevant.
- **First home:** M00, `L00-01`.
- **Revisits:** M02, M05, M12, M16, M19, M23.
- **Related:** Interface, Indirection, Specification.
- **Common confusions:** simplification vs guaranteed behavior; abstraction vs implementation.
- **Big Ideas:** Abstraction.

### EC-CON-003 表示 — Representation (qualifiers: in-memory, on-wire, on-disk)

- **Definition:** A concrete encoding or structure used to carry information. The same information can have multiple representations with different costs and validity rules.
- **First home:** M01, `L01-01`.
- **Revisits:** M03, M05, M08, M11, M13, M16; P0–P1.
- **Related:** State, Interface, Specification, Correctness.
- **Common confusions:** information vs representation; serialization vs schema; encoding vs encryption.
- **Big Ideas:** Representation.

### EC-CON-004 间接 — Indirection (qualifiers: address, name, service, intermediary)

- **Definition:** Reaching a resource through a reference, name, mapping, or intermediary so location or implementation can change without changing every caller. Indirection introduces lookup and failure points.
- **First home:** M00, `L00-01`.
- **Revisits:** M05, M07, M11, M16, M19, M23.
- **Related:** Abstraction, Interface, State.
- **Common confusions:** indirection vs abstraction; pointer/reference vs ownership; proxy vs authority.
- **Big Ideas:** Indirection.

### EC-CON-005 接口 — Interface (qualifiers: API, ABI, syscall, file, HTTP, SQL, RPC)

- **Definition:** The externally visible contract for interaction: accepted forms, meaning, guarantees, errors, boundaries. An interface is not its implementation or product wrapper.
- **First home:** M00, `L00-01`.
- **Revisits:** M02, M03, M06, M08, M11, M13, M16, M19, M24.
- **Related:** Specification, Representation, Indirection.
- **Common confusions:** API vs implementation; protocol vs interface; user interface vs system interface.
- **Big Ideas:** Interface.

### EC-CON-006 权衡 — Trade-off (qualifiers: performance, reliability, security, privacy, cost)

- **Definition:** A constrained choice where gaining one property changes cost, risk, complexity, or another property. A trade-off requires a stated constraint; it is not a synonym for compromise or preference.
- **First home:** M02, `L02-02`.
- **Revisits:** M04, M09, M11, M13, M14, M17, M18, M19, M23, M24.
- **Related:** State, Specification, Correctness.
- **Common confusions:** "pros and cons" without a constraint; trade-off vs arbitrary compromise.
- **Big Ideas:** Trade-off.

### EC-CON-007 规格 — Specification

- **Definition:** A testable statement of permitted behavior, required behavior, or guarantees under stated assumptions. It is not an implementation, an example, or an unbounded goal.
- **First home:** M02, `L02-03`.
- **Revisits:** M05, M11, M14, M15, M16, M21, M22, M24.
- **Related:** Interface, Invariant, Correctness.
- **Common confusions:** specification vs test case; desired feature vs guarantee; implementation detail vs contract.
- **Big Ideas:** Specification.

### EC-CON-008 不变量 — Invariant

- **Definition:** A property that remains true across all permitted state transitions under a specified model. It may be temporarily absent during an internal operation if the specification does not expose that intermediate state.
- **First home:** M02, `L02-03` (M01 round-trip usage is an application, not a second definition).
- **Revisits:** M01, M05, M07, M08, M13, M14, M15, M16, M17, M21, M22, M24; P0–P9.
- **Related:** Specification, Correctness, Consistency.
- **Common confusions:** invariant vs precondition; invariant vs consistency; "usually true" heuristic vs property.
- **Big Ideas:** Invariant.

### EC-CON-009 正确性 — Correctness

- **Definition:** Conformance of observable behavior to its specification under stated inputs, concurrency, failure, and trust assumptions. Correctness is not merely speed, security, or success on a sample.
- **First home:** M02, `L02-03` (M01 supplies representation-correctness evidence only).
- **Revisits:** M05, M07, M08, M13, M14, M15, M16, M17, M18, M21, M22, M24.
- **Related:** Specification, Invariant, Consistency.
- **Common confusions:** correctness vs reliability; correctness vs performance; "it ran" vs conformance.
- **Big Ideas:** Correctness.

### EC-CON-010 故障 — Failure

- **Definition:** A loss, deviation, or uncertainty relative to a specified capability or assumption — crashes, wrong results, unavailability, partial completion. Not every exception or unexpected event is a system failure.
- **First home:** M03, `L03-03` (M00 is a preview only: "systems fail").
- **Revisits:** M06–M20, M22, M23, M24; P3, P5, P6, P8, P9.
- **Related:** Correctness, State, Isolation, Consistency.
- **Common confusions:** error vs bug vs failure; timeout vs known non-commit; incident vs root cause.
- **Big Ideas:** Failure.

### EC-CON-011 缓存 — Caching (qualifiers: hardware, page, HTTP, database, application)

- **Definition:** Retaining a prior result or copy for reuse under a validity/freshness policy. A cache is not automatically durable, authoritative, private, or correct under mutation.
- **First home:** M04, `L04-01` (hardware-cache context).
- **Revisits:** M08 page cache; M11 HTTP/cache/CDN; M13 buffer pool; M17 stale-replica discussion; M19 resource case; M23.
- **Related:** Locality, State, Consistency, Trade-off.
- **Common confusions:** cache vs buffer; cache vs replica; cache vs durable store; cache hit vs correctness.
- **Big Ideas:** Caching.

### EC-CON-012 局部性 — Locality (qualifiers: temporal, spatial, data, network)

- **Definition:** The tendency for related accesses or communication to occur near one another in time, space, or placement, allowing lower resource cost. Locality can be exploited by a cache but is not itself a cache.
- **First home:** M04, `L04-02`.
- **Revisits:** M08 disk/file access; M13 index/data layout; M17 replica placement; M23.
- **Related:** Caching, Representation, Trade-off.
- **Common confusions:** locality vs proximity alone; locality vs caching mechanism.
- **Big Ideas:** Locality.

### EC-CON-013 隔离 — Isolation (qualifiers: memory, process, browser, transaction, container)

- **Definition:** Limiting interference or visibility between executions, identities, resources, or fault domains. Isolation can support security or correctness but does not alone establish either.
- **First home:** M07, `L07-01` (M06 process boundary is a preview only).
- **Revisits:** M12 browser/site boundary; M14 transaction isolation; M15 synchronization scope; M16–M17 fault domains; M19 containers; M21–M22 trust/authority.
- **Related:** Trust Boundary, Concurrency, Consistency, State.
- **Common confusions:** isolation vs encryption; process vs VM; transaction isolation vs distributed consistency.
- **Big Ideas:** Isolation.

### EC-CON-014 一致性 — Consistency (qualifiers: transaction, replicated system)

- **Definition:** The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee. It must be qualified; "consistent" does not mean merely fresh, durable, or correct in every sense.
- **First home:** M14, `L14-02` (M12/M14 may preview related problems but do not define it).
- **Revisits:** M17 replication/linearizability/eventual; M18 delivery/ordering; M23, M24.
- **Related:** Correctness, Invariant, Isolation, Durability.
- **Common confusions:** ACID "consistency" vs isolation/visibility guarantees; consistency vs correctness; consistency vs durability; consistency vs consensus; database isolation vs replicated consistency.
- **Big Ideas:** Consistency.

### EC-CON-015 并发 — Concurrency (qualifiers: threads, processes, event loops, distributed operations)

- **Definition:** Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations.
- **First home:** M15, `L15-01` (M12 event loop and M14 transaction overlap are previews only).
- **Revisits:** M16–M18, M20, M23, M24.
- **Related:** State, Isolation, Correctness, Failure.
- **Common confusions:** concurrency vs parallelism; async I/O vs no concurrency; distributed execution vs one thread.
- **Big Ideas:** Concurrency.

### EC-CON-016 持久性 — Durability (qualifiers: filesystem, database, object storage)

- **Definition:** A committed state survives a named restart or failure bound. Durability is a claim about a failure model, not a synonym for backup, replication, availability, or "written to a file".
- **First home:** M09, `L09-01`.
- **Revisits:** M14 WAL/commit; M17 replication; M18 durable handoff; M24; P0/P6.
- **Related:** State, Failure, Consistency, Trade-off.
- **Common confusions:** durability vs persistence as mere storage; backup vs replication; commit vs survive power loss.
- **Big Ideas:** State, Failure, Consistency, Trade-off.

### EC-CON-017 信任边界 — Trust Boundary (qualifiers: process, browser, service, user, data)

- **Definition:** A boundary where authority, trust assumptions, or enforcement responsibility changes; inputs crossing it need explicit validation/authorization and outputs need bounded exposure.
- **First home:** M07, `L07-01`. Virtual-memory/process isolation provides the first concrete protection boundary: introduce the trust-boundary definition here while explicitly distinguishing an isolation boundary from a trust boundary (they often coincide, but neither implies the other).
- **Revisits:** M11 TLS/certificate trust; M12 origin/site isolation; M19 deployment/supply-chain boundaries; M21 threat-model/crypto synthesis; M22 composition/authz; M23 technology judgment; M24; P2/P8/P9.
- **Related:** Interface, Isolation, Specification, Failure.
- **Common confusions:** trust boundary vs network boundary; authentication alone; encryption alone; "internal" means trusted.
- **Big Ideas:** Interface, Isolation, Specification, Failure.

### EC-CON-018 进程 — Process (qualifier: OS execution context)

- **Definition:** A managed execution context with identity, resources, and normally an address-space boundary through which a program runs. It is not source code, a thread, a container image, or a virtual machine.
- **First home:** M06, `L06-01`.
- **Revisits:** M07 address spaces; M12 browser processes; M16 remote process failure; M19 containers; M24.
- **Related:** State, Isolation, Concurrency, Interface.
- **Common confusions:** program vs process; process vs thread; container vs VM; process state vs durable state.
- **Big Ideas:** State, Isolation, Concurrency, Interface.

## Deliberately deferred (explicit, not omissions)

| Item | Status | Reason |
|---|---|---|
| `Consensus` (共识) | Concept is Core at M17 `L17-02` (R10) — **no Registry ID yet** | #15 §8.5 deferral preserved: concept/implementation boundary and revisit semantics were resolved (#9), but a stable ID is postponed until a full boundary review so the ID cannot harden an architecture decision. |
| Schema evolution / reader-writer compatibility / provenance / derived data | **Application pattern only** — M13 `L13-03` homes under State / Representation / Interface / Invariant (R6) | Existing canonical concepts are sufficient; no new ID, no new Big Idea, no PROV ontology. |
| Queue, Replication, Transaction, RPC, Container, Observability | Not in first population | Important Module-level mechanisms; their ID boundaries depend on dossier/lab work, and premature IDs would harden architecture decisions. |
| AI / model / evaluation concepts | Not in first population | OQ-BP-001 (bounded AI literacy) — RFC-gated; safe interim pattern is verification-of-AI-generated-claims (Current Case). |
| HCI / accessibility / consent / user mental model | Not in first population | OQ-BP-003 (human-facing boundary) — RFC-gated. |
| Applied probability / statistics / uncertainty concepts | Not in first population (R1) | Treated as the measurement-uncertainty toolkit under Estimate/Diagnose; M04 `L04-02` owns the first assessed home; no ID. |
| Product names, commands, frameworks, vendor services | Never concept IDs | Invariant 4 + Registry policy: principle before product; products are replaceable Current Cases. |

## Canonical explanation rule (enforcement note)

A later lesson may: recap in one sentence, apply to a new context, name a failure mode, or reopen a trade-off. It must **not** re-state the full definition above. The Lesson map (`core-stage-module-lesson-map-v0.1.md` §8) records every scheduled revisit per concept; a new revisit that would require a duplicate definition is a conflict to raise, not a silent second teaching.

## Related policies

- First-home and revisit table: `meta/blueprint/core-stage-module-lesson-map-v0.1.md` §8.
- Big Idea changes: require architecture review (none made by Issue #9).
- Environment/tool names and versions: never Registry entries; see OQ-BP-006.
