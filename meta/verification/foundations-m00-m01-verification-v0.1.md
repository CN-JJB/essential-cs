# Foundations M00–M01 Technical Verification + Learner-Pilot Readiness v0.1

**Task:** EC-TASK-031 / Issue #31
**Role:** Independent Technical Verification Engineer / Learner-Pilot Readiness Reviewer
**Recommendation:** `READY FOR LEAD VERIFICATION REVIEW`

## 1. Verified target

### Exact target

- Assigned branch: `verification/issue-31-m00-m01-gate`
- Verified repository commit: `39e6ad3a1f872fdabdf312f4eb6892a3ca8b6243`
- GitHub branch comparison at verification start: branch and checked base were identical (`ahead_by=0`, `behind_by=0`, merge base `39e6ad3a...`).
- `main` was also `39e6ad3a...` at verification start, so no task staleness was observed.
- PR #30 learner-packet merge commit: `c187e80fe820c84ae66a0918756eb2a561be399b`.
- PR #32 then added status integration only; the verified `39e6ad3a...` target contains the PR #30 learner packet without a subsequent activity/Lesson change.

PR #30 merge did **not** make the learner packet `VERIFIED`. This verification task also does not self-promote the curriculum to `VERIFIED`.

### Relationship to Issue #29 / PR #30

Issue #29 / PR #30 produced the bounded M00–M01 learner-facing packet. Independent Web Lead review repaired three SIMPLE FIX findings before merge: the L00-02 debugger-light observable outcome, answer-first progressive-support risk, and narrow-layout Mermaid source risk. Those Lead fixes were Markdown-only; the activity implementation/tests were unchanged. GitHub exposes zero check runs for PR #30 head `d3545c83279536b6151602febb591d792e406411`.

### File/scope inventory verified

Learner Lessons:

- `book/00-the-map/L00-01.md`
- `book/00-the-map/L00-02.md`
- `book/01-information-representation/L01-01.md`
- `book/01-information-representation/L01-02.md`
- `book/01-information-representation/L01-03.md`
- `book/01-information-representation/L01-04.md`

Shared activity:

- `labs/foundations/m00-m01/.gitignore`
- `labs/foundations/m00-m01/README.md`
- `labs/foundations/m00-m01/activity.py`
- `labs/foundations/m00-m01/change.py`
- `labs/foundations/m00-m01/fixtures/baseline-input.json`
- `labs/foundations/m00-m01/input.json`
- `labs/foundations/m00-m01/opaque_store.py`
- `labs/foundations/m00-m01/reset.py`
- `labs/foundations/m00-m01/test_activity.py`

Existing evidence template:

- `course/evidence/foundations-m00-m01-evidence-template.md`

This verification PR adds only:

- `meta/verification/foundations-m00-m01-verification-v0.1.md`
- `course/evidence/foundations-m00-m01-pilot-observation-template.md`

## 2. Repository hygiene and execution constraints

A normal network clone was attempted with:

```bash
git clone https://github.com/CN-JJB/essential-cs.git /tmp/essential-cs-31
```

The local runner could not resolve `github.com`, so a fresh remote checkout was **BLOCKED** by DNS/network access. This is not reported as a checkout pass.

To keep runtime verification independent of PR #30's prior execution, the exact merged activity/test contents were fetched through the authenticated GitHub repository surface at commit `39e6ad3a...` and reconstructed in an isolated local Git working directory. That reconstruction is sufficient for the activity runtime and exact controlled-diff checks below, but it is **not equivalent to a full remote checkout**.

Literal Git hygiene checks performed on the local reconstruction:

```bash
git diff --check
```

- Before verification artifact authoring: PASS, exit 0.
- First post-authoring check: found four trailing-space lines in this new dossier; those authoring-only hygiene defects were removed immediately.
- Final handoff check: PASS, exit 0 after the two new files were included in the local diff.
- Limitation: these literal checks ran against the reconstructed verification working tree, not a network-cloned checkout of the complete remote branch.

Remote branch ancestry/base identity was independently checked through GitHub comparison and was exact (`39e6ad3a...` = branch head = merge base at start).

## 3. Environment matrix

| Environment actually used / attempted | OS | Arch | Python | Git | Shell / constraints | Result |
|---|---|---|---|---|---|---|
| Local isolated runtime reconstruction | Debian GNU/Linux 13 (trixie), kernel 6.18.35 | x86_64 | 3.13.5 | 2.47.3 | GNU bash 5.2.37; outbound DNS to GitHub unavailable; local filesystem/process execution available | **PASS for activity/runtime claims; PARTIAL for repository-checkout/canonical-environment claims** |
| Current Research/Design target | Ubuntu 24.04 LTS Noble | not run | Python 3.12 | not run | No Noble/Python 3.12 image/interpreter was available in this execution surface | **BLOCKED / NOT RUN** |

