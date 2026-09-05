# Foundations M14 Evidence Template — Databases: Transactions, Recovery & Isolation

Use this template for **one actual learner observation**. Do not prefill or copy another learner's timing, error strings, process return codes, or host versions.

---

## A — SQLite Environment, Journal Mode & Synchronous Settings

- Execution commit / ref: `<actual HEAD commit SHA>`
- Host Operating System & Architecture: `<actual OS and CPU arch>`
- Python Implementation & Version: `<actual python runtime>`
- Embedded SQLite Version (`sqlite3.sqlite_version`): `<actual version>`
- Database File Path: `<actual course-owned path>`
- Journal Mode Configuration (`PRAGMA journal_mode`): `<actual: DELETE>`
- Synchronous Configuration (`PRAGMA synchronous`): `<actual: 1 / NORMAL or other>`
- Command Executed: `python labs/foundations/m14/activity_l14_01.py`

---

## B — Declared Transaction Balance Invariant

- Schema:
  ```sql
  CREATE TABLE accounts (
      id TEXT PRIMARY KEY,
      balance INTEGER NOT NULL CHECK (balance >= 0)
  );
  ```
- Declared System Invariant: $\text{balance}_A + \text{balance}_B = 1000$
- Initial Baseline State ($S_0$):
  - Account A: `<actual balance>`
  - Account B: `<actual balance>`
  - Initial Total Balance: `<actual sum>`
- Invariant Holds at $S_0$: `<YES / NO>`

---

## C — Dual-Connection Committed-Only Visibility Timeline

- Activity Script: `labs/foundations/m14/activity_l14_02.py`
- Connection 1 Action: `BEGIN IMMEDIATE; UPDATE accounts SET balance = 500 WHERE id = 'A';`
  - Connection 1 Uncommitted Value Observed by Conn 1: `<actual>`
- Connection 2 Action: `SELECT balance FROM accounts WHERE id = 'A';`
  - Connection 2 Value Observed while Conn 1 Transaction is Open: `<actual>`
- Dirty Read ($P_1$) Detected: `<YES / NO>`
- Named Guarantee Verified: **SQLite committed-only visibility under the declared local locking/journal baseline** (do not label as generic ANSI Read Committed).

---

## D — Second-Writer Conflict & Driver Disposition

- Connection 2 Competing Action: `BEGIN IMMEDIATE;` while Connection 1 holds write intent.
- Conflict Caught: `<YES / NO>`
- Raw Driver Exception Type: `<actual exception class, e.g. OperationalError>`
- Raw Driver Message: `<actual driver message string without fixed expectation>`
- SQLite Error Name (`sqlite_errorname`): `<actual, e.g. SQLITE_BUSY or none>`
- SQLite Error Code (`sqlite_errorcode`): `<actual code number, e.g. 5 or none>`
- Driver Disposition Classification: `<BUSY_CONFLICT_CAPTURED / GENERIC_SQLITE_ERROR_CAPTURED / OTHER>`
- State Corruption Observed: `<YES / NO>`

---

## E — Explicit Rollback Verification

- Connection 1 Rollback Action: `ROLLBACK;`
- Connection 1 Balances Observed Post-Rollback: `<actual>`
- Connection 2 Balances Observed Post-Rollback: `<actual>`
- Invariant Total Post-Rollback: `<actual sum>`
- Verified Property: Explicit `ROLLBACK` aborts all uncommitted mutations and restores baseline $S_0$ without leaving partial state transitions.

---

## F — Child Interruption Point & Process Reaping Record

- Subprocess Harness: `labs/lab_req_05/harness.py` (Checkpoint 4)
- Child Process Spawning Method: `subprocess.Popen([sys.executable, child_worker_path, db_path])`
- Child Process PID: `<actual PID>`
- Child State at Interruption:
  - Transaction initiated: `BEGIN IMMEDIATE;`
  - Partial mutation executed: `UPDATE accounts SET balance = 100 WHERE id = 'A';`
  - Child reported signal: `CHILD_MUTATED`
- Interruption Primitive: `<proc.kill() / SIGKILL / OS equivalent>`
- Watchdog Reaping Method: `proc.wait(timeout=...)`
- Child Reaped Return Code: `<actual return code / signal number>`
- Unowned / Zombie Process Residuals: `<NONE / OTHER>`

---

## G — Reopen Recovery & Journal Side-File Observation

- Journal Side-File Path: `<actual db_path-journal>`
- Journal Side-File Observed During Active Uncommitted Write: `<YES / NO>`
- Fresh Reopen Action: `sqlite3.connect(db_path)`
- Automatic Hot-Journal Rollback Recovery Triggered: `<YES / NO>`
- Journal Side-File Observed After Reopen & Recovery: `<YES / NO / CLEANED_UP>`
- Recovered Account Balances:
  - Account A: `<actual>`
  - Account B: `<actual>`
  - Total Sum: `<actual>`
