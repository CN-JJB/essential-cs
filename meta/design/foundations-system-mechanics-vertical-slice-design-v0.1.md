# Foundations / System Mechanics Vertical-Slice Design v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #27 — Foundations/System Mechanics Vertical-Slice Design v0.1
Branch: `vertical-slice/issue-27-foundations-system-mechanics-design`
Base reconciled: `main @ 955a6974214542e6d9d053da01b62cbe41b739c1`
Role: Vertical Slice Design Architect / Instructional Systems Designer
Scope: Design step only for M00–M04. This document specifies teaching, activity, evidence, support, and implementation contracts. It is not learner-facing Lesson prose, runnable Lab/project code, a Dev Container implementation, or an architecture change.

## 1. Design contract and authority

This design converts the Lead-accepted `research/foundations-system-mechanics-vertical-slice-v0.1.md` into a production contract for the first post-Blueprint vertical slice:

`Research → DESIGN → Lesson → Lab → Project → Verification → Learner Validation`

The canonical architecture remains unchanged: 7 Stages, 25 Modules, 70 preliminary Lessons, 40 hard + 22 soft Module edges, exactly 8 competencies, 18 canonical concepts, 15 Big Ideas, the accepted 5 Required / 5 Optional / 5 Source Expeditions, and P0–P9 as project mapping rather than curriculum dependency. OQ-BP-001 and OQ-BP-003 remain RFC-gated; OQ-BP-006 remains open implementation-time work.

### 1.1 Slice-level capability transition

Entry is the accepted learner baseline: basic programming, approximately high-school mathematics, no assumed shell/Git/C/assembly/Linux-administration fluency. Bridge remains optional/skippable and outside the Core DAG.

By the end of M04, the learner should be able to move from a program-level view to an evidence-grounded systems view:

1. map a small local system and separate prediction, observation, explanation, and uncertainty;
2. reason about information through finite representations and detect representation-boundary failures;
3. reason about algorithm growth, specifications, invariants, correctness, and constrained trade-offs;
4. connect minimal C source to native x86-64 instructions, registers, memory, and a call frame while distinguishing language semantics, ISA/ABI rules, and compiler observations;
5. run a controlled locality experiment, retain raw evidence, summarize variation, consider competing explanations, and state a bounded conclusion.

### 1.2 Design-wide non-goals

This slice does **not** become a Linux/Git course, a full discrete-math or algorithms course, a C/assembly course, digital logic/CPU construction, compiler construction, OS/virtual-memory teaching, persistence/durability teaching, database internals, networking, distributed systems, cloud/vendor training, or AI/ML Core expansion. It does not introduce a Required Lab.

### 1.3 Canonical competencies used

Only the canonical eight are referenced: **Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, Learn-New-Tech**. No new competency is implied by phrases such as “measure,” “investigate,” or “transfer.”

### 1.4 Assessment and support grammar

Primary assessment modes remain **Explain / Predict / Break / Judge**. Cumulative modes remain **Recall / Connect / Transfer**. Evidence is assessed by claim↔evidence alignment, mechanism accuracy, assumptions, correctness/invariant reasoning, measurement quality, causal restraint, trade-off reasoning, uncertainty recognition, and transfer—not prose polish.

All module support ladders use the accepted progressive-disclosure shape:

`Question → Hint 1 → Hint 2 → Expected Observation → Full Explanation`

If the learner needs the Full Explanation, that attempt becomes remediation evidence rather than independent exit evidence; a short transfer check may later establish independence.

## 2. Shared environment and preflight contract

### 2.1 Baseline family — proposal preserved, OQ-BP-006 not closed

Use the Research Dossier's first-slice direction as the Design baseline family:

- Ubuntu 24.04 LTS Noble Dev Container / Codespace;
- Python 3.12;
- Noble GCC toolchain;
- GNU binutils including `objdump`;
- GDB;
- Git;
- minimal shell/core utilities.

This is a **CURRENT PRACTICE / IMPLEMENTATION** baseline, not a curriculum invariant. The exact immutable image digest and exact package builds remain implementation-time choices under OQ-BP-006. `perf` remains optional and non-blocking. No QEMU/RISC-V cross-toolchain is required for this slice.

### 2.2 Preflight evidence record

The first-slice preflight produces one reusable environment record, not a repeated module report. It must capture enough information to explain assessed observations:

