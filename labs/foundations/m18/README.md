# M18 Foundations Activities: Distributed State & Coordination

This directory contains executable, course-owned fixtures and worked-trace harnesses for Module M18.

## Core Boundary Rules

- **Zero External Brokers**: Strictly no Kafka, RabbitMQ, Redis, ActiveMQ, or cloud queues (AWS SQS).
- **Zero Listening Daemons**: No external database servers or network listening ports required by Core.
- **Broker-Neutral Core Mechanism**: File-backed SQLite transactional outbox and worker deduplication.
- **Deterministic State Evaluation**: Scripted fault paths, transaction boundaries, and trace state machines rather than probabilistic network timing.

## Files Overview

1. **`outbox_fixture.py`** (and facade **`s6_m18_outbox_fixture.py`**)
   - **Broken Dual Write**: Demonstrates state divergence when local database commit is uncoordinated with separate message enqueue.
   - **Transactional Outbox**: Demonstrates atomic local commit of business state (`orders`) and outbound events (`outbox_events`) within a single SQLite transaction (`BEGIN IMMEDIATE` ... `COMMIT`).
   - **Outbox Relay**: Polls undispatched events with at-least-once retry delivery; scripted failure hook injects deliver-before-mark crash.
   - **Worker Deduplication**: Executes message claim (`processed_events`) and selected consumer effect (`fulfillments`) within **one local SQLite transaction**; safely suppresses duplicates without reapplying the business effect.

2. **`coordination_trace.py`**
   - **Classic Two-Phase Commit (2PC)**: Models Prepare, Vote, and Decision phases; evaluates participant `PREPARED` blocking uncertainty under coordinator failure/silence; demonstrates why a participant voting `NO` can safely abort unilaterally.
   - **Saga Pattern (3 Steps)**: Executes `CreateOrder` -> `ReserveInventory` -> `ProcessPayment` with configured reverse-order compensations upon failure; captures intermediate dirty-read anomaly proving lack of Isolation ($I \in \text{ACID}$).
   - **Distributed Leases & Fencing Tokens**: Models lock lease expiry during client pause; demonstrates resource-boundary fencing token validation and stale-holder write rejection.

3. **`activity_l18_01.py`**
   - Runs the complete L18-01 dual-write divergence, transactional outbox staging, relay crash redelivery, and worker deduplication sequence.
   - Generates `.scratch/l18_01_observation.json`.

4. **`activity_l18_02.py`**
   - Runs the complete L18-02 2PC uncertainty, Saga compensation / isolation anomaly, and fencing token validation sequence.
   - Generates `.scratch/l18_02_observation.json`.

5. **`reset.py`**
   - Fail-closed, idempotent cleanup removing `.scratch/` and local `__pycache__/`.

6. **`test_m18.py`**
   - Automated unit test suite verifying all 11 core contracts, fault injections, and reset idempotence.

## Running the Activities

```bash
# 1. Preflight check for M18 Core capabilities
python tests/preflight_distributed_infra.py --module m18

# 2. Run L18-01 hands-on activity (Outbox & Deduplication)
python labs/foundations/m18/activity_l18_01.py

# 3. Run L18-02 hands-on activity (2PC, Saga & Fencing)
python labs/foundations/m18/activity_l18_02.py

# 4. Run automated test suite
python -m unittest discover -s labs/foundations/m18 -p "test_*.py"

# 5. Clean up temporary artifacts (idempotent, safe to run repeatedly)
python labs/foundations/m18/reset.py
```
