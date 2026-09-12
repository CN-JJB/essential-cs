"""P3 (network path, timeout, retry, idempotency) and P4 (measurement) tests."""

from __future__ import annotations

import http.client
import shutil
import socket
import unittest
from unittest import mock

from _support import BlackHoleServer, RunningStack, temp_dir

from minicloud.bench import run_benchmark
from minicloud.client import MiniCloudClient


def _raising_connection(exc: BaseException):
    """A stand-in HTTPConnection whose every request raises ``exc``."""
    connection = mock.MagicMock()
    connection.request.side_effect = exc
    return connection


def _free_port() -> int:
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


class TestP3NetworkAndFailure(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def _stack(self, **overrides):
        stack = RunningStack(self.tmp, **overrides)
        self.addCleanup(stack.__exit__, None, None, None)
        return stack.__enter__()

    def test_client_timeout_is_reported_as_ambiguous(self):
        blackhole = BlackHoleServer()
        self.addCleanup(blackhole.close)
        client = MiniCloudClient(blackhole.url, timeout_ms=300)
        outcome = client.request("POST", "/v1/items", body={"kind": "note", "title": "x"})
        self.assertIsNone(outcome.status)
        self.assertTrue(outcome.ambiguous)
        self.assertEqual(outcome.error, "timeout")

    def test_connection_refused_is_not_ambiguous(self):
        """A refused connection is a definite failure, unlike a timeout.

        Driven with an injected exception because whether a closed loopback port
        refuses or blackholes is host-dependent; the *policy* is what is under
        test here.
        """
        client = MiniCloudClient("http://127.0.0.1:9", timeout_ms=500, max_attempts=1)
        with mock.patch.object(
            http.client, "HTTPConnection", return_value=_raising_connection(ConnectionRefusedError())
        ):
            outcome = client.request("POST", "/v1/items", body={"kind": "note", "title": "x"})
        self.assertIsNone(outcome.status)
        self.assertFalse(outcome.ambiguous)

    def test_safe_request_is_retried_but_mutation_is_not(self):
        client = MiniCloudClient("http://127.0.0.1:9", timeout_ms=400, max_attempts=3)
        with mock.patch.object(
            http.client, "HTTPConnection", return_value=_raising_connection(ConnectionRefusedError())
        ):
            safe = client.request("GET", "/health", safe=True)
            unsafe = client.request("POST", "/v1/items", body={"kind": "note", "title": "x"})
        self.assertEqual(safe.attempts, 3)  # safe => bounded retry
        self.assertEqual(unsafe.attempts, 1)  # mutation without idempotency key => no retry

    def test_mutation_with_idempotency_key_is_retried(self):
        client = MiniCloudClient("http://127.0.0.1:9", timeout_ms=400, max_attempts=3)
        with mock.patch.object(
            http.client, "HTTPConnection", return_value=_raising_connection(ConnectionRefusedError())
        ):
            outcome = client.request(
                "POST", "/v1/items", body={"kind": "note", "title": "x"}, idempotency_key="k1"
            )
        self.assertEqual(outcome.attempts, 3)

    def test_idempotency_key_prevents_duplicate_effect(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        first = stack.client.create_item(
            token, kind="note", title="once", idempotency_key="dup-key"
        )
        second = stack.client.create_item(
            token, kind="note", title="once", idempotency_key="dup-key"
        )
        self.assertEqual(first.status, 201)
        self.assertEqual(second.status, 201)
        self.assertTrue(second.body.get("idempotent_replay"))
        self.assertEqual(first.body["item_id"], second.body["item_id"])
        self.assertEqual(stack.client.list_items(token).body["count"], 1)

    def test_dependency_unavailable_degrades_index_not_the_item(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        stack.set_fault("unavailable")
        outcome = stack.client.create_item(
            token, kind="bookmark", title="Rust", url="https://rust-lang.org"
        )
        self.assertEqual(outcome.status, 201)
        self.assertEqual(outcome.body["index"]["status"], "pending")
        self.assertIn("dependency_unavailable", outcome.body["index"]["note"])
        # The item is durable regardless of the dependency.
        self.assertEqual(stack.client.get_item(token, outcome.body["item_id"]).status, 200)

    def test_dependency_timeout_is_distinct_and_degrades(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        stack.set_fault("slow")
        outcome = stack.client.create_item(token, kind="bookmark", title="Go", url="https://go.dev")
        self.assertEqual(outcome.status, 201)
        self.assertEqual(outcome.body["index"]["status"], "pending")
        self.assertIn("dependency_timeout", outcome.body["index"]["note"])

    def test_recovery_reindex_after_dependency_returns(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        stack.set_fault("unavailable")
        created = stack.client.create_item(
            token, kind="bookmark", title="Rust", url="https://rust-lang.org"
        )
        item_id = created.body["item_id"]
        self.assertEqual(created.body["index"]["status"], "pending")

        stack.set_fault("ok")
        recovered = stack.client.reindex_item(token, item_id)
        self.assertEqual(recovered.status, 200)
        self.assertEqual(recovered.body["index"]["status"], "ready")
        self.assertTrue(recovered.body["index"]["summary"])

    def test_healthy_dependency_indexes_immediately(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        outcome = stack.client.create_item(
            token, kind="bookmark", title="Python", url="https://python.org"
        )
        self.assertEqual(outcome.body["index"]["status"], "ready")
        self.assertIn("python.org", outcome.body["index"]["summary"])

    def test_notes_are_not_indexed(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        outcome = stack.client.create_item(token, kind="note", title="plain")
        self.assertEqual(outcome.body["index"]["status"], "none")


class TestP4Measurement(unittest.TestCase):
    def test_benchmark_is_bounded_reproducible_and_correct(self):
        result = run_benchmark(rows=800, repetitions=7, write_rows=100)
        self.assertEqual(result["disposition"], "PASS")
        self.assertTrue(result["result_equivalence"])
        # The access path must actually differ; otherwise the benchmark proves nothing.
        self.assertNotEqual(result["plan_baseline"], result["plan_indexed"])
        self.assertTrue(any("INDEX" in line for line in result["plan_indexed"]))
        self.assertTrue(any("SCAN" in line for line in result["plan_baseline"]))
        # Both sides must have been measured the stated number of times.
        self.assertEqual(result["latency_baseline"]["repetitions"], 7)
        self.assertEqual(result["latency_indexed"]["repetitions"], 7)
        self.assertGreater(result["db_size_bytes"]["index_overhead_bytes"], 0)
        # Inference limits must be stated, not implied.
        self.assertTrue(result["inference_limits"])


if __name__ == "__main__":
    unittest.main()
