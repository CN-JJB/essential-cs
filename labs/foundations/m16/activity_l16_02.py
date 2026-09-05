#!/usr/bin/env python3
"""
Activity L16-02: Safe Remote Invocations, Retry Amplification & Idempotency.
Demonstrates:
1. Unsafe path: Retrying ambiguous non-idempotent mutations causes duplicate side effects.
2. Protected path: SQLite atomic deduplication ensures exactly-once business side effects
   within the declared transaction boundary.
3. Concurrent duplicate safety: Atomic key claim serializes concurrent retries.
4. Retention boundary: Key eviction demonstrates the lifetime limits of deduplication tables.
5. Retry amplification analysis: Exponential backoff with full jitter as a policy choice.
"""

import os
import sys
import threading
import time
from typing import Any, Dict, List

try:
    from .rpc_fixture import (
        FaultAction,
        FaultShim,
        IdempotencyStore,
        RetryPolicy,
        RPCClient,
        RPCServer,
    )
except ImportError:
    from rpc_fixture import (
        FaultAction,
        FaultShim,
        IdempotencyStore,
        RetryPolicy,
        RPCClient,
        RPCServer,
    )

INFERENCE_LIMITS_L16_02 = {
    "scope_of_idempotency": (
        "Idempotency in this fixture is proven strictly within the declared SQLite "
        "transaction boundary. It does NOT prove arbitrary exactly-once delivery across "
        "arbitrary distributed side effects (such as physical third-party webhooks or emails)."
    ),
    "retention_boundary": (
        "Deduplication keys cannot be stored indefinitely; all practical idempotency stores "
        "have a finite retention window (TTL). A retry arriving after the retention window "
        "has expired will be treated as a new request."
    ),
    "response_identity": (
        "Idempotency guarantees invariant state transitions (f(f(x)) = f(x)), not "
        "byte-for-byte identical network responses. Dynamic headers, arrival timestamps, "
        "or internal IDs may vary across duplicate responses."
    ),
    "backoff_policy_nature": (
        "Exponential backoff with full jitter is an architectural policy option to prevent "
        "thundering herds; it is not a timeless natural law or universal formula."
    ),
}


