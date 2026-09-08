#!/usr/bin/env python3
"""
labs/foundations/m22/activity_l22_01.py — Authentication, Password Verifiers & Token Validation
=============================================================================================

Course-owned, synthetic educational harness for L22-01: "How do I know who is calling?"
Uses Python standard library only (hashlib, hmac, secrets, base64, json, time).

Demonstrates:
1. Password Verifiers vs Plaintext / Fast Hashes:
   - Salts generated via secrets.token_bytes (>= 32 bits per NIST SP 800-63B-4; default 128 bits);
   - Slow compute-hard KDF (PBKDF2-HMAC-SHA256 per SP 800-132 / RFC 8018);
   - Formatted verifier string (algo$params$salt$hash);
   - Constant-time equality comparison via hmac.compare_digest.
2. TeachingProfile-BearerV1 Token Validation:
   - Educational bearer token profile modeled on standard claims (RFC 7519 / RFC 8725 BCP);
   - Strict rejection of alg: "none" and unapproved algorithms;
   - Cryptographic signature check under configured verifier policy;
   - Required claims: alg, sub, aud, exp, iat;
   - Audience restriction (aud) to prevent token substitution;
   - Temporal expiration (exp) verification.
3. Separation of Authentication (Authn) from Authorization (Authz):
   - Proof of identity != proof of resource authority;
   - Decoupled policy evaluation on (subject, action, resource).

Safety & Invariants:
- Zero real user credentials or live networks;
- Pure standard library, zero external dependencies;
- Educational profile: valid signature != issuer trust != authorization.
"""

from __future__ import annotations

import base64
import dataclasses
import hashlib
import hmac
import json
import secrets
import time
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------------------------------------------------------
# Part 1: Password Verifier Generation & Verification (NIST SP 800-63B-4)
# -----------------------------------------------------------------------------

DEFAULT_PBKDF2_ITERATIONS = 100_000  # Policy parameter; not a timeless constant!
MIN_SALT_BYTES = 4  # 32 bits minimum per NIST SP 800-63B-4
DEFAULT_SALT_BYTES = 16  # 128 bits recommended for collision minimization


def generate_password_verifier(
    password: str,
    iterations: int = DEFAULT_PBKDF2_ITERATIONS,
    salt_bytes: int = DEFAULT_SALT_BYTES,
) -> str:
    """
    Derives a secure password verifier using PBKDF2-HMAC-SHA256.

    Format: pbkdf2_sha256$iterations=<N>$<salt_hex>$<hash_hex>

    Guarantees:
    - Unique per-credential salt (minimizes cross-credential collision and rainbow tables);
    - Tunable iteration work factor (imposes cost on offline brute-force);
    - Salt length >= 32 bits per NIST SP 800-63B-4 §3.1.1.2.
    """
    if salt_bytes < MIN_SALT_BYTES:
        raise ValueError(f"Salt length must be at least {MIN_SALT_BYTES} bytes ({MIN_SALT_BYTES*8} bits)")
    if iterations < 1:
        raise ValueError("Iteration count must be positive")

    salt = secrets.token_bytes(salt_bytes)
    derived = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=iterations,
    )
    salt_hex = salt.hex()
    hash_hex = derived.hex()
    return f"pbkdf2_sha256$iterations={iterations}${salt_hex}${hash_hex}"


def verify_password(password: str, verifier_record: str) -> bool:
    """
    Verifies a candidate password against a stored verifier record.

    Uses hmac.compare_digest to prevent timing-attack side channels.
    Returns True if valid, False otherwise.
    """
    parts = verifier_record.split("$")
    if len(parts) != 4:
        return False

    algo, param_str, salt_hex, expected_hash_hex = parts
    if algo != "pbkdf2_sha256":
        return False

    if not param_str.startswith("iterations="):
        return False

    try:
        iterations = int(param_str.split("=", 1)[1])
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(expected_hash_hex)
    except (ValueError, TypeError):
        return False

    if len(salt) < MIN_SALT_BYTES or iterations < 1:
        return False

    candidate_hash = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=salt,
        iterations=iterations,
    )

    # Constant-time comparison to prevent timing leaks
    return hmac.compare_digest(candidate_hash, expected_hash)


# -----------------------------------------------------------------------------
# Part 2: TeachingProfile-BearerV1 Token Handling (RFC 7519 / RFC 8725 BCP)
# -----------------------------------------------------------------------------

def _b64url_encode(data: bytes) -> str:
    """Encodes bytes to base64url without padding '='."""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(s: str) -> bytes:
    """Decodes base64url string, restoring stripped padding."""
    padding = 4 - (len(s) % 4)
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s.encode("ascii"))


