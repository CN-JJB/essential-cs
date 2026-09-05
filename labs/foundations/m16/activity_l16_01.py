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
from typing import Any, Dict

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


def run_activity_l16_01(verbose: bool = True) -> Dict[str, Any]:
    """
    Executes the deterministic L16-01 observation.
    Coordinates an application-layer delay such that the client times out,
    while the server completes the exact same request ID after the client stopped waiting.
    """
    fault_shim = FaultShim()
    server = RPCServer(fault_shim=fault_shim)
    port = server.start()

    client = RPCClient(host="127.0.0.1", port=port, default_timeout=0.3)
    target_req_id = f"l16-01-req-{int(time.time() * 1000)}"

    # Coordination: client gives up at 0.3s.
    # Server business handler pauses for 0.6s before finishing execution.
    server_completed_event = threading.Event()
    server_execution_record: Dict[str, Any] = {}

    def delayed_business_method(params: dict) -> dict:
        account = params.get("account", "acc-01")
        amount = params.get("amount", 100)
        # Introduce application-layer processing latency
        time.sleep(0.6)
        completion_time = time.time()
        server_execution_record["account"] = account
        server_execution_record["amount"] = amount
        server_execution_record["completion_time"] = completion_time
        server_completed_event.set()
        return {"status": "SUCCESS", "debited": amount, "timestamp": completion_time}

    server.register_method("debit_account", delayed_business_method)

    client_stopped_time: float = 0.0
    client_outcome: str = "UNKNOWN"
    client_exception_type: Optional[str] = None

    if verbose:
        print("=" * 72)
        print(" Activity L16-01: Partial Failure & No-Response Ambiguity")
        print("=" * 72)
        print(f" [Localhost RPC Server]: Listening on 127.0.0.1:{port} (ephemeral)")
        print(f" [Target Request ID]:   {target_req_id}")
        print(" [Client Deadline]:       300ms")
        print(" [Server Execution Time]: 600ms (Application-layer simulated delay)")
        print(" Disagreeing clocks and independent process lifecycles engaged...")

    dispatch_time = time.time()
    try:
        # Client executes with 300ms timeout, NO_RETRY
        client.call(
            method="debit_account",
            params={"account": "user-wallet-42", "amount": 100},
            request_id=target_req_id,
            timeout=0.3,
            retry_policy=RetryPolicy.NO_RETRY,
            max_attempts=1,
        )
        client_outcome = "UNEXPECTED_SUCCESS"
    except (TimeoutError, Exception) as e:
        client_stopped_time = time.time()
        client_outcome = "TIMEOUT_STOPPED_WAITING"
        client_exception_type = type(e).__name__
        if verbose:
            print(f" [Client Event]: Stopped waiting after {client_stopped_time - dispatch_time:.3f}s")
            print(f"   Observed Outcome: {client_exception_type}")

    # Wait for server thread to finish execution
    server_finished = server_completed_event.wait(timeout=2.0)
    server_completed_time = server_execution_record.get("completion_time", 0.0)

    # Audit server records
    server_audit_entry = None
    for entry in server.audit_log:
        if entry.get("request_id") == target_req_id and entry.get("event") == "SERVER_COMPLETED_EXECUTION":
            server_audit_entry = entry
            break

    identical_id_confirmed = server_audit_entry is not None
    server_completed_after_client = server_completed_time > client_stopped_time

    if verbose:
        print(f" [Server Event]: Execution completed at {server_completed_time - dispatch_time:.3f}s")
        print(f"   Identical Request ID: {target_req_id}")
        print(f"   Completed after client stopped waiting: {server_completed_after_client}")
        print(" [Inference]:")
        print("   Local timeout DID NOT cancel remote execution!")
        print("   Client experienced failure/silence while server successfully committed state.")
        print("=" * 72)

    # Clean shutdown
    server.stop()

    passed = (
        client_outcome == "TIMEOUT_STOPPED_WAITING"
        and identical_id_confirmed
        and server_completed_after_client
    )

    return {
        "disposition": "PASS" if passed else "FAIL",
        "request_id": target_req_id,
        "client_timeout_configured_sec": 0.3,
        "client_outcome": client_outcome,
        "client_exception_type": client_exception_type,
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
