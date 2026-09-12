# Foundations M19 Evidence Template — Modern Infrastructure: Containers, Cloud Topology & Safe Delivery

Use this template for **one actual learner observation**. Do not prefill or copy another learner's timestamps, namespace inode numbers, cgroup controllers, downtime derivations, or simulation test pass markers.

---

## A — Environment Capabilities & Preflight

- Execution commit / ref: `[Record actual HEAD commit SHA]`
- Host Operating System / kernel / platform: `[Record actual OS and architecture]`
- Python Implementation & Version: `[Record actual Python version]`
- Canonical Linux Environment Status: `[Record observed Linux presence and /proc access]`
- Required Read-Only Capability Disposition: `[Record REQUIRED CAPABILITY PASS or ENVIRONMENT-BLOCKED / NOT RUN]`
- Optional `unshare` Extension Disposition: `[Record CAPABILITY PASS, ENVIRONMENT-BLOCKED, or NOT RUN]`
- OQ-BP-006 Environment Policy Status: `CLOSED (technical environment-definition/realization per #167; #158 re-check still required)`

---

## B — Linux Namespaces: View Partitioning (EC-CON-013 Isolation)

- `/proc/self/ns` Read-Only Inspection Status: `[Record observed inspection disposition]`
- Detected Active Namespace Handles:
  `[Record table or list of namespace types and actual symlink targets / inodes observed from /proc/self/ns/*]`
- Parent Process Namespace Comparison (if readable):
  `[Record comparison outcome between self and parent process namespace IDs]`
- Access / Block Reason (if restricted or non-Linux):
  `[Record reason if namespace inspection was blocked]`
- Mechanism Inference Limit:
  `[Learner explains what namespace inode matching proves about view partitioning, and what security properties namespaces do NOT provide]`

---

## C — Linux Cgroups: Resource Quotas & Accounting

- `/proc/self/cgroup` Evidence:
  `[Record lines read from /proc/self/cgroup]`
- Detected Hierarchy Arrangement:
  `[Record detected cgroup arrangement: cgroup_v2, cgroup_v1, hybrid, or unreadable]`
- Controllers Actually Observed:
  `[Record controllers present in /sys/fs/cgroup/cgroup.controllers or mounted v1 controllers]`
- Confirmation of Zero Host Mutation:
  `[Learner confirms zero writes were performed to /sys/fs/cgroup]`
- Quota vs. View Distinction:
  `[Learner contrasts Cgroups resource limits (e.g. memory.max, cpu.max) with Namespace view partitioning]`

---

## D — Process vs. Container vs. Virtual Machine Boundary

- Kernel Boundary Analysis:
  `[Learner articulates why canonical Linux containers share the host kernel while VMs run independent guest kernels]`
- Hardware Emulation & Virtualization:
  `[Learner identifies the role of hypervisors and hardware-assisted virtualization vs. kernel namespaces]`
- Isolation & Security Boundary (EC-CON-013 Isolation):
  `[Learner explains why container root without user namespaces shares the host kernel attack surface]`
- Security Claims Not Established by Read-Only Core:
  `[Learner lists why namespace/cgroup inspection alone does not prove a complete container security posture]`

---

## E — OCI Image / Runtime / Storage Boundary

- OCI Image Specification Source & Currentness:
  `[Record official OCI Image Spec version, release date, and URL checked]`
- OCI Runtime Specification Source & Currentness:
  `[Record official OCI Runtime Spec version, release date, and URL checked]`
- Image Artifact vs. Running Container Distinction:
  `[Learner explains the difference between an OCI image manifest/layer blob and a running process bundle]`
- Storage Driver Mechanism Boundary:
  `[Learner explains why OverlayFS is one Linux runtime storage driver, not an invariant requirement of the OCI specification]`

---

## F — Tag vs. Content Digest vs. Cryptographic Trust Boundaries (EC-CON-017 Trust Boundary)

- Tag / Reference Before & After Mapping in Course Scenario:
  `[Record tag name, target digest at T0, and target digest at T1 from simulation]`
- Content Digest Computation:
  `[Record calculated content digest and hash algorithm used]`
- Four-Part Trust Boundary Analysis:
  `[Learner articulates why: digest identity/integrity evidence != signature verification != provenance/attestation != trust policy decision]`
