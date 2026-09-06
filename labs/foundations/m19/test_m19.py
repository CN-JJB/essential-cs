#!/usr/bin/env python3
"""
test_m19.py
Essential CS: Stage 6 Module 19 (M19) Unit Test Suite.

Verifies:
1. Canonical Linux namespace, cgroup, and process status/limits inspector logic.
2. Cloud availability and physical fiber propagation lower-bound formulas (Activity L19-02).
3. Deployment simulation: broken version skew vs. protected Expand-Contract (Activity L19-03),
   including coexistence dual-writes and post-contract requests.
4. Mutable tag repointing and cryptographic trust boundary analysis.
5. Fail-closed idempotent reset functionality, including failure injection.
"""

import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import activity_l19_01
import activity_l19_02
import activity_l19_03
import reset
import s6_m19_ns_cgroup_inspector as inspector


class TestInspectorComponents(unittest.TestCase):
    def test_os_preflight_truthful(self):
        pre = inspector.OSPreflight.inspect()
        self.assertIn("platform_system", pre)
        self.assertIn("is_canonical_linux", pre)
        self.assertIn(
            pre["disposition"],
            {"REQUIRED CAPABILITY PASS", "ENVIRONMENT-BLOCKED / NOT RUN"},
        )
        if pre["is_canonical_linux"]:
            self.assertTrue(pre["proc_ns_readable"])
            self.assertTrue(pre["proc_cgroup_readable"])
            self.assertTrue(pre["mounts_readable"])
            self.assertTrue(pre["proc_status_readable"])
            self.assertTrue(pre["proc_limits_readable"])
            self.assertEqual(pre["disposition"], "REQUIRED CAPABILITY PASS")

    def test_parse_ns_symlink(self):
        ns_type, inode = inspector.NamespaceInspector.parse_ns_symlink("net:[4026531992]")
        self.assertEqual(ns_type, "net")
        self.assertEqual(inode, 4026531992)

        ns_type, inode = inspector.NamespaceInspector.parse_ns_symlink("pid_for_children:[4026531836]")
        self.assertEqual(ns_type, "pid_for_children")
        self.assertEqual(inode, 4026531836)

        ns_type, inode = inspector.NamespaceInspector.parse_ns_symlink("/usr/bin/python3")
        self.assertIsNone(ns_type)
        self.assertIsNone(inode)

    def test_namespace_inspector_nonexistent_dir(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_nonexistent_") as tmpdir:
            res = inspector.NamespaceInspector.inspect(proc_dir=os.path.join(tmpdir, "nonexistent"))
            self.assertFalse(res["available"])
            self.assertEqual(res["disposition"], "ENVIRONMENT-BLOCKED / NOT RUN")
            self.assertEqual(res["namespace_count"], 0)

    def test_namespace_inspector_empty_or_unreadable(self):
        """
        Verifies that an empty namespace directory reports available=False (Finding 9).
        """
        with tempfile.TemporaryDirectory(prefix="m19_test_empty_ns_") as tmpdir:
            ns_dir = Path(tmpdir) / "self" / "ns"
            ns_dir.mkdir(parents=True)
            res = inspector.NamespaceInspector.inspect(proc_dir=tmpdir)
            self.assertFalse(res["available"])
            self.assertEqual(res["disposition"], "ENVIRONMENT-BLOCKED / NOT RUN")

    def test_namespace_inspector_synthetic_fixture(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_proc_") as tmpdir:
            ns_dir = Path(tmpdir) / "self" / "ns"
            ns_dir.mkdir(parents=True)

            try:
                os.symlink("net:[4026531992]", str(ns_dir / "net"))
                os.symlink("pid:[4026531836]", str(ns_dir / "pid"))
                os.symlink("time:[4026531834]", str(ns_dir / "time"))
                symlinks_created = True
            except (OSError, NotImplementedError):
                symlinks_created = False

            if symlinks_created:
                res = inspector.NamespaceInspector.inspect(proc_dir=tmpdir)
                self.assertTrue(res["available"])
                self.assertEqual(res["disposition"], "REQUIRED CAPABILITY PASS")
                self.assertEqual(res["namespace_count"], 3)
                self.assertIn("net", res["namespaces_present"])
                self.assertEqual(res["namespaces_present"]["net"]["inode"], 4026531992)
                self.assertIn("time", res["namespaces_present"])

    def test_cgroup_inspector_synthetic_v2(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_cg_") as tmpdir:
            proc_self = Path(tmpdir) / "self"
            proc_self.mkdir(parents=True)

            with open(str(proc_self / "cgroup"), "w", encoding="utf-8") as f:
                f.write("0::/user.slice/user-1000.slice/session-1.scope\n")

            with open(str(Path(tmpdir) / "mounts"), "w", encoding="utf-8") as f:
                f.write("cgroup2 /sys/fs/cgroup cgroup2 rw,nosuid,nodev,noexec,relatime 0 0\n")

            sys_cg = Path(tmpdir) / "sys_mock" / "fs" / "cgroup"
            sys_cg.mkdir(parents=True)
            with open(str(sys_cg / "cgroup.controllers"), "w", encoding="utf-8") as f:
                f.write("cpuset cpu io memory pids\n")

            res = inspector.CgroupInspector.inspect(
                proc_dir=tmpdir,
                sys_dir=str(Path(tmpdir) / "sys_mock"),
            )
            self.assertTrue(res["available"])
            self.assertEqual(res["arrangement"], "cgroup_v2")
            self.assertEqual(res["cgroup_v2_controllers"], ["cpu", "cpuset", "io", "memory", "pids"])
            self.assertTrue(res["read_only_verified"])

    def test_cgroup_inspector_synthetic_v1(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_cg_v1_") as tmpdir:
            proc_self = Path(tmpdir) / "self"
            proc_self.mkdir(parents=True)

            with open(str(proc_self / "cgroup"), "w", encoding="utf-8") as f:
                f.write("2:memory:/user.slice\n1:cpu,cpuacct:/\n")

            with open(str(Path(tmpdir) / "mounts"), "w", encoding="utf-8") as f:
                f.write("cgroup /sys/fs/cgroup/memory cgroup rw,memory 0 0\n")
                f.write("cgroup /sys/fs/cgroup/cpu cgroup rw,cpu 0 0\n")

            res = inspector.CgroupInspector.inspect(
                proc_dir=tmpdir,
                sys_dir=str(Path(tmpdir) / "sys_mock"),
            )
            self.assertTrue(res["available"])
            self.assertEqual(res["arrangement"], "cgroup_v1")
            self.assertIn("memory", res["cgroup_v1_controllers"])

    def test_cgroup_inspector_unknown_arrangement_reports_unavailable(self):
        """
        Verifies that an unclassifiable cgroup arrangement returns available=False (Finding 9).
        """
        with tempfile.TemporaryDirectory(prefix="m19_test_cg_unknown_") as tmpdir:
            proc_self = Path(tmpdir) / "self"
            proc_self.mkdir(parents=True)
            with open(str(proc_self / "cgroup"), "w", encoding="utf-8") as f:
                f.write("malformed_line_without_colon\n")

            res = inspector.CgroupInspector.inspect(proc_dir=tmpdir)
            self.assertFalse(res["available"])
            self.assertEqual(res["arrangement"], "unknown")
            self.assertEqual(res["disposition"], "ENVIRONMENT-BLOCKED / NOT RUN")

    def test_process_status_inspector_synthetic(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_status_") as tmpdir:
            proc_self = Path(tmpdir) / "self"
            proc_self.mkdir(parents=True)

            with open(str(proc_self / "status"), "w", encoding="utf-8") as f:
                f.write("Name:\tpython3\nUid:\t1000\t1000\t1000\t1000\nGid:\t1000\t1000\t1000\t1000\nCapEff:\t0000000000000000\n")

            with open(str(proc_self / "limits"), "w", encoding="utf-8") as f:
                f.write("Limit                     Soft Limit           Hard Limit           Units\n")
                f.write("Max open files            1024                 1048576              files\n")
                f.write("Max processes             31024                31024                processes\n")

            res = inspector.ProcessStatusInspector.inspect(proc_dir=tmpdir)
            self.assertTrue(res["available"])
            self.assertEqual(res["disposition"], "REQUIRED CAPABILITY PASS")
            self.assertIn("Uid", res["status_fields"])
            self.assertIn("Max open files", res["limits_fields"])

    def test_capability_signals_and_unshare_probe(self):
        signals = inspector.CapabilityGate.inspect_signals()
        self.assertIn("unprivileged_userns_clone_present", signals)
        self.assertIn("signal_note", signals)

        probe_res = inspector.CapabilityGate.probe_unshare_capability()
        self.assertIn(probe_res["disposition"], {"CAPABILITY PASS", "ENVIRONMENT-BLOCKED / NOT RUN"})


class TestCloudAvailabilityCalculations(unittest.TestCase):
    def test_annual_downtime_minutes(self):
        self.assertEqual(activity_l19_02.calculate_annual_downtime(100.0), 0.0)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.0), 5256.0, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.9), 525.6, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.95), 262.8, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.99), 52.56, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.999), 5.256, places=2)

        with self.assertRaises(ValueError):
            activity_l19_02.calculate_annual_downtime(101.0)

    def test_parallel_availability(self):
        self.assertAlmostEqual(activity_l19_02.calculate_parallel_availability(0.9, 0.9), 0.99)
        self.assertAlmostEqual(activity_l19_02.calculate_parallel_availability(0.99, 0.99), 0.9999)

        with self.assertRaises(ValueError):
            activity_l19_02.calculate_parallel_availability(-0.1, 0.9)

    def test_serial_availability_bounded_by_minimum(self):
        res = activity_l19_02.calculate_serial_availability([0.99, 0.99, 0.99])
        self.assertAlmostEqual(res, 0.970299, places=6)
        self.assertLessEqual(res, 0.99)

        # When all other components are 1.0, system availability equals min
        res_with_ones = activity_l19_02.calculate_serial_availability([1.0, 0.95, 1.0])
        self.assertEqual(res_with_ones, 0.95)

    def test_fiber_propagation_floor(self):
        res = activity_l19_02.calculate_fiber_propagation_floor(100.0)
        self.assertEqual(res["modeled_distance_km"], 100.0)
        self.assertAlmostEqual(res["rtt_propagation_floor_ms"], 1.0, places=1)
        self.assertIn("real_network_overhead_factors", res)

    def test_cloud_architecture_evaluation(self):
        scenario = {
            "web_instance_availability": 0.99,
            "db_primary_availability": 0.999,
            "db_standby_availability": 0.999,
            "load_balancer_availability": 0.9999,
            "inter_zone_modeled_distance_km": 30.0,
            "inter_region_modeled_distance_km": 3800.0,
        }
        res = activity_l19_02.evaluate_cloud_architecture(scenario)
        avail = res["modeled_availability"]
        self.assertIn("web_tier_parallel_availability", avail)
        self.assertIn("omitted_shared_dependencies", res)
        self.assertIn("provider_sla_boundary", res)
        self.assertTrue(len(res["omitted_shared_dependencies"]) >= 4)


