# Data & Concurrency (M13–M15) Design Dossier v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #86 — [Design] M13–M15 Data & Concurrency Design Dossier v0.1
Repository state designed: `main @ 5edb6f8eb7bba14437327f7195c0f03cdf1b5226`
Research authority: `research/data-concurrency-m13-m15-v0.1.md @ 4c47e74a7d8c5d4ba17416f8ac364bcd087faba2`
Design Date: **2026-09-04**
Role: Design Agent — Curriculum Architecture, Learner Contract, Lab Contract, and Evidence Contract Designer for Stage 5
Scope: Design step only; no learner Lesson files, runnable Lab code implementations, Source Expedition learner guides, Concept Registry edits, Blueprint edits, or Open Question closures.

---

## 1. Executive Design Decision & Readiness

**Recommendation: READY FOR LESSON / ACTIVITY IMPLEMENTATION**

This Design Dossier establishes the complete pedagogical, technical, experimental, and verification contract for Stage 5 (S5) Data & Concurrency:

$$\text{M13 (Databases: Storage \& Indexing)} \longrightarrow \text{M14 (Databases: Transactions, Recovery \& Isolation)}$$

and the structurally decoupled concurrency branch:

$$\text{M15 (Concurrency: Threads, Races \& Synchronization)}$$

### Key Design Commitments

1. **Strict DAG & Module Decoupling Preserved:**
   - M13 hard prerequisites: `M08` (Filesystems) + `M09` (Storage Engines & Durability); soft/preferred `M04` (Hardware Cache & Locality).
   - M14 hard prerequisites: `M13` + `M09`; soft/preferred none.
   - M15 hard prerequisite: `M06` (OS Kernel & Processes); soft/preferred `M14` + `M03` + `M12`.
   - **M14 $\leftrightarrow$ M15 is not a hard DAG edge.** Concurrency in M15 does not assume database transaction mastery; transaction isolation in M14 does not assume C pthread synchronization mastery. S4 (M10–M12) is not a hard prerequisite for S5.
2. **Concept Registry & Canonical First-Home Protection:**
   - **Zero new concept IDs introduced.** All concepts remain strictly within the 18 canonical entries in `meta/CONCEPT_REGISTRY.md`.
   - **EC-CON-014 Consistency (一致性)** enters its canonical first home in **M14 (`L14-02`)**. Exact canonical definition: **“The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee.”** The qualifier mandate is enforced separately: It must be qualified; "consistent" does not mean merely fresh, durable, or correct in every sense. ACID "Consistency" is explicitly disambiguated as application invariant preservation rather than an engine-level visibility contract. SQLite's declared visibility behavior is treated under its own engine locking/journal contract, not labeled as generic ANSI Read Committed.
   - **EC-CON-015 Concurrency (并发)** enters its canonical first home in **M15 (`L15-01`)**. Exact canonical definition: **“Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations.”** Concurrency is fundamentally distinguished from physical parallelism. M12's event loop and M14's transaction overlap are treated strictly as previews.
   - **R6 Schema Evolution & Provenance:** Handled in M13 `L13-03` as an **application pattern** spanning existing concepts (`EC-CON-001`, `003`, `005`, `008`). No new concept ID is created.
   - **Concept Revisit Alignment:** In accordance with the canonical Concept Registry contract, `EC-CON-018 Process` is not an authorized canonical revisit in M15 (its first home is M06); thread-vs-process comparisons remain pedagogical context without claiming an unapproved Concept Registry revisit.
3. **Lab & Source Expedition Contracts:**
   - **LAB-REQ-04 (SQLite Query Plans & Indexing):** Required baseline is the `sqlite3` CLI. Python stdlib `sqlite3` is permitted for fixture generation and automated evaluation, but is not an equivalent interactive replacement. If `sqlite3` CLI is absent, the learner path is classified `ENVIRONMENT-BLOCKED / NOT RUN`. Fixture sizes are determined by implementation smoke test (e.g. smaller baseline vs. larger multi-page workload), rejecting hardcoded row/page constants. Truthful planner scans on smaller fixtures or low selectivity are explicitly accepted and celebrated; tests do not force `SEARCH ... USING INDEX`. DB file size is an empirical observation and must not be machine-asserted as inevitably increasing.
   - **LAB-REQ-05 (SQLite Transactions & Recovery):** Required baseline is local SQLite with **rollback journal** (`DELETE` mode). WAL mode is an optional comparison. Dual-connection architecture verifies committed-only visibility and writer/lock-upgrade conflicts without fixed exception string matching. Child process termination via `SIGKILL` tests client crash recovery; Design strictly prohibits inferring physical power-loss durability from process interruption.
   - **LAB-REQ-03 (POSIX Threads Race & Rendezvous):** Required baseline is C11 + POSIX threads on canonical Linux. The broken path uses C11 atomics (`<stdatomic.h>`) for defined atomic accesses in a compound read-modify-write update, avoiding C language data race / Undefined Behavior (UB). Preferred evidence utilizes course-controlled phase handoff / barrier coordination to produce real pthread lost-update interleaving without simulating threads; natural scheduler observation is supplemental only and truthfully bounded by an attempt budget, rejecting fixed percentage assertions ($\ge 95\%$) or fixed count ranges. Mutex repair, condition-variable predicate loop, and an owned-child deadlock watchdog with a configurable timeout parameter are fully specified without absolute shell-freeze promises.
   - **LAB-OPT-03 (PostgreSQL EXPLAIN & Isolation):** Strictly Optional. Requires explicit rollback design for `EXPLAIN ANALYZE` mutation statements. PostgreSQL/Docker must never become hidden Core requirements.
   - **LAB-OPT-05 (OSTEP Semaphore Rendezvous):** Strictly Optional and **link-only** (commit `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`). Zero bundled code, tests, or skeletons.
   - **EXP-02 (PostgreSQL Source Expedition):** Preserves the exact three canonical paths (`src/backend/optimizer/plan/README`, `src/backend/optimizer/path/costsize.c`, `src/backend/storage/buffer/README`). The learner-facing card explicitly documents Target 1's historical subselect drift. The parent `optimizer/README` is cited as supplemental reviewer context, not a substitute or fourth canonical step. No PostgreSQL compilation.
4. **Environment & OQ-BP-006 Preservation:**
   - Preflight contract classifies capabilities across 14 explicit dimensions into Required, Optional, Environment-Sensitive, and Privileged.
   - OQ-BP-006 remains explicitly **OPEN**. Current tool versions are treated as empirical observations, not permanent curriculum constants.

---

## 2. Canonical Constraints & DAG Architecture

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

### Module Prerequisites & Ordering

| Module | Hard Prerequisites | Soft / Preferred Prerequisites | Canonical First Home | Primary Competency |
|---|---|---|---|---|
| **M13** | `M08`, `M09` | `M04` | None | **Observe** |
| **M14** | `M13`, `M09` | None | **EC-CON-014 Consistency (L14-02)** | **Correctness** |
| **M15** | `M06` | `M14`, `M03`, `M12` | **EC-CON-015 Concurrency (L15-01)** | **Diagnose** |

**Prohibited DAG Additions:**
- `M12` is NOT a hard prerequisite for `M15`.
- `M14` is NOT a hard prerequisite for `M15`.
- `LAB-REQ-03` is NOT a prerequisite for `M14`.
- `LAB-REQ-05` is NOT a prerequisite for `M15`.
- PostgreSQL and Docker are NOT prerequisites for any Required Module.

---

## 3. Research Findings Adopted, Rejected & Bounded

| Item / Finding | Research Dossier Status | Design Pass Disposition | Hard Design Boundary Enforced |
|---|---|---|---|
| **EXP-02 Target 1 Drift** | Target 1 (`plan/README`) is largely historical subselect notes; does not describe general Path $\to$ Plan. | **Adopted with boundary** | Preserve Target 1; document historical drift on the learner card; cite parent `optimizer/README` as supplemental support only. Do NOT replace Target 1. |
| **LAB-REQ-03 Scheduling** | `sched_yield()` alone does not guarantee a lost-update observation across all OS schedulers. | **Adopted with boundary** | Preferred evidence uses course-controlled phase handoff / barrier coordination; natural scheduler observation is supplemental under an attempt budget. Reject hardcoded "$\ge 95\%$" or "100%" occurrence assertions and fixed count ranges. |
| **LAB-REQ-04 Dataset Sizes** | Bounded fixture sizes must be chosen from implementation smoke, not canonized constants. | **Adopted** | Specify smaller baseline vs. larger multi-page workload determined by smoke test; do not canonize specific row counts or page counts. |
| **LAB-REQ-04 Plan Choice** | Query planner choice is cost- and workload-dependent. | **Adopted** | Tests must accept truthful planner scan choices on small tables or low selectivity; do not force `SEARCH ... USING INDEX`. File size is an observation, not machine-asserted. |
| **LAB-REQ-04 CLI Baseline** | `sqlite3` CLI is required for authentic plan and tool interaction. | **Adopted** | Missing CLI = `ENVIRONMENT-BLOCKED / NOT RUN`. Python is not an interactive substitute. |
| **LAB-REQ-05 Baseline** | Rollback journal is SQLite default; WAL is optional comparison. | **Adopted** | Establish rollback journal (`DELETE`) as default; WAL as bounded extension. No fixed exception string matching. |
| **Process Interruption** | `SIGKILL` tests client abnormal termination, not hardware power loss. | **Adopted** | Explicit inference boundary: Process kill $\ne$ power loss. |
| **L15-03 Python GIL** | Free-threaded Python 3.14 / PEP 779 in supported phase II; conventional GIL build common. | **Adopted** | Do not teach GIL as a Python language invariant or `counter += 1` as guaranteed to fail; observe named runtime capability. |
| **OQ-BP-006 Versions** | Agent host vs. upstream currentness separated; neither is a pin. | **Adopted** | OQ-BP-006 remains **OPEN**. Current versions recorded as evidence only. |

---

## 4. S5 Implementation Batching

Implementation must proceed in three independent, bounded batches:

```
Batch 1: S5-B1 (M13 Core)
+-----------------------------------------------------------------------------------+
| M13 Lessons (L13-01, L13-02, L13-03)                                              |
| LAB-REQ-04 (SQLite Query Plans, Indexing & Workload Evidence)                     |
| EXP-02 (PostgreSQL Planner & Buffer Source Expedition)                            |
+-----------------------------------------------------------------------------------+
                                  |
                                  v
Batch 2: S5-B2 (M14 Core)
+-----------------------------------------------------------------------------------+
| M14 Lessons (L14-01, L14-02, L14-03) [EC-CON-014 Consistency First Home]          |
| LAB-REQ-05 (SQLite Transactions, Isolation, Rollback & Recovery Boundary)         |
| LAB-OPT-03 (PostgreSQL EXPLAIN & Isolation Comparison - Optional)                 |
+-----------------------------------------------------------------------------------+
                                  |
                                  v
Batch 3: S5-B3 (M15 Core)
+-----------------------------------------------------------------------------------+
| M15 Lessons (L15-01, L15-02, L15-03) [EC-CON-015 Concurrency First Home]          |
| LAB-REQ-03 (POSIX Threads Race, Rendezvous & Progress Boundaries)                 |
| LAB-OPT-05 (OSTEP Semaphore Rendezvous - Optional Link-Only)                      |
+-----------------------------------------------------------------------------------+
```

---

## 5. Module M13 Architecture — Databases: Storage & Indexing

