#!/usr/bin/env python3
"""
test_m22.py — Standard Library Unit Test Suite for Foundations Module M22
========================================================================

Verifies:
1. L22-01 Authentication, Password Verifiers & Token Validation (activity_l22_01.py)
   - Password verifier generation with independently generated salt (>= 32 bits; chosen to minimize collisions)
   - PBKDF2-HMAC-SHA256 verifier formatting and compare_digest timing-analysis mitigation
   - Rejection of incorrect passwords without data leakage
   - TeachingProfile-BearerV1 token validation (alg whitelist, reject alg: none)
   - Tampered HS256 HMAC authentication-tag detection
   - Temporal expiration (exp) and audience restriction (aud) enforcement
   - Decoupled authentication from resource authorization (Authn != Authz)
2. L22-02 Web Security, SQL Parameterization & SSRF Egress (activity_l22_02.py)
   - SQL string concatenation vulnerability (data syntax mutation)
   - Structural parameterized value binding (? placeholder; bounded to value positions)
   - SSRF destination policy (rejection of RFC 1918, link-local metadata 169.254.x.x, loopback)
   - Bounded direct-socket path avoids a second hostname lookup after address validation
   - CSRF defenses: SameSite cookies, Origin validation, anti-CSRF synchronizer tokens
   - Managed server lifecycle and fail-closed teardown
3. L22-03 Software Supply Chain 9-Layer Model (activity_l22_03.py)
   - Layer 1 Version Pinning and Layer 2 Expected Digest Ownership
   - Layer 3 Fetched-Byte Integrity (SHA-256 matching and tamper detection)
   - Layer 4 Build Reproducibility (independent build artifact comparison)
   - Layer 5 & 6 conceptual signature/identity separation; Core uses a labeled HMAC stand-in
   - Layer 7 & 8 synthetic provenance metadata and builder-policy validation
   - Layer 9 Verifier Policy Enforcement (comprehensive pipeline judgment)
4. M22 Fail-Closed, Idempotent Reset (reset.py)
"""

from __future__ import annotations

import json
import os
import secrets
import sys
import unittest
import urllib.error
import urllib.request
from pathlib import Path

# Ensure labs/foundations/m22 is in sys.path for direct or test-runner execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

import activity_l22_01
import activity_l22_02
import activity_l22_03
import reset


