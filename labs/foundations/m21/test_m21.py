#!/usr/bin/env python3
"""
test_m21.py — Standard Library Unit Test Suite for Foundations Module M21
========================================================================

Verifies:
1. L21-01 Path Confinement & Boundary Verification (path_confinement.py)
   - Naive string check limitations
   - Sibling-prefix confusion trap
   - Commonpath ancestry verification
   - Embedded NUL byte rejection without file open
   - Symlink escape detection (or truthful BLOCKED/NOT RUN reporting)
   - Zero host-sensitive file access
2. L21-02 Cryptographic Roles & Misuse Boundaries (crypto_roles.py)
   - Deterministic SHA-256 hashing
   - In-path active modifier demonstration (unkeyed hash != authenticity)
   - HMAC-SHA-256 tamper detection under shared secret
   - compare_digest API contract & timing mitigation (no physical proof claim)
   - Primitive selection matrix invariants (no unconditional non-repudiation)
   - Optional Ed25519 signature probe
3. Activity execution & observation schema (activity_l21_01.py, activity_l21_02.py)
4. Idempotent, fail-closed cleanup (reset.py)
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

# Ensure labs/foundations/m21 is in sys.path for root or direct execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

import activity_l21_01
import activity_l21_02
import crypto_roles
import path_confinement
import reset


class TestL21_01_PathConfinement(unittest.TestCase):
    """Unit tests for L21-01 filesystem boundary & confinement mechanism."""

    def setUp(self) -> None:
        self.tree = path_confinement.build_synthetic_tree()

    def tearDown(self) -> None:
        self.tree.cleanup()

    def test_naive_string_looks_safe(self) -> None:
        # Relative clean path looks safe
        self.assertTrue(path_confinement.naive_string_looks_safe("notes/hello.txt"))
        # Dotdot rejected by naive syntactic check
        self.assertFalse(path_confinement.naive_string_looks_safe("../outside.txt"))
        self.assertFalse(path_confinement.naive_string_looks_safe("notes/../notes/hello.txt"))
        # Absolute path rejected
        self.assertFalse(path_confinement.naive_string_looks_safe(str(self.tree.outside_file)))
        # Embedded NUL rejected
        self.assertFalse(path_confinement.naive_string_looks_safe("hello.txt\x00extra"))
        # Traversal without dotdot looks safe to naive check (symlink trap)
        self.assertTrue(path_confinement.naive_string_looks_safe("escape_link"))

    def test_prefix_startswith_confusion(self) -> None:
        """Demonstrates that startswith falsely considers sibling-prefix contained."""
        authorized = self.tree.authorized_root.resolve()
        sibling_evil = self.tree.sibling_evil_file.resolve()
        # Sibling directory has authorized root name as string prefix ('.../store' in '.../store-evil')
        prefix_match = path_confinement.prefix_startswith_looks_contained(authorized, sibling_evil)
        self.assertTrue(prefix_match, "startswith should demonstrate sibling-prefix confusion")
        # But real resolved ancestry correctly identifies it as NOT contained
        contained = path_confinement.is_resolved_contained(authorized, sibling_evil)
        self.assertFalse(contained, "commonpath ancestry must reject sibling-prefix")

    def test_is_resolved_contained(self) -> None:
        authorized = self.tree.authorized_root.resolve()
        allowed = self.tree.allowed_file.resolve()
        outside = self.tree.outside_file.resolve()

        self.assertTrue(path_confinement.is_resolved_contained(authorized, allowed))
        self.assertFalse(path_confinement.is_resolved_contained(authorized, outside))

    def test_embedded_nul_byte_rejection(self) -> None:
        verdict = path_confinement.classify_candidate(
            self.tree.authorized_root,
            "notes/hello.txt\x00../outside.txt",
            "nul-test",
            read_if_allowed=True,
        )
        self.assertEqual(verdict.decision, "DENIED")
        self.assertFalse(verdict.opened_file)
        self.assertFalse(verdict.opened_host_sensitive_path)

    def test_symlink_escape_or_blocked(self) -> None:
        verdict = path_confinement.classify_candidate(
            self.tree.authorized_root,
            "escape_link",
            "symlink-test",
            read_if_allowed=True,
            symlink_dimension=self.tree.symlink_disposition,
        )
        if self.tree.symlink_path is not None:
            # Symlinks are supported on this host: escape must be DENIED
            self.assertEqual(verdict.decision, "DENIED")
            self.assertFalse(verdict.resolved_contained)
            self.assertFalse(verdict.opened_file)
        else:
            # Symlinks not supported: must report BLOCKED / NOT RUN truthfully
            self.assertIn("BLOCKED / NOT RUN", verdict.symlink_dimension)

    def test_standard_cases_evaluation(self) -> None:
        cases = path_confinement.evaluate_standard_cases(self.tree, read_if_allowed=True)
        self.assertGreaterEqual(len(cases), 7)
        decisions = {c.case_id: c.decision for c in cases}
        self.assertEqual(decisions["contained-relative"], "ALLOWED")
        self.assertEqual(decisions["dotdot-but-still-contained"], "ALLOWED")
        self.assertEqual(decisions["parent-traversal"], "DENIED")
        self.assertEqual(decisions["absolute-outside"], "DENIED")
        self.assertEqual(decisions["sibling-prefix"], "DENIED")
        self.assertEqual(decisions["embedded-nul"], "DENIED")

        # Zero access to host sensitive paths across all evaluated cases
        for c in cases:
            self.assertFalse(c.opened_host_sensitive_path)


class TestL21_02_CryptoRoles(unittest.TestCase):
    """Unit tests for L21-02 cryptographic primitive roles & misuse boundaries."""

    def test_unkeyed_hash_deterministic(self) -> None:
        msg = b"test-message-for-sha256"
        digest1 = crypto_roles.compute_unkeyed_hash(msg)
        digest2 = crypto_roles.compute_unkeyed_hash(msg)
        self.assertEqual(digest1, digest2)
        self.assertEqual(len(digest1), 64)

    def test_unkeyed_hash_active_modifier_vulnerability(self) -> None:
        demo = crypto_roles.demonstrate_unkeyed_hash_tamper(
            crypto_roles.SYNTHETIC_MESSAGE, crypto_roles.SYNTHETIC_TAMPERED
        )
        # Original message passes original digest
        self.assertTrue(demo["verify_original_against_original_digest"])
        # Tampered message fails against original digest (corruption detected)
        self.assertFalse(demo["verify_tampered_against_original_digest"])
        # BUT tampered message PASSES against recomputed digest (in-path active modifier)
        self.assertTrue(demo["verify_tampered_against_recomputed_digest"])

    def test_hmac_tamper_detection(self) -> None:
        key = crypto_roles.new_synthetic_mac_key()
        self.assertEqual(len(key), 32)
        demo = crypto_roles.demonstrate_hmac_tamper(
            key, crypto_roles.SYNTHETIC_MESSAGE, crypto_roles.SYNTHETIC_TAMPERED
        )
        # Original verifies
        self.assertTrue(demo["verify_original"])
        # Tampered message rejected
        self.assertFalse(demo["verify_modified_message"])
        # Forged tag rejected
        self.assertFalse(demo["verify_modified_tag"])

    def test_compare_digest_probe(self) -> None:
        probe = crypto_roles.compare_digest_contract_probe()
        self.assertTrue(probe["same_ascii_hex_equal"])
        self.assertFalse(probe["different_ascii_hex_equal"])
        self.assertEqual(probe["mixed_str_bytes_error"], "TypeError")
        self.assertFalse(probe["physical_constant_time_claimed"])

    def test_primitive_selection_matrix(self) -> None:
        matrix = crypto_roles.primitive_selection_matrix()
        self.assertEqual(len(matrix), 6)
        for row in matrix:
            self.assertIn("scenario", row)
            self.assertIn("required_property", row)
            self.assertIn("chosen_primitive", row)
            self.assertIn("incorrect_tempting_primitive", row)
            self.assertIn("non_guarantee", row)
            # Must not claim unconditional non-repudiation as a primitive guarantee
            self.assertNotIn("unconditional non-repudiation", row["chosen_primitive"].lower())

    def test_optional_signature_demo(self) -> None:
        demo = crypto_roles.optional_signature_demo(crypto_roles.SYNTHETIC_MESSAGE)
        self.assertIn(demo["disposition"], ["OPTIONAL PACKAGE AVAILABLE", "NOT RUN / CAPABILITY ABSENT"])
        if demo["disposition"] == "OPTIONAL PACKAGE AVAILABLE":
            self.assertTrue(demo["verified_under_matching_public_key"])
            self.assertFalse(demo["verified_under_unrelated_public_key"])


class TestM21ActivitiesAndReset(unittest.TestCase):
    """Verifies that activities run and generate compliant observations, and reset works."""

    def test_activity_l21_01_execution(self) -> None:
        res = activity_l21_01.run_activity(verbose=False)
        self.assertEqual(res["module"], "M21")
        self.assertEqual(res["lesson"], "L21-01")
        self.assertGreaterEqual(len(res["cases_evaluated"]), 7)

    def test_activity_l21_02_execution(self) -> None:
        res = activity_l21_02.run_activity(verbose=False)
        self.assertEqual(res["module"], "M21")
        self.assertEqual(res["lesson"], "L21-02")
        self.assertTrue(res["hash_tamper_demonstration"]["verify_original_against_original_digest"])
        self.assertTrue(res["hmac_tamper_demonstration"]["verify_original"])

    def test_reset_idempotent(self) -> None:
        # First reset cleans whatever scratch/cache was created
        reset.reset_m21_environment(verbose=False)
        scratch = Path(__file__).resolve().parent / ".scratch"
        self.assertFalse(scratch.exists())
        # Second reset should cleanly succeed without error (idempotence)
        count = reset.reset_m21_environment(verbose=False)
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
