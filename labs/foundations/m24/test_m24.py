#!/usr/bin/env python3
"""M24 standard-library structural validator tests."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from labs.foundations.m24.defense_validator import validate_defense_dossier
from labs.foundations.m24.preship_validator import simulate_sqlite_schema_evolution, validate_risk_matrix_data
from labs.foundations.m24.activity_l24_01 import SCENARIOS
from labs.foundations.m24.reset import reset_m24_environment

M24_DIR = Path(__file__).resolve().parent
SAMPLE_DOSSIER_PATH = M24_DIR / "sample_dossier.md"
SAMPLE_PRESHIP_PATH = M24_DIR / "sample_preship.json"
SCRATCH_DIR = M24_DIR / ".scratch"


class TestDefenseValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = SAMPLE_DOSSIER_PATH.read_text(encoding="utf-8")

    def test_sample_dossier_passes_structural_audit(self) -> None:
        report = validate_defense_dossier(self.sample, str(SAMPLE_DOSSIER_PATH))
        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.status, "STRUCTURAL_CHECK_PASS")
        self.assertEqual(len(report.traces_found), 16)
        self.assertEqual(report.evidence_rows_valid, 12)
        self.assertEqual(report.claims_count, 5)
        self.assertEqual(report.explicit_unknown_ids, report.learning_plan_linked_ids)
        self.assertIn("REVIEWER-REQUIRED", report.disclaimer)

    def test_reject_missing_trace_heading(self) -> None:
        report = validate_defense_dossier(
            self.sample.replace("### 14. Explicit Unknowns", "### 14. Ignored Area"), "<test>"
        )
        self.assertFalse(report.is_valid)

    def test_reject_missing_evidence_matrix_row(self) -> None:
        report = validate_defense_dossier(self.sample.replace("| E05 |", "| X05 |"), "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("E05" in err for err in report.errors))

    def test_reject_dangling_claim_reference(self) -> None:
        corrupted = self.sample.replace(
            "| E01 | End-to-End Request Flow | CLM-01 |",
            "| E01 | End-to-End Request Flow | CLM-99 |",
        )
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertIn("CLM-99", report.dangling_claim_refs)
        self.assertEqual(report.claims_count, 5, "an Evidence Matrix CLM reference must not be re-parsed as a claim row")

    def test_evidence_matrix_clm_refs_are_not_claim_rows(self) -> None:
        """Issue #127: E01-E12 rows referencing CLM-01 must never count as Claim Register rows."""
        corrupted = re.sub(
            r"(?im)^##\s+Architectural Claim Register\s*$.*?(?=^##\s+)",
            "",
            self.sample,
            flags=re.S,
        )
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertEqual(report.claims_count, 0, "E-matrix CLM references must not be parsed as Claim Register rows")
        self.assertTrue(any("at least 5" in err for err in report.errors))
        self.assertIn("CLM-01", report.dangling_claim_refs)

    def test_claim_register_row_missing_field_fails(self) -> None:
        """Issue #127: a malformed Claim Register row inside the register section must still FAIL."""
        corrupted = self.sample.replace("UNVERIFIED_MEASUREMENT_REQUIRED", "-")
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("CLM-03" in err and "status" in err.lower() for err in report.errors))

    def test_reject_missing_evidence_inference_limit(self) -> None:
        corrupted = self.sample.replace(
            "| E02 | State & Data Lifecycle | CLM-01 | Trace 2 | Course reference maps volatile, durable, and configuration state | Synthetic fixture only; learner must replace with actual state evidence |",
            "| E02 | State & Data Lifecycle | CLM-01 | Trace 2 | Course reference maps volatile, durable, and configuration state | - |",
        )
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("E02" in err and "inference" in err.lower() for err in report.errors))

    def test_reject_placeholders(self) -> None:
        report = validate_defense_dossier(self.sample + "\n[TODO: learner evidence]\n", "<test>")
        self.assertFalse(report.is_valid)

    def test_allow_placeholders_flag(self) -> None:
        report = validate_defense_dossier(
            self.sample + "\n[TODO: learner evidence]\n", "<test>", allow_placeholders=True
        )
        self.assertTrue(report.is_valid)

    def test_reject_unlinked_unknown(self) -> None:
        corrupted = self.sample.replace("UNK-02", "UNK-99", 1)
        report = validate_defense_dossier(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("Learning Plan" in err for err in report.errors))

    def test_mechanism_name_is_reviewer_question_not_blacklist(self) -> None:
        report = validate_defense_dossier(
            self.sample + "\nReviewer note: an actual learner system might genuinely contain Raft.\n", "<test>"
        )
        self.assertTrue(report.is_valid)


class TestPreShipValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = json.loads(SAMPLE_PRESHIP_PATH.read_text(encoding="utf-8"))

    def test_sample_preship_passes_structural_validation(self) -> None:
        report = validate_risk_matrix_data(self.sample, str(SAMPLE_PRESHIP_PATH))
        self.assertTrue(report.is_valid, report.errors)
        self.assertEqual(report.status, "PRE_SHIP_STRUCTURAL_CHECK_PASS")
        self.assertEqual(len(report.classes_found), 4)

    def test_reject_missing_risk_class(self) -> None:
        corrupted = json.loads(json.dumps(self.sample))
        del corrupted["risk_matrix"]["must_measure"]
        self.assertFalse(validate_risk_matrix_data(corrupted, "<test>").is_valid)

    def test_reject_missing_risk_priority_field(self) -> None:
        corrupted = json.loads(json.dumps(self.sample))
        del corrupted["risk_matrix"]["must_test"][0]["evidence_gap"]
        report = validate_risk_matrix_data(corrupted, "<test>")
        self.assertFalse(report.is_valid)
        self.assertTrue(any("evidence_gap" in err for err in report.errors))

    def test_reject_naive_test_coverage_claim(self) -> None:
        corrupted = json.loads(json.dumps(self.sample))
        corrupted["risk_matrix"]["must_test"][0]["success_criterion"] = "100% test coverage means safe to ship"
        self.assertFalse(validate_risk_matrix_data(corrupted, "<test>").is_valid)

    def test_reject_unqualified_zero_data_loss_claim(self) -> None:
        corrupted = json.loads(json.dumps(self.sample))
        corrupted["deployment_compatibility"]["stated_data_loss_bound"] = "guarantees zero data loss in all circumstances"
        self.assertFalse(validate_risk_matrix_data(corrupted, "<test>").is_valid)

    def test_recovery_strategy_is_not_hardcoded_enum(self) -> None:
        customized = json.loads(json.dumps(self.sample))
        customized["deployment_compatibility"]["chosen_recovery_strategy"] = (
            "Project-specific verified snapshot restore followed by forward migration"
        )
        customized["deployment_compatibility"]["recovery_justification"] = (
            "The synthetic scenario records separate code, schema, and restore evidence for this choice."
        )
        self.assertTrue(validate_risk_matrix_data(customized, "<test>").is_valid)

    def test_data_loss_not_applicable_requires_reason(self) -> None:
        no_state = json.loads(json.dumps(self.sample))
        deploy = no_state["deployment_compatibility"]
        deploy["data_loss_applicable"] = False
        deploy["stated_data_loss_bound"] = ""
        deploy["data_loss_not_applicable_reason"] = "Synthetic stateless scenario persists no learner-owned durable data."
        self.assertTrue(validate_risk_matrix_data(no_state, "<test>").is_valid)
        del deploy["data_loss_not_applicable_reason"]
        self.assertFalse(validate_risk_matrix_data(no_state, "<test>").is_valid)


class TestSchemaMigrationSimulation(unittest.TestCase):
    def test_additive_nullable_column_preserves_old_query_in_fixture(self) -> None:
        ok, msg = simulate_sqlite_schema_evolution(
            "CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);",
            "INSERT INTO items (name) VALUES ('widget');",
            "ALTER TABLE items ADD COLUMN note TEXT;",
            "SELECT id, name FROM items WHERE id = 1;",
        )
        self.assertTrue(ok)
        self.assertIn("does not prove whole-application rollback safety", msg)

    def test_column_rename_breaks_old_query_in_fixture(self) -> None:
        ok, msg = simulate_sqlite_schema_evolution(
            "CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);",
            "INSERT INTO items (name) VALUES ('widget');",
            "ALTER TABLE items RENAME COLUMN name TO item_name;",
            "SELECT id, name FROM items WHERE id = 1;",
        )
        self.assertFalse(ok)
        self.assertIn("incompatible", msg)

    def test_not_null_without_default_is_blocked_in_fixture(self) -> None:
        ok, msg = simulate_sqlite_schema_evolution(
            "CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT);",
            "INSERT INTO items (name) VALUES ('widget');",
            "ALTER TABLE items ADD COLUMN code TEXT NOT NULL;",
            "SELECT id, name FROM items WHERE id = 1;",
        )
        self.assertFalse(ok)
        self.assertIn("Migration statement failed", msg)


class TestActivityL24Harness(unittest.TestCase):
    def test_scenario_cards_are_prompts_not_answer_keys(self) -> None:
        self.assertEqual(len(SCENARIOS), 3)
        for sid, card in SCENARIOS.items():
            self.assertEqual(card.id, sid)
            self.assertTrue(card.original_assumption)
            self.assertTrue(card.perturbed_constraint)
            self.assertGreaterEqual(len(card.learner_questions), 5)


class TestResetIdempotence(unittest.TestCase):
    def test_reset_cleans_scratch_and_is_idempotent(self) -> None:
        SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
        (SCRATCH_DIR / "test_scratch.tmp").write_text("scratch-data", encoding="utf-8")
        self.assertGreaterEqual(reset_m24_environment(verbose=False), 1)
        self.assertFalse(SCRATCH_DIR.exists())
        self.assertEqual(reset_m24_environment(verbose=False), 0)


if __name__ == "__main__":
    unittest.main()
