# LAB-REQ-04 Evidence Template — SQLite Indexing, Plan Inspection & Access Path Trace

Use this form for **one actual execution**. Do not copy example outputs, timing, plan texts, or hashes from another host.

---

## A — Execution Identity & Capability

- Execution base commit: `<actual execution base commit>`
- Working commit / ref: `<actual>`
- OS / kernel / architecture: `<actual>`
- Python implementation / version: `<actual>`
- `sqlite3` CLI path: `<actual or None>`
- `sqlite3 --version` evidence: `<actual or None>`
- Preflight disposition: `<actual>`
- LAB-REQ-04 disposition: `<actual: PASS / ENVIRONMENT-BLOCKED / NOT RUN>`

> **Learner Gate Warning:**
> If `sqlite3` CLI is missing from PATH or cannot execute, stop the interactive CLI trace and record:
> ```text
> TOOL MISSING: sqlite3 CLI is required for LAB-REQ-04 learner trace
> ENVIRONMENT-BLOCKED / NOT RUN
> ```
> Do not substitute Python standard library `sqlite3` execution to claim a full CLI `PASS`.

---

## B — Checkpoint 1: Prediction Before Plan & Unindexed Trace

Command:
```bash
sqlite3 labs/lab_req_04/lab_orders.db "EXPLAIN QUERY PLAN SELECT id, user_id, amount, status FROM orders WHERE user_id = 42 ORDER BY id;"
```

Record:
- Pre-observation prediction: `<SCAN / SEARCH>`
- Learner prediction rationale: `<actual>`
- Actual CLI EQP verbatim output: `<actual>`
- Semantic access path classification: `<actual: e.g. SCAN orders / TABLE_SCAN>`

---

## C — Checkpoint 2: Index Creation & Result-Set Equivalence

1. Index creation statement:
   ```sql
   CREATE INDEX idx_orders_user ON orders(user_id);
   ```
2. Indexed CLI EQP verbatim output: `<actual>`
3. Semantic access path classification: `<actual: e.g. SEARCH orders USING INDEX idx_orders_user>`
4. Result-Set Equivalence Audit:
   - Unindexed row count: `<actual>`
   - Indexed row count: `<actual>`
   - Unindexed SHA-256 hash: `<actual>`
   - Indexed SHA-256 hash: `<actual>`
   - Row count delta ($\Delta$): `<actual>`
   - Hash match verified: `<YES / NO>`

---

## D — Checkpoint 3: Repeated Read Timing & Symmetric Warmup Protocol

Command / Script:
```bash
python labs/lab_req_04/harness.py
```

Record:
- Symmetric warmup executed for both unindexed and indexed: `<YES / NO>`
- Number of trials: `<e.g. 10>`
- Cache assumption: `<in-memory OS page cache warm vs cold>`
- Raw unindexed latency samples (ns or ms): `<actual raw array>`
- Raw indexed latency samples (ns or ms): `<actual raw array>`
- Unindexed summary: Min=`<actual>`, Median=`<actual>`, Max=`<actual>`
- Indexed summary: Min=`<actual>`, Median=`<actual>`, Max=`<actual>`
- Inference limit note: Timing depends on hardware, cache state, and OS scheduling; no universal speedup ratio is asserted.

---

## E — Checkpoint 4: Write Overhead & Storage Footprint

- Unindexed database file size: `<actual bytes>`
- Indexed database file size: `<actual bytes>`
- File size delta: `<actual delta bytes>`
- Batch insert size: `<actual rows, e.g. 200>`
- Bulk insert duration (unindexed): `<actual ms>`
- Bulk insert duration (indexed): `<actual ms>`
- Analysis: Why secondary indexes add write cost when indexed columns are affected: `<learner explanation>`

---

## F — Checkpoint 5: Changed Workload & Planner Choice on Relevant Index

Relevant index created:
```sql
CREATE INDEX idx_orders_amount ON orders(amount);
```

Query tested:
```sql
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE amount > 0.0;
```

Record:
- Actual CLI EQP verbatim output: `<actual>`
- Semantic classification: `<actual: SCAN / SEARCH / other>`
- Observed Planner Choice & Reasoning: `<learner analysis of why the planner selected this access path based on selectivity, cost model, or heuristics>`
- Inference Limits: `<why this observation does not constitute a universal planner law>`

---

## G — Reset & Safety Audit

- [ ] Ran entirely inside `labs/lab_req_04/` or temporary files.
- [ ] No root / sudo / administrator permissions required.
- [ ] Reset utility executed cleanly: `python labs/lab_req_04/reset.py`
- [ ] Residual untracked files: **0**

---

## H — Reviewer Synthesis

Write one paragraph synthesizing:
1. What the query planner chose before and after index creation;
2. How result-set equivalence ($\Delta = 0$) demonstrates the boundary between relational correctness and performance;
3. The concrete engineering costs (storage footprint and write latency) of maintaining a secondary index;
4. How the query planner evaluated the changed workload query against the relevant index.
