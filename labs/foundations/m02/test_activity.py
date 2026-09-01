import io
import unittest
from contextlib import redirect_stdout

import activity


class GrowthCountTests(unittest.TestCase):
    def test_exact_fixed_counts(self) -> None:
        expected = {
            8: (8, 28, 3),
            16: (16, 120, 4),
            32: (32, 496, 5),
            64: (64, 2016, 6),
        }
        for n, counts in expected.items():
            self.assertEqual(
                (
                    activity.one_pass_count(activity.make_records(n)),
                    activity.nested_pair_count(n),
                    activity.halving_steps(n),
                ),
                counts,
            )

    def test_canonical_bounded_labels(self) -> None:
        self.assertEqual(activity.ASYMPTOTIC_LABELS["one_pass"], "O(n)")
        self.assertEqual(activity.ASYMPTOTIC_LABELS["nested_pairs"], "O(n^2)")
        self.assertEqual(activity.ASYMPTOTIC_LABELS["halving"], "O(log n)")
        self.assertEqual(activity.ASYMPTOTIC_LABELS["linear_lookup"], "O(n)")
        self.assertIn("O(1)", activity.ASYMPTOTIC_LABELS["indexed_lookup_model"])


class LookupTradeoffTests(unittest.TestCase):
    def test_last_key_counts(self) -> None:
        for n in (8, 64, 1024):
            records = activity.make_records(n)
            index, build_count = activity.build_index(records)
            target = records[-1].key
            linear, linear_count = activity.linear_lookup(records, target)
            indexed, indexed_count = activity.indexed_lookup(records, index, target)
            self.assertEqual(linear, indexed)
            self.assertEqual(linear_count, n)
            self.assertEqual(indexed_count, 1)
            self.assertEqual(build_count, n)

    def test_missing_lookup_is_deterministic(self) -> None:
        records = activity.make_records(8)
        index, _ = activity.build_index(records)
        self.assertEqual(activity.linear_lookup(records, "missing"), (None, 8))
        self.assertEqual(activity.indexed_lookup(records, index, "missing"), (None, 1))


class CorrectnessTests(unittest.TestCase):
    def test_baseline_invariant_and_reset_determinism(self) -> None:
        records1, index1 = activity.baseline_state()
        records2, index2 = activity.baseline_state()
        self.assertTrue(activity.invariant_holds(records1, index1))
        self.assertEqual(records1, records2)
        self.assertEqual(index1, index2)

    def test_duplicate_counterexample_breaks_invariant_and_lookup_agreement(self) -> None:
        records, index = activity.baseline_state()
        activity.flawed_update_duplicate(records, index, "r0002", 999)
        self.assertFalse(activity.invariant_holds(records, index))
        linear, _ = activity.linear_lookup(records, "r0002")
        indexed, _ = activity.indexed_lookup(records, index, "r0002")
        self.assertEqual(linear, activity.Record("r0002", 20))
        self.assertEqual(indexed, activity.Record("r0002", 999))
        self.assertNotEqual(linear, indexed)

    def test_correct_update_preserves_invariant(self) -> None:
        records, index = activity.baseline_state()
        self.assertTrue(activity.correct_update(records, index, "r0002", 999))
        self.assertTrue(activity.invariant_holds(records, index))
        linear, _ = activity.linear_lookup(records, "r0002")
        indexed, _ = activity.indexed_lookup(records, index, "r0002")
        self.assertEqual(linear, activity.Record("r0002", 999))
        self.assertEqual(linear, indexed)

    def test_missing_update_changes_nothing(self) -> None:
        records, index = activity.baseline_state()
        before_records = list(records)
        before_index = dict(index)
        self.assertFalse(activity.correct_update(records, index, "missing", 777))
        self.assertEqual(records, before_records)
        self.assertEqual(index, before_index)
        self.assertTrue(activity.invariant_holds(records, index))

    def test_flow_contains_required_cycle(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            activity.command_flow()
        output = buffer.getvalue()
        required_fragments = [
            "RESET invariant=True",
            "BASELINE invariant=True",
            "COUNTS 64 64 2016 6",
            "LOOKUP 1024 r1023 1024 1 1024",
            "BREAK after.invariant=False",
            "BREAK paths_agree=False",
            "CORRECT invariant=True",
            "CORRECT paths_agree=True",
            "CORRECT missing.updated=False unchanged=True",
        ]
        for fragment in required_fragments:
            self.assertIn(fragment, output)
        self.assertEqual(output.count("RESET invariant=True"), 2)


if __name__ == "__main__":
    unittest.main()
