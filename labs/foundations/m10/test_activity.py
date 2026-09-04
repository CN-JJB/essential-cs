#!/usr/bin/env python3
"""
M10 Automated Activity Test Suite.

Verifies:
1. Endpoint observation on dynamic port 0 (getsockname, 16-byte exchange, clean teardown).
2. TCP byte-stream reconstruction across arbitrary recv() buffer partitions (framing loop).
3. UDP datagram boundary preservation.
4. Failure fixture cases (active refusal, silent read timeout, DNS .invalid observation).
5. Teardown and reset idempotency.

Strictly enforces Essential CS invariants:
- Port 0 allocation only;
- No hardcoded errno assertions;
- No fixed latency or timeout ratio assertions;
- Truthful reporting of optional tool capabilities.
"""

import socket
import unittest

from endpoint_observer import inspect_host_tools, run_endpoint_observation
from failure_fixture import (
    observe_dns_failure,
    observe_loopback_refusal,
    observe_read_timeout,
    run_all_failure_observations,
)
from reset import probe_endpoint_after_close, run_reset
from stream_framing import run_tcp_stream_reconstruction, run_udp_datagram_contrast


class TestM10EndpointObserver(unittest.TestCase):
    """L10-01 tests: dynamic port allocation, addressing, and loopback exchange."""

    def test_dynamic_port_and_loopback_exchange(self):
        record = run_endpoint_observation(b"0123456789ABCDEF")
        self.assertTrue(record["exchange_success"], f"Exchange failed: {record.get('error')}")
        self.assertEqual(record["payload_received"], "0123456789ABCDEF")

        # Invariant: Port must be dynamically assigned (non-zero)
        assigned_port = record["assigned_endpoint"]["port"]
        self.assertIsInstance(assigned_port, int)
        self.assertGreater(assigned_port, 0)
        self.assertEqual(record["assigned_endpoint"]["host"], "127.0.0.1")

        # Invariant: Process ID is recorded
        self.assertGreater(record["process_id"], 0)

        # Invariant: a fresh connection is not established to the old course endpoint.
        # Record the raw host disposition without requiring one errno/exception.
        cleanup_probe = probe_endpoint_after_close("127.0.0.1", assigned_port)
        self.assertFalse(cleanup_probe["connection_established"], cleanup_probe)

    def test_invalid_payload_length_rejected(self):
        with self.assertRaises(ValueError):
            run_endpoint_observation(b"TOO_SHORT")

    def test_inspect_host_tools_truthful(self):
        tools = inspect_host_tools()
        self.assertIn("ss", tools)
        self.assertIn("ip_route", tools)
        self.assertIsInstance(tools["ss"]["available"], bool)
        self.assertIsInstance(tools["ip_route"]["available"], bool)


class TestM10StreamFraming(unittest.TestCase):
    """L10-02 tests: TCP stream reconstruction and UDP datagram contrast."""

    def test_tcp_stream_reconstruction_varying_buffers(self):
        test_messages = [
            b"HELLO_WORLD",
            b"STREAM_RECORD_2",
            b"TINY",
            b"A_LONGER_BLOCK_TO_TEST_PARTITIONING_ACROSS_RECV_CALLS_RELIABLY",
            b"END",
        ]

        # Test with multiple buffer sizes to enforce receiver loop independence
        for buf_size in [7, 13, 32, 1024]:
            with self.subTest(buffer_size=buf_size):
                result = run_tcp_stream_reconstruction(test_messages, buffer_size=buf_size)
                self.assertTrue(
                    result["reconstruction_matches"],
                    f"Failed reconstruction with buffer {buf_size}: {result.get('error')}",
                )
                self.assertEqual(len(result["reconstructed_messages"]), len(test_messages))
                # Verify that recv() partitions were recorded empirically
                self.assertGreater(len(result["actual_recv_partitions"]), 0)
                # Verify logical byte count invariant
                expected_total = sum(len(m) for m in test_messages)
                self.assertEqual(result["total_logical_bytes_sent"], expected_total)

    def test_udp_datagram_preservation(self):
        test_datagrams = [
            b"DATAGRAM_ONE",
            b"DATAGRAM_TWO_WITH_DIFFERENT_LENGTH",
            b"DATAGRAM_THREE",
        ]
        result = run_udp_datagram_contrast(test_datagrams)
        self.assertTrue(result["boundaries_preserved"], f"UDP test failed: {result.get('error')}")
        self.assertEqual(result["datagrams_received_count"], len(test_datagrams))


class TestM10FailureFixture(unittest.TestCase):
    """L10-03 tests: refusal, read timeout, DNS .invalid, and partial failure."""

    def test_loopback_refusal_observation(self):
        refusal = observe_loopback_refusal()
        self.assertTrue(refusal["success"], "Expected refusal observation to succeed")
        self.assertEqual(refusal["disposition"], "CONNECTION_REFUSED_OBSERVED")
        # Raw host exception/errno/timing are evidence only, never acceptance constants.
        self.assertIsNotNone(refusal["exception_type"])
        self.assertIsNotNone(refusal["elapsed_ms"])

    def test_read_timeout_observation(self):
        # Configure a short deadline and bounded watchdog
        deadline_s = 0.2
        timeout = observe_read_timeout(client_deadline_s=deadline_s, harness_watchdog_s=2.0)
        self.assertTrue(timeout["success"], f"Read timeout failed: {timeout.get('error')}")
        self.assertEqual(timeout["disposition"], "READ_TIMEOUT_OBSERVED")
        # Record the implementation-specific timeout exception and raw elapsed sample.
        # Do not enforce a class name, millisecond threshold, or ratio.
        self.assertIsNotNone(timeout["exception_type"])
        self.assertIsNotNone(timeout["elapsed_ms"])

    def test_dns_failure_observation(self):
        dns = observe_dns_failure("essential-cs-m10-test.invalid")
        # Invariant: disposition must be either LIVE_DNS_FAILURE_OBSERVED or NO_LIVE_DNS_FAILURE_OBSERVATION
        self.assertIn(
            dns["disposition"],
            ["LIVE_DNS_FAILURE_OBSERVED", "NO_LIVE_DNS_FAILURE_OBSERVATION"],
        )
        if dns["disposition"] == "LIVE_DNS_FAILURE_OBSERVED":
            self.assertTrue(dns["success"])
            self.assertIsNotNone(dns["exception_type"])

    def test_run_all_failure_fixture_integrated(self):
        all_res = run_all_failure_observations()
        self.assertTrue(all_res["refusal_observation"]["success"])
        self.assertTrue(all_res["read_timeout_observation"]["success"])
        self.assertIn("partial_failure_doctrine", all_res)


class TestM10Reset(unittest.TestCase):
    """Teardown and reset verification."""

    def test_reset_idempotent(self):
        # First reset
        r1 = run_reset()
        self.assertEqual(r1["status"], "CLEAN_NO_PERSISTENT_ARTIFACTS")
        # Second reset immediately follows
        r2 = run_reset()
        self.assertEqual(r2["status"], "CLEAN_NO_PERSISTENT_ARTIFACTS")
        self.assertTrue(r2["idempotent"])


if __name__ == "__main__":
    unittest.main()
