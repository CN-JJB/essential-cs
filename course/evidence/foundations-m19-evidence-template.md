# Foundations M19 Evidence Template — Modern Infrastructure: Containers, Cloud Topology & Safe Delivery

Use this template for **one actual learner observation**. Do not prefill or copy another learner's timestamps, namespace inode numbers, cgroup controllers, downtime derivations, or simulation test pass markers.

---

## A — Environment Capabilities & Execution Ref

- Execution commit / ref: `<actual HEAD commit SHA>`
- Host Operating System: `<actual OS and architecture>`
- Canonical Linux Environment: `<True / False>`
- Python Implementation & Version: `<actual Python version>`
- Local Writable Scratch Capability: `<PASS / FAIL / BLOCKED>`
- Preflight Distributed Infra M19 Status: `<READY / ENVIRONMENT-BLOCKED / NOT RUN>`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED`

---

## B — Linux Namespaces: View Partitioning (EC-CON-013 Isolation)

- `/proc/self/ns` Read-Only Inspection Status: `<PASS / ENVIRONMENT-BLOCKED / NOT RUN>`
- Detected Active Namespace Handles:
  - `cgroup`: `<actual inode or N/A>`
  - `ipc`: `<actual inode or N/A>`
  - `mnt`: `<actual inode or N/A>`
  - `net`: `<actual inode or N/A>`
  - `pid`: `<actual inode or N/A>`
  - `pid_for_children`: `<actual inode or N/A>`
  - `time`: `<actual inode or N/A>`
  - `user`: `<actual inode or N/A>`
- Child Process Inode Comparison:
  - Did child in same namespace share identical inode numbers? `<YES / NO / N/A>`
  - Mechanism Reflection:
    `<Learner explains why matching inode numbers prove shared namespace view, and what namespace isolation does NOT prevent>`

---

## C — Linux Cgroups: Resource Quotas & Accounting

- Cgroup Arrangement Detected: `<cgroup_v2 / cgroup_v1 / hybrid_unknown / ENVIRONMENT-BLOCKED>`
- Unified Hierarchy Root Present: `<True / False / N/A>`
- Active / Available Controllers Observed:
  `<Learner lists actual controllers present in /sys/fs/cgroup/cgroup.controllers or N/A>`
- Current Process Cgroup Membership:
  `<Learner records entry from /proc/self/cgroup>`
- Quota vs. View Distinction:
  `<Learner contrasts Cgroups resource limits (memory.max, cpu.max, pids.max) with Namespace view partitioning>`

---

## D — Capability-Gated Namespace Creation Extension

- Probe Method Attempted: `unshare(CLONE_NEWUSER | CLONE_NEWPID)`
- Probe Execution Disposition: `<PASS / ENVIRONMENT-BLOCKED / NOT RUN>`
- Child PID Observed Inside New Namespace: `<1 / N/A>`
- Actual Error / Limitation (if blocked): `<PermissionError / EPERM / Unsupported / N/A>`
- Privilege Invariant:
  `<Learner explains why missing privilege or non-Linux host must remain ENVIRONMENT-BLOCKED rather than converted to PASS>`

---

## E — Process vs. Container vs. Virtual Machine Boundary

- Boundary Matrix Evaluation:
  - Kernel Sharing: `<Learner states which abstractions share the host kernel>`
  - Hardware Virtualization / Hypervisor: `<Learner identifies where hypervisor isolation exists>`
  - Isolation Boundary: `<Learner articulates why containers are host processes with view/resource limits, not VMs>`
  - Security Blast Radius:
    `<Learner explains why a container root process without user namespaces shares the host kernel attack surface>`

---

## F — Availability 'Nines' & Downtime Mathematics

- Basis: Non-leap calendar year = 525,600 minutes
- Downtime Derivations:
  - 99.0% (2 nines): `<actual calculated minutes>` (equivalent days)
  - 99.9% (3 nines): `<actual calculated minutes>` (equivalent hours)
  - 99.95%: `<actual calculated minutes>` (equivalent hours)
  - 99.99% (4 nines): `<actual calculated minutes>` (equivalent minutes)
  - 99.999% (5 nines): `<actual calculated minutes>` (equivalent minutes)
- Mathematical Invariant:
  `<Learner explains why downtime decreases by an order of magnitude with each added 'nine'>`

---

## G — Parallel Redundancy Math vs. Shared Dependencies

- Single Instance Modeled Availability: `<e.g. 99.0%>`
- Dual Independent Parallel Instance Modeled Availability:
  - Formula: $A = 1 - (1 - a_1)(1 - a_2)$
  - Result: `<e.g. 99.99%>`
- Shared Upstream Dependency Evaluated (e.g. Load Balancer / DNS):
  - Upstream Availability: `<e.g. 99.9%>`
  - System Availability Ceiling: `<Learner derives why system availability cannot exceed 99.9%>`
- Common-Mode Failure Analysis:
  `<Learner lists at least 3 common-mode failures (e.g. poison config, rack PDU, shared DB) that invalidate independent failure assumptions>`

---

## H — Fiber Optic Propagation Floors (Speed of Light in Silica)

- Physical Constants:
  - Vacuum speed of light ($c$): $\approx 299,792\,\text{km/s}$
  - Single-mode silica fiber refractive index ($n$): $\approx 1.4682$
  - Fiber speed of light ($v$): $\approx 204,190\,\text{km/s} \approx 204.2\,\text{km/ms}$
  - Propagation delay lower bound: $\approx 0.004897\,\text{ms/km} \approx 5\,\mu\text{s/km}$
- Evaluated Topology RTT Lower Bounds:
  - Metro Adjacent AZs (30 km): `<actual calculated theoretical RTT ms>`
  - Cross-Zone Edge (100 km): `<actual calculated theoretical RTT ms>`
  - Trans-Continental (3,800 km): `<actual calculated theoretical RTT ms>`
  - Trans-Atlantic (5,500 km): `<actual calculated theoretical RTT ms>`
  - Trans-Pacific (8,700 km): `<actual calculated theoretical RTT ms>`
- Distributed Consistency Consequence:
  `<Learner explains why Multi-Region synchronous consensus (e.g. cross-continent Raft) cannot beat the fiber RTT floor>`

---

## I — Cloud Failure Domains & Architectural Trade-off

- Topology Selected for Scenario: `<Single-AZ / Multi-AZ / Multi-Region>`
- Justification (EC-CON-006 Trade-off):
  - Blast Radius Handled: `<Rack / Datacenter / Regional>`
  - Latency Penalty Incurred: `<ms penalty>`
  - Data Transfer / Egress Cost Trade-off: `<Learner notes financial impact of cross-AZ / cross-region traffic>`
- Cloud SLA vs. MTBF Distinction:
  `<Learner explains why a cloud provider SLA is a commercial billing credit policy, not a guarantee that an individual VM will not reboot>`

---

## J — Rolling Deployment Version Skew (The Broken Path)

- Simulation Run: `activity_l19_03.py` (Part 1)
- Breaking Schema Action: `Immediate column rename (phone -> contact_phone)`
- Total Requests Evaluated during Skew Window: `<count>`
- Successful Requests (HTTP 200): `<count>`
- Failed Requests (HTTP 500): `<count>`
- Observed Error Spike: `<percentage>`
- Crash Diagnosis:
  `<Learner quotes the exact SQL error and explains why surviving v1 instances failed>`

---

## K — Expand-Contract (Parallel Run) Safe Migration (The Protected Path)

- Simulation Run: `activity_l19_03.py` (Part 2)
- Phase 1 (Expand) Actions:
  `<Learner records additive nullable column and dual-write behavior>`
- Phase 2 (Transition / Rolling Update) Actions:
  `<Learner records rolling deployment of v2 instances with fallback-read and dual-write>`
- Phase 3 (Contract) Actions:
  `<Learner records removal of legacy column after 100% v2 adoption>`
- Transition Window Request Evaluation:
  - Total Transition Requests: `<count>`
  - Total Failures: `<0>`
  - Transition Error Rate: `<0.0%>`
- Invariant Judgment:
  `<Learner explains what Expand-Contract proves for this deterministic scenario, and why it does not guarantee universal zero-downtime under unhandled concurrent mutations>`

---

## L — OCI Content Digest vs. Mutable Tag & Cryptographic Trust

- Tag Mutation Observed:
  - Tag Name: `<e.g. payment-service:v1.0>`
  - Digest at T0: `<sha256:...>`
  - Digest at T1: `<sha256:...>`
  - Mutation Demonstrated: `<YES / NO>`
- Immutability Boundary:
  `<Learner explains why tags are mutable pointers while digests bind exact manifest bits>`
- Trust Boundary Analysis (EC-CON-017 Trust Boundary):
  - What Digest Guarantees: `<Integrity / Tamper Detection>`
  - What Digest Does NOT Guarantee: `<Authorship / Provenance / Pipeline Integrity / Malicious Intent>`
  - Required Trust Infrastructure: `<Cryptographic Signatures (Cosign/Sigstore) + SLSA Provenance Attestations>`
