"""HTTP client with explicit timeout / retry / ambiguity semantics (P3).

This is where the P3 lesson is made concrete and testable:

* ``connect`` and ``read`` share one explicit deadline — no silent infinite
  wait.
* A **safe** operation (GET) may be retried on a connection failure, because
  repeating it cannot change state.
* A **mutation** may only be retried when the caller supplied an
  ``Idempotency-Key``; otherwise a retry could duplicate the effect.
* A **timeout on a mutation is reported as ambiguous**, never as "failed".
  ``Outcome.ambiguous`` is the machine-readable form of "we do not know whether
  this committed".
"""

from __future__ import annotations

import http.client
import json
import socket
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from .errors import ValidationError


@dataclass
class Outcome:
    status: int | None
    body: dict | None
    attempts: int
    ambiguous: bool = False
    error: str | None = None
    request_id: str | None = None
    headers: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300

    def raise_for_status(self) -> "Outcome":
        if self.ambiguous:
            raise RuntimeError("ambiguous outcome: the request may or may not have committed")
        if not self.ok:
            raise RuntimeError(f"HTTP {self.status}: {self.body}")
        return self


class MiniCloudClient:
    def __init__(
        self,
        base_url: str,
        *,
        timeout_ms: int = 1500,
        max_attempts: int = 2,
        observability=None,
    ) -> None:
        parts = urlsplit(base_url)
        if parts.scheme != "http":
            raise ValidationError("MiniCloudClient supports http:// base URLs only (local teaching boundary)")
        self.host = parts.hostname or "127.0.0.1"
        self.port = parts.port or 80
        self.base_url = base_url.rstrip("/")
        self.timeout_s = max(timeout_ms, 1) / 1000.0
        self.max_attempts = max(max_attempts, 1)
        self.obs = observability

    # ------------------------------------------------------------------ raw
    def request(
        self,
        method: str,
        path: str,
        *,
        body: dict | None = None,
        token: str | None = None,
        idempotency_key: str | None = None,
        safe: bool = False,
        request_id: str | None = None,
    ) -> Outcome:
        retryable = safe or bool(idempotency_key)
        attempts = 0
        last_error: str | None = None

        while attempts < (self.max_attempts if retryable else 1):
            attempts += 1
            headers = {"Accept": "application/json"}
            if request_id:
                headers["X-Request-ID"] = request_id
            if token:
                headers["Authorization"] = f"Bearer {token}"
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key
            payload = None
            if body is not None:
                payload = json.dumps(body).encode("utf-8")
                headers["Content-Type"] = "application/json"

            conn = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout_s)
            try:
                conn.request(method, path, body=payload, headers=headers)
                response = conn.getresponse()
                raw = response.read()
                parsed = json.loads(raw.decode("utf-8")) if raw else None
                return Outcome(
                    status=response.status,
                    body=parsed,
                    attempts=attempts,
                    request_id=response.getheader("X-Request-ID") or request_id,
                )
            except socket.timeout:
                # Do not retry: the remote may have completed the work.
                if self.obs is not None:
                    self.obs.log("client.timeout", request_id=request_id, path=path, attempts=attempts, level="warning")
                return Outcome(
                    status=None,
                    body=None,
                    attempts=attempts,
                    ambiguous=True,
                    error="timeout",
                    request_id=request_id,
                )
            except (ConnectionRefusedError, ConnectionResetError, http.client.HTTPException, OSError) as exc:
                last_error = type(exc).__name__
                if self.obs is not None:
                    self.obs.log("client.connection_error", request_id=request_id, path=path, attempts=attempts, error=last_error, level="warning")
                continue
            finally:
                conn.close()

        return Outcome(
            status=None,
            body=None,
            attempts=attempts,
            ambiguous=False,
            error=last_error or "unreachable",
            request_id=request_id,
        )

    # -------------------------------------------------------- convenience
    def health(self) -> Outcome:
        return self.request("GET", "/health", safe=True)

    def create_user(self, username: str, password: str) -> Outcome:
        return self.request("POST", "/v1/users", body={"username": username, "password": password})

    def login(self, username: str, password: str) -> Outcome:
        return self.request("POST", "/v1/sessions", body={"username": username, "password": password})

    def logout(self, token: str) -> Outcome:
        return self.request("DELETE", "/v1/sessions", token=token)

    def create_item(self, token: str, **fields) -> Outcome:
        idem = fields.pop("idempotency_key", None)
        return self.request(
            "POST", "/v1/items", body=fields, token=token, idempotency_key=idem
        )

    def list_items(self, token: str, *, limit: int | None = None) -> Outcome:
        body = {"limit": limit} if limit is not None else None
        return self.request("GET", "/v1/items", body=body, token=token, safe=True)

    def get_item(self, token: str, item_id: str) -> Outcome:
        return self.request("GET", f"/v1/items/{item_id}", token=token, safe=True)

    def update_item(self, token: str, item_id: str, *, expected_version: int, **fields) -> Outcome:
        payload = dict(fields)
        payload["expected_version"] = expected_version
        return self.request("PATCH", f"/v1/items/{item_id}", body=payload, token=token)

    def delete_item(self, token: str, item_id: str) -> Outcome:
        return self.request("DELETE", f"/v1/items/{item_id}", token=token)

    def share_item(self, token: str, item_id: str, grantee: str) -> Outcome:
        return self.request("POST", f"/v1/items/{item_id}/shares", body={"grantee": grantee}, token=token)

    def revoke_share(self, token: str, item_id: str, grantee: str) -> Outcome:
        return self.request("DELETE", f"/v1/items/{item_id}/shares/{grantee}", token=token)

    def reindex_item(self, token: str, item_id: str) -> Outcome:
        return self.request("POST", f"/v1/items/{item_id}/reindex", body={}, token=token)
