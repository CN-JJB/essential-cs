"""P9 — the integrated walkthrough must hold end to end."""

from __future__ import annotations

import unittest

from _support import temp_dir  # noqa: F401  (keeps the bootstrap import explicit)

from minicloud.walkthrough import run_walkthrough


class TestP9Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The walkthrough is a full end-to-end run; do it once and assert on the
        # single evidence packet rather than paying for it three times.
        cls.result = run_walkthrough()

    def test_full_chain_passes(self):
        failed = [c["step"] for c in self.result["checkpoints"] if not c["ok"]]
        self.assertEqual(failed, [], f"failed checkpoints: {failed}")
        self.assertEqual(self.result["disposition"], "PASS")

    def test_walkthrough_covers_every_layer(self):
        steps = " | ".join(c["step"] for c in self.result["checkpoints"])
        for expected in (
            "health over HTTP",
            "create + read back",
            "malformed request rejected",
            "cross-user read denied",
            "share grants read",
            "revocation removes access",
            "dependency indexed a bookmark",
            "dependency failure degrades only the index",
            "timeout reported as ambiguous",
            "reconciliation",
            "idempotency key",
            "recovery completes the pending index",
            "optimistic concurrency",
            "survives a full service restart",
            "correlates HTTP",
            "metrics recorded",
            "secrets redacted",
            "clean shutdown",
        ):
            self.assertIn(expected, steps, f"missing checkpoint: {expected}")

    def test_walkthrough_states_inference_limits(self):
        limits = " ".join(self.result["inference_limits"])
        self.assertIn("loopback", limits)
        self.assertIn("single-node", limits)


if __name__ == "__main__":
    unittest.main()
