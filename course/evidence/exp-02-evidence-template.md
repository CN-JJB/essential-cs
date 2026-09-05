# EXP-02 Evidence Template — PostgreSQL Planner & Buffer Route

Use this form for **one actual source inspection**. Do not copy another learner's revision, date, formula excerpts, or notes.

---

## 0 — Course Reference Benchmark (Implementation Baseline)

- Reference Inspection Date: `2026-09-04`
- Reference Commit: `7344937cbe640cd8c5304cefe7d6b726187ad4ab`
- Reference Branch: `master` (development branch; PostgreSQL 18.6 is separate current stable release/doc line)
- Official Host: `https://git.postgresql.org/gitweb/?p=postgresql.git`
- Canonical Route (3 Paths):
  1. `src/backend/optimizer/plan/README`
  2. `src/backend/optimizer/path/costsize.c`
  3. `src/backend/storage/buffer/README`

---

## 1 — Learner Inspection Identity & Source Reachability

- Inspection date / time: `<actual>`
- Official source host: `<git.postgresql.org or GitHub mirror>`
- Branch / ref inspected: `<actual e.g. master>`
- Exact PostgreSQL commit / revision inspected: `<actual commit hash>`
- Source access disposition:
  - `LIVE_POSTGRESQL_SOURCE_ACCESSIBLE`, or
  - `NO LIVE SOURCE RECHECK / EXP-02 LIVE SOURCE OBSERVATION NOT RUN`

> **Guardrail:** If live source access is unavailable, record `NO LIVE SOURCE RECHECK`. The Course Reference Benchmark above may be used as **REFERENCE EVIDENCE ONLY**; never fabricate a commit hash or source excerpt.

---

## 2 — Exact Bounded Route Audit

Record whether each target exists at the exact inspected revision:

1. `src/backend/optimizer/plan/README`
   - Exists: `<actual>`
   - Link / reference: `<actual>`
2. `src/backend/optimizer/path/costsize.c`
   - Exists: `<actual>`
   - Link / reference: `<actual>`
3. `src/backend/storage/buffer/README`
   - Exists: `<actual>`
   - Link / reference: `<actual>`

---

## 3 — Target 1 Finding: Historical Subselect Caveat

In `src/backend/optimizer/plan/README`:
- Target 1 Caveat Confirmation:
  - Does this README serve as a general Path->Plan architecture overview, or is it focused on subselect/subplan planning history?
  - Learner Observation: `<actual description of document scope>`
- Key subquery planning tradeoff noted in document: `<actual paraphrase>`
- Inference Limit: What this document does **not** prove: `<actual>`

---

## 4 — Target 2 Finding: Cost Estimation in `costsize.c`

At `cost_seqscan()` and `cost_index()`:
- `cost_seqscan` formula components:
  - Disk page I/O factor: `<e.g. baserel->pages * seq_page_cost>`
  - CPU tuple processing factor: `<e.g. baserel->tuples * cpu_tuple_cost>`
  - Startup cost observed: `<e.g. 0.0>`
- `cost_index` cost components:
  - Index page I/O vs heap page random I/O: `<actual>`
  - Why `random_page_cost` default exceeds `seq_page_cost`: `<actual>`
- Inference Limit: Why cost units are dimensionless heuristics and not physical execution milliseconds: `<learner explanation>`

---

## 5 — Target 3 Finding: Buffer Pool Management in `buffer/README`

In `src/backend/storage/buffer/README`:
- Buffer Descriptor state & BufferTag: `<actual paraphrase>`
- Pinning mechanism (`refcount` increment): `<why it prevents concurrent eviction>`
- Clock Sweep replacement algorithm:
  - Role of `usage_count`: `<actual>`
  - Victim selection condition: `<refcount == 0 && usage_count == 0>`
- Stopping point verification: Stopped at clock sweep; did not inspect lwlock or WAL redo.

---

## 6 — Supplemental Reference Citation

- Upper-level architecture reference consulted: `src/backend/optimizer/README`
- Explicit Role: Supplemental reviewer context only; **not** a substitute for the three bounded learner targets.

---

## 7 — Stop-Rule Compliance Audit

- [ ] Did not clone or download the full PostgreSQL git repository.
- [ ] Did not compile PostgreSQL locally.
- [ ] Did not wander into unbounded helper callees beyond the three targets.
- [ ] Followed link-and-inspection-first methodology.

---

## 8 — Licensing & Provenance Review

- PostgreSQL License reviewed: `YES`
- Source code vendored or mirrored into course repo: expected **NO**
- Excerpt copied into submission: `<NO / if YES, exact file + lines>`
- Required attribution retained: `YES`

---

## 9 — Reviewer Synthesis

Write one paragraph synthesizing:
1. What the PostgreSQL source confirmed regarding query plan cost estimation;
2. How the buffer pool maintains page residency safety via pinning while using Clock Sweep for eviction;
3. Why `plan/README` contains historical subselect details rather than a modern generic architecture overview;
4. What concepts (`EC-CON-005 Interface`, `EC-CON-006 Trade-off`, `EC-CON-011 Caching`, `EC-CON-012 Locality`) were directly verified in production code.
