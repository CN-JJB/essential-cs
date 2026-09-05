# LAB-REQ-04 — SQLite Indexing, Plan Inspection & Access Path Trace

LAB-REQ-04 is the required Module 13 laboratory. It investigates the physical access paths chosen by the SQLite database engine, verifies result-set equivalence between unindexed and indexed executions, and observes the trade-offs in read latency, write overhead, and storage footprint using the host's **real `sqlite3` CLI**.

## Safety and Scope

- **Local Files Only:** All databases are created in `labs/lab_req_04/` (or temporary directories).
- **Bounded Scale:** Datasets are deterministically generated with bounded size (~5,000 rows), ensuring instant smoke tests without disk or memory pressure.
- **Zero Elevated Privileges:** No root/administrator access, network ports, external database servers, credentials, or cloud resources required.
- **Idempotent Cleanup:** `reset.py` completely removes all database and journal files.

---

## Tool Requirement: `sqlite3` CLI is a Mandatory Learner Gate

Run the preflight check before attempting this lab:

```bash
python tests/preflight_data_concurrency.py
```

The interactive learner trace requires a functioning `sqlite3` CLI binary in your system `PATH`. If the CLI is not found or cannot execute:

```text
DISPOSITION: ENVIRONMENT-BLOCKED / NOT RUN
REASON: sqlite3 CLI binary is required for LAB-REQ-04 learner trace
```

Per **Curriculum Invariants**, Python's standard library `sqlite3` module cannot be quietly substituted to fabricate a CLI `PASS`. When the CLI is absent, record `ENVIRONMENT-BLOCKED / NOT RUN` in your evidence submission. All unit tests and Python-based activities remain valid.

---

## Lab Execution Flow

When the `sqlite3` CLI is installed, execute the automated harness:

```bash
python labs/lab_req_04/harness.py
```

### Checkpoint 1 — Prediction Before Plan Inspection
1. Before inspecting the query plan, predict which physical access path SQLite must use to execute:
   ```sql
   SELECT id, user_id, amount, status FROM orders WHERE user_id = 42 ORDER BY id;
   ```
2. Execute `EXPLAIN QUERY PLAN` via CLI:
   ```bash
   sqlite3 labs/lab_req_04/lab_orders.db "EXPLAIN QUERY PLAN SELECT id, user_id, amount, status FROM orders WHERE user_id = 42 ORDER BY id;"
   ```
3. Observe and classify the reported access path (`SCAN orders`).

### Checkpoint 2 — Index Creation & Result Equivalence
1. Create a secondary B-tree index:
   ```sql
   CREATE INDEX idx_orders_user ON orders(user_id);
   ```
2. Inspect the new query plan:
   ```bash
   sqlite3 labs/lab_req_04/lab_orders.db "EXPLAIN QUERY PLAN SELECT id, user_id, amount, status FROM orders WHERE user_id = 42 ORDER BY id;"
   ```
3. Observe the change to `SEARCH orders USING INDEX idx_orders_user`.
4. **Machine-Checkable Invariant:** Execute the query both before and after indexing. Verify that the result sets match exactly ($\Delta = 0$ rows, identical cryptographic hash). Adding an index changes performance, never declarative correctness.

### Checkpoint 3 — Repeated Read Timing & Inference Limits
1. Perform a warmup execution to populate buffer cache.
2. Run repeated trials (e.g., 10 trials) measuring execution latency.
3. Record raw samples, min, max, and median.
4. **Inference Limit:** Timing results are hardware- and environment-specific. Essential CS strictly forbids asserting universal speedup factors or fixed ratios.

### Checkpoint 4 — Write Cost & Storage Footprint
1. Observe database file size before and after index creation (`os.path.getsize` or `ls -l`).
2. Measure bulk insert latency into the unindexed table vs the indexed table.
3. Note that maintaining the secondary B-tree requires additional I/O and disk blocks on every write.

### Checkpoint 5 — Scan Acceptance on Changed Workload
1. Execute a query with low selectivity or an un-sargable predicate:
   ```sql
   EXPLAIN QUERY PLAN SELECT * FROM orders WHERE amount > 0.0;
   ```
2. Observe that the query planner chooses a full table scan (`SCAN`) despite the existence of `idx_orders_user`, demonstrating that index availability does not guarantee index selection.

---

## Reset Utility

To clean up all database artifacts:

```bash
python labs/lab_req_04/reset.py
```

Record all findings using `course/evidence/lab-req-04-evidence-template.md`.
