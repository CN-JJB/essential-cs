#!/usr/bin/env python3
"""
crypto_roles.py — Standard-library cryptographic *use* helpers for L21-02.

Required Core uses only hashlib, hmac, and secrets.
Learners do not implement SHA-256, HMAC, AES, RSA, or ECDSA.

Optional PyCA cryptography (Ed25519 sign/verify) is capability-gated.
Absence is NOT RUN / CAPABILITY ABSENT and is not claimed as equivalent Core evidence.

Password-verifier storage/policy is owned by M22/L22-01. This module does not
implement a password hashing schema or freeze a work factor.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Any, Dict, List, Optional


SYNTHETIC_MESSAGE = b"ecs-m21-audit-log-v1:order=42:status=paid"
SYNTHETIC_TAMPERED = b"ecs-m21-audit-log-v1:order=42:status=refunded"


def compute_unkeyed_hash(data: bytes) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like")
    return hashlib.sha256(data).hexdigest()


def verify_unkeyed_tamper(data: bytes, expected_hash: str) -> bool:
    """
    Equality against a caller-supplied digest.

    If the caller also controls the digest (same-channel unkeyed hash), an
    active modifier who replaces both message and digest will pass this check.
    """
    if not isinstance(expected_hash, str):
        raise TypeError("expected_hash must be str")
    return compute_unkeyed_hash(data) == expected_hash


def compute_hmac(key: bytes, data: bytes) -> str:
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes-like")
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like")
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def verify_hmac(key: bytes, data: bytes, expected_mac: str) -> bool:
    """
    HMAC verification using hmac.compare_digest.

    API contract (Python hmac.compare_digest): designed to reduce timing-analysis
    risk by avoiding content-based short-circuiting. Type/length information may
    still theoretically leak. This is not a physical constant-time proof.
    """
    if not isinstance(expected_mac, str):
        raise TypeError("expected_mac must be str")
    computed = compute_hmac(key, data)
    return hmac.compare_digest(computed, expected_mac)


def new_synthetic_mac_key() -> bytes:
    """CSPRNG material for the teaching fixture. Not a real secret."""
    return secrets.token_bytes(32)


def demonstrate_unkeyed_hash_tamper(message: bytes, tampered: bytes) -> Dict[str, Any]:
    original_digest = compute_unkeyed_hash(message)
    recomputed_for_tamper = compute_unkeyed_hash(tampered)
    return {
        "message_id": "SYNTHETIC_MESSAGE",
        "tampered_id": "SYNTHETIC_TAMPERED",
        "original_digest_sha256": original_digest,
        "tampered_recomputed_digest_sha256": recomputed_for_tamper,
        "verify_original_against_original_digest": verify_unkeyed_tamper(message, original_digest),
        "verify_tampered_against_original_digest": verify_unkeyed_tamper(tampered, original_digest),
        "verify_tampered_against_recomputed_digest": verify_unkeyed_tamper(
            tampered, recomputed_for_tamper
        ),
        "inference": (
            "An active modifier who controls both the message and the same-channel "
            "digest can replace both; the unkeyed check then returns True. "
            "An unkeyed hash is not authenticity against that adversary."
        ),
    }


def demonstrate_hmac_tamper(key: bytes, message: bytes, tampered: bytes) -> Dict[str, Any]:
    tag = compute_hmac(key, message)
    forged_tag = compute_hmac(key, tampered)  # attacker without key cannot compute this
    unused_forged = forged_tag  # noqa: F841 — documented contrast only
    return {
        "message_id": "SYNTHETIC_MESSAGE",
        "mac_hex": tag,
        "verify_original": verify_hmac(key, message, tag),
        "verify_modified_message": verify_hmac(key, tampered, tag),
        "verify_modified_tag": verify_hmac(key, message, "00" * 32),
        "compare_digest_api": "hmac.compare_digest",
        "compare_digest_contract": (
            "Designed to avoid content-based short-circuiting; type/length may "
            "still theoretically leak; not a physical constant-time proof."
        ),
        "inference": (
            "Without the shared secret, the modifier cannot produce a verifying "
            "tag. HMAC authenticity is under the shared-secret assumption and "
            "does not identify which key holder produced the tag."
        ),
    }


def primitive_selection_matrix() -> List[Dict[str, str]]:
    """
    Teaching matrix. Rows are scenarios, not runtime PASS claims.
    Non-repudiation is never listed as an unconditional primitive guarantee.
    """
    return [
        {
            "scenario": "Detect accidental bit-rot against a digest published on a trusted channel",
            "required_property": "Integrity detection vs a trusted expected digest",
            "chosen_primitive": "Unkeyed cryptographic hash (SHA-256)",
            "incorrect_tempting_primitive": "Treat the hash as a sender authenticator",
            "non_guarantee": "No authenticity against an active modifier who can recompute the digest",
        },
        {
            "scenario": "Two endpoints sharing a secret need to detect in-path message modification",
            "required_property": "Integrity + authenticity under a shared secret",
            "chosen_primitive": "MAC (HMAC-SHA-256)",
            "incorrect_tempting_primitive": "Unkeyed SHA-256 sent on the same channel",
            "non_guarantee": "Cannot distinguish which of the secret holders produced the tag; not a public-verifiable signature",
        },
        {
            "scenario": "Many independent verifiers must check a log without holding a signing secret",
            "required_property": "Verification under a specific public key",
            "chosen_primitive": "Digital signature (e.g. Ed25519 / FIPS 186-5 algorithms)",
            "incorrect_tempting_primitive": "HMAC with the secret shipped to every verifier",
            "non_guarantee": "Does not by itself prove human identity, key custody, or legal/organizational non-repudiation",
        },
        {
            "scenario": "Confidential application payload on an untrusted hop, with tamper detection",
            "required_property": "Confidentiality + authenticity",
            "chosen_primitive": "AEAD (e.g. AES-GCM per SP 800-38D, or ChaCha20-Poly1305)",
            "incorrect_tempting_primitive": "Un-authenticated CTR/CBC encryption",
            "non_guarantee": "Nonce reuse can be catastrophic; AEAD does not authenticate the peer's identity",
        },
        {
            "scenario": "Establish ephemeral traffic keys between two TLS 1.3 endpoints",
            "required_property": "Key agreement (and, separately, peer authentication)",
            "chosen_primitive": "(EC)DHE key share; peer authentication via certificate/signature or PSK binding",
            "incorrect_tempting_primitive": "Treat key agreement as peer authentication",
            "non_guarantee": "Key agreement does not identify the peer; PSK-only psk_ke is not the same forward-secrecy property as (EC)DHE",
        },
        {
            "scenario": "Store a user password verifier (preview only; owned by M22/L22-01)",
            "required_property": "Slow, salted password verification",
            "chosen_primitive": "Password hashing scheme (compute-hard or memory-hard) — M22",
            "incorrect_tempting_primitive": "Fast unkeyed SHA-256, even if salted",
            "non_guarantee": "M21 does not implement or freeze a password work factor; SHA-256 is not a password verifier",
        },
    ]


def optional_signature_demo(message: bytes) -> Dict[str, Any]:
    """
    Optional Learn-New-Tech path. Required Core must not depend on this package.

    If PyCA cryptography is present, demonstrate Ed25519 sign/verify on synthetic
    bytes. Private keys are generated in memory and never written to disk.
    """
    try:
        import cryptography
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError:
        return {
            "disposition": "NOT RUN / CAPABILITY ABSENT",
            "package": "cryptography",
            "version": None,
            "algorithm": None,
            "verified_under_matching_public_key": None,
            "verified_under_unrelated_public_key": None,
            "inference_limit": (
                "Optional candidate API absent. Required Core (hash/HMAC/compare_digest) "
                "is independent and is not substituted by this path."
            ),
        }

    try:
        version = getattr(cryptography, "__version__", "UNKNOWN")
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        signature = private_key.sign(message)
        matching_ok = False
        try:
            public_key.verify(signature, message)
            matching_ok = True
        except Exception:
            matching_ok = False

        other_pub = Ed25519PrivateKey.generate().public_key()
        unrelated_ok = False
        try:
            other_pub.verify(signature, message)
            unrelated_ok = True
        except Exception:
            unrelated_ok = False

        return {
            "disposition": "OPTIONAL PACKAGE AVAILABLE",
            "package": "cryptography",
            "version": version,
            "algorithm": "Ed25519",
            "verified_under_matching_public_key": matching_ok,
            "verified_under_unrelated_public_key": unrelated_ok,
            "inference_limit": (
                "Proves mathematical verification under a specific public key on synthetic "
                "in-memory material. Does not prove signer identity, key custody, host "
                "integrity, verifier policy, or legal/organizational non-repudiation. "
                "Observed package version is implementation-time currentness, not a "
                "course-wide pin (OQ-BP-006 remains OPEN)."
            ),
        }
    except Exception as exc:
        return {
            "disposition": "BLOCKED / NOT RUN",
            "package": "cryptography",
            "version": getattr(cryptography, "__version__", "UNKNOWN"),
            "algorithm": "Ed25519",
            "verified_under_matching_public_key": None,
            "verified_under_unrelated_public_key": None,
            "error": f"{type(exc).__name__}: {exc}",
            "inference_limit": (
                "Optional package is installed but the Ed25519 capability probe could not "
                "complete in this environment. Required Core remains independent; this "
                "blocked optional route is never converted to PASS."
            ),
        }


def compare_digest_contract_probe() -> Dict[str, Any]:
    """Documented API contract checks; not a timing benchmark."""
    a = "ab" * 32
    b_same = "ab" * 32
    b_diff = "cd" * 32
    same = hmac.compare_digest(a, b_same)
    different = hmac.compare_digest(a, b_diff)
    mixed_type_error: Optional[str] = None
    try:
        hmac.compare_digest(a, b_same.encode("ascii"))  # type: ignore[arg-type]
    except TypeError as exc:
        mixed_type_error = type(exc).__name__
    return {
        "api": "hmac.compare_digest",
        "same_ascii_hex_equal": same,
        "different_ascii_hex_equal": different,
        "mixed_str_bytes_error": mixed_type_error,
        "length_mismatch_equal": hmac.compare_digest(a, a[:-2]),
        "physical_constant_time_claimed": False,
        "contract": (
            "Designed to prevent timing analysis by avoiding content-based "
            "short-circuiting. If a and b differ in length or an error occurs, "
            "a timing attack could theoretically reveal type/length — not values. "
            "CPython 3.10+ may use OpenSSL CRYPTO_memcmp when available. "
            "Hosted software timers are not used as proof."
        ),
    }
