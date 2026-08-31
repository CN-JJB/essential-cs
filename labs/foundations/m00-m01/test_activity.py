import subprocess
import sys
import unittest
from pathlib import Path

import activity
import change
import reset
from opaque_store import load_payload

HERE = Path(__file__).resolve().parent
EXPECTED_BASELINE_HEX = "45 43 53 31 01 02 fe ff 04 00 41 e4 b8 ad"
EXPECTED_CHANGED_HEX = "45 43 53 31 01 02 fe ff 04 00 41 e6 96 87"


class ActivityTests(unittest.TestCase):
    def setUp(self) -> None:
        reset.main()

    def tearDown(self) -> None:
        reset.main()

    def test_baseline_exact_bytes_and_round_trip(self) -> None:
        result = activity.run_once(quiet=True)
        self.assertEqual(activity.hex_bytes(result["payload"]), EXPECTED_BASELINE_HEX)
        self.assertEqual(result["decoded"], result["record"])
        self.assertEqual(len(result["payload"]), 14)

    def test_utf8_exact_bytes(self) -> None:
        self.assertEqual("A中".encode("utf-8"), bytes.fromhex("41 e4 b8 ad"))
        self.assertEqual("A文".encode("utf-8"), bytes.fromhex("41 e6 96 87"))

    def test_explicit_endian_encode_decode(self) -> None:
        self.assertEqual(activity.encode_uint16(513, "little"), bytes.fromhex("01 02"))
        self.assertEqual(activity.encode_uint16(513, "big"), bytes.fromhex("02 01"))
        self.assertEqual(activity.decode_uint16(bytes.fromhex("01 02"), "little"), 513)
        self.assertEqual(activity.decode_uint16(bytes.fromhex("02 01"), "big"), 513)
        self.assertEqual(activity.decode_uint16(bytes.fromhex("02 01"), "little"), 258)

    def test_signed_ranges_and_twos_complement_bytes(self) -> None:
        self.assertEqual(activity.encode_int16(-2, "big"), bytes.fromhex("ff fe"))
        self.assertEqual(activity.decode_int16(bytes.fromhex("ff fe"), "big"), -2)
        with self.assertRaises(ValueError):
            activity.encode_uint16(65536, "little")
        with self.assertRaises(ValueError):
            activity.encode_int16(32768, "little")

    def test_controlled_change_then_reset(self) -> None:
        baseline = activity.run_once(quiet=True)["payload"]
        change.main()
        changed = activity.run_once(quiet=True)["payload"]
        self.assertEqual(activity.hex_bytes(changed), EXPECTED_CHANGED_HEX)
        self.assertNotEqual(changed, baseline)
        reset.main()
        restored = activity.run_once(quiet=True)["payload"]
        self.assertEqual(restored, baseline)

    def test_opaque_boundary_can_return_saved_record(self) -> None:
        result = activity.run_once(quiet=True)
        self.assertEqual(load_payload(), result["payload"])
        self.assertEqual(activity.deserialize_record(load_payload()), result["record"])

    def test_cli_break_utf8_is_safe_and_deterministic(self) -> None:
        completed = subprocess.run(
            [sys.executable, "activity.py", "break-utf8"],
            cwd=HERE,
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("break.utf8.error=UnicodeDecodeError", completed.stdout)

    def test_cli_break_record_rejects_truncation(self) -> None:
        completed = subprocess.run(
            [sys.executable, "activity.py", "break-record"],
            cwd=HERE,
            check=True,
            text=True,
            capture_output=True,
        )
        self.assertIn("break.record.original_bytes=14", completed.stdout)
        self.assertIn("break.record.truncated_bytes=13", completed.stdout)
        self.assertIn("break.record.error=ValueError", completed.stdout)
        self.assertIn("record length does not match text_len", completed.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