class TestDeploymentAndVersionSkew(unittest.TestCase):
    def test_breaking_rolling_deployment_simulation(self):
        breaking = activity_l19_03.simulate_breaking_rolling_deployment()
        self.assertGreater(breaking["total_requests"], 0)
        self.assertGreater(breaking["failed_requests"], 0)
        self.assertGreater(breaking["failure_rate_pct"], 0.0)
        self.assertIn("no such column: phone", str(breaking["version_skew_window_requests"]))

    def test_expand_contract_deployment_simulation_full_lifecycle(self):
        """
        Verifies that Expand-Contract exercises transition coexistence (cross-reads, dual-writes)
        and post-contract requests without errors, and includes post-contract requests in the invariant (Finding 7).
        """
        protected = activity_l19_03.simulate_expand_contract_deployment()
        self.assertGreater(protected["phase_2_coexistence_requests"], 0)
        self.assertGreater(protected["phase_4_post_contract_requests"], 0)
        self.assertEqual(protected["failed_requests"], 0)
        self.assertEqual(protected["failure_rate_pct"], 0.0)
        self.assertTrue(protected["invariant_satisfied"])
        self.assertEqual(protected["total_requests"], 24)

    def test_tag_vs_digest_and_trust_boundaries(self):
        demo = activity_l19_03.simulate_tag_vs_digest()
        tag_demo = demo["tag_demonstration"]
        self.assertTrue(tag_demo["tag_repointed_and_mutable"])
        self.assertNotEqual(tag_demo["target_at_t0"], tag_demo["target_at_t1"])

        tb = demo["trust_boundary_analysis"]
        self.assertIn("four_part_boundary_formula", tb)
        self.assertIn("digest_identity_evidence", tb)
        self.assertIn("signature_verification", tb)
        self.assertIn("provenance_attestation", tb)
        self.assertIn("trust_policy_decision", tb)