def run_activity_l16_02(verbose: bool = True) -> Dict[str, Any]:
    this_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(this_dir, "m16_idempotency_activity.db")

    # Clean prior DB if exists
    for ext in ("", "-journal", "-wal", "-shm"):
        f = db_path + ext
        if os.path.exists(f):
            try:
                os.remove(f)
            except OSError:
                pass

    idempotency_store = IdempotencyStore(db_path=db_path)
    fault_shim = FaultShim()
    server = RPCServer(fault_shim=fault_shim, idempotency_store=idempotency_store)
    port = server.start()
    client = RPCClient(host="127.0.0.1", port=port, default_timeout=0.4)

    if verbose:
        print("=" * 72)
        print(" Activity L16-02: Retry Amplification, Backoff & Idempotency Store")
        print("=" * 72)
        print(f" [RPC Server]: 127.0.0.1:{port} (SQLite: {os.path.basename(db_path)})")

    # -------------------------------------------------------------------------
    # Phase 1: Unsafe Path (No Idempotency Key)
    # -------------------------------------------------------------------------
    if verbose:
        print("\n--- Phase 1: Unsafe Path (Mutating Call Retried without Idempotency) ---")

    unsafe_req_id = "unsafe-payment-001"
    # Script fault shim to DROP the first response, causing client retry
    fault_shim.set_rule(
        request_id=unsafe_req_id,
        action=FaultAction.DROP_RESPONSE,
        max_triggers=1,
    )

    initial_unsafe_counter = idempotency_store.get_counter_value("primary")
    unsafe_attempts = 0
    unsafe_success = False

    try:
        # Client configured for 2 attempts with deterministic retry
        resp = client.call(
            method="unsafe_increment",
            params={"delta": 1, "name": "primary"},
            request_id=unsafe_req_id,
            timeout=0.3,
            retry_policy=RetryPolicy.DETERMINISTIC,
            max_attempts=2,
            base_backoff_ms=50.0,
        )
        unsafe_success = True
    except Exception as e:
        if verbose:
            print(f" [Unsafe Call] Exception: {e}")

    final_unsafe_counter = idempotency_store.get_counter_value("primary")
    unsafe_delta = final_unsafe_counter - initial_unsafe_counter

    if verbose:
        print(f"   Configured attempts: 2, Response dropped on attempt 1")
        print(f"   Observed Counter Increment: {unsafe_delta} (Expected duplicate side effect: 2)")
        print(f"   Duplicate Side Effect Manifested: {unsafe_delta > 1}")

    # -------------------------------------------------------------------------
    # Phase 2: Protected Path (With Idempotency Key)
    # -------------------------------------------------------------------------
    if verbose:
        print("\n--- Phase 2: Protected Path (With Idempotency Key + SQLite Atomic Store) ---")

    protected_req_id = "protected-payment-002"
    idempotency_key = "idemp-key-uuid-999"

    # Script fault shim to DROP the first response
    fault_shim.set_rule(
        request_id=protected_req_id,
        action=FaultAction.DROP_RESPONSE,
        max_triggers=1,
    )

    initial_protected_counter = idempotency_store.get_counter_value("primary")
    protected_attempts = 0
    protected_resp = None

    try:
        # Client retries up to 3 attempts with deterministic retry
        protected_resp = client.call(
            method="protected_increment",
            params={
                "idempotency_key": idempotency_key,
                "delta": 1,
                "name": "primary",
            },
            request_id=protected_req_id,
            timeout=0.3,
            retry_policy=RetryPolicy.DETERMINISTIC,
            max_attempts=3,
            base_backoff_ms=50.0,
        )
    except Exception as e:
        if verbose:
            print(f" [Protected Call] Exception: {e}")

    final_protected_counter = idempotency_store.get_counter_value("primary")
    protected_delta = final_protected_counter - initial_protected_counter

    if verbose:
        print(f"   Idempotency Key: {idempotency_key}")
        print(f"   Configured attempts: 3, Response dropped on attempt 1")
        print(f"   Observed Counter Increment: {protected_delta} (Exactly 1 expected!)")
        print(f"   Server reported is_duplicate: {protected_resp.get('result', {}).get('is_duplicate')}")
        print(f"   Protected Invariant Preserved: {protected_delta == 1}")

    # -------------------------------------------------------------------------
    # Phase 3: Concurrent Duplicate Safety
    # -------------------------------------------------------------------------
    if verbose:
        print("\n--- Phase 3: Concurrent Duplicate Safety ---")

    concurrent_key = "concurrent-key-777"
    concurrent_threads = 4
    results: List[Any] = []
    errors: List[Exception] = []

    before_concurrent_counter = idempotency_store.get_counter_value("primary")

    def _concurrent_worker(worker_id: int):
        worker_client = RPCClient(host="127.0.0.1", port=port, default_timeout=1.0)
        try:
            r = worker_client.call(
                method="protected_increment",
                params={
                    "idempotency_key": concurrent_key,
                    "delta": 1,
                    "name": "primary",
                },
                request_id=f"concurrent-req-{worker_id}",
                timeout=1.0,
                retry_policy=RetryPolicy.NO_RETRY,
                max_attempts=1,
            )
            results.append(r)
        except Exception as err:
            errors.append(err)

    threads = [
        threading.Thread(target=_concurrent_worker, args=(i,))
        for i in range(concurrent_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=3.0)

    after_concurrent_counter = idempotency_store.get_counter_value("primary")
    concurrent_delta = after_concurrent_counter - before_concurrent_counter

    if verbose:
        print(f"   Dispatched {concurrent_threads} concurrent workers with same key: {concurrent_key}")
        print(f"   Counter Delta: {concurrent_delta} (Must be exactly 1)")
        print(f"   Successful responses: {len(results)}, Handled conflicts: {len(errors)}")

    # -------------------------------------------------------------------------
    # Phase 4: Retention Boundary Demonstration
    # -------------------------------------------------------------------------
    if verbose:
        print("\n--- Phase 4: Retention Boundary Demonstration ---")

    ttl_key = "short-lived-ttl-key"
    short_ttl = 0.2  # 200ms TTL

    # First call creates the entry
    client.call(
        method="protected_increment",
        params={
            "idempotency_key": ttl_key,
            "delta": 1,
            "name": "primary",
            "ttl_seconds": short_ttl,
        },
        timeout=0.5,
        retry_policy=RetryPolicy.NO_RETRY,
        max_attempts=1,
    )
    counter_after_first = idempotency_store.get_counter_value("primary")

    # Immediate duplicate within TTL: counter must NOT increase
    client.call(
        method="protected_increment",
        params={
            "idempotency_key": ttl_key,
            "delta": 1,
            "name": "primary",
            "ttl_seconds": short_ttl,
        },
        timeout=0.5,
        retry_policy=RetryPolicy.NO_RETRY,
        max_attempts=1,
    )
    counter_within_ttl = idempotency_store.get_counter_value("primary")
    protected_within_ttl = (counter_within_ttl == counter_after_first)

    # Wait past retention window and purge
    time.sleep(0.25)
    purged_count = idempotency_store.purge_expired(current_time=time.time())

    # Call again after retention expired: entry is gone, so mutation executes again!
    client.call(
        method="protected_increment",
        params={
            "idempotency_key": ttl_key,
            "delta": 1,
            "name": "primary",
            "ttl_seconds": short_ttl,
        },
        timeout=0.5,
        retry_policy=RetryPolicy.NO_RETRY,
        max_attempts=1,
    )
    counter_after_expiry = idempotency_store.get_counter_value("primary")
    re_executed_after_purge = (counter_after_expiry > counter_within_ttl)

    if verbose:
        print(f"   Short TTL key: {ttl_key} (TTL={short_ttl}s)")
        print(f"   Within TTL deduplication active: {protected_within_ttl}")
        print(f"   Expired records purged: {purged_count}")
        print(f"   Re-executed after retention horizon expired: {re_executed_after_purge}")
        print("=" * 72)

    # Clean shutdown
    server.stop()

    # Clean database side-files
    for ext in ("", "-journal", "-wal", "-shm"):
        f = db_path + ext
        if os.path.exists(f):
            try:
                os.remove(f)
            except OSError:
                pass

    all_passed = (
        unsafe_delta > 1
        and protected_delta == 1
        and concurrent_delta == 1
        and protected_within_ttl
        and re_executed_after_purge
    )

    return {
        "disposition": "PASS" if all_passed else "FAIL",
        "unsafe_path": {
            "initial_counter": initial_unsafe_counter,
            "final_counter": final_unsafe_counter,
            "delta": unsafe_delta,
            "duplicate_effect_observed": unsafe_delta > 1,
        },
        "protected_path": {
            "idempotency_key": idempotency_key,
            "initial_counter": initial_protected_counter,
            "final_counter": final_protected_counter,
            "delta": protected_delta,
            "exact_once_invariant_preserved": protected_delta == 1,
        },
        "concurrent_path": {
            "workers": concurrent_threads,
            "delta": concurrent_delta,
            "exact_once_invariant_preserved": concurrent_delta == 1,
        },
        "retention_boundary": {
            "ttl_seconds": short_ttl,
            "protected_within_ttl": protected_within_ttl,
            "purged_records": purged_count,
            "re_executed_after_purge": re_executed_after_purge,
        },
        "inference_limits": INFERENCE_LIMITS_L16_02,
    }


if __name__ == "__main__":
    res = run_activity_l16_02(verbose=True)
    sys.exit(0 if res["disposition"] == "PASS" else 1)
