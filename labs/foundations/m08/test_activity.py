#!/usr/bin/env python3
"""Automated machine-checkable test suite for M08 lab packet.

Verifies:
- L08-01: File identity, hard link equality, open-unlink lifetime semantics, and /proc/self/fd.
- L08-02: User-space write buffering, strace capability reporting, meminfo dirty page observation,
          and machine-checked durability boundary audit.
- L08-03: Deterministic ENOENT, capability-gated EACCES handling, safe bounded ENOSPC model,
          and diagnostic triage mapping.
- Workspace cleanup and reset verification.
"""

import errno
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add current directory to path for imports
HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from file_identity import get_file_identity, inspect_proc_fd, run_identity_experiment
from buffered_io_observer import (
    check_durability_boundary_claim,
    check_strace_capability,
    observe_dirty_pages_directional,
    observe_user_space_buffering,
    read_proc_meminfo,
    trace_buffered_syscalls,
)
from io_failure_fixture import (
    BoundedSpaceWriter,
    classify_io_failure,
    is_privileged_user,
    reproduce_bounded_enospc,
    reproduce_eacces,
    reproduce_enoent,
)
from reset import reset_m08_workspace


class TestL0801FileIdentity(unittest.TestCase):
    """L08-01: File identity, hard-link sharing, and open-unlink reference lifetime."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="_test_m08_id_")
        self.work_path = Path(self.temp_dir)

    def tearDown(self):
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_hard_link_shares_inode_and_device(self):
        src = self.work_path / "test_src.txt"
        link = self.work_path / "test_link.txt"
        src.write_text("hard link identity content", encoding="utf-8")

        os.link(src, link)
        s_src = get_file_identity(src)
        s_link = get_file_identity(link)

        self.assertEqual(s_src["inode"], s_link["inode"], "Hard link must share identical inode number")
        self.assertEqual(s_src["device"], s_link["device"], "Hard link must reside on identical device")
        self.assertEqual(s_src["nlink"], 2, "Link count must increment to 2")
        self.assertEqual(s_link["nlink"], 2, "Link count must be 2 on hard link")

    def test_open_unlink_continued_access_and_reclaim(self):
        target = self.work_path / "ephemeral.txt"
        target_link = self.work_path / "ephemeral_link.txt"
        initial_data = b"Persistent data in open kernel file description\n"
        target.write_bytes(initial_data)

        os.link(target, target_link)
        fd = os.open(target, os.O_RDWR)

        # Inspect proc fd if on Linux
        p_fd = inspect_proc_fd(fd)
        if p_fd["available"]:
            self.assertIsNotNone(p_fd["target"])

        # Unlink both names so nlink drops to 0
        os.unlink(target)
        self.assertFalse(target.exists())
        self.assertTrue(target_link.exists())

        os.unlink(target_link)
        self.assertFalse(target_link.exists())

        # Check /proc/self/fd shows (deleted) if on Linux
        p_fd_deleted = inspect_proc_fd(fd)
        if p_fd_deleted["available"] and p_fd_deleted["target"] is not None:
            self.assertTrue(p_fd_deleted["is_deleted_marked"] or "deleted" in p_fd_deleted["target"])

        # Read back initial content from open descriptor
        os.lseek(fd, 0, os.SEEK_SET)
        read_back = os.read(fd, len(initial_data))
        self.assertEqual(read_back, initial_data)

        # Write new content to unlinked inode
        new_data = b"New bytes written while unlinked\n"
        n_written = os.write(fd, new_data)
        self.assertEqual(n_written, len(new_data))

        os.lseek(fd, 0, os.SEEK_SET)
        total_read = os.read(fd, len(initial_data) + len(new_data))
        self.assertEqual(total_read, initial_data + new_data)

        # Close descriptor
        os.close(fd)

    def test_run_identity_experiment_runner(self):
        report = run_identity_experiment()
        v = report["verifications"]
        self.assertTrue(v["same_inode"])
        self.assertTrue(v["same_device"])
        self.assertTrue(v["nlink_incremented_on_link"])
        self.assertTrue(v["nlink_decremented_on_unlink"])
        self.assertTrue(v["both_pathnames_removed"])
        self.assertTrue(v["open_fd_io_succeeded"])


class TestL0802BufferedIO(unittest.TestCase):
    """L08-02: User-space write buffering, strace truthfulness, meminfo, and durability audit."""

    def test_user_space_buffering_and_size_integrity(self):
        rep = observe_user_space_buffering(num_chunks=512, chunk_size=32)
        v = rep["verifications"]
        self.assertTrue(v["buffered_bytes_match"])
        self.assertTrue(v["unbuffered_bytes_match"])
        self.assertEqual(rep["buffered_file_bytes_on_disk"], 512 * 32)
        self.assertEqual(rep["unbuffered_file_bytes_on_disk"], 512 * 32)

        with self.assertRaises(ValueError):
            observe_user_space_buffering(num_chunks=1024 * 1024, chunk_size=2)

    def test_durability_boundary_audit(self):
        dur = check_durability_boundary_claim()
        self.assertFalse(
            dur["durability_proven_by_ordinary_write"],
            "Machine check: ordinary write success must NEVER be asserted as proving durability",
        )
        self.assertTrue(dur["durability_check_passed"])
        self.assertEqual(dur["canonical_home_module"], "M09")
        self.assertEqual(dur["canonical_home_lesson"], "L09-01")
        self.assertEqual(dur["canonical_concept_id"], "EC-CON-016")

    def test_proc_meminfo_dirty_handling(self):
        mem = read_proc_meminfo()
        if mem["available"]:
            self.assertIsInstance(mem["dirty_kb"], int)
            self.assertIsInstance(mem["writeback_kb"], int)

        # Bounded directional observation
        with self.assertRaises(ValueError):
            observe_dirty_pages_directional(size_mb=9)

        d_rep = observe_dirty_pages_directional(size_mb=4)
        if d_rep["status"] == "PASS":
            self.assertEqual(d_rep["size_written_mb"], 4)
            self.assertIsNotNone(d_rep["dirty_before_kb"])
            self.assertIsNotNone(d_rep["dirty_after_kb"])
        else:
            self.assertEqual(d_rep["status"], "SKIP")

    def test_strace_capability_and_truthful_trace(self):
        cap = check_strace_capability()
        self.assertIn(cap["status"], ["PASS", "RESTRICTED", "MISSING", "ERROR"])

        s_rep = trace_buffered_syscalls()
        if cap["status"] == "PASS":
            self.assertEqual(s_rep["status"], "PASS")
            self.assertTrue(s_rep["batched_relation_confirmed"])
            self.assertLess(s_rep["detected_write_syscalls"], 1000)
        else:
            self.assertEqual(s_rep["status"], "SKIP")
            self.assertEqual(s_rep["disposition"], "NO LIVE SYSCALL TRACE")


class TestL0803IOFailureFixture(unittest.TestCase):
    """L08-03: POSIX error reproduction, capability gating, and bounded capacity model."""

    def test_deterministic_enoent(self):
        rep = reproduce_enoent()
        self.assertEqual(rep["status"], "PASS")
        self.assertEqual(rep["errno"], errno.ENOENT)
        self.assertEqual(rep["errno_name"], "ENOENT")
        self.assertIn("Path lookup invariant", rep["broken_invariant"])

    def test_capability_gated_eacces(self):
        rep = reproduce_eacces()
        self.assertIn(rep["status"], ["PASS", "SKIP"])
        if rep["status"] == "PASS":
            self.assertEqual(rep["disposition"], "REPRODUCED")
            self.assertFalse(rep["mode_bit_denial_bypassed"])
            self.assertEqual(rep["errno"], errno.EACCES)
            self.assertEqual(rep["errno_name"], "EACCES")
        else:
            self.assertEqual(rep["disposition"], "ENVIRONMENT-LIMITED")
            self.assertTrue(rep["mode_bit_denial_bypassed"])
            self.assertIn("0444", rep["reason"])
            # euid==0 is metadata only; the actual write probe decides disposition.
            self.assertIn("euid_is_zero", rep)

    def test_bounded_enospc_model_and_partial_writes(self):
        # 1. Direct device testing
        dev = BoundedSpaceWriter(capacity_bytes=256)
        with self.assertRaises(ValueError):
            BoundedSpaceWriter(capacity_bytes=1024 * 1024 + 1)
        n1 = dev.write_raw(b"A" * 200)
        self.assertEqual(n1, 200)
        self.assertEqual(dev.remaining_bytes, 56)

        # Partial write
        n2 = dev.write_raw(b"B" * 100)
        self.assertEqual(n2, 56)
        self.assertEqual(dev.remaining_bytes, 0)

        # Exhausted -> raises ENOSPC
        with self.assertRaises(OSError) as ctx:
            dev.write_raw(b"C")
        self.assertEqual(ctx.exception.errno, errno.ENOSPC)

        # 2. Higher-level runner testing
        rep = reproduce_bounded_enospc(capacity_bytes=512)
        self.assertEqual(rep["status"], "PASS")
        self.assertEqual(rep["evidence_type"], "DETERMINISTIC_MODEL_EVIDENCE")
        self.assertTrue(rep["partial_write_occurred"])
        self.assertTrue(rep["enospc_raised_when_full"])
        self.assertEqual(rep["observed_errno"], errno.ENOSPC)
        self.assertEqual(rep["errno_name"], "ENOSPC")

    def test_diagnostic_triage_classification(self):
        c_enoent = classify_io_failure(errno.ENOENT)
        self.assertEqual(c_enoent["name"], "ENOENT")
        self.assertIn("Naming", c_enoent["subsystem"])

        c_eacces = classify_io_failure(errno.EACCES)
        self.assertEqual(c_eacces["name"], "EACCES")
        self.assertIn("Security", c_eacces["subsystem"])

        c_enospc = classify_io_failure(errno.ENOSPC)
        self.assertEqual(c_enospc["name"], "ENOSPC")
        self.assertIn("Capacity", c_enospc["subsystem"])

        c_ebadf = classify_io_failure(errno.EBADF)
        self.assertEqual(c_ebadf["name"], "EBADF")


class TestResetAndWorkspace(unittest.TestCase):
    """Workspace cleanup verification."""

    def test_reset_cleans_workspace(self):
        ret = reset_m08_workspace()
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
