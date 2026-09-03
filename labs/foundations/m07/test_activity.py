#!/usr/bin/env python3
"""test_activity.py - Essential CS M07 Automated Lab Suite.

Verifies:
1. L07-01: maps_observer parses procfs maps, identifies permissions dynamically
   without hardcoding memory addresses.
2. L07-02: residency_fixture executes bounded reservation, observes directional
   increase in RSS / minor page faults upon touching pages, and cleans up.
3. L07-03: fault_runner compiles bad_address.c, runs child with timeout, captures
   signal termination on hosted Linux, avoids shell exit 139 assumption, and cleans up.
"""

from __future__ import annotations

import os
import signal
import sys
import unittest
from pathlib import Path

# Add current directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import fault_runner
import maps_observer
import residency_fixture


class TestL0701MapsObserver(unittest.TestCase):
    """Verifies virtual memory mapping inspection."""

    def test_parse_maps_synthetic_lines(self) -> None:
        # Synthetic sample line from x86-64 Linux
        sample_line = (
            "55ea1b65e000-55ea1b685000 r-xp 00000000 08:02 1048602 /usr/bin/python3.12\n"
        )
        entry = maps_observer.parse_maps_line(sample_line)
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry.start_addr, 0x55EA1B65E000)
        self.assertEqual(entry.end_addr, 0x55EA1B685000)
        self.assertEqual(entry.perms, "r-xp")
        self.assertTrue(entry.is_readable)
        self.assertFalse(entry.is_writable)
        self.assertTrue(entry.is_executable)
        self.assertTrue(entry.is_private)
        self.assertFalse(entry.is_shared)
        self.assertEqual(entry.pathname, "/usr/bin/python3.12")
        self.assertFalse(entry.is_anonymous)

        # Synthetic anonymous mapping line
        anon_line = "7f1b2c000000-7f1b2c021000 rw-p 00000000 00:00 0 \n"
        anon_entry = maps_observer.parse_maps_line(anon_line)
        self.assertIsNotNone(anon_entry)
        assert anon_entry is not None
        self.assertTrue(anon_entry.is_writable)
        self.assertFalse(anon_entry.is_executable)
        self.assertTrue(anon_entry.is_anonymous)

    def test_live_maps_inspection(self) -> None:
        if not os.path.exists("/proc/self/maps"):
            self.skipTest("/proc/self/maps is not available on this host.")

        entries = maps_observer.read_maps("/proc/self/maps")
        self.assertGreater(len(entries), 0, "Expected at least one mapping entry.")

        # Confirm dynamically identified permissions without hardcoded addresses
        exec_entries = [e for e in entries if e.is_executable]
        writable_entries = [e for e in entries if e.is_writable]

        self.assertGreater(
            len(exec_entries),
            0,
            "Expected at least one executable mapping (code segment).",
        )
        self.assertGreater(
            len(writable_entries),
            0,
            "Expected at least one writable mapping (data/heap/stack).",
        )

        # Check summarize function
        summary = maps_observer.summarize_mappings(entries)
        self.assertEqual(summary["total_mappings"], len(entries))
        self.assertGreater(summary["total_virtual_kb"], 0)


class TestL0702ResidencyFixture(unittest.TestCase):
    """Verifies virtual reservation vs physical residency directional relationships."""

    def test_bounded_residency_behavior(self) -> None:
        # Use a safe, bounded allocation of 8 MiB for the test
        test_alloc_bytes = 8 * 1024 * 1024
        res = residency_fixture.run_residency_experiment(alloc_bytes=test_alloc_bytes)

        baseline = res["baseline"]
        reserved = res["reserved"]
        fully_touched = res["fully_touched"]

        # 1. Virtual memory reservation check
        if reserved.vm_size_kb is not None and baseline.vm_size_kb is not None:
            # Reservation must increase or keep virtual size >= baseline
            self.assertGreaterEqual(
                reserved.vm_size_kb,
                baseline.vm_size_kb,
                "Virtual reservation should expand or maintain process VmSize.",
            )

        # 2. Resident set size directional check
        if fully_touched.vm_rss_kb is not None and reserved.vm_rss_kb is not None:
            # Touching pages must cause physical frame allocation (RSS growth)
            self.assertGreaterEqual(
                fully_touched.vm_rss_kb,
                reserved.vm_rss_kb,
                "Touching pages must directionally increase or maintain VmRSS.",
            )

        # 3. Minor page faults directional check
        if fully_touched.minor_faults is not None and reserved.minor_faults is not None:
            self.assertGreaterEqual(
                fully_touched.minor_faults,
                reserved.minor_faults,
                "Touching newly mapped pages must trigger minor page faults in OS accounting.",
            )


class TestL0703FaultRunner(unittest.TestCase):
    """Verifies safe child-process memory fault observation and cleanup."""

    def setUp(self) -> None:
        fault_runner.cleanup_binary()

    def tearDown(self) -> None:
        fault_runner.cleanup_binary()

    def test_bad_address_compilation_and_signal(self) -> None:
        compiler_info = fault_runner.find_native_compiler()
        if not compiler_info:
            self.skipTest("No native C compiler (gcc/clang) available.")

        # Bounded child execution
        result = fault_runner.run_fault_child(
            fault_runner.BINARY_PATH, timeout=5.0
        )

        self.assertTrue(result.compiled, f"Compilation failed: {result.stderr}")
        self.assertFalse(result.timed_out, "Child process timed out unexpectedly.")

        # On Linux/x86-64 hosted execution, invalid dereference should terminate by signal
        if sys.platform.startswith("linux"):
            self.assertTrue(
                result.terminated_by_signal,
                f"Child process was expected to terminate via signal, got returncode={result.returncode}",
            )
            # Machine check negative returncode in Python subprocess
            self.assertLess(
                result.returncode,
                0,
                "Python subprocess should report negative returncode for signal termination.",
            )
            # Specifically check signal 11 (SIGSEGV)
            self.assertEqual(
                result.signal_number,
                int(signal.SIGSEGV),
                f"Expected SIGSEGV ({signal.SIGSEGV}), got {result.signal_number}",
            )
            self.assertEqual(result.signal_name, "SIGSEGV")


if __name__ == "__main__":
    unittest.main()
