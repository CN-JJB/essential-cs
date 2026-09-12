"""P5 (concurrency/transactions) and P6 (durable recovery) tests."""

from __future__ import annotations

import os
import shutil
import sqlite3
import unittest

from _support import PASSWORD, make_service, temp_dir

from minicloud.errors import StorageError
from minicloud.race import (
    demonstrate_lost_update,
    demonstrate_optimistic_protection,
    demonstrate_serialized_increment,
    run_concurrency_demo,
)
from minicloud.store import Store


class TestP5Concurrency(unittest.TestCase):
    def test_naive_read_modify_write_loses_an_update(self):
        result = demonstrate_lost_update()
        self.assertTrue(result["lost_update_observed"])
        self.assertEqual(result["both_read_version"], [1, 1])
        self.assertEqual(result["final_title"], "writer-B")

    def test_optimistic_version_check_prevents_the_lost_update(self):
        result = demonstrate_optimistic_protection()
        self.assertTrue(result["first_write_applied"])
        self.assertTrue(result["second_write_rejected"])
        self.assertTrue(result["no_lost_update"])
        self.assertEqual(result["final_title"], "writer-A")

    def test_serialized_transaction_keeps_the_invariant(self):
        result = demonstrate_serialized_increment(threads=6, per_thread=20)
        self.assertTrue(result["invariant_holds"])
        self.assertEqual(result["observed_final_value"], 6 * 20)
        self.assertTrue(result["threads_joined"])

    def test_concurrency_demo_disposition(self):
        self.assertEqual(run_concurrency_demo()["disposition"], "PASS")

    def test_http_conflict_returns_409(self):
        tmp = temp_dir()
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        from _support import RunningStack

        with RunningStack(tmp) as stack:
            token = stack.register_and_login("alice")
            item = stack.client.create_item(token, kind="note", title="v1").body
            first = stack.client.update_item(token, item["item_id"], expected_version=1, title="v2")
            stale = stack.client.update_item(token, item["item_id"], expected_version=1, title="v3")
            self.assertEqual(first.status, 200)
            self.assertEqual(stale.status, 409)
            self.assertEqual(stale.body["error"]["code"], "conflict")
            self.assertEqual(stale.body["error"]["details"]["current_version"], 2)


class TestP6Recovery(unittest.TestCase):
    def setUp(self):
        self.tmp = temp_dir()
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))

    def test_backup_and_restore_round_trip(self):
        service, config, _obs = make_service(self.tmp)
        service.create_user("alice", PASSWORD)
        identity = service.authenticate(service.login("alice", PASSWORD)["token"])
        item = service.create_item(identity, kind="note", title="before-backup")

        backup_path = os.path.join(self.tmp, "backup.db")
        service.store.backup_to(backup_path)
        self.assertTrue(os.path.exists(backup_path))

        # Mutate after the backup, then restore and confirm we are back at the
        # declared recovery point.
        service.create_item(identity, kind="note", title="after-backup")
        self.assertEqual(service.store.count_items(identity["user_id"]), 2)

        service.store.restore_from(backup_path)
        self.assertEqual(service.store.count_items(identity["user_id"]), 1)
        self.assertEqual(service.store.integrity_check(), "ok")

    def test_restore_refuses_a_corrupt_backup(self):
        service, _config, _obs = make_service(self.tmp)
        corrupt = os.path.join(self.tmp, "corrupt.db")
        with open(corrupt, "wb") as handle:
            handle.write(b"this is definitely not a sqlite database" * 10)
        with self.assertRaises(StorageError):
            service.store.restore_from(corrupt)

    def test_restore_refuses_a_missing_backup(self):
        service, _config, _obs = make_service(self.tmp)
        with self.assertRaises(StorageError):
            service.store.restore_from(os.path.join(self.tmp, "nope.db"))

    def test_schema_version_is_recorded_and_stable(self):
        store = Store(os.path.join(self.tmp, "v.db"))
        store.initialize()
        self.assertEqual(store.schema_version(), 2)
        store.initialize()
        self.assertEqual(store.schema_version(), 2)

    def test_uninitialized_database_reports_version_zero_then_initializes(self):
        store = Store(os.path.join(self.tmp, "fresh.db"))
        self.assertEqual(store.schema_version(), 0)
        self.assertEqual(store.initialize(), [1, 2])
        self.assertEqual(store.schema_version(), 2)

    def test_restored_database_still_enforces_ownership(self):
        service, _config, _obs = make_service(self.tmp)
        service.create_user("alice", PASSWORD)
        service.create_user("bob", PASSWORD)
        alice = service.authenticate(service.login("alice", PASSWORD)["token"])
        bob = service.authenticate(service.login("bob", PASSWORD)["token"])
        service.create_item(alice, kind="note", title="private")

        backup = os.path.join(self.tmp, "b.db")
        service.store.backup_to(backup)
        service.store.restore_from(backup)

        from minicloud.errors import NotFoundError

        # Re-authenticate after restore (sessions were part of the backup too).
        bob2 = service.authenticate(service.login("bob", PASSWORD)["token"])
        listing = service.list_items(bob2)
        self.assertEqual(listing["count"], 0)
        self.assertGreaterEqual(service.list_items(service.authenticate(service.login("alice", PASSWORD)["token"]))["count"], 1)

    def test_integrity_check_reports_ok(self):
        service, _config, _obs = make_service(self.tmp)
        self.assertEqual(service.store.integrity_check(), "ok")

    def test_reset_removes_database_and_sidecars(self):
        store = Store(os.path.join(self.tmp, "r.db"))
        store.initialize()
        removed = store.reset()
        self.assertTrue(any(p.endswith("r.db") for p in removed))
        self.assertFalse(os.path.exists(store.db_path))
        # Idempotent: a second reset removes nothing and does not error.
        self.assertEqual(store.reset(), [])


class TestMigrationSemantics(unittest.TestCase):
    def test_partial_migration_does_not_report_success(self):
        """A migration that fails must roll back and leave the old version."""
        from minicloud import schema

        tmp = temp_dir()
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        db = os.path.join(tmp, "m.db")
        conn = sqlite3.connect(db, isolation_level=None)
        conn.row_factory = sqlite3.Row
        try:
            schema.apply_migrations(conn)
            self.assertEqual(schema.schema_version(conn), 2)

            # Force a re-run of migration 2 with a statement that must fail.
            conn.execute("DELETE FROM schema_version")
            conn.execute("INSERT INTO schema_version (version) VALUES (1)")
            original = schema.MIGRATIONS
            broken = [
                (1, original[0][1], original[0][2]),
                (2, "broken", ["ALTER TABLE items ADD COLUMN index_status TEXT NOT NULL DEFAULT 'none'"]),
            ]
            schema.MIGRATIONS = broken
            try:
                with self.assertRaises(sqlite3.Error):
                    schema.apply_migrations(conn)
                # Version must still be 1: the failed migration did not claim success.
                self.assertEqual(schema.schema_version(conn), 1)
            finally:
                schema.MIGRATIONS = original
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
