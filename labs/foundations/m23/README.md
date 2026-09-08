# M23 Lab Fixtures — Systems Thinking & Judgment

Welcome to the hands-on lab environment for **Module M23 — Systems Thinking & Judgment**.

This directory provides the authoritative, course-owned Python standard-library fixtures for empirical systems measurement, technology evaluation (Decision D-015), and bounded capacity/cost modeling.

---

## 1. Architectural Fixtures Overview

| File | Purpose | Corresponding Lesson | Key Concepts & Invariants |
| :--- | :--- | :--- | :--- |
| **`activity_l23_01.py`** | Question-driven measurement & coordinated omission harness | `L23-01` | Compares uncoordinated synchronous loops with arrival-scheduled open arrival generators. Injects explicitly labeled synthetic pauses. Probes monotonic clock characteristics. |
| **`activity_l23_02.py`** | Decision D-015 Technology Evaluation & ADR validator | `L23-02` | Validates candidate technologies across all 12 dimensions of Decision D-015. Treats **REJECT** as a first-class valid decision category while keeping decision quality reviewer-required. Audits AI recommendations as unverified hypotheses. |
| **`fermi_cost.py`** | Bounded capacity planning, Fermi estimation & TCO modeling | `L23-03` | Enforces assumption-first arithmetic. Distinguishes bits vs Bytes (`b` vs `B`), decimal vs binary units (`KB` vs `KiB`), average vs peak egress, storage retention vs unbounded growth, and infra bill vs human operational TCO. |
| **`reset.py`** | Fail-closed idempotent cleanup | Maintenance | Safely removes course-owned `.scratch/` observation files and Python cache without touching source code. |
| **`test_m23.py`** | Verification suite | Module Gate | Standard library `unittest` suite testing mathematical and deterministic invariants across all M23 modules. |

---

## 2. Safety & Bounded Execution Guarantees

1. **Zero External Dependencies:** Runs entirely on the standard Python runtime (`math`, `time`, `json`, `dataclasses`, `unittest`).
2. **Zero Network Calls:** No outbound internet traffic, no live cloud API probes, no public benchmark targets.
3. **Local & Ephemeral:** Workload parameters are safety-capped and local; wall-clock runtime can still vary with host scheduling. No unbounded loops or stress-test intent.
4. **Synthetic Stall Transparency:** Pauses injected during latency experiments are explicitly documented as synthetic pauses, not claimed to be uninstrumented GC or OS scheduler pauses.
5. **No Universal Constants:** The fixtures reject universal rules of thumb (e.g., mandatory sample size of 30, universal p99 targets, or timeless cloud pricing). All metrics and decisions are bound to explicit engineering questions.

---

## 3. How to Run

### Step 1: Preflight Capability Check
Run the Stage 7 preflight probe for Module M23:
```bash
python tests/preflight_security_synthesis.py --module M23
```

### Step 2: Run L23-01 Latency Measurement
```bash
python labs/foundations/m23/activity_l23_01.py
```
Observe the comparative summary table between naive synchronous and arrival-scheduled generators under a 50ms synthetic pause.

### Step 3: Run L23-02 Technology Evaluation
```bash
python labs/foundations/m23/activity_l23_02.py
```
Audit the 12-dimension evaluation for Redis caching, Kafka message queues, and AI-suggested architectures. Observe that the three supplied synthetic scenarios are structurally complete and intentionally support `REJECT`; this is not a universal technology-winner rule.

### Step 4: Run L23-03 Capacity & Cost Modeling
```bash
python labs/foundations/m23/fermi_cost.py
```
Inspect the napkin-math resource estimates and bottleneck breakdown for a photo-sharing service.

### Step 5: Run Automated Unit Tests
```bash
python -m unittest labs/foundations/m23/test_m23.py
```

### Step 6: Idempotent Environment Reset
```bash
python labs/foundations/m23/reset.py
```
