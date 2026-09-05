# M15 Foundations Activities: Concurrency, Threads, Races & Synchronization

## Overview

This directory provides the companion hands-on activities for Module M15:
- **L15-01**: `activity_l15_01.py` — Verifies the canonical definition of **EC-CON-015 Concurrency**, contrasts it with Parallelism, and demonstrates compound update lost updates using defined C11 atomics without language-level Undefined Behavior (UB).
- **L15-02**: `activity_l15_02.py` — Demonstrates POSIX mutex critical section repair, condition-variable rendezvous with mandatory predicate re-evaluation loop guards (`while (!predicate)`), and controlled deadlock preconditions under an owned-child watchdog harness.
- **L15-03**: `activity_l15_03.py` — Inspects Python runtime build flags (`Py_GIL_DISABLED`, `_is_gil_enabled`), disassembles compound update bytecode (`x += 1`), demonstrates cooperative single-loop task execution with executor delegation, and establishes the architectural selection matrix (**NO UNIVERSAL WINNER — WORKLOAD/RUNTIME DRIVEN**).

## Structure

- `activity_l15_01.py`: L15-01 runnable activity script.
- `activity_l15_02.py`: L15-02 runnable activity script.
- `activity_l15_03.py`: L15-03 runnable activity script.
- `reset.py`: Idempotent cleanup script.
- `test_activity.py`: Automated unittest suite verifying all 3 activities and reset idempotence.

## Running Activities

```bash
# L15-01
python labs/foundations/m15/activity_l15_01.py

# L15-02
python labs/foundations/m15/activity_l15_02.py

# L15-03
python labs/foundations/m15/activity_l15_03.py
```

## Running Tests

```bash
python -m unittest discover -s labs/foundations/m15
```

## Idempotent Reset

```bash
python labs/foundations/m15/reset.py
```
