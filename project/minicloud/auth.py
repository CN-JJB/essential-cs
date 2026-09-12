"""Credential primitives (P2).

Two rules this module exists to enforce:

1. **Never store a plaintext password.** Passwords are stored only as a
   PBKDF2-HMAC-SHA256 verifier with a per-user random salt.
2. **Never store a raw session token.** Only the SHA-256 of a token is
   persisted, so a database read does not yield a usable credential.

Comparison always uses :func:`hmac.compare_digest` so verification time does
not depend on how many leading bytes matched.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

#: Bounded password policy. Length is checked here, not in the adapter, so the
#: CLI and HTTP paths cannot diverge.
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 256


def validate_password(password: str) -> None:
    from .errors import ValidationError

    if not isinstance(password, str) or len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"password must be a string of at least {MIN_PASSWORD_LENGTH} characters"
        )
    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValidationError(f"password must be at most {MAX_PASSWORD_LENGTH} characters")


def hash_password(password: str, *, iterations: int, salt: bytes | None = None) -> tuple[str, str, int]:
    """Return ``(salt_hex, hash_hex, iterations)`` for storage."""
    if salt is None:
        salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return salt.hex(), digest.hex(), iterations


def verify_password(password: str, salt_hex: str, hash_hex: str, iterations: int) -> bool:
    """Constant-time verification of a stored verifier."""
    try:
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
    except ValueError:
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate, expected)


def new_session_token() -> str:
    """Generate an opaque, high-entropy session token (never stored raw)."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Deterministic lookup hash for a session token."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def constant_time_equals(left: str, right: str) -> bool:
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))
