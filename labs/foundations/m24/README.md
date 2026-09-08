# M24 Fixtures — Final System Defense & Pre-Ship Assessment

This directory contains **course-owned, standard-library-only structural fixtures** for M24. The validators are actual-system-agnostic. The bundled samples are **synthetic reference scenarios**, not learner evidence and not assertions about a real repository application.

## 1. Files

| File | Purpose | Boundary |
| :--- | :--- | :--- |
| `defense_validator.py` | Checks the 16 trace headings, Claim Register, E01–E12 traceability rows, unknown→learning-plan links, and unresolved placeholders | Does not judge architecture quality, artifact truth, evidence sufficiency, or learner PASS |
| `preship_validator.py` | Checks four risk classes, explicit risk-priority fields, compatibility/recovery rationale, and data-loss-bound fields | Does not prescribe a universal recovery strategy or authorize release |
| `activity_l24_01.py` | Audits a completed dossier or presents a changed-constraint prompt | Scenario cards provide facts/questions only; no answer is machine-selected |
| `activity_l24_02.py` | Audits a pre-ship JSON record and runs bounded SQLite DDL/query examples | Migration examples apply only to the exact DDL/query pair exercised |
| `sample_dossier.md` | Synthetic 16-trace / 12-area structural reference | NOT learner evidence; performance is explicitly NOT MEASURED |
| `sample_preship.json` | Synthetic risk-matrix schema reference | NOT a release decision or current production measurement |
| `reset.py` | Removes only M24-owned scratch/cache artifacts | Idempotent, bounded cleanup |
| `test_m24.py` | Standard-library unit tests for structural contracts | Machine tests do not award M24 competency PASS |

## 2. Safety

- No outbound network calls, cloud credentials, production targets, destructive production migrations, or stress tests.
- Samples are synthetic. A learner must replace scenario assumptions with evidence from the **actual system under defense**.
- No arbitrary percentage grade, universal SLO, universal data-loss promise, universal rollback strategy, or predetermined changed-constraint answer.
- Runtime outcomes use PASS / FAIL / BLOCKED / NOT RUN truthfully. Learner/reviewer evidence is separate.

## 3. Commands

### Preflight
```bash
python tests/preflight_security_synthesis.py --module M24
```

### Audit the synthetic dossier
```bash
python labs/foundations/m24/activity_l24_01.py --dossier labs/foundations/m24/sample_dossier.md
```

### Present a changed-constraint prompt
```bash
python labs/foundations/m24/activity_l24_01.py --scenario SCENARIO_01_HIGH_LATENCY
```
The output supplies the changed assumption and learner/reviewer questions. It does **not** diagnose the bottleneck or prescribe the adaptation.

### Audit the synthetic pre-ship matrix
```bash
python labs/foundations/m24/activity_l24_02.py --matrix labs/foundations/m24/sample_preship.json
```

### Run SQLite compatibility examples
```bash
python labs/foundations/m24/activity_l24_02.py --simulate-migration
```
Interpret only the exact observed DDL/query relationship. Do not infer whole-application rollback safety from these examples.

### Tests and cleanup
```bash
python -m unittest labs/foundations/m24/test_m24.py
python labs/foundations/m24/reset.py
```
