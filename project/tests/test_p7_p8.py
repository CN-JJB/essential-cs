"""P7 (configuration/reproducibility) and P8 (observability) tests."""

from __future__ import annotations

import json
import os
import shutil
import unittest

from _support import PASSWORD, RunningStack, temp_dir

from minicloud.config import Config, environment_report
from minicloud.errors import ConfigurationError
from minicloud.observability import REDACTED, Observability, sanitize_fields
from minicloud.walkthrough import _correlate


class TestP7Configuration(unittest.TestCase):
    def test_defaults_contain_no_secret_and_no_dependency(self):
        config = Config.from_env({})
        self.assertIsNone(config.indexer_url)
        self.assertFalse(any("password" in field for field in config.__dataclass_fields__))
        self.assertEqual(config.host, "127.0.0.1")  # local-only by default

    def test_invalid_values_fail_closed(self):
        with self.assertRaises(ConfigurationError):
            Config.from_env({"MINICLOUD_PBKDF2_ITERATIONS": "100"})
        with self.assertRaises(ConfigurationError):
            Config.from_env({"MINICLOUD_PORT": "99999"})
        with self.assertRaises(ConfigurationError):
            Config.from_env({"MINICLOUD_DEP_TIMEOUT_MS": "0"})
        with self.assertRaises(ConfigurationError):
            Config.from_env({"MINICLOUD_MAX_BODY_BYTES": "10"})
        with self.assertRaises(ConfigurationError):
            Config.from_env({"MINICLOUD_LIST_LIMIT": "100000"})

    def test_environment_floors_are_met_here(self):
        report = environment_report()
        self.assertTrue(report["python_ok"], report)
        self.assertTrue(report["sqlite_ok"], report)

    def test_same_code_different_config(self):
        """Reproducibility boundary: only injected config differs."""
        a = Config.from_env({"MINICLOUD_DB_PATH": "a.db", "MINICLOUD_PORT": "8001"})
        b = Config.from_env({"MINICLOUD_DB_PATH": "b.db", "MINICLOUD_PORT": "8002"})
        self.assertNotEqual(a.db_path, b.db_path)
        self.assertNotEqual(a.port, b.port)


class TestP8Observability(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def test_redaction_removes_secret_bearing_fields(self):
        record = sanitize_fields(
            {
                "token": "super-secret",
                "password": "hunter2",
                "Authorization": "Bearer abc",
                "session_token_hash": "deadbeef",
                "title": "a normal title",
            }
        )
        self.assertEqual(record["token"], REDACTED)
        self.assertEqual(record["password"], REDACTED)
        self.assertEqual(record["Authorization"], REDACTED)
        self.assertEqual(record["session_token_hash"], REDACTED)
        self.assertEqual(record["title"], "a normal title")

    def test_long_free_text_is_truncated(self):
        record = sanitize_fields({"body": "x" * 500})
        self.assertLess(len(record["body"]), 500)
        self.assertIn("…", record["body"])

    def test_request_id_is_returned_and_logged(self):
        log_path = os.path.join(self.tmp, "mc.log")
        with RunningStack(self.tmp, MINICLOUD_LOG_PATH=log_path) as stack:
            token = stack.register_and_login("alice")
            rid = "test-request-id-0001"
            outcome = stack.client.request(
                "POST",
                "/v1/items",
                body={"kind": "note", "title": "correlated"},
                token=token,
                request_id=rid,
            )
            self.assertEqual(outcome.request_id, rid)

        events = _correlate(log_path, rid)
        self.assertIn("http.request", events["events"])
        self.assertIn("item.created", events["events"])

    def test_password_never_reaches_the_log(self):
        log_path = os.path.join(self.tmp, "mc.log")
        with RunningStack(self.tmp, MINICLOUD_LOG_PATH=log_path) as stack:
            stack.register_and_login("alice")
        with open(log_path, encoding="utf-8") as handle:
            blob = handle.read()
        self.assertNotIn(PASSWORD, blob)

    def test_metrics_have_bounded_labels_and_record_latency(self):
        with RunningStack(self.tmp) as stack:
            stack.register_and_login("alice")
            snapshot = stack.service.metrics_snapshot()
        self.assertIn("requests_total", snapshot["counters"])
        self.assertGreater(snapshot["counters"]["requests_total"], 0)
        self.assertIn("item_id", snapshot["labels"]["excluded"])
        self.assertTrue(snapshot["latency_ms"])
        for route, entry in snapshot["latency_ms"].items():
            self.assertIn("mean_ms", entry)
            self.assertGreaterEqual(entry["count"], 1)

    def test_logging_failure_does_not_break_the_request(self):
        # A log path in a non-creatable location must be swallowed, not raised.
        obs = Observability(log_path="\0invalid/path.log")
        record = obs.log("test.event", request_id="x", token="secret")
        self.assertEqual(record["token"], REDACTED)

    def test_log_lines_are_valid_json(self):
        log_path = os.path.join(self.tmp, "json.log")
        obs = Observability(log_path=log_path)
        obs.log("a", request_id="1", value=5)
        obs.log("b", request_id="2", nested={"k": "v"})
        with open(log_path, encoding="utf-8") as handle:
            for line in handle:
                json.loads(line)


if __name__ == "__main__":
    unittest.main()