| Capability | Required check | Blocking? | Used by |
|---|---|---:|---|
| Canonical OS family | Linux + release identity recorded; canonical implementation expected to report Ubuntu 24.04/Noble | Yes for canonical assessed path | M00–M04 |
| CPU architecture | architecture recorded; canonical M03 path requires `x86_64`/equivalent x86-64 identity | Yes for canonical M03 only | M03/M04 provenance |
| Python | Python 3.12 runtime available; version recorded | Yes | M00/M01/M04 timing harness if used |
| Git | status/diff/change-record capability available; version recorded | Yes for M00 evidence workflow | M00 |
| C toolchain | compile + link + execute a minimal native probe | Yes | M03/M04 native fixture |
| binutils | disassemble a named function/symbol; version recorded | Yes | M03 |
| GDB | start target, set/stop at a known location, inspect registers and memory without privileged-container changes | Yes | M03 |
| High-resolution monotonic timing | timer is monotonic, resolution metadata can be recorded, and repeated elapsed-time differences can be collected | Yes | M04 |
| Writable working area | create/remove learner-owned temporary evidence files | Yes | M00–M04 |
| `perf` | capability detection only; record available/restricted/unavailable | **No** | Optional M04 corroboration |

### 2.3 Preflight failure routing

- A missing/misconfigured required capability is an **environment/preflight defect**, not learner conceptual failure.
- A non-x86-64 local convenience environment may continue through M00–M02, but canonical M03 assessment must move to the supported x86-64 Codespace/container unless implementation later supplies an explicitly approved equivalent path. Do not add a second ISA curriculum.
- `perf` failure must never ask the learner to weaken host/container security settings.
- Preflight implementation must preserve raw diagnostics sufficient for maintainers to distinguish course-image failure from learner command error.

### 2.4 Implementation smoke tests before learner release

The implementation task must smoke-test, in the actual pinned container/Codespace image:

1. fresh-start preflight from a clean learner account;
2. the exact architecture identity used by the canonical M03 path;
3. compile/link/run of the M03 fixture;
4. source-aware disassembly with stable-enough symbol/source anchors for the activity;
5. GDB breakpoint/step/register/memory inspection under the hosted container security policy;
6. the bounded M03 failure observation and its cleanup/reset;
7. the M04 timing source and recorded resolution/monotonicity;
8. the complete M04 workload with the required repetitions, acceptable runtime, raw-evidence retention, and a robust locality effect across fresh hosted sessions;
9. `perf` capability detection behaving as optional/non-blocking in both allowed and restricted cases;
10. evidence-packet generation/checking without requiring unlisted tools or privileges.

If M03 or M04 cannot meet these checks without privileged containers or substantial new setup, implementation must simplify the observation/fixture first. A change to curriculum scope, Lab selection, Module edges, or architecture is an escalation, not an implementation workaround.

## 3. M00 — The Map & Investigation Discipline

### 3.1 Learner capability transition

**Before:** can run small programs but may treat a computer/system as a black box and tool output as explanation.

**After:** can trace one bounded local path through interfaces/state/representations, write a falsifiable prediction before inspection, preserve a minimal evidence record, and distinguish observation from causal explanation and unresolved uncertainty.

Primary module capability remains **Trace**; M00 also introduces practical **Observe** and **Learn-New-Tech** habits without claiming Stage-exit mastery for them.

### 3.2 Explicit non-goals

No shell command encyclopedia; no Git branching/rebase workflow; no debugger mastery; no HTTP/network mechanism teaching; no database/storage mechanism; no formal statistics; no AI prompting/model curriculum; no system-design pattern catalog.

### 3.3 Mapping to existing preliminary Lessons

| Lesson | Existing topic | Design role |
|---|---|---|
| `L00-01` | Whole-system map; abstraction/interface/indirection; system question set | Establish path-and-boundary mental model using one local fixture and preview that systems can fail without defining canonical Failure. |
| `L00-02` | Investigation: shell/task execution, unfamiliar file/code reading, debugger-light inspection, Git evidence, environment/version record, baseline preservation, AI output as untrusted hypothesis | First Core evidence/investigation home. Produce the reusable evidence header and one controlled investigation. |

No new Lesson IDs are created.

### 3.4 Canonical concepts introduced vs previewed/revisited

**Canonical first introductions at `L00-01`:**

- `EC-CON-001` State
- `EC-CON-002` Abstraction
- `EC-CON-004` Indirection
- `EC-CON-005` Interface

**Preview only:** Failure (“systems can fail”) without the canonical definition; Representation as a question asked at boundaries without pre-empting `EC-CON-003` at M01. Technical Literacy and debugging are horizontal practices, not new canonical concepts.

### 3.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisites: none. Entry baseline: basic programming only.

Hidden-prerequisite support is part of the module, not an entry gate:

