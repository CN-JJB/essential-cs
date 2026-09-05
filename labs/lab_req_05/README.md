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

## Running the Lab

```bash
# Run interactive harness
python labs/lab_req_05/runner.py

# Run with machine-readable JSON output
python labs/lab_req_05/runner.py --json

# Run unit tests
python -m unittest discover -s labs/lab_req_05 -p "test_*.py"

# Clean up all generated artifacts
python labs/lab_req_05/reset.py
```
