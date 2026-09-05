# M13 Activity Suite — Databases, Storage Engines & Indexing

These course-owned laboratory fixtures support Module 13 (M13) on local files using SQLite and Python standard library tooling.

## Safety & Environment Invariants

- **Course-Scoped Local Files:** All database files are created strictly inside `labs/foundations/m13/` (or temporary directories during automated testing). Zero modification to system directories.
- **Privilege & System Boundaries:** Zero root/administrator privileges required; zero external network access, credentials, or cloud services needed.
- **Bounded Resources:** Deterministic synthetic generators produce bounded row counts (~2000 rows). Never exhausts disk space or memory.
- **Observation Truthfulness:** Python stdlib `sqlite3` provides fixture generation and programmatic testing. For interactive CLI inspection, see `labs/lab_req_04/`. If a tool is missing, report the status truthfully without simulating tool presence.

---

## Preflight Verification

Before running activities, verify your host environment:

```bash
python tests/preflight_data_concurrency.py --json

# Opt in to public PostgreSQL source reachability probe for EXP-02:
python tests/preflight_data_concurrency.py --json --check-postgres-source
```

---

## L13-01 — Query Plans, Indexing & Access Paths

Explore how the database engine translates SQL queries into physical access paths:

```bash
python labs/foundations/m13/fixture_l13.py
```

### Observation Focus:
1. **Unindexed Table Scan:** Prior to creating a secondary index on `orders.user_id`, observe `EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42;`. The engine reports a `SCAN` (reading all pages).
2. **Indexed Search:** After executing `CREATE INDEX idx_orders_user ON orders(user_id);`, observe the updated plan. The engine switches to `SEARCH` using the secondary B-tree index.
3. **Plan Choice Invariant:** Plan selection is implementation- and workload-dependent. Indexes accelerate selective lookup queries, but add write and storage overhead.

---

## L13-02 — SQL Declarative Intent vs Named Engine Reality

Examine the boundary between declarative relational intent and physical evaluation:

### Sargability (Search-Argument-Able) Predicates:
Run `fixture_l13.py` to compare:
- **Sargable Query:** `SELECT * FROM users WHERE username = 'user_42';` — Direct column comparison allows the engine to perform a B-tree search.
- **Non-Sargable Query:** `SELECT * FROM users WHERE UPPER(username) = 'USER_42';` — Wrapping the column in an expression prevents direct B-tree root-to-leaf traversal, forcing a full table scan (`SCAN`) unless a specialized expression index exists.

---

## L13-03 — Schema Evolution, Invariants & Derived Data

Execute the Expand-Contract migration workflow and derived view recomputation:

```bash
python labs/foundations/m13/schema_evolution.py
```

### Observation Focus:
1. **Controlled Break:** Notice that attempting to add a `NOT NULL` column without a `DEFAULT` value to an already populated table in SQLite fails with `OperationalError`.
2. **Expand Phase:** Add the column with a safe `DEFAULT` value, enabling older and newer readers to operate concurrently.
3. **Backfill Phase:** Perform a bounded batch migration of existing rows to new operational values.
4. **Source of Truth vs Derived Views:** Aggregates in `user_order_summary` are derived from the canonical `orders` table. Recomputation can be performed idempotently while tracking provenance metadata (`source_tables`, `recomputed_at`, `schema_version`).

---

## Reset & Cleanup

To clean up all generated database and journal files:

```bash
python labs/foundations/m13/reset.py
```