The exact Ubuntu 24.04 Noble + Python 3.12 target was therefore **not verified by this task**. No Dev Container, image pin, package pin, or environment Decision was introduced.

## 4. Commands and results

### Automated activity checks

From the reconstructed exact merged activity directory:

```bash
cd labs/foundations/m00-m01
python3 -m unittest -v test_activity.py
```

Result: **PASS — 8/8 tests**.

Compile/import surface:

```bash
python3 -m py_compile activity.py change.py reset.py opaque_store.py test_activity.py
```

Result: **PASS**.

Static import inventory observed:

```text
__future__, argparse, json, pathlib, typing,
shutil, subprocess, sys, unittest,
activity, change, reset, opaque_store
```

All non-local imports are Python standard-library modules. No network package/import or privileged-operation surface was found.

### Deterministic learner-visible path

Executed independently:

```text
reset
→ baseline run
→ inspect
→ debugger-light observation
→ one controlled change
→ git diff
→ changed run / inspect
→ reset
→ restored baseline
```

Meaningful evidence:

- `python3 reset.py` → `reset.ok input=baseline state=baseline`
- baseline run → `INPUT id=513 delta=-2 text='A中'`, `OUTPUT bytes=14 ...`, `ROUNDTRIP ok=True`
- baseline inspect → exact field offsets/sizes and UTF-8 bytes
- L00-02 debugger-light command:
  ```bash
  python3 -c 'import pdb, activity; pdb.runcall(activity.accept_record, activity.load_input())'
  ```
  At function entry the debugger stopped in `accept_record`; `p raw` showed:
  ```text
  {'id': 513, 'delta': -2, 'text': 'A中'}
  ```
  `c` continued normally.
- `python3 change.py` changed only `input.json` field `text: "A中" → "A文"`.
- literal `git diff -- input.json` showed exactly that one semantic line change.
- changed run remained 14 bytes and ended in `41 e6 96 87`.
- final `python3 reset.py` restored an empty `git diff -- input.json` and the exact baseline bytes.

The debugger check is verified **at runtime on Python 3.13.5**. Python 3.12 runtime verification remains unavailable; the official Python 3.12 `pdb.runcall` documentation nevertheless specifies that the debugger prompt appears as soon as the function is entered.

## 5. Expected-observation matrix

| Claim | Expected | Observed | Result | Evidence location |
|---|---|---|---|---|
| Baseline record | `id=513`, `delta=-2`, `text="A中"` | Exact values observed | PASS | `activity.py run`; `input.json` |
| Compact record field boundaries | magic 0/4; id 4/2; delta 6/2; text_len 8/2; text 10/4 | Exact offsets/sizes observed | PASS | `activity.py inspect` |
| Baseline total | 14 bytes | 14 bytes | PASS | `activity.py run`; test `test_baseline_exact_bytes_and_round_trip` |
| Baseline exact bytes | `45 43 53 31 01 02 fe ff 04 00 41 e4 b8 ad` | Exact match | PASS | `activity.py run`; `inspect`; unit test |
| Controlled change | `A中 → A文` only | Exact one-field Git diff | PASS | `change.py`; `git diff -- input.json` |
| Changed UTF-8 bytes | `41 e6 96 87` | Exact match | PASS | changed `activity.py inspect`; unit test |
| Changed total | remains 14 bytes | 14 bytes | PASS | changed `activity.py run` |
| Unsigned 16-bit range | `0..65535` | exact | PASS | `activity.py ranges` |
| Signed 16-bit range | `-32768..32767` | exact | PASS | `activity.py ranges` |
| `-2` two's-complement | bits `1111111111111110`, hex `fffe` | exact | PASS | `activity.py ranges`; unit test |
| 513 byte order | LE `01 02`; BE `02 01` | exact | PASS | `activity.py endian`; unit test |
| Wrong-order decode | BE bytes `02 01` decoded as LE → `258` | `258` | PASS | `activity.py break-endian`; unit test |
| Truncated UTF-8 | `41 e4 b8` rejected | `UnicodeDecodeError` | PASS | `activity.py break-utf8`; unit test |
| Valid encode/decode round trip | decoded record equals input record | `ROUNDTRIP ok=True` | PASS | baseline/changed run; unit test |
| Truncated record / declared-length mismatch | 14→13 byte truncation rejected | `ValueError: record length does not match text_len` | PASS | `activity.py break-record`; unit test |
| Deterministic reset | restored tracked input + baseline payload | exact baseline restored; input diff empty | PASS | `reset.py`; final run |
| Opaque save/load observation | later invocation may return supplied data, without durability claim | `LOAD id=513 delta=-2 text='A中'` plus explicit note that this is not proof of durability | PASS | `activity.py load`; README; L01-04 |

## 6. Static dependency / scope verification