- Verification Prerequisite:
  `[Learner explains why content digest verification requires comparing against an expected digest received via a trusted channel]`

---

## G — Cloud Provider Source Audit (EC-CON-010 Failure)

- Named Cloud Provider Audited:
  `[Record provider name, e.g. AWS or Google Cloud]`
- Official Current Region / Zone Documentation Source:
  `[Record document title, official URL, and audit date]`
- Provider-Defined Failure Domain Claim:
  `[Record how the audited provider explicitly defines Region and Zone / Availability Zone]`
- Non-Universal Scope & Shared Dependencies:
  `[Learner explains why provider region/zone definitions are provider-specific logical failure domains, not universal physical hierarchies]`

---

## H — Availability Mathematics & Physical Latency Floors (EC-CON-006 Trade-off)

- Scenario Mathematical Inputs:
  `[Record component availability values used in the evaluation scenario]`
- Parallel Redundancy Derivation:
  - Formula Applied: `[Record formula, e.g. A = 1 - (1-a1)(1-a2)]`
  - Stated Scenario Assumptions: `[Record independence and substitutable capacity assumptions]`
  - Modeled System Availability Result: `[Record calculated availability percentage and annual downtime minutes]`
- Serial Dependency Ceiling:
  `[Learner explains why a shared serial component constrains overall system availability: A_system <= min(A_i)]`
- Optical Fiber Physical Propagation Floor:
  - Propagation Model Parameters: `[Record modeled propagation speed and delay per km]`
  - Evaluated Path Lower Bounds: `[Record calculated one-way and RTT propagation floors for modeled scenario distances]`
- Provider SLA Boundary:
  `[Learner records the named provider/service SLA source if one is used, then explains why its specific measurement/remedy terms are not automatically an independent per-instance failure probability]`

---

## I — Deployment Strategies & Version Skew (The Broken Path)

- Rolling Deployment Simulation Execution:
  `[Record execution of activity_l19_03.py breaking path]`
- Breaking Schema Action:
  `[Record the uncoordinated schema modification performed]`
- Observed Version-Skew Error Spike:
  - Total Requests in Skew Window: `[Record count]`
  - Failed Requests (HTTP 500): `[Record count]`
  - Observed Failure Rate %: `[Record percentage]`
- Root Cause Diagnosis:
  `[Learner quotes the exact SQL error and explains why surviving v1 instances crashed on live traffic]`

---

## J — Expand-Contract Safe Migration (The Protected Path)

- Simulation Lifecycle Execution:
  `[Record execution of activity_l19_03.py protected path]`
- Phase 1 (Expand) Actions:
  `[Record additive schema change and initial backfill]`
- Phase 2 (Transition / Coexistence) Verification:
  - Cross-Version Compatibility: `[Record observed result of V2 reading V1 write]`
  - Dual-Write Verification: `[Record observed result of V1 reading V2 dual-write]`
  - Coexistence Requests Evaluated: `[Record count]`
- Phase 3 (Contract) Actions:
  `[Record removal of deprecated column after 100% adoption of V2Final]`
- Phase 4 (Post-Contract) Verification:
  - Requests Evaluated on Contracted Schema: `[Record count of reads and writes evaluated post-contract]`
- Overall Invariant & Scope:
  - Total Requests Evaluated Across All Phases: `[Record total request count]`
  - Observed Error Rate %: `[Record observed percentage]`
  - Scenario-Specific Inference Scope: `[Learner explains why 0 errors in this deterministic test is not a universal zero-downtime guarantee]`

---

## K — Cleanup, Competencies, Concepts & Visuals

- Idempotent Cleanup Verification:
  `[Record outcome of running reset.py twice consecutively]`
- Primary Competencies Exercised:
  `[Learner notes specific activities exercising Explain, Judge, Trace, Estimate, Diagnose]`
- Concepts Formally Revisited:
  `[Learner notes revisits to EC-CON-013, EC-CON-018, EC-CON-002, EC-CON-006, EC-CON-010, EC-CON-005, EC-CON-017]`
- Visual Artifact Review:
  `[Learner confirms review of FIG-M19-01, FIG-M19-02, and FIG-M19-03]`
- Authoritative Source Recheck:
  `[Record dates and status for Linux, OCI Image Spec v1.1.1, OCI Runtime Spec v1.3.0, and cloud provider documentation]`