- **Module Purpose:** Establish the mental model of a database engine: declarative SQL $\to$ engine parser/planner/code generator in a named engine $\to$ access path $\to$ page/cache/storage work $\to$ result set. Unpack the trade-offs of B-tree indexing and schema invariants without claiming universal pipeline or node structures.
- **Primary Competency:** **Observe** (query execution plans, access paths, storage footprint observations, timing distributions).
- **Secondary Competencies:** Trace, Explain, Estimate, Judge, Correctness.
- **Canonical Concepts Revisit:** `EC-CON-001 State`, `EC-CON-003 Representation`, `EC-CON-005 Interface`, `EC-CON-006 Trade-off`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`, `EC-CON-011 Caching`, `EC-CON-012 Locality`.
- **Application Pattern:** Schema evolution, reader/writer compatibility, migration trade-offs, source of truth vs. derived data, lightweight provenance (R6).

---

## 6. Lesson L13-01 Design — “Why is my query fast/slow?”

### 6.1 Learner Question & Capability Transition
- **Learner Question:** "Why does the exact same `SELECT` statement run quickly on some tables, but take noticeably longer on others—and why does adding an index sometimes make no difference at all?"
- **Capability Transition:** Moves from treating a database as a black box where queries have mysterious speeds to inspecting the engine's access path (`EXPLAIN QUERY PLAN`), understanding page-level I/O, and evaluating B-tree index trade-offs.

### 6.2 Mechanism Model & Claim Layer
- **Mechanism:** Tables are stored on disk as structured pages managed by the database engine. A full table scan reads pages sequentially. A B-tree index stores keys and row pointers in balanced multi-way tree pages; lookups probe root through internal nodes down to leaf pages. Plan choice is cost- and workload-dependent: when a query matches a large fraction of table rows or when the table is small enough that scanning pages sequentially costs less than index traversal plus scattered page lookups, the optimizer chooses a scan.
- **Claim Layers:**
  - *PRINCIPLE:* Tree lookup ($O(\log N)$ access steps) vs. linear scan ($O(N)$ access steps); random vs. sequential page access trade-off; index maintenance cost on data mutations.
  - *SPECIFICATION:* SQL declarative semantics specify the result set, not the retrieval path.
  - *IMPLEMENTATION:* SQLite query planner cost estimation heuristics; `EXPLAIN QUERY PLAN` semantic output (`SCAN`, `SEARCH ... USING INDEX`, `USING COVERING INDEX`).
  - *CURRENT PRACTICE:* Default engine page allocations; automatic index generation heuristics in specific CLI or embedded environments.

### 6.3 Hands-On Activity & Controlled Failure
- **Activity:** In the `sqlite3` CLI, load a synthetic table across bounded scales selected by implementation smoke. Execute queries on indexed vs. unindexed columns. Capture `EXPLAIN QUERY PLAN`.
- **Prediction Before Observation:** Before running `EXPLAIN QUERY PLAN`, learner must predict whether the engine will choose a table scan or an index lookup based on table size and predicate selectivity.
- **Controlled Break:** Execute a query with lower selectivity or a modified query shape where SQLite chooses `SCAN TABLE` despite an available index. Observe and document this authentic planner choice: Traversing the index to fetch scattered rows incurs higher estimated cost than scanning pages sequentially.

### 6.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Adding an index always makes queries faster."* (False: On small tables or low selectivity, indexes add overhead; indexes always add maintenance overhead to insertions and updates).
  2. *"`EXPLAIN QUERY PLAN` executes the query and measures actual run time."* (False: EQP displays the optimizer's estimated plan without executing the query).
  3. *"The database page size or B-tree node shape is universal across all systems."* (False: Page sizes, branching factors, and page formats are named-engine implementation choices).
- **What You Can Ignore — For Now:** Internal B-tree page balancing and page-split algorithms; VDBE bytecode opcodes; LSM-trees; bitmap index structures.

### 6.5 Progressive Support Ladder
- **Question:** How do you determine whether SQLite will use an index for `SELECT * FROM orders WHERE user_id = 42`?
- **Hint 1:** The declarative query does not state how rows are fetched. You need to inspect the engine's chosen access path.
- **Hint 2:** Prefix the query with `EXPLAIN QUERY PLAN` in the `sqlite3` shell.
- **Expected Observation:** The detail column reports a semantic access path such as `SEARCH orders USING INDEX ...` or `SCAN orders`.
- **Full Explanation:** SQLite's planner evaluates available access paths. If an index exists and selectivity justifies it, EQP outputs an index search detail. If no index exists or scanning is estimated to be cheaper, it outputs `SCAN orders`.

### 6.6 Visual Specification & Exit Criteria
- **Visual:** Diagram showing a declarative SQL query entering the query engine, branching into two possible access paths: Path A (Sequential Page Scan visiting physical table pages) vs. Path B (B-Tree traversal visiting Root $\to$ Internal $\to$ Leaf $\to$ Data Page). Prominently labeled: **PLAN CHOICE IS WORKLOAD AND IMPLEMENTATION DEPENDENT**.
- **Exit Criteria:** Learner captures an actual CLI EQP output showing observed access paths (e.g. `SCAN` or `SEARCH ... USING INDEX`), and writes an evidence-based explanation of why an index is not a universal performance solution.

### 6.7 Lesson Contract Audit
- **Canonical Competencies:** `Explain`, `Observe`, `Estimate`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-001 State`, `EC-CON-005 Interface`, `EC-CON-006 Trade-off`, `EC-CON-011 Caching`.
- **Learner Evidence:** Verbatim CLI capture of `EXPLAIN QUERY PLAN` showing observed access paths (`SCAN` or `SEARCH ... USING INDEX`) on unindexed vs. indexed queries; query elapsed time observations across bounded scales; result row count equivalence ($\Delta = 0$); and a written explanation of the sequential scan vs. index lookup trade-off.
- **Provenance & Currentness:** SQLite Public Domain; official SQLite implementation and documentation as authority; actual CLI/library version is recorded in learner evidence / preflight without implying a permanent version range (OQ-BP-006 remains OPEN).
- **Exact Inference Limits:** Observing `SEARCH ... USING INDEX` on a specific query shape does not prove an index improves overall workload throughput; observing fast execution on an in-memory or operating system cache does not prove disk I/O reduction; single-query timing does not represent multi-client concurrency.

---

## 7. Lesson L13-02 Design — “What is SQL doing?”

### 7.1 Learner Question & Capability Transition
- **Learner Question:** "If SQL only describes what data I want, who decides how to get it, and where is the line between relational logic and storage engine reality?"
- **Capability Transition:** Moves from viewing SQL as an imperative programming language to understanding it as a declarative interface (`EC-CON-005`) backed by a query optimization and execution pipeline in a named engine.

### 7.2 Mechanism Model & Claim Layer
- **Mechanism:** The bounded named-engine model:
  $$\text{SQL intent} \longrightarrow \text{parser/planner/code generation in a named engine} \longrightarrow \text{access path} \longrightarrow \text{page/cache/storage work} \longrightarrow \text{result}$$
  Relational algebra operations: Selection ($\sigma$), Projection ($\pi$), Join ($\bowtie$). The storage engine manages physical pages, record formats (such as slotted pages), and buffer pool caching.
- **Claim Layers:**
  - *PRINCIPLE:* Relational model equivalence; declarative interface abstraction; separation of logical query intent from physical access path.
  - *SPECIFICATION:* ANSI/ISO SQL standard grammar and semantics.
  - *IMPLEMENTATION:* Named engine execution strategies (e.g., SQLite compiles SQL queries into Virtual Database Engine / VDBE bytecode; PostgreSQL parses SQL into parse trees, generates path trees, and produces plan nodes for an executor).
  - *CURRENT PRACTICE:* Engine-specific query preparation interfaces and execution models.
- **Explicit Non-Universal Rule:** Do not teach a universal AST $\to$ logical plan $\to$ physical plan $\to$ Volcano pipeline. Specific pipeline stages and execution paradigms (Volcano iterator, bytecode evaluation, JIT compilation, or vectorized batch execution) are engine-specific implementation models, not universal laws of relational databases.

### 7.3 Hands-On Activity & Controlled Failure
- **Activity:** Query a multi-table SQLite database. Compare an un-sargable query (`WHERE UPPER(username) = 'ALICE'`) with a sargable indexed query (`WHERE username = 'Alice'`).
- **Prediction Before Observation:** Predict whether SQLite can use a standard B-tree index on `username` when wrapped in a function call.
- **Controlled Break:** Observe that wrapping the indexed column in `UPPER(...)` forces a table scan (`SCAN TABLE`), breaking the index abstraction. Explain why: Standard B-tree indexes are ordered by raw column values, not transformed function outputs.

### 7.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"SQL executes in the exact order written (SELECT first, then FROM)."* (False: Logical processing evaluates `FROM` $\to$ `WHERE` $\to$ `GROUP BY` $\to$ `HAVING` $\to$ `SELECT` $\to$ `ORDER BY`).
  2. *"Every relational database uses the same query compilation pipeline and Volcano iterator executor."* (False: Different engines compile to bytecode, interpreted trees, or native machine code; execution models range from Volcano iterators to vectorized batch processing).
- **What You Can Ignore — For Now:** Cost-based join order dynamic programming (Selinger optimizer); VDBE register allocation details; cost-model tuning parameters.

### 7.5 Progressive Support Ladder
- **Question:** Why does `SELECT * FROM users WHERE id + 1 = 100` fail to use the primary key index on `id`?
- **Hint 1:** Look at the predicate on the column. Is `id` an isolated term?
- **Hint 2:** The query planner matches expressions. It does not perform algebraic inversion to rewrite `id + 1 = 100` into `id = 99`.
- **Expected Observation:** EQP displays a table scan access path instead of an index search on the primary key.
- **Full Explanation:** Expressions on indexed columns prevent index access unless an expression-specific index exists. Rewriting the predicate to `WHERE id = 99` allows the optimizer to utilize the primary key index.

### 7.6 Visual Specification & Exit Criteria
- **Visual:** Two-layer architectural diagram. Top Layer: SQL Declarative Contract (`SELECT`, `FROM`, `WHERE` relational intent). Bottom Layer: Named Engine Implementation (Parser/Planner/Code Generator $\to$ Physical Access Path $\to$ Storage Engine / Page Cache). Shows the abstraction boundary and how expression predicates leak through to force full scans.
- **Exit Criteria:** Learner traces one query through logical intent vs. physical access path in a named engine and explains the performance difference between a sargable and non-sargable predicate.

