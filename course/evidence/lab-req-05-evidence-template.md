# LAB-REQ-05 Evidence Template — SQLite Transactions, Isolation, Rollback & Recovery Boundary

Use this form for **one actual execution**. Do not copy example outputs, timing, exception strings, process return codes, or host versions from another system.

---

## A — Execution Identity & Capability

- Execution base commit: `<actual execution base commit SHA>`
- Working commit / ref: `<actual HEAD commit SHA>`
- Operating System & Architecture: `<actual OS and CPU architecture>`
- Python Implementation & Version: `<actual python runtime>`
- Embedded SQLite Version (`sqlite3.sqlite_version`): `<actual version>`
- Journal Mode Configuration (`PRAGMA journal_mode`): `<actual: DELETE>`
- Synchronous Configuration (`PRAGMA synchronous`): `<actual: 1 / NORMAL or other>`
- Command Executed: `python labs/lab_req_05/runner.py`
- Overall Result: `<PASS / FAIL>`

---

## B — Checkpoint 1: Invariant Definition & Committed Visibility

- Declared System Invariant: $\text{balance}_A + \text{balance}_B = 1000$
- Connection 1 Action:
  ```sql
  BEGIN IMMEDIATE;
  UPDATE accounts SET balance = 500 WHERE id = 'A';
  ```
  - Connection 1 Uncommitted Value Observed: `<actual>`
- Connection 2 Action:
  ```sql
  SELECT balance FROM accounts WHERE id = 'A';
  ```
  - Connection 2 Observed Balance: `<actual>`
- Checkpoint 1 Verdict: `<PASS / FAIL>`
- Dirty Read ($P_1$) Detected: `<NO / YES>`
- Named Visibility Guarantee: **SQLite committed-only visibility under the declared local locking/journal baseline** (do not label as generic ANSI Read Committed).

---

## C — Checkpoint 2: Bounded Writer Conflict

- Competing Action: Connection 2 attempts `BEGIN IMMEDIATE;` while Connection 1 holds active write intent.
- Conflict Caught: `<YES / NO>`
- Raw Driver Exception Class: `<actual exception type, e.g. OperationalError>`
- Raw Driver Exception Message: `<actual driver message, e.g. database is locked>`
- SQLite Error Name (`sqlite_errorname`): `<actual, e.g. SQLITE_BUSY or None>`
- SQLite Error Code (`sqlite_errorcode`): `<actual code number, e.g. 5 or None>`
- Driver Disposition Classification: `<BUSY_CONFLICT_CAPTURED / GENERIC_SQLITE_ERROR_CAPTURED / OTHER>`
- Database Invariant Post-Conflict Check:
  - Account A: `<actual>`
  - Account B: `<actual>`
  - Invariant Sum: `<actual>`
- State Corruption Observed: `<NO / YES>`
- Checkpoint 2 Verdict: `<PASS / FAIL>`

---

## D — Checkpoint 3: Explicit Rollback Restoration

- Connection 1 Action: `ROLLBACK;`
- Connection 1 Post-Rollback Balances: `<actual>`
- Connection 2 Post-Rollback Balances: `<actual>`
- Invariant Total: `<actual>`
- State Matches Baseline $S_0$: `<YES / NO>`
- Checkpoint 3 Verdict: `<PASS / FAIL>`

---

## E — Checkpoint 4: Owned Child Interruption & Recovery

- Child Process Command: `python labs/lab_req_05/child_worker.py <db_path>`
- Child Process Owned PID: `<actual PID>`
- Child State Prior to Interruption:
  - Child transaction active: `BEGIN IMMEDIATE;`
  - Child uncommitted debit: `UPDATE accounts SET balance = 100 WHERE id = 'A';`
  - Child handshake line: `CHILD_MUTATED`
- Watchdog Timeout Parameter: `<actual, e.g. 5.0 seconds>`
- Interruption Method: `child.kill()` / OS process termination
- Reaped Return Code: `<actual process returncode / signal>`
- Journal Side-File Observation:
  - Journal file present during active uncommitted mutation: `<YES / NO>`
  - Fresh connection opened post-kill: `<YES / NO>`
  - Hot journal automatic recovery executed: `<YES / NO>`
  - Journal file present post-recovery: `<NO / CLEANED_UP>`
- Recovered Database Balances:
  - Account A: `<actual>`
  - Account B: `<actual>`
  - Invariant Total: `<actual>`
- Invariant Preserved: `<YES / NO>`
- Checkpoint 4 Verdict: `<PASS / FAIL>`

### Reviewer-Required Durability Inference Response
> **Question**: Why does surviving child process termination (`kill()`) verify client crash recovery, but **NOT** physical power-loss durability?

- Learner Explanation:
  `<Explain why client process termination leaves the operating system kernel, page cache, file descriptors, and disk controller fully operational to ensure log/journal records exist, whereas operating system crashes or physical power loss can cause unwritten RAM buffers and volatile drive caches to be lost. Mention PRAGMA synchronous and write barriers.>`

---

## F — Checkpoint 5: Backup & Storage Boundary Verification

- Online Backup API: `src_conn.backup(dst_conn, pages=0)`
- Backup Destination Path: `labs/lab_req_05/lab_req_05_backup.db`
- Backup File Size (Bytes): `<actual>`
- Backup Restoration Query: `SELECT id, balance FROM accounts ORDER BY id ASC;`
- Backup Database Balances:
  - Account A: `<actual>`
  - Account B: `<actual>`
  - Invariant Total: `<actual>`
- Backup Verification Verdict: `<PASS / FAIL>`
- Post-Test Backup File Cleaned Up: `<YES / NO>`
- Checkpoint 5 Verdict: `<PASS / FAIL>`

---

## G — Cleanup, Reset Idempotence & Residual Risk Audit

- Reset Command: `python labs/lab_req_05/reset.py`
- Run 1 Removed File Count: `<actual>`
- Run 2 Removed File Count: `0` (Idempotence PASS)
- Residual Database / Journal / WAL / SHM Artifacts: `<NONE / OTHER>`
- Machine-Checkable Test Suite Result:
  - Command: `python -m unittest discover -s labs/lab_req_05 -p "test_*.py"`
  - Tests Ran: `<actual count>`
  - Suite Verdict: `<PASS / FAIL>`
- Residual Risks / Known Limits: `<actual notes, e.g. non-canonical host observations under OQ-BP-006>`
