"""SQLite persistence layer (P0, P3, P4, P5, P6).

Everything that touches durable state goes through :class:`Store`. The rules:

* **Parameterized SQL only.** No external string ever reaches SQL as code.
* **Explicit transactions.** Multi-step mutations use ``BEGIN IMMEDIATE`` so a
  partial mutation cannot be observed (P5).
* **Optimistic concurrency.** Updates carry ``expected_version`` and bump
  ``version``; a stale writer loses the race deterministically instead of
  silently overwriting (P5 "no lost update").
* **Recoverable.** Schema version, backup, restore, and integrity checks are
  first-class so a P6 claim can actually be tested.

Connections are opened per call (never shared across threads) so the HTTP
adapter can serve concurrent requests safely.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import sqlite3
from datetime import datetime, timezone

from . import schema
from .errors import NotFoundError, StorageError, ValidationError

DB_SUFFIXES = ("", "-journal", "-wal", "-shm")


def utcnow() -> str:
    """Microsecond-resolution UTC timestamp; sortable and tie-free enough."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class Store:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    # ------------------------------------------------------------------ core
    def connect(self) -> sqlite3.Connection:
        parent = os.path.dirname(os.path.abspath(self.db_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0, isolation_level=None)
        except sqlite3.Error as exc:
            raise StorageError(f"cannot open database {self.db_path}: {exc}") from exc
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 10000")
        return conn

    @contextlib.contextmanager
    def _tx(self):
        conn = self.connect()
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield conn
            conn.execute("COMMIT")
        except BaseException:
            with contextlib.suppress(sqlite3.Error):
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    # ------------------------------------------------------------ lifecycle
    def initialize(self) -> list[int]:
        conn = self.connect()
        try:
            return schema.apply_migrations(conn)
        except sqlite3.Error as exc:
            raise StorageError(f"migration failed: {exc}") from exc
        finally:
            conn.close()

    def migrate(self) -> list[int]:
        return self.initialize()

    def schema_version(self) -> int:
        conn = self.connect()
        try:
            return schema.schema_version(conn)
        except sqlite3.Error as exc:
            raise StorageError(f"cannot read schema version: {exc}") from exc
        finally:
            conn.close()

    def integrity_check(self) -> str:
        conn = self.connect()
        try:
            return str(conn.execute("PRAGMA integrity_check").fetchone()[0])
        except sqlite3.Error as exc:
            raise StorageError(f"integrity check failed: {exc}") from exc
        finally:
            conn.close()

    # ---------------------------------------------------------------- users
    def create_user(self, user_id: str, username: str, salt: str, pwhash: str, iterations: int) -> dict:
        now = utcnow()
        try:
            with self._tx() as conn:
                conn.execute(
                    "INSERT INTO users (user_id, username, password_salt, password_hash,"
                    " password_iterations, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, username, salt, pwhash, iterations, now),
                )
        except sqlite3.IntegrityError as exc:
            raise ValidationError(f"username already exists: {username}") from exc
        return {"user_id": user_id, "username": username, "created_at": now}

    def get_user_by_username(self, username: str) -> dict | None:
        conn = self.connect()
        try:
            row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        finally:
            conn.close()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: str) -> dict | None:
        conn = self.connect()
        try:
            row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        finally:
            conn.close()
        return dict(row) if row else None

    # ------------------------------------------------------------- sessions
    def create_session(self, token_hash: str, user_id: str, expires_at: str) -> None:
        try:
            with self._tx() as conn:
                conn.execute(
                    "INSERT INTO sessions (token_hash, user_id, issued_at, expires_at, revoked_at)"
                    " VALUES (?, ?, ?, ?, NULL)",
                    (token_hash, user_id, utcnow(), expires_at),
                )
        except sqlite3.Error as exc:
            raise StorageError(f"cannot create session: {exc}") from exc

    def get_session(self, token_hash: str) -> dict | None:
        conn = self.connect()
        try:
            row = conn.execute(
                "SELECT * FROM sessions WHERE token_hash = ?", (token_hash,)
            ).fetchone()
        finally:
            conn.close()
        return dict(row) if row else None

    def revoke_session(self, token_hash: str) -> bool:
        with self._tx() as conn:
            cur = conn.execute(
                "UPDATE sessions SET revoked_at = ? WHERE token_hash = ? AND revoked_at IS NULL",
                (utcnow(), token_hash),
            )
            return cur.rowcount > 0

    def purge_expired_sessions(self, now_iso: str) -> int:
        with self._tx() as conn:
            cur = conn.execute(
                "DELETE FROM sessions WHERE expires_at < ? OR revoked_at IS NOT NULL", (now_iso,)
            )
            return cur.rowcount

    # ---------------------------------------------------------------- items
    def insert_item(
        self,
        *,
        item_id: str,
        owner_id: str,
        kind: str,
        title: str,
        body: str,
        url: str | None,
        visibility: str,
        index_status: str = "none",
        index_summary: str | None = None,
    ) -> dict:
        now = utcnow()
        try:
            with self._tx() as conn:
                conn.execute(
                    "INSERT INTO items (item_id, owner_id, kind, title, body, url, visibility,"
                    " version, created_at, updated_at, index_status, index_summary)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)",
                    (item_id, owner_id, kind, title, body, url, visibility, now, now,
                     index_status, index_summary),
                )
                row = conn.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
        except sqlite3.IntegrityError as exc:
            raise ValidationError(f"cannot create item: {exc}") from exc
        return dict(row)

    def get_item(self, item_id: str) -> dict | None:
        conn = self.connect()
        try:
            row = conn.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
        finally:
            conn.close()
        return dict(row) if row else None

    def list_items(self, owner_id: str, *, limit: int, descending: bool = True) -> list[dict]:
        order = "DESC" if descending else "ASC"
        conn = self.connect()
        try:
            rows = conn.execute(
                f"SELECT * FROM items WHERE owner_id = ? ORDER BY created_at {order} LIMIT ?",
                (owner_id, limit),
            ).fetchall()
        finally:
            conn.close()
        return [dict(r) for r in rows]

    def update_item(
        self,
        *,
        item_id: str,
        owner_id: str,
        expected_version: int,
        fields: dict,
        index_status: str | None = None,
        index_summary: str | None = None,
    ) -> dict | None:
        """Optimistic update. Returns the new row, or ``None`` on a version conflict."""
        assignments = []
        params: list = []
        for column in ("title", "body", "url", "visibility"):
            if column in fields:
                assignments.append(f"{column} = ?")
                params.append(fields[column])
        if index_status is not None:
            assignments.append("index_status = ?")
            params.append(index_status)
        if index_summary is not None:
            assignments.append("index_summary = ?")
            params.append(index_summary)
        assignments.append("version = version + 1")
        assignments.append("updated_at = ?")
        params.append(utcnow())
        params.extend([item_id, owner_id, expected_version])

        with self._tx() as conn:
            cur = conn.execute(
                f"UPDATE items SET {', '.join(assignments)}"
                " WHERE item_id = ? AND owner_id = ? AND version = ?",
                params,
            )
            if cur.rowcount == 0:
                return None
            row = conn.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()
        return dict(row)

    def delete_item(self, item_id: str, owner_id: str) -> bool:
        with self._tx() as conn:
            cur = conn.execute(
                "DELETE FROM items WHERE item_id = ? AND owner_id = ?", (item_id, owner_id)
            )
            return cur.rowcount > 0

    def count_items(self, owner_id: str) -> int:
        conn = self.connect()
        try:
            return int(
                conn.execute("SELECT COUNT(*) FROM items WHERE owner_id = ?", (owner_id,)).fetchone()[0]
            )
        finally:
            conn.close()

    def query_plan(self, owner_id: str) -> list[str]:
        """Return the SQLite access plan for the P4 list query."""
        conn = self.connect()
        try:
            rows = conn.execute(
                "EXPLAIN QUERY PLAN SELECT * FROM items WHERE owner_id = ?"
                " ORDER BY created_at DESC LIMIT ?",
                (owner_id, 50),
            ).fetchall()
        finally:
            conn.close()
        return [str(r["detail"]) for r in rows]

    # --------------------------------------------------------------- shares
    def upsert_share(self, item_id: str, grantee_id: str, granted_at: str) -> None:
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO shares (item_id, grantee_id, granted_at, revoked_at)"
                " VALUES (?, ?, ?, NULL)"
                " ON CONFLICT(item_id, grantee_id)"
                " DO UPDATE SET granted_at = excluded.granted_at, revoked_at = NULL",
                (item_id, grantee_id, granted_at),
            )

    def revoke_share(self, item_id: str, grantee_id: str) -> bool:
        with self._tx() as conn:
            cur = conn.execute(
                "UPDATE shares SET revoked_at = ? WHERE item_id = ? AND grantee_id = ?"
                " AND revoked_at IS NULL",
                (utcnow(), item_id, grantee_id),
            )
            return cur.rowcount > 0

    def active_share(self, item_id: str, grantee_id: str) -> dict | None:
        conn = self.connect()
        try:
            row = conn.execute(
                "SELECT * FROM shares WHERE item_id = ? AND grantee_id = ? AND revoked_at IS NULL",
                (item_id, grantee_id),
            ).fetchone()
        finally:
            conn.close()
        return dict(row) if row else None

    def list_shares(self, item_id: str) -> list[dict]:
        conn = self.connect()
        try:
            rows = conn.execute(
                "SELECT s.grantee_id, u.username, s.granted_at, s.revoked_at"
                " FROM shares s JOIN users u ON u.user_id = s.grantee_id"
                " WHERE s.item_id = ? ORDER BY s.granted_at",
                (item_id,),
            ).fetchall()
        finally:
            conn.close()
        return [dict(r) for r in rows]

    # ---------------------------------------------------------- idempotency
    def get_idempotent(self, key: str) -> dict | None:
        conn = self.connect()
        try:
            row = conn.execute("SELECT * FROM idempotency WHERE key = ?", (key,)).fetchone()
        finally:
            conn.close()
        return dict(row) if row else None

    def put_idempotent(self, key: str, user_id: str, operation: str, response_json: str) -> None:
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO idempotency (key, user_id, operation, response_json, created_at)"
                " VALUES (?, ?, ?, ?, ?)"
                " ON CONFLICT(key) DO NOTHING",
                (key, user_id, operation, response_json, utcnow()),
            )

    # ------------------------------------------------------------ recovery
    def backup_to(self, target_path: str) -> str:
        parent = os.path.dirname(os.path.abspath(target_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        if os.path.exists(target_path):
            os.remove(target_path)
        source = self.connect()
        try:
            dest = sqlite3.connect(target_path)
            try:
                source.backup(dest)
            finally:
                dest.close()
        except sqlite3.Error as exc:
            raise StorageError(f"backup failed: {exc}") from exc
        finally:
            source.close()
        return target_path

    def restore_from(self, source_path: str) -> None:
        if not os.path.exists(source_path):
            raise StorageError(f"backup file does not exist: {source_path}")
        # Validate the backup is a readable database before clobbering live state.
        probe = sqlite3.connect(source_path)
        try:
            check = probe.execute("PRAGMA integrity_check").fetchone()[0]
            if str(check) != "ok":
                raise StorageError(f"refusing to restore a corrupt backup: {check}")
        except sqlite3.DatabaseError as exc:
            raise StorageError(f"refusing to restore an unreadable backup: {exc}") from exc
        finally:
            probe.close()

        parent = os.path.dirname(os.path.abspath(self.db_path))
        if parent:
            os.makedirs(parent, exist_ok=True)
        source = sqlite3.connect(source_path)
        try:
            dest = self.connect()
            try:
                source.backup(dest)
            finally:
                dest.close()
        except sqlite3.Error as exc:
            raise StorageError(f"restore failed: {exc}") from exc
        finally:
            source.close()

    def require_item(self, item_id: str) -> dict:
        item = self.get_item(item_id)
        if item is None:
            raise NotFoundError("item not found")
        return item

    # ----------------------------------------------------------------- misc
    def reset(self) -> list[str]:
        """Remove the database and its sidecar files. Idempotent."""
        removed = []
        for suffix in DB_SUFFIXES:
            path = self.db_path + suffix
            if os.path.exists(path):
                os.remove(path)
                removed.append(path)
        # A leftover directory from a corrupt path is not silently deleted.
        if os.path.isdir(self.db_path):
            shutil.rmtree(self.db_path, ignore_errors=True)
            removed.append(self.db_path)
        return removed
