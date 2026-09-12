# LAB-REQ-05: SQLite Transactions, Isolation, Rollback & Recovery Boundary

## Lab Overview

- **Lab ID:** `LAB-REQ-05`
- **Module:** M14 Databases — Transactions, Recovery & Isolation
- **Type:** Build — Essential CS Original
- **Baseline:** Local SQLite database file under default **rollback journal (`DELETE` mode)** and `PRAGMA synchronous = NORMAL;`.

This Required Lab investigates database transaction boundaries, committed-only visibility, competing-writer conflict handling, explicit rollback, and crash recovery boundaries.

## Checkpoint Architecture

1. **Checkpoint 1 — Invariant Definition & Committed Visibility:**
   - Initializes accounts A ($600) and B ($400) with declared invariant $\sum = 1000$.
   - Connection 1 opens `BEGIN IMMEDIATE;` and mutates Account A.
   - Connection 2 reads Account A.
   - Asserts Connection 2 observes the committed balance ($600$), proving absence of Dirty Reads ($P_1$) under SQLite's declared committed-only visibility contract.

2. **Checkpoint 2 — Bounded Writer Conflict:**
   - While Connection 1 holds active write intent, Connection 2 attempts `BEGIN IMMEDIATE;`.
   - Captures actual SQLite error code (`SQLITE_BUSY`, code 5) and driver exception disposition.
   - Rejects hardcoded error strings.
   - Verifies zero database state corruption.

3. **Checkpoint 3 — Explicit Rollback:**
   - Connection 1 issues `ROLLBACK;`.
   - Verifies both connections observe the restored baseline invariant state.

4. **Checkpoint 4 — Owned Child Interruption & Reopen Recovery:**
   - Spawns an owned child worker process (`child_worker.py`).
   - Child starts an immediate transaction, mutates data, and pauses before committing.
   - Parent terminates the child abruptly using `SIGKILL` / `kill()`.
   - Parent reaps the child process handle with a bounded watchdog timer.
   - Parent reopens the database with a fresh connection, triggering automatic rollback journal recovery.
   - Asserts all account balances reflect the last committed state ($S_0$).
   - **Critical Inference Limit:** Terminating a client process proves *client crash recovery*, NOT operating system crash recovery or physical power-loss durability.

5. **Checkpoint 5 — Backup & Storage Boundary:**
   - Copies the database using the SQLite online backup API (`Connection.backup`) to a clean destination.
   - Reopens the backup database and verifies the invariant holds.
   - Cleans up all backup and database artifacts.

## Prerequisites

- Hard prerequisites: M08 (Files, filesystems & I/O), M09 (Disks, Flash & WAL), M13 (Indexing), M14 (`L14-01` transaction boundaries, `L14-02` rollback journal & crash recovery, `L14-03` concurrency conflicts & retry discipline).
- Preflight Gate: `python tests/preflight_data_concurrency.py` (evaluates Python embedded SQLite capabilities).

## Prediction-Before-Observation

1. If Connection 1 mutates Account A inside `BEGIN IMMEDIATE;` without committing, predict whether Connection 2 can read that uncommitted value.
2. If Connection 2 attempts `BEGIN IMMEDIATE;` while Connection 1 holds write intent, predict the exact structural conflict class returned.
3. If an owned child process is terminated abruptly (`kill()`) while holding uncommitted writes, predict what state a fresh database connection observes after rollback journal recovery.

## Controlled Breaks & Failure Modes

- **Transactionless Multi-Step Update**: Executing multi-step mutations outside a transaction (`BEGIN`/`COMMIT`) permanently commits partial state upon mid-flight interruption, violating the balance conservation invariant ($\sum \ne 1000$).
- **Restore from Missing/Invalid Backup**: Attempting to restore from a non-existent or corrupted backup source fails closed without corrupting or wiping the active database.

## Exit Criteria

- Execute all 5 checkpoints via `python labs/lab_req_05/runner.py`.
- Confirm committed-only visibility ($0$ dirty reads).
- Structurally classify `SQLITE_BUSY` conflict without hardcoded error strings.
- Verify child interruption recovery under parent watchdog.
- Confirm online backup API creates consistent, recoverable replica.
- Record evidence in `course/evidence/lab-req-05-evidence-template.md`.

## Provenance & Standards

- SQLite Documentation: *Atomic Commit in SQLite* (https://www.sqlite.org/atomiccommit.html).
- SQLite Documentation: *Isolation In SQLite* (https://www.sqlite.org/isolation.html).

## Running the Lab

### Preflight Gate
```bash
python tests/preflight_data_concurrency.py
```

### Run Interactive Harness
```bash
python labs/lab_req_05/runner.py
```

### Run with Machine-Readable JSON Output
```bash
python labs/lab_req_05/runner.py --json
```

### Run Unit Tests
```bash
python -m unittest discover -s labs/lab_req_05 -p "test_*.py"
```

### Clean Up All Generated Artifacts
```bash
python labs/lab_req_05/reset.py
```
