# M19 Foundations Activities: Modern Infrastructure, Cloud Topology & Safe Delivery

This directory contains executable, course-owned fixtures and worked-trace harnesses for Module M19.

## Core Boundary Rules

- **Zero Container Runtimes Required**: Strictly no Docker, Podman, containerd, Kubernetes, or cloud provider accounts required to execute Core activities or verify invariants.
- **Strictly Read-Only Observation**: Core Linux container deconstruction uses read-only inspection of `/proc/self/ns` and `/proc/self/cgroup`. Zero mutations of host namespaces or cgroup files are performed.
- **Truthful Non-Linux Disposition**: On non-Linux host platforms (Windows/macOS), the environment is truthfully classified as `ENVIRONMENT-BLOCKED / NOT RUN`. The inspector/activity CLI exits non-zero when Required Core mechanism evidence is unavailable; process exit success is never used to disguise a blocked semantic result. To record Required Core evidence for L19-01, execution must take place inside a canonical Linux environment (native Linux, WSL2, or a Linux VM).
- **Physical Availability & Latency Lower-Bounds**: Mathematical models demonstrate the speed-of-light propagation floor in optical fiber and the series-component availability ceiling under shared single points of failure.
- **Zero-Downtime Myth Busted**: Deterministic simulations demonstrate rolling deployment version-skew crashes under uncoordinated database schema renames, and verify the multi-phase Expand-Contract pattern.

## Files Overview

1. **`s6_m19_ns_cgroup_inspector.py`**
   - **OSPreflight**: Checks platform OS, kernel version, and verifies read-only access to `/proc/self/ns` and `/proc/self/cgroup`.
   - **NamespaceInspector**: Dynamically discovers active namespaces without freezing a fixed count; inspects target symlinks and numeric inodes; safely compares with parent process.
   - **CgroupInspector**: Classifies cgroup hierarchy (`cgroup_v2`, `cgroup_v1`, `hybrid`, or `unavailable`); lists enabled v2/v1 controllers; inspects self cgroup path.
   - **CapabilityGate**: Heuristically checks distro sysctl signals and executes a safe, bounded unshare capability probe in an owned child process (reaped cleanly).

2. **`activity_l19_01.py`**
   - Runs the L19-01 container deconstruction inspection.
   - Walks through host preflight, namespace view partitioning, cgroup resource quotas, and the architectural boundary comparison (Host Process vs. Container vs. Virtual Machine).
   - Generates `.scratch/l19_01_observation.json`.

3. **`activity_l19_02.py`**
   - Evaluates availability "nines" and converts percentages to annual downtime minutes.
   - Computes parallel redundancy math and highlights why $A = 1 - (1-a_1)(1-a_2)$ collapses when components share hidden dependencies.
   - Computes a course-owned optical propagation lower-bound model for explicitly labeled illustrative path lengths; outputs are not provider RTT, zone distance, or SLA claims.
   - Generates `.scratch/l19_02_worksheet.json`.

4. **`activity_l19_03.py`**
   - **Breaking Rolling Update**: Simulates a 3-instance service pool where an uncoordinated column rename causes version-skew SQL crashes on live customer traffic during the rolling rollout window.
   - **Protected Expand-Contract**: Executes the course-owned Expand-Contract fixture across coexistence and post-contract phases; its observed zero errors are scoped to this deterministic scenario only.
   - **Digest vs. Tag**: Demonstrates a course-owned repointable tag/reference map versus content digests, while making real registry tag policy explicit and separating digest identity, signature verification, provenance/attestation, and trust-policy decisions.
   - Generates `.scratch/l19_03_deployment.json`.

5. **`reset.py`**
   - Fail-closed, idempotent cleanup removing `.scratch/` and local `__pycache__/`.

6. **`test_m19.py`**
   - Automated test suite verifying inspector components, mock fixtures, availability math, deployment simulations, and reset idempotence.

## Running the Activities

```bash
# 1. Preflight check for M19 Core capabilities
python tests/preflight_distributed_infra.py --module m19

# 2. Run L19-01 hands-on activity (Container Deconstruction)
python labs/foundations/m19/activity_l19_01.py

# 3. Run L19-02 hands-on activity (Cloud Topology & Availability)
python labs/foundations/m19/activity_l19_02.py

# 4. Run L19-03 hands-on activity (Deployment Strategies & Version Skew)
python labs/foundations/m19/activity_l19_03.py

# 5. Run automated test suite
python -m unittest discover -s labs/foundations/m19 -p "test_*.py"

# 6. Clean up temporary artifacts (idempotent, safe to run repeatedly)
python labs/foundations/m19/reset.py
```
