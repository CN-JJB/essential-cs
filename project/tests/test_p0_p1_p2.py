"""P0 (durable collection), P1 (boundary), P2 (trust boundary) tests."""

from __future__ import annotations

import http.client
import json
import os
import sqlite3
import unittest

import _support
from _support import PASSWORD, RunningStack, make_service, temp_dir

from minicloud.errors import ConflictError, NotFoundError, UnauthenticatedError, ValidationError


class TestP0Persistence(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))

    def test_migrations_reach_target_and_are_idempotent(self):
        service, _config, _obs = make_service(self.tmp)
        self.assertEqual(service.store.schema_version(), 2)
        # Re-running must not error and must not re-apply.
        self.assertEqual(service.store.migrate(), [])
        self.assertEqual(service.store.schema_version(), 2)

    def test_write_read_restart_persistence(self):
        service, config, _obs = make_service(self.tmp)
        service.create_user("alice", PASSWORD)
        token = service.login("alice", PASSWORD)["token"]
        identity = service.authenticate(token)
        created = service.create_item(identity, kind="note", title="durable", body="payload")

        # Simulate a process restart: brand-new store/service objects on the same file.
        from minicloud.store import Store

        reopened = Store(config.db_path)
        from minicloud.service import MiniCloudService

        service2 = MiniCloudService(store=reopened, config=config)
        service2.initialize()
        again = service2.get_item(service2.authenticate(token), created["item_id"])
        self.assertEqual(again["title"], "durable")
        self.assertEqual(again["body"], "payload")

    def test_external_input_is_data_not_sql(self):
        service, _config, _obs = make_service(self.tmp)
        service.create_user("alice", PASSWORD)
        identity = service.authenticate(service.login("alice", PASSWORD)["token"])
        hostile = "'; DROP TABLE items; --"
        item = service.create_item(identity, kind="note", title=hostile)
        self.assertEqual(item["title"], hostile)
        # The table must still exist and the row must still be readable.
        self.assertEqual(service.get_item(identity, item["item_id"])["title"], hostile)
        self.assertEqual(service.store.count_items(identity["user_id"]), 1)

    def test_owner_and_identifier_invariants(self):
        service, _config, _obs = make_service(self.tmp)
        service.create_user("alice", PASSWORD)
        identity = service.authenticate(service.login("alice", PASSWORD)["token"])
        ids = {service.create_item(identity, kind="note", title=f"n{i}")["item_id"] for i in range(5)}
        self.assertEqual(len(ids), 5)  # stable, unique identifiers
        # An item cannot be represented without a valid owner (FK enforced).
        conn = service.store.connect()
        try:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO items (item_id, owner_id, kind, title, body, url, visibility,"
                    " version, created_at, updated_at, index_status)"
                    " VALUES ('x','ghost','note','t','',NULL,'private',1,'n','n','none')"
                )
        finally:
            conn.close()


