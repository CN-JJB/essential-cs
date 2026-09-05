# LAB-REQ-03: POSIX Threads Race, Rendezvous & Progress Boundaries

## Overview

`LAB-REQ-03` is a Core Required systems lab in Essential CS designed to demystify multi-threaded execution, logical race conditions, synchronization primitives, and progress boundaries under real preemptive scheduling.

## Core Lab Requirements & Constraints

1. **UB-Free Race Demonstration**:
   - Demonstrates lost updates using legal C11 atomics (`<stdatomic.h>`) with `atomic_load_explicit` and `atomic_store_explicit` (`memory_order_relaxed`).
   - Individual memory operations are legal and defined; the multi-step state transition (Read $\to$ Compute $\to$ Store) is non-atomic.
   - Zero C-language data-race Undefined Behavior (UB) is used as teaching evidence.
2. **Deterministic Coordination**:
   - Employs course-controlled phase handoffs so real pthread workers participate in a verified lost-update interleaving.
3. **Supplemental Natural Scheduler Observation**:
   - Observes natural scheduling under cooperative yields (`sched_yield()`).
   - Recorded truthfully as supplemental evidence; no fixed manifestation rate or failure percentage is asserted.
4. **POSIX Mutex Repair**:
   - Protects the compound update with `pthread_mutex_t`, verifying that the invariant holds across all runs.
5. **Condition-Variable Rendezvous**:
   - Implements producer-consumer synchronization using `pthread_cond_t` and an associated mutex.
   - Enforces the mandatory predicate re-evaluation loop (`while (!predicate) pthread_cond_wait(...)`) to defend against spurious wakeups.
6. **Controlled Deadlock & Watchdog**:
   - Executes lock-inversion circular wait in an owned child process.
   - Verifies circular wait preconditions (both workers holding first lock and attempting the other's lock) before parent watchdog timeout is interpreted as deadlock evidence.
   - Parent terminates and reaps the child cleanly.

## Files

- `broken_counter.c`: C11 source for deterministic and natural lost-update demonstration.
- `mutex_counter.c`: C11 source for POSIX mutex repair.
- `cond_rendezvous.c`: C11 source for condition-variable rendezvous with predicate recheck.
- `deadlock_preconditions.c`: C11 source for circular wait deadlock preconditions in child process.
- `harness.py`: Python orchestration harness running all 5 checkpoints.
- `runner.py`: CLI entry point supporting human-readable and `--json` machine reporting.
- `reset.py`: Idempotent cleanup script.
- `test_lab.py`: Comprehensive unittest suite.

## Execution

### Compile & Run All Checkpoints
```bash
python labs/lab_req_03/runner.py
```

### JSON Machine-Readable Output
```bash
python labs/lab_req_03/runner.py --json
```

### Run Automated Unit Tests
```bash
python -m unittest discover -s labs/lab_req_03
```

### Idempotent Reset
```bash
python labs/lab_req_03/reset.py
```
