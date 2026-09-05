# M14 Foundations Activities: Databases — Transactions, Recovery & Isolation

This directory contains executable exploratory activities for Module M14.

## Scripts Overview

1. **`activity_l14_01.py`** — Transaction Boundaries, Invariant Transitions & Rollback Mechanics
   - Demonstrates multi-step transfer preserving declared invariant ($\sum = 1000$).
   - Injects simulated failure mid-transaction, followed by explicit `ROLLBACK`.
   - Demonstrates successful multi-step transfer and `COMMIT` to $S_1$.
   - Observes rollback journal side-file under SQLite `DELETE` mode.
   - Highlights the inference limit: client crash recovery $\ne$ physical power-loss durability.

2. **`activity_l14_02.py`** — Concurrent Interleaving, Visibility & Consistency First Home
   - Dual independent connections to a single course-owned SQLite database under rollback journal `DELETE` mode.
   - Proves absence of Dirty Reads ($P_1$) under SQLite's declared committed-only visibility baseline.
   - Demonstrates bounded second-writer conflict (`SQLITE_BUSY`) without fixed exception strings.
   - Anchors the canonical first home and verbatim definition of **`EC-CON-014 Consistency`** with its mandatory qualifier.

3. **`activity_l14_03.py`** — Atomic Write Design, Lock Upgrades & Boundary Retries
   - Demonstrates the lock-upgrade collision hazard when using `BEGIN DEFERRED`.
   - Refactors to `BEGIN IMMEDIATE` to serialize write intent upfront and avoid upgrade collisions.
   - Implements a transaction-boundary retry loop with bounded exponential backoff.
   - Implements an idempotency token check ($f(f(x)) = f(x)$) preventing duplicate mutations.
   - Demonstrates that non-transient errors (syntax, constraints) fail fast without retry.

4. **`reset.py`** — Idempotent cleanup script removing all `.db`, `.db-journal`, `.db-wal`, `.db-shm`, and `.bak` files.

5. **`test_activity.py`** — Automated unit test suite verifying all three activities and reset idempotence.

## Running the Activities

```bash
# Run each activity interactively
python labs/foundations/m14/activity_l14_01.py
python labs/foundations/m14/activity_l14_02.py
python labs/foundations/m14/activity_l14_03.py

# Run unit tests
python -m unittest discover -s labs/foundations/m14 -p "test_*.py"

# Clean up all generated database files
python labs/foundations/m14/reset.py
```
