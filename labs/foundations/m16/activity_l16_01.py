#!/usr/bin/env python3
"""
Activity L16-01: Partial Failure & The Fundamental No-Response Ambiguity.
Demonstrates that when a remote call falls silent, the client's local timeout
erases only the client's waiting — it does NOT cancel or undo remote execution.
"""

import os
import sys
import threading
import time
from typing import Any, Dict, Optional

try:
    from .rpc_fixture import FaultAction, FaultShim, RetryPolicy, RPCClient, RPCServer
except ImportError:
    from rpc_fixture import FaultAction, FaultShim, RetryPolicy, RPCClient, RPCServer

INFERENCE_LIMITS_L16_01 = {
    "silence_ambiguity": (
        "Silence across a network boundary does not reveal whether the request was lost, "
        "the remote process crashed before executing, execution completed but the response "
        "was dropped, or work is merely delayed."
    ),
    "timeout_local_nature": (
        "A client-side timeout is a local decision to stop waiting; it does not cancel, "
        "roll back, or communicate anything to the remote server."
    ),
    "transport_vs_application": (
        "TCP connection establishment or OS-level byte receipt indicates transport transit; "
        "it is not proof of application processing or durable business state commitment."
    ),
    "fault_shim_boundary": (
        "The fault injection shim operates strictly at the application layer; simulated delays "
        "and dropped messages must never be mislabeled as literal physical packet loss."
    ),
}


