"""Typed error taxonomy for the Mini Cloud service boundary (P1/P2).

Every error carries a stable machine ``code`` and an HTTP status so the same
taxonomy is usable from the CLI, the in-process service, and the HTTP adapter
without duplicating mapping logic.

Security note (P2): :class:`NotFoundError` is returned both for a genuinely
missing resource *and* for a resource the effective user is not authorized to
see. That is intentional — the boundary must not disclose whether another
user's private item exists.
"""

from __future__ import annotations


class MiniCloudError(Exception):
    """Base class for all Mini Cloud boundary errors."""

    code = "internal_error"
    http_status = 500

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_payload(self, request_id: str | None = None) -> dict:
        error: dict = {"code": self.code, "message": self.message}
        if self.details:
            error["details"] = self.details
        if request_id:
            error["request_id"] = request_id
        return {"error": error}


class ValidationError(MiniCloudError):
    """Malformed, missing, or out-of-range external input (P1/P2)."""

    code = "validation_error"
    http_status = 400


class PayloadTooLargeError(MiniCloudError):
    """Declared or actual body exceeded the bounded request limit (P1)."""

    code = "payload_too_large"
    http_status = 413


class UnauthenticatedError(MiniCloudError):
    """Missing, expired, revoked, or invalid credential (P2)."""

    code = "unauthenticated"
    http_status = 401


class NotFoundError(MiniCloudError):
    """Resource absent *or* not visible to the effective user (P2 no-leak)."""

    code = "not_found"
    http_status = 404


class ConflictError(MiniCloudError):
    """A concurrent write lost the optimistic version check (P5)."""

    code = "conflict"
    http_status = 409


class DependencyUnavailableError(MiniCloudError):
    """A bounded downstream dependency could not be reached (P3/P6/P9)."""

    code = "dependency_unavailable"
    http_status = 503


class DependencyTimeoutError(MiniCloudError):
    """A downstream dependency exceeded the application deadline (P3/P9).

    This is deliberately distinct from :class:`DependencyUnavailableError`:
    a timeout does **not** prove the remote side did nothing.
    """

    code = "dependency_timeout"
    http_status = 504


class StorageError(MiniCloudError):
    """The durable store is missing, corrupt, or not writable (P6)."""

    code = "storage_error"
    http_status = 500


class ConfigurationError(MiniCloudError):
    """Configuration is missing or invalid; fail closed, do not guess (P7)."""

    code = "configuration_error"
    http_status = 500
