"""Configuration and secret separation (P7).

All tunables come from the environment with safe, deterministic defaults so a
fresh clone runs without any hidden setup. There are **no committed secrets**:
passwords are supplied by the caller, session tokens are generated at runtime,
and the database path defaults to a course-owned, gitignored location.

Keeping configuration in one place makes the P7 "configuration vs durable
state" boundary inspectable: the same code runs unchanged, only the injected
environment differs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from .errors import ConfigurationError

#: Bounded request body limit. Untrusted input is rejected before it can
#: consume unbounded memory (P1/P2).
DEFAULT_MAX_BODY_BYTES = 64 * 1024

#: Bounded page size for list operations.
DEFAULT_LIST_LIMIT = 50
MAX_LIST_LIMIT = 500

#: Environment floors this project actually depends on (D-032 canonical image).
MIN_PYTHON = (3, 12)
MIN_SQLITE = (3, 45)


def environment_report() -> dict:
    """Report the capability floors the Mini Cloud genuinely requires (P7)."""
    import sqlite3
    import sys

    sqlite_version = sqlite3.sqlite_version
    try:
        sqlite_tuple = tuple(int(part) for part in sqlite_version.split(".")[:2])
    except ValueError:
        sqlite_tuple = (0, 0)
    return {
        "python_version": sys.version.split()[0],
        "python_ok": sys.version_info[:2] >= MIN_PYTHON,
        "python_floor": ".".join(str(p) for p in MIN_PYTHON),
        "sqlite_version": sqlite_version,
        "sqlite_ok": sqlite_tuple >= MIN_SQLITE,
        "sqlite_floor": ".".join(str(p) for p in MIN_SQLITE),
    }


def _get_int(env: dict, name: str, default: int) -> int:
    raw = env.get(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer, got {raw!r}") from exc
    return value


def _get_str(env: dict, name: str, default: str | None) -> str | None:
    raw = env.get(name)
    if raw is None or raw == "":
        return default
    return raw


@dataclass(frozen=True)
class Config:
    """Immutable, validated runtime configuration."""

    db_path: str
    host: str
    port: int
    indexer_url: str | None
    token_ttl_seconds: int
    pbkdf2_iterations: int
    log_path: str | None
    metrics_path: str | None
    dep_timeout_ms: int
    dep_max_attempts: int
    max_body_bytes: int
    default_list_limit: int

    @classmethod
    def from_env(cls, env: dict | None = None) -> "Config":
        env = dict(os.environ) if env is None else dict(env)

        db_path = _get_str(env, "MINICLOUD_DB_PATH", "project/var/minicloud.db")
        assert db_path is not None

        port = _get_int(env, "MINICLOUD_PORT", 0)  # 0 => OS-assigned ephemeral
        if port < 0 or port > 65535:
            raise ConfigurationError(f"MINICLOUD_PORT out of range: {port}")

        iterations = _get_int(env, "MINICLOUD_PBKDF2_ITERATIONS", 200_000)
        if iterations < 10_000:
            raise ConfigurationError(
                "MINICLOUD_PBKDF2_ITERATIONS below the 10000 floor is not acceptable"
            )

        token_ttl = _get_int(env, "MINICLOUD_TOKEN_TTL_SECONDS", 3600)
        if token_ttl <= 0:
            raise ConfigurationError("MINICLOUD_TOKEN_TTL_SECONDS must be positive")

        dep_timeout = _get_int(env, "MINICLOUD_DEP_TIMEOUT_MS", 1500)
        if dep_timeout <= 0:
            raise ConfigurationError("MINICLOUD_DEP_TIMEOUT_MS must be positive")

        dep_attempts = _get_int(env, "MINICLOUD_DEP_MAX_ATTEMPTS", 2)
        if dep_attempts < 1:
            raise ConfigurationError("MINICLOUD_DEP_MAX_ATTEMPTS must be >= 1")

        max_body = _get_int(env, "MINICLOUD_MAX_BODY_BYTES", DEFAULT_MAX_BODY_BYTES)
        if max_body < 1024:
            raise ConfigurationError("MINICLOUD_MAX_BODY_BYTES must be >= 1024")

        list_limit = _get_int(env, "MINICLOUD_LIST_LIMIT", DEFAULT_LIST_LIMIT)
        if list_limit < 1 or list_limit > MAX_LIST_LIMIT:
            raise ConfigurationError(
                f"MINICLOUD_LIST_LIMIT must be between 1 and {MAX_LIST_LIMIT}"
            )

        return cls(
            db_path=db_path,
            host=_get_str(env, "MINICLOUD_HOST", "127.0.0.1") or "127.0.0.1",
            port=port,
            indexer_url=_get_str(env, "MINICLOUD_INDEXER_URL", None),
            token_ttl_seconds=token_ttl,
            pbkdf2_iterations=iterations,
            log_path=_get_str(env, "MINICLOUD_LOG_PATH", None),
            metrics_path=_get_str(env, "MINICLOUD_METRICS_PATH", None),
            dep_timeout_ms=dep_timeout,
            dep_max_attempts=dep_attempts,
            max_body_bytes=max_body,
            default_list_limit=list_limit,
        )