@dataclasses.dataclass(frozen=True)
class TokenValidationResult:
    valid: bool
    subject: Optional[str] = None
    claims: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TeachingTokenAuthority:
    """
    Reference validator and issuer for TeachingProfile-BearerV1 tokens.

    Educational token profile invariants:
    - Fixed approved algorithm list (default ['HS256']);
    - Strictly rejects alg: 'none';
    - Verifies signature using hmac.compare_digest;
    - Enforces mandatory claims: alg, sub, aud, exp, iat;
    - Enforces audience matching to prevent token substitution across services.
    """

    PROFILE_NAME = "TeachingProfile-BearerV1"
    ALLOWED_ALGORITHMS = ("HS256",)

    def __init__(self, signing_secret: bytes, expected_audience: str, issuer_id: str = "teaching-idp.local"):
        if len(signing_secret) < 16:
            raise ValueError("Signing secret must be at least 16 bytes")
        self._secret = signing_secret
        self.expected_audience = expected_audience
        self.issuer_id = issuer_id

    def issue_token(
        self,
        subject: str,
        audience: Optional[str] = None,
        lifetime_seconds: int = 300,
        custom_claims: Optional[Dict[str, Any]] = None,
        override_alg: Optional[str] = None,
    ) -> str:
        """Issues a signed TeachingProfile-BearerV1 token."""
        alg = override_alg or "HS256"
        now = int(time.time())
        header = {
            "alg": alg,
            "typ": "JWT",
            "profile": self.PROFILE_NAME,
        }
        payload: Dict[str, Any] = {
            "sub": subject,
            "aud": audience or self.expected_audience,
            "iss": self.issuer_id,
            "iat": now,
            "exp": now + lifetime_seconds,
        }
        if custom_claims:
            payload.update(custom_claims)

        header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
        payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

        if alg == "none":
            # For testing controlled failure: unsigned token
            sig_b64 = ""
        elif alg == "HS256":
            sig = hmac.new(self._secret, signing_input, hashlib.sha256).digest()
            sig_b64 = _b64url_encode(sig)
        else:
            raise ValueError(f"Unsupported signing algorithm: {alg}")

        return f"{header_b64}.{payload_b64}.{sig_b64}"

    def validate_token(
        self,
        token_str: str,
        current_time: Optional[int] = None,
    ) -> TokenValidationResult:
        """
        Validates a TeachingProfile-BearerV1 token against security invariants.
        """
        parts = token_str.split(".")
        if len(parts) != 3:
            return TokenValidationResult(valid=False, error="Malformed token: must contain exactly 3 dot-separated segments")

        header_b64, payload_b64, sig_b64 = parts

        # 1. Parse header
        try:
            header_bytes = _b64url_decode(header_b64)
            header = json.loads(header_bytes.decode("utf-8"))
        except Exception:
            return TokenValidationResult(valid=False, error="Invalid header encoding or JSON")

        # 2. Enforce algorithm whitelist & reject alg: 'none'
        alg = header.get("alg")
        if alg == "none" or alg is None:
            return TokenValidationResult(valid=False, error="Rejected algorithm: 'none' or missing alg header is forbidden")
        if alg not in self.ALLOWED_ALGORITHMS:
            return TokenValidationResult(valid=False, error=f"Unsupported algorithm '{alg}'; expected one of {self.ALLOWED_ALGORITHMS}")

        # 3. Verify cryptographic signature
        signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
        expected_sig = hmac.new(self._secret, signing_input, hashlib.sha256).digest()
        try:
            actual_sig = _b64url_decode(sig_b64)
        except Exception:
            return TokenValidationResult(valid=False, error="Malformed signature base64url")

        if not hmac.compare_digest(expected_sig, actual_sig):
            return TokenValidationResult(valid=False, error="Cryptographic signature verification failed (tampered token)")

        # 4. Parse payload claims
        try:
            payload_bytes = _b64url_decode(payload_b64)
            payload = json.loads(payload_bytes.decode("utf-8"))
        except Exception:
            return TokenValidationResult(valid=False, error="Invalid payload encoding or JSON")

        # 5. Validate mandatory claims presence
        for claim in ("sub", "aud", "exp", "iat"):
            if claim not in payload:
                return TokenValidationResult(valid=False, error=f"Missing mandatory claim '{claim}'")

        # 6. Validate temporal claim (exp)
        now = current_time if current_time is not None else int(time.time())
        exp = payload["exp"]
        if not isinstance(exp, (int, float)) or now >= exp:
            return TokenValidationResult(valid=False, error=f"Token has expired (exp={exp}, now={now})")

        # 7. Validate audience claim (aud)
        aud = payload["aud"]
        if aud != self.expected_audience:
            return TokenValidationResult(
                valid=False,
                error=f"Audience mismatch: token intended for '{aud}', but service requires '{self.expected_audience}'",
            )

        return TokenValidationResult(valid=True, subject=str(payload["sub"]), claims=payload)


