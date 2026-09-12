"""The transport-independent service core (P0–P9).

This module is the *only* place where domain rules, authorization, transactions,
and dependency policy live. The HTTP adapter and the CLI are thin shells over
it, which is what makes the P1 claim ("the interface is an adapter, not the
implementation") true rather than aspirational.

Authorization rules (P2):

* A user may read an item they own, or an item actively shared with them.
* Only the owner may write, delete, share, revoke, or re-index.
* Anything the effective user is not allowed to see is reported as
  ``not_found`` — never as ``forbidden`` — so denial cannot be used to probe
  whether another user's private item exists.
"""

from __future__ import annotations

import json
import uuid

from . import auth
from .config import MAX_LIST_LIMIT
from .dependency import IndexerClient
from .errors import (
    ConflictError,
    DependencyTimeoutError,
    DependencyUnavailableError,
    NotFoundError,
    UnauthenticatedError,
    ValidationError,
)
from .observability import Observability
from .store import Store, utcnow

KINDS = ("note", "bookmark")
VISIBILITIES = ("private", "shared")
MAX_TITLE = 200
MAX_BODY = 10_000
MAX_URL = 2_000
MAX_USERNAME = 64
MIN_USERNAME = 2


class MiniCloudService:
    def __init__(
        self,
        *,
        store: Store,
        config,
        observability: Observability | None = None,
        dependency: IndexerClient | None = None,
    ) -> None:
        self.store = store
        self.config = config
        self.obs = observability or Observability()
        self.dependency = dependency

    # ------------------------------------------------------------ lifecycle
    def initialize(self) -> list[int]:
        applied = self.store.initialize()
        self.obs.log("service.initialize", applied_versions=applied)
        return applied

    def health(self) -> dict:
        return {
            "status": "ok",
            "service": "minicloud",
            "schema_version": self.store.schema_version(),
            "dependency_configured": self.dependency is not None,
        }

    def metrics_snapshot(self) -> dict:
        return self.obs.snapshot()

    # ---------------------------------------------------------------- users
    def create_user(self, username: str, password: str, *, request_id: str | None = None) -> dict:
        self._validate_username(username)
        auth.validate_password(password)
        salt, pwhash, iterations = auth.hash_password(
            password, iterations=self.config.pbkdf2_iterations
        )
        user_id = uuid.uuid4().hex
        user = self.store.create_user(user_id, username, salt, pwhash, iterations)
        self.obs.log("user.created", request_id=request_id, user_id=user_id, username=username)
        return {"user_id": user["user_id"], "username": user["username"], "created_at": user["created_at"]}

    def login(self, username: str, password: str, *, request_id: str | None = None) -> dict:
        user = self.store.get_user_by_username(username)
        # Verify even when the user is absent, using a dummy verifier, so timing
        # does not trivially reveal account existence.
        if user is None:
            auth.verify_password(password, "00" * 16, "00" * 32, self.config.pbkdf2_iterations)
            raise UnauthenticatedError("invalid credentials")
        if not auth.verify_password(
            password, user["password_salt"], user["password_hash"], user["password_iterations"]
        ):
            self.obs.log("user.login_failed", request_id=request_id, username=username, level="warning")
            raise UnauthenticatedError("invalid credentials")

        token = auth.new_session_token()
        token_hash = auth.hash_token(token)
        expires_at = _expiry_iso(self.config.token_ttl_seconds)
        self.store.create_session(token_hash, user["user_id"], expires_at)
        self.obs.log("user.login_ok", request_id=request_id, user_id=user["user_id"])
        return {
            "token": token,
            "token_type": "Bearer",
            "expires_at": expires_at,
            "user_id": user["user_id"],
            "username": user["username"],
        }

    def logout(self, token: str, *, request_id: str | None = None) -> dict:
        identity = self._require_identity(token)
        revoked = self.store.revoke_session(auth.hash_token(token))
        self.obs.log("user.logout", request_id=request_id, user_id=identity["user_id"])
        return {"revoked": revoked}

    # --------------------------------------------------------------- items
    def create_item(
        self,
        identity: dict,
        *,
        kind: str,
        title: str,
        body: str = "",
        url: str | None = None,
        visibility: str = "private",
        idempotency_key: str | None = None,
        request_id: str | None = None,
    ) -> dict:
        scoped_idempotency_key = None
        if idempotency_key:
            # Client-provided idempotency keys are only meaningful inside an
            # authenticated principal + operation scope. Persisting the raw key
            # globally would let another user replay a cached response.
            scoped_idempotency_key = self._scoped_idempotency_key(
                identity["user_id"], "create_item", idempotency_key
            )
            replay = self._replay(scoped_idempotency_key)
            if replay is not None:
                self.obs.log("item.create.idempotent_replay", request_id=request_id)
                return replay

        kind = self._validate_kind(kind)
        title = self._require_text(title, "title", MAX_TITLE)
        body = self._optional_text(body, "body", MAX_BODY)
        visibility = self._validate_visibility(visibility)
        url = self._validate_url(url, kind)

        index_status = "none"
        index_summary = None
        index_note = None
        if url and self.dependency is not None:
            index_status, index_summary, index_note = self._try_index(
                url=url, title=title, request_id=request_id
            )

        item_id = uuid.uuid4().hex
        if scoped_idempotency_key:
            # The replay decision, item insert and replay-record insert must be
            # one SQLite transaction. A pre-check alone is racy under concurrent
            # duplicate requests.
            now = utcnow()
            candidate = {
                "item_id": item_id,
                "owner_id": identity["user_id"],
                "kind": kind,
                "title": title,
                "body": body,
                "url": url,
                "visibility": visibility,
                "version": 1,
                "created_at": now,
                "updated_at": now,
                "index_status": index_status,
                "index_summary": index_summary,
            }
            view = self._item_view(candidate, viewer_id=identity["user_id"])
            if index_note:
                view["index"]["note"] = index_note
            stored = self.store.insert_item_idempotent(
                item_id=item_id,
                owner_id=identity["user_id"],
                kind=kind,
                title=title,
                body=body,
                url=url,
                visibility=visibility,
                index_status=index_status,
                index_summary=index_summary,
                created_at=now,
                idempotency_key=scoped_idempotency_key,
                operation="create_item",
                response_json=json.dumps(view, sort_keys=True),
            )
            if stored["replayed"]:
                replay = json.loads(stored["response_json"])
                replay["idempotent_replay"] = True
                self.obs.log("item.create.idempotent_replay", request_id=request_id)
                return replay
            self.obs.log("item.created", request_id=request_id, item_id=item_id, kind=kind)
            return view

        item = self.store.insert_item(
            item_id=item_id,
            owner_id=identity["user_id"],
            kind=kind,
            title=title,
            body=body,
            url=url,
            visibility=visibility,
            index_status=index_status,
            index_summary=index_summary,
        )
        view = self._item_view(item, viewer_id=identity["user_id"])
        if index_note:
            view["index"]["note"] = index_note
        self.obs.log("item.created", request_id=request_id, item_id=item["item_id"], kind=kind)
        return view

    def list_items(self, identity: dict, *, limit: int | None = None, request_id: str | None = None) -> dict:
        limit = limit if limit is not None else self.config.default_list_limit
        if not isinstance(limit, int) or limit < 1 or limit > MAX_LIST_LIMIT:
            raise ValidationError(f"limit must be between 1 and {MAX_LIST_LIMIT}")
        rows = self.store.list_items(identity["user_id"], limit=limit)
        items = [self._item_view(r, viewer_id=identity["user_id"]) for r in rows]
        self.obs.log("items.listed", request_id=request_id, count=len(items))
        return {"items": items, "count": len(items), "limit": limit}

    def get_item(self, identity: dict, item_id: str, *, request_id: str | None = None) -> dict:
        item = self._load_visible_item(identity, item_id)
        self.obs.log("item.read", request_id=request_id, item_id=item_id)
        return self._item_view(item, viewer_id=identity["user_id"])

    def update_item(
        self,
        identity: dict,
        item_id: str,
        *,
        expected_version: int,
        fields: dict,
        request_id: str | None = None,
    ) -> dict:
        self._require_owner(identity, item_id)
        if not isinstance(expected_version, int) or expected_version < 1:
            raise ValidationError("expected_version must be a positive integer")

        clean: dict = {}
        if "title" in fields:
            clean["title"] = self._require_text(fields["title"], "title", MAX_TITLE)
        if "body" in fields:
            clean["body"] = self._optional_text(fields["body"], "body", MAX_BODY)
        if "url" in fields:
            clean["url"] = self._validate_url(fields["url"], "bookmark", allow_none=True)
        if "visibility" in fields:
            clean["visibility"] = self._validate_visibility(fields["visibility"])
        if not clean:
            raise ValidationError("no updatable fields supplied")

        updated = self.store.update_item(
            item_id=item_id,
            owner_id=identity["user_id"],
            expected_version=expected_version,
            fields=clean,
        )
        if updated is None:
            current = self.store.require_item(item_id)
            self.obs.log("item.update.conflict", request_id=request_id, item_id=item_id, level="warning")
            raise ConflictError(
                "version conflict: the item changed since it was read",
                details={"expected_version": expected_version, "current_version": current["version"]},
            )
        self.obs.log("item.updated", request_id=request_id, item_id=item_id, version=updated["version"])
        return self._item_view(updated, viewer_id=identity["user_id"])

    def delete_item(self, identity: dict, item_id: str, *, request_id: str | None = None) -> dict:
        self._require_owner(identity, item_id)
        deleted = self.store.delete_item(item_id, identity["user_id"])
        if not deleted:  # pragma: no cover - guarded by _require_owner
            raise NotFoundError("item not found")
        self.obs.log("item.deleted", request_id=request_id, item_id=item_id)
        return {"deleted": True, "item_id": item_id}

    # -------------------------------------------------------------- sharing
    def share_item(
        self, identity: dict, item_id: str, grantee_username: str, *, request_id: str | None = None
    ) -> dict:
        # Preserve the non-enumeration boundary: prove ownership before looking
        # up the named grantee, then re-check ownership inside the write tx.
        self._require_owner(identity, item_id)
        grantee = self.store.get_user_by_username(grantee_username)
        if grantee is None:
            raise ValidationError(f"no such user: {grantee_username}")
        if grantee["user_id"] == identity["user_id"]:
            raise ValidationError("cannot share an item with its owner")
        shares = self.store.share_item_atomic(
            item_id, identity["user_id"], grantee["user_id"], utcnow()
        )
        if shares is None:
            raise NotFoundError("item not found")
        self.obs.log("item.shared", request_id=request_id, item_id=item_id, grantee=grantee_username)
        return {
            "item_id": item_id,
            "grantee": grantee["username"],
            "active": True,
            "shares": shares,
        }

    def revoke_share(
        self, identity: dict, item_id: str, grantee_username: str, *, request_id: str | None = None
    ) -> dict:
        self._require_owner(identity, item_id)
        grantee = self.store.get_user_by_username(grantee_username)
        if grantee is None:
            raise ValidationError(f"no such user: {grantee_username}")
        result = self.store.revoke_share_atomic(
            item_id, identity["user_id"], grantee["user_id"]
        )
        if result is None:
            raise NotFoundError("item not found")
        revoked, remaining = result
        self.obs.log("item.share_revoked", request_id=request_id, item_id=item_id, grantee=grantee_username)
        return {
            "item_id": item_id,
            "grantee": grantee["username"],
            "revoked": revoked,
            "remaining_active_shares": remaining,
        }

    def list_shares(self, identity: dict, item_id: str, *, request_id: str | None = None) -> dict:
        self._require_owner(identity, item_id)
        return {"item_id": item_id, "shares": self.store.list_shares(item_id)}

    # ------------------------------------------------------------- indexing
    def reindex_item(self, identity: dict, item_id: str, *, request_id: str | None = None) -> dict:
        item = self._require_owner(identity, item_id)
        if not item["url"]:
            raise ValidationError("only bookmarks with a URL can be indexed")
        if self.dependency is None:
            raise ValidationError("no indexer dependency is configured")
        status, summary, note = self._try_index(
            url=item["url"], title=item["title"], request_id=request_id
        )
        updated = self.store.update_item(
            item_id=item_id,
            owner_id=identity["user_id"],
            expected_version=item["version"],
            fields={},
            index_status=status,
            index_summary=summary,
        )
        if updated is None:
            raise ConflictError("version conflict while recording index result")
        view = self._item_view(updated, viewer_id=identity["user_id"])
        if note:
            view["index"]["note"] = note
        return view

    # ---------------------------------------------------------------- auth
    def authenticate(self, token: str | None) -> dict:
        return self._require_identity(token)

    def _require_identity(self, token: str | None) -> dict:
        if not token:
            raise UnauthenticatedError("missing bearer token")
        session = self.store.get_session(auth.hash_token(token))
        if session is None:
            raise UnauthenticatedError("unknown or revoked session")
        if session["revoked_at"] is not None:
            raise UnauthenticatedError("session revoked")
        if session["expires_at"] < utcnow():
            raise UnauthenticatedError("session expired")
        user = self.store.get_user_by_id(session["user_id"])
        if user is None:  # pragma: no cover - FK guarantees this
            raise UnauthenticatedError("session user no longer exists")
        return {"user_id": user["user_id"], "username": user["username"]}

    # -------------------------------------------------------------- helpers
    def _load_visible_item(self, identity: dict, item_id: str) -> dict:
        item = self.store.get_item(item_id)
        if item is None:
            raise NotFoundError("item not found")
        if item["owner_id"] == identity["user_id"]:
            return item
        if self.store.active_share(item_id, identity["user_id"]) is not None:
            return item
        # Deliberately indistinguishable from "does not exist": the message is a
        # constant and does not echo the requested identifier, so the denial
        # cannot be used to probe which identifiers exist.
        raise NotFoundError("item not found")

    def _require_owner(self, identity: dict, item_id: str) -> dict:
        item = self.store.get_item(item_id)
        if item is None or item["owner_id"] != identity["user_id"]:
            raise NotFoundError("item not found")
        return item

    def _try_index(self, *, url: str, title: str, request_id: str | None) -> tuple[str, str | None, str | None]:
        """Return ``(status, summary, note)``; never raise for dependency faults.

        The item is durable regardless. A dependency fault only changes the
        *index* state and is reported honestly to the caller (P3/P9).
        """
        assert self.dependency is not None
        try:
            result = self.dependency.index(url=url, title=title, request_id=request_id)
            return "ready", str(result.get("summary") or ""), None
        except DependencyTimeoutError as exc:
            return "pending", None, f"dependency_timeout: {exc.message}"
        except DependencyUnavailableError as exc:
            return "pending", None, f"dependency_unavailable: {exc.message}"

    @staticmethod
    def _scoped_idempotency_key(user_id: str, operation: str, key: str) -> str:
        """Namespace an opaque client key by principal and operation.

        JSON encoding keeps the tuple unambiguous without changing the schema.
        The stored key is an implementation detail; callers still send their
        original opaque Idempotency-Key value.
        """
        return json.dumps([user_id, operation, key], separators=(",", ":"), ensure_ascii=False)

    def _replay(self, key: str) -> dict | None:
        record = self.store.get_idempotent(key)
        if record is None:
            return None
        view = json.loads(record["response_json"])
        view["idempotent_replay"] = True
        return view

    def _item_view(self, item: dict, *, viewer_id: str) -> dict:
        is_owner = item["owner_id"] == viewer_id
        view = {
            "item_id": item["item_id"],
            "owner_id": item["owner_id"],
            "kind": item["kind"],
            "title": item["title"],
            "body": item["body"],
            "url": item["url"],
            "visibility": item["visibility"],
            "version": item["version"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "index": {"status": item.get("index_status", "none"), "summary": item.get("index_summary")},
            "is_owner": is_owner,
        }
        if is_owner:
            view["shared_with"] = [
                s["username"] for s in self.store.list_shares(item["item_id"]) if s["revoked_at"] is None
            ]
        return view

    # ---------------------------------------------------------- validation
    @staticmethod
    def _validate_username(username: str) -> None:
        if not isinstance(username, str):
            raise ValidationError("username must be a string")
        if not (MIN_USERNAME <= len(username) <= MAX_USERNAME):
            raise ValidationError(
                f"username must be {MIN_USERNAME}..{MAX_USERNAME} characters"
            )
        if not all(c.isalnum() or c in "-_" for c in username):
            raise ValidationError("username may contain only letters, digits, '-' and '_'")

    @staticmethod
    def _validate_kind(kind: str) -> str:
        if kind not in KINDS:
            raise ValidationError(f"kind must be one of {KINDS}")
        return kind

    @staticmethod
    def _validate_visibility(visibility: str) -> str:
        if visibility not in VISIBILITIES:
            raise ValidationError(f"visibility must be one of {VISIBILITIES}")
        return visibility

    @staticmethod
    def _require_text(value, name: str, max_len: int) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{name} must be a non-empty string")
        if len(value) > max_len:
            raise ValidationError(f"{name} must be at most {max_len} characters")
        return value

    @staticmethod
    def _optional_text(value, name: str, max_len: int) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            raise ValidationError(f"{name} must be a string")
        if len(value) > max_len:
            raise ValidationError(f"{name} must be at most {max_len} characters")
        return value

    @staticmethod
    def _validate_url(url, kind: str, allow_none: bool = False) -> str | None:
        if url is None or url == "":
            if kind == "bookmark" and not allow_none:
                raise ValidationError("a bookmark requires a url")
            return None
        if not isinstance(url, str):
            raise ValidationError("url must be a string")
        if len(url) > MAX_URL:
            raise ValidationError(f"url must be at most {MAX_URL} characters")
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValidationError("url must start with http:// or https://")
        return url


def _expiry_iso(ttl_seconds: int) -> str:
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )
