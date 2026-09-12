"""Versioned schema and migrations (P0/P6).

The schema is declared as an ordered list of migrations. ``apply_migrations``
brings a database from whatever version it is at (including empty) to the
latest, and records the resulting version. This is what makes a P6 recovery
claim testable: a completed migration has a *known* version, and a failed
migration must not silently claim success.

Only standard SQLite DDL is used. ``ALTER TABLE ... ADD COLUMN`` is restricted
to what SQLite actually supports (no added CHECK/UNIQUE/PKIMARY KEY), so value
validation for those columns lives in the service layer instead.
"""

from __future__ import annotations

import sqlite3

#: Current target schema version.
TARGET_VERSION = 2

#: (version, description, statements)
MIGRATIONS: list[tuple[int, str, list[str]]] = [
    (
        1,
        "base schema: users, items, shares, sessions, idempotency",
        [
            """
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id           TEXT PRIMARY KEY,
                username          TEXT NOT NULL UNIQUE,
                password_salt     TEXT NOT NULL,
                password_hash     TEXT NOT NULL,
                password_iterations INTEGER NOT NULL,
                created_at        TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS items (
                item_id     TEXT PRIMARY KEY,
                owner_id    TEXT NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
                kind        TEXT NOT NULL CHECK (kind IN ('note', 'bookmark')),
                title       TEXT NOT NULL,
                body        TEXT NOT NULL DEFAULT '',
                url         TEXT,
                visibility  TEXT NOT NULL DEFAULT 'private'
                            CHECK (visibility IN ('private', 'shared')),
                version     INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS shares (
                item_id    TEXT NOT NULL REFERENCES items(item_id) ON DELETE CASCADE,
                grantee_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
                granted_at TEXT NOT NULL,
                revoked_at TEXT,
                PRIMARY KEY (item_id, grantee_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id    TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                issued_at  TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                revoked_at TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS idempotency (
                key           TEXT PRIMARY KEY,
                user_id       TEXT NOT NULL,
                operation     TEXT NOT NULL,
                response_json TEXT NOT NULL,
                created_at    TEXT NOT NULL
            )
            """,
        ],
    ),
    (
        2,
        "index status columns + owner/time index (justified by the P4 measurement)",
        [
            "ALTER TABLE items ADD COLUMN index_status TEXT NOT NULL DEFAULT 'none'",
            "ALTER TABLE items ADD COLUMN index_summary TEXT",
            "CREATE INDEX IF NOT EXISTS idx_items_owner_created ON items(owner_id, created_at)",
        ],
    ),
]

#: Allowed values for ``items.index_status`` (validated in the service layer,
#: because SQLite cannot add a CHECK constraint via ALTER TABLE).
INDEX_STATUSES = ("none", "pending", "ready", "failed")


def _current_version(conn: sqlite3.Connection) -> int:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
    ).fetchone()
    if row is None:
        return 0
    version_row = conn.execute("SELECT version FROM schema_version").fetchone()
    if version_row is None:
        return 0
    return int(version_row[0])


def _set_version(conn: sqlite3.Connection, version: int) -> None:
    conn.execute("DELETE FROM schema_version")
    conn.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))


def apply_migrations(conn: sqlite3.Connection) -> list[int]:
    """Apply every pending migration atomically per step.

    Returns the list of versions that were newly applied. Re-running on an
    up-to-date database is a no-op, which is what makes ``init`` idempotent.
    """
    applied: list[int] = []
    for version, _description, statements in MIGRATIONS:
        if _current_version(conn) >= version:
            continue
        conn.execute("BEGIN IMMEDIATE")
        try:
            for statement in statements:
                conn.execute(statement)
            if version == 1:
                _set_version(conn, 1)
            else:
                _set_version(conn, version)
            conn.execute("COMMIT")
        except sqlite3.Error:
            conn.execute("ROLLBACK")
            raise
        applied.append(version)
    return applied


def schema_version(conn: sqlite3.Connection) -> int:
    """Return the recorded schema version (0 for an uninitialized database)."""
    return _current_version(conn)