### 7.7 Lesson Contract Audit
- **Canonical Competencies:** `Trace`, `Explain`, `Judge`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-003 Representation`, `EC-CON-005 Interface`, `EC-CON-006 Trade-off`, `EC-CON-012 Locality`.
- **Learner Evidence:** CLI trace of EQP showing a sargable predicate (`WHERE username = 'Alice'`) utilizing index search vs. a non-sargable expression predicate (`WHERE UPPER(username) = 'ALICE'`) forcing a table scan; written evaluation explaining why expression evaluation breaks the index abstraction layer.
- **Provenance & Currentness:** ANSI SQL-92 declarative grammar; SQLite VDBE compiler model vs. PostgreSQL parser/planner/executor model.
- **Exact Inference Limits:** Demonstrating that an expression on an indexed column prevents index utilization in SQLite does not prove that all relational engines lack expression indexing; functional/expression indexes exist in some engines as an explicit DDL feature.

---

## 8. Lesson L13-03 Design — “Why do my schema choices matter?”

### 8.1 Learner Question & Capability Transition
- **Learner Question:** "How do I change a database schema in production without corrupting existing data, locking up the system, or breaking older versions of my application?"
- **Capability Transition:** Moves from treating schema design as static table creation to mastering schema invariants, evolution trade-offs, reader/writer compatibility, and source-of-truth vs. derived data.

### 8.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *Schema Invariants (`EC-CON-008`):* Enforced by DBMS constraints (`PRIMARY KEY`, `NOT NULL`, `CHECK`, `UNIQUE`, `FOREIGN KEY`).
  - *Schema Evolution & Compatibility:* Backward compatibility (new code can read data written by old code); Forward compatibility (old code can read data written by new code).
  - *Expand-Contract Pattern:* Step 1 (Expand): Add new nullable column / dual-write; Step 2 (Backfill): Populate historical data; Step 3 (Contract): Switch readers to new column and deprecate old column.
  - *Source-of-Truth vs. Derived Data:* Authoritative operational state vs. derived views or cached aggregates. In the bounded course application pattern (R6), a derived view is defined to be intentionally recomputable from the named source-of-truth table plus declared transformation and provenance inputs (preserving the no-new-concept-ID boundary).
  - *Lightweight Provenance:* Storing metadata (`created_at`, `updated_by`, `schema_version`) to track state lineage.
- **Claim Layers:**
  - *PRINCIPLE:* Invariant preservation across state transitions; trade-offs of redundancy (normalization vs. denormalization); expand-contract migration lifecycle.
  - *SPECIFICATION:* SQL DDL constraint definitions (`ALTER TABLE`).
  - *IMPLEMENTATION:* SQLite `ALTER TABLE` capabilities and limitations across versions.
  - *CURRENT PRACTICE:* Online schema migration patterns and tools in operational environments.

### 8.3 Hands-On Activity & Controlled Failure
- **Activity:** Design a user account schema. Add a new required field (`email_verified BOOLEAN NOT NULL`) to an existing populated table.
- **Prediction Before Observation:** Predict what happens when you execute `ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL;` on a table with existing rows without specifying a default value.
- **Controlled Break:** SQLite returns an error indicating that a `NOT NULL` column cannot be added without a default value. Explain the failure: Adding a non-nullable column to existing data violates the table's invariant for historical rows unless a default or backfill is provided.

### 8.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Schema migrations can always be performed instantly with a single ALTER TABLE."* (False: On large tables or older systems, schema changes can trigger table rewrites and exclusive locks).
  2. *"Derived data is just as authoritative as source-of-truth data."* (False: Derived data can become stale or inconsistent; only source-of-truth state is canonical).
- **What You Can Ignore — For Now:** Distributed schema registries (Avro/Protobuf); W3C PROV-O semantic ontologies; enterprise ETL data pipelines; NoSQL document schema design.

### 8.5 Progressive Support Ladder
- **Question:** How do you safely add a non-nullable `status` column to a populated table without migration errors?
- **Hint 1:** Existing rows must satisfy the `NOT NULL` constraint immediately upon column creation.
- **Hint 2:** Provide a sensible default value in the `ALTER TABLE` statement.
- **Expected Observation:** `ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'ACTIVE';` succeeds.
- **Full Explanation:** Supplying `DEFAULT 'ACTIVE'` allows the engine to satisfy the invariant for all existing rows without requiring immediate table rebuilds in metadata-only evolution engines.

### 8.6 Visual Specification & Exit Criteria
- **Visual:** Schema Evolution Lifecycle diagram showing Version $N$ migrating to Version $N+1$ across three stages: Stage 1 (Expand: Add new nullable column, application dual-writes), Stage 2 (Backfill: Batch update historical rows), Stage 3 (Contract: Readers consume new column, old column dropped). Includes a sidecar showing Source-of-Truth table feeding a Derived View with a Provenance timestamp.
- **Exit Criteria:** Learner designs a multi-step migration script that adds a new column, backfills historical data, and demonstrates backward reader compatibility.

### 8.7 Lesson Contract Audit
- **Canonical Competencies:** `Correctness`, `Judge`, `Diagnose`, `Learn-New-Tech`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-001 State`, `EC-CON-003 Representation`, `EC-CON-005 Interface`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness` (R6 Schema Evolution & Provenance application pattern; no new concept ID).
- **Learner Evidence:** DDL migration script executing the expand-contract pattern: (1) schema change adding nullable/default column, (2) backfill update populating historical rows, (3) reader query validation; plus definition of a bounded derived view intentionally recomputed from the named source-of-truth data plus declared transformation/provenance inputs (`created_at`, `schema_version`).
- **Provenance & Currentness:** SQL DDL specification; SQLite `ALTER TABLE` table-rewrite vs. metadata-only evolution capabilities across versions.
- **Exact Inference Limits:** The expand-contract pattern guarantees backward compatibility for application readers across transitions, but does not eliminate concurrency serialization conflicts or the operational cost of large-table backfills. Bounded derived data is recomputable only when the transformation and source-of-truth data are fully preserved.

---

## 9. Required Lab LAB-REQ-04 Design — SQLite Query Plans, Indexing & Workload Evidence

### 9.1 Overview & Required Baseline
- **Lab ID:** `LAB-REQ-04`
- **Module Placement:** M13 Databases: Storage & Indexing
- **Type:** Build — Essential CS original
- **Execution Baseline:** **`sqlite3` CLI is Required**. Python stdlib `sqlite3` is permitted for synthetic fixture generation and automated test verification, but does not replace the learner's interactive CLI inspection.
- **Missing CLI Disposition:** If `sqlite3` CLI is missing on the host, the learner path is classified **`ENVIRONMENT-BLOCKED / NOT RUN`**.

### 9.2 Fixture & Data Generation
- Synthetic dataset: An `orders` table with columns `(id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL, status TEXT, created_at TEXT)`.
- Bounded dataset sizes selected by implementation smoke test (e.g., a smaller baseline fixture vs. a larger multi-page fixture). Do not canonize fixed row counts or page counts.
- Synthetic data generator generates deterministic, pseudo-random records using a fixed seed.

### 9.3 Experimental Procedure
1. **Checkpoint 1 — Baseline & Prediction:**
   - Execute query on unindexed `user_id`: `SELECT * FROM orders WHERE user_id = ?;`
   - Record predicted access path.
   - Run `EXPLAIN QUERY PLAN` in `sqlite3` CLI and capture actual output.
2. **Checkpoint 2 — Index Creation & EQP Inspection:**
   - Create index: `CREATE INDEX idx_orders_user ON orders(user_id);`
   - Run `EXPLAIN QUERY PLAN` for the selective query.
   - Assert semantic access path without forcing an index: If the optimizer chooses an index, record `SEARCH ... USING INDEX`; if the optimizer chooses a scan on a small fixture, accept and record that truthful result. (Do not bind tests to exact ASCII tree formatting).
3. **Checkpoint 3 — Result Equivalence Verification:**
   - Verify that results returned by the indexed query are identical to the unindexed query:
     $$\text{Result}(\text{Query}_{\text{unindexed}}) \equiv \text{Result}(\text{Query}_{\text{indexed}})$$
4. **Checkpoint 4 — Workload Measurement & Trade-offs:**
   - Measure repeated read query execution times (capturing raw timing samples, median, and spread across iterations, explicitly recording warmup and cache state).
   - Observe write overhead: Measure execution time of bulk `INSERT` statements with and without the secondary index.
   - Observe database file size via filesystem stat before and after index creation. (DB file size is an empirical observation and must not be machine-asserted as inevitably increasing).
5. **Checkpoint 5 — Truthful Scan Acceptance:**
   - Execute a query with lower selectivity or a changed workload.
   - If SQLite chooses `SCAN TABLE` despite an available index, record this truthful result and explain why cost estimation preferred sequential I/O.

### 9.4 Machine-Checkable vs. Reviewer-Required Gates
- **Machine-Checkable:**
  - Automated runner executes SQL script;
  - Parses EQP detail string semantically (`SCAN` vs. `SEARCH ... USING INDEX`);
  - Asserts result set equivalence ($\Delta = 0$ rows);
  - Records DB file size observation without machine-asserting a mandatory increase.
- **Reviewer-Required:**
  - Review learner's written justification of the write/space trade-off;
  - Confirm learner did not assert universal "index = faster" claims.

---

## 10. Source Expedition EXP-02 Design — PostgreSQL Planner & Buffer Route

### 10.1 Canonical Inspection Paths & Roles
The three canonical paths from the Curriculum Blueprint are preserved exactly:

1. **Target 1:** `src/backend/optimizer/plan/README`
   - *Current Source Reality:* As established in Research, Target 1 is primarily historical notes on subselect planning, rather than a broad Path $\to$ Plan overview.
   - *Design Contract:* The learner guide **must explicitly document this historical drift**. The learner inspects Target 1 as an authentic lesson in large-codebase evolution: Comments and README files drift over decades.
   - *Supplemental Context:* The parent `src/backend/optimizer/README` is cited in reviewer notes as supplemental context for how the planner operates, but does **not** become a fourth canonical learner inspection step.
2. **Target 2:** `src/backend/optimizer/path/costsize.c`
   - *Current Source Reality:* Active, core cost-estimation routines.
   - *Learner Inspection Point:* Inspect `cost_seqscan()` and `cost_index()`. Observe how disk I/O (page fetches) and CPU cost (tuple processing) are mathematically modeled as weighted cost estimates.
3. **Target 3:** `src/backend/storage/buffer/README`
   - *Current Source Reality:* Authoritative shared buffer pool documentation.
   - *Learner Inspection Point:* Read sections on buffer pool organization, page pinning/unpinning, buffer headers, and the clock-sweep page replacement algorithm.

### 10.2 Bounded Rules & Prohibitions
- **Strictly Link / Inspection Only:** No PostgreSQL compilation, server setup, or database initialization required.
- **Explicit Stopping Point:** Stop after inspecting the cost functions and buffer replacement description; write a two-paragraph summary connecting cost estimates to buffer hits.
- **Prohibited:** Do not attempt to trace a query through the executor; do not inspect index access method internals (GiST/GIN).

---

## 11. Module M14 Architecture — Databases: Transactions, Recovery & Isolation

- **Module Purpose:** Demystify ACID transactions. Establish the transaction as an invariant-preserving state transition. Unpack isolation anomalies, locking vs. MVCC, and the true boundaries of crash recovery.
- **Primary Competency:** **Correctness** (specifying invariants, classifying isolation anomalies, verifying rollback and crash recovery).
- **Secondary Competencies:** Diagnose, Judge, Explain, Trace.
- **Canonical Concept First Home:** **EC-CON-014 Consistency (L14-02)**.
- **Canonical Concepts Revisit:** `EC-CON-001 State`, `EC-CON-006 Trade-off`, `EC-CON-007 Specification`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`, `EC-CON-013 Isolation`, `EC-CON-016 Durability`.

---

## 12. Lesson L14-01 Design — “What is a transaction?”

### 12.1 Learner Question & Capability Transition
- **Learner Question:** "What happens if a program crashes or loses power halfway through transferring money between two accounts, and how does a database make multi-step operations all-or-nothing?"
- **Capability Transition:** Moves from assuming database writes are simple file updates to understanding atomic transaction boundaries, write-ahead logging (WAL), and commit/rollback mechanics.

### 12.2 Mechanism Model & Claim Layer
- **Mechanism:** Transaction boundary (`BEGIN ... COMMIT / ROLLBACK`). Invariant preservation ($S_0 \to S_1$). Atomicity via logging:
  - *Rollback Journal:* Undo logging. Original disk pages are copied to `<db>-journal` before in-place mutation. If a crash occurs, the journal restores pre-transaction pages. On commit, the journal is deleted or invalidated.
  - *Write-Ahead Logging (WAL):* Redo logging. New page versions are appended sequentially to `<db>-wal`. The main database file remains untouched. Checkpoints periodically sync WAL pages back to the database.
- **Claim Layers:**
  - *PRINCIPLE:* Invariant-preserving state transitions; Write-Ahead Logging invariant (log records must reach durable storage before dirty pages reach the database file); Atomicity and Durability failure models.
  - *SPECIFICATION:* SQL-92 transaction control statements (`BEGIN TRANSACTION`, `COMMIT`, `ROLLBACK`).
  - *IMPLEMENTATION:* SQLite rollback journal modes (`DELETE`, `TRUNCATE`, `PERSIST`, `MEMORY`, `WAL`); synchronous pragmas (`FULL`, `NORMAL`, `OFF`).
  - *CURRENT PRACTICE:* Default single-file transaction handling in embedded systems.

### 12.3 Hands-On Activity & Controlled Failure
- **Activity:** Open an SQLite database. Initiate a multi-step financial transfer across two accounts inside `BEGIN TRANSACTION`.
- **Prediction Before Observation:** Predict database state if an explicit `ROLLBACK` is issued after Step 1 but before Step 2.
- **Controlled Break:** Intentionally raise an error between the debit and credit steps, triggering `ROLLBACK`. Query the database and verify that neither account was mutated, preserving the system invariant.