| Constraint | Result | Evidence |
|---|---|---|
| Python stdlib or local modules only | PASS | AST/import inventory above |
| No third-party package requirement | PASS | no third-party imports/install steps |
| No network requirement | PASS | no network imports/calls; tests ran offline |
| No privileged-operation requirement | PASS | local file/process operations only |
| No new Required Lab | PASS | shared surface explicitly says it is not a Required Lab and has no Lab ID |
| No new Lesson IDs | PASS | only L00-01, L00-02, L01-01..04 in learner packet |
| No M02–M04 learner-facing implementation | PASS | no M02–M04 learner files introduced; references to M02 are stopping/defer markers only |
| Exactly eight canonical competencies | PASS | learner mappings use only Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, Learn-New-Tech |
| No ninth competency | PASS | no extra competency label found |
| Concept first homes unchanged | PASS | L00-01 matches EC-CON-001/002/004/005; L01-01 matches EC-CON-003; Specification/Invariant/Correctness remain M02 L02-03 |
| Open Questions remain open | PASS | OQ-BP-001, OQ-BP-003, OQ-BP-006 remain OPEN; packet does not decide them |
| No early database/storage/durability mechanism teaching | PASS | supplied persistence adapter remains conceptually opaque; learner prose explicitly defers durability/filesystem/database mechanisms |

P0 remains an integration surface rather than a curriculum DAG edge. The activity's supplied file-backed adapter is implementation detail behind the accepted opaque save/load boundary; the learner-facing packet does not use later retrieval as durability proof.

## 7. Technical source / provenance recheck

| Claim layer | Authoritative route rechecked | Verification result | Limitation / boundary |
|---|---|---|---|
| Unicode code point / scalar value / UTF-8 bytes | Unicode Standard 17.0, §3.9 (`https://www.unicode.org/versions/Unicode17.0.0/`) | PASS. UTF-8 assigns Unicode scalar values to 1–4 byte sequences; surrogate code points are excluded from scalar values. | Lesson correctly stops before grapheme segmentation/normalization depth. |
| Human-visible character vs code point | Unicode Standard + the packet's explicit grapheme stopping point | PASS. Packet does not equate code point count with general grapheme count. | `A中` is only a bounded example. |
| UTF-8 and host endianness | Unicode 17 Core Specification chapter 2 and Unicode UTF FAQ (`https://www.unicode.org/faq/utf_bom.html`) | PASS. UTF-8 uses 8-bit code units/bytes in defined sequence; host big/little endian reversal does not apply. | Endianness discussion for multibyte integers is kept separate. |
| C23 signed representation | WG14 official home (`https://open-std.org/jtc1/sc22/wg14/`) + WG14 N2888 (`https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2888.htm`) | PASS for the bounded source-layer example. WG14 identifies C23/ISO/IEC 9899:2024; N2888 explicitly records C23's two's-complement sign representation. | N2888 is proposal/history material, not a substitute for reproducing the full normative ISO text. The Lesson already labels it as specification history. |
| Representation vs signed arithmetic semantics | Accepted Research/Design boundary plus WG14 route above | PASS. Packet explicitly rejects “signed overflow always wraps” and does not infer language arithmetic semantics from representation. | This slice does not teach C overflow semantics. |
| Python integer byte conversion / explicit byte order | Python 3.12 `int.to_bytes` / `int.from_bytes` docs (`https://docs.python.org/3.12/library/stdtypes.html`) | PASS. Docs define explicit `big`/`little` ordering and `signed` behavior; fixture uses explicit byte order. | Runtime here was Python 3.13.5, not 3.12. |
| Python debugger-light behavior | Python 3.12 `pdb.runcall` docs (`https://docs.python.org/3.12/library/pdb.html`) | PASS at documentation layer; runtime behavior also reproduced on 3.13.5. Docs state prompt appears as soon as function is entered. | Exact 3.12 runtime execution remains unverified. |

The packet maintains evidence-layer discipline: Unicode/WG14 material supports specification/principle claims; Python documentation supports tool/API behavior; the local run supports this implementation/environment observation.

## 8. Technical review

### Accuracy

**PASS.** No technical contradiction was found in the fixed M00–M01 claims. In particular:

- information/text, code point, scalar-value applicability, encoded bytes, byte count, and visible-character stopping points are separated;
- UTF-8 is not described as following host integer endianness;
- finite signed/unsigned ranges and two's-complement representation are correct;
- representation is separated from language arithmetic semantics;
- “signed overflow always wraps” is explicitly rejected;
- explicit byte order is used in the Python implementation rather than host-order guessing.

### Activity / reproducibility

**PASS in the observed Debian 13 / Python 3.13.5 environment; PARTIAL across the intended environment family.** All automated checks and the full learner path reproduced. Exact Noble/Python 3.12 execution remains unestablished.

### Dependencies

**PASS.** Standard library/local modules only; offline; no privileged operation.