# -----------------------------------------------------------------------------
# Part 3: Authorization Evaluation (Authn != Authz)
# -----------------------------------------------------------------------------

def evaluate_resource_authorization(
    authenticated_subject: str,
    action: str,
    resource: str,
    user_roles: Dict[str, List[str]],
    role_permissions: Dict[str, List[str]],
) -> Tuple[bool, str]:
    """
    Evaluates whether an authenticated identity has permission for action on resource.

    Core Principle:
    Authentication establishes 'who' (authenticated_subject).
    Authorization determines 'what' (permission rule: role has action:resource).

    A valid token proves who is calling; it does NOT prove authority on the resource!
    """
    roles = user_roles.get(authenticated_subject, [])
    if not roles:
        return False, f"Subject '{authenticated_subject}' has no assigned roles"

    target_perm = f"{action}:{resource}"
    wildcard_perm = f"{action}:*"
    admin_perm = "*:*"

    for role in roles:
        perms = role_permissions.get(role, [])
        if target_perm in perms or wildcard_perm in perms or admin_perm in perms:
            return True, f"Authorized via role '{role}' granting '{target_perm}'"

    return False, f"Forbidden: Subject '{authenticated_subject}' lacks permission for '{target_perm}'"


# -----------------------------------------------------------------------------
# Self-Test / CLI Demonstration
# -----------------------------------------------------------------------------

def run_demonstration() -> None:
    print("=" * 78)
    print("  L22-01 DEMONSTRATION: AUTHN, PASSWORD VERIFIERS & TOKEN VALIDATION")
    print("=" * 78)

    # 1. Password verifier
    password = "CorrectHorseBatteryStaple-2026!"
    print(f"\n[1] Creating password verifier for password: '{password}'")
    verifier = generate_password_verifier(password, iterations=50_000)
    print(f"    Stored verifier record: {verifier}")

    assert verify_password(password, verifier) is True
    print("    Verification with correct password: PASS")
    assert verify_password("WrongPassword-123", verifier) is False
    print("    Verification with incorrect password: REJECTED (PASS)")

    # 2. Token Authority
    secret = secrets.token_bytes(32)
    authority = TeachingTokenAuthority(secret, expected_audience="document-service.local")

    print("\n[2] Issuing TeachingProfile-BearerV1 Token for subject 'alice':")
    valid_token = authority.issue_token("alice", lifetime_seconds=60)
    print(f"    Token: {valid_token[:50]}...{valid_token[-20:]}")

    res = authority.validate_token(valid_token)
    print(f"    Validation result: valid={res.valid}, subject={res.subject}")
    assert res.valid is True

    # 3. Tampering failure
    parts = valid_token.split(".")
    tampered_token = f"{parts[0]}.{parts[1]}.{_b64url_encode(b'bad_signature_bytes_1234')}"
    res_tampered = authority.validate_token(tampered_token)
    print(f"    Tampered signature check: valid={res_tampered.valid}, error={res_tampered.error}")
    assert res_tampered.valid is False

    # 4. alg: none rejection
    none_token = authority.issue_token("alice", override_alg="none")
    res_none = authority.validate_token(none_token)
    print(f"    alg: none check: valid={res_none.valid}, error={res_none.error}")
    assert res_none.valid is False

    # 5. Wrong audience rejection (token substitution defense)
    subst_token = authority.issue_token("alice", audience="billing-service.local")
    res_subst = authority.validate_token(subst_token)
    print(f"    Audience mismatch check: valid={res_subst.valid}, error={res_subst.error}")
    assert res_subst.valid is False

    # 6. Authn vs Authz
    user_roles = {"alice": ["reader"], "bob": ["editor"]}
    role_perms = {
        "reader": ["read:doc-101", "read:doc-102"],
        "editor": ["read:*", "write:*"],
    }
    print("\n[3] Evaluating Resource Authorization (Authn != Authz):")
    authz_read, reason_read = evaluate_resource_authorization("alice", "read", "doc-101", user_roles, role_perms)
    print(f"    Alice read doc-101: allowed={authz_read} ({reason_read})")
    assert authz_read is True

    authz_write, reason_write = evaluate_resource_authorization("alice", "write", "doc-101", user_roles, role_perms)
    print(f"    Alice write doc-101: allowed={authz_write} ({reason_write})")
    assert authz_write is False

    print("\n" + "=" * 78)
    print("  L22-01 ACTIVITY CONTRACT VERIFIED.")
    print("=" * 78)


if __name__ == "__main__":
    run_demonstration()
