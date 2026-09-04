# Data & Concurrency (M13–M15) Research Dossier v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #83 — [Research] M13–M15 Data & Concurrency Research Dossier v0.1
Repository state researched: `main @ 69195f9630f792c138318cc8eb8ed413682b5409`
Checked date for current specifications, sources, and tools: **2026-09-04**
Role: Research Agent — Database / Transaction / Concurrency Mechanism, Source, Provenance, and Implementation-Feasibility Researcher
Scope: Research step only; no learner Lessons, runnable Lab implementation, Mini Cloud App feature work, Blueprint redesign, Concept Registry edits, or Open Question closure.

---

## Evidence-Layer Legend

This dossier strictly adheres to the repository source policy (`meta/RESEARCH_AND_SOURCE_POLICY.md`):

- **PRINCIPLE** — stable mechanism, theory, or reasoning pattern independent of a specific product or version.
- **SPECIFICATION** — normative or official contract from a formal standard, RFC, language specification, ABI, protocol, or platform interface definition.
- **IMPLEMENTATION** — actual tool, runtime, database engine, or kernel behavior within a named environment.
- **CURRENT PRACTICE** — replaceable present-day convention, deployed version baseline, provider behavior, or operational pattern subject to periodic change.

Confidence and context labels:

- **ESTABLISHED** — strongly supported by stable primary/authoritative evidence and consensus systems practice.
- **IMPLEMENTATION-SPECIFIC** — valid only for the named implementation, toolchain, version, or environment.
- **CURRENT-PRACTICE** — useful at the checked date (2026-09-04) but expected to require scheduled review.
- **CONTESTED** — credible sources, specifications, or implementations disagree under comparable assumptions.
- **UNCERTAIN** — evidence is incomplete or the design choice requires empirical implementation testing.

---

## 1. Executive Recommendation / Readiness

**Recommendation: READY FOR DESIGN**

This Research Dossier establishes the technical, pedagogical, tooling, environment, Required-Lab, Optional-Lab, Source-Expedition, provenance, currentness, and claim-boundary evidence required to design the complete Stage 5 (S5) Data & Concurrency slice without guessing:

$$\text{M13 (Databases: Storage \& Indexing)} \longrightarrow \text{M14 (Databases: Transactions, Recovery \& Isolation)}$$

along with the partially independent concurrency branch:

$$\text{M15 (Concurrency: Threads, Races \& Synchronization)}$$

### Key Findings and Invariant Alignment

1. **Architecture and Registry Integrity Preserved:**
   - **Zero new canonical concept IDs introduced:** The 18 canonical concepts in `meta/CONCEPT_REGISTRY.md` remain strictly authoritative.
   - **Canonical First Homes Honored:**
     - **EC-CON-014 Consistency (一致性)** enters its canonical first home in **M14 (`L14-02`)**. Canonical definition: *"The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee."* It must be qualified; "consistent" does not mean merely fresh, durable, or correct in every sense. ACID "Consistency" is explicitly dissected as application-invariant preservation rather than an engine-level ordering/visibility guarantee.
     - **EC-CON-015 Concurrency (并发)** enters its canonical first home in **M15 (`L15-01`)**. Canonical definition: *"Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations."* M12's event loop and M14's transaction overlap were previews only.
   - **Schema Evolution & Provenance as Application Pattern:** In accordance with R6 and Blueprint reconciliation, schema evolution, reader/writer compatibility, migration/backfill trade-offs, source-of-truth vs. derived data, and lightweight provenance are treated as an **application pattern** spanning existing concepts (`EC-CON-001 State`, `EC-CON-003 Representation`, `EC-CON-005 Interface`, `EC-CON-008 Invariant`). No new concept ID is created.
2. **LAB-REQ-04 Re-Audit (SQLite Query Plans, Indexing & Workload Evidence):**
   - Feasible as a self-contained **local-file** activity using the Blueprint-required `sqlite3` CLI plus Essential CS-owned Python support/test fixtures. Determinism applies to generated data and semantic checks, not to planner choice, timing, cache state, or exact EQP text.
   - Investigates SQLite EQP's semantic **`SCAN` vs `SEARCH`** categories and index use across bounded synthetic workloads. Exact detail strings, page counts, and planner choices remain version/data/statistics dependent.
   - Preserves result equivalence before and after indexing while exposing the trade-off of index maintenance on `INSERT`/`UPDATE` writes and storage space.
   - Truthful outcome respected: SQLite may choose `SCAN` even when an index exists. The lab records the actual plan and workload rather than treating a fixed selectivity threshold or literal sequential-disk-I/O story as a rule.
3. **LAB-REQ-05 Re-Audit (SQLite Transactions, Isolation, Rollback & Recovery Boundary):**
   - Feasible using two concurrent connections to a local SQLite database file without server daemon, root privileges, or external dependencies.
   - Demonstrates committed-only visibility under the declared SQLite configuration, a bounded second-writer/conflict disposition, and atomicity via `ROLLBACK`; actual result codes/messages are recorded rather than fixed.
   - Explores recovery after abrupt termination of an **owned child** on canonical Linux, recording the declared journal mode and actual side-file/reopen behavior. This is process-crash evidence, not a universal rollback-journal/WAL narrative.
   - Critical claim boundary enforced: Child process interruption demonstrates recovery from *client process abnormal termination*; it does *not* prove physical durability against power loss or hardware storage failure.
4. **LAB-REQ-03 Re-Audit (POSIX Threads Race, Rendezvous & Progress Boundaries):**
   - Feasible as an Essential CS original C11 + POSIX threads activity (`gcc -std=c11 -pthread`).
   - **Critical UB-free broken path:** The intentional lost-update scenario avoids undefined behavior from unsynchronized conflicting scalar accesses. It uses defined atomic load/store operations to make the **compound** read→compute→write transition non-atomic. A `sched_yield()` or bounded delay may widen the observation window, but neither POSIX scheduling nor one host guarantees that a particular lost-update interleaving will occur. Design must use bounded repetition and/or a course-controlled phase handoff if deterministic evidence is required, and record the actual observed interleaving.
   - Mutex repair can protect the course compound transition. For the Required Lab, the condition-variable rendezvous uses the canonical `while (!predicate) pthread_cond_wait(...)` pattern so the predicate is re-evaluated after wakeup; this is the course design rule grounded in POSIX condition-wait semantics, not a claim that POSIX mandates one literal C syntax.
   - Safety boundary: Deliberate deadlock work runs only in an owned child under a configured watchdog with termination/reaping. The watchdog bounds the course process; its duration and the wider host/UI behavior are not guarantees.
5. **Optional Labs & Source Expedition Audited:**
   - **LAB-OPT-03 (PostgreSQL EXPLAIN & Isolation Comparison):** Remains strictly **Optional**. It can compare `EXPLAIN (ANALYZE, BUFFERS)` and one documented PostgreSQL isolation/update-conflict behavior. PostgreSQL is not a required Core dependency, and current PostgreSQL labels/semantics must be used rather than a blanket “Snapshot Isolation” description.
   - **LAB-OPT-05 (OSTEP Semaphore Rendezvous):** Remains strictly **Optional and link-only** (commit `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`). Due to upstream repository licensing ambiguity (no formal OSS license declared in `ostep-homework`), Essential CS supplies zero copied skeleton code, instructions, or test suites.
   - **EXP-02 (PostgreSQL Planner and Buffer Source Route):** All three canonical paths still exist on moving PostgreSQL `master`, but **Target 1 has pedagogical drift**: `src/backend/optimizer/plan/README` is largely historical subselect notes rather than the current high-level Path→Plan overview. `costsize.c` and `buffer/README` remain directly useful. Keep the canonical route for Research; Design must surface this source-route risk instead of pretending all three files prove the originally intended claims.
6. **Environment and OQ-BP-006 Dispositions:**
   - Canonical feasibility is **Linux + the actually recorded toolchain/filesystem capabilities**. WSL and Dev Containers can be useful hosted Linux environments, but parity is not assumed: compiler, filesystem locking, process-signal, sanitizer, and package behavior must be preflighted on the actual host.
   - OQ-BP-006 (environment and version pinning) remains **OPEN**. The Agent host observation was Python 3.13.1 with its bundled SQLite 3.45.3 and GCC 14.2; current upstream checks on 2026-09-04 separately identify SQLite 3.53.4, PostgreSQL 18.6, and Python 3.14.7 as current stable releases. Host observations and current upstream versions are evidence, not curriculum-wide pins.

---

## 2. Scope and Canonical Constraints

### 2.1 Scope Chain and Module Definitions

| Module | Canonical Name | Preliminary Lessons | Hard Prereqs | Soft/Preferred Prereqs | Canonical Concept First Home | Primary Competencies |
|---|---|---|---|---|---|---|
| **M13** | Databases: Storage & Indexing | L13-01: "Why is my query fast/slow?"<br>L13-02: "What is SQL doing?"<br>L13-03: "Why do my schema choices matter?" | M08, M09 | M04 | None (revisits State, Representation, Interface, Trade-off, Invariant, Correctness, Caching, Locality) | Observe, Trace, Explain, Estimate, Judge, Correctness |
| **M14** | Databases: Transactions, Recovery & Isolation | L14-01: "What is a transaction?"<br>L14-02: "Why does concurrent access corrupt data?"<br>L14-03: "How do I design an atomic write?" | M13, M09 | None | **EC-CON-014 Consistency (L14-02)** (revisits State, Trade-off, Specification, Invariant, Correctness, Isolation, Durability) | Correctness, Diagnose, Judge, Explain, Trace |
| **M15** | Concurrency: Threads, Races & Synchronization | L15-01: "Why is my threaded code wrong?"<br>L15-02: "How do I make it right?"<br>L15-03: "Thread or async?" | M06 | M14, M03, M12 | **EC-CON-015 Concurrency (L15-01)** (revisits State, Specification, Invariant, Correctness, Isolation) | Diagnose, Trace, Correctness, Explain, Judge |

### 2.2 Canonical Concept Registry Constraints

No new concept IDs are introduced in this Research task. The canonical 18 concepts from `meta/CONCEPT_REGISTRY.md` are respected:

- **EC-CON-014 一致性 — Consistency:**
  - **Canonical first home:** M14 `L14-02`.
  - **Authoritative definition:** *"The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee. It must be qualified; 'consistent' does not mean merely fresh, durable, or correct in every sense."*
  - **Disambiguation mandate:** Dissect the historic overloaded usage: ACID "Consistency" (application invariant preservation, $C \in \text{ACID}$) vs. database transaction isolation levels vs. replicated system consistency (linearizability, sequential, eventual). M17 owns replicated consistency; M14 must not steal M17's distributed synthesis.
- **EC-CON-015 并发 — Concurrency:**
  - **Canonical first home:** M15 `L15-01`.
  - **Authoritative definition:** *"Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations."*
  - **Disambiguation mandate:** Explicitly distinguish concurrency (logical composition and interleaved progress) from parallelism (simultaneous physical execution across multiple processing units). M12 (event loop) and M14 (interleaved transactions) were strictly previews.
