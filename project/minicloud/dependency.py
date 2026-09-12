"""Caller-side client for the bounded loopback dependency (P3/P9).

The teaching point lives here: a bounded retry policy applies only where the
operation is safe to repeat, and a **timeout is not the same as a definite
failure**. :class:`IndexerClient` therefore raises two different errors:

* :class:`DependencyUnavailableError` — the dependency answered "I am down" or
  refused the connection. Repeating is safe and bounded.
* :class:`DependencyTimeoutError` — the dependency did not answer in time. It
  may still have done the work; the caller must not assume otherwise.

No retry is attempted after a timeout, because retrying an operation whose
outcome is unknown is exactly the mistake the curriculum is teaching against.
"""

from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request

from .errors import DependencyTimeoutError, DependencyUnavailableError


class IndexerClient:
    def __init__(
        self,
        base_url: str,
        *,
        timeout_ms: int = 1500,
        max_attempts: int = 2,
        observability=None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_s = max(timeout_ms, 1) / 1000.0
        self.max_attempts = max(max_attempts, 1)
        self.observability = observability

    def _post(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
            body = response.read().decode("utf-8")
        return json.loads(body) if body else {}

    def index(self, *, url: str, title: str, request_id: str | None = None) -> dict:
        """Index a bookmark with bounded retries. Raises on failure."""
        last_error: Exception | None = None
        attempts = 0
        while attempts < self.max_attempts:
            attempts += 1
            try:
                result = self._post("/index", {"url": url, "title": title})
                if self.observability is not None:
                    self.observability.log(
                        "dependency.index.ok", request_id=request_id, attempts=attempts
                    )
                result["attempts"] = attempts
                return result
            except socket.timeout as exc:
                # Unknown outcome: do NOT retry, and do NOT report "not done".
                if self.observability is not None:
                    self.observability.log(
                        "dependency.index.timeout",
                        request_id=request_id,
                        attempts=attempts,
                        level="warning",
                    )
                raise DependencyTimeoutError(
                    "indexer did not answer before the application deadline",
                    details={"attempts": attempts, "timeout_ms": int(self.timeout_s * 1000)},
                ) from exc
            except urllib.error.HTTPError as exc:
                last_error = exc
                if 500 <= exc.code < 600:
                    if self.observability is not None:
                        self.observability.log(
                            "dependency.index.unavailable",
                            request_id=request_id,
                            attempts=attempts,
                            status=exc.code,
                            level="warning",
                        )
                    continue  # bounded retry: the dependency answered, so retrying is safe
                raise DependencyUnavailableError(
                    f"indexer rejected the request with HTTP {exc.code}"
                ) from exc
            except (urllib.error.URLError, ConnectionError, OSError) as exc:
                last_error = exc
                if self.observability is not None:
                    self.observability.log(
                        "dependency.index.unreachable",
                        request_id=request_id,
                        attempts=attempts,
                        level="warning",
                    )
                continue

        raise DependencyUnavailableError(
            "indexer unavailable after bounded attempts",
            details={"attempts": attempts, "cause": type(last_error).__name__ if last_error else None},
        )
