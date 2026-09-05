# Foundations M13 Evidence Template — Databases, Storage Engines & Indexing

Use this form for **one actual learner observation**. Do not copy another learner's timing, row counts, plans, or source hashes.

---

## A — Environment / Filesystem / Capability Preflight

- Execution commit / ref: `<actual>`
- Operating System & Architecture: `<actual>`
- Python Implementation & Version: `<actual>`
- Embedded SQLite Version: `<actual>`
- `sqlite3` CLI Availability & Path: `<actual>`
- Preflight Command: `python tests/preflight_data_concurrency.py --json`
- Preflight Summary Disposition:
  - M13 Core Status: `READY`
  - LAB-REQ-04 Status: `PASS` or `ENVIRONMENT-BLOCKED / NOT RUN`
  - Writable VFS / Locking: `REQUIRED CAPABILITY PASS`

---

## B — Prediction Before Plan & Actual EQP Inspection

- Query Analyzed:
  ```sql
  SELECT id, user_id, amount, status FROM orders WHERE user_id = 42 ORDER BY id;
  ```
- Learner Prediction (prior to plan inspection):
  - Expected access path: `<SCAN / SEARCH / other>`
  - Rationale: `<learner explanation>`
- Actual Raw EQP Output (Unindexed): `<actual verbatim EQP output>`
- Semantic Classification: `<e.g. TABLE_SCAN / SCAN>`
- Actual Raw EQP Output (After `idx_orders_user`): `<actual verbatim EQP output>`
- Semantic Classification: `<e.g. INDEX_SEARCH / SEARCH>`

---

## C — Result-Set Equivalence Verification ($\Delta = 0$)

- Unindexed Result Row Count: `<actual>`
- Indexed Result Row Count: `<actual>`
- Unindexed Result Hash (SHA-256): `<actual>`
- Indexed Result Hash (SHA-256): `<actual>`
- Row Count Delta ($\Delta$): **0**
- Cryptographic Hash Match: `YES / NO`
- Principle Verified: Adding a secondary index changes execution strategy and latency, but preserves relational correctness.

---

## D — Repeated Read Timing & Cache Assumptions

- Workload: `<query string>`
- Trials: `<e.g. 10>`
- Warmup Run Completed: `YES`
- Cache-State Assumptions: `<e.g. in-memory page cache warm vs cold disk>`
- Raw Unindexed Latency Samples (ns or ms): `<actual raw array>`
- Raw Indexed Latency Samples (ns or ms): `<actual raw array>`
- Unindexed Summary: Min=`<actual>`, Median=`<actual>`, Max=`<actual>`
- Indexed Summary: Min=`<actual>`, Median=`<actual>`, Max=`<actual>`

---

## E — Write Overhead & Storage Footprint Observations

- Database File Size (Unindexed): `<actual bytes>`
- Database File Size (Indexed): `<actual bytes>`
- File Size Delta: `<actual delta bytes>`
- Bulk Insert Duration (Unindexed, e.g. 200 rows): `<actual ms>`
- Bulk Insert Duration (Indexed, e.g. 200 rows): `<actual ms>`
- Trade-off Analysis: Why does every secondary index add write amplification and storage cost?

---

## F — Inference Boundary & Universal Ratio Invariant

- Inference Limit Warning:
  Essential CS strictly forbids asserting universal speedup factors, fixed latency ratios, or universal index win guarantees.
- Observed Factors Influencing Performance:
  - Working set size vs RAM;
  - Table cardinality and selectivity;
  - Storage medium (NVMe SSD vs HDD);
  - OS page cache state.

---

## G — SQL Relational Intent vs Named Engine Reality (L13-02)

- Named Engine Evaluated: SQLite (VDBE) / PostgreSQL
- Sargable Predicate Tested:
  ```sql
  SELECT * FROM users WHERE username = 'user_42';
  ```
  - EQP Access Path: `<SEARCH / INDEX>`
- Non-Sargable Predicate Tested:
  ```sql
  SELECT * FROM users WHERE UPPER(username) = 'USER_42';
  ```
  - EQP Access Path: `<SCAN / TABLE_SCAN>`
- Engine Mechanism Explanation:
  Why wrapping a column in a function breaks standard B-tree index lookup in the absence of an expression index.

---

## H — Schema Evolution, Expand-Contract & Provenance (L13-03)

- Expand Phase Observed:
  - Statement Executed: `ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT '...';`
  - Backward Compatibility Result: `<actual>`
- Backfill Phase Observed:
  - Batch Migration Query: `UPDATE users SET status = ... WHERE ...;`
  - Rows Updated: `<actual>`
- Source of Truth vs Derived View:
  - Canonical Source: `orders`
  - Recomputed View: `user_order_summary`
  - Provenance Metadata Attached:
    `<actual JSON metadata: source_tables, recomputed_at, schema_version>`

---

## I — Changed Workload / Controlled Break Case

- Controlled Break (L13-03):
  - Attempted Statement: `ALTER TABLE users ADD COLUMN phone_number TEXT NOT NULL;`
  - Error Observed: `<actual SQLite OperationalError>`
- Scan Acceptance on Changed Workload (L13-01 / LAB-REQ-04):
  - Low Selectivity Query: `SELECT * FROM orders WHERE amount > 0.0;`
  - Observed EQP: `<SCAN>`
  - Why Planner Rejected Index: `<selectivity / cost explanation>`

---

## J — EXP-02 Source Route & Currentness Record

- Host Inspected: `git.postgresql.org` / GitHub
- Inspected Branch / Commit: `<actual>`
- Live Source Reachability: `LIVE_POSTGRESQL_SOURCE_ACCESSIBLE` or `NO LIVE SOURCE RECHECK`
- Target 1 Caveat Acknowledged: `src/backend/optimizer/plan/README` documents historical subselect planning, not universal Path->Plan architecture.
- Target 2 Finding: `cost_seqscan` vs `cost_index` formulas in `costsize.c`.
- Target 3 Finding: Buffer descriptors, Pinning (`refcount`), and Clock Sweep (`usage_count`) in `buffer/README`.
- Stop Rule Compliance: `YES` (no repo clone, no compile, no deep traversal).

---

## K — Concept, Competency, Visual & Progressive Support Audit

- Authorized Concepts Revalidated:
  - `EC-CON-001 State`
  - `EC-CON-003 Representation`
  - `EC-CON-005 Interface`
  - `EC-CON-006 Trade-off`
  - `EC-CON-008 Invariant`
  - `EC-CON-009 Correctness`
  - `EC-CON-011 Caching`
  - `EC-CON-012 Locality`
- New Concept IDs Created: **NONE**
- Canonical Competencies Practiced:
  - Primary: **Observe**
  - Secondary: **Explain**, **Estimate**, **Trace**, **Judge**, **Correctness**, **Diagnose**
- Progressive Support Ladder Verified: `Question → Hint 1 → Hint 2 → Expected Observation → Full Explanation` across all checkpoints.
- No `<details open>` used.
- Mandatory Visual Label Present in L13-01: `PLAN CHOICE IS IMPLEMENTATION AND WORKLOAD DEPENDENT`.

---

## L — Safety & Cleanup Verification

- No root / administrator privileges used: `YES`
- No host filesystem exhaustion or denial of service: `YES`
- Reset executed twice: `python labs/foundations/m13/reset.py`
- Residual untracked files: **0**
