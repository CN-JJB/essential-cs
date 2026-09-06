#!/usr/bin/env python3
"""
Activity L16-02: Safe Remote Invocations, Retry Amplification & Idempotency.
Demonstrates:
1. Unsafe path: Retrying ambiguous non-idempotent mutations causes duplicate side effects.
2. Protected path: a scoped SQLite transaction ensures one intended counter effect for
   duplicate attempts inside the declared local transaction boundary.
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
        "A deduplication design must state its retention/eviction boundary. If the chosen "
        "policy evicts a key, a later duplicate can be treated as a new request unless some "
        "other durable business identifier or contract prevents re-execution."
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


def run_activity_l16_02(
    verbose: bool = True,
    *,
    unsafe_attempt_budget: int = 2,
    protected_attempt_budget: int = 3,
    concurrent_workers: int = 4,
    client_timeout_sec: float = 0.3,
    deterministic_backoff_ms: float = 50.0,
    retention_ttl_sec: float = 60.0,
    thread_join_timeout_sec: float = 3.0,
) -> Dict[str, Any]:
    """
    Execute the bounded L16-02 fixture.

    All numeric defaults are course-owned smoke parameters. Learner evidence records
    the actual values used; none is a curriculum-wide retry/timeout/retention constant.
    """
    if unsafe_attempt_budget < 2:
        raise ValueError("unsafe_attempt_budget must be >= 2 for the duplicate scenario")
    if protected_attempt_budget < 2:
        raise ValueError("protected_attempt_budget must be >= 2 for the retry scenario")
    if concurrent_workers < 2:
        raise ValueError("concurrent_workers must be >= 2")
    if client_timeout_sec <= 0 or deterministic_backoff_ms < 0:
        raise ValueError("timeout must be positive and backoff non-negative")
    if retention_ttl_sec <= 0 or thread_join_timeout_sec <= 0:
        raise ValueError("retention and join bounds must be positive")

    this_dir = os.path.dirname(os.path.abspath(__file__))
    scratch_dir = os.path.join(this_dir, ".scratch")
    os.makedirs(scratch_dir, exist_ok=True)
    db_path = os.path.join(scratch_dir, "m16_idempotency_activity.db")

    def _remove_db_artifacts() -> None:
        errors = []
        for ext in ("", "-journal", "-wal", "-shm"):
            f = db_path + ext
            if os.path.exists(f):
                try:
                    os.remove(f)
                except OSError as e:
                    errors.append(f"{f}: {e}")
        if errors:
            raise RuntimeError("Failed to clean M16 SQLite artifacts: " + "; ".join(errors))

    _remove_db_artifacts()

    idempotency_store = IdempotencyStore(db_path=db_path)
    fault_shim = FaultShim()
    server = RPCServer(
        fault_shim=fault_shim,
        idempotency_store=idempotency_store,
        watchdog_timeout=max(thread_join_timeout_sec, client_timeout_sec),
    )
    port = server.start()
    client = RPCClient(host="127.0.0.1", port=port, default_timeout=client_timeout_sec)

    unsafe_delta = protected_delta = concurrent_delta = 0
    protected_within_ttl = False
    re_executed_after_purge = False
    purged_count = 0
    unsafe_req_id = "unsafe-payment-001"
    protected_req_id = "protected-payment-002"
    idempotency_key = "idemp-key-course-owned"
    concurrent_key = "concurrent-key-course-owned"
    ttl_key = "retention-key-course-owned"
    results: List[Any] = []
    errors: List[Exception] = []
    results_lock = threading.Lock()
    concurrent_threads_joined = False
    cleanup_error = None

    try:
        if verbose:
            print("=" * 72)
            print(" Activity L16-02: Retry Amplification, Backoff & Idempotency Store")
            print("=" * 72)
            print(f" [RPC Server]: 127.0.0.1:{port} (ephemeral)")
            print(
                " [Fixture Parameters]: "
                f"unsafe_budget={unsafe_attempt_budget}, "
                f"protected_budget={protected_attempt_budget}, "
                f"workers={concurrent_workers}, "
                f"client_timeout={client_timeout_sec}s, "
                f"backoff={deterministic_backoff_ms}ms"
            )

        # Phase 1: deterministic unsafe duplicate path.
        fault_shim.set_rule(
            request_id=unsafe_req_id,
            action=FaultAction.DROP_RESPONSE,
            max_triggers=1,
        )
        initial_unsafe_counter = idempotency_store.get_counter_value("primary")
        client.call(
            method="unsafe_increment",
            params={"delta": 1, "name": "primary"},
            request_id=unsafe_req_id,
            timeout=client_timeout_sec,
            retry_policy=RetryPolicy.DETERMINISTIC,
            max_attempts=unsafe_attempt_budget,
            base_backoff_ms=deterministic_backoff_ms,
        )
        final_unsafe_counter = idempotency_store.get_counter_value("primary")
        unsafe_delta = final_unsafe_counter - initial_unsafe_counter
        unsafe_attempts = len(
            [t for t in client.call_traces if t.get("request_id") == unsafe_req_id]
        )

        # Phase 2: same ambiguity, but a scoped SQLite idempotency transaction.
        fault_shim.set_rule(
            request_id=protected_req_id,
            action=FaultAction.DROP_RESPONSE,
            max_triggers=1,
        )
        initial_protected_counter = idempotency_store.get_counter_value("primary")
        protected_resp = client.call(
            method="protected_increment",
            params={
                "idempotency_key": idempotency_key,
                "delta": 1,
                "name": "primary",
            },
            request_id=protected_req_id,
            timeout=client_timeout_sec,
            retry_policy=RetryPolicy.DETERMINISTIC,
            max_attempts=protected_attempt_budget,
            base_backoff_ms=deterministic_backoff_ms,
        )
        final_protected_counter = idempotency_store.get_counter_value("primary")
        protected_delta = final_protected_counter - initial_protected_counter
        protected_attempts = len(
            [t for t in client.call_traces if t.get("request_id") == protected_req_id]
        )

        # Phase 3: concurrent duplicate safety under the same local SQLite boundary.
        before_concurrent_counter = idempotency_store.get_counter_value("primary")

        def _concurrent_worker(worker_id: int) -> None:
            worker_client = RPCClient(
                host="127.0.0.1",
                port=port,
                default_timeout=max(client_timeout_sec, thread_join_timeout_sec),
            )
            try:
                r = worker_client.call(
                    method="protected_increment",
                    params={
                        "idempotency_key": concurrent_key,
                        "delta": 1,
                        "name": "primary",
                    },
                    request_id=f"concurrent-req-{worker_id}",
                    timeout=max(client_timeout_sec, thread_join_timeout_sec),
                    retry_policy=RetryPolicy.NO_RETRY,
                    max_attempts=1,
                )
                with results_lock:
                    results.append(r)
            except Exception as err:
                with results_lock:
                    errors.append(err)

        threads = [
            threading.Thread(target=_concurrent_worker, args=(i,))
            for i in range(concurrent_workers)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=thread_join_timeout_sec)
        concurrent_threads_joined = all(not t.is_alive() for t in threads)

        after_concurrent_counter = idempotency_store.get_counter_value("primary")
        concurrent_delta = after_concurrent_counter - before_concurrent_counter

        # Phase 4: retention boundary without depending on wall-clock sleep timing.
        # We inject a future "current_time" into the explicit purge API to exercise the
        # eviction policy deterministically; this is a policy-model observation, not
        # reproduction of real network delay or a prescribed TTL duration.
        client.call(
            method="protected_increment",
            params={
                "idempotency_key": ttl_key,
                "delta": 1,
                "name": "primary",
                "ttl_seconds": retention_ttl_sec,
            },
            timeout=client_timeout_sec,
            retry_policy=RetryPolicy.NO_RETRY,
            max_attempts=1,
        )
        counter_after_first = idempotency_store.get_counter_value("primary")

        client.call(
            method="protected_increment",
            params={
                "idempotency_key": ttl_key,
                "delta": 1,
                "name": "primary",
                "ttl_seconds": retention_ttl_sec,
            },
            timeout=client_timeout_sec,
            retry_policy=RetryPolicy.NO_RETRY,
            max_attempts=1,
        )
        counter_within_ttl = idempotency_store.get_counter_value("primary")
        protected_within_ttl = counter_within_ttl == counter_after_first

        synthetic_after_expiry = time.time() + retention_ttl_sec + 1.0
        purged_count = idempotency_store.purge_expired(
            current_time=synthetic_after_expiry
        )

        client.call(
            method="protected_increment",
            params={
                "idempotency_key": ttl_key,
                "delta": 1,
                "name": "primary",
                "ttl_seconds": retention_ttl_sec,
            },
            timeout=client_timeout_sec,
            retry_policy=RetryPolicy.NO_RETRY,
            max_attempts=1,
        )
        counter_after_expiry = idempotency_store.get_counter_value("primary")
        re_executed_after_purge = counter_after_expiry > counter_within_ttl

        if verbose:
            print(f" [Unsafe]: attempts={unsafe_attempts}, observed_delta={unsafe_delta}")
            print(
                f" [Protected]: attempts={protected_attempts}, "
                f"observed_delta={protected_delta}, "
                f"duplicate={protected_resp.get('result', {}).get('is_duplicate')}"
            )
            print(
                f" [Concurrent]: workers={concurrent_workers}, delta={concurrent_delta}, "
                f"responses={len(results)}, errors={len(errors)}, joined={concurrent_threads_joined}"
            )
            print(
                f" [Retention policy model]: ttl={retention_ttl_sec}s, "
                f"purged={purged_count}, reexecuted_after_purge={re_executed_after_purge}"
            )
            print("=" * 72)

    finally:
        try:
            server.stop()
        except Exception as e:
            cleanup_error = f"server cleanup: {e}"
        try:
            _remove_db_artifacts()
        except Exception as e:
            cleanup_error = (
                f"{cleanup_error}; db cleanup: {e}" if cleanup_error else f"db cleanup: {e}"
            )

    all_passed = (
        unsafe_delta > 1
        and protected_delta == 1
        and concurrent_delta == 1
        and concurrent_threads_joined
        and not errors
        and protected_within_ttl
        and purged_count >= 1
        and re_executed_after_purge
        and cleanup_error is None
    )

    return {
        "disposition": "PASS" if all_passed else "FAIL",
        "fixture_parameters": {
            "unsafe_attempt_budget": unsafe_attempt_budget,
            "protected_attempt_budget": protected_attempt_budget,
            "concurrent_workers": concurrent_workers,
            "client_timeout_sec": client_timeout_sec,
            "deterministic_backoff_ms": deterministic_backoff_ms,
            "retention_ttl_sec": retention_ttl_sec,
            "thread_join_timeout_sec": thread_join_timeout_sec,
        },
        "unsafe_path": {
            "attempts": unsafe_attempts,
            "initial_counter": initial_unsafe_counter,
            "final_counter": final_unsafe_counter,
            "delta": unsafe_delta,
            "duplicate_effect_observed": unsafe_delta > 1,
        },
        "protected_path": {
            "attempts": protected_attempts,
            "idempotency_key": idempotency_key,
            "initial_counter": initial_protected_counter,
            "final_counter": final_protected_counter,
            "delta": protected_delta,
            "one_intended_effect_preserved": protected_delta == 1,
        },
        "concurrent_path": {
            "workers": concurrent_workers,
            "successful_responses": len(results),
            "errors": [type(e).__name__ for e in errors],
            "threads_joined": concurrent_threads_joined,
            "delta": concurrent_delta,
            "one_intended_effect_preserved": concurrent_delta == 1,
        },
        "retention_boundary": {
            "ttl_seconds": retention_ttl_sec,
            "clock_mode": "INJECTED_FUTURE_PURGE_TIME",
            "protected_within_ttl": protected_within_ttl,
            "purged_records": purged_count,
            "re_executed_after_purge": re_executed_after_purge,
        },
        "cleanup_error": cleanup_error,
        "inference_limits": INFERENCE_LIMITS_L16_02,
    }

if __name__ == "__main__":
    res = run_activity_l16_02(verbose=True)
    sys.exit(0 if res["disposition"] == "PASS" else 1)