class TestL22_01_AuthnAndTokens(unittest.TestCase):
    """Unit tests for L22-01 authn, password verifiers, and bearer tokens."""

    def test_password_verifier_generation_and_verification(self) -> None:
        password = "SyntheticLearnerPassword-2026!"
        verifier = activity_l22_01.generate_password_verifier(password, iterations=10_000, salt_bytes=16)

        # Assert format: pbkdf2_sha256$iterations=10000$<salt_hex>$<hash_hex>
        parts = verifier.split("$")
        self.assertEqual(len(parts), 4)
        self.assertEqual(parts[0], "pbkdf2_sha256")
        self.assertEqual(parts[1], "iterations=10000")
        self.assertEqual(len(bytes.fromhex(parts[2])), 16)  # 16 bytes = 128 bits >= 32 bits
        self.assertEqual(len(bytes.fromhex(parts[3])), 32)  # SHA-256 output = 32 bytes

        # Correct password succeeds
        self.assertTrue(activity_l22_01.verify_password(password, verifier))
        # Wrong password fails
        self.assertFalse(activity_l22_01.verify_password("WrongPassword!", verifier))
        # Corrupted verifier record fails
        self.assertFalse(activity_l22_01.verify_password(password, "corrupted_record"))

    def test_password_verifier_independent_salts_in_fixture(self) -> None:
        password = "IdenticalPasswordUsedTwice"
        v1 = activity_l22_01.generate_password_verifier(password, iterations=1000)
        v2 = activity_l22_01.generate_password_verifier(password, iterations=1000)
        # Two independent fixture draws should differ; this is not a mathematical uniqueness proof.
        self.assertNotEqual(v1.split("$")[2], v2.split("$")[2])
        # Derived hash must be different due to distinct salts
        self.assertNotEqual(v1.split("$")[3], v2.split("$")[3])

    def test_token_authority_valid_flow(self) -> None:
        secret = secrets.token_bytes(32)
        authority = activity_l22_01.TeachingTokenAuthority(secret, expected_audience="api.local")
        token = authority.issue_token(subject="alice", lifetime_seconds=120)

        result = authority.validate_token(token)
        self.assertTrue(result.valid)
        self.assertEqual(result.subject, "alice")
        self.assertIsNone(result.error)
        self.assertIsNotNone(result.claims)
        self.assertEqual(result.claims["aud"], "api.local")

    def test_token_authority_tampered_hmac_tag_rejection(self) -> None:
        secret = secrets.token_bytes(32)
        authority = activity_l22_01.TeachingTokenAuthority(secret, expected_audience="api.local")
        token = authority.issue_token(subject="alice", lifetime_seconds=120)

        parts = token.split(".")
        # Tamper payload
        tampered_token = f"{parts[0]}.{activity_l22_01._b64url_encode(b'{\"sub\":\"admin\"}')}.{parts[2]}"
        result = authority.validate_token(tampered_token)
        self.assertFalse(result.valid)
        self.assertIn("authentication-tag verification failed", result.error or "")

    def test_token_authority_rejects_alg_none(self) -> None:
        secret = secrets.token_bytes(32)
        authority = activity_l22_01.TeachingTokenAuthority(secret, expected_audience="api.local")
        token_none = authority.issue_token(subject="alice", override_alg="none")

        result = authority.validate_token(token_none)
        self.assertFalse(result.valid)
        self.assertIn("none", result.error or "")

    def test_token_authority_rejects_expired(self) -> None:
        secret = secrets.token_bytes(32)
        authority = activity_l22_01.TeachingTokenAuthority(secret, expected_audience="api.local")
        # Issued with negative lifetime -> already expired
        token = authority.issue_token(subject="alice", lifetime_seconds=-10)

        result = authority.validate_token(token)
        self.assertFalse(result.valid)
        self.assertIn("expired", result.error or "")

    def test_token_authority_rejects_audience_mismatch(self) -> None:
        secret = secrets.token_bytes(32)
        authority = activity_l22_01.TeachingTokenAuthority(secret, expected_audience="api.local")
        token_other_aud = authority.issue_token(subject="alice", audience="billing.local")

        result = authority.validate_token(token_other_aud)
        self.assertFalse(result.valid)
        self.assertIn("Audience mismatch", result.error or "")

    def test_token_authority_rejects_issuer_mismatch(self) -> None:
        secret = secrets.token_bytes(32)
        authority = activity_l22_01.TeachingTokenAuthority(
            secret,
            expected_audience="api.local",
            issuer_id="trusted-idp.local",
        )
        token_wrong_issuer = authority.issue_token(
            subject="alice",
            custom_claims={"iss": "untrusted-idp.local"},
        )

        result = authority.validate_token(token_wrong_issuer)
        self.assertFalse(result.valid)
        self.assertIn("Issuer mismatch", result.error or "")

    def test_authn_separated_from_authz(self) -> None:
        user_roles = {"alice": ["analyst"], "bob": ["admin"]}
        role_permissions = {
            "analyst": ["read:reports", "read:metrics"],
            "admin": ["read:*", "write:*", "delete:*"],
        }
        # Alice authenticated, but lacks write permission
        can_read, msg_read = activity_l22_01.evaluate_resource_authorization(
            "alice", "read", "reports", user_roles, role_permissions
        )
        self.assertTrue(can_read)

        can_write, msg_write = activity_l22_01.evaluate_resource_authorization(
            "alice", "write", "reports", user_roles, role_permissions
        )
        self.assertFalse(can_write)
        self.assertIn("Forbidden", msg_write)