- supply exact task-entry commands or one-click actions rather than assume shell fluency;
- explain only the Git operations needed to inspect and preserve a change;
- use a small unfamiliar file with a clearly bounded reading task;
- debugger-light observation must have a supplied command path and expected stop/output;
- distinguish “tool failed to run” from “prediction was wrong.”

### 3.6 Teaching sequence / mechanism exposure

Use the sequence:

1. **Question:** Where does input/data/state travel in this small local system, and what could we actually observe?
2. **Mental Model:** path-and-boundary diagram: `input → interface → representation → executing state → supplied lower boundary → output/state change`.
3. **Mechanism:** interfaces expose contracts; abstractions omit detail; indirection inserts lookup/mapping; state influences later observations.
4. **Predict:** learner marks one expected output/state change and one possible failure location before running anything.
5. **Observe:** run the baseline fixture and inspect one boundary using a real tool.
6. **Build/Break:** make one controlled, reversible change to an input/configuration/source constant supplied by the activity.
7. **Explain:** separate observed fact from mechanism explanation; record one competing explanation or uncertainty.
8. **Judge:** select the best evidence source/tool for one claim and explain why another source layer would be insufficient.

### 3.7 Observation/activity design — specification level

Use one course-owned local fixture with no network dependency and no learner-visible persistence mechanism requirement. The fixture must expose:

- one input;
- at least two named interfaces/boundaries;
- one process-local state change;
- one supplied persistence boundary that is explicitly opaque if P0 is used;
- deterministic baseline output plus one safe controlled change/failure;
- an unfamiliar-but-small source/config/data file that can be read without prior tool expertise.

The learner must first predict, then run baseline, inspect one boundary, make exactly one controlled change, rerun, compare evidence, and reset. Git is used only to show/preserve the change. An AI-generated claim/code snippet may be offered only as an **untrusted hypothesis** to verify from docs/test/observation; AI use is not required.

### 3.8 Required learner evidence

Reuse the shared packet:

- environment/preflight header;
- one path trace with interface/state labels;
- pre-run prediction;
- baseline and changed-condition observation excerpts;
- exact changed variable and Git diff/reference;
- one sentence each for observation, explanation, competing explanation/uncertainty;
- source-layer judgment: specification/docs/source/experiment and why.

### 3.9 Assessment modes

Primary: **Predict, Explain, Judge**. Controlled **Break** is used when the fixture supports a reversible failure. Cumulative: **Connect** to the learner's prior programming experience.

### 3.10 Machine-checkable vs reviewer-required evidence

**Machine-checkable:** preflight keys present; baseline command/task completed; changed variable differs from baseline; diff/evidence record exists; reset returns fixture to baseline; required output anchors exist.

**Reviewer-required:** correctness of path/boundary labels; State vs storage distinction; source-layer choice; observation vs explanation separation; causal restraint; whether the uncertainty is meaningful rather than boilerplate.

### 3.11 Misconceptions

- “The diagram is the system.” → It is a purpose-bounded model with omissions.
- “I ran a command, therefore I investigated.” → Investigation begins with a question/prediction and ends with interpreted evidence.
- “The output says X, so X caused it.” → Observation and causal explanation are different claims.
- “State means whatever is stored on disk.” → State is any information that can affect future behavior/observations.
- “Official docs answer every question.” → Authority depends on the claim layer.
- “Git/Linux knowledge is the learning objective.” → They are evidence instruments here.

### 3.12 Hint/support ladder

- **Question:** Which boundary could produce an observation that distinguishes your two explanations?
- **Hint 1:** Mark input, one interface, one piece of state, and output before choosing a command.
- **Hint 2:** Compare exactly one baseline/changed variable and inspect the smallest boundary that can reveal its effect.
- **Expected Observation:** supplied expected baseline/change anchors plus reset state, without the causal explanation.
- **Full Explanation:** model trace, why the selected tool/source answers the claim, and why the evidence does not prove more than it observed.

### 3.13 Visual/diagram requirements

1. **Path-and-boundary map:** must demonstrate data/control direction, interface boundaries, state locations, indirection point(s), and which mechanisms are intentionally opaque.
2. **Evidence ladder visual:** must demonstrate `prediction → observation → explanation → competing explanation → bounded conclusion`, with observation visually separated from causal claim.
3. **Model-expiration callout:** the same system map must mark at least one omitted mechanism to reinforce that abstraction is purpose-bounded.

### 3.14 Provenance/source anchors

Accepted Research Dossier §§3.1–3.8, 8, 10, 12–13; Source Register anchors: Git `git diff` documentation, GitHub Codespaces/dev-container documentation, canonical Blueprint/policy artifacts. Evidence layer emphasis: **PRINCIPLE** for investigation discipline; **IMPLEMENTATION/CURRENT PRACTICE** for Git/Linux/container surfaces.

