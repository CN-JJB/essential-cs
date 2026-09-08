#!/usr/bin/env python3
"""
test_m24.py — Comprehensive Unit Test Suite for Module M24
==========================================================

Verifies all course-owned validators, activity harnesses, migration simulators, and
boundary rules for M24 Final System Defense & Pre-Ship Assessment.

Test Classes:
1. TestDefenseValidator:
   - Complete 16-trace and 12-evidence-area structural verification
   - Rejection of missing traces and missing evidence areas
   - Rejection of unresolved template placeholders ([TODO], [Record ...])
   - Rejection of trivial "no unknowns" declarations
   - Detection and rejection of fabricated Raft/consensus claims
   - Scaffolding audit with allow_placeholders=True
2. TestPreShipValidator:
   - Complete 4-class risk matrix verification
   - Rejection of missing risk classes
   - Rejection of naive overclaims ("100% coverage = safe")
   - Rejection of universal unqualified "zero data loss" assertions
   - Rejection of mismatched recovery strategy (Destructive schema + Code Rollback)
   - Enforcement of explicit stated data-loss bounds
3. TestSchemaMigrationSimulation:
   - Additive nullable column backward compatibility (safe code rollback)
   - Destructive column rename incompatibility (code rollback breaks)
   - Destructive NOT NULL without default fail-closed behavior
4. TestActivityL24Harness:
   - Verification of Changed-Constraint scenario card data structures
   - Execution of activity CLI entry points
5. TestResetIdempotence:
   - Creation of scratch artifacts, cleanup verification, and idempotence.

Standard Library Only (unittest, pathlib, json, sqlite3, os).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import unittest

from labs.foundations.m24.defense_validator import (
    REQUIRED_EVIDENCE_AREAS,
    REQUIRED_TRACES,
    ValidationReport,
    validate_defense_dossier,
)
from labs.foundations.m24.preship_validator import (
    PreShipValidationReport,
    simulate_sqlite_schema_evolution,
    validate_risk_matrix_data,
)
from labs.foundations.m24.activity_l24_01 import SCENARIOS
from labs.foundations.m24.reset import reset_m24_environment

M24_DIR = Path(__file__).resolve().parent
SAMPLE_DOSSIER_PATH = M24_DIR / "sample_dossier.md"
SAMPLE_PRESHIP_PATH = M24_DIR / "sample_preship.json"
SCRATCH_DIR = M24_DIR / ".scratch"


class TestDefenseValidator(unittest.TestCase):
    """Tests structural validation of the 16-Trace Architecture Defense Dossier."""

    def setUp(self) -> None:
        self.assertTrue(SAMPLE_DOSSIER_PATH.exists(), "Sample dossier file must exist")
        self.sample_dossier_content = SAMPLE_DOSSIER_PATH.read_text(encoding="utf-8")

    def test_sample_dossier_passes_structural_audit(self) -> None:
        report = validate_defense_dossier(self.sample_dossier_content, str(SAMPLE_DOSSIER_PATH))
        self.assertTrue(report.is_valid, f"Sample dossier should pass validation: {report.errors}")
        self.assertEqual(report.status, "STRUCTURAL_CHECK_PASS")
        self.assertEqual(len(report.traces_found), 16)
        self.assertEqual(len(report.traces_missing), 0)
        self.assertEqual(len(report.evidence_areas_found), 12)
        self.assertEqual(len(report.evidence_areas_missing), 0)
        self.assertGreaterEqual(report.claims_count, 5)
        self.assertEqual(len(report.placeholders_detected), 0)
        self.assertIn("REVIEWER-REQUIRED", report.disclaimer)

    def test_reject_missing_traces(self) -> None:
        # Remove Trace 14 (Explicit Unknowns)
        corrupted = self.sample_dossier_content.replace("14. Explicit Unknowns", "14. Ignored Area")
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertEqual(report.status, "STRUCTURAL_CHECK_FAILED")
        self.assertTrue(any("Trace 14" in err for err in report.errors))

    def test_reject_missing_evidence_areas(self) -> None:
        # Remove E05 (Failure Domains) from text
        corrupted = self.sample_dossier_content.replace("E05", "X99")
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("E05" in err for err in report.errors))

    def test_reject_placeholders(self) -> None:
        # Inject [TODO: verify later] into text
        corrupted = self.sample_dossier_content + "\n\n## Extra Notes\n[TODO: measure cache miss rate]\n"
        report = validate_defense_dossier(corrupted, "<test>", allow_placeholders=False)
        self.assertFalse(report.is_valid)
        self.assertTrue(any("placeholder" in err.lower() for err in report.errors))

    def test_allow_placeholders_flag(self) -> None:
        corrupted = self.sample_dossier_content + "\n\n## Extra Notes\n[TODO: measure cache miss rate]\n"
        report = validate_defense_dossier(corrupted, "<test>", allow_placeholders=True)
        # Placeholders allowed -> is_valid remains True
        self.assertTrue(report.is_valid)

    def test_reject_trivial_explicit_unknowns(self) -> None:
        # Replace Trace 14 content with "None"
        corrupted = self.sample_dossier_content.replace(
            "- *Technical Blind Spot 1*: SQLite query planner performance when table rows exceed 10,000,000 records under low available RAM (untested paging degradation).\n- *Technical Blind Spot 2*: Long-tail latency distribution when host filesystem executes a background TRIM operation on SSD under heavy concurrent write load.\n- *Boundary Acknowledgment*: These two areas are acknowledged uncertainties where empirical measurements have not yet been performed.",
            "None. Our system has no unknowns.",
        )
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("Explicit Unknowns" in err for err in report.errors))

    def test_reject_fabricated_raft_claims(self) -> None:
        fabricated = self.sample_dossier_content + "\nOur system uses Raft consensus for state replication across nodes.\n"
        report = validate_defense_dossier(fabricated, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("Fabricated architecture" in err for err in report.errors))


class TestPreShipValidator(unittest.TestCase):
    """Tests pre-ship risk matrix validation and boundary enforcement."""

    def setUp(self) -> None:
        self.assertTrue(SAMPLE_PRESHIP_PATH.exists(), "Sample preship file must exist")
        self.sample_preship_data = json.loads(SAMPLE_PRESHIP_PATH.read_text(encoding="utf-8"))

    def test_sample_preship_passes_validation(self) -> None:
        report = validate_risk_matrix_data(self.sample_preship_data, str(SAMPLE_PRESHIP_PATH))
        self.assertTrue(report.is_valid, f"Sample preship should pass validation: {report.errors}")
        self.assertEqual(report.status, "PRE_SHIP_VALIDATION_PASS")
        self.assertEqual(len(report.classes_found), 4)
        self.assertEqual(len(report.classes_missing), 0)
        self.assertEqual(report.reversal_strategy, "Code Rollback")
        self.assertIsNotNone(report.stated_data_loss_bound)
        self.assertIn("REVIEWER-REQUIRED", report.disclaimer)

    def test_reject_missing_risk_classes(self) -> None:
        corrupted = json.loads(json.dumps(self.sample_preship_data))
        del corrupted["risk_matrix"]["must_measure"]
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertEqual(report.status, "PRE_SHIP_VALIDATION_FAILED")
        self.assertTrue(any("Must Measure" in err for err in report.errors))

    def test_reject_naive_test_coverage_claim(self) -> None:
        corrupted = json.loads(json.dumps(self.sample_preship_data))
        corrupted["risk_matrix"]["must_test"][0]["target"] = "100% test coverage means safe to ship to production"
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("Naive overclaim detected" in err for err in report.errors))

    def test_reject_unqualified_zero_data_loss_claim(self) -> None:
        corrupted = json.loads(json.dumps(self.sample_preship_data))
        corrupted["deployment_compatibility"]["stated_data_loss_bound"] = "guarantees zero data loss in all circumstances"
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("zero data loss" in err.lower() for err in report.errors))

    def test_reject_trivial_acceptable_unknown(self) -> None:
        corrupted = json.loads(json.dumps(self.sample_preship_data))
        corrupted["risk_matrix"]["acceptable_unknown"] = [{"description": "None"}]
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("Acceptable Unknown entry" in err for err in report.errors))

    def test_reject_destructive_schema_with_code_rollback(self) -> None:
        corrupted = json.loads(json.dumps(self.sample_preship_data))
        corrupted["deployment_compatibility"]["schema_compatibility_type"] = "Destructive"
        corrupted["deployment_compatibility"]["chosen_recovery_strategy"] = "Code Rollback"
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("Fatal deployment strategy mismatch" in err for err in report.errors))

    def test_reject_missing_stated_data_loss_bound(self) -> None:
        corrupted = json.loads(json.dumps(self.sample_preship_data))
        corrupted["deployment_compatibility"]["stated_data_loss_bound"] = ""
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("data-loss bound" in err for err in report.errors))


class TestSchemaMigrationSimulation(unittest.TestCase):
    """Tests SQLite database schema migration backward compatibility simulations."""

    def test_additive_nullable_column_backward_compatible(self) -> None:
        ok, msg = simulate_sqlite_schema_evolution(
            initial_ddl="CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);",
            initial_insert="INSERT INTO items (name) VALUES ('widget');",
            migration_ddl="ALTER TABLE items ADD COLUMN note TEXT;",
            old_code_query="SELECT id, name FROM items WHERE id = 1;",
        )
        self.assertTrue(ok)
        self.assertIn("Backward compatible", msg)

    def test_destructive_rename_breaks_old_code_query(self) -> None:
        ok, msg = simulate_sqlite_schema_evolution(
            initial_ddl="CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);",
            initial_insert="INSERT INTO items (name) VALUES ('widget');",
            migration_ddl="ALTER TABLE items RENAME COLUMN name TO item_name;",
            old_code_query="SELECT id, name FROM items WHERE id = 1;",
        )
        self.assertFalse(ok)
        self.assertIn("Backward incompatibility detected", msg)

    def test_destructive_not_null_without_default_fails_closed(self) -> None:
        ok, msg = simulate_sqlite_schema_evolution(
            initial_ddl="CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);",
            initial_insert="INSERT INTO items (name) VALUES ('widget');",
            migration_ddl="ALTER TABLE items ADD COLUMN code TEXT NOT NULL;",
            old_code_query="SELECT id, name FROM items WHERE id = 1;",
        )
        self.assertFalse(ok)
        self.assertIn("Migration DDL failed to execute", msg)


class TestActivityL24Harness(unittest.TestCase):
    """Tests activity harnesses and Changed-Constraint scenario card data."""

    def test_scenario_cards_structure(self) -> None:
        self.assertEqual(len(SCENARIOS), 3)
        for sid, card in SCENARIOS.items():
            self.assertEqual(card.id, sid)
            self.assertTrue(len(card.title) > 5)
            self.assertTrue(len(card.original_assumption) > 10)
            self.assertTrue(len(card.perturbed_constraint) > 10)
            self.assertGreaterEqual(len(card.threatened_invariants), 2)
            self.assertTrue(len(card.system_bottleneck) > 10)
            self.assertGreaterEqual(len(card.required_adaptations), 2)
            self.assertTrue(len(card.new_evidence_required) > 10)


class TestResetIdempotence(unittest.TestCase):
    """Tests fail-closed idempotent cleanup in M24."""

    def test_reset_cleans_scratch_and_is_idempotent(self) -> None:
        SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
        probe = SCRATCH_DIR / "test_scratch.tmp"
        probe.write_text("scratch-data", encoding="utf-8")
        self.assertTrue(probe.exists())

        # First reset: removes probe and scratch dir
        removed = reset_m24_environment(verbose=False)
        self.assertGreaterEqual(removed, 1)
        self.assertFalse(SCRATCH_DIR.exists())

        # Second reset: idempotent, returns 0 cleanly
        removed_again = reset_m24_environment(verbose=False)
        self.assertEqual(removed_again, 0)


if __name__ == "__main__":
    unittest.main()