### 12.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Transactions automatically make my business logic correct."* (False: A transaction provides atomicity and isolation; if the application writes flawed numbers inside the transaction, the database commits the flawed numbers).
  2. *"Rollback is the same thing as a backup."* (False: Rollback reverts uncommitted active transaction mutations; backup creates a separate point-in-time copy of committed data).
- **What You Can Ignore — For Now:** ARIES recovery algorithm details (Compensation Log Records / Analysis-Redo-Undo passes); distributed Two-Phase Commit (2PC); hardware non-volatile dual-ported RAM.

### 12.5 Progressive Support Ladder
- **Question:** If your script crashes after subtracting $100 from Account A but before adding $100 to Account B, how does SQLite prevent money from vanishing?
- **Hint 1:** Look at the disk directory while the transaction is open.
- **Hint 2:** SQLite creates a rollback journal file before modifying any database pages.
- **Expected Observation:** The next time any connection opens the database, SQLite detects the incomplete journal and rolls back the partial debit.
- **Full Explanation:** SQLite enforces the WAL/journal invariant: Original pages are preserved on disk. If uncommitted, recovery automatically restores original pages on the next connection open.

### 12.6 Visual Specification & Exit Criteria
- **Visual:** State Transition diagram showing initial state $S_0$ with invariant $\sum = 1000$. Demonstrates Step 1 (Debit A: $\sum = 900$, invariant broken in volatile memory) $\to$ Step 2 (Credit B: $\sum = 1000$, invariant restored). Shows the fork: `COMMIT` (persists state $S_1$) vs. Failure / `ROLLBACK` (journal restores state $S_0$).
- **Exit Criteria:** Learner writes a transaction script that executes a multi-step update, simulates mid-operation failure, and proves that rollback preserves the declared invariant.

### 12.7 Lesson Contract Audit
- **Canonical Competencies:** `Correctness`, `Trace`, `Explain`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-001 State`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`, `EC-CON-016 Durability`.
- **Learner Evidence:** Transaction script execution log demonstrating: (1) baseline invariant balance check, (2) multi-step transfer with simulated failure between steps, (3) explicit `ROLLBACK` execution, (4) post-rollback balance check verifying zero partial state mutation, (5) filesystem directory observation showing creation and removal/invalidation of rollback journal (`<db>-journal`).
- **Provenance & Currentness:** SQL-92 transaction control specification; SQLite rollback journal modes (`DELETE`, `TRUNCATE`, `PERSIST`).
- **Exact Inference Limits:** Demonstrating rollback upon software error or process termination proves application crash recovery, but does not prove power-loss durability against hardware write-cache loss or operating system sync failures.

---

## 13. Lesson L14-02 Design — “Why does concurrent access corrupt data?”

### 13.1 Learner Question & Capability Transition
- **Learner Question:** "If two users update the same database simultaneously, how does their work collide, and what does it actually mean when a system claims to be 'consistent'?"
- **Capability Transition:** Moves from assuming databases automatically isolate concurrent users to diagnosing specific isolation anomalies and anchoring the formal, qualified definition of **EC-CON-014 Consistency**.

### 13.2 Mechanism Model & Claim Layer
- **Mechanism:** Concurrent transaction execution and isolation anomalies:
  - *Dirty Read ($P_1/A_1$):* Reading uncommitted mutations from another transaction that subsequently aborts.
  - *Non-Repeatable Read ($P_2/A_2$):* Re-reading the same row within a transaction and observing mutations committed by another transaction.
  - *Lost Update ($P_4$):* Two transactions read row $X$, compute updates, and overwrite each other, losing one update.
  - *Phantom Read ($P_3/A_3$):* A query reading a range of rows observes new rows inserted and committed by another transaction.
  - *Write Skew ($A5B$):* Transactions concurrently read overlapping data, modify disjoint rows, and commit an outcome violating a cross-row invariant.
  - *Concurrency Control Mechanisms:* Locking (Two-Phase Locking / 2PL: Shared read locks, Exclusive write locks) vs. MVCC (Multi-Version Concurrency Control: Readers do not block writers; writers do not block readers).
