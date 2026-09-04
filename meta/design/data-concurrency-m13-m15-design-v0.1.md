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
   - **Zero new concept IDs introduced.** All concepts remain within the 18 canonical entries in `meta/CONCEPT_REGISTRY.md`.
   - **EC-CON-014 Consistency (一致性)** enters its canonical first home in **M14 (`L14-02`)**. Definition: *"The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee. It must be qualified; 'consistent' does not mean merely fresh, durable, or correct in every sense."* The qualifier is mandatory. ACID "Consistency" is explicitly disambiguated as application invariant preservation rather than an engine-level visibility contract.
   - **EC-CON-015 Concurrency (并发)** enters its canonical first home in **M15 (`L15-01`)**. Definition: *"Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations."* Concurrency is fundamentally distinguished from physical parallelism. M12's event loop and M14's transaction overlap are treated strictly as previews.
   - **R6 Schema Evolution & Provenance:** Handled in M13 `L13-03` as an **application pattern** spanning existing concepts (`EC-CON-001`, `003`, `005`, `008`). No new concept ID is created.
3. **Lab & Source Expedition Contracts:**
   - **LAB-REQ-04 (SQLite Query Plans & Indexing):** Required baseline is the `sqlite3` CLI. Python stdlib `sqlite3` is permitted for fixture generation and automated evaluation, but is not an equivalent interactive replacement. If `sqlite3` CLI is absent, the learner path is classified `ENVIRONMENT-BLOCKED / NOT RUN`. Fixture sizes are determined by implementation smoke (small: 1–2 pages; medium: multi-page), rejecting hardcoded "100 vs 50,000 rows" constants. Truthful planner scans on small tables or low selectivity are explicitly accepted and celebrated.
   - **LAB-REQ-05 (SQLite Transactions & Recovery):** Required baseline is local SQLite with **rollback journal** (`DELETE` mode). WAL mode is an optional comparison. Dual-connection architecture verifies committed-only visibility and writer serialization (`SQLITE_BUSY`). Child process termination via `SIGKILL` tests client crash recovery; Design strictly prohibits inferring physical power-loss durability from process interruption.
   - **LAB-REQ-03 (POSIX Threads Race & Rendezvous):** Required baseline is C11 + POSIX threads on canonical Linux. The broken path uses C11 atomics (`<stdatomic.h>`) for defined atomic accesses in a compound read-modify-write update, avoiding C language data race / Undefined Behavior (UB). To prevent flaky scheduling, the design specifies a bounded coordination contract (phase handoff / attempt budget), rejecting fixed percentage assertions ($\ge 95\%$). Mutex repair, condition-variable while-loop rendezvous, and an owned-child deadlock watchdog with explicit timeout are fully specified.
   - **LAB-OPT-03 (PostgreSQL EXPLAIN & Isolation):** Strictly Optional. Requires explicit rollback design for `EXPLAIN ANALYZE` mutation statements. PostgreSQL/Docker must never become hidden Core requirements.
   - **LAB-OPT-05 (OSTEP Semaphore Rendezvous):** Strictly Optional and **link-only** (commit `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`). Zero bundled code, tests, or skeletons.
   - **EXP-02 (PostgreSQL Source Expedition):** Preserves the exact three canonical paths (`src/backend/optimizer/plan/README`, `src/backend/optimizer/path/costsize.c`, `src/backend/storage/buffer/README`). The learner-facing card explicitly documents Target 1's historical subselect drift. The parent `optimizer/README` is cited as supplemental reviewer context, not a substitute or fourth canonical step. No PostgreSQL compilation.
4. **Environment & OQ-BP-006 Preservation:**
   - Preflight contract classifies capabilities into Required, Optional, Environment-Sensitive, and Privileged.
   - OQ-BP-006 remains explicitly **OPEN**. Current tool versions are treated as empirical evidence, not permanent curriculum constants.

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
| **LAB-REQ-03 Scheduling** | `sched_yield()` alone does not guarantee a lost-update observation across all OS schedulers. | **Adopted with boundary** | Design bounded coordination (phase handoff or attempt budget). Reject hardcoded "$\ge 95\%$" or "100%" occurrence assertions. |
| **LAB-REQ-04 Dataset Sizes** | 100 vs. 50,000 rows was empirical smoke evidence, not a universal constant. | **Adopted** | Specify small (1–2 pages) vs. medium (multi-page) based on implementation smoke; do not canonize specific row counts. |
| **LAB-REQ-04 CLI Baseline** | `sqlite3` CLI is required for authentic plan and tool interaction. | **Adopted** | Missing CLI = `ENVIRONMENT-BLOCKED / NOT RUN`. Python is not an interactive substitute. |
| **LAB-REQ-05 Baseline** | Rollback journal is SQLite default; WAL is optional comparison. | **Adopted** | Establish rollback journal (`DELETE`) as default; WAL as bounded extension. No fixed exception string matching. |
| **Process Interruption** | `SIGKILL` tests client abnormal termination, not hardware power loss. | **Adopted** | Explicit inference boundary: Process kill $\ne$ power loss. |
| **L15-03 Python GIL** | Free-threaded Python 3.14.7 / PEP 779; GIL is implementation detail. | **Adopted** | Do not teach GIL as a Python language invariant or `counter += 1` as guaranteed to fail. |
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