class TestL22_02_WebSecurity(unittest.TestCase):
    """Unit tests for L22-02 web security, SQL injection, CSRF, and SSRF."""

    def setUp(self) -> None:
        self.db = activity_l22_02.setup_synthetic_database()

    def tearDown(self) -> None:
        self.db.close()

    def test_sql_injection_vs_parameterization(self) -> None:
        payload = "admin' OR '1'='1"

        # Unsafe concatenation: alters query AST, leaks all user records
        leaked = activity_l22_02.query_user_unsafe(self.db, payload)
        self.assertGreater(len(leaked), 1, "Unsafe query should leak all records on boolean tautology")

        # Safe parameterization: driver binds payload strictly as string literal
        safe = activity_l22_02.query_user_safe(self.db, payload)
        self.assertEqual(len(safe), 0, "Parameterized query must return 0 records for injection payload")

        # Legitimate lookup works
        alice_data = activity_l22_02.query_user_safe(self.db, "alice")
        self.assertEqual(len(alice_data), 1)
        self.assertEqual(alice_data[0][1], "alice")

    def test_ssrf_disallowed_ip_filters(self) -> None:
        # Loopback
        disallowed, _ = activity_l22_02.is_ip_disallowed("127.0.0.1", allow_loopback_for_testing=False)
        self.assertTrue(disallowed)

        # RFC 1918 Private
        for ip in ("10.0.0.1", "172.16.5.20", "192.168.1.1"):
            disallowed, _ = activity_l22_02.is_ip_disallowed(ip)
            self.assertTrue(disallowed, f"Private IP {ip} must be disallowed")

        # Cloud Metadata (RFC 3927 Link-Local)
        disallowed, _ = activity_l22_02.is_ip_disallowed("169.254.169.254")
        self.assertTrue(disallowed, "Metadata IP 169.254.169.254 must be disallowed")

        # Multicast
        disallowed, _ = activity_l22_02.is_ip_disallowed("224.0.0.1")
        self.assertTrue(disallowed, "Multicast IP must be disallowed")

    def test_safe_fetch_contract_rejects_https_and_loopback_by_default(self) -> None:
        ok_https, status_https, _ = activity_l22_02.safe_http_fetch_over_socket(
            "https://127.0.0.1:443/synthetic"
        )
        self.assertFalse(ok_https)
        self.assertEqual(status_https, 403)

        ok_loop, status_loop, _ = activity_l22_02.safe_http_fetch_over_socket(
            "http://127.0.0.1:9/synthetic"
        )
        self.assertFalse(ok_loop)
        self.assertEqual(status_loop, 403)

    def test_server_lifecycle_and_csrf_defenses(self) -> None:
        server = activity_l22_02.SafeLocalhostServer()
        server.start()
        self.assertGreater(server.port, 0)
        self.assertTrue(server.origin.startswith("http://127.0.0.1:"))

        try:
            # 1. Login to obtain session cookie and anti-CSRF token
            login_req = urllib.request.Request(
                f"{server.origin}/login",
                data=json.dumps({"username": "alice"}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(login_req) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                csrf_token = data["csrf_token"]
                cookie = resp.headers.get("Set-Cookie")

            self.assertTrue(csrf_token)
            self.assertIn("SameSite=Lax", cookie or "")

            # 2. Malicious Cross-Origin request without CSRF token -> Rejected 403
            bad_req = urllib.request.Request(
                f"{server.origin}/update_email",
                data=json.dumps({"email": "hacked@evil.local"}).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Cookie": cookie,
                    "Origin": "http://malicious-site.local",
                },
            )
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(bad_req)
            self.assertEqual(ctx.exception.code, 403)

            # 3. Prefix-shaped Origin must NOT pass an exact-origin policy.
            prefix_origin_req = urllib.request.Request(
                f"{server.origin}/update_email",
                data=json.dumps({"email": "prefix_attack@example.local", "csrf_token": csrf_token}).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Cookie": cookie,
                    "Origin": server.origin + ".evil.example",
                    "X-CSRF-Token": csrf_token,
                },
            )
            with self.assertRaises(urllib.error.HTTPError) as prefix_ctx:
                urllib.request.urlopen(prefix_origin_req)
            self.assertEqual(prefix_ctx.exception.code, 403)

            # 4. Legitimate request with matching Origin and CSRF token -> Accepted 200
            good_req = urllib.request.Request(
                f"{server.origin}/update_email",
                data=json.dumps({"email": "alice_updated@example.local", "csrf_token": csrf_token}).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Cookie": cookie,
                    "Origin": server.origin,
                    "X-CSRF-Token": csrf_token,
                },
            )
            with urllib.request.urlopen(good_req) as resp:
                self.assertEqual(resp.status, 200)
                res_data = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(res_data["status"], "email_updated")

        finally:
            server.stop()