- **Application Patterns (No New Concept IDs):**
  - Schema evolution, reader/writer compatibility, migration/backfill trade-offs, source-of-truth vs. derived data, and lightweight provenance are taught in M13 `L13-03` under existing concepts (`EC-CON-001 State`, `EC-CON-003 Representation`, `EC-CON-005 Interface`, `EC-CON-008 Invariant`). They do not receive separate Registry IDs.

### 2.3 Competency Progression Constraints

Only the 8 canonical competencies (`meta/COMPETENCY_MATRIX.md`) are used across S5:

- **M13 Primary Competency — Observe:**
  - Connect high-level SQL queries to observable execution plans (`EXPLAIN QUERY PLAN`);
  - Inspect table scans vs. B-tree index searches;
  - Measure execution latency and storage footprints across data scales;
  - Verify result-set equivalence between indexed and unindexed executions.
- **M14 Primary Competency — Correctness:**
  - Define and verify transaction invariants across multi-step state transitions;
  - Identify and classify concurrent execution anomalies (dirty read, non-repeatable read, lost update);
  - Reason about atomic recovery boundaries and rollback mechanisms;
  - Select the minimal isolation level that guarantees safety for a stated workload.
- **M15 Primary Competency — Diagnose:**
  - Trace and enumerate non-deterministic thread interleavings;
  - Reproduce and diagnose a lost update in concurrent execution;
  - Repair shared-state hazards using mutual exclusion and condition synchronization;
  - Evaluate synchronization overhead and deadlock vulnerabilities.

---

## 3. S5 DAG and M13/M14/M15 Partial-Order Implications

### 3.1 Prerequisite Analysis and Partial Ordering

The curriculum DAG defines clear, authoritative dependency edges for Stage 5:

```
                  +--------------------------------+
                  | M08 Filesystems & Storage I/O  |
                  +---------------+----------------+
                                  |
                                  v
+-----------------------+  +-------------------------------+
| M04 Hardware Cache &  |  | M09 Storage Engines, Log &    |
| Locality (Soft/Pref)  |  | Crash Durability              |
+-----------+-----------+  +---------------+---------------+
            |                              |
            +------------+    +------------+
                         |    |
                         v    v
                  +--------------------------------+
                  | M13 Databases: Storage &       |
                  | Indexing                       |
                  +---------------+----------------+
                                  |
                                  v
                  +--------------------------------+
                  | M14 Databases: Transactions,   |
                  | Recovery & Isolation           |
                  +---------------+----------------+
                                  : (Soft/Preferred)
                                  v
+-----------------------+  +-------------------------------+
| M06 OS Kernel &       |->| M15 Concurrency: Threads,     |
| Processes (Hard)      |  | Races & Synchronization       |
+-----------------------+  +-------------------------------+
            ^                              ^
            |                              |
    (Soft: M03 Debug, M12 Event Loop) -----+
```

### 3.2 Pedagogical Rationale and Structural Decoupling

1. **Decoupling of M14 and M15:**
   - M14 requires M13 and M09 (database storage, pages, files, and write-ahead logging).
   - M15 requires M06 (operating system processes, address spaces, and kernel scheduling).
   - **M14 $\leftrightarrow$ M15 is not a hard DAG edge.** While M14 provides an intuitive high-level preview of concurrent interference (interleaved database transactions), M15 examines bare-metal operating system threads, shared virtual memory, hardware atomics, and POSIX synchronization primitives.
   - A learner may study M15 immediately after M06, or follow the canonical curriculum order M13 $\to$ M14 $\to$ M15. The dossier ensures neither module makes hidden structural assumptions about the other.
2. **S4 (Networking & Web) Independence:**
   - Stage 4 (M10–M12) is **not** a hard prerequisite for Stage 5 (M13–M15).
   - Learners taking a data-centric or systems-centric learning path may proceed directly from S3 (M06–M09) to S5 without completing M10–M12.
   - Where M15 `L15-03` revisits asynchronous event loops, it uses general event-driven I/O principles; familiarity with M12 browser microtasks is treated as optional enrichment.
3. **M04 Locality & Measurement Bridge:**
   - M04 is a soft/preferred prerequisite for M13. M13 leverages M04's measurement discipline (benchmarking baselines, variance, warm vs. cold cache) to prevent naive performance claims when evaluating query execution times.

---

## 4. Cross-Module Mechanism Chain: Storage $\to$ Query/Index $\to$ Transaction/Isolation

The database sequence (M13 $\to$ M14) traces data management from physical disk blocks up to transactional guarantees:

```
+-----------------------------------------------------------------------------------------+
| M08 / M09 Foundations                                                                   |
| Files/storage layers + named synchronization/failure bounds -> Durability (M09)        |
+-------------------------------------------+---------------------------------------------+
                                            | Page/storage mechanisms and named durability assumptions
                                            v
+-----------------------------------------------------------------------------------------+
| M13: Databases: Storage & Indexing                                                      |
| Storage Engine: named engine page/row representation; generic page model only as concept |
| Index Structure: B-tree-family mechanism; exact node/page shape is implementation evidence |
| Access Paths: full scan vs. indexed search; asymptotic intuition + actual plan evidence   |
| Query Route: parse -> named engine planning/code generation -> execution                  |
| Cost/Planner: estimates and heuristics are named-engine implementation evidence           |
| Cache/Buffer: SQLite pager/page cache vs PostgreSQL shared buffers kept distinct           |
| Schema Evolution: Invariant preservation, compatibility, source of truth vs. derived    |
+-------------------------------------------+---------------------------------------------+
                                            | Atomic page modifications & concurrent access
                                            v
+-----------------------------------------------------------------------------------------+
| M14: Databases: Transactions, Recovery & Isolation                                      |
| Transaction Boundary: Multi-step atomic state transition (BEGIN ... COMMIT / ROLLBACK)  |
| Atomicity & Recovery: Undo logging (Rollback Journal) vs. Redo logging (WAL)            |
| Concurrency Control: Writer serialization, page/row locks, MVCC snapshots               |
| Anomalies: Dirty Read, Non-Repeatable Read, Lost Update, Phantom Read, Write Skew       |
| Isolation Levels: Read Uncommitted -> Read Committed -> Snapshot Isolation / Serial    |
| Consistency (EC-CON-014): Named visibility guarantees vs. application schema invariants|
+-----------------------------------------------------------------------------------------+
```

---

## 5. Parallel Concurrency Mechanism Chain: Process $\to$ Thread $\to$ Interleaving $\to$ Synchronization

The concurrency thread (M06 $\to$ M15) traces execution control from isolated operating system processes down to shared-memory thread coordination:

```
+-----------------------------------------------------------------------------------------+
| M06 / M07 Foundations                                                                   |
| OS Process (EC-CON-018): Separate virtual address spaces, isolated memory, page tables  |
+-------------------------------------------+---------------------------------------------+
                                            | Threads share address space
                                            v
+-----------------------------------------------------------------------------------------+
| M15: Concurrency: Threads, Races & Synchronization                                      |
| Thread Execution: Shared heap/globals, private execution contexts (registers & stacks)  |
| Interleaving (EC-CON-015): permitted ordering/interleaving; observed schedule is host evidence |
| Hazards: logical race conditions vs. C language data-race undefined behavior                |
| Required Lab path: C11-compatible atomic accesses around a deliberately non-atomic compound update |
| Mutual Exclusion: POSIX Mutex (pthread_mutex_t), critical sections, lock invariants     |
| Coordination: POSIX Condition Variables (pthread_cond_t), predicate while-loop wait     |
| Progress Failures: Deadlock (Coffman conditions), lock hierarchies, watchdogs           |
| Execution Models: OS threads vs. async/event-loop tasks; mechanism/cost depends on runtime |
| Runtime Realities: CPython GIL modes; PEP 703 foundation + PEP 779 supported free-threading |
+-----------------------------------------------------------------------------------------+
```

---

## 6. M13 Research — Databases: Storage & Indexing

### 6.1 Capability Transition
- **From:** File I/O where applications manage their own ad-hoc byte layouts, sequential files, and unstructured storage (M08/M09).
- **To:** Declarative relational database access where queries express *what* data is needed, while the storage engine and query optimizer determine *how* records are indexed, laid out on disk pages, cached in memory, and retrieved.

### 6.2 Minimum Mechanism Model
1. **Paged Storage and Row Layout:**
   - Database engines commonly organize persistent data into fixed-size pages, but page size and row/page layout are implementation/configuration facts. SQLite's default page size is currently 4,096 bytes and PostgreSQL commonly uses 8,192-byte blocks; neither value is a universal database law.
   - A slotted-page model is a useful generic teaching pattern for variable-length records. SQLite and PostgreSQL have their own documented on-disk/page formats; Design must not present one generic slot-array diagram as the literal physical layout of every engine.
2. **B-Tree / B+ Tree Family Indexing:**
   - Multi-way balanced search trees give logarithmic-height lookup intuition, but exact node shape, fanout, height, payload placement, and page-probe count depend on engine format, key width, page size, fill, cache state, and query.
   - SQLite uses B-trees for tables and indexes. A rowid table is stored in a table B-tree keyed by rowid; calling that a universal “clustered index” would import terminology with engine-specific meanings.
   - A covering index can satisfy the columns needed by a query without an additional table lookup in a particular chosen plan; `USING COVERING INDEX` is SQLite EQP implementation evidence, not SQL-standard vocabulary.
3. **Query Compilation / Planning / Execution Boundary:**
   - Stable teaching model: SQL text is parsed; an engine chooses an executable strategy; execution produces rows/effects.
   - **SQLite implementation:** current official architecture documents SQL → parser/AST → code generation/query planning → VDBE bytecode → virtual-machine execution. Do not label SQLite as a Volcano `open/next/close` engine.
   - **PostgreSQL implementation:** Query/Path/Plan/executor objects provide a different concrete route. Generic “logical plan → physical plan → iterator” diagrams must be labeled conceptual or tied to the named engine.
   - Planner estimates can use statistics and cost assumptions, but the exact model and inputs are implementation-specific.
4. **Access Path Selection:**
   - SQLite EQP `SCAN` means the engine will scan the relevant table/subquery/index access path rather than perform the named selective search. Do not infer literal sequential disk I/O from the token alone.
   - SQLite EQP `SEARCH ... USING INDEX` records use of an index for a subset lookup. Whether it wins depends on the query, statistics, data distribution, covering behavior, cache state, and engine version; there is no fixed selectivity threshold.
5. **Database Cache / Buffer Management vs. OS Page Cache:**
   - Some DBMSs, notably PostgreSQL, maintain an explicit shared buffer pool with pins/content locks and replacement policy while the OS may also cache file pages.
   - SQLite has a pager/page-cache subsystem but does not share PostgreSQL's server buffer-manager architecture. “Database buffer pool” is therefore a mechanism family, not one universal implementation. EXP-02 may use PostgreSQL pins/clock-sweep as named implementation evidence.
6. **Schema Evolution and Invariant Preservation (R6 Application Pattern):**
   - Schema invariants (`NOT NULL`, `CHECK`, `UNIQUE`, `FOREIGN KEY`, `PRIMARY KEY`).
   - Evolution patterns: Adding nullable/default fields vs. dropping/renaming fields. Backward and forward reader/writer compatibility.
   - Source-of-truth vs. derived data: Storing primary authoritative state versus maintaining derived materialized views or aggregate tables.
   - Lightweight provenance: Recording metadata regarding update origin, timestamp, and versioning.