def run_activity_l16_01(
    verbose: bool = True,
    *,
    client_timeout_sec: float = 0.3,
    server_request_delay_sec: float = 0.6,
    completion_wait_timeout_sec: float = 2.0,
) -> Dict[str, Any]:
    """
    Execute the bounded L16-01 observation.

    The numeric defaults are course-owned smoke parameters, not curriculum constants.
    The required relation is server_request_delay_sec > client_timeout_sec so the
    application-layer shim delays server execution until after the caller stops waiting.
    """
    if client_timeout_sec <= 0:
        raise ValueError("client_timeout_sec must be positive")
    if server_request_delay_sec <= client_timeout_sec:
        raise ValueError(
            "server_request_delay_sec must exceed client_timeout_sec for this observation"
        )
    if completion_wait_timeout_sec <= server_request_delay_sec:
        raise ValueError(
            "completion_wait_timeout_sec must exceed the scripted server request delay"
        )

    fault_shim = FaultShim()
    server = RPCServer(
        fault_shim=fault_shim,
        watchdog_timeout=completion_wait_timeout_sec,
    )
    port = server.start()

    client = RPCClient(
        host="127.0.0.1",
        port=port,
        default_timeout=client_timeout_sec,
    )
    target_req_id = f"l16-01-req-{time.time_ns()}"

    # Delay the request in the course-owned application shim before business execution.
    # This is not literal packet loss and it is not a claim about real network latency.
    fault_shim.set_rule(
        request_id=target_req_id,
        action=FaultAction.DELAY_REQUEST,
        delay_seconds=server_request_delay_sec,
        max_triggers=1,
    )
    server_executed_event = fault_shim.get_execution_event(target_req_id)

    server_execution_record: Dict[str, Any] = {}

    def bounded_business_method(params: dict) -> dict:
        completion_time = time.time()
        server_execution_record["account"] = params.get("account", "acc-01")
        server_execution_record["amount"] = params.get("amount", 100)
        server_execution_record["completion_time"] = completion_time
        return {
            "status": "SUCCESS",
            "processed_amount": server_execution_record["amount"],
            "timestamp": completion_time,
        }

    server.register_method("debit_account", bounded_business_method)

    client_stopped_time = 0.0
    client_outcome = "UNKNOWN"
    client_exception_type: Optional[str] = None
    unexpected_error: Optional[str] = None
    dispatch_time = time.time()

    if verbose:
        print("=" * 72)
        print(" Activity L16-01: Partial Failure & No-Response Ambiguity")
        print("=" * 72)
        print(f" [Localhost RPC Server]: Listening on 127.0.0.1:{port} (ephemeral)")
        print(f" [Target Request ID]:   {target_req_id}")
        print(f" [Client Deadline]:       {client_timeout_sec}s (fixture parameter)")
        print(
            f" [Application Shim Delay]: {server_request_delay_sec}s before server execution "
            "(fixture parameter, NOT packet loss)"
        )

    try:
        client.call(
            method="debit_account",
            params={"account": "user-wallet-42", "amount": 100},
            request_id=target_req_id,
            timeout=client_timeout_sec,
            retry_policy=RetryPolicy.NO_RETRY,
            max_attempts=1,
        )
        client_outcome = "UNEXPECTED_SUCCESS"
    except TimeoutError as e:
        client_stopped_time = time.time()
        client_outcome = "TIMEOUT_STOPPED_WAITING"
        client_exception_type = type(e).__name__
        if verbose:
            print(f" [Client Event]: Stopped waiting after {client_stopped_time - dispatch_time:.3f}s")
            print(f"   Observed Outcome: {client_exception_type}")
    except Exception as e:
        # Any non-timeout failure is materially different evidence and must not be
        # mislabeled as the required timeout observation.
        client_stopped_time = time.time()
        client_outcome = "UNEXPECTED_CLIENT_ERROR"
        client_exception_type = type(e).__name__
        unexpected_error = str(e)
        if verbose:
            print(f" [Client Event]: Unexpected non-timeout failure: {type(e).__name__}: {e}")

    server_finished = server_executed_event.wait(timeout=completion_wait_timeout_sec)

    server_audit_entry = next(
        (
            entry
            for entry in server.audit_log
            if entry.get("request_id") == target_req_id
            and entry.get("event") == "SERVER_COMPLETED_EXECUTION"
        ),
        None,
    )
    server_completed_time = (
        float(server_audit_entry.get("completion_time", 0.0))
        if server_audit_entry
        else 0.0
    )
    identical_id_confirmed = server_audit_entry is not None
    server_completed_after_client = (
        client_stopped_time > 0
        and server_completed_time > client_stopped_time
    )

    if verbose:
        if server_audit_entry:
            print(f" [Server Event]: Handler completed after {server_completed_time - dispatch_time:.3f}s")
            print(f"   Identical Request ID: {target_req_id}")
        else:
            print(" [Server Event]: Required completion evidence was not observed")
        print(f"   Completed after client stopped waiting: {server_completed_after_client}")
        print(" [Inference]:")
        print("   Local timeout DID NOT cancel remote handler execution.")
        print("   This fixture does not claim a durable database commit for L16-01.")
        print("=" * 72)

    try:
        server.stop()
    except RuntimeError as e:
        unexpected_error = f"cleanup failure: {e}"
        server_finished = False

    passed = (
        client_outcome == "TIMEOUT_STOPPED_WAITING"
        and server_finished
        and identical_id_confirmed
        and server_completed_after_client
        and unexpected_error is None
    )

    return {
        "disposition": "PASS" if passed else "FAIL",
        "request_id": target_req_id,
        "client_timeout_configured_sec": client_timeout_sec,
        "server_request_delay_configured_sec": server_request_delay_sec,
        "client_outcome": client_outcome,
        "client_exception_type": client_exception_type,
        "unexpected_error": unexpected_error,
        "client_stopped_waiting_timestamp": client_stopped_time,
        "server_completed_timestamp": server_completed_time,
        "server_request_id_completed": target_req_id if identical_id_confirmed else None,
        "identical_request_id_confirmed": identical_id_confirmed,
        "server_completed_after_client_stopped_waiting": server_completed_after_client,
        "inference_limits": INFERENCE_LIMITS_L16_01,
    }

if __name__ == "__main__":
    res = run_activity_l16_01(verbose=True)
    sys.exit(0 if res["disposition"] == "PASS" else 1)
