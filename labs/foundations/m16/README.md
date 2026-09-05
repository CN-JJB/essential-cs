# M16 Foundations Activities: Distributed Systems — Partial Failure & RPC

This directory contains executable, course-owned exploratory activities and fixtures for Module M16.

## Scripts Overview

1. **`rpc_fixture.py` (alias `s6_m16_rpc_fixture.py`)** — Localhost RPC, Fault Injection & Idempotency Fixture
   - Binds exclusively to `127.0.0.1` on an ephemeral OS-assigned port (`port=0`).
   - Length-prefixed framing (`>I` 4-byte header + UTF-8 JSON) eliminating TCP `recv` boundary equivalence reliance.
   - User-space `FaultShim` simulating application-layer delays (`DELAY_RESPONSE`) and message drops (`DROP_RESPONSE`).
   - Explicitly labeled: application-layer behavior only, **NEVER literal packet loss**.
   - `IdempotencyStore`: SQLite-backed atomic key claim and mutation under `BEGIN IMMEDIATE` transactions with explicit TTL retention horizons.
   - Explicit shutdown ownership: closes all sockets, joins all threads (no daemon-thread-exit-as-cleanup).
   - Configurable harness safety watchdog.

2. **`activity_l16_01.py`** — Partial Failure & The Fundamental No-Response Ambiguity
   - Demonstrates caller-alive remote ambiguity.
   - Client stops waiting upon local deadline expiration (`TimeoutError`).
   - Server independently records completion of the **exact same request ID** after the client gave up.
   - Proves that a local timeout erases client waiting, but does NOT undo or cancel remote execution.

3. **`activity_l16_02.py`** — Retry Amplification, Backoff & Idempotency Store
   - **Phase 1 (Unsafe)**: Scripted response drop triggers client retries without idempotency; server records duplicate side effects (counter $> 1$).
   - **Phase 2 (Protected)**: Client carries `idempotency_key`; server deduplication table ensures exactly-once business side effects within the declared SQLite transaction boundary (counter $= 1$).
   - **Phase 3 (Concurrent)**: Multiple concurrent threads dispatching the identical idempotency key serialize safely without duplicate side effects.
   - **Phase 4 (Retention Horizon)**: Demonstrates that expired deduplication keys allow re-execution after TTL eviction.
   - Analyzes retry amplification across call graphs and presents exponential backoff with full jitter as an architectural policy choice.

4. **`reset.py`** — Idempotent cleanup script removing all `.db`, `.db-journal`, `.db-wal`, `.db-shm`, `.tmp`, and `.log` files.

5. **`test_activity.py`** — Automated unit test suite verifying both activities, attempt-budget enforcement, framing assembly, and reset idempotence.

## Running the Activities

```bash
# Run each activity interactively
python labs/foundations/m16/activity_l16_01.py
python labs/foundations/m16/activity_l16_02.py

# Run unit tests
python -m unittest discover -s labs/foundations/m16 -p "test_*.py"

# Clean up all generated files (idempotent, safe to run repeatedly)
python labs/foundations/m16/reset.py
```
