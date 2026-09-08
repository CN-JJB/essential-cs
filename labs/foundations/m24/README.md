# M24 Lab Fixtures — Final System Defense & Pre-Ship Assessment

Welcome to the hands-on lab environment for **Module M24 — Final System Defense & Pre-Ship Assessment**.

This directory provides the authoritative, course-owned Python standard-library fixtures for validating Capstone Architectural Defense Dossiers, executing Changed-Constraint challenge drills, auditing pre-ship risk matrices, and simulating database schema migration compatibility.

---

## 1. Architectural Fixtures Overview

| File | Purpose | Corresponding Lesson | Key Concepts & Invariants |
| :--- | :--- | :--- | :--- |
| **`defense_validator.py`** | 16-Trace & 12-Evidence-Area structural audit | `L24-01` | Audits structural presence of all 16 traces and E01–E12 evidence mapping. Rejects unresolved placeholders (`[TODO]`). Confirms explicit unknowns and learning plans. Emits `STRUCTURAL_CHECK_PASS` only; machine checks never issue a learner PASS. |
| **`preship_validator.py`** | Pre-ship risk matrix & migration compatibility engine | `L24-02` | Validates classification across Must Measure, Must Test, Must Inspect, and Acceptable Unknown. Rejects naive claims ("100% test coverage = safe"). Audits code rollback vs schema evolution; simulates SQLite backward compatibility. |
| **`activity_l24_01.py`** | Architecture defense & changed-constraint drill | `L24-01` | Runnable CLI for auditing dossiers and running scenario drills (`SCENARIO_01_HIGH_LATENCY`, `SCENARIO_02_100X_DATA`, `SCENARIO_03_MALICIOUS_CLIENT`). |
| **`activity_l24_02.py`** | Pre-ship verification & schema evolution harness | `L24-02` | Runnable CLI for auditing candidate release risk matrices and simulating schema migration rollback vs roll-forward strategies. |
| **`sample_dossier.md`** | Reference single-node defense dossier | `L24-01` | Authoritative example of a complete 16-trace dossier for the single-node Mini Cloud App (SQLite WAL, loopback HTTP, zero fake Raft/replicas). |
| **`sample_preship.json`** | Reference pre-ship risk matrix | `L24-02` | Authoritative example of a risk-prioritized pre-ship matrix with stated data-loss bounds and additive schema rollback justification. |
| **`reset.py`** | Fail-closed idempotent cleanup | Maintenance | Safely removes course-owned `.scratch/` observation files and Python cache without touching source code. |
| **`test_m24.py`** | Verification test suite | Module Gate | Standard library `unittest` suite testing all structural validation, migration simulation, and boundary enforcement rules. |

---

## 2. Safety & Bounded Execution Guarantees

1. **Zero External Dependencies**: Operates entirely on Python standard library modules (`dataclasses`, `sqlite3`, `json`, `re`, `pathlib`, `unittest`).
2. **Zero Live Network Calls**: No outbound internet traffic, no remote cloud API probes, no production deployment targets.
3. **Grounded in Actual System Reality**: All architectural claims and scenario drills are grounded in the learner's actual system (e.g. single-node Mini Cloud App with SQLite WAL). Zero fabricated Raft consensus, fake replicas, or simulated cloud clusters.
4. **No Universal Constants or Arbitrary Grades**: The validators reject arbitrary percentage scoring (e.g. "85% passing grade"). Machine tooling enforces structural completeness; final learner pass and evidence sufficiency remain strictly human reviewer-required.
5. **Fail-Closed Cleanup**: Transient files are confined to `.scratch/` and cleaned up safely via `reset.py`.

---

## 3. How to Run

### Step 1: Preflight Capability Check
Run the Stage 7 preflight probe for Module M24:
```bash
python tests/preflight_security_synthesis.py --module M24
```

### Step 2: Audit Sample Architecture Defense Dossier
```bash
python labs/foundations/m24/activity_l24_01.py --dossier labs/foundations/m24/sample_dossier.md
```
Observe the verification of all 16 traces, 12 evidence areas, declared claims, and zero placeholder tokens.

### Step 3: Run Changed-Constraint Challenge Drill
```bash
python labs/foundations/m24/activity_l24_01.py --scenario SCENARIO_01_HIGH_LATENCY
```
Inspect the diagnosis of bottleneck shifts (thread pool exhaustion under 200ms WAN latency) and the required architectural adaptations.

### Step 4: Audit Pre-Ship Risk Matrix
```bash
python labs/foundations/m24/activity_l24_02.py --matrix labs/foundations/m24/sample_preship.json
```
Verify the four mandatory risk classes (Must Measure, Must Test, Must Inspect, Acceptable Unknown) and stated data-loss bounds.

### Step 5: Simulate Database Schema Evolution
```bash
python labs/foundations/m24/activity_l24_02.py --simulate-migration
```
Observe the three migration scenarios: additive nullable (rollback safe), destructive rename (rollback forbidden), and destructive NOT NULL without default (fails closed).

### Step 6: Run Automated Unit Tests
```bash
python -m unittest labs/foundations/m24/test_m24.py
```

### Step 7: Idempotent Environment Reset
```bash
python labs/foundations/m24/reset.py
```
