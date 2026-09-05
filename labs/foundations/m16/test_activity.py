#!/usr/bin/env python3
"""
Unit tests for M16 Foundations activities (L16-01, L16-02), RPC fixture framing,
attempt budgets, concurrency, and reset idempotence.
"""

import io
import json
import os
import socket
import struct
import threading
import time
import unittest

try:
    from .activity_l16_01 import run_activity_l16_01
    from .activity_l16_02 import run_activity_l16_02
    from .reset import reset_m16_foundations
    from .rpc_fixture import (
        FaultAction,
        FaultShim,
        IdempotencyStore,
        RetryPolicy,
        RPCClient,
        RPCServer,
        recv_exact,
        recv_msg,
        send_msg,
    )
except ImportError:
    from activity_l16_01 import run_activity_l16_01
    from activity_l16_02 import run_activity_l16_02
    from reset import reset_m16_foundations
    from rpc_fixture import (
        FaultAction,
        FaultShim,
        IdempotencyStore,
        RetryPolicy,
        RPCClient,
        RPCServer,
        recv_exact,
        recv_msg,
        send_msg,
    )


class TestM16Foundations(unittest.TestCase):
    def setUp(self):
        reset_m16_foundations(verbose=False)

    def tearDown(self):
        reset_m16_foundations(verbose=False)

    def test_activity_l16_01_timeout_and_server_completion(self):
        res = run_activity_l16_01(verbose=False)
        self.assertEqual(res["disposition"], "PASS")
        self.assertEqual(res["client_outcome"], "TIMEOUT_STOPPED_WAITING")
        self.assertTrue(res["identical_request_id_confirmed"])
        self.assertTrue(res["server_completed_after_client_stopped_waiting"])
        self.assertGreater(res["server_completed_timestamp"], res["client_stopped_waiting_timestamp"])
        self.assertIn("silence_ambiguity", res["inference_limits"])
        self.assertIn("timeout_local_nature", res["inference_limits"])
        self.assertIn("transport_vs_application", res["inference_limits"])

    def test_activity_l16_02_idempotency_and_duplicates(self):
        res = run_activity_l16_02(verbose=False)
        self.assertEqual(res["disposition"], "PASS")
        self.assertTrue(res["unsafe_path"]["duplicate_effect_observed"])
        self.assertGreater(res["unsafe_path"]["delta"], 1)
        self.assertTrue(res["protected_path"]["exact_once_invariant_preserved"])
        self.assertEqual(res["protected_path"]["delta"], 1)
        self.assertTrue(res["concurrent_path"]["exact_once_invariant_preserved"])
        self.assertEqual(res["concurrent_path"]["delta"], 1)
        self.assertTrue(res["retention_boundary"]["protected_within_ttl"])
        self.assertTrue(res["retention_boundary"]["re_executed_after_purge"])
        self.assertIn("scope_of_idempotency", res["inference_limits"])
        self.assertIn("retention_boundary", res["inference_limits"])

    def test_retry_budget_enforcement(self):
        """Verifies that the client strictly enforces the total-attempt budget."""
        shim = FaultShim()
        server = RPCServer(fault_shim=shim)
        port = server.start()

        req_id = "budget-test-req"
        shim.set_rule(req_id, FaultAction.DROP_RESPONSE, max_triggers=10)

        client = RPCClient(host="127.0.0.1", port=port, default_timeout=0.1)
        max_budget = 3

        with self.assertRaises((TimeoutError, ConnectionError)):
            client.call(
                method="ping",
                params={},
                request_id=req_id,
                timeout=0.1,
                retry_policy=RetryPolicy.DETERMINISTIC,
                max_attempts=max_budget,
                base_backoff_ms=10.0,
            )

        matching_traces = [t for t in client.call_traces if t.get("request_id") == req_id]
        self.assertEqual(len(matching_traces), max_budget)
        server.stop()

    def test_message_framing_no_recv_boundary_reliance(self):
        """
        Verifies that length-prefixed framing handles fragmented stream delivery
        without relying on OS recv boundaries.
        """
        # Create a dummy socket pair using loopback listener
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.bind(("127.0.0.1", 0))
        srv_port = srv_sock.getsockname()[1]
        srv_sock.listen(1)

        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli_sock.connect(("127.0.0.1", srv_port))
        conn, _ = srv_sock.accept()

        try:
            # Construct a test message
            payload = {"test": "hello_world" * 50, "array": list(range(50))}
            raw_json = json.dumps(payload).encode("utf-8")
            header = struct.pack(">I", len(raw_json))
            full_data = header + raw_json

            # Fragment data into small slices (e.g. 7 bytes each)
            chunk_size = 7
            for i in range(0, len(full_data), chunk_size):
                conn.sendall(full_data[i : i + chunk_size])
                time.sleep(0.002)

            received = recv_msg(cli_sock)
            self.assertEqual(received, payload)
        finally:
            conn.close()
            cli_sock.close()
            srv_sock.close()

    def test_reset_idempotence(self):
        """Verifies that reset_m16_foundations runs idempotently without error."""
        this_dir = os.path.dirname(os.path.abspath(__file__))
        dummy_file = os.path.join(this_dir, "test_dummy_artifact.tmp")
        with open(dummy_file, "w") as f:
            f.write("temporary data")

        self.assertTrue(os.path.exists(dummy_file))
        removed_first = reset_m16_foundations(verbose=False)
        self.assertGreaterEqual(removed_first, 1)
        self.assertFalse(os.path.exists(dummy_file))

        # Second reset must pass cleanly with 0 removals and 0 errors
        removed_second = reset_m16_foundations(verbose=False)
        self.assertEqual(removed_second, 0)


if __name__ == "__main__":
    unittest.main()
