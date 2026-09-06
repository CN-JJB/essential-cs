#!/usr/bin/env python3
"""
test_m19.py
Essential CS: Stage 6 Module 19 (M19) Unit Test Suite.

Verifies:
1. Canonical Linux namespace and cgroup inspector logic (OSPreflight, NamespaceInspector,
   CgroupInspector, CapabilityGate).
2. Cloud availability and physical fiber propagation formulas (Activity L19-02).
3. Deployment simulation: broken version skew vs. protected Expand-Contract (Activity L19-03).
4. Mutable tag repointing and cryptographic trust boundary analysis.
5. Fail-closed idempotent reset functionality.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add current directory to path
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
            self.assertEqual(pre["disposition"], "REQUIRED CAPABILITY PASS")

    def test_parse_ns_symlink(self):
        # Valid symlinks
        ns_type, inode = inspector.NamespaceInspector.parse_ns_symlink("net:[4026531992]")
        self.assertEqual(ns_type, "net")
        self.assertEqual(inode, 4026531992)

        ns_type, inode = inspector.NamespaceInspector.parse_ns_symlink("pid_for_children:[4026531836]")
        self.assertEqual(ns_type, "pid_for_children")
        self.assertEqual(inode, 4026531836)

        # Invalid or non-namespace symlink
        ns_type, inode = inspector.NamespaceInspector.parse_ns_symlink("/usr/bin/python3")
        self.assertIsNone(ns_type)
        self.assertIsNone(inode)

    def test_namespace_inspector_nonexistent_dir(self):
        with tempfile.TemporaryDirectory(prefix="m19_test_nonexistent_") as tmpdir:
            res = inspector.NamespaceInspector.inspect(proc_dir=os.path.join(tmpdir, "nonexistent"))
            self.assertFalse(res["available"])
            self.assertEqual(res["disposition"], "ENVIRONMENT-BLOCKED / NOT RUN")
            self.assertEqual(res["namespace_count"], 0)

    def test_namespace_inspector_synthetic_fixture(self):
        """
        Verifies dynamic namespace discovery without freezing a fixed count.
        """
        with tempfile.TemporaryDirectory(prefix="m19_test_proc_") as tmpdir:
            ns_dir = Path(tmpdir) / "self" / "ns"
            ns_dir.mkdir(parents=True)

            # Create mock namespace symlinks
            # Note: on Windows, creating symlinks may require privileges, so test readlink handling
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

            # Create v2 /proc/self/cgroup line
            with open(str(proc_self / "cgroup"), "w", encoding="utf-8") as f:
                f.write("0::/user.slice/user-1000.slice/session-1.scope\n")

            # Create /proc/mounts with cgroup2
            with open(str(Path(tmpdir) / "mounts"), "w", encoding="utf-8") as f:
                f.write("cgroup2 /sys/fs/cgroup cgroup2 rw,nosuid,nodev,noexec,relatime 0 0\n")

            # Create /sys/fs/cgroup/cgroup.controllers
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

            # Create v1 /proc/self/cgroup lines
            with open(str(proc_self / "cgroup"), "w", encoding="utf-8") as f:
                f.write("2:memory:/user.slice\n1:cpu,cpuacct:/\n")

            # Create /proc/mounts with v1 cgroups
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

    def test_capability_signals_and_unshare_probe(self):
        signals = inspector.CapabilityGate.inspect_signals()
        self.assertIn("unprivileged_userns_clone_present", signals)
        self.assertIn("signal_note", signals)

        # probe_unshare_capability should report a truthful disposition without unhandled crash
        probe_res = inspector.CapabilityGate.probe_unshare_capability()
        self.assertIn(probe_res["disposition"], {"CAPABILITY PASS", "ENVIRONMENT-BLOCKED / NOT RUN"})


class TestCloudAvailabilityCalculations(unittest.TestCase):
    def test_annual_downtime_minutes(self):
        self.assertEqual(activity_l19_02.calculate_annual_downtime(100.0), 0.0)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.0), 5256.0, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.9), 525.6, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.99), 52.56, places=2)
        self.assertAlmostEqual(activity_l19_02.calculate_annual_downtime(99.999), 5.256, places=2)

        with self.assertRaises(ValueError):
            activity_l19_02.calculate_annual_downtime(101.0)

    def test_parallel_availability(self):
        # Two nodes with 90% availability: A = 1 - 0.1 * 0.1 = 0.99
        self.assertAlmostEqual(activity_l19_02.calculate_parallel_availability(0.9, 0.9), 0.99)
        # Two nodes with 99% availability: A = 1 - 0.01 * 0.01 = 0.9999
        self.assertAlmostEqual(activity_l19_02.calculate_parallel_availability(0.99, 0.99), 0.9999)

        with self.assertRaises(ValueError):
            activity_l19_02.calculate_parallel_availability(-0.1, 0.9)

    def test_serial_availability(self):
        # 3 components in series: 0.99 * 0.99 * 0.99 = 0.970299
        res = activity_l19_02.calculate_serial_availability([0.99, 0.99, 0.99])
        self.assertAlmostEqual(res, 0.970299, places=6)

    def test_fiber_propagation_floor(self):
        res = activity_l19_02.calculate_fiber_propagation_floor(100.0)
        self.assertEqual(res["distance_km"], 100.0)
        # Speed of light in fiber is approx 204,000 km/s -> ~0.49 ms one-way, ~0.98 ms RTT
        self.assertGreater(res["rtt_propagation_floor_ms"], 0.9)
        self.assertLess(res["rtt_propagation_floor_ms"], 1.1)
        self.assertIn("real_network_overhead_factors", res)

    def test_cloud_architecture_evaluation(self):
        scenario = {
            "web_instance_availability": 0.99,
            "db_primary_availability": 0.999,
            "db_standby_availability": 0.999,
            "load_balancer_availability": 0.9999,
            "inter_az_distance_km": 30.0,
            "inter_region_distance_km": 3800.0,
        }
        res = activity_l19_02.evaluate_cloud_architecture(scenario)
        self.assertIn("web_tier_redundant_availability", res)
        self.assertIn("critical_shared_dependencies_omitted", res)
        self.assertTrue(len(res["critical_shared_dependencies_omitted"]) >= 4)


class TestDeploymentAndVersionSkew(unittest.TestCase):
    def test_breaking_rolling_deployment_simulation(self):
        breaking = activity_l19_03.simulate_breaking_rolling_deployment()
        self.assertGreater(breaking["total_requests"], 0)
        # During the version skew window, v1 nodes must fail because column was renamed
        self.assertGreater(breaking["failed_requests"], 0)
        self.assertGreater(breaking["failure_rate_pct"], 0.0)
        self.assertIn("no such column: phone", str(breaking["version_skew_window_requests"]))

    def test_expand_contract_deployment_simulation(self):
        protected = activity_l19_03.simulate_expand_contract_deployment()
        self.assertEqual(protected["failed_requests"], 0)
        self.assertEqual(protected["failure_rate_pct"], 0.0)
        self.assertTrue(protected["invariant_satisfied"])
        self.assertIn("Expand-Contract", protected["scenario"])

    def test_tag_vs_digest_and_trust(self):
        demo = activity_l19_03.simulate_tag_vs_digest()
        tag_demo = demo["tag_demonstration"]
        self.assertTrue(tag_demo["tag_repointed_and_mutable"])
        self.assertNotEqual(tag_demo["target_at_t0"], tag_demo["target_at_t1"])

        trust = demo["trust_boundary_analysis"]
        self.assertIn("what_digest_does_NOT_guarantee", trust)
        self.assertTrue(len(trust["what_digest_does_NOT_guarantee"]) >= 3)


class TestResetIdempotence(unittest.TestCase):
    def test_reset_passes_twice_cleanly(self):
        # Create a dummy scratch file
        scratch_dir = CURRENT_DIR / ".scratch"
        scratch_dir.mkdir(parents=True, exist_ok=True)
        test_file = scratch_dir / "test_scratch.tmp"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("temporary data")

        # First run removes it
        reset.reset_m19_environment(verbose=False)
        self.assertFalse(test_file.exists())

        # Second run succeeds without error
        reset.reset_m19_environment(verbose=False)
        self.assertFalse(scratch_dir.exists())


if __name__ == "__main__":
    unittest.main()