- **Module Purpose:** Establish the mental model of a database engine: declarative SQL $\to$ engine parser/planner $\to$ access path $\to$ page/buffer I/O $\to$ result set. Unpack the trade-offs of B-tree indexing and schema invariants.
- **Primary Competency:** **Observe** (query execution plans, table scans vs. index searches, storage overhead, timing variance).
- **Secondary Competencies:** Trace, Explain, Estimate, Judge, Correctness.
- **Canonical Concepts Revisit:** `EC-CON-001 State`, `EC-CON-003 Representation`, `EC-CON-005 Interface`, `EC-CON-006 Trade-off`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`, `EC-CON-011 Caching`, `EC-CON-012 Locality`.
- **Application Pattern:** Schema evolution, reader/writer compatibility, migration trade-offs, source of truth vs. derived data, lightweight provenance (R6).

---

## 6. Lesson L13-01 Design — “Why is my query fast/slow?”

### 6.1 Learner Question & Capability Transition
- **Learner Question:** "Why does the exact same `SELECT` statement run in sub-milliseconds on some tables, but take seconds on others—and why does adding an index sometimes make no difference at all?"
- **Capability Transition:** Moves from treating a database as a black box where queries have mysterious speeds to inspecting the engine's access path (`EXPLAIN QUERY PLAN`), understanding page-level I/O, and evaluating B-tree index trade-offs.

### 6.2 Mechanism Model & Claim Layer
- **Mechanism:** Tables are stored on disk in fixed-size pages (e.g., SQLite 4,096 bytes). A table scan (`SCAN TABLE`) reads every page sequentially ($O(N)$ pages). A B-tree index stores keys and row pointers in balanced multi-way tree pages; lookups probe root $\to$ internal $\to$ leaf pages ($O(\log_B N)$ pages, where $B \approx 100\text{--}1000$).
- **Claim Layers:**
  - *PRINCIPLE:* $O(\log_B N)$ tree lookup vs. $O(N)$ linear scan; random vs. sequential I/O trade-off; index maintenance overhead on mutations.
  - *SPECIFICATION:* SQL declarative semantics specify the result set, not the retrieval path.
  - *IMPLEMENTATION:* SQLite query planner cost estimation; `EXPLAIN QUERY PLAN` output format (`SCAN`, `SEARCH`, `USING INDEX`, `USING COVERING INDEX`).
  - *CURRENT PRACTICE:* SQLite 4KB default page size; automatic temporary index generation heuristics.

### 6.3 Hands-On Activity & Controlled Failure
- **Activity:** In the `sqlite3` CLI, load a synthetic table at two bounded scales (Small: 1–2 pages; Medium: hundreds of pages). Execute queries on indexed vs. unindexed columns. Capture `EXPLAIN QUERY PLAN`.
- **Prediction Before Observation:** Before running `EXPLAIN QUERY PLAN`, learner must predict whether the engine will choose a table scan or an index lookup based on table size and predicate selectivity.
- **Controlled Break:** Execute a query matching $>50\%$ of rows with an index available. Observe that SQLite chooses `SCAN TABLE` despite the index. Explain why: Traversing the index and performing random I/O for 50% of the rows is slower than a sequential scan of all pages.

### 6.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Adding an index always makes queries faster."* (False: On small tables or low selectivity, indexes add overhead; indexes always slow down `INSERT`/`UPDATE`).
  2. *"`EXPLAIN QUERY PLAN` executes the query and measures actual time."* (False: EQP displays the static chosen plan, not execution measurements).
- **What You Can Ignore — For Now:** Internal B-tree page balancing and page-split algorithms; VDBE bytecode instructions; LSM-trees; bitmap index structures.

### 6.5 Progressive Support Ladder
- **Question:** How do you determine whether SQLite will use an index for `SELECT * FROM orders WHERE user_id = 42`?
- **Hint 1:** The declarative query does not state how rows are fetched. You need to ask SQLite for its chosen access path.
- **Hint 2:** Prefix the query with `EXPLAIN QUERY PLAN` in the `sqlite3` shell.
- **Expected Observation:** The detail column reports `SEARCH orders USING INDEX idx_orders_user (user_id=?)` or `SCAN orders`.
- **Full Explanation:** SQLite's planner evaluates available indexes. If `idx_orders_user` exists and selectivity justifies it, EQP outputs `SEARCH ... USING INDEX`. If no index exists, it outputs `SCAN orders`.

### 6.6 Visual Specification & Exit Criteria
- **Visual:** Diagram showing a declarative SQL query entering the query engine, branching into two access paths: Path A (Sequential Page Scan visiting all physical disk pages) vs. Path B (B-Tree traversal visiting Root $\to$ Internal $\to$ Leaf $\to$ Data Page). Prominently labeled: **PLAN CHOICE IS WORKLOAD AND IMPLEMENTATION DEPENDENT**.
- **Exit Criteria:** Learner captures an actual EQP output showing both `SCAN` and `SEARCH ... USING INDEX`, and writes an evidence-based explanation of why an index is not a universal performance solution.

---

## 7. Lesson L13-02 Design — “What is SQL doing?”

### 7.1 Learner Question & Capability Transition
- **Learner Question:** "If SQL only describes what data I want, who decides how to get it, and where is the line between relational logic and storage engine reality?"
- **Capability Transition:** Moves from viewing SQL as an imperative programming language to understanding it as a declarative interface (`EC-CON-005`) backed by a query optimization and execution pipeline.

### 7.2 Mechanism Model & Claim Layer
- **Mechanism:** Relational Model (Codd 1970). Relational algebra operations: Selection ($\sigma$), Projection ($\pi$), Join ($\bowtie$). The query pipeline: SQL text $\to$ Parser $\to$ Abstract Syntax Tree $\to$ Logical Query Plan $\to$ Query Optimizer / Planner $\to$ Physical Plan $\to$ Execution Engine (Iterator/Volcano model: `open()`, `next()`, `close()`). The storage engine manages physical pages, record formats (slotted pages), and buffer pool caching.
- **Claim Layers:**
  - *PRINCIPLE:* Relational algebra equivalence; declarative interface abstraction; separation of logical query from physical access path.
  - *SPECIFICATION:* ANSI/ISO SQL standard grammar and semantics.
  - *IMPLEMENTATION:* SQLite query engine pipeline; virtual database engine (VDBE) opcodes; rowid table structure.
  - *CURRENT PRACTICE:* SQLite single-file database architecture; absence of dedicated background server processes.

### 7.3 Hands-On Activity & Controlled Failure
- **Activity:** Query a multi-table SQLite database. Compare an un-sargable query (`WHERE UPPER(username) = 'ALICE'`) with an indexed query (`WHERE username = 'Alice'`).
- **Prediction Before Observation:** Predict whether SQLite can use a standard B-tree index on `username` when wrapped in a function call.
- **Controlled Break:** Observe that wrapping the indexed column in `UPPER(...)` forces a full table scan (`SCAN TABLE`), breaking the index abstraction. Explain why: B-tree indexes are sorted by raw column values, not transformed function outputs.

### 7.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"SQL executes in the exact order written (SELECT first, then FROM)."* (False: Logical processing evaluates `FROM` $\to$ `WHERE` $\to$ `GROUP BY` $\to$ `HAVING` $\to$ `SELECT` $\to$ `ORDER BY`).
  2. *"Every relational database uses the Volcano iterator model."* (False: Modern columnar/analytical engines use vectorized execution or JIT compilation).
- **What You Can Ignore — For Now:** Cost-based join order dynamic programming (Selinger optimizer); VDBE register allocation details; cost-model tuning parameters.

### 7.5 Progressive Support Ladder
- **Question:** Why does `SELECT * FROM users WHERE id + 1 = 100` fail to use the primary key index on `id`?
- **Hint 1:** Look at the left side of the comparison operator. Is `id` isolated?
- **Hint 2:** The query planner evaluates expressions. It does not perform algebraic inversion to rewrite `id + 1 = 100` into `id = 99`.
- **Expected Observation:** EQP displays `SCAN users` instead of `SEARCH users USING INTEGER PRIMARY KEY`.
- **Full Explanation:** Expressions on indexed columns prevent index usage unless an expression index exists. Rewriting the predicate to `WHERE id = 99` enables direct index search.

### 7.6 Visual Specification & Exit Criteria
- **Visual:** Two-layer architectural diagram. Top Layer: SQL Declarative Contract (`SELECT`, `FROM`, `WHERE` relational intent). Bottom Layer: Named Engine Implementation (Parser $\to$ Planner $\to$ Physical Access Path $\to$ Slotted Page Storage Engine). Shows the abstraction boundary and how expression predicates leak through to force scans.
- **Exit Criteria:** Learner traces one query through logical vs. physical access paths and explains the performance difference between a sargable and non-sargable predicate.

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
  - *Source-of-Truth vs. Derived Data:* Authoritative operational state vs. materialized views/cached aggregates. Derived data is always recomputable from the source of truth.
  - *Lightweight Provenance:* Storing metadata (`created_at`, `updated_by`, `schema_version`) to track state lineage.
- **Claim Layers:**
  - *PRINCIPLE:* Invariant preservation across state transitions; trade-offs of redundancy (normalization vs. denormalization); expand-contract migration lifecycle.
  - *SPECIFICATION:* SQL DDL constraint definitions (`ALTER TABLE`).
  - *IMPLEMENTATION:* SQLite `ALTER TABLE` capabilities and limitations (e.g., historical constraints on dropping columns vs. modern table recreations).
  - *CURRENT PRACTICE:* Online schema migration tools (gh-ost, pt-online-schema-change) in enterprise environments.

### 8.3 Hands-On Activity & Controlled Failure
- **Activity:** Design a user account schema. Add a new required field (`email_verified BOOLEAN NOT NULL`) to an existing populated table.
- **Prediction Before Observation:** Predict what happens when you execute `ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL;` on a table with existing rows without specifying a default value.
- **Controlled Break:** SQLite returns an error (`Cannot add a NOT NULL column with default value NULL`). Explain the failure: Adding a non-nullable column to existing data violates the table's invariant for historical rows unless a default or backfill is provided.

### 8.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Schema migrations can always be performed instantly with a single ALTER TABLE."* (False: On large tables, schema changes can trigger full table rewrites and exclusive locks).
  2. *"Derived data is just as authoritative as source-of-truth data."* (False: Derived data can become stale or inconsistent; only source-of-truth state is canonical).
- **What You Can Ignore — For Now:** Distributed schema registries (Avro/Protobuf); W3C PROV-O semantic ontologies; enterprise ETL data pipelines; NoSQL document schema design.

### 8.5 Progressive Support Ladder
- **Question:** How do you safely add a non-nullable `status` column to a populated table without migration errors?
- **Hint 1:** Existing rows must satisfy the `NOT NULL` constraint immediately upon column creation.
- **Hint 2:** Provide a sensible default value in the `ALTER TABLE` statement.
- **Expected Observation:** `ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'ACTIVE';` succeeds.
- **Full Explanation:** Supplying `DEFAULT 'ACTIVE'` allows the engine to satisfy the invariant for all existing rows without requiring immediate row rewrites in metadata-only evolution engines.

### 8.6 Visual Specification & Exit Criteria
- **Visual:** Schema Evolution Lifecycle diagram showing Version $N$ migrating to Version $N+1$ across three stages: Stage 1 (Expand: Add new nullable column, application dual-writes), Stage 2 (Backfill: Batch update historical rows), Stage 3 (Contract: Readers consume new column, old column dropped). Includes a sidecar showing Source-of-Truth table feeding a Derived View with a Provenance timestamp.
- **Exit Criteria:** Learner designs a multi-step migration script that adds a new column, backfills historical data, and demonstrates backward reader compatibility.

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
- Bounded dataset sizes determined by implementation smoke test:
  - *Small Scale:* Sized so the table occupies 1–2 pages (e.g., ~50–100 rows).
  - *Medium Scale:* Sized so the table occupies hundreds of pages (e.g., tens of thousands of rows; exact count determined at smoke time).
- Synthetic data generator generates deterministic, pseudo-random records using a fixed seed.

### 9.3 Experimental Procedure
1. **Checkpoint 1 — Baseline & Prediction:**
   - Execute query on unindexed `user_id`: `SELECT * FROM orders WHERE user_id = ?;`
   - Record predicted access path.
   - Run `EXPLAIN QUERY PLAN` in `sqlite3` CLI and capture actual output.
2. **Checkpoint 2 — Index Creation & EQP Inspection:**
   - Create index: `CREATE INDEX idx_orders_user ON orders(user_id);`
   - Run `EXPLAIN QUERY PLAN` for the selective query.
   - Assert semantic access path: Detail contains `SEARCH orders USING INDEX idx_orders_user`. (Do not bind to exact ASCII tree formatting).
3. **Checkpoint 3 — Result Equivalence Verification:**
   - Verify that results returned by the indexed query are identical to the unindexed query:
     $$\text{Result}(\text{Query}_{\text{unindexed}}) \equiv \text{Result}(\text{Query}_{\text{indexed}})$$
4. **Checkpoint 4 — Workload Measurement & Trade-offs:**
   - Measure repeated read query execution times (capturing median and spread across multiple iterations, accounting for warm cache).
   - Observe write overhead: Measure execution time of bulk `INSERT` statements with and without the secondary index.
   - Observe database file size inflation via filesystem `ls -l` / file stat before and after index creation.
5. **Checkpoint 5 — Truthful Scan Acceptance:**
   - Execute a query matching a large fraction of table rows (e.g., `WHERE status = 'ACTIVE'`).
   - If SQLite chooses `SCAN TABLE` despite an available index, record this truthful result and explain why cost estimation preferred sequential I/O.

### 9.4 Machine-Checkable vs. Reviewer-Required Gates
- **Machine-Checkable:**
  - Automated runner executes SQL script;
  - Parses EQP detail string semantically (`SCAN` vs. `SEARCH ... USING INDEX`);
  - Asserts result set equivalence ($\Delta = 0$ rows);
  - Asserts DB file size increased after index creation.
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
  - *IMPLEMENTATION:* SQLite locking architecture: Single active writer; shared read locks; `SQLITE_BUSY` conflict handling; committed-only visibility.
  - *CURRENT PRACTICE:* PostgreSQL default Read Committed vs. MySQL InnoDB default Repeatable Read.

### 13.3 Canonical Concept First Home: EC-CON-014 Consistency
- **Exact First Home:** M14 / `L14-02`.
- **Mandatory Canonical Definition:**
  > **“The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee. It must be qualified; 'consistent' does not mean merely fresh, durable, or correct in every sense.”**
- **Disambiguation Mandate in Teaching:**
  - Disambiguate ACID $C$ from systems consistency. ACID "Consistency" is application-level invariant preservation.
  - Transaction consistency is defined by a **named isolation level** (e.g., Read Committed guarantees observers never see uncommitted state transitions).
  - Explicitly warn learners: Transaction isolation on a single database node is not distributed consistency (which M17 revisits).

### 13.4 Hands-On Activity & Controlled Failure
- **Activity:** Open two separate terminal sessions with `sqlite3` connecting to the same database. Session 1 begins an immediate transaction and updates a row. Session 2 queries the row.
- **Prediction Before Observation:** Predict whether Session 2 will observe the uncommitted modification made by Session 1.
- **Controlled Break:** Session 2 observes the committed value, proving absence of dirty reads. Session 2 then attempts to execute `BEGIN IMMEDIATE;` and immediately fails with a busy/lock conflict, demonstrating SQLite writer serialization.

### 13.5 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Consistency means data is always up to date and correct."* (False: Consistency must be qualified by a named contract; an observer reading a consistent snapshot under Snapshot Isolation may read valid, non-corrupt historical state).
  2. *"Serializable isolation means the database only executes one query at a time."* (False: Engines execute transactions concurrently, intervening only when conflicting interleavings threaten equivalence to a serial schedule).
- **What You Can Ignore — For Now:** Serializable Snapshot Isolation (SSI) dependency graph cycle detection; distributed consensus protocols (Raft/Paxos); cross-shard distributed transactions.

### 13.6 Progressive Support Ladder
- **Question:** If Connection 1 has an uncommitted update, why doesn't Connection 2 see the new value?
- **Hint 1:** What isolation level does SQLite enforce by default?
- **Hint 2:** SQLite enforces committed-only visibility; uncommitted changes in the journal or WAL are invisible to other connections.
- **Expected Observation:** Connection 2's `SELECT` returns the original value until Connection 1 commits.
- **Full Explanation:** SQLite prevents Dirty Reads ($P_1$). Under its visibility guarantee, observers only see committed state transitions.

### 13.7 Visual Specification & Exit Criteria
- **Visual:** Timeline interleaving diagram comparing Connection 1 ($T_1$) and Connection 2 ($T_2$). Displays $T_1$ modifying Row A, $T_2$ reading Row A (observing original committed value under Read Committed), and $T_2$ attempting to write (blocked by exclusive lock). Prominently displays the full text of **EC-CON-014 Consistency** with its mandatory named qualifier.
- **Exit Criteria:** Learner reproduces a concurrent conflict across two connections, correctly identifies the prevented anomaly, and states `EC-CON-014` with its required qualifier.

---

## 14. Lesson L14-03 Design — “How do I design an atomic write?”

### 14.1 Learner Question & Capability Transition
- **Learner Question:** "When multiple processes write to a database, how do I design write operations that handle lock conflicts, avoid deadlocks, and remain safe against retries?"
- **Capability Transition:** Moves from writing naive single-statement queries to designing robust, retryable transactional write operations with deadlock awareness and idempotency previews.

### 14.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *Atomic Single-Statement vs. Multi-Statement Transactions:* Using atomic expressions (`UPDATE inventory SET stock = stock - 1 WHERE id = 10 AND stock > 0;`) vs. multi-step transactions (`BEGIN IMMEDIATE ... COMMIT`).
  - *Conflict Handling & Whole-Transaction Retries:* Handling `SQLITE_BUSY` / lock conflicts. Retries must restart at the outer transaction boundary, not blindly retry a failed mid-transaction statement.
  - *Deadlock Light:* Coffman circular wait conditions in database locks. Prevented by consistent lock ordering (e.g., always update Account A before Account B).
  - *Idempotency Preview:* Ensuring that re-executing a transaction (e.g., following a network timeout or retry) does not duplicate state mutations (using unique transaction tokens or idempotency keys).
- **Claim Layers:**
  - *PRINCIPLE:* Atomic state transitions; deadlock preconditions; idempotency invariant ($f(f(x)) = f(x)$); transaction retry boundaries.
  - *SPECIFICATION:* SQL transaction retry and conflict error specifications.
  - *IMPLEMENTATION:* SQLite busy handler timeout (`sqlite3_busy_timeout`); `BEGIN DEFERRED` vs. `BEGIN IMMEDIATE` vs. `BEGIN EXCLUSIVE`.
  - *CURRENT PRACTICE:* Exponential backoff with jitter in application retry loops.

### 14.3 Hands-On Activity & Controlled Failure
- **Activity:** Write a Python script simulating two concurrent workers transferring balances. Worker 1 transfers Account 1 $\to$ Account 2; Worker 2 transfers Account 2 $\to$ Account 1 using `BEGIN DEFERRED`.
- **Prediction Before Observation:** Predict what happens when both workers read their source accounts, then both attempt to upgrade their shared read locks to exclusive write locks simultaneously.
- **Controlled Break:** Both workers attempt lock upgrade; SQLite detects lock deadlock and rejects one connection with `SQLITE_BUSY` (`database is locked`).
- **Correction:** Refactor both workers to use `BEGIN IMMEDIATE`, acquiring write intent locks upfront and serializing access safely.

### 14.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Retrying a single failed SQL query inside a transaction is sufficient."* (False: If a statement fails or encounters a conflict, the entire transaction must be rolled back and retried from the beginning).
  2. *"Setting a high busy timeout guarantees your write will never fail."* (False: Under sustained write contention, timeouts expire; applications must handle persistent contention gracefully).
- **What You Can Ignore — For Now:** Distributed transaction managers; sagas; compensating transaction workflows; two-phase locking wait-for-graph cycle detection algorithms.

### 14.5 Progressive Support Ladder
- **Question:** Why does using `BEGIN DEFERRED` cause concurrent writer deadlocks in SQLite?
- **Hint 1:** When does `BEGIN DEFERRED` actually acquire a write lock?
- **Hint 2:** It starts with a shared read lock and attempts to upgrade to an exclusive write lock on the first write.
- **Expected Observation:** If two connections hold shared locks, neither can upgrade to an exclusive lock, resulting in an immediate lock conflict.
- **Full Explanation:** `BEGIN IMMEDIATE` acquires a reserved write lock at transaction start, preventing multiple connections from entering conflicting upgrade cycles.

### 14.6 Visual Specification & Exit Criteria
- **Visual:** Flowchart comparing Naive Retry vs. Transaction-Boundary Retry. Displays Worker encountering a conflict, issuing an immediate `ROLLBACK`, entering an exponential backoff sleep, and restarting at `BEGIN IMMEDIATE`. Includes an idempotency key check preventing duplicate processing.
- **Exit Criteria:** Learner designs a multi-statement transaction script featuring upfront write-locking (`BEGIN IMMEDIATE`), whole-transaction retry on busy conflict, and invariant verification.

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
   - Record the actual SQLite result code and driver exception (e.g., `sqlite3.OperationalError` reporting database locking / busy conflict).
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
- **Canonical Concepts Revisit:** `EC-CON-001 State`, `EC-CON-007 Specification`, `EC-CON-008 Invariant`, `EC-CON-009 Correctness`, `EC-CON-013 Isolation` (synchronization scope), `EC-CON-018 Process`.

---

## 17. Lesson L15-01 Design — “Why is my threaded code wrong?”

### 17.1 Learner Question & Capability Transition
- **Learner Question:** "Why does running code in two threads produce different, incorrect results every time, and why does my code pass tests when I run it once but fail under load?"
- **Capability Transition:** Moves from assuming sequential line-by-line execution to understanding preemptive kernel scheduling, arbitrary instruction interleaving, and anchoring the formal definition of **EC-CON-015 Concurrency**.

### 17.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *Threads vs. Processes (`EC-CON-018`):* Processes possess private virtual address spaces. Threads within a process share the heap, global variables, and file descriptors, but maintain private program counters, registers, and stacks.
  - *Interleaving:* The kernel scheduler preempts threads arbitrarily. Instructions interleave across threads.
  - *Logical Race Condition vs. C Data Race (UB):* A data race in C (concurrent unsynchronized accesses where at least one is a write) is **Undefined Behavior (UB)** under ISO C11 §5.1.2.4. Compilers may optimize away loops containing data races.
  - *The Essential CS Teaching Solution:* To demonstrate race conditions rigorously without UB, we use C11 atomics (`<stdatomic.h>`) with relaxed memory order for individual reads and writes. Individual memory operations are strictly legal and defined, but the multi-step compound read-modify-write operation is non-atomic, deterministically exposing lost updates.
- **Claim Layers:**
  - *PRINCIPLE:* Concurrency vs. parallelism; logical race conditions; non-deterministic interleaving.
  - *SPECIFICATION:* ISO/IEC 9899:2011 (C11) atomics specification; POSIX IEEE Std 1003.1-2024 thread model.
  - *IMPLEMENTATION:* Linux NPTL thread scheduling; glibc thread management.
  - *CURRENT PRACTICE:* GCC/Clang thread compilation flags (`-pthread`).

### 17.3 Canonical Concept First Home: EC-CON-015 Concurrency
- **Exact First Home:** M15 / `L15-01`.
- **Mandatory Canonical Definition:**
  > **“Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations.”**
- **Disambiguation Mandate in Teaching:**
  - Explicitly distinguish concurrency (system composition allowing interleaved progress) from parallelism (physical simultaneous execution on multiple cores).
  - Prove that concurrency bugs occur on single-core processors due to preemptive time-slicing.

### 17.4 Hands-On Activity & Controlled Failure
- **Activity:** Compile and run a C11 program with two threads executing a compound update on an atomic counter using `atomic_load_explicit` and `atomic_store_explicit` with a cooperative yield (`sched_yield()`).
- **Prediction Before Observation:** Predict the final counter value after two threads each execute 10,000 increments.
- **Controlled Break:** The final counter value is significantly less than 20,000 (typically ~10,000–15,000), proving real lost updates despite 100% legal atomic memory accesses.

### 17.5 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"Concurrency and parallelism are the exact same thing."* (False: Concurrency is about structure and interleaving; parallelism is about physical simultaneous hardware execution).
  2. *"Making a variable atomic automatically makes compound multi-step operations correct."* (False: Atomic reads and writes prevent memory corruption, but compound state transitions remain non-atomic).
- **What You Can Ignore — For Now:** Formal C++ memory model release-acquire formal operational proofs; lock-free algorithms; kernel futex internals.

### 17.6 Progressive Support Ladder
- **Question:** Why did our counter lose thousands of updates even though every load and store was an atomic C11 operation?
- **Hint 1:** Trace the sequence of events when Thread 1 reads `42`.
- **Hint 2:** Thread 1 reads `42`. Before it can store `43`, Thread 2 also reads `42`.
- **Expected Observation:** Both threads compute `43` and write `43`. One increment vanished.
- **Full Explanation:** Individual memory operations were atomic, but the compound state transition (Read $\to$ Compute $\to$ Store) was not. Interleaving caused a lost update.

### 17.7 Visual Specification & Exit Criteria
- **Visual:** Interleaving Trace diagram contrasting Concurrency (single core, time-sliced interleaved execution blocks) vs. Parallelism (dual cores, simultaneous timeline bars). Shows Thread 1 reading Counter $= 42$, Thread 2 reading Counter $= 42$, both computing $43$, and both writing $43$. Prominently displays the full text of **EC-CON-015 Concurrency**.
- **Exit Criteria:** Learner draws an instruction interleaving diagram explaining a lost update and correctly recites `EC-CON-015`.

---

## 18. Lesson L15-02 Design — “How do I make it right?”

### 18.1 Learner Question & Capability Transition
- **Learner Question:** "How do I protect shared state without introducing deadlocks, and how do threads coordinate when one must wait for another to finish?"
- **Capability Transition:** Moves from observing concurrency bugs to implementing synchronization primitives: mutual exclusion via POSIX mutexes, condition synchronization via condition variables, and deadlock avoidance.

### 18.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *POSIX Mutex (`pthread_mutex_t`):* Guarantees that at most one thread executes a critical section at any instant. Enforces acquire/release memory visibility. Does *not* guarantee fair FIFO ordering among waiting threads.
  - *POSIX Condition Variable (`pthread_cond_t`):* Mechanism for event rendezvous. Atomically releases associated mutex and suspends calling thread in `pthread_cond_wait`. Upon wake, re-acquires the mutex.
  - *Spurious Wakeups & The Mandatory While Loop:* A thread may wake up without any explicit signal. The condition predicate must **always** be checked in a `while` loop:
    ```c
    pthread_mutex_lock(&lock);
    while (!predicate_is_true) {
        pthread_cond_wait(&cond, &lock);
    }
    // Critical invariant guaranteed
    pthread_mutex_unlock(&lock);
    ```
  - *Deadlock & Coffman Conditions:* Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. Avoidance via lock acquisition hierarchies.
- **Claim Layers:**
  - *PRINCIPLE:* Mutual exclusion; Dijkstra critical section invariants; condition synchronization; Coffman deadlock conditions.
  - *SPECIFICATION:* The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024 (`pthread_mutex_*`, `pthread_cond_*`).
  - *IMPLEMENTATION:* Linux futex-backed mutex and condition variable implementation in glibc.
  - *CURRENT PRACTICE:* Compiler warnings for uninitialized mutex attributes.

### 18.3 Hands-On Activity & Controlled Failure
- **Activity:** Protect the compound update from L15-01 with a POSIX mutex. Implement a condition-variable rendezvous where Worker 2 waits for Worker 1 to produce data.
- **Prediction Before Observation:** Predict whether replacing the `while` loop with an `if` statement around `pthread_cond_wait` is safe under POSIX specifications.
- **Controlled Break:** Demonstrate the spurious wakeup hazard theoretically and explain why POSIX specification requires re-checking the predicate in a `while` loop.
- **Controlled Deadlock:** Implement a reversed lock acquisition order (Thread 1: Lock A $\to$ B; Thread 2: Lock B $\to$ A) using a controlled barrier handshake so both threads hold their first lock before requesting their second lock. Run under an owned-child watchdog with a configured timeout.

### 18.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"A mutex guarantees that threads take turns fairly."* (False: POSIX mutexes do not guarantee fairness; newly unblocked threads can re-acquire locks ahead of long-waiting threads).
  2. *"A condition variable notification means the predicate is currently true."* (False: A signal wakes a thread, but by the time the thread re-acquires the mutex, another thread may have altered the predicate; spurious wakeups can also occur).
- **What You Can Ignore — For Now:** Lock-free hazard pointers; reader-writer lock starvation engineering; priority inheritance protocols in real-time kernels.

### 18.5 Progressive Support Ladder
- **Question:** Why does POSIX Issue 8 explicitly state that `pthread_cond_wait` may return spuriously?
- **Hint 1:** Consider low-level kernel signal interruptions or multi-processor wake optimizations.
- **Hint 2:** If waking up does not guarantee the predicate changed, how must you structure your check?
- **Expected Observation:** The waiting code must re-evaluate the predicate: `while (!ready) pthread_cond_wait(...)`.
- **Full Explanation:** Kernel scheduling and multiprocessor memory events permit spurious wakeups. The `while` loop ensures the thread never proceeds unless the shared predicate is genuinely true.

### 18.6 Visual Specification & Exit Criteria
- **Visual:** Mutex & Condition Rendezvous diagram. Panel 1: Mutex Lock Invariant (one thread in critical section, other threads blocked in wait queue). Panel 2: Condition Variable Protocol (Worker 1 holds lock $\to$ `pthread_cond_wait` atomically unlocks and sleeps $\to$ Worker 2 acquires lock, updates predicate, calls `signal` $\to$ Worker 1 re-awakens, re-acquires lock, and loops on predicate).
- **Exit Criteria:** Learner repairs a broken threaded counter with a mutex (verifying 100% correct counts) and implements a condition rendezvous with a verified `while` loop predicate.

---

## 19. Lesson L15-03 Design — “Thread or async?”

### 19.1 Learner Question & Capability Transition
- **Learner Question:** "Should I build my application with multi-threading or asynchronous event loops, and what does the Python GIL actually do to my code?"
- **Capability Transition:** Moves from treating "threads vs. async" as an ideological flame war to evaluating concurrency models based on resource costs, blocking behavior, and runtime realities.

### 19.2 Mechanism Model & Claim Layer
- **Mechanism:**
  - *OS Threads:* Preemptive kernel scheduling; private execution stack (2–8 MB); kernel context switches; transparent blocking on system calls. Ideal for CPU-intensive parallel work across physical cores.
  - *Asynchronous Event Loops:* Cooperative single-threaded multitasking (`async`/`await`); lightweight coroutines (bytes of memory); non-blocking I/O multiplexing (`epoll`/`kqueue`/`IOCP`). Cooperative yields occur only at explicit `await` points.
  - *CPython GIL Reality:* The Global Interpreter Lock is a CPython implementation detail, not a Python language invariant. The GIL protects interpreter internals; it does **not** make Python application code thread-safe. Bytecode switches between instructions cause lost updates in compound expressions like `counter += 1`.
  - *Currentness Note:* Upstream Python 3.14.7 / PEP 779 free-threaded build provides an experimental option to disable the GIL, but conventional GIL builds remain common.
- **Claim Layers:**
  - *PRINCIPLE:* Preemptive vs. cooperative scheduling; memory footprint trade-offs; I/O multiplexing mechanics.
  - *SPECIFICATION:* Python language syntax (`async`/`await` coroutines).
  - *IMPLEMENTATION:* CPython interpreter bytecode evaluation loop and GIL implementation.
  - *CURRENT PRACTICE:* Python 3.13 / 3.14 free-threaded builds (`--disable-gil`).

### 19.3 Hands-On Activity & Controlled Failure
- **Activity:** Run a companion Python script with two threads incrementing a shared variable `counter += 1`.
- **Prediction Before Observation:** Predict whether Python's GIL prevents lost updates when two native threads update a shared variable without a lock.
- **Controlled Break:** On standard CPython, the final count is less than the expected total because `counter += 1` compiles into four distinct bytecode opcodes (`LOAD_GLOBAL`, `LOAD_CONST`, `BINARY_OP`, `STORE_GLOBAL`), and thread switching occurs between opcodes.
- **Comparison:** Implement the same task using `asyncio` and explain why cooperative concurrency avoids data races between `await` points, while still requiring logical locking across multi-step `await` workflows.

### 19.4 Misconceptions & What You Can Ignore
- **Misconceptions:**
  1. *"The GIL means multi-threaded Python programs never need mutexes."* (False: The GIL protects interpreter memory; compound application updates lose data).
  2. *"Async code is always faster than threaded code."* (False: Async code avoids thread memory overhead for high-concurrency I/O, but provides zero parallel speedup for CPU-bound computations).
- **What You Can Ignore — For Now:** Deep CPython C-API extension internals; custom asyncio event loop policy implementations; Rust async executor internals.

### 19.5 Progressive Support Ladder
- **Question:** If the GIL only lets one thread execute Python bytecode at a time, how can `x += 1` lose updates?
- **Hint 1:** Disassemble `x += 1` using Python's `dis` module.
- **Hint 2:** Is `x += 1` a single atomic opcode?
- **Expected Observation:** It requires loading `x`, loading `1`, computing addition, and storing `x`.
- **Full Explanation:** Preemptive thread switching can occur between `BINARY_OP` and `STORE_GLOBAL`. Both threads read the same initial value and store the same incremented value.

### 19.6 Visual Specification & Exit Criteria
- **Visual:** Execution Model Comparison matrix. Columns: OS Preemptive Threads vs. Cooperative Async Event Loop vs. CPython GIL Reality. Rows: Scheduling Type, Memory per Task, CPU Parallelism, Data Race Vulnerability across Steps, Best Workload Fit.
- **Exit Criteria:** Learner disassembles a Python compound operation, explains why the GIL does not guarantee application thread safety, and articulates when to choose threads vs. async based on workload constraints.

---

## 20. Required Lab LAB-REQ-03 Design — POSIX Threads Race, Rendezvous & Progress Boundaries

### 20.1 Overview & Required Baseline
- **Lab ID:** `LAB-REQ-03`
- **Module Placement:** M15 Concurrency: Threads, Races & Synchronization
- **Type:** Build — Essential CS original
- **Execution Baseline:** Canonical Linux with `gcc -std=c11 -pthread`.

### 20.2 The UB-Free Broken Path Contract
- **No Undefined Behavior:** The broken path strictly uses C11 atomics (`<stdatomic.h>`) with `memory_order_relaxed`. Individual reads and writes are defined, legal atomic operations under ISO C11.
- **Scheduler Evidence Contract:**
  - Because `sched_yield()` alone is not a deterministic scheduler guarantee across all kernel platforms, the design specifies a **controlled phase-handoff / attempt-budget contract**:
  - The fixture runs a loop where two threads execute non-atomic compound updates:
    ```c
    int val = atomic_load_explicit(&counter, memory_order_relaxed);
    sched_yield();
    atomic_store_explicit(&counter, val + 1, memory_order_relaxed);
    ```
  - If a natural scheduler run produces a lost update within an attempt budget (e.g., 5 runs of 10,000 iterations), the learner records the natural trace.
  - If a host scheduler serializes threads without interruption, the fixture provides a cooperative step barrier demonstrating the exact interleaved execution trace.
  - **Prohibition:** Tests must never assert hardcoded "$\ge 95\%$" or "100%" failure probabilities or fixed erroneous count ranges.

### 20.3 Mutex Repair & Condition Rendezvous
- **Mutex Repair:** Wrapping the compound update in `pthread_mutex_lock` / `unlock` guarantees that every completed run satisfies the invariant ($\text{final\_count} == 2 \times \text{iterations}$).
- **Condition Variable Rendezvous:** Worker 2 waits for Worker 1 to signal that a shared buffer is ready. The wait is enclosed in a mandatory `while (!buffer_ready) pthread_cond_wait(&cond, &mutex);` loop.

### 20.4 Controlled Deadlock & Watchdog Harness
- **Deadlock Precondition:** Thread 1 acquires Lock A $\to$ Lock B; Thread 2 acquires Lock B $\to$ Lock A.
- **Deterministic Coordination:** Threads synchronize via a start gate so both threads hold their first lock before either attempts to acquire its second lock.
- **Watchdog Execution:** The deadlock test runs in an owned child process. The parent watchdog enforces a configured timeout (e.g., 2–3 seconds).
- **Inference Boundary:** The parent records that both threads entered their respective first locks and stalled on their second locks before interpreting the timeout as deadlock evidence. The timeout duration is an execution parameter, not a curriculum constant.

---

## 21. Optional Content Design Disposition (LAB-OPT-03 & LAB-OPT-05)

### 21.1 LAB-OPT-03 Design — PostgreSQL EXPLAIN & Isolation Comparison
- **Status:** Strictly Optional.
- **Scope:** Adapts official PostgreSQL 18.x documentation for query plan inspection (`EXPLAIN (ANALYZE, BUFFERS)`) and repeatable read serialization conflict detection.
- **Safety Gate:** Any `EXPLAIN ANALYZE` examples that execute mutations (`INSERT`/`UPDATE`) must be wrapped inside a transaction and rolled back (`BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`).
- **Dependency Boundary:** PostgreSQL and Docker are not required. If unavailable, the lab is recorded as **`OPTIONAL LAB NOT RUN / TOOL UNAVAILABLE`**.

### 21.2 LAB-OPT-05 Design — OSTEP Semaphore Rendezvous
- **Status:** Strictly Optional.
- **Scope:** Adopt as **link-only** pointer to OSTEP homework commit `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2` (`threads-sema/rendezvous.c`).
- **Rights & Provenance:** No code, tests, or text from the unlicensed `ostep-homework` repository will be copied, vendored, or bundled into Essential CS.

---

## 22. S5 Preflight & Environment Contract

The S5 preflight script must evaluate host capabilities before Lab execution without closing OQ-BP-006:

```
+-----------------------------------------------------------------------------------------+
| S5 Environment Preflight Check                                                          |
+-----------------------------------------------------------------------------------------+
| 1. POSIX Kernel & OS Architecture: Linux / POSIX environment verified                   |
| 2. Python Environment: Python 3.x available (record actual version)                     |
| 3. SQLite Library: Embedded sqlite3 version reported                                    |
| 4. SQLite CLI: sqlite3 binary checked in PATH -> [PASS | BLOCKED]                       |
| 5. C Compiler: GCC or Clang checked -> [PASS | BLOCKED]                                 |
| 6. C11 Atomics: <stdatomic.h> compilation test -> [PASS | BLOCKED]                       |
| 7. POSIX Threads: -pthread linking test -> [PASS | BLOCKED]                             |
| 8. Local Storage: Course-owned local writable directory -> [PASS | BLOCKED]             |
| 9. Child Watchdog: Process spawn & SIGKILL reaping capability -> [PASS | BLOCKED]       |
| 10. Optional Tools: PostgreSQL / psql / Docker checked -> [AVAILABLE | SKIP]            |
+-----------------------------------------------------------------------------------------+
```

### Truthful Preflight Dispositions
- `REQUIRED CAPABILITY PASS`: All Required Core capabilities confirmed.
- `ENVIRONMENT-BLOCKED / NOT RUN`: Specific missing tool blocks a specific Lab (e.g., missing `sqlite3` CLI blocks LAB-REQ-04; missing `gcc` blocks LAB-REQ-03).
- `OPTIONAL TOOL UNAVAILABLE / SKIP`: Optional PostgreSQL or Docker missing; optional labs skipped without penalty.
- `NO LIVE SOURCE RECHECK`: Network disconnected; EXP-02 uses local source snapshot or cached reference.

---

## 23. Evidence-Template Contracts

Later implementation must produce standardized evidence templates for learner records:

### 23.1 M13 Evidence Template Structure
- **Section A:** Environment / CLI / SQLite versions recorded.
- **Section B:** L13-01 prediction + actual CLI `EXPLAIN QUERY PLAN` capture.
- **Section C:** Result set equivalence confirmation ($\Delta = 0$).
- **Section D:** Read timing distributions and cache-state assumptions.
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
- **Section B:** Declared transaction balance invariant ($\sum = 1000$).
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
- **Section F:** Condition variable while-loop predicate rendezvous verification.
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
- **Bound & Safety Confirmation:** Explicit confirmation that inspection stopped at the bounded lines; zero compilation attempted; zero source code vendored.

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
  |-- Points to specific tools, syntax, or inspection methods (e.g., EQP or while-loop guards).
  v
[ Tier 4: Expected Observation ]
  |-- Describes the pattern or semantic structure to expect (using placeholders, never fake data).
  v
[ Tier 5: Full Explanation ]
  |-- Complete systems explanation unpacking root causes, trade-offs, and invariants.
```