### 6.3 Explicit Non-Goals
- Writing a B-tree or database storage engine from scratch in C/C++.
- Implementing a full cost-based query optimizer.
- In-depth survey of non-relational storage engines (LSM-trees, column stores, vector databases).
- Enterprise PostgreSQL/Oracle database administration or tuning.
- Data engineering, distributed lineage platforms, or W3C PROV-O semantic ontologies.

### 6.4 Hidden Prerequisites / Just-in-Time Support
- Basic understanding of tree data structures and algorithmic complexity ($O(\log N)$ vs. $O(N)$) from M02.
- Operating system file and disk block concepts from M08.
- Measurement discipline and variance awareness from M04.

### 6.5 Candidate Real Observation / Activity
- Execute `EXPLAIN QUERY PLAN` in SQLite on a synthetic table with 50,000 rows.
- Observe actual SQLite `SCAN` / `SEARCH` detail categories on the committed fixture; do not bind acceptance to the assumed phrase `SCAN TABLE`.
- Demonstrate query execution time before/after indexing for **explicit course fixture selectivities**, recording actual plan, cache/warmup state, repetitions, distribution, environment, and inference limits.
- Measure the actual write-time and file-size difference caused by maintaining the course index; do not pre-state a universal percentage overhead.

### 6.6 Required Learner Evidence
- Plan inspection: Identify whether SQLite chose `SCAN` or `SEARCH`.
- Workload judgment: Explain the actual measured plan/read/write/space trade-off. If the index did not accelerate the observed workload, preserve that result.
- Equivalence verification: Confirm that indexed and unindexed queries return identical result sets.
- Selectivity prediction: Predict why the query planner may reject an index when a query matches 80% of the table.

### 6.7 Authority Classification
- **PRINCIPLE:** Relational algebra, B-tree search complexity ($O(\log_B N)$), cost-based access path selection, index read/write trade-off.
- **SPECIFICATION:** ANSI/ISO SQL standard grammar and semantics.
- **IMPLEMENTATION:** SQLite 3 query planner heuristics, B-tree page layout, `EXPLAIN QUERY PLAN` output format.
- **CURRENT PRACTICE / IMPLEMENTATION:** SQLite 3.53.4 current release behavior, current default page-size setting, planner/automatic-index heuristics, VDBE/EQP and CLI presentation. Record exact engine/library/CLI versions because the Python module may embed a different SQLite version.

### 6.8 Authoritative Sources
- SQLite Official Query Planner Guide: <https://sqlite.org/queryplanner.html>
- SQLite `EXPLAIN QUERY PLAN` Documentation: <https://sqlite.org/eqp.html>
- SQLite CLI Shell Reference: <https://sqlite.org/cli.html>
- Codd, E. F. (1970). "A Relational Model of Data for Large Shared Data Banks." *Communications of the ACM*.
- Ramakrishnan & Gehrke. *Database Management Systems* (3rd ed.), Chapters 8–12.

