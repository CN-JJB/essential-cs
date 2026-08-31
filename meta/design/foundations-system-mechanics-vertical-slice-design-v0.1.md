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