### Serialization / failure boundaries

**PASS.** Field layout, size, wrong byte order, truncated UTF-8, declared-length mismatch, and valid round trip behave as specified. The record failure check rejects a truncated payload based on the declared length before treating it as a successful record.

### P0 / durability boundary

**PASS.** The learner packet says only that a later invocation returned previously supplied data. It explicitly refuses to convert that observation into a durability guarantee and defers durability's canonical home.

## 9. Pedagogy / presentation-source review

### Six-Lesson structure

All six Lessons were reviewed for the required learner-facing loop. Every Lesson contains:

- learner question / why it matters;
- learning objective;
- prerequisites;
- Mental Model;
- Mechanism;
- prediction-before-reveal;
- a real Observe step;
- Explain;
- Judge;
- Common Misconceptions;
- What You Can Ignore—for Now;
- progressive stuck support;
- Exit Criteria;
- competency mapping;
- provenance.

Build/Break are present where justified by the lesson mechanism rather than mechanically forced into every Lesson.

### Progressive disclosure

**PASS at source level.**

Across six Lessons:

- 24 `<details>` opens and 24 matching closes;
- each Lesson presents a visible `Question` first;
- then closed disclosures in this order:
  `Hint 1 → Hint 2 → Expected Observation → Full Explanation`;
- no `<details open>` default was found;
- Full Explanation is therefore not displayed by default in ordinary HTML behavior.

This preserves the accepted support ladder and avoids answer-first static source.

### Mermaid / render review

**Source-level review only.** An actual target course renderer/browser render was not available in this execution surface.

Observed source inventory: **7 Mermaid diagrams** total.

- L00-01: bounded path + intentionally opaque save/load boundary.
- L00-02: evidence ladder; evidence/source-layer map.
- L01-01: one information → multiple representations.
- L01-03: UTF-8 layer/byte zoom; integer endianness.
- L01-04: round-trip pipeline and break points.

Each diagram carries mental-model/mechanism content; none is decorative-only. Node counts and Lead-compacted TB/LR layouts are bounded, and no M02–M04 mechanism leakage was found. Because the eventual renderer may treat Mermaid and `<details>` differently, narrow/mobile readability and disclosure behavior remain release-surface checks rather than claims made here.

### Learner-risk observations

No curriculum defect is asserted from source inspection alone. Remaining pilot risks worth observing:

- learners may still overgeneralize a successful save/load observation into durability;
- learners may collapse code point / visible character / UTF-8 byte layers;
- learners may infer arithmetic wrap semantics from two's-complement representation;
- tooling discovery (`git diff`, `pdb`) may create incidental friction even when the mental model is sound;
- renderer behavior may alter the intended progressive disclosure or diagram readability.

These are pilot observation targets, not learner-validation results.

## 10. OQ-BP-006 status

OQ-BP-006 remains **OPEN**.

Actually verified here:

- Debian GNU/Linux 13 (trixie)
- x86_64
- Python 3.13.5
- Git 2.47.3
- GNU bash 5.2.37
- exact merged activity/test sources from commit `39e6ad3a...`

Not verified here:

- Ubuntu 24.04 LTS Noble runtime
- Python 3.12 runtime
- a pinned/immutable canonical container image
- final package/toolchain version pins

This task does not close OQ-BP-006, convert the Design baseline into a Decision, or define a canonical Dev Container.

## 11. Finding classification

### Learner-packet defects

No new learner-packet defect was found that requires classification as SIMPLE FIX, COMPLEX REWORK, or ARCHITECTURE.

### Verification limitations / environment observations

1. **Fresh remote checkout blocked by runner DNS/network.**
   This is an execution-environment limitation, not evidence of a repository defect. Literal `git diff --check` was run on the exact-source local reconstruction and final artifact diff, while the remote branch/base identity was verified separately through GitHub.

2. **Ubuntu 24.04 Noble / Python 3.12 unavailable.**
   This is an OQ-BP-006-related verification gap, not a basis to silently choose or pin an environment.

No ARCHITECTURE finding is raised. If later pilot or canonical-environment evidence reveals one, route it through:

`Open Question → Research → RFC/Decision if needed → New Task`

## 12. Lifecycle statement

- PR #30 merge did **not** make the M00–M01 content `VERIFIED`.
- This independent verifier must not and does not self-promote the curriculum to `VERIFIED`.
- Creating a pilot observation template does **not** constitute learner validation.
- No learner identities, quotations, session logs, completion rates, success percentages, transfer-success claims, or learner-validation conclusions were fabricated.
- D-023 construction order is preserved: `Research → Design → Lesson → Lab → Project → Verification → Learner Validation`; this task stays at the verification/pilot-readiness gate and does not implement M02.

## 13. Final recommendation

`READY FOR LEAD VERIFICATION REVIEW`
