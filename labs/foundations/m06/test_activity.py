"""Unit tests for M06 Process & Execution Context Activity.

Verifies:
1. Process identity extraction (os.getpid).
2. Procfs parsing and PID equality (on Linux).
3. Fork lifecycle and exit status reaping (where os.fork is supported).
4. Controlled zombie observation and guaranteed reaping.
5. Scheduler states (Running 'R' vs Sleeping 'S').
6. Clean, leak-free process management.
"""

import os
import platform
import sys
import unittest
from pathlib import Path

# Ensure local fixtures are importable regardless of working directory
sys.path.insert(0, str(Path(__file__).parent))

from fork_exec_fixture import is_fork_supported, observe_controlled_zombie, run_fork_lifecycle
from process_observer import get_process_identity, inspect_procfs, observe_syscall
from scheduler_fixture import is_procfs_supported, run_scheduler_observation


class ProcessIdentityTests(unittest.TestCase):
    """Tests basic process identity attributes."""

    def test_identity_fields(self):
        ident = get_process_identity()
        self.assertIsInstance(ident["pid"], int)
        self.assertGreater(ident["pid"], 0)
        self.assertIn("platform", ident)

    def test_procfs_pid_equality_on_linux(self):
        proc = inspect_procfs()
        if not proc["procfs_available"]:
            self.skipTest(f"procfs not available: {proc['reason']}")

        self.assertTrue(proc["pid_matches"])
        self.assertEqual(proc["status_pid"], os.getpid())
        self.assertIn("state", proc)
        self.assertIn("vmsize", proc)


class ForkLifecycleTests(unittest.TestCase):
    """Tests fork semantics, variable isolation, and wait status."""

    def test_fork_lifecycle_on_posix(self):
        if not is_fork_supported():
            self.skipTest(f"os.fork not supported on {platform.system()}")

        res = run_fork_lifecycle()
        self.assertTrue(res["supported"])
        self.assertEqual(res["child_pid"], res["fork_returned_pid"])
        self.assertTrue(res["memory_isolated"])
        self.assertEqual(res["parent_var_after_fork"], 100)
        self.assertEqual(res["child_var_after_mutation"], 999)
        self.assertTrue(res["exit_code_matches"])
        self.assertEqual(res["exit_code"], 42)

    def test_zombie_observation_and_reap(self):
        if not is_fork_supported() or not is_procfs_supported():
            self.skipTest("fork or /proc not supported")

        res = observe_controlled_zombie()
        self.assertTrue(res["supported"])
        self.assertTrue(res["reaped"])
        # On Linux, state prior to wait should be 'Z'
        self.assertEqual(res["observed_state"], "Z")
        self.assertTrue(res["zombie_observed"])


class SchedulerStateTests(unittest.TestCase):
    """Tests running vs waiting process state detection."""

    def test_scheduler_states_on_linux(self):
        if not is_fork_supported() or not is_procfs_supported():
            self.skipTest("fork or /proc not supported")

        res = run_scheduler_observation(sample_duration=1.0)
        self.assertTrue(res["supported"])
        self.assertTrue(
            res["cpu_showed_running"],
            f"CPU worker did not show 'R': {res['observed_cpu_states']}",
        )
        self.assertTrue(
            res["sleep_showed_sleeping"],
            f"Sleeping worker did not show 'S': {res['observed_sleep_states']}",
        )


class SyscallObservationTests(unittest.TestCase):
    """Tests strace detection and fallback reporting."""

    def test_syscall_detection_structure(self):
        res = observe_syscall()
        self.assertIn("status", res)
        self.assertIn(res["status"], ("PASS", "RESTRICTED", "UNAVAILABLE"))
        if res["status"] != "PASS":
            self.assertIn("fallback_trace", res)
            self.assertTrue(len(res["fallback_trace"]) > 0)


if __name__ == "__main__":
    unittest.main()