### 3.15 Module exit criteria

M00 exits when the learner can, with at most early hints and then a short independent transfer check if needed:

- trace one bounded local path and name State/Interface/Abstraction/Indirection correctly;
- make a falsifiable prediction before inspection;
- preserve environment + baseline/change evidence;
- separate observation from explanation and name one unresolved uncertainty;
- choose an evidence/source layer appropriate to a claim.

### 3.16 Handoff to M01

M01 reuses the same fixture/evidence packet but zooms into the question M00 has deliberately left open: **what concrete representation crosses this boundary, how many bytes does it use, and under what interpretation is it valid?**

## 4. M01 — Bits, Bytes & Representation

### 4.1 Learner capability transition

**Before:** can point to data crossing a boundary but may assume values/text have one intrinsic machine form.

**After:** can encode/decode bounded values and UTF-8 text, inspect exact bytes, reason about endianness and finite ranges, estimate representation size, and detect/diagnose a broken round trip without conflating information with representation.

Primary module capability remains **Explain**, with **Trace, Estimate, Correctness, Diagnose** exercised in the canonical S1 pattern.

### 4.2 Explicit non-goals

No digital logic/gates, Boolean algebra, Shannon information theory, compression theory, floating-point deep dive, arbitrary-precision internals, bus/protocol history, Unicode normalization/grapheme algorithm deep dive, or bit-trick puzzle course. Do not define Specification/Invariant/Correctness canonically before M02.

### 4.3 Mapping to existing preliminary Lessons

| Lesson | Existing topic | Design role |
|---|---|---|
| `L01-01` | bit/byte/binary/counting | First home of Representation; inspect bounded values as bits/bytes/hex. |
| `L01-02` | signed/unsigned, two's complement, overflow | Separate signed representation from language arithmetic semantics; use boundary cases. |
| `L01-03` | UTF-8/encoding; endianness | Observe code point/text-to-bytes and explicit byte-order changes; break decoding. |
| `L01-04` | size estimation; serialization; round-trip | Integrate one record representation, estimate size, and test round-trip property. |

### 4.4 Canonical concepts introduced vs previewed/revisited

**Canonical first introduction:** `EC-CON-003` Representation at `L01-01`.

**Revisited/applied:** State and Interface from M00. The round-trip property may use intuitive “must remain true” language, but `EC-CON-007` Specification, `EC-CON-008` Invariant, and `EC-CON-009` Correctness remain canonical first homes at M02 `L02-03`.

### 4.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisite: M00. Lesson hard prerequisite for `L01-01`: `L00-01`.

Support assumptions:

- no hand-conversion speed requirement; provide powers-of-two/hex reference;
- no command-specific hexdump dependency; Python byte inspection is sufficient;
- Unicode terminology is introduced only to the boundary needed for UTF-8 correctness;
- any filesystem size observation is evidence of byte count only, not storage/durability teaching.

### 4.6 Teaching sequence / mechanism exposure

1. **Question:** How can the same information have different byte sequences, sizes, and validity rules?
2. **Mental Model:** information → representation contract → bytes → interpretation.
3. **Mechanism:** positional binary/hex; bounded integer patterns; signed representation; UTF-8 encoding; explicit byte order; serialization fields/lengths.
4. **Predict:** exact byte sequence/range/length for a bounded fixture before running.
5. **Observe:** inspect bytes using Python standard-library mechanisms and exact fixtures.
6. **Break:** wrong byte order, malformed/truncated UTF-8, out-of-range integer, or ambiguous/truncated record.
7. **Explain:** distinguish “these are the bytes observed” from “this is the representation contract.”
8. **Judge:** choose a representation under stated constraints such as readability, fixed width, size, or interoperability.

### 4.7 Observation/activity design — specification level

Use one compact record fixture, preferably the P0 record shape when it reduces duplicate work. The activity must include:

- one unsigned and one signed fixed-width integer boundary example;
- one UTF-8 string containing both ASCII and a multi-byte code point;
- explicit little-endian and big-endian packing of the same multi-byte integer;
- one simple serialized record with unambiguous field boundaries;
- an encode→bytes→decode round trip;
- at least one controlled failure: mismatched byte order, malformed/truncated UTF-8, range violation, or ambiguous/truncated serialization;
- a byte-size estimate made before observation and reconciled afterward.

Python stdlib is the canonical low-burden observation surface. CLI hex tools may be convenience-only, never required.

### 4.8 Required learner evidence

Append to the shared packet:

