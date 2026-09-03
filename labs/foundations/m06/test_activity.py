"""Unit tests for M06 Process & Execution Context Activity.

Verifies:
1. Process identity extraction.
2. Procfs PID equality on Linux.
3. fork semantics + ordinary-variable separation + wait status.
4. exec image replacement preserves PID and parent reaps exit status.
5. Controlled zombie cleanup, with environment-sensitive observation.
6. Linux scheduler-state sampling, with bounded non-observation reported as skip.
7. strace capability/trace truthfulness.
"""

import os
import platform
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fork_exec_fixture import (
    is_fork_supported,
    observe_controlled_zombie,
    run_exec_lifecycle,
    run_fork_lifecycle,
)
from process_observer import get_process_identity, inspect_procfs, observe_syscall
from scheduler_fixture import is_procfs_supported, run_scheduler_observation


class ProcessIdentityTests(unittest.TestCase):
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


class ForkExecLifecycleTests(unittest.TestCase):
    def test_fork_lifecycle_on_posix(self):
        if not is_fork_supported():
            self.skipTest(f"os.fork not supported on {platform.system()}")
        res = run_fork_lifecycle()
        self.assertTrue(res["supported"])
        self.assertEqual(res["child_pid"], res["fork_returned_pid"])
        self.assertTrue(res["ordinary_variable_copy_separate"])
        self.assertEqual(res["parent_var_after_fork"], 100)
        self.assertEqual(res["child_var_after_mutation"], 999)
        self.assertTrue(res["exit_code_matches"])
        self.assertEqual(res["exit_code"], 42)

    def test_exec_replaces_image_preserves_pid(self):
        if not is_fork_supported():
            self.skipTest(f"os.fork not supported on {platform.system()}")
        res = run_exec_lifecycle()
        self.assertTrue(res["supported"])
        self.assertTrue(res["pid_preserved_across_exec"], res["output"])
        self.assertEqual(res["exec_reported_pid"], res["fork_child_pid"])
        self.assertTrue(res["exit_code_matches"])
        self.assertEqual(res["exit_code"], 7)

    def test_zombie_observation_and_reap(self):
        if not is_fork_supported() or not is_procfs_supported():
            self.skipTest("fork or /proc not supported")
        res = observe_controlled_zombie()
        self.assertTrue(res["supported"])
        self.assertTrue(res["reaped"])
        if not res["zombie_observed"]:
            self.skipTest(
                f"Linux zombie state was not observed in the bounded polling window; "
                f"last state={res['observed_state']}"
            )
        self.assertEqual(res["observed_state"], "Z")


class SchedulerStateTests(unittest.TestCase):
    def test_scheduler_states_on_linux(self):
        if not is_fork_supported() or not is_procfs_supported():
            self.skipTest("fork or /proc not supported")
        res = run_scheduler_observation(sample_duration=1.0)
        self.assertTrue(res["supported"])
        if not res["cpu_showed_running_or_runnable"]:
            self.skipTest(f"Linux 'R' not observed for CPU worker: {res['observed_cpu_states']}")
        if not res["sleep_showed_interruptible_sleep"]:
            self.skipTest(f"Linux 'S' not observed for sleeping worker: {res['observed_sleep_states']}")
        self.assertIn("R", res["observed_cpu_states"])
        self.assertIn("S", res["observed_sleep_states"])


class SyscallObservationTests(unittest.TestCase):
    def test_syscall_detection_structure(self):
        res = observe_syscall()
        self.assertIn("status", res)
        self.assertIn(res["status"], ("PASS", "RESTRICTED", "UNAVAILABLE", "FAILED"))
        if res["status"] == "PASS":
            self.assertIn("write(", res["stderr_trace"])
            self.assertIn("SYSCALL_PROBE_OK", res["stderr_trace"])
        else:
            self.assertIn("fallback_note", res)
            self.assertIn("NO LIVE SYSCALL TRACE", res["fallback_note"])


if __name__ == "__main__":
    unittest.main()