class TestP1Boundary(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))

    def _stack(self, **overrides):
        stack = RunningStack(self.tmp, **overrides)
        self.addCleanup(stack.__exit__, None, None, None)
        return stack.__enter__()

    def test_health_and_roundtrip(self):
        stack = self._stack()
        self.assertEqual(stack.client.health().status, 200)
        token = stack.register_and_login("alice")
        created = stack.client.create_item(token, kind="note", title="hi")
        self.assertEqual(created.status, 201)
        fetched = stack.client.get_item(token, created.body["item_id"])
        self.assertEqual(fetched.body["title"], "hi")

    def test_malformed_json_rejected_at_boundary(self):
        stack = self._stack()
        conn = http.client.HTTPConnection("127.0.0.1", int(stack.base_url.rsplit(":", 1)[1]), timeout=5)
        try:
            conn.request(
                "POST",
                "/v1/users",
                body=b"{not json",
                headers={"Content-Type": "application/json", "Content-Length": "9"},
            )
            response = conn.getresponse()
            payload = json.loads(response.read().decode())
        finally:
            conn.close()
        self.assertEqual(response.status, 400)
        self.assertEqual(payload["error"]["code"], "validation_error")

    def test_oversized_body_rejected(self):
        stack = self._stack(MINICLOUD_MAX_BODY_BYTES="1024")
        token = stack.register_and_login("alice")
        outcome = stack.client.request(
            "POST", "/v1/items", body={"kind": "note", "title": "x" * 5000}, token=token
        )
        self.assertEqual(outcome.status, 413)
        self.assertEqual(outcome.body["error"]["code"], "payload_too_large")

    def test_unknown_path_and_wrong_method_are_distinguished(self):
        stack = self._stack()
        self.assertEqual(stack.client.request("GET", "/v1/nope").status, 404)
        self.assertEqual(stack.client.request("POST", "/health", body={}).status, 405)

    def test_invalid_enum_and_url_rejected(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        self.assertEqual(stack.client.create_item(token, kind="bogus", title="t").status, 400)
        self.assertEqual(
            stack.client.create_item(token, kind="bookmark", title="t", url="ftp://x").status, 400
        )


class TestP2TrustBoundary(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))

    def _stack(self, **overrides):
        stack = RunningStack(self.tmp, **overrides)
        self.addCleanup(stack.__exit__, None, None, None)
        return stack.__enter__()

    def test_authentication_is_required(self):
        stack = self._stack()
        self.assertEqual(stack.client.request("GET", "/v1/items").status, 401)
        self.assertEqual(stack.client.request("GET", "/v1/items", token="not-a-token").status, 401)

    def test_bad_password_rejected(self):
        stack = self._stack()
        stack.client.create_user("alice", PASSWORD)
        self.assertEqual(stack.client.login("alice", "wrong-password").status, 401)

    def test_cross_user_read_is_indistinguishable_from_missing(self):
        stack = self._stack()
        alice = stack.register_and_login("alice")
        bob = stack.register_and_login("bob")
        item = stack.client.create_item(alice, kind="note", title="private").body["item_id"]

        real_missing = stack.client.get_item(bob, "0" * 32)
        cross_user = stack.client.get_item(bob, item)
        self.assertEqual(cross_user.status, 404)
        self.assertEqual(cross_user.status, real_missing.status)
        # The denial must be indistinguishable: identical code and message.
        # (request_id is per-request transport metadata, not part of the denial.)
        self.assertEqual(cross_user.body["error"]["code"], real_missing.body["error"]["code"])
        self.assertEqual(cross_user.body["error"]["message"], real_missing.body["error"]["message"])
        self.assertIn("request_id", cross_user.body["error"])

    def test_cross_user_write_and_delete_denied(self):
        stack = self._stack()
        alice = stack.register_and_login("alice")
        bob = stack.register_and_login("bob")
        item = stack.client.create_item(alice, kind="note", title="private").body["item_id"]
        self.assertEqual(
            stack.client.update_item(bob, item, expected_version=1, title="hijack").status, 404
        )
        self.assertEqual(stack.client.delete_item(bob, item).status, 404)

    def test_share_grants_then_revocation_removes_access(self):
        stack = self._stack()
        alice = stack.register_and_login("alice")
        bob = stack.register_and_login("bob")
        item = stack.client.create_item(alice, kind="note", title="shared").body["item_id"]

        self.assertEqual(stack.client.get_item(bob, item).status, 404)
        self.assertEqual(stack.client.share_item(alice, item, "bob").status, 201)
        shared = stack.client.get_item(bob, item)
        self.assertEqual(shared.status, 200)
        self.assertFalse(shared.body["is_owner"])
        self.assertEqual(stack.client.revoke_share(alice, item, "bob").status, 200)
        self.assertEqual(stack.client.get_item(bob, item).status, 404)

    def test_shared_item_cannot_be_written_by_grantee(self):
        stack = self._stack()
        alice = stack.register_and_login("alice")
        bob = stack.register_and_login("bob")
        item = stack.client.create_item(alice, kind="note", title="shared").body["item_id"]
        stack.client.share_item(alice, item, "bob")
        self.assertEqual(stack.client.update_item(bob, item, expected_version=1, title="x").status, 404)

    def test_no_plaintext_password_or_raw_token_is_stored(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        with open(stack.config.db_path, "rb") as handle:
            blob = handle.read()
        self.assertNotIn(PASSWORD.encode("utf-8"), blob)
        self.assertNotIn(token.encode("utf-8"), blob)

    def test_session_revocation(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        self.assertEqual(stack.client.list_items(token).status, 200)
        self.assertEqual(stack.client.logout(token).status, 200)
        self.assertEqual(stack.client.list_items(token).status, 401)

    def test_expired_session_rejected(self):
        stack = self._stack()
        token = stack.register_and_login("alice")
        conn = stack.service.store.connect()
        try:
            conn.execute("UPDATE sessions SET expires_at = '1970-01-01T00:00:00.000000Z'")
        finally:
            conn.close()
        self.assertEqual(stack.client.list_items(token).status, 401)


class TestServiceErrors(unittest.TestCase):
    def test_typed_errors_map_to_expected_codes(self):
        self.assertEqual(ValidationError("x").http_status, 400)
        self.assertEqual(UnauthenticatedError("x").http_status, 401)
        self.assertEqual(NotFoundError("x").http_status, 404)
        self.assertEqual(ConflictError("x").http_status, 409)


if __name__ == "__main__":
    unittest.main()