class TestL22_03_SoftwareSupplyChain(unittest.TestCase):
    """Unit tests for L22-03 software supply chain 9-layer integrity model."""

    def setUp(self) -> None:
        self.signing_secret = b"test-maintainer-key-32-bytes!!"
        self.key_id = "synthetic-maintainer-shared-key-alice-2026"
        self.policy = activity_l22_03.VerifierPolicy()

        self.code = b"def core_func(): return 42\n"
        self.artifact = activity_l22_03.SyntheticArtifact("trusted-lib", "2.1.0", self.code)
        self.entry = activity_l22_03.LockfileEntry(
            "trusted-lib", "2.1.0", self.artifact.sha256, "https://repo.local/trusted-lib-2.1.0.tar.gz"
        )
        import hmac, hashlib
        self.authenticator = hmac.new(self.signing_secret, self.artifact.sha256.encode("ascii"), hashlib.sha256).digest()
        self.prov = activity_l22_03.SLSAProvenanceV1_2(
            type="https://in-toto.io/Statement/v1",
            predicate_type="https://slsa.dev/provenance/v1",
            subject_name="trusted-lib",
            subject_sha256=self.artifact.sha256,
            builder_id="https://builder.example/essential-cs@v1",
            source_repository="https://source.example/trusted-lib",
            source_commit="e0f1d2c3b4a5968778695a4b3c2d1e0f12345678",
            build_type="https://build.example/types/essential-cs-python/v1",
        )

    def test_supply_chain_legitimate_package_accept(self) -> None:
        report = activity_l22_03.audit_dependency_against_policy(
            self.entry, self.artifact, self.prov, self.authenticator, self.key_id, self.signing_secret, self.policy,
            rebuild_bytes=self.artifact.content,
        )
        self.assertEqual(report["verdict"], "ACCEPT")
        self.assertEqual(len(report["reasons"]), 0)
        self.assertTrue(report["layers"]["layer1_version_pinned"])
        self.assertTrue(report["layers"]["layer2_expected_digest_present"])
        self.assertTrue(report["layers"]["layer3_byte_integrity"])
        self.assertTrue(report["layers"]["layer4_reproducibility"])
        self.assertTrue(report["layers"]["layer5_6_teaching_authenticator_and_identity_policy"])
        self.assertTrue(report["layers"]["layer7_8_provenance_and_builder"])

    def test_layer5_6_report_key_consistency_across_paths(self) -> None:
        """Issue #125: verify layer 5/6 canonical key across success, missing, and skipped paths."""
        canonical_key = "layer5_6_teaching_authenticator_and_identity_policy"
        stale_key = "layer5_6_signature_and_identity"

        # 1. Success path
        rep_success = activity_l22_03.audit_dependency_against_policy(
            self.entry, self.artifact, self.prov, self.authenticator, self.key_id, self.signing_secret, self.policy,
            rebuild_bytes=self.artifact.content,
        )
        self.assertIn(canonical_key, rep_success["layers"])
        self.assertNotIn(stale_key, rep_success["layers"])
        self.assertIs(rep_success["layers"][canonical_key], True)

        # 2. Missing authenticator path
        rep_missing = activity_l22_03.audit_dependency_against_policy(
            self.entry, self.artifact, self.prov, None, self.key_id, self.signing_secret, self.policy,
            rebuild_bytes=self.artifact.content,
        )
        self.assertIn(canonical_key, rep_missing["layers"])
        self.assertNotIn(stale_key, rep_missing["layers"])
        self.assertIs(rep_missing["layers"][canonical_key], False)

        # 3. Policy skipped path
        policy_skip = activity_l22_03.VerifierPolicy(require_signature=False)
        rep_skipped = activity_l22_03.audit_dependency_against_policy(
            self.entry, self.artifact, self.prov, None, self.key_id, self.signing_secret, policy_skip,
            rebuild_bytes=self.artifact.content,
        )
        self.assertIn(canonical_key, rep_skipped["layers"])
        self.assertNotIn(stale_key, rep_skipped["layers"])
        self.assertEqual(rep_skipped["layers"][canonical_key], "SKIPPED_BY_POLICY")

    def test_layer3_tampered_byte_rejection(self) -> None:
        tampered_artifact = activity_l22_03.SyntheticArtifact("trusted-lib", "2.1.0", self.code + b"# corrupted\n")
        report = activity_l22_03.audit_dependency_against_policy(
            self.entry, tampered_artifact, self.prov, self.authenticator, self.key_id, self.signing_secret, self.policy,
            rebuild_bytes=tampered_artifact.content,
        )
        self.assertEqual(report["verdict"], "REJECT")
        self.assertFalse(report["layers"]["layer3_byte_integrity"])
        self.assertTrue(any("Layer 3 FAIL" in r for r in report["reasons"]))

    def test_layer4_build_reproducibility(self) -> None:
        build_1 = b"reproducible-binary-package-content"
        build_2 = b"reproducible-binary-package-content"
        build_diff = b"reproducible-binary-package-content-with-jitter"

        ok_rep, _ = activity_l22_03.verify_layer4_reproducibility(build_1, build_2)
        self.assertTrue(ok_rep)

        bad_rep, _ = activity_l22_03.verify_layer4_reproducibility(build_1, build_diff)
        self.assertFalse(bad_rep)

    def test_layer4_policy_rejects_mismatched_rebuild(self) -> None:
        report = activity_l22_03.audit_dependency_against_policy(
            self.entry,
            self.artifact,
            self.prov,
            self.authenticator,
            self.key_id,
            self.signing_secret,
            self.policy,
            rebuild_bytes=b"independent-rebuild-does-not-match",
        )
        self.assertEqual(report["verdict"], "REJECT")
        self.assertFalse(report["layers"]["layer4_reproducibility"])
        self.assertTrue(any("Layer 4 FAIL" in r for r in report["reasons"]))

    def test_layer7_8_untrusted_builder_rejection(self) -> None:
        rogue_prov = activity_l22_03.SLSAProvenanceV1_2(
            type="https://in-toto.io/Statement/v1",
            predicate_type="https://slsa.dev/provenance/v1",
            subject_name="trusted-lib",
            subject_sha256=self.artifact.sha256,
            builder_id="https://builder.example/untrusted@v1",
            source_repository="https://source.example/trusted-lib",
            source_commit="e0f1d2c3b4a5968778695a4b3c2d1e0f12345678",
            build_type="https://build.example/types/untrusted/v1",
        )
        report = activity_l22_03.audit_dependency_against_policy(
            self.entry, self.artifact, rogue_prov, self.authenticator, self.key_id, self.signing_secret, self.policy,
            rebuild_bytes=self.artifact.content,
        )
        self.assertEqual(report["verdict"], "REJECT")
        self.assertFalse(report["layers"]["layer7_8_provenance_and_builder"])
        layer78_reasons = [r for r in report["reasons"] if "Layer 7/8" in r]
        self.assertTrue(layer78_reasons, "rejection must be attributed to Layer 7/8")
        self.assertTrue(
            any("builder" in r.lower() for r in layer78_reasons),
            "Layer 7/8 rejection must identify the builder check",
        )
        self.assertTrue(
            any("allowlist" in r for r in layer78_reasons),
            "Layer 7/8 rejection must reference the local synthetic builder allowlist",
        )
        self.assertTrue(
            any(rogue_prov.builder_id in r for r in layer78_reasons),
            "Layer 7/8 rejection must name the rejected builder id",
        )
        self.assertFalse(
            any("digital signature" in r.lower() or "attestation verification" in r.lower() for r in layer78_reasons),
            "Layer 7/8 rejection must not claim real signature or attestation verification",
        )


class TestM22_ResetAndCleanup(unittest.TestCase):
    """Unit tests for M22 idempotent fail-closed reset mechanism."""

    def test_reset_m22_scratch(self) -> None:
        scratch = Path(reset.SCRATCH_DIR)
        scratch.mkdir(parents=True, exist_ok=True)
        dummy_file = scratch / "test_scratch_artifact.tmp"
        dummy_file.write_text("temporary-m22-data", encoding="utf-8")

        # Run reset
        removed = reset.reset_m22_environment(verbose=False)
        self.assertGreaterEqual(removed, 1)
        self.assertFalse(scratch.exists())

        # Second run: idempotent success
        removed_again = reset.reset_m22_environment(verbose=False)
        self.assertEqual(removed_again, 0)
        self.assertFalse(scratch.exists())


if __name__ == "__main__":
    unittest.main()