- **Formatting Rule:** HTML `<details open>` is strictly prohibited. Hints must remain collapsed until explicitly opened by the learner.
- **Truthful Placeholder Rule:** Expected observations must never invent exact timings, page counts, or machine-specific memory addresses.

---

## 25. Visual Contract

All visual assets must be original, editable diagrams complying with `meta/VISUAL_AND_WRITING_POLICY.md`:

| Lesson / Lab | Visual Title | Core Pedagogical Content | Mandatory Inscription / Label |
|---|---|---|---|
| **L13-01** | Query Access Paths & Storage | SQL intent branching into Sequential Scan vs. B-Tree index lookup visiting disk pages. | **"PLAN CHOICE IS IMPLEMENTATION AND WORKLOAD DEPENDENT"** |
| **L13-02** | Declarative Intent vs. Engine Reality | Two-layer diagram: Declarative SQL intent mapped to Engine Parser, Planner, and Storage Engine. | Abstraction boundary and sargable vs. non-sargable predicate leakage. |
| **L13-03** | Schema Evolution Lifecycle | Expand-Contract three-stage migration pattern (Expand $\to$ Backfill $\to$ Contract) with Source of Truth vs. Derived View. | Source of Truth is authoritative; Derived Data is recomputable. |
| **L14-01** | Transaction State & Recovery Boundary | State transition from $S_0$ through dirty buffer changes to $S_1$ via `COMMIT` vs. Rollback Journal restoration. | Rollback reverts uncommitted mutations; client kill $\ne$ power loss. |
| **L14-02** | Concurrent Interleaving & Visibility | Timeline showing $T_1$ and $T_2$ interleavings, dirty read prevention, and writer lock conflicts. | **EC-CON-014 Consistency: Full canonical definition with mandatory qualifier.** |
| **L14-03** | Transaction-Boundary Retry | Flowchart comparing naive statement retry with whole-transaction rollback, exponential backoff, and idempotency key check. | Whole-transaction retry boundary. |
| **L15-01** | Concurrency vs. Parallelism & Interleaving | Visual contrasting single-core time-slicing vs. multi-core simultaneous execution, detailing atomic lost update. | **EC-CON-015 Concurrency: Full canonical definition.** |
| **L15-02** | Mutex Invariant & Condition Rendezvous | Mutex critical section exclusion combined with condition variable predicate while-loop wait protocol. | Mandatory while-loop predicate evaluation guard. |
| **L15-03** | Concurrency Execution Models | Comparison matrix: OS Preemptive Threads vs. Async Event Loops vs. CPython GIL reality. | No universal winner; workload-driven model selection. |
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
| - Atomic counter lost-update demonstration (erroneous count under compound update).     |
| - Mutex-protected counter verification (100% target count reached).                     |
| - Condition rendezvous ordering verification.                                           |
| - Deadlock watchdog timeout termination (< 5 seconds).                                  |
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
- **Process & Thread Boundaries:** Thread pools bounded to 2–4 workers. Deadlock demonstrations must run in an owned child process governed by an automated watchdog timer, guaranteeing that learner shells never freeze.

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
3. **Scheduler Sensitivity in Lost Updates:** Handled by the bounded coordination / attempt-budget contract in LAB-REQ-03, avoiding flakiness without UB.
4. **OQ-BP-006 (Environment Pinning):** Remains open; tool versions are treated as empirical observations rather than permanent curriculum constants.
5. **Historical Debt:** Issue #34 (learner validation deferred under D-027), M03 GDB debt, and M06 MIT grader debt remain non-blocking.

---

## 31. Final Recommendation

**READY FOR LESSON / ACTIVITY IMPLEMENTATION**

The Design foundation for Stage 5 Data & Concurrency (M13, M14, M15) is fully specified, architecturally aligned, technically hardened, and ready for immediate, independent lesson and lab authoring.