- **Claim Layers:**
  - *PRINCIPLE:* Isolation anomaly classifications (Berenson et al. 1995); serializability theory; optimistic vs. pessimistic concurrency control.
  - *SPECIFICATION:* ANSI SQL-92 isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable).
  - *IMPLEMENTATION:* SQLite locking architecture: Single active writer; shared read locks; busy conflict handling; committed-only visibility under its engine locking and journal architecture. (Do not label SQLite's declared visibility behavior as generic ANSI Read Committed).
  - *CURRENT PRACTICE:* Engine default isolation settings across enterprise databases.

### 13.3 Canonical Concept First Home: EC-CON-014 Consistency
- **Exact First Home:** M14 / `L14-02`.
- **Exact Canonical Definition:**
  > **“The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee.”**
- **Mandatory Qualifier Mandate (Written Separately):**
  - The qualifier is mandatory: It must be qualified; "consistent" does not mean merely fresh, durable, or correct in every sense.
- **Disambiguation Mandate in Teaching:**
  - Disambiguate ACID $C$ from systems consistency. ACID "Consistency" is application-level invariant preservation.
  - Transaction consistency is defined by a **named isolation level** (e.g., Serializable guarantees observers see outcomes equivalent to some serial schedule; SQLite provides committed-only visibility where observers do not see uncommitted transitions).
  - Explicitly warn learners: Transaction isolation on a single database node is not distributed consistency (which M17 revisits).

### 13.4 Hands-On Activity & Controlled Failure
- **Activity:** Open two separate terminal sessions with `sqlite3` connecting to the same database. Session 1 begins an immediate transaction and updates a row. Session 2 queries the row.
- **Prediction Before Observation:** Predict whether Session 2 will observe the uncommitted modification made by Session 1.
- **Controlled Break:** Session 2 observes the committed value, proving absence of dirty reads under SQLite's committed-only visibility contract. Session 2 then attempts to execute `BEGIN IMMEDIATE;` and immediately fails with a busy/lock conflict, demonstrating SQLite writer serialization.

### 13.5 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Consistency means data is always up to date and correct."* (False: Consistency must be qualified by a named contract; an observer reading a consistent snapshot under Snapshot Isolation may read valid, non-corrupt historical state).
  2. *"Serializable isolation means the database only executes one query at a time."* (False: Engines execute transactions concurrently, intervening only when conflicting interleavings threaten equivalence to a serial schedule).
- **What You Can Ignore — For Now:** Serializable Snapshot Isolation (SSI) dependency graph cycle detection; distributed consensus protocols (Raft/Paxos); cross-shard distributed transactions.

### 13.6 Progressive Support Ladder
- **Question:** If Connection 1 has an uncommitted update, why doesn't Connection 2 see the new value?
- **Hint 1:** What visibility contract does SQLite enforce by default?
- **Hint 2:** SQLite enforces committed-only visibility; uncommitted changes in the journal or WAL are invisible to other connections.
- **Expected Observation:** Connection 2's `SELECT` returns the original value until Connection 1 commits.
- **Full Explanation:** SQLite prevents Dirty Reads ($P_1$). Under its declared visibility guarantee, observers only see committed state transitions.

### 13.7 Visual Specification & Exit Criteria
- **Visual:** Timeline interleaving diagram comparing Connection 1 ($T_1$) and Connection 2 ($T_2$). Displays $T_1$ modifying Row A, $T_2$ reading Row A (observing original committed value under committed-only visibility), and $T_2$ attempting to write (blocked by exclusive lock). Prominently displays the exact one-sentence definition of **EC-CON-014 Consistency** along with its mandatory named qualifier.
- **Exit Criteria:** Learner reproduces a concurrent conflict across two connections, correctly identifies the prevented anomaly, and states `EC-CON-014 Consistency` with its required qualifier.

### 13.8 Lesson Contract Audit
- **Canonical Competencies:** `Diagnose`, `Judge`, `Correctness`.
- **Concepts & Revisits:** **EC-CON-014 Consistency (First Home)**; canonical revisits `EC-CON-006 Trade-off`, `EC-CON-007 Specification`, `EC-CON-008 Invariant`, `EC-CON-013 Isolation`.
- **Learner Evidence:** Dual-connection CLI log showing: Session 1 holding an active uncommitted write; Session 2 executing `SELECT` and observing only committed data (verifying absence of dirty reads under SQLite's committed-only visibility guarantee); Session 2 attempting write access and failing with busy conflict; verbatim recitation of `EC-CON-014 Consistency` with its mandatory named qualifier.
- **Provenance & Currentness:** ANSI SQL-92 isolation levels; Berenson et al. 1995 anomaly taxonomy; SQLite locking and journal visibility model.
- **Exact Inference Limits:** Committed-only visibility prevents dirty reads, but does not prevent non-repeatable reads, phantom reads, or write skew under concurrent interleavings. Single-node transaction consistency does not guarantee distributed linearizability or cross-datacenter consistency.

---

## 14. Lesson L14-03 Design — “How do I design an atomic write?”

### 14.1 Learner Question & Capability Transition
- **Learner Question:** "When multiple processes write to a database, how do I design write operations that handle lock conflicts, avoid lock-upgrade collisions, and remain safe against retries?"
- **Capability Transition:** Moves from writing naive single-statement queries to designing robust, retryable transactional write operations with conflict awareness and idempotency previews.

### 14.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *Atomic Single-Statement vs. Multi-Statement Transactions:* Using atomic expressions (`UPDATE inventory SET stock = stock - 1 WHERE id = 10 AND stock > 0;`) vs. multi-step transactions (`BEGIN IMMEDIATE ... COMMIT`).
  - *Conflict Handling & Appropriate Transaction Boundary Retries:* Handling writer/lock-upgrade conflicts. When a write conflict occurs, retry must restart from an **appropriate transaction boundary** (where state is refreshed). Do not teach that any statement failure unconditionally requires a whole-transaction retry (e.g., parameter or constraint errors do not require blind retries).
  - *Lock-Upgrade Conflicts:* Under the declared SQLite rollback-journal baseline, locking transitions through engine-specific lock states (`SHARED`, `RESERVED`, `EXCLUSIVE`). Note that these lock states are **SQLite rollback-journal locking implementation details under the declared baseline**, not universal transaction semantics and not WAL-mode behavior. `BEGIN DEFERRED` defers starting the actual transaction until the first database access. If the first access is a `SELECT`, a read transaction begins (acquiring a shared lock under rollback-journal mode). A later write statement attempts to upgrade that read transaction to a write transaction (attempting to acquire a reserved lock). If another connection has already acquired a reserved lock, the upgrade attempt cannot proceed and returns a busy conflict (`SQLITE_BUSY`). SQLite does not run a general wait-for-graph cycle detector; deadlock is kept strictly conceptual/light here, with the deterministic deadlock evidence contract residing in M15. The learner must record the actual SQLite result code and driver disposition.
  - *Idempotency Preview:* Ensuring that re-executing a transaction (e.g., following a transient conflict or network retry) does not duplicate state mutations (using unique transaction tokens or idempotency keys).
- **Claim Layers:**
  - *PRINCIPLE:* Atomic state transitions; conflict preconditions; idempotency invariant ($f(f(x)) = f(x)$); transaction retry boundaries.
  - *SPECIFICATION:* SQL transaction retry and conflict error specifications.
  - *IMPLEMENTATION:* SQLite busy handler timeout (`sqlite3_busy_timeout`); `BEGIN DEFERRED` vs. `BEGIN IMMEDIATE` vs. `BEGIN EXCLUSIVE`; actual SQLite result codes and driver dispositions.
  - *CURRENT PRACTICE:* Exponential backoff with jitter in application retry loops.

### 14.3 Hands-On Activity & Controlled Failure
- **Activity:** Write a Python script simulating two concurrent workers transferring balances. Worker 1 transfers Account 1 $\to$ Account 2; Worker 2 transfers Account 2 $\to$ Account 1 using `BEGIN DEFERRED`. Both workers begin by reading account balances.
- **Prediction Before Observation:** Predict what happens when both workers read their source accounts (starting read transactions), and then both attempt to execute writes that upgrade their read transactions to write transactions under rollback-journal locking.
- **Controlled Break:** Both workers attempt lock upgrade; SQLite encounters a writer/lock-upgrade conflict under the rollback-journal implementation and returns a busy conflict (recording actual SQLite result code `SQLITE_BUSY` and driver disposition, without hardcoding a fixed error string).
- **Correction:** Refactor both workers to use `BEGIN IMMEDIATE`, which acquires a reserved write lock at the start of the transaction before any data access under the rollback-journal baseline, serializing write intent and avoiding lock-upgrade collisions.

### 14.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Any SQL statement failure unconditionally requires retrying the entire transaction."* (False: Retries belong at transaction boundaries for transient conflicts or serialization failures; syntax or constraint violations must be diagnosed and handled).
  2. *"Setting a high busy timeout guarantees your write will never fail."* (False: Under sustained write contention, timeouts expire; applications must handle persistent contention gracefully).
  3. *"SQLite runs a full cycle-detection deadlock graph algorithm."* (False: SQLite does not run a general wait-for-graph cycle detector; it handles immediate lock acquisition and upgrade collisions, returning `SQLITE_BUSY`).
- **What You Can Ignore — For Now:** Distributed transaction managers; sagas; compensating transaction workflows; two-phase locking wait-for-graph cycle detection algorithms.

### 14.5 Progressive Support Ladder
- **Question:** Why does using `BEGIN DEFERRED` cause concurrent writer lock-upgrade conflicts in SQLite?
- **Hint 1:** When does `BEGIN DEFERRED` actually start a transaction or acquire a lock?
- **Hint 2:** `BEGIN DEFERRED` defers starting the actual transaction until first database access. If the first access is a `SELECT`, a read transaction begins (acquiring a shared lock under rollback-journal mode); a later write must attempt an upgrade to a write transaction (attempting to acquire a reserved lock). Note that shared/reserved lock states are SQLite rollback-journal implementation details under the declared baseline, not universal transaction semantics or WAL behavior.
- **Expected Observation:** If another connection has already acquired a reserved lock or also holds a shared lock preventing an exclusive upgrade, the upgrade attempt cannot proceed and returns a busy conflict (`SQLITE_BUSY`).
- **Full Explanation:** `BEGIN IMMEDIATE` acquires a reserved write lock at transaction start, serializing write intent upfront and preventing concurrent connections from colliding during later lock-upgrade attempts.

### 14.6 Visual Specification & Exit Criteria
- **Visual:** Flowchart comparing Naive Retry vs. Transaction-Boundary Retry. Displays Worker encountering a lock-upgrade conflict (`SQLITE_BUSY`), issuing an immediate `ROLLBACK`, entering an exponential backoff sleep, and restarting at `BEGIN IMMEDIATE` from the appropriate transaction boundary. Includes an idempotency key check preventing duplicate processing.
- **Exit Criteria:** Learner designs a multi-statement transaction script featuring upfront write-locking (`BEGIN IMMEDIATE`), retry from the appropriate transaction boundary on busy conflict, and invariant verification.

### 14.7 Lesson Contract Audit
- **Canonical Competencies:** `Judge`, `Correctness`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-001 State`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`.
- **Learner Evidence:** Python script execution log demonstrating: (1) two concurrent connections executing deferred reads and colliding on write lock upgrades under the declared rollback-journal baseline, capturing the actual `SQLITE_BUSY` result code and driver disposition; (2) correction using `BEGIN IMMEDIATE` to prevent upgrade conflicts; (3) transaction-boundary retry harness with exponential backoff and idempotency verification.
- **Provenance & Currentness:** SQLite locking specification (`sqlite3_busy_timeout`, `BEGIN DEFERRED`, `BEGIN IMMEDIATE`); application retry patterns.
- **Exact Inference Limits:** Upfront locking (`BEGIN IMMEDIATE`) prevents concurrent writer lock-upgrade conflicts in SQLite, but serializes writers and limits write concurrency. Retrying from the transaction boundary resolves transient concurrency conflicts, but cannot resolve persistent constraint, schema, or application logic errors.

---

## 15. Required Lab LAB-REQ-05 Design — SQLite Transactions, Isolation, Rollback & Recovery Boundary

### 15.1 Overview & Required Baseline
- **Lab ID:** `LAB-REQ-05`
- **Module Placement:** M14 Databases: Transactions, Recovery & Isolation
- **Type:** Build — Essential CS original
- **Execution Baseline:** Local SQLite database file with default **rollback journal** (`DELETE` mode). WAL mode is an optional comparison.
- **Subprocess Safety:** Child processes used for interruption testing must be owned handles, reaped explicitly, and bounded by a watchdog timer.

### 15.2 Experimental Procedure
1. **Checkpoint 1 — Invariant Definition & Committed Visibility:**
   - Initialize two accounts with invariant: $\text{balance}_A + \text{balance}_B = 1000$.
   - Connection 1 opens `BEGIN IMMEDIATE;` and updates Account A.
   - Connection 2 queries Account A. Assert that Connection 2 observes original committed balance (prevention of dirty reads).
2. **Checkpoint 2 — Bounded Writer Conflict:**
   - Connection 2 attempts `BEGIN IMMEDIATE;` while Connection 1 holds its transaction open.
   - Record the actual SQLite result code and driver exception (e.g., `SQLITE_BUSY`, recording the driver disposition without asserting one fixed error string).
   - Verify that Connection 2 does not corrupt database state.
3. **Checkpoint 3 — Explicit Rollback:**
   - Connection 1 issues `ROLLBACK;`.
   - Verify that all account balances remain exactly at their initial state across both connections.
4. **Checkpoint 4 — Owned Child Interruption & Recovery:**
   - Parent spawns an owned child process that opens a transaction and updates balances.
   - Before the child commits, the parent terminates the child abruptly using `SIGKILL` (or OS equivalent).
   - Parent reaps the terminated child process handle.
   - Parent opens a new connection to the database file. Observe the cleanup of the rollback journal and assert that balances reflect pre-crash committed state.
5. **Checkpoint 5 — Backup & Storage Boundary:**
   - Use the SQLite online backup API (`conn.backup()`) to copy the database to a clean destination file.
   - Verify consistency of the restored backup.
   - Document the critical inference boundary: Terminating a child process verifies *client crash recovery*, not power-loss hardware durability.

### 15.3 Machine-Checkable vs. Reviewer-Required Gates
- **Machine-Checkable:**
  - Dual-connection test runner verifies absence of dirty reads;
  - Captures exception on concurrent write attempts;
  - Asserts balance sum invariant equals 1000 before and after child process termination.
- **Reviewer-Required:**
  - Audit learner's written distinction between client process termination, OS crash, and physical power failure.

---

## 16. Module M15 Architecture — Concurrency: Threads, Races & Synchronization

- **Module Purpose:** Demystify multi-threaded programming. Transition from isolated processes to shared memory. Unpack thread interleaving, logical race conditions without undefined behavior, mutual exclusion, condition variable synchronization, and execution model trade-offs (threads vs. async).
- **Primary Competency:** **Diagnose** (identifying thread interleavings, reproducing lost updates, diagnosing deadlocks).
- **Secondary Competencies:** Trace, Correctness, Explain, Judge.
- **Canonical Concept First Home:** **EC-CON-015 Concurrency (L15-01)**.
- **Canonical Concepts Revisit:** `EC-CON-001 State`, `EC-CON-007 Specification`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`, `EC-CON-013 Isolation` (synchronization scope).
  *(Note: `EC-CON-018 Process` is not an authorized canonical Concept Revisit in M15; thread-vs-process comparisons remain pedagogical context without an unauthorized Concept Registry mapping).*

---

## 17. Lesson L15-01 Design — “Why is my threaded code wrong?”

### 17.1 Learner Question & Capability Transition
- **Learner Question:** "Why does running code in two threads produce different, incorrect results, and why does my code pass tests when I run it once but fail under load?"
- **Capability Transition:** Moves from assuming sequential line-by-line execution to understanding preemptive kernel scheduling, arbitrary instruction interleaving, and anchoring the formal definition of **EC-CON-015 Concurrency**.

### 17.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *Threads vs. Processes:* Processes possess private virtual address spaces. Threads within a process share heap, global variables, and file descriptors, but maintain private program counters, registers, and stacks.
  - *Interleaving:* The kernel scheduler preempts threads arbitrarily. Instructions interleave across threads.
  - *Logical Race Condition vs. C Data Race (UB):* A data race in C (concurrent unsynchronized accesses where at least one is a write) is **Undefined Behavior (UB)** under ISO C11 §5.1.2.4. Compilers may optimize away loops containing data races.
  - *The Essential CS Teaching Solution:* To demonstrate race conditions rigorously without UB, we use C11 atomics (`<stdatomic.h>`) with relaxed memory order for individual reads and writes. Individual memory operations are strictly legal and defined, but the multi-step compound read-modify-write operation is non-atomic, exposing real lost updates under thread interleaving.
- **Claim Layers:**
  - *PRINCIPLE:* Concurrency vs. parallelism; logical race conditions; non-deterministic interleaving.
  - *SPECIFICATION:* ISO/IEC 9899:2011 (C11) atomics specification; POSIX IEEE Std 1003.1-2024 thread model.
  - *IMPLEMENTATION:* Linux NPTL thread scheduling; glibc thread management.
  - *CURRENT PRACTICE:* GCC/Clang thread compilation flags (`-pthread`).

### 17.3 Canonical Concept First Home: EC-CON-015 Concurrency
- **Exact First Home:** M15 / `L15-01`.
- **Exact Canonical Definition:**
  > **“Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations.”**
- **Disambiguation Mandate in Teaching:**
  - Explicitly distinguish concurrency (system composition allowing interleaved progress) from parallelism (physical simultaneous execution on multiple cores).
  - Prove that concurrency bugs occur on single-core processors due to preemptive time-slicing.

### 17.4 Hands-On Activity & Controlled Failure
- **Activity:** Compile and run a C11 program with two threads executing a compound update on an atomic counter using `atomic_load_explicit` and `atomic_store_explicit`.
- **Preferred Evidence Contract:** The activity uses a **course-controlled phase handoff / barrier coordination** between threads to deterministically produce a real pthread lost-update interleaving with defined C11 atomic accesses.
- **Supplemental Scheduler Observation:** Natural scheduler observation under cooperative yield (`sched_yield()`) is supplemental only and bounded by an attempt budget. Tests must not assert fixed failure percentages (such as $\ge 95\%$ or $100\%$) or fixed count ranges.
- **Prediction Before Observation:** Predict the final counter value if both threads interleave during the read-modify-write sequence.
- **Controlled Break:** The final counter value reflects lost updates despite 100% legal atomic memory accesses, proving a logical race condition without language-level undefined behavior.

### 17.5 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Concurrency and parallelism are the exact same thing."* (False: Concurrency is about structure and interleaving; parallelism is about physical simultaneous hardware execution).
  2. *"Making a variable atomic automatically makes compound multi-step operations correct."* (False: Atomic reads and writes prevent memory corruption, but compound state transitions remain non-atomic).
  3. *"A race condition must be a C/C++ data race."* (False: A data race is an undefined memory access; a race condition is a logical flaw in state transition ordering).
- **What You Can Ignore — For Now:** Formal C++ memory model release-acquire operational semantics proofs; lock-free algorithms; kernel futex internals.

### 17.6 Progressive Support Ladder
- **Question:** Why did our counter lose updates even though every load and store was an atomic C11 operation?
- **Hint 1:** Trace the sequence of events when Thread 1 reads `42`.
- **Hint 2:** Thread 1 reads `42`. Before it can store `43`, Thread 2 also reads `42`.
- **Expected Observation:** Both threads compute `43` and write `43`. One increment vanished.
- **Full Explanation:** Individual memory operations were atomic, but the compound state transition (Read $\to$ Compute $\to$ Store) was not. Interleaving caused a lost update.

### 17.7 Visual Specification & Exit Criteria
- **Visual:** Interleaving Trace diagram contrasting Concurrency (single core, time-sliced interleaved execution blocks) vs. Parallelism (dual cores, simultaneous timeline bars). Shows Thread 1 reading Counter $= 42$, Thread 2 reading Counter $= 42$, both computing $43$, and both writing $43$. Prominently displays the exact one-sentence definition of **EC-CON-015 Concurrency**.
- **Exit Criteria:** Learner draws an instruction interleaving diagram explaining a lost update and correctly recites `EC-CON-015`.

### 17.8 Lesson Contract Audit
- **Canonical Competencies:** `Trace`, `Diagnose`, `Correctness`.
- **Concepts & Revisits:** **EC-CON-015 Concurrency (First Home)**; canonical revisits `EC-CON-001 State`, `EC-CON-009 Correctness`. (Note: `EC-CON-018 Process` is not an authorized canonical revisit in M15).
- **Learner Evidence:** Compile log and run execution output of C11 pthreads program demonstrating a lost update: two threads execute compound updates on an atomic counter using `atomic_load_explicit` / `atomic_store_explicit`; phase handoff / barrier log proving instruction interleaving; final counter value demonstrating missing increments despite zero undefined behavior (UB); verbatim recitation of `EC-CON-015 Concurrency`.
- **Provenance & Currentness:** ISO/IEC 9899:2011 (C11) §5.1.2.4 memory model and atomics; POSIX IEEE Std 1003.1-2024 thread model; Linux NPTL.
- **Exact Inference Limits:** Demonstrating a lost update with relaxed atomics proves that compound state transitions are non-atomic, but does not prove memory ordering violations or cache coherency flaws. Natural scheduler interleaving without barrier coordination is non-deterministic and must not be asserted as a guaranteed occurrence rate.

---

## 18. Lesson L15-02 Design — “How do I make it right?”

### 18.1 Learner Question & Capability Transition
- **Learner Question:** "How do I protect shared state without introducing deadlocks, and how do threads coordinate when one must wait for another to finish?"
- **Capability Transition:** Moves from observing concurrency bugs to implementing synchronization primitives: mutual exclusion via POSIX mutexes, condition synchronization via condition variables, and deadlock avoidance.

### 18.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *POSIX Mutex (`pthread_mutex_t`):* Guarantees that at most one thread executes a critical section at any instant. Enforces acquire/release memory visibility. Does *not* guarantee fair FIFO ordering among waiting threads.
  - *POSIX Condition Variable (`pthread_cond_t`):* Mechanism for event rendezvous. Atomically releases associated mutex and suspends calling thread in `pthread_cond_wait`. Upon wake, re-acquires the mutex.
  - *Condition-Variable Re-check Contract:* The predicate must be rechecked under mutex protection after wake; the course adopts the `while (!predicate)` pattern:
    ```c
    pthread_mutex_lock(&lock);
    while (!predicate_is_true) {
        pthread_cond_wait(&cond, &lock);
    }
    // Critical invariant guaranteed
    pthread_mutex_unlock(&lock);
    ```
    *(Do not claim that POSIX specification mandates literal `while` syntax; POSIX specifies that `pthread_cond_wait` may return spuriously, requiring condition re-evaluation upon return; `while` is the idiomatic course pattern).*
  - *Deadlock & Coffman Conditions:* Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. Avoidance via lock acquisition hierarchies.
- **Claim Layers:**
  - *PRINCIPLE:* Mutual exclusion; Dijkstra critical section invariants; condition synchronization; Coffman deadlock conditions.
  - *SPECIFICATION:* The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024 (`pthread_mutex_*`, `pthread_cond_*`).
  - *IMPLEMENTATION:* Linux futex-backed mutex and condition variable implementation in glibc.
  - *CURRENT PRACTICE:* Compiler warnings for uninitialized mutex attributes.

### 18.3 Hands-On Activity & Controlled Failure
- **Activity:** Protect the compound update from L15-01 with a POSIX mutex. Implement a condition-variable rendezvous where Worker 2 waits for Worker 1 to produce data.
- **Prediction Before Observation:** Predict whether checking the condition only once without a loop around `pthread_cond_wait` is safe under POSIX specifications.
- **Controlled Break:** Explain the spurious wakeup hazard and why the condition predicate must be rechecked upon return from `pthread_cond_wait`.
- **Controlled Deadlock:** Implement a reversed lock acquisition order (Thread 1: Lock A $\to$ B; Thread 2: Lock B $\to$ A) using a controlled handshake so both threads hold their first lock before requesting their second lock. Run under an owned-child watchdog with a configurable timeout parameter.

### 18.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"A mutex guarantees that threads take turns fairly."* (False: POSIX mutexes do not guarantee fairness; newly unblocked threads can re-acquire locks ahead of long-waiting threads).
  2. *"A condition variable notification means the predicate is currently true."* (False: A signal wakes a thread, but by the time the thread re-acquires the mutex, another thread may have altered the predicate; spurious wakeups can also occur).
  3. *"A timeout alone proves a deadlock occurred."* (False: A timeout only proves progress stalled within the allotted duration; deadlock proof requires demonstrating that threads hold locks in circular wait).
- **What You Can Ignore — For Now:** Lock-free hazard pointers; reader-writer lock starvation engineering; priority inheritance protocols in real-time kernels.

### 18.5 Progressive Support Ladder
- **Question:** Why does POSIX Issue 8 state that `pthread_cond_wait` may return spuriously?
- **Hint 1:** Consider kernel signal interruptions or multi-processor wake optimizations.
- **Hint 2:** If waking up does not guarantee the predicate changed, how must you structure your check?
- **Expected Observation:** The waiting code must re-evaluate the predicate under mutex protection.
- **Full Explanation:** Kernel scheduling and multiprocessor memory events permit spurious wakeups. Rechecking the predicate ensures the thread never proceeds unless the shared condition is genuinely true.

### 18.6 Visual Specification & Exit Criteria
- **Visual:** Mutex & Condition Rendezvous diagram. Panel 1: Mutex Lock Invariant (one thread in critical section, other threads blocked in wait queue). Panel 2: Condition Variable Protocol (Worker 1 holds lock $\to$ `pthread_cond_wait` atomically unlocks and sleeps $\to$ Worker 2 acquires lock, updates predicate, calls `signal` $\to$ Worker 1 re-awakens, re-acquires lock, and loops on predicate).
- **Exit Criteria:** Learner repairs a broken threaded counter with a mutex (verifying that every completed run satisfies the declared invariant) and implements a condition rendezvous with a verified predicate recheck loop.

### 18.7 Lesson Contract Audit
- **Canonical Competencies:** `Explain`, `Correctness`, `Judge`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-001 State`, `EC-CON-007 Specification`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`.
- **Learner Evidence:** C program execution logs showing: (1) successful repair of the counter from L15-01 using `pthread_mutex_t`, verifying that final count matches expected invariant across runs; (2) condition-variable rendezvous using `pthread_cond_t` with a verified predicate recheck loop (`while (!predicate)`); (3) controlled lock-order inversion executed in an owned child process, terminated cleanly by a watchdog timer governed by a configurable timeout parameter.
- **Provenance & Currentness:** POSIX IEEE Std 1003.1-2024 mutex and condition variable specifications; Linux futex implementation.
- **Exact Inference Limits:** Passing a mutex-protected counter test proves mutual exclusion for the protected critical section, but does not prove lock fairness or absence of lock starvation under high thread counts. Watchdog termination of a stalled process indicates lack of progress within the configured timeout, which must be paired with lock-order evidence to prove circular deadlock.

---

## 19. Lesson L15-03 Design — “Thread or async?”

### 19.1 Learner Question & Capability Transition
- **Learner Question:** "Should I build my application with multi-threading or asynchronous event loops, and what does the Python GIL actually do to my code across different runtimes and workloads?"
- **Capability Transition:** Moves from treating "threads vs. async" as an ideological dichotomy to evaluating concurrency models based on blocking behavior, CPU-bound work, runtime capabilities (e.g. CPython GIL vs. free-threading), extension behavior, and executor architectures.

### 19.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *OS Threads:* Preemptive kernel scheduling; private execution stack; kernel context switches; transparent blocking on system calls. Threads can execute concurrently across multiple physical cores when supported by the underlying language runtime and platform.
  - *Asynchronous Event Loops:* Cooperative multitasking (`async`/`await`); lightweight coroutines/tasks multiplexed over I/O notification mechanisms (`epoll`/`kqueue`/`IOCP`). A single event loop cooperatively schedules its Tasks without thread preemption between `await` points, while blocking operations or heavy CPU computations may be explicitly delegated to executors. For CPU-bound work, process executors (`ProcessPoolExecutor`) or sub-interpreter executors can provide multi-core parallel execution under their respective process/interpreter isolation contracts; thread executors (`ThreadPoolExecutor`) can provide CPU parallelism only when the named runtime/build (such as free-threaded CPython / PEP 779) or invoked native C extensions explicitly release the GIL without imposing interpreter lock contention.
  - *CPython Runtime & GIL Reality:* The Global Interpreter Lock (GIL) is a CPython implementation mechanism, not an invariant of the Python language. In a named GIL-enabled CPython build, the GIL serializes bytecode execution within an interpreter instance to protect runtime memory structures. It does *not* make Python application-level compound operations thread-safe; thread switching between bytecode instructions can interleave compound operations.
  - *Python 3.14 Free-Threading Capability:* In Python 3.14 / PEP 779, free-threading is in **supported phase II** (officially supported build configuration without a global interpreter lock), allowing multi-threaded Python bytecode to execute simultaneously across multiple physical CPU cores.
  - *Workload Judgment Criteria:* Architectural selection between threads and async depends on blocking behavior (I/O-wait vs. CPU computation), task scale and memory overhead, runtime/build capabilities (GIL vs. free-threaded vs. multi-process), C-extension behaviors, and executor composition.
- **Claim Layers:**
  - *PRINCIPLE:* Preemptive vs. cooperative scheduling; memory footprint trade-offs; I/O multiplexing mechanics; coordination scope.
  - *SPECIFICATION:* Python language syntax (`async`/`await` coroutines); PEP 492 / PEP 779.
  - *IMPLEMENTATION:* CPython bytecode evaluation loop; named GIL vs. free-threaded build capabilities; `asyncio` event loop scheduling.
  - *CURRENT PRACTICE:* Hybrid architectures (async I/O event loops delegating blocking/CPU tasks to thread/process pools).

### 19.3 Hands-On Activity & Controlled Failure
- **Activity:** Run a companion Python script inspecting bytecode disassembly of a compound update (`x += 1`) using Python's `dis` module, and compare cooperative `asyncio` task scheduling with multi-threaded execution under a named Python/CPython runtime.
- **Prediction Before Observation:** Predict whether `x += 1` executes as an indivisible single bytecode instruction or compiles into multiple distinct bytecode steps in CPython.
- **Controlled Break / Observation:** Observe that `x += 1` compiles into multiple distinct bytecode operations (e.g., loading the object, performing the operation, storing the result). Observe that in a multi-threaded CPython environment, thread preemption can occur between bytecode instructions, demonstrating why atomicity cannot be assumed. Disassembly is a runtime mechanism observation only; it is not a required lost-update race outcome or a universal proof across all runtimes.
- **Comparison:** Implement an asynchronous task using `asyncio` and observe that a single event loop runs tasks cooperatively without preemption between `await` points. Demonstrate how blocking calls within a coroutine stall the entire loop unless delegated to an executor.

### 19.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"The GIL means multi-threaded Python programs never need mutexes or locks."* (False: The GIL protects interpreter memory; compound application updates lose data under thread interleaving in GIL-enabled builds).
  2. *"Async is universally faster than threaded code or provides zero parallel speedup."* (False: Performance depends on workload and architecture; single-loop async minimizes task memory overhead for high-concurrency I/O. For CPU-intensive work, process or sub-interpreter executors can provide multi-core execution under their respective isolation contracts; a thread executor can provide CPU parallelism only when the named runtime/build or invoked native extension releases/does not impose the relevant GIL constraint; free-threaded CPython may allow parallel Python bytecode execution; actual workload/runtime capability remains the judgment authority).
  3. *"The GIL is a permanent rule of the Python language."* (False: The GIL is an implementation detail of standard CPython; alternative runtimes and Python 3.14 PEP 779 free-threaded builds operate without it).
- **What You Can Ignore — For Now:** Deep CPython C-API internal reference counting macros; custom asyncio event loop policy implementations; Rust async executor internals.

### 19.5 Progressive Support Ladder
- **Question:** In a named GIL-enabled CPython build, if the GIL allows only one thread to execute Python bytecode at a time, why can a compound update like `x += 1` still suffer from concurrency issues?
- **Hint 1:** Disassemble `x += 1` using Python's `dis` module.
- **Hint 2:** Is `x += 1` executed as a single indivisible instruction?
- **Expected Observation:** It compiles into multiple bytecode operations (e.g., loading the object, executing the increment, and storing the reference back) rather than an indivisible single step.
- **Full Explanation:** Preemptive thread switching can occur between individual bytecode operations in a GIL-enabled build. Both threads can read the same initial value and store the same updated value.

### 19.6 Visual Specification & Exit Criteria
- **Visual:** Execution Model Comparison matrix. Columns: OS Preemptive Threads vs. Cooperative Async Event Loop (with Executor Delegation) vs. CPython Runtime Reality (GIL-enabled vs. Free-threaded). Rows: Scheduling Mechanism, Memory per Task, Multiprocessor Parallelism, Shared-State Coordination Scope, Best Workload Fit.
- **Exit Criteria:** Learner disassembles a Python compound operation, explains why the GIL does not guarantee application thread safety in GIL-enabled CPython, and articulates workload-driven model selection based on blocking behavior and runtime capabilities.

### 19.7 Lesson Contract Audit
- **Canonical Competencies:** `Judge`, `Explain`.
- **Concepts & Revisits:** Canonical revisits `EC-CON-007 Specification`, `EC-CON-013 Isolation` (synchronization scope).
- **Learner Evidence:**
  - Prediction before observation predicting whether `x += 1` executes as an atomic opcode in CPython bytecode.
  - Python session log running `dis.dis()` on a compound increment, recording actual bytecode operations under named Python/CPython version and build.
  - Asynchronous task log using `asyncio` demonstrating cooperative task execution and executor delegation for blocking operations.
  - Written evaluation matrix judging when to choose OS threads vs. cooperative async event loops based on blocking behavior, CPU work, runtime/build, extension behavior, and actual runtime capability.
- **Provenance & Currentness:** Python 3.14 PEP 779 free-threading supported phase II vs. default GIL-enabled CPython; Python `asyncio` specification.
- **Exact Inference Limits:** Bytecode disassembly of `x += 1` demonstrates that compound operations are multi-step in CPython, but does not guarantee a specific lost-update manifestation rate. A single `asyncio` event loop eliminates preemption between `await` points, but multi-step operations spanning `await` expressions still require logical coordination.

---

## 20. Required Lab LAB-REQ-03 Design — POSIX Threads Race, Rendezvous & Progress Boundaries

### 20.1 Overview & Required Baseline
- **Lab ID:** `LAB-REQ-03`
- **Module Placement:** M15 Concurrency: Threads, Races & Synchronization
- **Type:** Build — Essential CS original
- **Execution Baseline:** Canonical Linux with `gcc -std=c11 -pthread`.

### 20.2 The UB-Free Broken Path Contract
- **No Undefined Behavior:** The broken path strictly uses C11 atomics (`<stdatomic.h>`) with `memory_order_relaxed`. Individual reads and writes are defined, legal atomic operations under ISO C11.
- **Evidence Contract:**
  - *Preferred Evidence:* The fixture uses **course-controlled phase handoff / barrier coordination** between threads to deterministically produce a real pthread lost-update interleaving using defined C11 atomic accesses.
  - *Supplemental Scheduler Observation:* Natural scheduler observation under cooperative yield is supplemental only and bounded by an attempt budget. Tests must never assert hardcoded failure percentages (such as $\ge 95\%$ or $100\%$) or fixed erroneous count ranges.

### 20.3 Mutex Repair & Condition Rendezvous
- **Mutex Repair:** Wrapping the compound update in `pthread_mutex_lock` / `unlock` guarantees that every completed run satisfies the invariant.
- **Condition Variable Rendezvous:** Worker 2 waits for Worker 1 to signal that a shared buffer is ready. The wait is enclosed in a condition predicate recheck loop under mutex protection (`while (!buffer_ready) pthread_cond_wait(&cond, &mutex);`).

### 20.4 Controlled Deadlock & Watchdog Harness
- **Deadlock Preconditions:** Thread 1 acquires Lock A $\to$ Lock B; Thread 2 acquires Lock B $\to$ Lock A.
- **Deterministic Coordination:** Threads synchronize via a start gate so both threads hold their first lock before either attempts to acquire its second lock.
- **Watchdog Execution:** The deadlock test runs in an owned child process. The parent watchdog enforces a **configurable timeout parameter**.
- **Inference Boundary:** The parent records that both threads entered their respective first locks and stalled on their second locks before interpreting the timeout as deadlock evidence. The safety harness bounds the course child process with a configured timeout; it cannot literally guarantee that host environments or terminal UIs never stall. The timeout duration is a harness parameter, not a curriculum constant.

---

## 21. Optional Content Design Disposition (LAB-OPT-03 & LAB-OPT-05)

### 21.1 LAB-OPT-03 Design — PostgreSQL EXPLAIN & Isolation Comparison
- **Status:** Strictly Optional.
- **Scope:** Adapts official PostgreSQL documentation for query plan inspection (`EXPLAIN (ANALYZE, BUFFERS)`) and repeatable read serialization conflict detection.
- **Safety Gate:** Any `EXPLAIN ANALYZE` examples that execute mutations (`INSERT`/`UPDATE`) must be wrapped inside a transaction and rolled back (`BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`).
- **Dependency Boundary:** PostgreSQL and Docker are not required. If unavailable, the lab is recorded as **`OPTIONAL LAB NOT RUN / TOOL UNAVAILABLE`**.

### 21.2 LAB-OPT-05 Design — OSTEP Semaphore Rendezvous
- **Status:** Strictly Optional.
- **Scope:** Adopt as **link-only** pointer to OSTEP homework commit `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2` (`threads-sema/rendezvous.c`).
- **Rights & Provenance:** No code, tests, or text from the unlicensed `ostep-homework` repository will be copied, vendored, or bundled into Essential CS.

---

## 22. S5 Preflight & Environment Contract

The S5 preflight script evaluates host capabilities before Lab execution without closing OQ-BP-006. It inspects and records actual:

1. **Host OS / Kernel / Architecture:** Actual platform, kernel release, and CPU architecture where available.
2. **Python Implementation & Version:** Runtime identity and version (e.g., CPython 3.14.x / 3.13.x).
3. **Embedded SQLite Version:** Reported via `sqlite3.sqlite_version`.
4. **SQLite CLI Availability & Version:** Presence and version of `sqlite3` binary in PATH.
5. **Local Filesystem & VFS Disposition:** Course-owned writable directory path and VFS locking capability.
6. **Compiler Identity & Version:** GCC or Clang compiler identity and version.
7. **C11 & Pthreads Compilation Capability:** Verification of `-std=c11 -pthread` compilation.
8. **C11 Atomics Capability:** Compilation check for `<stdatomic.h>`.
9. **POSIX Mutex & Condition Variable Capability:** Linkage and execution check for `pthread_mutex_*` and `pthread_cond_*`.
10. **Owned Child Process & Watchdog Capability:** Subprocess spawn, timeout, and reaping capability.
11. **Optional PostgreSQL Server / `psql` Client:** Availability and version of `psql` and local database service.
12. **Optional Container Runtime:** Availability of Docker or Podman.
13. **Optional Sanitizer / Race Tool Capability:** Availability of ThreadSanitizer (`-fsanitize=thread`).
14. **EXP-02 Source Access & Current Revision:** Local source access and git commit hash disposition for PostgreSQL source tree.

### Truthful Preflight Dispositions
- `REQUIRED CAPABILITY PASS`: All Required Core capabilities confirmed.
- `ENVIRONMENT-BLOCKED / NOT RUN`: Specific missing tool blocks a specific Lab (e.g., missing `sqlite3` CLI blocks LAB-REQ-04; missing compiler blocks LAB-REQ-03; does not block the entire course automatically).
- `OPTIONAL TOOL UNAVAILABLE / SKIP`: Optional PostgreSQL or Docker missing; optional labs skipped without penalty.
- `NO LIVE SOURCE RECHECK`: Network disconnected; EXP-02 uses local source snapshot or cached reference.

---

## 23. Evidence-Template Contracts

Later implementation must produce standardized evidence templates for learner records:

### 23.1 M13 Evidence Template Structure
- **Section A:** Environment / CLI / SQLite versions recorded.
- **Section B:** L13-01 prediction + actual CLI `EXPLAIN QUERY PLAN` capture.
- **Section C:** Result set equivalence confirmation ($\Delta = 0$).
- **Section D:** Read timing distributions, cache-state assumptions, warmup protocol, environment notes, and **raw timing samples**.
- **Section E:** Write latency and file size observations after index creation.
- **Section F:** Inference limit articulation (index $\ne$ universal speedup).
- **Section G:** L13-02 SQL declarative intent vs. physical access path explanation.
- **Section H:** L13-03 Schema evolution, compatibility, source of truth, and provenance record.
- **Section I:** LAB-REQ-04 break case (un-sargable query or low-selectivity scan choice).
- **Section J:** EXP-02 exact revision, date, three paths, and Target 1 drift notes.
- **Section K:** Concepts, competencies, visuals, and support audit.
- **Section L:** Safety and cleanup verification.

### 23.2 M14 Evidence Template Structure
- **Section A:** SQLite environment, journal mode (`DELETE`), and synchronous settings.
- **Section B:** Declared transaction balance invariant.
- **Section C:** Dual-connection committed-only visibility timeline.
- **Section D:** Second-writer conflict observation and actual driver disposition.
- **Section E:** Explicit rollback verification.
- **Section F:** Child process interruption point and process reaping record.
- **Section G:** Reopen recovery and journal side-file cleanup observation.
- **Section H:** Online backup creation and clean-file restoration verification.
- **Section I:** Durability inference limit (client kill $\ne$ power loss).
- **Section J:** EC-CON-014 Consistency exact canonical definition and named qualifier.
- **Section K:** ACID Consistency vs. transaction isolation disambiguation.
- **Section L:** Whole-transaction retry and idempotency preview judgment.
- **Section M:** Concepts, competencies, visuals, support, and cleanup audit.

### 23.3 M15 Evidence Template Structure
- **Section A:** OS, compiler, POSIX thread, and C11 atomic capabilities.
- **Section B:** EC-CON-015 Concurrency exact canonical definition.
- **Section C:** Broken compound-update source code audit confirming legal atomic accesses (no UB).
- **Section D:** Observed lost-update interleaving and scheduler disposition.
- **Section E:** Mutex repair verification proving invariant restoration.
- **Section F:** Condition variable predicate rendezvous verification.
- **Section G:** Controlled deadlock preconditions and watchdog reaping record.
- **Section H:** Fairness and scheduler progress inference limits.
- **Section I:** Thread vs. async architectural evaluation.
- **Section J:** CPython runtime, bytecode disassembly, and GIL/free-threading observation.
- **Section K:** Concepts, competencies, visuals, support, and cleanup audit.

### 23.4 EXP-02 Evidence Template Structure
- **Inspection Date & Revision:** Exact git commit hash and date of inspected PostgreSQL repository.
- **Path 1 Finding (`src/backend/optimizer/plan/README`):** Summary of historical subselect notes; explicit confirmation of historical drift.
- **Path 2 Finding (`src/backend/optimizer/path/costsize.c`):** Code citation for `cost_seqscan()` and `cost_index()`, explaining CPU vs. I/O cost estimation weights.
- **Path 3 Finding (`src/backend/storage/buffer/README`):** Summary of clock-sweep page replacement and buffer pinning protocols.
- **Supplemental-Source Note:** Record if parent `src/backend/optimizer/README` was consulted as supplemental reviewer context.
- **Bound & Safety Confirmation:** Explicit confirmation that inspection stopped at bounded lines; zero compilation attempted; zero source code vendored.
- **Provenance / License Disposition:** Confirmation of PostgreSQL License notice preservation.

---

## 24. Progressive-Support Contract

Every future Lesson and Lab checkpoint must follow the strict five-tier progressive support ladder without revealing answers prematurely:

```
[ Tier 1: Question ]
  |-- Prompts the learner with the core challenge or diagnostic puzzle.
  v
[ Tier 2: Hint 1 ]
  |-- Focuses the learner's attention on the relevant mechanism without naming the solution.
  v
[ Tier 3: Hint 2 ]
  |-- Points to specific tools, syntax, or inspection methods (e.g., EQP or predicate loops).
  v
[ Tier 4: Expected Observation ]
  |-- Describes the pattern or semantic structure to expect (using placeholders, never fake data).
  v
[ Tier 5: Full Explanation ]
  |-- Complete systems explanation unpacking root causes, trade-offs, and invariants.
```

- **Formatting Rule:** HTML `<details open>` is strictly prohibited. Hints must remain collapsed until explicitly opened by the learner.
- **Truthful Placeholder Rule:** Expected observations must **never fabricate** any of the following:
  1. exact SQLite plan text;
  2. timing;
  3. page count;
  4. file-size ratio;
  5. error string;
  6. lock timing;
  7. scheduler ordering;
  8. race manifestation rate;
  9. GIL mode;
  10. PostgreSQL plan;
  11. source revision.
  Expected observations must use structural placeholders, patterns, and learner-recorded values.

---

## 25. Visual Contract

All visual assets must be original, editable diagrams complying with `meta/VISUAL_AND_WRITING_POLICY.md`:

| Lesson / Lab | Visual Title | Core Pedagogical Content | Mandatory Inscription / Label |
|---|---|---|---|
| **L13-01** | Query Access Paths & Storage | SQL intent branching into Sequential Scan vs. B-Tree index lookup visiting disk pages. | **"PLAN CHOICE IS IMPLEMENTATION AND WORKLOAD DEPENDENT"** |
| **L13-02** | Declarative Intent vs. Engine Reality | Two-layer diagram: Declarative SQL intent mapped to Engine Parser/Planner/Code Generator and Storage Engine. | Abstraction boundary and sargable vs. non-sargable predicate leakage. |
| **L13-03** | Schema Evolution Lifecycle | Expand-Contract three-stage migration pattern (Expand $\to$ Backfill $\to$ Contract) with Source of Truth vs. Derived View. | Source of Truth is authoritative; bounded derived view is recomputable. |
| **L14-01** | Transaction State & Recovery Boundary | State transition from $S_0$ through dirty buffer changes to $S_1$ via `COMMIT` vs. Rollback Journal restoration. | Rollback reverts uncommitted mutations; client kill $\ne$ power loss. |
| **L14-02** | Concurrent Interleaving & Visibility | Timeline showing $T_1$ and $T_2$ interleavings, committed-only visibility, and writer lock conflicts. | **EC-CON-014 Consistency: Full canonical definition with mandatory qualifier.** |
| **L14-03** | Transaction-Boundary Retry | Flowchart comparing naive statement retry with whole-transaction rollback, exponential backoff, and idempotency key check. | Whole-transaction retry boundary. |
| **L15-01** | Concurrency vs. Parallelism & Interleaving | Visual contrasting single-core time-slicing vs. multi-core simultaneous execution, detailing atomic lost update. | **EC-CON-015 Concurrency: Full canonical definition.** |
| **L15-02** | Mutex Invariant & Condition Rendezvous | Mutex critical section exclusion combined with condition variable predicate recheck loop protocol. | Mandatory predicate evaluation recheck guard. |
| **L15-03** | Concurrency Execution Models | Comparison matrix: OS Preemptive Threads vs. Async Event Loops vs. CPython Runtime Reality. | No universal winner; workload-driven model selection. |
| **EXP-02** | PostgreSQL Planner & Buffer Map | Tabular route map covering the three canonical paths, actual findings, and historical caveats. | Target 1 historical drift note; no compilation required. |

---

## 26. Machine-Checkable vs. Reviewer-Required Gates

```
+-----------------------------------------------------------------------------------------+
| Automated Machine-Checkable Gates (Run by CI / Test Runner)                             |
| - Preflight tool checks (Python, GCC, SQLite CLI, pthread compile).                     |
| - Semantic parsing of SQLite EQP output (SCAN vs. SEARCH ... USING INDEX).              |
| - Result set equivalence assertions (unindexed == indexed rows).                        |
| - Multi-connection committed-only visibility verification (no dirty reads).             |
| - Atomic counter lost-update demonstration under compound update.                       |
| - Mutex-protected counter verification (target invariant satisfied).                    |
| - Condition rendezvous ordering verification.                                           |
| - Deadlock watchdog timeout termination under configured harness parameter.             |
| - Deterministic cleanup of temporary database files and child processes.                |
+-----------------------------------------------------------------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------------+
| Reviewer-Required Gates (Evaluated by Human / Lead Review)                              |
| - Learner's explanation of index write/space trade-offs.                                |
| - Correct qualification of EC-CON-014 Consistency with a named isolation guarantee.    |
| - Clear disambiguation between client process crash recovery and power-loss durability. |
| - Accurate instruction interleaving diagram explaining a lost update.                   |
| - Justification of thread vs. async execution model selection based on workload.        |
| - Accuracy of EXP-02 source inspection notes regarding Target 1 historical drift.       |
+-----------------------------------------------------------------------------------------+
```

---

## 27. Safety & Cleanup Design

### 27.1 Safety Guardrails
- **Confined Localhost Execution:** All database files, subprocesses, and threads execute strictly within the local course-owned workspace. Zero external network connections, zero cloud resources, zero credentials.
- **Synthetic Data Exclusively:** All schemas and datasets are generated procedurally with random strings and numbers. Zero sensitive or personal data.
- **Zero Privileged Operations:** No `sudo`, `root`, or kernel-level capabilities permitted for any Required Lab.
- **Destruction Prevention:** Zero filesystem-fill tests (synthetic databases capped at $< 10\text{ MB}$); zero power-cut tests; zero kernel panics.
- **Process & Thread Boundaries:** Thread pools bounded to 2–4 workers. Deadlock demonstrations must run in an owned child process governed by an automated watchdog timer with a configurable timeout parameter. The safety harness bounds the course child process; it cannot literally guarantee that host environments or terminal UIs never stall.

### 27.2 Cleanup Protocol
- **Idempotent Removal:** Lab teardown functions must clean up all generated files: `<name>.db`, `<name>.db-journal`, `<name>.db-wal`, `<name>.db-shm`.
- **Process Reaping:** All child processes spawned for interruption or deadlock tests must be explicitly reaped using `waitpid` / `process.wait()`.
- **Binary Cleanup:** Compiled C test binaries in scratch directories must be removed upon test completion.
- **Scope Restriction:** No wildcard file deletions (`rm -rf *`) outside the explicitly owned lab scratch folder.

---

## 28. Source, Currentness & Provenance Rules

- **SQLite Documentation & Code:** Dedicated to the **Public Domain**. Permitted to quote and base original fixtures upon. All lab instructions and fixtures remain Essential CS original works.
- **The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024:** Normative standard for POSIX threads and synchronization. Permitted to reference stable URLs; no full standard mirroring.
- **PostgreSQL Documentation & Source:** Governed by the permissive **PostgreSQL License**. Permitted to inspect source files (EXP-02) and adapt documentation (LAB-OPT-03) with required copyright preservation.
- **OSTEP Homework:** Repository lacks a declared open-source license. Governed by a **strict link-only policy (LAB-OPT-05)**. Zero vendoring or code distribution.
- **Python Documentation:** Governed by the **PSF License**. Permitted to use standard libraries in lab runners.

---

## 29. Concept & Competency Audit

### 29.1 Concept Audit
- **Total Canonical Concepts:** 18 (unchanged).
- **EC-CON-014 Consistency First Home:** `M14` / `L14-02`. Fully specified with mandatory named guarantee qualifier.
- **EC-CON-015 Concurrency First Home:** `M15` / `L15-01`. Fully specified and distinguished from parallelism.
- **New Concept IDs Introduced:** **Zero (0)**.
- **Schema Evolution / Provenance:** Treated strictly as an application pattern under existing concepts (`EC-CON-001`, `003`, `005`, `008`).
- **Canonical Concept Revisit Mappings:**
  - `M13`: `EC-CON-001`, `003`, `005`, `006`, `008`, `009`, `011`, `012`.
  - `M14`: `EC-CON-001`, `006`, `007`, `008`, `009`, `013`, `016`.
  - `M15`: `EC-CON-001`, `007`, `008`, `009`, `013`. (`EC-CON-018 Process` is not an authorized canonical revisit in M15).

### 29.2 Competency Audit
Only canonical competencies from `meta/COMPETENCY_MATRIX.md` are used:
- `M13`: **Observe** (Primary), Trace, Explain, Estimate, Judge, Correctness.
- `M14`: **Correctness** (Primary), Diagnose, Judge, Explain, Trace.
- `M15`: **Diagnose** (Primary), Trace, Correctness, Explain, Judge.

---

## 30. Implementation Handoff & Non-Blocking Risks

### 30.1 Handoff to Next Engineering Batches
Upon Lead approval of this Design Dossier, implementation may be dispatched across three bounded tasks:
1. **Issue S5-B1:** M13 Lessons (`L13-01` to `L13-03`), `LAB-REQ-04` implementation, and `EXP-02` guide.
2. **Issue S5-B2:** M14 Lessons (`L14-01` to `L14-03`), `LAB-REQ-05` implementation, and `LAB-OPT-03` guide.
3. **Issue S5-B3:** M15 Lessons (`L15-01` to `L15-03`), `LAB-REQ-03` implementation, and `LAB-OPT-05` guide.

### 30.2 Explicit Non-Blocking Risks
1. **EXP-02 Target 1 Drift:** Target 1 contains historical subselect notes. Handled transparently by learner documentation; does not block implementation.
2. **SQLite Plan Variability Across Minor Versions:** Handled by semantic EQP checking (`SCAN` vs. `SEARCH ... USING INDEX`) rather than literal string matching.
3. **Scheduler Sensitivity in Lost Updates:** Handled by the bounded coordination contract in LAB-REQ-03, avoiding flakiness without UB.
4. **OQ-BP-006 (Environment Pinning):** Remains open; tool versions are treated as empirical observations rather than permanent curriculum constants.
5. **Historical Debt:** Issue #34 (learner validation deferred under D-027), M03 GDB debt, and M06 MIT grader debt remain non-blocking.

---

## 31. Final Recommendation

**READY FOR LESSON / ACTIVITY IMPLEMENTATION**

The Design foundation for Stage 5 Data & Concurrency (M13, M14, M15) is fully specified, architecturally aligned, technically hardened, and ready for immediate, independent lesson and lab authoring.
