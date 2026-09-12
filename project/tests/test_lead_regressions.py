"""Web Lead regression tests for PR #154 security/failure-boundary fixes."""

from __future__ import annotations

import http.client
import shutil
import unittest
from unittest import mock

from _support import RunningStack, temp_dir

from minicloud.client import MiniCloudClient
from minicloud.observability import REDACTED, sanitize_fields


class _ResetAfterSendConnection:
    """Pretend the request was sent, then lose the response connection."""

    def request(self, *args, **kwargs):
        return None

    def getresponse(self):
        raise ConnectionResetError("response connection reset")

    def close(self):
        return None


class TestLeadTrustBoundaryRegressions(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def test_idempotency_key_is_scoped_to_authenticated_user(self):
        with RunningStack(self.tmp) as stack:
            alice = stack.register_and_login("alice")
            bob = stack.register_and_login("bob")

            first = stack.client.create_item(
                alice, kind="note", title="alice-only", idempotency_key="same-client-key"
            )
            second = stack.client.create_item(
                bob, kind="note", title="bob-only", idempotency_key="same-client-key"
            )

            self.assertEqual(first.status, 201)
            self.assertEqual(second.status, 201)
            self.assertNotEqual(first.body["item_id"], second.body["item_id"])
            self.assertEqual(first.body["title"], "alice-only")
            self.assertEqual(second.body["title"], "bob-only")
            self.assertEqual(stack.client.list_items(alice).body["count"], 1)
            self.assertEqual(stack.client.list_items(bob).body["count"], 1)

    def test_same_user_same_idempotency_key_still_replays(self):
        with RunningStack(self.tmp) as stack:
            alice = stack.register_and_login("alice")
            first = stack.client.create_item(
                alice, kind="note", title="once", idempotency_key="same-user-key"
            )
            replay = stack.client.create_item(
                alice, kind="note", title="changed-input", idempotency_key="same-user-key"
            )
            self.assertEqual(replay.status, 201)
            self.assertTrue(replay.body["idempotent_replay"])
            self.assertEqual(first.body["item_id"], replay.body["item_id"])
            self.assertEqual(replay.body["title"], "once")


class TestLeadNetworkAmbiguityRegressions(unittest.TestCase):
    def test_mutation_response_reset_is_ambiguous(self):
        client = MiniCloudClient("http://127.0.0.1:9", timeout_ms=200, max_attempts=1)
        with mock.patch.object(
            http.client, "HTTPConnection", return_value=_ResetAfterSendConnection()
        ):
            outcome = client.request(
                "POST", "/v1/items", body={"kind": "note", "title": "x"}
            )
        self.assertIsNone(outcome.status)
        self.assertTrue(outcome.ambiguous)
        self.assertEqual(outcome.error, "ConnectionResetError")

    def test_safe_response_reset_remains_nonambiguous(self):
        client = MiniCloudClient("http://127.0.0.1:9", timeout_ms=200, max_attempts=1)
        with mock.patch.object(
            http.client, "HTTPConnection", return_value=_ResetAfterSendConnection()
        ):
            outcome = client.request("GET", "/health", safe=True)
        self.assertIsNone(outcome.status)
        self.assertFalse(outcome.ambiguous)


class TestLeadRedactionRegressions(unittest.TestCase):
    def test_nested_secret_fields_are_redacted_recursively(self):
        sanitized = sanitize_fields(
            {
                "context": {
                    "Authorization": "Bearer nested-secret",
                    "child": {"session_token": "nested-token", "title": "ok"},
                    "items": [{"password": "nested-password"}],
                }
            }
        )
        self.assertEqual(sanitized["context"]["Authorization"], REDACTED)
        self.assertEqual(sanitized["context"]["child"]["session_token"], REDACTED)
        self.assertEqual(sanitized["context"]["items"][0]["password"], REDACTED)
        self.assertEqual(sanitized["context"]["child"]["title"], "ok")


if __name__ == "__main__":
    unittest.main()