- Recovery Matches Last Committed State ($S_0$): `<YES / NO>`

---

## H — Online Backup & Clean-File Restoration Verification

- Online Backup API Used: `src_conn.backup(dst_conn)`
- Clean Backup File Path: `<actual path>`
- Backup File Size (Bytes): `<actual size>`
- Reopened Backup File Verification:
  - Account A: `<actual>`
  - Account B: `<actual>`
  - Invariant Total: `<actual>`
- Backup Matches Committed State: `<YES / NO>`

---

## I — Durability Inference Limit Review

> **Critical Distinction**: Why does surviving a client process kill (`SIGKILL`) prove application crash recovery, but **NOT** physical power-loss durability?

- Learner Explanation:
  `<Explain the difference between client process termination where OS kernel and filesystem caches remain alive to preserve log records/files, versus OS crash or sudden power cut where volatile write caches may be lost or un-flushed. Explicitly note why PRAGMA synchronous settings and underlying hardware storage matter.>`

---

## J — EC-CON-014 Consistency Exact Definition & Named Qualifier

- **First Home**: M14 / `L14-02`
- **Verbatim Canonical Definition**:
  > “The relationship between allowed state transitions and what observers may see, according to a named ordering/visibility guarantee.”
- **Mandatory Named Qualifier**:
  - “Consistent” must be qualified by a named ordering/visibility guarantee;
  - Consistency is not automatically freshness;
  - Consistency is not automatically correctness in every sense;
  - Consistency is not durability;
  - ACID $C$ is application invariant preservation, not the whole systems-consistency concept;
  - Single-node transaction isolation is not distributed consistency.

---

## K — ACID Consistency vs. Transaction Isolation Disambiguation

- Learner Disambiguation:
  `<Explain why ACID 'C' (application invariant preservation, e.g. sum(balance) == 1000) differs fundamentally from transaction isolation levels (e.g. Read Committed vs Serializable) and from distributed consistency models.>`

---

## L — Transaction-Boundary Retry & Idempotency Preview

- Script: `labs/foundations/m14/activity_l14_03.py`
- Lock-Upgrade Hazard Observation:
  - Collision Observed with `BEGIN DEFERRED`: `<YES / NO>`
  - Mechanism: `<Explain the actual order: both connections establish read transactions; one connection becomes the writer first; the other connection's later read-to-write upgrade fails because a writer already exists. Do not claim both upgrades fail symmetrically.>`
- Upfront Write-Intent Serialization:
  - Statement Used: `BEGIN IMMEDIATE;`
  - Upgrade Collision Prevented: `<YES / NO>`
- Boundary Retry Protocol:
  - Action upon busy/locked result: if a transaction is active, `ROLLBACK`; then bounded exponential backoff and retry from `BEGIN IMMEDIATE`. If `BEGIN IMMEDIATE` itself failed before a transaction began, record that no rollback was required.
- Idempotency Token Verification:
  - Token Key Used: `<actual token string>`
  - First Execution Disposition: `<actual: COMMITTED>`
  - Duplicate Re-execution Disposition: `<actual: ALREADY_PROCESSED>`
  - Non-Transient Constraint / Syntax Error Handling: `<Explain why non-transient errors must fail fast rather than retry>`

---

## M — Concepts, Competencies, Visuals & Cleanup Audit

- Canonical Concept First Home:
  - `EC-CON-014 Consistency` (L14-02): `<VERIFIED / NOT VERIFIED>`
- Canonical Concept Revisits Checked:
  - `EC-CON-001 State`: `<CHECKED>`
  - `EC-CON-006 Trade-off`: `<CHECKED>`
  - `EC-CON-007 Specification`: `<CHECKED>`
  - `EC-CON-008 Invariant`: `<CHECKED>`
  - `EC-CON-009 Correctness`: `<CHECKED>`
  - `EC-CON-013 Isolation`: `<CHECKED>`
  - `EC-CON-016 Durability`: `<CHECKED>`
- Competencies Assessed:
  - Primary: `Correctness`
  - Secondary: `Diagnose`, `Judge`, `Explain`, `Trace`
- Visual Artifacts Inspected:
  - L14-01: Transaction State & Recovery Boundary (includes "client kill $\ne$ power loss")
  - L14-02: Concurrent Interleaving & Visibility (includes EC-CON-014 definition + qualifier)
  - L14-03: Transaction-Boundary Retry (includes no "all errors retry" guardrail)
- Progressive Support Ladder Verified: No `<details open>` tags present.
- Cleanup Idempotence:
  - Command: `python labs/foundations/m14/reset.py`
  - Run 1 Removed Count: `<actual>`
  - Run 2 Removed Count: `0` (Idempotent PASS)