class TestResetIdempotenceAndFailClosed(unittest.TestCase):
    def test_reset_passes_twice_cleanly(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_reset_clean_") as tmpdir:
            test_file = Path(tmpdir) / "test_scratch.tmp"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("temporary data")

            # First run cleans it
            reset.reset_m19_environment(verbose=False, scratch_dir=tmpdir, pycache_dir=tmpdir)
            self.assertFalse(test_file.exists())

            # Second run succeeds idempotently
            reset.reset_m19_environment(verbose=False, scratch_dir=tmpdir, pycache_dir=tmpdir)

    def test_reset_fails_closed_on_deletion_error(self):
        """
        Injects a deletion failure and verifies that reset fails closed (raises RuntimeError)
        without reporting successful cleanup (Finding 12).
        """
        with tempfile.TemporaryDirectory(prefix="m19_test_reset_err_") as tmpdir:
            test_file = Path(tmpdir) / "test_scratch.tmp"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write("locked content")

            with patch("os.remove", side_effect=OSError("Simulated deletion permission denied")):
                with self.assertRaises(RuntimeError) as ctx:
                    reset.reset_m19_environment(verbose=False, scratch_dir=tmpdir, pycache_dir=tmpdir)
                self.assertIn("M19 cleanup incomplete", str(ctx.exception))
                self.assertIn("Simulated deletion permission denied", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