### 6.9 Likely Misconceptions
- *"Adding an index always makes queries faster."* (False: plan and runtime depend on workload, statistics, covering behavior, cache state, write pattern, and engine. An index adds maintenance/storage work, but the magnitude and even measured wall-time effect are workload-specific.)
- *"`EXPLAIN` executes the query and measures actual run time."* (False: Standard `EXPLAIN` or `EXPLAIN QUERY PLAN` displays the optimizer's estimated plan without executing the query).
- *"Database buffer pool is the same thing as the OS page cache."* (False: The DB buffer pool is application-level allocated memory managed with domain-specific replacement policies; the OS page cache operates at the kernel VFS layer).
- *"The exact text of a query plan is stable across database versions."* (False: Planner heuristics and plan formatting evolve across minor engine versions).

### 6.10 Environment & Tool Constraints
- Tools: Standard Python stdlib `sqlite3` and/or `sqlite3` CLI.
- Storage: Requires a local writable directory for synthetic SQLite database files (`.db`).
- Cleanliness: Must clean up temporary database and journal files upon completion.

### 6.11 Implementation-Time Smoke Requirements
- Verify the fixture can produce at least one **documented, version-recorded** indexed-search case while also accepting truthful `SCAN` outcomes when the planner chooses them.
- Verify bounded fixture generation completes under a harness watchdog; do not make a fixed two-second wall-clock threshold a curriculum invariant.

---

## 7. M14 Research — Databases: Transactions, Recovery & Isolation

### 7.1 Capability Transition
- **From:** Single queries operating on stable tables without considering concurrent modifications or mid-operation system crashes.
- **To:** Transactional systems that provide named atomicity/isolation/recovery mechanisms under a specific engine/configuration, while the application and schema still own the business invariant they intend each transaction to preserve.

### 7.2 Minimum Mechanism Model
1. **Transaction Boundary & Invariant Preservation:**
   - A transaction supplies an atomicity/isolation boundary for a group of operations; it does **not by itself prove** an application invariant. The learner must state the invariant/constraints and show that the transaction's intended transition preserves them.
   - `ROLLBACK` removes the effects of the current uncommitted transaction according to the named engine semantics. It should not be described as restoring the entire database to one universal global $S_0$ when other committed activity may exist.
2. **Atomicity / Journal / WAL Boundaries:**
   - **General WAL principle:** recovery designs arrange log/data ordering so enough recovery information reaches the required durability boundary before data pages whose recovery depends on it. The exact record/page/flush protocol is engine-specific.
   - **SQLite rollback-journal mode:** original page content is journaled before in-place database changes; a hot rollback journal may be used by a later opener to restore an interrupted transaction under SQLite's documented rules.
   - **SQLite WAL mode:** changed database pages are appended as WAL frames; a commit is represented in the WAL and checkpointing later transfers eligible content back to the main database. Readers can coexist with a writer by using snapshots, but SQLite still uses locking/shared-memory coordination. Do not teach “WAL readers run without locking”.
3. **Isolation Anomalies (Berenson et al. / ANSI SQL-92):**
   - **Dirty Read ($P_1 / A_1$):** Transaction $T_1$ modifies data; Transaction $T_2$ reads uncommitted modification; $T_1$ rolls back.
   - **Non-Repeatable Read ($P_2 / A_2$):** $T_1$ reads data; $T_2$ modifies/commits data; $T_1$ re-reads and observes mutated values.
   - **Lost Update ($P_4$):** $T_1$ and $T_2$ both read $x$, compute new values, and write back; one overwrite obliterates the other's update.
   - **Phantom Read ($P_3 / A_3$):** $T_1$ reads a set of rows satisfying a predicate; $T_2$ inserts new rows satisfying the predicate and commits; $T_1$ re-executes and sees "phantom" rows.
   - **Write Skew ($A5B$):** $T_1$ reads $x$ and $y$, modifies $x$; $T_2$ reads $x$ and $y$, modifies $y$; each preserves local constraints, but combined state violates a cross-record invariant (manifests under Snapshot Isolation).
4. **Isolation Levels & Mechanisms:**
   - ANSI levels: Read Uncommitted $\to$ Read Committed $\to$ Repeatable Read $\to$ Serializable.
   - Mechanisms: Locking (Two-Phase Locking / 2PL) vs. Multi-Version Concurrency Control (MVCC).
   - In SQLite: Default configuration operates with serialized writers and committed-only visibility. In WAL mode, writers append to the log while readers query immutable snapshots.
5. **Recovery vs. Durability Boundaries:**
   - Distinguish distinct failure classes:
     1. Application `ROLLBACK`: Intentional programmatic cancellation.
     2. Learner-owned client process interruption: the process dies and OS-owned locks/resources are released. In rollback-journal mode a later open may perform hot-journal recovery; in WAL mode uncommitted frames are not a committed transaction. Record the actual journal mode and artifacts rather than asserting one identical recovery path.
     3. OS crash / kernel failure: volatile kernel/application state may be lost; guarantees depend on the named SQLite journal/synchronous settings plus filesystem/device semantics.
     4. Power loss / hardware failure: a stronger failure bound involving device/controller persistence and ordering behavior. The course process-kill experiment does not exercise this bound.

### 7.3 Explicit Non-Goals
- Implementing the ARIES recovery algorithm.
- Building a lock manager or Two-Phase Locking scheduler.
- Deep dive into Serializable Snapshot Isolation (SSI) mathematics.
- Distributed transaction coordination (Two-Phase Commit / 2PC, Raft, Paxos).
- Database backup administration, disaster recovery planning, or replication topologies.

### 7.4 Hidden Prerequisites / Just-in-Time Support
- Invariant definition and state transition concepts from M02.
- Crash durability and log concepts from M09.
- SQLite query execution basics from M13.

### 7.5 Candidate Real Observation / Activity
- Initialize an account balance table with invariant: `balance_a + balance_b == 1000`.
- Open two independent SQLite connections:
  - Connection 1 opens a transaction and updates `balance_a = 900`.
  - Connection 2 performs a `SELECT` and records the committed snapshot visible under the fixture's actual SQLite configuration. This is evidence for the documented committed-only visibility path; one run is not a universal proof about every SQLite shared-cache/read-uncommitted configuration.
- Connection 2 attempts a bounded concurrent write and records the actual SQLite/Python disposition (for example a busy/locked result, wait, or WAL snapshot-related conflict depending on transaction/journal configuration). Do not require one fixed exception string as the curriculum invariant.
- Connection 1 issues `ROLLBACK`; Connection 2 verifies balances remain exactly 1000.
- Execute an uncommitted transaction in a child process, kill the child with `SIGKILL`, reopen the database from the parent process, and verify that recovery leaves the database in its pre-transaction state.

### 7.6 Required Learner Evidence
- Invariant validation: State the system invariant mathematically and verify its retention before and after concurrent operations.
- Isolation classification: Correctly classify an observed execution as preventing dirty reads while enforcing writer serialization.
- Failure boundary articulation: Explain why killing a learner-owned process verifies client crash recovery, but does not prove power-loss durability.

### 7.7 Authority Classification
- **PRINCIPLE:** ACID definitions (Haerder & Reuter 1983), isolation anomaly taxonomy (Berenson et al. 1995), Write-Ahead Logging invariant.
- **SPECIFICATION / HISTORICAL AUTHORITY:** SQL standard isolation-level terminology plus the Berenson et al. critique/taxonomy. Research must name which source defines each anomaly because SQL-standard phenomena and later anomaly labels are not one universal taxonomy.
- **IMPLEMENTATION:** SQLite locking states (`UNLOCKED`, `SHARED`, `RESERVED`, `PENDING`, `EXCLUSIVE`), WAL checkpointing, `sqlite3` busy timeout handling.
- **CURRENT PRACTICE:** SQLite default journal mode (`DELETE` rollback journal) vs. WAL mode (`PRAGMA journal_mode=WAL`).

### 7.8 Authoritative Sources
- SQLite Transaction Control Documentation: <https://sqlite.org/lang_transaction.html>
- SQLite Isolation & Concurrency Guide: <https://sqlite.org/isolation.html>
- SQLite Atomic Commit in SQLite: <https://sqlite.org/atomiccommit.html>
- SQLite Write-Ahead Logging: <https://sqlite.org/wal.html>
- SQLite Online Backup API: <https://sqlite.org/backup.html>
- Haerder, T., & Reuter, A. (1983). "Principles of Transaction-Oriented Database Recovery." *ACM Computing Surveys*.
- Berenson, H., Bernstein, P., Gray, J., Melton, J., O'Neil, E., & O'Neil, P. (1995). "A Critique of ANSI SQL Isolation Levels." *ACM SIGMOD*.

### 7.9 Likely Misconceptions
- *"ACID Consistency is the same as distributed consistency (or EC-CON-014)."* (False: ACID Consistency means preserving application/schema invariants; EC-CON-014 defines named ordering and visibility guarantees).
- *"Serializable isolation means transactions execute one at a time on a single CPU core."* (False: Serializable means the observable outcome is equivalent to *some* serial execution order; engines can execute transactions concurrently if interleavings are serializable).
- *"Killing a database client process tests physical power-loss durability."* (False: terminating one learner-owned process leaves the OS/filesystem/device running. Power-loss behavior depends on additional volatile caches, ordering and persistence assumptions not exercised by this test.)
- *"Database rollback is the same thing as a backup."* (False: Rollback reverts uncommitted mutations in the active transaction log; backup produces a point-in-time snapshot copy of the database file).

### 7.10 Environment & Tool Constraints
- Tools: Python stdlib `sqlite3` supports multi-connection and subprocess management out of the box.
- Concurrency: SQLite depends on the selected VFS/filesystem locking semantics. The Required Lab must use a course-owned **local** writable directory and record the actual VFS/environment. Network/remote filesystem semantics vary by implementation/configuration and are outside the Core acceptance path.
- Cleanup: Must cleanly remove test database files and sidecars (`.db`, `.db-journal`, `.db-wal`, `.db-shm`).

### 7.11 Implementation-Time Smoke Requirements
- Verify a bounded second-writer/conflict scenario and record the actual SQLite result/code/exception without binding the Lab to one message string.
- On canonical Linux, an owned child may be terminated abruptly (for example via `SIGKILL`); verify bounded child reaping, lock release, reopen behavior, journal-mode-specific artifacts, and invariant state. Process termination remains a process-crash observation only.

---

## 8. M15 Research — Concurrency: Threads, Races & Synchronization

### 8.1 Capability Transition
- **From:** Isolated single-threaded processes with private address spaces where state can only be shared via explicit IPC or database transactions (M06/M07/M14).
- **To:** Multi-threaded programs sharing a single virtual address space, requiring explicit synchronization (mutexes, atomics, condition variables) to prevent race conditions, memory corruption, and deadlock.

### 8.2 Minimum Mechanism Model
1. **Threads vs. Processes:**
   - A process (`EC-CON-018`) has an independent virtual address space, file descriptor table, and security credentials.
   - Threads within a process share the entire address space (global variables, heap memory, open file descriptors), but each possesses private registers, program counter, and stack.
2. **Interleaving and Concurrency (EC-CON-015):**
   - The OS kernel preemptively schedules threads onto available CPU cores.
   - Instructions from different threads can interleave in arbitrary order. Even on a single-core system, time-slicing creates concurrency.
3. **Logical Race Condition vs. C Language Data Race (Undefined Behavior):**
   - **Logical Race Condition:** a higher-level correctness failure whose outcome depends on permitted concurrent ordering/interleaving.
   - **C data race:** a language-level condition involving conflicting accesses in different threads under the C memory model; a non-atomic conflicting access without the required ordering can make program behavior undefined.
   - **Pedagogical Requirement:** the Required broken path must **not rely on C undefined behavior**. The selected C11-compatible teaching pattern uses atomic load/store operations for each access while deliberately leaving the multi-step read→compute→write transition non-atomic.
   - `sched_yield()` is only an observation aid. It does not promise another thread will run or guarantee a lost update. The Design must distinguish the stable logical interleaving from scheduler-specific evidence.
4. **Mutual Exclusion via POSIX Mutex (`pthread_mutex_t`):**
   - A correctly shared mutex can exclude conflicting critical-section execution according to POSIX mutex semantics.
   - Lock/unlock operations are synchronization operations with memory-ordering consequences under POSIX/C integration; Design should avoid importing a C++-specific “synchronizes-with” sentence as if it were the POSIX wording.
   - Default mutex use does not establish a FIFO/fairness curriculum guarantee.
5. **Condition Synchronization via POSIX Condition Variables (`pthread_cond_t`):**
   - A condition variable is a wait/notification mechanism used together with a mutex-protected predicate; the condition variable itself is not the truth value.
   - `pthread_cond_wait` atomically releases the associated mutex as part of waiting and returns with that mutex reacquired.
   - A return from the wait does not prove the predicate is currently true: spurious wakeups and competing threads are possible.
   - **Course Required-Lab pattern:** re-evaluate the predicate in a loop:
     ```c
     pthread_mutex_lock(&mutex);
     while (!predicate_is_true) {
         pthread_cond_wait(&cond, &mutex);
     }
     /* predicate observed true while holding mutex */
     pthread_mutex_unlock(&mutex);
     ```
     The loop is the accepted course pattern; equivalent correct predicate-recheck structures are a programming matter, not a claim that POSIX requires one literal syntax.
6. **Deadlock & Progress Failures:**
   - Four Coffman conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.
   - L15 addresses deadlock avoidance via strict lock acquisition hierarchies (e.g., always acquire Lock A before Lock B).
7. **Thread vs. Asynchronous Event-Loop Models:**
   - OS-thread models use kernel-scheduled execution contexts and may run in parallel when runtime/hardware permit; blocking, stack/resource cost and scheduling overhead are workload/runtime dependent.
   - An async runtime can cooperatively interleave tasks around suspension points in an event loop, but the wider process may still use multiple threads or native services. Async does not inherently remove shared-state races, ordering bugs, blocking calls, or parallelism concerns.
   - Design should compare mechanism/cost/constraints for a stated workload rather than declare “threads for CPU, async for I/O” as a universal rule.
8. **CPython GIL / Free-Threading Reality:**
   - The GIL is a CPython runtime implementation mechanism, not a Python-language invariant.
   - In a conventional GIL-enabled CPython build, only a thread holding the GIL executes Python object/C-API work at a time, but thread switching and GIL release around blocking operations mean application synchronization is still required for shared invariants. Do **not** use a specific `counter += 1` lost-update result or opcode sequence as a Core invariant.
   - CPython 3.13 introduced an optional free-threaded build. As of current stable Python 3.14, PEP 779 moved free-threaded CPython into an **officially supported phase**, but it is not the default phase-III runtime model; extensions can still cause the GIL to be enabled. Record build/runtime capability when observing it.

### 8.3 Explicit Non-Goals
- Formal memory model operational semantics (Java Memory Model / C++11 Acquire-Release memory order proofs).
- Lock-free data structures (Hazard pointers, ABA problem, lock-free queues).
- Software transactional memory or kernel futex internals.
- Proving starvation freedom or fair queuing algorithms.
- Full Python asynchronous framework (FastAPI/Tornado) engineering.

### 8.4 Hidden Prerequisites / Just-in-Time Support
- Process execution model and kernel scheduling from M06.
- Virtual memory and address spaces from M07.
- C language basics and compilation from M00/M03.

### 8.5 Candidate Real Observation / Activity
- Compile a C11 program with two threads incrementing a shared counter using relaxed atomic operations with an explicit yield:
  ```c
  int val = atomic_load_explicit(&counter, memory_order_relaxed);
  sched_yield();
  atomic_store_explicit(&counter, val + 1, memory_order_relaxed);
  ```
- Run the broken atomic compound update under a **bounded attempt budget** and record whether a lost-update interleaving is actually observed; no fixed erroneous-count range or success percentage is a specification.
- Repair the compound update with the course mutex and assert the intended final invariant on every completed repaired run.
- Implement the condition-variable rendezvous and verify the predicate/order invariant.
- For Python, record the actual CPython build/GIL capability and use documentation plus a controlled shared-state example if needed. Do not require `counter += 1` to lose updates on every/current CPython build.

### 8.6 Required Learner Evidence
- Interleaving enumeration: Draw an execution trace showing how two threads reading value `42` both write back `43`, losing one increment.
- Mutex verification: Prove that adding mutex locks guarantees mutual exclusion and restores invariant correctness.
- Predicate explanation: Explain why a single pre-wait `if` is insufficient for the course predicate and why the predicate must be rechecked after `pthread_cond_wait` returns.
- GIL boundary analysis: Explain why a named CPython GIL mode does not substitute for an application synchronization contract, and distinguish default GIL-enabled vs free-threaded builds.

### 8.7 Authority Classification
- **PRINCIPLE:** Concurrency vs. parallelism, mutual exclusion, condition rendezvous, Coffman deadlock conditions, race conditions.
- **SPECIFICATION:** The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024 for pthread interfaces; the Required Lab deliberately uses the C11 atomic API/semantics introduced in ISO/IEC 9899:2011, while **ISO/IEC 9899:2024 (C23) is the current C standard** and must be recorded as such.
- **IMPLEMENTATION:** named Linux/glibc/NPTL behavior where observed; named CPython build/runtime behavior where observed.
- **CURRENT PRACTICE:** Python 3.14.7 is current stable on the review date; PEP 779 describes supported free-threaded CPython phase II. `-pthread` is an explicit compiler/link-driver option on the canonical toolchain, not a universal compiler default.

### 8.8 Authoritative Sources
- The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024:
  - `pthread_mutex_lock`: <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html>
  - `pthread_cond_wait`: <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_wait.html>
- ISO/IEC 9899:2011 (C11), atomics introduced for the Required C11-compatible path; current-standard status must also cite ISO/IEC 9899:2024 (C23).
- Python Software Foundation: PEP 703 – *Making the Global Interpreter Lock Optional in CPython*: <https://peps.python.org/pep-0703/>
- Python Software Foundation: PEP 779 – *Criteria for Supported Status for Free-Threaded Python*: <https://peps.python.org/pep-0779/>
- Python Official Threading Documentation: <https://docs.python.org/3/library/threading.html>
- OSTEP: Arpaci-Dusseau, R. & Arpaci-Dusseau, A. *Operating Systems: Three Easy Pieces*, Concurrency chapters (26–32).

### 8.9 Likely Misconceptions
- *"Concurrency is just another name for parallelism."* (False: Concurrency is about program structure and dealing with multiple things at once; parallelism is about simultaneous physical execution on multiple hardware cores).
- *"Running a threaded program once without errors proves it is thread-safe."* (False: Thread scheduling is non-deterministic; a data race may manifest once in a million runs).
- *"A race condition is the same thing as a C/C++ data race."* (False: A data race is a specific language-level construct producing undefined behavior; a race condition is a general logical flaw in system state transitions).
- *"Using atomic variables automatically makes compound multi-step operations correct."* (False: Individual reads and writes may be atomic, but the compound state transition across multiple variables or steps remains non-atomic).
- *"A mutex guarantees fair FIFO turn-taking among waiting threads."* (False: Standard POSIX mutexes make no fairness guarantees; recently unblocked or running threads may re-acquire the lock ahead of long-waiting threads).
- *"Python's GIL means multi-threaded Python programs do not need locks."* (False: application invariants still require synchronization. Exact opcode switching and whether one expression such as `x += 1` exhibits a lost update are version/build/implementation observations, not a Python-language guarantee.)

### 8.10 Environment & Tool Constraints
- Compiler: `gcc` or `clang` with `-std=c11 -pthread`.
- OS: **canonical Linux** with actual pthread/toolchain capability recorded. WSL is a hosted Linux path that must be preflighted; MinGW is not treated as equivalent POSIX/NPTL evidence for the Required Core.
- Execution Safety: Deadlock experiments must be wrapped in a watchdog process with a hard timeout to prevent hanging student terminals.

### 8.11 Implementation-Time Smoke Requirements
- Verify that `gcc -std=c11 -pthread` compiles the atomic compound test cleanly without compiler errors or warnings.
- Under a bounded attempt budget, require at least one **actually observed** lost-update trace on the accepted canonical implementation image before calling that smoke path PASS. If scheduler behavior makes the chosen yield-only fixture unreliable, Design must add a bounded course-controlled phase handoff or classify the observation as environment-sensitive; do not encode a ≥95% scheduler probability.

---

## 9. EC-CON-014 Consistency First-Home Evidence (M14 / L14-02)

### 9.1 Canonical Registry Contract
- **ID:** `EC-CON-014`
- **Canonical Names:** 一致性 — Consistency (qualifiers: transaction, replicated system)
- **Canonical Definition:** *"The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee. It must be qualified; 'consistent' does not mean merely fresh, durable, or correct in every sense."*
- **First Home:** M14, `L14-02`.
- **Scheduled Revisits:** M17 (replication/linearizability/eventual consistency), M18 (delivery/ordering), M23, M24.

### 9.2 Disambiguation of the Overloaded Term "Consistency"

| Domain | What "Consistency" Means | Who / What Enforces It | Failure Mode / Manifestation |
|---|---|---|---|
| **ACID "C" (Traditional DB)** | Application and schema invariant preservation (e.g., account balance $\ge 0$, total conservation of money). | Application logic + database schema constraints (`CHECK`, `FOREIGN KEY`). | Application bug commits state where invariants are violated. |
| **Transaction Isolation (EC-CON-014 Home)** | Named ordering and visibility guarantees for concurrent transactions (Read Committed, Repeatable Read, Snapshot, Serializable). | Database engine concurrency control (2PL, MVCC, Locks, WAL). | Anomalies: Dirty read, non-repeatable read, lost update, write skew. |
| **Replicated Systems (M17 Revisit)** | Named replicated-state visibility/ordering models such as linearizability or eventual consistency. | Implementation may use leaders, quorums, consensus, anti-entropy, or other mechanisms depending on the system. | Stale/ordering/divergence observations must be interpreted under the named model and failure assumptions. |

### 9.3 Pedagogy in L14-02
- In `L14-02`, learners analyze concurrent database transactions.
- They analyze an interleaving whose final state **violates the stated account invariant**. Avoid using bare “inconsistent state” here before the named EC-CON-014 guarantee is stated.
- The lesson introduces `EC-CON-014` by demonstrating that "consistent" cannot be claimed without specifying the **exact named guarantee**:
  - Under *Read Committed*, an observer is guaranteed never to see uncommitted state transitions (preventing dirty reads), but concurrent writers can still produce lost updates.
  - Under *Serializable*, the database guarantees that all observers see results consistent with *some* sequential execution of allowed state transitions.
- Guardrail: M14 must explicitly stop at database single-node transaction isolation. Distributed consistency, network partitions, and CAP theorem trade-offs are strictly preserved for M17.

---

## 10. EC-CON-015 Concurrency First-Home Evidence (M15 / L15-01)

### 10.1 Canonical Registry Contract
- **ID:** `EC-CON-015`
- **Canonical Names:** 并发 — Concurrency (qualifiers: threads, processes, event loops, distributed operations)
- **Canonical Definition:** *"Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations."*
- **First Home:** M15, `L15-01`.
- **Scheduled Revisits:** M16–M18, M20, M23, M24.

### 10.2 Disambiguation: Concurrency vs. Parallelism

```
Concurrency (Logical Interleaving / Overlapping Progress):
Single Core:   [Task A: step 1] -> [Task B: step 1] -> [Task A: step 2] -> [Task B: step 2]
(Interleaving creates shared-state and ordering hazards even without simultaneous hardware execution)

Parallelism (Physical Simultaneous Execution):
Core 0:        [Task A: step 1] ------> [Task A: step 2] ------> [Task A: step 3]
Core 1:        [Task B: step 1] ------> [Task B: step 2] ------> [Task B: step 3]
(Simultaneous execution requires multiple execution units; exposes memory bus contention & cache coherency)
```

### 10.3 Pedagogy in L15-01
- In `L15-01`, learners encounter the canonical definition of `EC-CON-015`.
- They explore how preemptive time-slicing by an operating system scheduler causes independent instruction sequences to interleave arbitrarily.
- The lesson proves that concurrency is an architectural property: Even on a single-core computer or inside a single-threaded virtual machine with context switches, concurrency creates shared-state and ordering obligations.
- Guardrails: M12's event loop was an application preview of asynchronous task queues; M14's transactions were an application preview of interleaved database transactions. M15 provides the foundational, unified systems definition.

---

## 11. Canonical Concept Revisit & No-New-ID Audit

### 11.1 Audit Table for S5

| Canonical Concept ID | Canonical Name | M13 Role | M14 Role | M15 Role | Boundary / Guardrail Enforced |
|---|---|---|---|---|---|
| `EC-CON-001` | State (状态) | Revisit: On-disk table and index state | Revisit: Transaction state transitions ($S_0 \to S_1$) | Revisit: Shared memory state vs. thread private stacks | Distinguish state from storage |
| `EC-CON-003` | Representation (表示) | Revisit: Slotted pages, B-tree nodes, tuple binary layout | — | — | Differentiate logical tuples from on-disk binary representations |
| `EC-CON-005` | Interface (接口) | Revisit: SQL as a declarative interface | — | — | Distinguish SQL interface contract from physical query plan execution |
| `EC-CON-006` | Trade-off (权衡) | Revisit: Index read acceleration vs. write/space overhead | Revisit: Isolation level strictness vs. concurrency throughput | — | Requires explicit constraints; not vague "pros and cons" |
| `EC-CON-007` | Specification (规格) | — | Revisit: Transaction contract and isolation specifications | Revisit: POSIX thread and synchronization specifications | Contractual guarantees vs. implementation details |
| `EC-CON-008` | Invariant (不变量) | Revisit: Schema constraints (`CHECK`, `NOT NULL`, `FOREIGN KEY`) | Revisit: Transaction-preserving domain invariants | Revisit: Mutex-protected critical section invariants | A property that holds across all valid state transitions |
| `EC-CON-009` | Correctness (正确性) | Revisit: Result equivalence for the declared query | Revisit: Transaction execution satisfies the declared invariant / named isolation contract | Revisit: Synchronization preserves the declared invariant for executions allowed by the stated model | One observed run is evidence, not proof of all schedules |
| `EC-CON-011` | Caching (缓存) | Revisit: Database engine buffer pool | — | — | Distinguish DB buffer pool from OS page cache and hardware cache |
| `EC-CON-012` | Locality (局部性) | Revisit: B-tree page layout, clustered indexing, sequential I/O | — | — | Spatial locality on storage blocks |
| `EC-CON-013` | Isolation (隔离) | — | Revisit: Database transaction isolation levels | Revisit: Synchronization boundaries protecting shared state | Distinguish transaction isolation from OS process address space isolation |
| `EC-CON-014` | Consistency (一致性) | — | **CANONICAL FIRST HOME (`L14-02`)** | — | **Must be qualified by named guarantee; separate ACID C from systems consistency** |
| `EC-CON-015` | Concurrency (并发) | — | — | **CANONICAL FIRST HOME (`L15-01`)** | **Overlapping progress / interleaving; distinguish from parallelism** |
| `EC-CON-016` | Durability (持久性) | — | Revisit: Write-Ahead Logging (WAL) and commit persistence | — | Durability under named failure model; not a synonym for backup or replication |
| `EC-CON-018` | Process (进程) | — | — | Revisit: Process address space vs. thread execution contexts | Threads share process resources |

### 11.2 Confirmation of Zero New IDs
- Terminology such as *B-tree*, *Index*, *Query Plan*, *Buffer Pool*, *Transaction*, *ACID*, *MVCC*, *Lock*, *Deadlock*, *Mutex*, *Condition Variable*, *Semaphore*, *GIL*, and *Async/Await* are treated as technical mechanism terms, **not** new canonical concept IDs.
- *Schema Evolution*, *Reader/Writer Compatibility*, *Migration/Backfill*, *Source-of-Truth vs. Derived Data*, and *Provenance* remain strictly application patterns in M13 `L13-03` under existing concepts (`EC-CON-001`, `003`, `005`, `008`).

---

## 12. LAB-REQ-04 Re-Audit: SQLite Query Plans, Indexing & Workload Evidence

### 12.1 Objective and Scope
- **ID:** `LAB-REQ-04`
- **Module Placement:** M13 Databases: Storage & Indexing
- **Type:** Build — Essential CS original
- **Core Mechanism:** Relational query execution, semantic `SCAN` vs `SEARCH` access-path evidence, index trade-offs, result equivalence, and empirical workload measurement.

### 12.2 Technical Verification & Plan Output Structure
Empirical testing on SQLite 3.45.3 / 3.53.4 confirms that `EXPLAIN QUERY PLAN` outputs a structured 4-column record `(id, parent, notused, detail)`:

```sql
-- Schema setup
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    status TEXT,
    created_at TEXT
);
CREATE INDEX idx_orders_user ON orders(user_id);
```

1. **Selective Indexed Query:**
   ```sql
   EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 1042;
   -- Output detail: SEARCH orders USING INDEX idx_orders_user (user_id=?)
   ```
2. **Primary Key Lookup:**
   ```sql
   EXPLAIN QUERY PLAN SELECT * FROM orders WHERE id = 1042;
   -- Output detail: SEARCH orders USING INTEGER PRIMARY KEY (rowid=?)
   ```
3. **Unindexed Table Scan:**
   ```sql
   EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'COMPLETED';
   -- Output detail: SCAN orders
   ```
4. **Covering Index Query:**
   ```sql
   CREATE INDEX idx_user_amount ON orders(user_id, amount);
   EXPLAIN QUERY PLAN SELECT amount FROM orders WHERE user_id = 1042;
   -- Output detail: SEARCH orders USING COVERING INDEX idx_user_amount (user_id=?)
   ```

### 12.3 Workload Trade-off Verification
The Agent performed bounded synthetic smoke work at small and medium fixture sizes. Those numbers are **author-host evidence only**, not Design constants.

The Design handoff should preserve:
- actual row count, schema, data distribution, SQLite CLI/library versions and database page settings;
- actual `SCAN`/`SEARCH` detail before/after the index;
- result equivalence;
- repeated timing with warmup/cache-state notes and raw samples;
- database-file and write-time deltas.

Do **not** require:
- “100 rows = one page”;
- “50,000 rows = 2.5 MB”;
- 2–3 index page reads;
- sub-millisecond lookup;
- 15–30 ms scan;
- 35% file growth;
- 40% insert slowdown.

All of those depend on schema, values, page size, cache/filesystem/storage, build, query and engine version.

### 12.4 Truthful Fallback & Pedagogical Integrity
- If SQLite's cost-based optimizer chooses `SCAN` on a small table despite an available index, the lab **must celebrate this as a truthful teaching moment** rather than forcing an index via query hints. This reinforces the core principle: *An index is an implementation mechanism with trade-offs, not a magic speed button.*
- Result Equivalence: The lab fixture automated test verifies:
  $$\text{ResultSet}(\text{Query}_{\text{unindexed}}) \equiv \text{ResultSet}(\text{Query}_{\text{indexed}})$$

---

## 13. LAB-REQ-05 Re-Audit: SQLite Transactions, Isolation, Rollback & Recovery Boundary

### 13.1 Objective and Scope
- **ID:** `LAB-REQ-05`
- **Module Placement:** M14 Databases: Transactions, Recovery & Isolation
- **Type:** Build — Essential CS original
- **Core Mechanism:** Transaction atomicity, committed-only visibility (prevention of dirty reads), single-writer serialization conflicts, application rollback, and crash recovery boundaries.

### 13.2 Multi-Connection Architecture
Using Python's standard `sqlite3` library, the lab instantiates two independent database connection objects (`conn1`, `conn2`) connected to a single local filesystem database file:

```python
# Invariant: Total system balance must equal 1000
# conn1 initiates atomic transfer:
conn1.execute("BEGIN IMMEDIATE;")
conn1.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1;")
conn1.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2;")

# conn2 reads balances concurrently:
cur2 = conn2.cursor()
cur2.execute("SELECT balance FROM accounts WHERE id = 1;")
val = cur2.fetchone()[0]
# VERIFICATION: val is 500 (original committed balance), NOT 400 (uncommitted mutation)
# Proves committed-only visibility and absence of Dirty Reads.

# conn2 attempts to modify:
try:
    conn2.execute("BEGIN IMMEDIATE;")
except sqlite3.OperationalError as e:
    # Record the actual SQLite result code / Python exception / message.
    # The stable evidence is the bounded second-writer conflict disposition,
    # not one fixed English string.
```

### 13.3 Rollback and Child Crash Recovery
1. **Explicit Rollback:** In the isolated course fixture, calling `conn1.rollback()` removes conn1's uncommitted transfer effects; verify the declared account invariant and the rows visible from a fresh/appropriate second-connection observation. Do not generalize this to restoring a whole multi-user database to one prior global state.
2. **Interrupted Child Process:**
   - A child process opens a transaction and modifies rows in a declared journal mode.
   - Before `COMMIT`, the parent terminates only that owned child under a bounded watchdog.
   - The parent reaps the child and reopens the database.
   - Record the actual side files and reopen behavior. In rollback-journal mode a hot journal may require recovery; in WAL mode the presence of WAL content does not mean an uncommitted transaction is “rolled back from WAL” in the same way. Verify the declared application invariant/committed state, not one universal internal recovery narrative.
3. **Safety & Claim Boundary:**
   - The lab explicitly instructs learners: Terminating a child process tests **client crash recovery** (recovery from an abnormal application crash). It does **not** test physical durability against hardware power failure.

---

## 14. LAB-REQ-03 Re-Audit: POSIX Threads Race, Rendezvous & Progress Boundaries

### 14.1 Objective and Scope
- **ID:** `LAB-REQ-03`
- **Module Placement:** M15 Concurrency: Threads, Races & Synchronization
- **Type:** Build — Essential CS original
- **Core Mechanism:** Multi-threaded shared memory, logical race condition reproduction without undefined behavior, mutex synchronization, condition-variable rendezvous, and deadlock watchdog design.

### 14.2 The UB-Free Lost Update Broken Path
In standard C, concurrent unsynchronized writes to a plain variable (`int counter; counter++;`) constitute a **Data Race**, which §5.1.2.4 of the C standard defines as **Undefined Behavior (UB)**. Under UB, modern optimizing compilers (GCC/Clang) may optimize loops into single register additions or vectorize accesses, eliminating the observable race or causing erratic failure modes.

To teach the authentic mechanism rigorously without language-level UB, `LAB-REQ-03` defines the counter using C11 atomics (`<stdatomic.h>`), but constructs a **compound, non-atomic read-modify-write operation**:

```c
#include <stdio.h>
#include <stdatomic.h>
#include <pthread.h>
#include <sched.h>

atomic_int shared_counter = 0;

void* worker(void* arg) {
    for (int i = 0; i < 10000; i++) {
        // Step 1: Defined atomic read (strictly legal, no data race)
        int current = atomic_load_explicit(&shared_counter, memory_order_relaxed);

        // Step 2: Explicit cooperative yield to maximize thread interleaving
        sched_yield();

        // Step 3: Defined atomic write (strictly legal, no data race)
        atomic_store_explicit(&shared_counter, current + 1, memory_order_relaxed);
    }
    return NULL;
}
```

- **Why this path is useful:** accesses to the shared counter are atomic, so the intended lost-update example does not rely on an unsynchronized conflicting access to that object. Research should not claim the entire future program has “zero undefined behaviors” until the exact implemented source is reviewed.
- **The observed failure:** Because the two-step sequence (Read $\to$ Write) is not atomic as a compound operation, Thread 1 and Thread 2 both read `current = 42`, both compute `43`, and both store `43`. One update is completely lost.
- **Agent host observation:** one tested source/toolchain/run set produced lost updates. Preserve raw run counts if useful, but **do not promote a 10,000–15,000 range or 100% manifestation rate into the Lab contract**; `sched_yield()` is not an interleaving guarantee.

### 14.3 Mutex Repair & Condition Rendezvous
1. **Mutex Repair:**
   - Wrapping the course compound sequence with the shared mutex is the proposed repair. For a fixture with two workers × 10,000 intended increments, every **completed repaired run** should satisfy the declared final target 20,000; repeated passing runs are not proof over every possible program/environment schedule.
2. **Condition-Variable Rendezvous:**
   - Worker 2 waits for Worker 1 to produce a payload:
     ```c
     pthread_mutex_lock(&lock);
     while (!payload_ready) {
         pthread_cond_wait(&cond, &lock);
     }
     consume(payload);
     pthread_mutex_unlock(&lock);
     ```
   - Reinforces the course rule that the predicate is re-evaluated in a `while` loop after condition-wait returns, covering spurious wakeups and competing-thread predicate changes.
3. **Deadlock Watchdog Architecture:**
   - Reversed lock order creates a **deadlock possibility**, not a scheduler guarantee. If deterministic evidence is desired, Design should add a bounded course-controlled handshake proving each worker acquired its first lock before both attempt the second.
   - An owned-child watchdog supplies a safety deadline and then performs platform-appropriate termination/reaping. A watchdog timeout by itself proves only “the child did not finish by the deadline”; interpret deadlock only together with the fixture's lock-state evidence.
   - The timeout value is configuration recorded in evidence, not a universal two-second rule; cleanup must be idempotent and must never target unrelated processes.

---

## 15. LAB-OPT-03 Currentness, Feasibility & Licensing: PostgreSQL EXPLAIN & Isolation Comparison

### 15.1 Objective and Status
- **ID:** `LAB-OPT-03`
- **Status:** **Optional** comparison lab after completing `LAB-REQ-04` and `LAB-REQ-05`.
- **Adopt vs. Adapt:** Adapt official PostgreSQL documentation into a bounded, reproducible local comparison.

### 15.2 Technical Content & Added Value
1. **`EXPLAIN` vs. `EXPLAIN (ANALYZE, BUFFERS)`:**
   - PostgreSQL provides `EXPLAIN (ANALYZE, BUFFERS)` which actually executes the query, recording:
     - Estimated startup and total cost vs. actual execution time;
     - Estimated rows vs. actual returned rows;
     - Shared buffer hits, reads, dirtied, and written pages.
   - This exposes the direct relationship between query plan execution and buffer pool cache behavior.
2. **Repeatable Read Update-Conflict Example:**
   - PostgreSQL 18 documents that a Repeatable Read transaction trying to update a row changed by another transaction since its snapshot can be rolled back with a serialization-failure disposition.
   - Record the actual SQLSTATE/message from the tested PostgreSQL version rather than binding the course to one exact English string.
   - PostgreSQL documentation requires applications using Repeatable Read to be prepared to retry a failed transaction from the beginning. Do not flatten PostgreSQL's MVCC + locking/conflict machinery into a generic “optimistic concurrency control” label.

### 15.3 Licensing & Provenance
- Source: Official PostgreSQL Documentation (<https://www.postgresql.org/docs/current/>).
- License: PostgreSQL License (a liberal BSD/MIT-style open-source license).
- Disposition: All lab documentation, setup scripts, and test harnesses will be original Essential CS works (Apache-2.0 / CC BY-SA 4.0), citing PostgreSQL documentation.

### 15.4 Environment & Non-Requirement Boundary
- **PostgreSQL must remain strictly Optional.**
- Core curriculum mastery must never depend on a running PostgreSQL daemon or container.
- For learners undertaking this Optional Lab, a local `initdb`/`pg_ctl` path or disposable container may be documented. If PostgreSQL cannot be run, record `OPTIONAL LAB NOT RUN / TOOL UNAVAILABLE`; a course reference trace may support explanation but must not be counted as the learner's live PostgreSQL observation.

---

## 16. LAB-OPT-05 Rights & Currentness Disposition: OSTEP Semaphore Rendezvous

### 16.1 Objective and Status
- **ID:** `LAB-OPT-05`
- **Module Placement:** M15 Concurrency
- **Status:** **Optional** external exercise.
- **Adopt vs. Adapt:** **Adopt — link-only**.

### 16.2 Upstream Rights & Licensing Review
- Upstream Repository: `remzi-arpacidusseau/ostep-homework` (<https://github.com/remzi-arpacidusseau/ostep-homework>)
- Bounded Commit Checked: `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`
- Bounded Path: `threads-sema/` (`README.md`, `rendezvous.c`, `barrier.c`)
- **Licensing Finding:** The `ostep-homework` repository contains **no formal license declaration** in its root directory. Upstream issue #71 requesting licensing clarification remains open.
- **Strict Rights Barrier:** Public accessibility on GitHub is not a license for redistribution or adaptation.

### 16.3 Educational Disposition
- Essential CS **will not redistribute, bundle, or vendor** any source code, skeletons, or solutions from `ostep-homework`.
- LAB-OPT-05 is presented as a **link-only pointer** for independent study.
- The self-contained Required Core mechanism is `LAB-REQ-03`; OSTEP is not needed to satisfy the selected Core evidence contract.

---

## 17. EXP-02 PostgreSQL Source-Route Recheck

### 17.1 Canonical Route Verification
All three canonical paths still exist in PostgreSQL's moving `master` source. Lead recheck on 2026-09-04 observed `master` at commit `7344937cbe640cd8c5304cefe7d6b726187ad4ab`. This **development branch is not “stable 18”**; PostgreSQL 18.6 is the separate current stable release/documentation line.

```
Target 1: src/backend/optimizer/plan/README
Status: Path still exists, but current content is largely historical subselect implementation notes originating in 1998.
Role: **Does not support the dossier's previous claim of being the current high-level Path→Plan architecture overview.** The parent `src/backend/optimizer/README` currently provides that overview, but it is supplemental Research authority only; this Research PR does not silently replace the Blueprint's canonical EXP-02 target.

Target 2: src/backend/optimizer/path/costsize.c
Status: Active, primary cost-estimation implementation.
Role: Contains cost calculation routines:
      - cost_seqscan(): Estimates I/O and CPU cost for sequential table scans.
      - cost_index(): Estimates I/O and CPU cost for B-tree index scans.

Target 3: src/backend/storage/buffer/README
Status: Active, core storage architecture document.
Role: Explains shared buffer pool management, page pin/unpin semantics, buffer header spinlocks, and the clock-sweep buffer replacement algorithm.
```

### 17.2 Bounded Pedagogical Stopping Point
- **What implementation reality becomes visible:** `costsize.c` exposes current cost-model implementation and `buffer/README` exposes current shared-buffer access rules. The canonical `plan/README` target primarily exposes historical/subselect implementation notes, which itself is useful currentness evidence: source-file names can remain while pedagogical meaning drifts.
- **Source-route risk:** later Design must not claim Target 1 proves the current general Path→Plan architecture. If Design needs the parent `src/backend/optimizer/README` in the learner's exact route, that is an explicit Lead source-selection adjustment rather than a silent replacement.
- **What the learner must ignore:** The learner must ignore executor dispatch loops, individual access method internals (GiST, GIN, BRIN), planner configuration variables (GUCs), catalog statistics generation, and WAL recovery logic.
- **Compilation Gate:** EXP-02 requires no PostgreSQL compilation. Learner inspection remains link/source-reading-only. “No compile required” is the Core boundary; a learner's unrelated local PostgreSQL install for LAB-OPT-03 is a separate Optional capability.

---

## 18. Environment / Tool / Reproducibility Matrix

### 18.1 Tool Classification Table

| Tool / Capability | Classification | Current Version Checked | Primary Purpose | Implementation Smoke Required | Truthful Fallback / Skip Disposition |
|---|---|---|---|---|---|
| **Python 3 + stdlib `sqlite3`** | Required for the planned original fixtures/tests | Agent host: Python 3.13.1 + SQLite 3.45.3; current upstream Python stable: 3.14.7 | Fixture generation, two-connection transaction harness, semantic EQP/result checks | Yes: record Python implementation/version and embedded SQLite version | Capability-gated on the actual canonical Linux image; do not assume parity across WSL/containers/other OSes |
| **`sqlite3` CLI** | **Required baseline for LAB-REQ-04 per Blueprint selection** | Current upstream SQLite stable: 3.53.4 | Learner-facing interactive `EXPLAIN QUERY PLAN` / SQL observation | Yes: record CLI version and semantic plan evidence | If absent: `ENVIRONMENT-BLOCKED / NOT RUN` for the CLI-required path; Python is support/test evidence, not “100% feature parity” with CLI dot-commands/presentation |
| **`gcc` or compatible C compiler** | Required for LAB-REQ-03 on canonical Linux | Agent host: GCC 14.2.0 x86-64 | Compile the C11-compatible atomic/pthread fixture with explicit `-std=c11 -pthread` | Yes | Record actual compiler and flag support; no cross-platform equivalence assumption |
| **POSIX Threads** | Required for LAB-REQ-03 on canonical Linux | Agent host: glibc 2.39/NPTL; normative API: POSIX Issue 8 | Mutex/condition-variable/thread execution | Yes | WSL/container paths must be preflighted; MinGW is not accepted as equivalent NPTL/POSIX evidence |
| **C atomics** | Required for the UB-free broken path | C11 API/semantics used by course; current C standard ISO/IEC 9899:2024 | Defined atomic accesses around a logically non-atomic compound update | Yes | Verify the chosen compiler/library exposes the required atomics; do not claim every “modern C compiler” is equivalent |
| **Owned-child watchdog** | Required safety mechanism | Course implementation choice | Bound deadlock/interruption experiments and reap children | Yes | Timeout duration/termination mechanism is a test parameter recorded by the harness, not a universal two-second law |
| **PostgreSQL Server / `psql`** | Optional | Current stable major/minor: PostgreSQL 18.6 | LAB-OPT-03 comparison only | Yes if Optional Lab is exercised/implemented | `SKIP / NOT RUN` if unavailable; never a Core dependency |
| **Docker / Podman** | Optional convenience | Record actual capability if used | Optional PostgreSQL runner only | Yes if used | Never required for Core; native/local alternative or skip |
| **ThreadSanitizer or race tooling** | Optional enrichment | Record actual compiler/runtime capability | Contrast language data-race detection with the course's defined logical-race path | Capability smoke if used | Absence is `TOOL UNAVAILABLE / SKIP`; it is not Required evidence |

### 18.2 OQ-BP-006 Alignment
This matrix documents current, verified tool versions without closing OQ-BP-006. Permanent curriculum-wide environment pinning remains open for final curriculum consolidation.

---

## 19. Source Authority Register

```
+------------------------------------------------------------------------------------------------------------------+
| PRINCIPLE (Stable Theories & Universal Mechanisms)                                                                |
| - Relational Model & Relational Algebra (Codd 1970)                                                              |
| - B-Tree & B+ Tree Search Complexity (Bayer & McCreight 1972)                                                     |
| - ACID Transaction Model (Haerder & Reuter 1983)                                                                  |
| - Isolation Anomaly Taxonomy (Berenson, Bernstein, Gray, Melton, O'Neil, O'Neil 1995)                             |
| - Concurrency, Mutual Exclusion & Critical Sections (Dijkstra 1965)                                              |
| - Coffman Deadlock Conditions (Coffman, Elphick, Shoshani 1971)                                                   |
+------------------------------------------------------------------------------------------------------------------+
                                                        |
                                                        v
+------------------------------------------------------------------------------------------------------------------+
| SPECIFICATION (Normative Contracts & Platform Standards)                                                          |
| - ISO/IEC 9075 SQL standard family — use exact edition/part only for claims actually sourced                    |
| - ISO/IEC 9899:2024 (current C standard); C11 atomics remain the compatibility target for LAB-REQ-03             |
| - The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024 (POSIX pthread interfaces)                  |
+------------------------------------------------------------------------------------------------------------------+
                                                        |
                                                        v
+------------------------------------------------------------------------------------------------------------------+
| IMPLEMENTATION (Concrete Database & Runtime Engine Mechanics)                                                     |
| - SQLite 3 Query Planner & Storage Engine (B-tree pages, master table, EQP detail strings)                       |
| - SQLite Transaction & Locking Engine (Rollback journal, WAL, busy handler, file locking)                        |
| - Linux/glibc/NPTL behavior only where actually inspected during implementation smoke; POSIX remains authority   |
| - Named CPython build/runtime GIL/free-threading behavior; Python language contract kept separate                  |
| - PostgreSQL Backend Optimizer & Buffer Manager (costsize.c, plan/README, buffer/README)                         |
+------------------------------------------------------------------------------------------------------------------+
                                                        |
                                                        v
+------------------------------------------------------------------------------------------------------------------+
| CURRENT PRACTICE (Present-Day Operational Baselines & Conventions)                                               |
| - SQLite 3.53.4 current upstream release; Agent Python 3.13.1 embedded SQLite 3.45.3 as separate host evidence    |
| - Python 3.14.7 current stable; free-threaded CPython is supported phase II under PEP 779, build/runtime-dependent |
| - Agent GCC 14.2 toolchain observation; explicit `-std=c11 -pthread` capability must be preflighted              |
| - PostgreSQL 18.6 current stable documentation; PostgreSQL `master` is a separate moving development source      |
+------------------------------------------------------------------------------------------------------------------+
```

---

## 20. Licensing, Redistribution & Adaptation Constraints

| Source / Entity | Owner / Maintainer | Exact URL / Route | Authority Class | Reuse / License Status | Curriculum Disposition |
|---|---|---|---|---|---|
| **SQLite official docs/source** | SQLite project / Hwaci | <https://sqlite.org/copyright.html> | OFFICIAL IMPLEMENTATION DOCUMENTATION / SOURCE | SQLite's official copyright page states project-authored code and documentation are dedicated to the public domain; later Design should still link/paraphrase and review any non-project/packaging artifact separately | Essential CS fixtures remain original; do not turn “public domain” into a reason to copy large manuals/figures |
| **The Open Group Base Specs Issue 8** | IEEE / The Open Group | <https://pubs.opengroup.org/onlinepubs/9799919799/> | SPECIFICATION | Copyrighted standard | Cite/link bounded normative clauses; do not mirror standard text |
| **PostgreSQL Source & Docs** | PostgreSQL Global Development Group | <https://github.com/postgres/postgres> | OFFICIAL DOCUMENTATION / IMPLEMENTATION | PostgreSQL License; exact notice obligations should be preserved for any actual excerpt/source reuse | EXP-02 is link/inspection-first; Optional Lab prose/scripts should remain Essential CS-authored |
| **OSTEP Homework** | Remzi & Andrea Arpaci-Dusseau | <https://github.com/remzi-arpacidusseau/ostep-homework> | EXTERNAL TEACHING SOURCE | No repository license established in the checked route; upstream issue #71 remains open | **Strictly link-only (LAB-OPT-05)** unless rights are later established |
| **Python docs / CPython** | Python Software Foundation | <https://docs.python.org/3/> | OFFICIAL CONTRACT / IMPLEMENTATION (claim-dependent) | PSF licensing applies to project material; examples have their documented terms | Use official docs for current runtime capability; distinguish Python language/stdlib contract from CPython implementation |

---

## 21. Misconceptions & Inference Boundaries

### 21.1 Query & Indexing Misconceptions (M13)
- **Misconception:** *"Indexes make every query faster."*
  - **Inference Boundary:** Indexes consume storage and add maintenance work on affected writes. Whether a full `SCAN`, index search, covering index, or another plan is faster depends on the named engine/version, query, statistics, data distribution, cache state, and storage. **No universal 20–30% selectivity cutoff is accepted.**
- **Misconception:** *"`EXPLAIN` output proves real-world performance."*
  - **Inference Boundary:** `EXPLAIN` displays the query optimizer's static mathematical model and chosen access path. It does not measure runtime latency, disk I/O wait, or buffer pool contention. Only empirical benchmarking under stated cache conditions measures execution time.
- **Misconception:** *"The database buffer cache is just a wrapper around the OS page cache."*
  - **Inference Boundary:** The database buffer pool is user-space application memory managed by domain-aware replacement algorithms (Clock, LRU, 2Q) with transactional page-pinning semantics. The OS page cache operates at the kernel VFS level and is unaware of database transaction boundaries.

### 21.2 Transactions & Isolation Misconceptions (M14)
- **Misconception:** *"ACID Consistency means the same thing as every systems consistency model."*
  - **Inference Boundary:** Historical ACID “C” is commonly framed around integrity/application constraints for a transaction, while **EC-CON-014 is first defined here in M14** as a qualified ordering/visibility guarantee and later revisited in M17 for replicated systems. Do not relocate the concept's first home to M17.
- **Misconception:** *"Serializable isolation means transactions run one-by-one sequentially."*
  - **Inference Boundary:** Serializability guarantees that the observable outcome of concurrent execution is equivalent to *some* serial execution. High-performance engines execute transactions concurrently using locking or multi-versioning, intervening only when an interleaving threatens serial equivalence.
- **Misconception:** *"WAL guarantees complete durability against any physical failure."*
  - **Inference Boundary:** A WAL design supports recovery only under its named commit/flush/filesystem/device assumptions. SQLite's guarantee also depends on journal mode, `synchronous` configuration and storage behavior. No single `fsync()` sentence is a universal physical-durability guarantee.
- **Misconception:** *"Killing a test process proves power-loss durability."*
  - **Inference Boundary:** Process termination removes one process while the OS/filesystem/device continue running. A power-loss bound concerns additional volatile state and storage ordering/atomicity behavior; this course experiment does not test those layers.

### 21.3 Concurrency Misconceptions (M15)
- **Misconception:** *"Threads always execute at the exact same physical instant."*
  - **Inference Boundary:** Threads represent independent execution contexts. On a single CPU core, threads are interleaved via preemptive time-slicing. Concurrency bugs exist independently of whether hardware executes instructions simultaneously.
- **Misconception:** *"Passing a concurrency test 100 times proves code is race-free."*
  - **Inference Boundary:** Thread scheduling is non-deterministic. An interleaving that exposes a race condition may depend on microsecond timing variations, cache misses, or external OS interrupts. Testing never proves the absence of concurrency bugs.
- **Misconception:** *"A race condition is always a C language data race."*
  - **Inference Boundary:** A C data race is an undefined memory access. A race condition is a high-level logical flaw where the correctness of system state transitions depends on timing. Compound operations built from defined atomic operations can be free of data races yet suffer severe race conditions.
- **Misconception:** *"A condition variable notification guarantees the predicate is true."*
  - **Inference Boundary:** Notifications only wake waiting threads; they do not guarantee the condition remains true when the awakened thread eventually re-acquires the mutex. Spurious wakeups and intervening thread execution mandate the use of a `while` loop around `pthread_cond_wait`.
- **Misconception:** *"Python's GIL makes multi-threaded Python programs thread-safe."*
  - **Inference Boundary:** A GIL-enabled CPython build serializes Python object/C-API execution under its runtime rules, but does not establish an application-level invariant. Thread switching, blocking-operation GIL release, extension behavior, and free-threaded builds all matter. Do not require a particular `count += 1` race outcome.

---

## 22. Candidate Machine-Checkable vs. Reviewer-Required Evidence

### 22.1 Machine-Checkable Evidence (Automated Tests & Graders)
1. **Query Plan Verification (M13):**
   - Automated parser checks `EXPLAIN QUERY PLAN` output for expected tokens: `SCAN` on unindexed queries, `SEARCH ... USING INDEX` on indexed queries.
   - Assert result-set identity: $\text{Result}(\text{Indexed}) == \text{Result}(\text{Unindexed})$.
2. **Transaction Isolation & Invariant Verification (M14):**
   - Execute two concurrent connections; assert that Connection 2 cannot observe uncommitted writes from Connection 1.
   - Assert the **fixture-defined conflict contract** using SQLite result codes/transaction state and record the actual Python exception/message if one occurs; do not require a fixed `database is locked` string across versions/configurations.
   - Terminate child process mid-transaction; assert that post-crash state preserves original invariant: `balance_a + balance_b == 1000`.
3. **Atomic Race & Mutex Repair Verification (M15):**
   - Run the broken atomic compound counter under a bounded attempt budget; PASS requires preserving at least one actual lost-update trace on the accepted environment, not a fixed percentage or count range.
   - Run the mutex-protected counter; every completed repaired run must satisfy the declared target-count invariant.
   - Execute condition-variable rendezvous; assert that consumer never executes before producer sets payload.
   - Execute the bounded deadlock/progress fixture under an owned-child watchdog. If Design uses a coordinated “each thread holds its first lock” handshake, record that precondition before interpreting a timeout as deadlock evidence. The configured timeout is a harness parameter, not a ≤3-second curriculum law.

### 22.2 Reviewer-Required Evidence (Pedagogical & Conceptual Judgment)
1. **Workload Justification (M13):**
   - Reviewer audits learner's written explanation of when a table scan is preferred over an index, ensuring the learner did not rely on generic "index = faster" tropes.
2. **Consistency & Anomaly Classification (M14):**
   - Reviewer validates that learner explicitly qualifies "consistency" with a named guarantee (e.g., Read Committed vs. Serializable) and does not conflate ACID Consistency with distributed consistency.
3. **Concurrency Reasoning (M15):**
   - Reviewer checks the learner's interleaving trace diagram, verifying accurate depiction of shared memory reads, preemptive yields, and overwritten state transitions.

---

## 23. Safety & Cleanup Model

### 23.1 Safety Boundary Enforcements
- **Localhost and Local Files Only:** All databases, threads, and processes are strictly confined to the local filesystem and local memory. Zero public network connections, zero cloud resources, and zero external credentials.
- **Synthetic Data Exclusively:** All lab fixtures operate strictly on procedurally generated synthetic records (e.g., `user1`, `amount=100.0`). Zero personal or sensitive data.
- **No Privileged Operations:** No `sudo`, `root`, or raw kernel capabilities are required for any Required Core lab.
- **No System Stress or Destruction:**
  - Zero filesystem-fill experiments (database file sizes capped at $\le 10\text{ MB}$).
  - Zero power-cut or kernel panic experiments.
  - Zero thread-storm or fork-bomb experiments (thread counts bounded to 2–4 workers).
  - Bounded deadlock experiments: run only in an owned child under a configured watchdog with explicit termination/reaping. The safety harness bounds the course child; it cannot literally guarantee the host/UI can never stall, and the timeout duration is not a curriculum constant.

### 23.2 Cleanup Protocol
Every test script and lab fixture must incorporate deterministic cleanup logic:
- Automatically remove temporary SQLite database files: `<name>.db`, `<name>.db-journal`, `<name>.db-wal`, `<name>.db-shm`.
- Terminate any dangling worker threads or child processes using structured `try...finally` blocks or context managers.
- Remove temporary compiled C binaries (`.exe` / `.out`) from scratch directories upon completion.

---

## 24. Design Handoff Requirements

The subsequent Design pass (`meta/design/data-concurrency-m13-m15-design-v0.1.md`) must establish the following without guessing:

1. **Lesson Plan Architecture:**
   - Detail the 9 canonical preliminary lessons (`L13-01` through `L13-03`, `L14-01` through `L14-03`, `L15-01` through `L15-03`).
   - Anchor `L14-02` as the canonical first home of `EC-CON-014 Consistency`, providing explicit disambiguation between ACID consistency and transaction ordering/visibility guarantees.
   - Anchor `L15-01` as the canonical first home of `EC-CON-015 Concurrency`, establishing the distinction between logical interleaving and physical parallelism.
   - Structure `L13-03` around the R6 application patterns (schema evolution, reader/writer compatibility, migration trade-offs, source of truth vs. derived data, lightweight provenance) under existing concepts without introducing new IDs.
2. **Lab Fixture Specifications:**
   - **LAB-REQ-04:** Specify a bounded deterministic schema/data generator and EQP inspection harness, but choose fixture sizes from implementation smoke rather than canonizing “100 vs 50,000 rows”. Tests must accept truthful planner choices and assert semantic evidence/result equivalence rather than exact text or timing.
   - **LAB-REQ-05:** Specify the dual-connection runner, invariant verification, journal-mode declaration, bounded second-writer/conflict evidence, owned-child interruption/reaping, reopen evidence, and backup/restore boundary without fixed exception text.
   - **LAB-REQ-03:** Specify a C11-compatible source using atomic accesses for the broken compound transition, mutex repair, condition-variable predicate loop, and owned-child watchdog. If the natural scheduler path is unreliable, add a bounded course-controlled phase handoff rather than a probability threshold.
3. **Optional Content & Source Expedition Guidelines:**
   - Specify `LAB-OPT-03` as an optional Docker/local comparison module.
   - Define `LAB-OPT-05` as a link-only guide to OSTEP `threads-sema`.
   - Bounded EXP-02 instructions must preserve the three canonical paths while explicitly noting that `plan/README` no longer serves as the current general Path→Plan overview. If the parent `src/backend/optimizer/README` is added to the learner route, treat that as an explicit Lead source-selection adjustment. No PostgreSQL compilation is required.

---

## 25. Open Risks & Open Question Interactions

1. **OQ-BP-001 (Bounded AI Literacy) & OQ-BP-003 (Human-Facing Systems):**
   - Both open questions remain **OPEN** and RFC-gated.
   - S5 does not require Core-scope expansion for AI or HCI. AI code verification (e.g., verifying AI-generated SQL queries or multi-threaded code against races) is treated as standard technical literacy practice without modifying Core architecture.
2. **OQ-BP-006 (Environment and Version Pinning):**
   - Remains **OPEN**. Separate **Agent-host observations** (Python 3.13.1 / embedded SQLite 3.45.3 / GCC 14.2) from **2026-09-04 upstream currentness** (Python 3.14.7 / SQLite 3.53.4 / PostgreSQL 18.6 / POSIX Issue 8 / ISO C23). None is a permanent curriculum pin.
3. **M03 GDB Debt & M06 Grader Debt:**
   - Historical debt (M03 GDB runtime debt, M06 MIT course-fork grader not run) remains explicit and non-blocking under D-027. S5 does not depend on M06's external grader.
4. **Filesystem / VFS Locking Sensitivity:**
   - SQLite concurrency semantics depend on the selected VFS and filesystem locking behavior.
   - Remote/network filesystems have implementation- and configuration-specific locking semantics; Research does not classify all NFS/SMB mounts as broken.
   - Design must use a course-owned local writable directory on the accepted environment and record the actual location/VFS capability. Do not require the literal path `/tmp` on every platform.
5. **EXP-02 source-route drift:**
   - The canonical Target 1 path still exists, but its current content does not provide the high-level planner architecture the Blueprint description expected.
   - This is a **non-blocking source-selection risk for Design**, not permission for Research to silently replace the route. The Design pass must either use Target 1 for what it actually contains or explicitly route a source adjustment through Lead review.
6. **Scheduler-dependent race manifestation:**
   - The UB-free atomic compound update is sound as a mechanism, but `sched_yield()` alone does not guarantee a lost-update observation on every environment.
   - Design must establish a bounded evidence strategy (attempt budget or controlled phase handoff) before implementation acceptance.

---

## 26. Final Recommendation

**READY FOR DESIGN**

The research foundation for Stage 5 is **READY FOR DESIGN with explicit non-blocking research risks carried forward**: EXP-02 Target 1 source-route drift, scheduler-dependent race manifestation, environment/version pinning, and Optional OSTEP rights. These do not require a Core architecture change before Design, but Design must resolve them into truthful learner/evidence contracts rather than erase them.
