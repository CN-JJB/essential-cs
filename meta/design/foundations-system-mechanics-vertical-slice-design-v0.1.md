# Foundations / System Mechanics Vertical-Slice Design v0.1

Status: **READY FOR LEAD REVIEW**

Issue: #27 — Foundations/System Mechanics Vertical-Slice Design v0.1
Branch: **vertical-slice/issue-27-foundations-system-mechanics-design**
Base reconciled: **main @ 955a6974214542e6d9d053da01b62cbe41b739c1**
Role: Vertical Slice Design Architect / Instructional Systems Designer
Scope: Design step only for M00–M04. This document is not learner-facing Lesson prose, runnable Lab/project code, a Dev Container implementation, or a curriculum-architecture change.

## 1. Authority, boundaries, and slice intent

This design converts the Lead-accepted Research Dossier, **research/foundations-system-mechanics-vertical-slice-v0.1.md**, into a production contract for the first post-Blueprint vertical slice:

**Research → DESIGN → Lesson → Lab → Project → Verification → Learner Validation**

The current canonical architecture remains unchanged: 7 Stages; 25 Modules; 70 preliminary Lessons; 40 hard + 22 soft Module edges; exactly 8 competencies; 18 canonical concepts; 15 Big Ideas; the accepted 5 Required / 5 Optional / 5 Source Expeditions; and P0–P9 as project mapping rather than curriculum prerequisite structure.

This design does not resolve OQ-BP-001, OQ-BP-003, or OQ-BP-006. It does not create a ninth competency, a new Required Lab, a new Lesson ID, a new concept first home, or a new hard/soft dependency.

### 1.1 Slice-level capability transition

Entry remains the accepted baseline: basic programming and approximately high-school mathematics. Shell, Git, C, assembly, Linux administration, and statistics fluency are not entry gates; hidden prerequisites are supported just in time.

By the end of M04, the learner should be able to:

1. trace a bounded local system through interfaces, state, representations, and observable boundaries;
2. inspect finite representations and reason about signed/unsigned integers, UTF-8, byte order, serialization, and size;
3. reason about operation growth, constrained data-structure choices, specification, invariant, correctness, and bounded tractability/decidability intuition;
4. connect minimal C source to native x86-64 instructions, registers, memory, and a call frame while distinguishing language semantics, ISA/ABI rules, and compiler/build observations; and
5. run a controlled locality experiment, retain raw timing evidence, summarize variation, consider competing explanations, and state a bounded conclusion.

The canonical competency vocabulary used here is only: **Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, Learn-New-Tech**.

### 1.2 Design-wide non-goals

The slice is not a shell/Git course, a discrete-mathematics sequence, a full algorithms course, a C/assembly programming course, a CPU-construction course, an OS/virtual-memory course, a persistence/durability course, a database course, a networking course, or an AI curriculum expansion. No mechanism that belongs first in M05+ is pulled forward merely because a tool exposes it.

The accepted primary assessment modes remain **Explain / Predict / Break / Judge**; cumulative review may use **Recall / Connect / Transfer**. Evidence quality is judged by claim↔evidence alignment, mechanism accuracy, assumptions, causal restraint, uncertainty, and transfer—not by prose polish or command memorization.

## 2. Shared environment and preflight contract

### 2.1 Baseline family; OQ-BP-006 remains open

Use the Research Dossier proposal as the Design baseline family:

- Ubuntu 24.04 LTS Noble Dev Container / Codespace;
- Python 3.12;
- Noble GCC toolchain;
- GNU binutils, including objdump;
- GDB;
- Git;
- minimal shell/core utilities.

This is a CURRENT PRACTICE / IMPLEMENTATION baseline, not a curriculum invariant. The exact immutable container image digest and exact package builds remain implementation-time choices under OQ-BP-006. Design does not close or edit that Open Question.

**perf remains optional and non-blocking.** Core completion must not depend on hardware counters, privileged tracing, modified host security settings, or QEMU/RISC-V setup.

### 2.2 Preflight record

M00 creates one reusable environment record. M03 and M04 recheck only capabilities relevant to their mechanism. The implementation may automate the checks, but the learner-facing activity must retain enough context to explain observations.

| Capability | Required check | Blocking? | Primary use |
|---|---|---:|---|
| OS family | Record Linux distribution/release; canonical path expects Ubuntu 24.04/Noble | Yes for canonical assessed path | M00–M04 provenance |
| CPU architecture | Record architecture; canonical M03 path requires native x86-64 | Yes for canonical M03 | M03/M04 context |
| Python | Python 3.12 available; record version | Yes where Python harness is used | M00/M01/M04 |
| Git | status/diff/change-record capability available; record version | Yes | M00 evidence discipline |
| C toolchain | Compile, link, and execute a minimal native C probe | Yes | M03/M04 |
| binutils | Disassemble a named function/symbol; record tool version | Yes | M03 |
| GDB | Start target, stop at known location, inspect registers and memory under hosted security policy | Yes | M03 |
| monotonic high-resolution timing | Monotonic clock usable; resolution metadata recordable; repeated elapsed-time samples possible | Yes | M04 |
| working area | Create, modify, compare, and reset learner-owned evidence files | Yes | M00–M04 |
| perf | Detect available / restricted / unavailable; no security weakening | No | Optional M04 corroboration |

A failed required capability is classified as an environment/preflight defect, not learner conceptual failure. The implementation must preserve raw diagnostics sufficient to distinguish environment failure from an incorrect learner command.

A non-x86-64 convenience environment may support M00–M02, but canonical M03 evidence must run in the supported x86-64 container/Codespace path unless a later approved implementation explicitly supplies an equivalent canonical path. This does not add a second ISA curriculum.

### 2.3 Implementation smoke tests before learner release

The implementation task must smoke-test, in the actual pinned environment eventually selected:

1. clean/fresh-start preflight;
2. exact architecture identity used by M03;
3. compile/link/run of the M03 fixture;
4. source-aware disassembly with stable-enough symbol/source anchors;
5. GDB breakpoint, stepping, register inspection, and memory inspection without privileged-container changes;
6. bounded M03 failure observation plus deterministic cleanup/reset;
7. M04 timing source monotonicity/resolution recording;
8. full M04 workload, warmups, repetitions, raw-evidence retention, and checksum/correctness guard using defined language semantics;
9. inspect the generated code/build behavior for both M04 traversal patterns so vectorization, dead-code elimination, or another compiler transformation does not make the intended locality lesson misleading; if a transformation materially dominates the observed difference, adjust the fixture/build or explicitly bound the claim before learner release;
10. robust locality direction across multiple fresh hosted sessions;
11. perf capability detection in both permitted and restricted cases, with identical Core completion behavior;
12. evidence-packet assembly/checking without unlisted privileged tools.

If M03 or M04 requires security weakening, privileged containers, or substantial setup not supported by the accepted baseline, implementation must simplify the fixture/observation before proposing curriculum changes.

---

## 3. M00 — The Map & Investigation Discipline

### 3.1 Learner capability transition

**Before:** can run small programs but may treat the computer/system as a black box and tool output as explanation.

**After:** can trace one bounded local path through named interfaces and state, write a falsifiable prediction before inspection, preserve a reproducible baseline/change record, and separate observation, mechanism explanation, competing explanation, and unresolved uncertainty.

Primary module capability remains **Trace**. M00 also begins practical Observe and Learn-New-Tech habits without claiming their Stage-exit mastery.

### 3.2 Explicit non-goals

No command encyclopedia; no Git branching/rebase curriculum; no debugger mastery; no HTTP/network mechanism teaching; no database/storage mechanism; no formal statistics; no AI prompting curriculum; no architecture-pattern catalog. “Systems fail” is a preview only, not the canonical Failure definition.

### 3.3 Existing preliminary Lesson mapping

| Lesson | Existing topic | Design responsibility |
|---|---|---|
| **L00-01** | whole-system map; abstraction/interface/indirection; question set | Establish a purpose-bounded path-and-boundary model using one local fixture. |
| **L00-02** | shell/task execution; unfamiliar file/code reading; debugger-light investigation; Git evidence; reproducibility/version/environment record; baseline preservation; AI output as untrusted hypothesis | First Core evidence/investigation home. Produce the reusable preflight/evidence header and one controlled investigation. |

No new Lesson ID is created.

### 3.4 Canonical concepts introduced vs previewed/revisited

Canonical first introductions at **L00-01** remain unchanged:

- EC-CON-001 State
- EC-CON-002 Abstraction
- EC-CON-004 Indirection
- EC-CON-005 Interface

Preview only: Failure as “a system can fail,” without the EC-CON-010 canonical definition; Representation as a question at boundaries, without pre-empting EC-CON-003 at M01.

### 3.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisites: none. Entry baseline: basic programming.

Hidden-prerequisite support is in-module:

- provide exact task-entry commands/actions rather than assume shell fluency;
- teach only Git operations needed to inspect/preserve one change;
- use one small unfamiliar file with a bounded reading question;
- debugger-light activity provides the invocation path and expected stop/output shape;
- explicitly distinguish “tool failed to run” from “prediction was wrong.”

Bridge remains optional/skippable and outside the Core DAG.

### 3.6 Teaching sequence / mechanism exposure

1. **Question:** Where do input, state, control, and output travel in this small local system?
2. **Mental model:** path + named boundaries + intentionally omitted detail.
3. **Mechanism:** interfaces expose contracts; abstraction hides detail for a purpose; indirection adds lookup/mapping; state can change later observations.
4. **Predict:** mark one expected state/output change and one possible failure location before running.
5. **Observe:** run the deterministic baseline and inspect one boundary with a real tool.
6. **Break/change:** alter exactly one supplied input/config/source constant; rerun.
7. **Explain:** separate observed fact from mechanism claim; record a competing explanation or uncertainty.
8. **Judge:** choose the evidence/source layer that can actually answer one claim.

### 3.7 Observation/activity design — specification level

Use one course-owned local fixture with no network dependency. It must expose:

- one input;
- at least two named interfaces/boundaries;
- one process-local state transition;
- deterministic baseline output;
- one safe, reversible controlled change;
- an unfamiliar-but-small source/config/data file;
- if P0 is used, a supplied persistence boundary that remains opaque.

The learner predicts first, runs baseline, inspects one boundary, makes exactly one controlled change, reruns, compares evidence, and resets. Git is evidence plumbing, not the learning object. An AI-generated claim/snippet may appear only as an optional untrusted hypothesis to verify; AI use is not required.

### 3.8 Required learner evidence

Reuse the shared packet:

- environment/preflight header;
- bounded system trace with interface/state labels;
- pre-run prediction;
- baseline and changed-condition observation excerpts;
- exact changed variable and Git diff/reference;
- reset evidence;
- one-sentence observation, explanation, competing explanation/uncertainty;
- source-layer judgment: specification/docs/source/experiment and why.

### 3.9 Assessment modes

Primary: **Predict, Explain, Judge**, plus **Break** where the supplied fixture supports a reversible failure. Cumulative: **Connect** to prior programming experience.

### 3.10 Machine-checkable vs reviewer-required evidence

**Machine-checkable:** required preflight fields exist; baseline task ran; controlled-change marker differs from baseline; Git/diff evidence exists; reset restores expected baseline; required output anchors exist.

**Reviewer-required:** path/boundary labels are accurate; State is not confused with storage; observation is separated from causal explanation; selected evidence layer fits the claim; uncertainty is substantive rather than boilerplate.

### 3.11 Misconceptions

- “The diagram is the system.”
- “I ran a command, therefore I investigated.”
- “The output says X, therefore X caused it.”
- “State means whatever is stored on disk.”
- “Official docs answer every claim layer.”
- “Git/Linux knowledge is the objective.”
- “AI output is evidence.”

### 3.12 Hint/support ladder

**Question → Hint 1:** mark input, one interface, one state item, and output before choosing a command.
**Hint 2:** compare exactly one baseline/change variable and inspect the smallest boundary that can reveal its effect.
**Expected Observation:** provide the expected baseline/change anchors and reset state, not the causal explanation.
**Full Explanation:** connect the path, tool/source choice, mechanism, and evidence limits. A later short transfer check is required for independent exit evidence after Full Explanation.

### 3.13 Visual/diagram requirements

1. **Path-and-boundary map:** demonstrate data/control direction, interfaces, state locations, indirection points, and intentionally opaque mechanisms.
2. **Evidence ladder:** demonstrate prediction → observation → explanation → competing explanation → bounded conclusion, with observation visually separated from causal claim.
3. **Model-expiration callout:** identify at least one omitted mechanism so abstraction is visibly purpose-bounded.

### 3.14 Provenance/source anchors

Accepted Research Dossier §§3, 8, 10, 12–13; its Source Register entries for Git diff documentation, GitHub Codespaces/Dev Containers, and canonical Blueprint/policy artifacts. Evidence layer: PRINCIPLE for investigation discipline; IMPLEMENTATION/CURRENT PRACTICE for tool/container surfaces.

### 3.15 Module exit criteria

M00 exits when the learner can, independently or after only early hints plus a short transfer check:

- trace one bounded local path and correctly name State/Interface/Abstraction/Indirection;
- make a falsifiable prediction before inspection;
- preserve environment + baseline/change evidence;
- separate observation from explanation and name one unresolved uncertainty;
- choose an appropriate evidence/source layer for a claim.

### 3.16 Handoff into M01

M01 reuses the same fixture/evidence packet but zooms into the open question: **what concrete representation crosses a boundary, how many bytes does it occupy, and under what interpretation is it valid?**

---

## 4. M01 — Bits, Bytes & Representation

### 4.1 Learner capability transition

**Before:** can identify data crossing boundaries but may assume values/text have one intrinsic machine form.

**After:** can encode/decode bounded values and UTF-8 text, inspect exact bytes, reason about finite integer ranges and endianness, estimate representation size, and diagnose a broken round trip without conflating information with representation.

Primary module capability remains **Explain**, with Trace, Estimate, Correctness, and Diagnose exercised.

### 4.2 Explicit non-goals

No digital logic/gates; no Shannon information theory; no compression theory; no floating-point deep dive; no arbitrary-precision internals; no Unicode normalization/grapheme algorithm deep dive; no bus/protocol history; no bit-trick puzzle course. Specification/Invariant/Correctness retain their canonical definitions at M02 L02-03.

### 4.3 Existing preliminary Lesson mapping

| Lesson | Existing topic | Design responsibility |
|---|---|---|
| **L01-01** | bit/byte/binary/counting | Canonical first home of Representation; inspect bounded values as bits/bytes/hex. |
| **L01-02** | signed/unsigned, two’s complement, overflow | Separate representation facts from language arithmetic semantics; use boundary cases. |
| **L01-03** | UTF-8/encoding; endianness | Observe text→bytes and explicit byte-order changes; controlled decode failure. |
| **L01-04** | size estimation; serialization; round trip | Integrate a compact record representation, estimate size, and test round-trip behavior. |

### 4.4 Canonical concepts introduced vs previewed/revisited

Canonical first introduction: **EC-CON-003 Representation at L01-01**.

Revisited/applied: State and Interface from M00. Round-trip activity may use ordinary “must remain true” language, but EC-CON-007 Specification, EC-CON-008 Invariant, and EC-CON-009 Correctness are not canonically defined until M02 L02-03.

### 4.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisite: M00. Lesson hard prerequisite for L01-01: L00-01.

Support:

- provide powers-of-two/hex reference; no hand-conversion speed requirement;
- Python standard-library byte inspection is sufficient; CLI hexdump tools are convenience-only;
- Unicode vocabulary is limited to what UTF-8 correctness needs;
- file-size observations, if any, are byte-count evidence only—not filesystem/durability teaching.

### 4.6 Teaching sequence / mechanism exposure

1. Question: how can the same information have different byte sequences, sizes, and validity rules?
2. Mental model: information → representation contract → bytes → interpretation.
3. Mechanisms: positional binary/hex; bounded integer width; signed representation; UTF-8; explicit byte order; field boundaries/lengths.
4. Predict exact bytes/range/length for bounded fixtures.
5. Observe with Python standard-library mechanisms.
6. Break with one mismatched byte order, malformed/truncated UTF-8, out-of-range integer, or ambiguous/truncated record.
7. Explain observed bytes versus representation rule.
8. Judge between two bounded representations under a stated constraint.

### 4.7 Observation/activity design — specification level

Use one compact record fixture, preferably compatible with P0 when that reduces duplicate work. It must include:

- one unsigned and one signed fixed-width integer boundary example;
- one UTF-8 string containing ASCII plus a multibyte code point;
- explicit little-endian and big-endian packing of the same multi-byte value;
- one simple serialized record with unambiguous field boundaries;
- encode → bytes → decode round trip;
- at least one controlled failure;
- a byte-size estimate made before observation and reconciled afterward.

Python stdlib is the canonical low-burden observation surface. No optional CLI hex utility may become a prerequisite.

### 4.8 Required learner evidence

Append to the shared packet:

- prediction + observed bytes for representative integer/text cases;
- finite range/width assumptions;
- explicit-endianness before/after trace;
- one broken round trip and diagnosis;
- record-size estimate with assumptions and observed size;
- one sentence identifying what information stayed the same while representation changed.

### 4.9 Assessment modes

Primary: **Predict, Break, Explain**. **Judge** for one constrained representation choice. Cumulative: **Transfer** by decoding one documented unfamiliar field.

### 4.10 Machine-checkable vs reviewer-required evidence

**Machine-checkable:** exact bytes for fixed fixtures; encode/decode equality; expected failure class; integer range checks; byte-size arithmetic for canonical fixture.

**Reviewer-required:** information-vs-representation distinction; scope of two’s-complement claim versus language overflow semantics; UTF-8/code-point/byte distinction; validity assumptions; quality of size assumptions.

### 4.11 Misconceptions

- “Bits contain meaning by themselves.”
- “Hex is how numbers are stored.”
- “One character equals one byte.”
- “One code point always equals one visible character.”
- “UTF-8 has host endianness.”
- “Two’s complement means signed overflow wraps in every language.”
- “Serialization is just converting to a string.”
- “One successful round trip proves a format correct.”

### 4.12 Hint/support ladder

**Question:** what interpretation must encoder and decoder agree on?
**Hint 1:** write the value/text separately from the proposed bytes.
**Hint 2:** mark width, byte order, field boundaries, and valid input domain.
**Expected Observation:** provide canonical bytes/errors for the supplied fixture only.
**Full Explanation:** connect information, representation contract, bytes, validity, and round-trip limits; then use a new documented field for independent transfer.

### 4.13 Visual/diagram requirements

1. **One value, multiple representations:** logical information distinct from binary/hex/serialized forms.
2. **UTF-8 zoom:** text/code-point concept → variable-length UTF-8 bytes; explicitly show byte count ≠ visible-character count.
3. **Endianness visual:** same multi-byte value with byte positions reversed by representation choice.
4. **Round-trip pipeline:** show where mismatch/truncation breaks reversibility.

### 4.14 Provenance/source anchors

Research Dossier §§4, 9, 11–12; Source Register anchors: Unicode Standard 17.0 and Unicode UTF FAQ (SPECIFICATION), WG14/C23 two’s-complement materials (SPECIFICATION), Python struct documentation (IMPLEMENTATION), CS50 only as bounded teaching reference. No copied third-party figures/code are required.

### 4.15 Module exit criteria

M01 exits when the learner can:

- inspect and explain a bounded integer/text/record representation;
- state finite range/width assumptions;
- distinguish signed representation from language overflow rules;
- round-trip valid data and diagnose one invalid/mismatched case;
- estimate byte size with explicit assumptions;
- transfer the representation reasoning to one documented unfamiliar field.

### 4.16 Handoff into M02

M02 receives concrete representations and asks: **given operations over these representations/state, what procedure is correct, how does its work grow, and what trade-off follows from the workload?**

---

## 5. M02 — Computation & Complexity

### 5.1 Learner capability transition

**Before:** can inspect representation and round-trip evidence but may equate measured speed with algorithmic complexity or passing examples with correctness.

**After:** can count meaningful operations, compare asymptotic growth, choose among a deliberately small set of data-structure interfaces under a stated workload, state a specification and invariant, construct a counterexample, and distinguish tractability intuition from decidability intuition.

Primary module capability remains **Correctness**. This module completes the S1 Judge and Estimate exit evidence.

### 5.2 Explicit non-goals

No competitive-programming repertoire; no Master theorem; no recurrence catalog; no formal asymptotic proof course; no graph-algorithm survey; no dynamic-programming track; no NP-completeness/reductions; no Turing-machine construction; no proof assistant; no standalone discrete-mathematics sequence. Timing is not the primary proof of Big-O.

### 5.3 Existing preliminary Lesson mapping

| Lesson | Existing topic | Design responsibility |
|---|---|---|
| **L02-01** | complexity as growth; counting/order-of-magnitude toolkit | Build operation-count and growth intuition before measurement. |
| **L02-02** | list/hash/tree trade-off | Workload + interface + growth + cost; canonical Trade-off first home. |
| **L02-03** | abstraction/interface; intuitive computation; expressibility/tractability/decidability; specification/invariant/correctness | Canonical first homes for Specification, Invariant, Correctness; bounded limits intuition. |

### 5.4 Canonical concepts introduced vs previewed/revisited

Canonical first introductions:

- **EC-CON-006 Trade-off — L02-02**
- **EC-CON-007 Specification — L02-03**
- **EC-CON-008 Invariant — L02-03**
- **EC-CON-009 Correctness — L02-03**

Revisited: Abstraction, Interface, State, Representation. M01 round-trip evidence becomes an explicit application of the newly defined Specification/Invariant/Correctness vocabulary after its canonical home appears.

### 5.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisite: M00. M01 is soft/preferred; canonical path completes M01 first. L02-01 cross-Module hard prerequisite remains M00.

Support:

- a compact powers/log-as-halvings/order-of-magnitude reference;
- operation-count tables before symbols;
- small supplied interfaces/examples rather than syntax-heavy learner implementations;
- one concrete transition/loop before formal vocabulary;
- undecidability remains intuition + stopping point, never a proof prerequisite.

No new H/S edge is created.

### 5.6 Teaching sequence / mechanism exposure

1. Question: what do “fast enough” and “correct” mean before benchmarking?
2. Mental model: input size + representation + operation model → work growth; specification + allowed transitions → correctness.
3. Count work for one pass, nested pass, and halving/search examples.
4. Predict growth and dominant operations for concrete sizes.
5. Compare list/hash/tree-like interfaces under one stated workload.
6. State one specification/invariant; use a supplied flawed transition/lookup to violate it.
7. Explain why tests are evidence for cases, not a complete correctness argument.
8. Judge a data-structure choice with explicit constraint/trade-off.
9. Bound: distinguish expensive growth from “not generally decidable.”

### 5.7 Observation/activity design — specification level

Use one coherent small workload, preferably the same P0 in-process record collection without relying on persistence mechanics:

- compare a linear scan with a key-based lookup structure for exact-key retrieval;
- define input size n and the counted dominant operation;
- compute concrete operation counts at several scales before timing;
- state a small lookup/update specification and application-level invariant;
- provide one intentionally flawed transition or lookup that violates the invariant at a boundary/duplicate/missing case;
- require a constrained choice between two data-structure alternatives with workload assumptions;
- include one transfer case where constants/locality can make asymptotic labels insufficient for a measured-time decision;
- include one short decidability-intuition item clearly separate from performance/tractability.

### 5.8 Required learner evidence

Append:

- operation-count table and asymptotic classification;
- one size/growth estimate with units/assumptions;
- data-structure choice with workload, gain, cost, and When NOT to use;
- explicit specification and invariant for a small transition;
- counterexample/controlled break and corrected reasoning;
- bounded explanation distinguishing “too expensive here” from “not generally decidable.”

### 5.9 Assessment modes

Primary: **Predict, Break, Judge, Explain**. Cumulative: minimal **Recall** for notation and **Transfer** to a new workload/container choice.

### 5.10 Machine-checkable vs reviewer-required evidence

**Machine-checkable:** fixed operation counts; canonical asymptotic labels; supplied counterexample trigger; invariant predicate on fixed transitions where expressible.

**Reviewer-required:** operation-model assumptions; workload fit of the chosen structure; quality of the Trade-off; Specification vs Invariant distinction; Correctness reasoning; tractability-vs-decidability boundary.

### 5.11 Misconceptions

- “Big-O is milliseconds.”
- “O(n) is always faster than O(n²).”
- “Hash lookup is free because it is O(1).”
- “Correct means the tests passed.”
- “Invariant means usually true.”
- “Exponential means impossible.”
- “Undecidable means analysis is useless.”

### 5.12 Hint/support ladder

**Question:** what operation are you counting, and what must remain true after every permitted transition?
**Hint 1:** write n, the dominant operation, and one concrete input size before writing Big-O.
**Hint 2:** separate precondition/specification from the property that must survive transitions; try the smallest boundary/duplicate/missing case.
**Expected Observation:** canonical counts and failing boundary case, without trade-off/correctness explanation.
**Full Explanation:** connect operation model→growth and specification→invariant→correctness, then transfer to a new workload.

### 5.13 Visual/diagram requirements

1. **Growth-by-count visual:** operation count versus n, not elapsed time.
2. **Interface/workload matrix:** same logical operation across a small set of structures with workload assumptions and trade-offs.
3. **Invariant transition diagram:** permitted transitions plus one violating counterexample.
4. **Limits boundary:** visually separate representable, computable-but-expensive, and not-generally-decidable questions without presenting them as one speed continuum.

### 5.14 Provenance/source anchors

Research Dossier §§5, 8–9, 12; Source Register anchors: Open Data Structures (classic teaching), MIT Mathematics for Computer Science and Cornell CS2110 as bounded designer references, Software Foundations for correctness/limits background. Proof-heavy machinery remains outside learner prerequisites.

### 5.15 Module exit criteria

M02 exits when the learner can:

- count operations and compare growth for simple transparent code;
- make an order-of-magnitude work estimate without confusing it with stopwatch evidence;
- choose a data structure for a stated workload and articulate a real Trade-off;
- state a Specification and Invariant, expose one violating case, and explain the correction;
- distinguish tractability intuition from decidability intuition.

### 5.16 Handoff into M03 and S1 completion

S1 is complete here when the shared packet satisfies the S1 exit rule in §8: **Trace, Explain, Correctness, Judge, Estimate** are supported by defensible evidence. No M03/M04 artifact is needed to retroactively complete S1.

M03 asks: **how are these represented computations exposed by a real machine interface, and which observed details come from language semantics, ISA/ABI, or this compiler/build?**

---

## 6. M03 — Machine: ISA & Execution

### 6.1 Learner capability transition

**Before:** can reason about representations, algorithms, interfaces, specifications, and invariants but lacks a programmer-visible machine model.

**After:** can trace one minimal native x86-64 function call from C source to instructions, registers, memory, instruction pointer, and call frame; use disassembly/debugger evidence; locate a bounded crash signal; and label each claim as C language semantics, ISA rule, ABI/platform rule, compiler/build observation, or hosted Linux observation.

Primary module capability remains **Trace**; **Observe** and **Diagnose** begin their S2 assessed growth.

### 6.2 Explicit non-goals

No multi-ISA mastery; no assembly-programming course; no instruction-encoding catalog; no pipeline/speculation/branch-prediction microarchitecture; no ELF/linker/loader deep dive; no virtual-memory explanation; no exploit-development/buffer-overflow training; no broad C course; no M06 xv6/QEMU/RISC-V setup.

### 6.3 Existing preliminary Lesson mapping

| Lesson | Existing topic | Design responsibility |
|---|---|---|
| **L03-01** | ISA, registers, instruction execution, disassembly | Establish ISA as the software-visible machine interface and trace a bounded source↔instruction path. |
| **L03-02** | function call, stack frame, call/return, stack-overflow intuition | Observe ABI calling convention, register/stack roles, one local memory value, call/return. |
| **L03-03** | memory access, address validity, crash/segfault | Canonical first home of Failure; induce/observe one bounded native failure and separate signal from root-cause claim. |

### 6.4 Canonical concepts introduced vs previewed/revisited

Canonical first introduction: **EC-CON-010 Failure — L03-03**.

Revisited: Representation, Interface, State, Specification/Correctness where relevant. ABI is treated as an Interface application, not a new canonical concept. Process remains reserved for M06; Isolation for M07; neither is defined early.

### 6.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisites remain exactly **M02 and M01**. Cross-Module lesson prerequisite for L03-01 remains **L01-01 and L02-02**.

Support:

- C is a microscope: supply the minimal source and explain only syntax needed for the case;
- provide an x86-64 register-role legend for the exact fixture, not an architecture encyclopedia;
- disassembly view highlights the small instruction region relevant to the source;
- GDB commands are supplied as an observation path;
- stack diagram precedes raw addresses;
- debugging questions ask “what do we know from this observation?” before “why did it happen?”

### 6.6 Canonical machine case and preflight gate

The canonical case is one **native x86-64 source → machine observation path**, conditional on preflight reporting x86-64 in the canonical environment.

Use minimal C only: a single small source file containing main plus one deliberately non-inlined helper. The helper should use two scalar arguments plus a pointer to a tiny record/array and one observable local value. Exact compiler flags, instruction sequence, register allocation, prologue/epilogue, and stack offsets are implementation observations and must not be presented as language guarantees.

The implementation must choose a debug-friendly build that preserves source mapping and an observable call frame while keeping the generated code small. If optimization changes an observation, that is explicitly compiler/build evidence, not a contradiction of C or the ISA.

### 6.7 Claim-layer discipline

| Claim layer | What may be taught/assessed |
|---|---|
| **C language semantics** | source-level values/objects, valid access assumptions, function semantics; invalid access may enter undefined behavior and must be labeled as such |
| **x86-64 ISA** | programmer-visible instructions/registers/addressing semantics actually used by the bounded trace |
| **System V AMD64 ABI / platform ABI** | calling convention and register/stack obligations relevant to the observed call |
| **compiler/build observation** | exact instruction selection, allocation, frame layout, optimization outcome, source mapping for this build |
| **hosted Linux observation** | debugger behavior and observed signal/termination for the controlled failure; not a universal C guarantee |

No evidence item may silently promote an implementation observation into an ISA/ABI/language guarantee.

### 6.8 Teaching sequence / mechanism exposure

1. Question: what does this C function actually execute on this machine?
2. Mental model: source operation → compiler artifact → ISA instructions → register/memory state transitions → call boundary.
3. Preflight: confirm canonical x86-64 + toolchain + debugger capability.
4. Predict: arguments/result and one likely state transition before disassembly/debugging.
5. Observe L03-01: source-aware disassembly; identify function boundaries and a small instruction path.
6. Observe L03-02: stop before/inside/after helper; inspect instruction pointer, relevant registers, stack pointer/frame, and one local/pointee memory value.
7. Break L03-03: trigger one safe bounded invalid-access/crash variant; record exact observed signal/stop.
8. Explain: classify every major claim by language / ISA / ABI / compiler-build / hosted observation.
9. Transfer: compare one tiny RISC-V specification excerpt only to identify what belongs to ISA versus ABI/compiler choice.

### 6.9 Observation/activity design — specification level

The activity must provide:

- fixed minimal C source;
- canonical x86-64 preflight;
- disassembly of named functions;
- at least three debugger observation points: caller before call, callee after entry, caller after return;
- inspection of instruction pointer, relevant argument/result registers, stack pointer/frame information, and one concrete memory value;
- a source↔instruction↔register/memory trace;
- one controlled failure variant with cleanup/reset;
- an explicit claim-layer labeling exercise.

The failure should be pedagogically bounded. If it relies on C undefined behavior, the design must say so and restrict the conclusion to the observed hosted implementation. Do not infer virtual-address mechanics, memory protection, or OS process semantics before their canonical homes.

### 6.10 RISC-V transfer boundary

RISC-V is a **bounded specification/transfer reference only**:

- use one short ratified-spec excerpt or tiny instruction comparison to ask which concepts are ISA-generic versus x86-64-specific;
- no RISC-V toolchain requirement;
- no QEMU;
- no xv6;
- no second assembly exercise;
- no claim that the RISC-V ABI is identical to x86-64.

M06 owns later xv6/QEMU/RISC-V setup if the canonical architecture still requires it.

### 6.11 Required learner evidence

Append:

- M03 preflight recheck with architecture/toolchain/debugger capability;
- source↔instruction mapping for the bounded helper;
- before-call / in-callee / after-return register/memory observations;
- call-frame sketch tied to actual observed addresses/values;
- one controlled failure observation;
- claim-layer table labeling C / ISA / ABI / compiler-build / hosted observation;
- one “fact vs guess” note naming what the evidence cannot establish;
- bounded RISC-V transfer answer.

### 6.12 Assessment modes

Primary: **Predict, Explain, Break**. Cumulative: **Connect** representation/interface from S1; **Transfer** through the RISC-V specification reference.

### 6.13 Machine-checkable vs reviewer-required evidence

**Machine-checkable:** architecture gate; compile/link/run; named symbols; disassembly existence; breakpoint/stop success; required register/memory capture fields; expected controlled-failure termination class for the pinned implementation; cleanup/reset.

**Reviewer-required:** source↔instruction trace correctness; call-frame interpretation; C-vs-ISA-vs-ABI-vs-compiler distinction; diagnostic restraint around the crash; quality of the RISC-V transfer.

### 6.14 Misconceptions

- “C defines which register holds a variable.”
- “The compiler output is the ISA specification.”
- “The stack frame has one universal shape.”
- “Every local variable must be on the stack.”
- “A segmentation fault proves the exact root cause.”
- “An invalid C access is guaranteed to segfault.”
- “A virtual address is already understood because GDB printed an address.”
- “Learning x86-64 means memorizing instructions.”
- “RISC-V should be set up now because xv6 uses it later.”

### 6.15 Hint/support ladder

**Question:** which observed fact belongs to source semantics, ISA, ABI, or this build?
**Hint 1:** mark call boundary, argument/result values, instruction pointer, and one memory value.
**Hint 2:** compare the compiler output with the ABI obligation: which details could change while the call still works?
**Expected Observation:** supplied breakpoint locations and expected value relationships, not the full claim-layer explanation.
**Full Explanation:** walk source→instruction→state transition and classify each guarantee/observation; then repeat classification on the bounded RISC-V transfer item.

### 6.16 Visual/diagram requirements

1. **Source↔instruction↔state trace:** must connect exact source operations to a small instruction range and changing registers/memory.
2. **Call-frame snapshot:** must show caller/callee boundary, instruction pointer, stack pointer/frame region, arguments/results, and one local/pointee without claiming a universal layout.
3. **Claim-layer visual:** C semantics / ISA / ABI / compiler-build / hosted OS evidence as separate layers with examples from the same trace.
4. **Failure evidence visual:** prediction → invalid operation → observed signal/stop → bounded conclusion, with “not proven” callout.
5. **RISC-V transfer card:** one bounded comparison showing ISA-level transfer without environment/toolchain expansion.

### 6.17 Provenance/source anchors

Research Dossier §§6, 9–10, 12; Source Register anchors: GNU objdump documentation (IMPLEMENTATION), GDB machine-code/register/memory documentation (IMPLEMENTATION), WG14/C language material for source semantics (SPECIFICATION), and ratified RISC-V specs (SPECIFICATION). For the x86-64 case, use the current official **AMD64 Architecture Programmer’s Manual** (AMD, publication 40332 and relevant application/instruction volumes) as ISA authority and the **x86-64 System V psABI** project maintained at `https://gitlab.com/x86-psABIs/x86-64-ABI` as ABI authority; both source routes were checked 2026-08-30. Tool output is observation evidence, not the ISA/ABI specification. Current hosted behavior remains implementation evidence and is smoke-tested before release.

### 6.18 Module exit criteria

M03 exits when the learner can:

- trace the bounded x86-64 function call through source, instructions, registers, memory, and call frame;
- use disassembly/debugger output as evidence rather than explanation;
- observe and diagnose one bounded failure without overclaiming causality;
- correctly classify key claims by language / ISA / ABI / compiler-build / hosted observation;
- transfer the ISA-vs-implementation distinction to one RISC-V specification reference.

### 6.19 Handoff into M04

M04 keeps the native machine path but changes the question from “what executes?” to **“why can the same logical work take different time when memory access order changes, and what can measurement actually support?”**

---

## 7. M04 — Memory Hierarchy, Locality & Measurement

### 7.1 Learner capability transition

**Before:** can inspect native execution but may treat memory as uniform and a single timing result as causal proof.

**After:** can explain hierarchy/caching at the needed level, predict how access order changes locality, run a fair repeated timing experiment, retain raw values, summarize central tendency/variation, consider competing explanations, and state a bounded causal/inference claim.

Primary module capability remains **Observe**, with Diagnose, Estimate, Explain, and Judge exercised in the canonical S2 pattern.

### 7.2 Explicit non-goals

No cache-coherence protocols; no set-associativity math course; no branch-prediction/SIMD track; no full microarchitecture; no storage hierarchy teaching beyond clearly marked order-of-magnitude context; no privileged-counter requirement; no formal statistics sequence; no production benchmarking claim from a microbenchmark; no “cold cache” ritual that cannot be defended.

### 7.3 Existing preliminary Lesson mapping

| Lesson | Existing topic | Design responsibility |
|---|---|---|
| **L04-01** | memory hierarchy; cache; latency ladder | Canonical first home of Caching; expose hierarchy and motivate access-order effects. Locality language may be previewed but not canonically defined here. |
| **L04-02** | locality/layout; applied measurement-uncertainty toolkit + experimental pattern | Canonical first home of Locality and first assessed home of measurement uncertainty / experiment pattern. Run the controlled locality experiment and bound inference. |

**Integration note:** the preliminary Lesson map contains wording that can read as “FI: locality” at L04-01, while the higher-authority Concept Registry places EC-CON-012 Locality at L04-02. This design follows the Concept Registry: L04-01 previews/motivates; L04-02 is the canonical first home. No canonical artifact is edited here.

### 7.4 Canonical concepts introduced vs previewed/revisited

- **EC-CON-011 Caching — first home L04-01**
- **EC-CON-012 Locality — first home L04-02**

Revisited: Representation, Trade-off, State, Correctness, Interface as needed. No new statistics concept ID is introduced; the measurement-uncertainty toolkit remains the canonical applied pattern at L04-02.

### 7.5 Prerequisites and hidden-prerequisite support

Hard Module prerequisite remains **M03**. L04-01 cross-Module hard prerequisites remain **L03-01 and M01**.

Support:

- provide hierarchy/latency orders as approximate, hardware-dependent context rather than constants to memorize;
- introduce median/IQR through the learner’s own repeated values, not a statistics prerequisite;
- supplied harness owns timing boilerplate and correctness checksum;
- no perf knowledge required;
- if M03 debugger is unavailable due environment failure, repair preflight rather than weaken M04’s conceptual standard.

### 7.6 Teaching sequence / mechanism exposure

1. Question: why can two loops doing the same logical work take different time?
2. Mental model: memory hierarchy + caching + spatial/temporal locality; access pattern changes reuse/cost opportunities.
3. Predict: choose which of two access patterns should be faster and why.
4. Baseline: same data, same arithmetic, canonical row-major traversal.
5. Controlled change: column-major traversal of the same row-major contiguous data; only access order changes.
6. Warmup: untimed warmups; make no “cold cache” claim.
7. Measure: monotonic high-resolution timing; repeated trials; counterbalanced order.
8. Preserve: retain every raw trial + environment/build/workload/checksum metadata.
9. Summarize: median + IQR + median ratio; optional percentiles only with a larger sample justified by a question.
10. Diagnose: compare within-pattern variation, outliers, and competing explanations.
11. Conclude: bounded claim consistent with locality/cache hierarchy; no exact cache-level causal claim without stronger evidence.
12. Optional corroboration: perf counters only when already available; never required.

### 7.7 Observation/activity design — canonical locality experiment specification

#### Hypothesis

For the same contiguous row-major two-dimensional fixed-width integer dataset and the same logical arithmetic over every element, row-major traversal will generally have lower elapsed time than column-major traversal in the canonical environment because adjacent accesses better exploit spatial locality and cache-line reuse.

The learner records this before timing.

#### Baseline

Row-major traversal of the fixed dataset. The harness verifies the same element count and result/checksum as the changed condition.

#### Controlled access-pattern change

Column-major traversal of the same underlying row-major allocation. Dataset, element type, total element count, source-level arithmetic, compilation mode, process invocation, and result validation remain the same; traversal order is the intended controlled source-level variable. Implementation must also inspect the resulting builds closely enough to detect a compiler transformation that would make a locality-focused causal story misleading.

#### Dataset/workload

Use one contiguous fixed-width integer matrix large enough that the two traversal orders expose a stable locality effect yet small enough for hosted learner sessions. An implementation starting candidate is approximately 64 MiB of data, for example 4096×4096 32-bit elements, but the exact dimension is **implementation-tunable**, not a curriculum pin.

The implementation must prevent dead-code elimination and must check semantic equivalence via a stable checksum/result. The measured arithmetic/checksum path must have **defined language semantics** (for example, a provably non-overflowing accumulator or unsigned/modular arithmetic where appropriate); no signed-overflow or other undefined behavior may be used to keep the loop alive.

#### Warmup policy

At least **2 untimed warmup traversals per pattern** before recorded trials. Warmup is described only as reducing obvious first-run/setup effects. It must not be presented as proof of a specific cache state and must not claim a clean “cold cache” baseline.

#### Repetitions and order

At least **15 recorded trials per pattern** for the canonical learner activity. Use counterbalanced AB/BA order or a fixed-seed randomized pattern order to reduce systematic order bias. Implementation may increase repetitions after smoke testing; it must not silently lower the minimum without Design review.

#### Raw evidence retention

Each recorded trial stores:

- access pattern;
- trial number and execution order;
- monotonic elapsed time in ns or equivalently precise unit;
- matrix dimensions and total bytes;
- checksum/result;
- environment/preflight reference;
- compiler/build identifier and flags selected by implementation;
- optional counter values only if perf is available.

Raw trials are first-class evidence and are retained even when the summary excludes or discusses an outlier.

#### Summary statistic

Required: **median elapsed time for each pattern**, **IQR for each pattern**, and **median ratio/change** between patterns.

Percentiles are not required for the 15-trial Core sample; p95/p99 should not be manufactured from a sample too small to support the intended interpretation. If implementation increases sample count and a question makes percentiles useful, they may be supplemental.

#### Variation

The learner must compare between-pattern difference with within-pattern spread and note visible outliers/instability. A single run cannot satisfy M04 exit evidence.

#### Competing explanations

The activity provides a checklist and requires at least two relevant alternatives/conditions such as:

- scheduler/host virtualization noise;
- CPU frequency/thermal changes;
- compiler optimization/vectorization differences;
- hardware prefetch behavior;
- TLB/page-fault effects;
- cache-state/order effects;
- timer overhead relative to workload duration.

The learner need not eliminate every alternative; they must say which are controlled, checked, plausible, or unresolved.

#### Bounded conclusion

Acceptable Core form:

“Under the recorded environment/build/workload, changing only traversal order changed the timing distribution in the predicted direction by an amount compared with the observed run-to-run variation. The result is consistent with spatial-locality/cache-hierarchy effects. Without stronger mechanism evidence such as validated hardware counters, this experiment does not identify one exact cache level or prove a universal machine-independent speedup.”

#### Inference limits

Do not infer:

- exact cache-miss counts without counter evidence;
- exact cache level as the unique cause;
- behavior on all CPUs/compilers/data sizes;
- production workload speedup;
- filesystem/storage effects;
- a truly controlled “cold cache” state;
- that a benchmark alone proves cause.

### 7.8 Core timing contract and perf boundary

Core completion uses a monotonic high-resolution timing source available in the baseline, with its resolution metadata recorded. No privileged counters are required.

**perf may strengthen evidence** by corroborating hardware-event changes when already available, but:

- preflight marks it optional;
- restricted/unavailable perf produces no learner penalty;
- the activity must not request weaker host/container security;
- the Core explanation remains valid using timing + controlled-design evidence;
- counter interpretation must itself be bounded by event availability/multiplexing/environment limits.

### 7.9 Required learner evidence

Append:

- M04 preflight/timer record;
- hypothesis before data;
- baseline vs controlled-change definition;
- dataset/workload/build metadata;
- warmup and trial-order record;
- at least 15 raw trials per pattern;
- checksum/equivalence evidence;
- median + IQR + median ratio/change;
- variation/outlier note;
- at least two competing explanations;
- bounded conclusion + inference limits;
- optional perf corroboration clearly labeled optional when present.

### 7.10 Assessment modes

Primary: **Predict, Explain, Judge**; **Break** may use a deliberately unfair experimental variant only as a repair exercise, not as the assessed result. Cumulative: **Transfer** to a new access-pattern/layout question.

### 7.11 Machine-checkable vs reviewer-required evidence

**Machine-checkable:** timer capability; workload dimensions/bytes; same checksum; required warmups/repetitions; counterbalanced/fixed-seed ordering; raw-trial completeness; median/IQR/ratio arithmetic; environment/build metadata; perf remains optional.

**Reviewer-required:** hypothesis quality; controlled-variable reasoning; explanation of locality/cache mechanism; interpretation of variation; competing explanations; causal restraint; inference limits; whether the conclusion matches the evidence.

### 7.12 Misconceptions

- “Memory has one latency.”
- “Cache means durable/authoritative storage.”
- “Locality and caching are the same thing.”
- “One faster run proves the cause.”
- “Median removes the need to inspect variation.”
- “p95 is always better than median.”
- “Warmup means the cache is now in a known state.”
- “perf is required for performance work.”
- “Hardware counters prove causality automatically.”
- “A microbenchmark predicts production speedup.”

### 7.13 Hint/support ladder

**Question:** what changed, what stayed fixed, and how large is the effect compared with normal variation?
**Hint 1:** write baseline/change/workload/metric and semantic-equivalence check before interpreting timing.
**Hint 2:** inspect raw trials, median, IQR, execution order, and at least two competing explanations.
**Expected Observation:** provide the expected qualitative direction for a smoke-tested canonical fixture, never a fixed runtime or required speedup ratio.
**Full Explanation:** connect access order→spatial locality→cache opportunity, then state exactly what timing evidence can and cannot establish. Independent transfer uses a new small layout/access pattern.

### 7.14 Visual/diagram requirements

1. **Memory hierarchy visual:** demonstrate relative hierarchy and caching relationships; latency values, if shown, are approximate/contextual.
2. **Row-major vs column-major address walk:** demonstrate identical elements/arithmetic but different address adjacency/order.
3. **Cache-line/locality visual:** demonstrate how adjacent row-major accesses reuse fetched neighboring bytes; avoid claiming exact hardware internals beyond evidence.
4. **Experiment funnel:** hypothesis → baseline → controlled change → metric/environment/workload → warmup/repetitions → raw evidence → summary/variation → competing explanations → bounded conclusion.
5. **Raw-to-summary visual:** show trial dots/values, median, IQR, and why one run/outlier is insufficient.
6. **Inference-boundary callout:** “consistent with” versus “proves exact cache-level cause.”

### 7.15 Provenance/source anchors

Research Dossier §§7, 9–10, 12; Source Register anchors: Python 3.12 time documentation for monotonic/high-resolution timing (IMPLEMENTATION), Linux perf security documentation for optional-counter constraints (IMPLEMENTATION/CURRENT PRACTICE), NIST measurement material for measurement/uncertainty principle, canonical assessment architecture for the experimental pattern. Current hardware behavior is re-smoke-tested before learner release.

### 7.16 Module exit criteria

M04 exits when the learner can:

- explain hierarchy/caching/locality at the bounded mechanism level;
- design/run the canonical fair access-order measurement;
- retain raw evidence and compute required summaries;
- compare effect size direction with within-pattern variation;
- name plausible competing explanations;
- state a bounded, causally restrained conclusion and inference limits;
- complete Core evidence without perf.

### 7.17 Handoff into M05

M03/M04 supply machine and measurement evidence to early S2. They do **not** complete S2. M05 still owns the source→language/runtime/compiler pipeline needed before the S2 checkpoint can be complete.

---

## 8. Compact S1 / early-S2 evidence packet

The slice uses **one logical evidence packet**, not an administrative artifact per Module. A single real observation may support more than one competency claim when the reviewer can point to the supporting evidence.

### 8.1 Packet shape

| Packet section | First populated | Reused/extended by | Evidence purpose |
|---|---|---|---|
| **A. Environment / preflight header** | M00 L00-02 | M03/M04 capability rechecks | Reproducibility and observation context |
| **B. System/P0 path trace** | M00 | M01/M02 optional annotations | Trace interfaces/state/boundaries |
| **C. Representation trace** | M01 | M03 representation revisit | Bytes, range, UTF-8, endianness, round trip, size |
| **D. Computation/correctness** | M02 | later transfer | Counts/growth, trade-off, spec, invariant, counterexample |
| **E. Machine trace** | M03 | M04 build provenance | Source↔instructions↔registers/memory/call frame; failure |
| **F. Measurement record** | M04 | eventual S2 checkpoint | Hypothesis, raw trials, summary, variation, alternatives, bounded conclusion |
| **G. Transfer/uncertainty index** | starts M00 | extended throughout | Support level, remaining unknowns, transfer evidence |

### 8.2 When S1 evidence is complete

S1 evidence becomes complete **at M02 exit**, not after M03/M04. The packet must support the canonical S1 Stage-exit competencies:

- **Trace:** bounded path/data/state trace;
- **Explain:** representation/mechanism explanation with boundary;
- **Correctness:** explicit spec/invariant plus violating/corrected case;
- **Judge:** constrained representation/data-structure/evidence choice;
- **Estimate:** byte-size and/or operation-growth estimate with assumptions.

M00 L00-02 remains the first Core evidence/investigation home.

### 8.3 Early S2 evidence status

M03 and M04 append real machine/debugging and measurement evidence that can feed the eventual S2 checkpoint. The packet must label its state:

**S2 evidence: PARTIAL — M03/M04 complete; M05 required before S2 checkpoint.**

This avoids pretending M05 has been completed. No S2 Stage-exit claim is made solely from this issue.

### 8.4 Support metadata

For each assessed artifact, record the highest support used: Independent / Hint 1 / Hint 2 / Expected Observation / Full Explanation. Hint use is diagnostic, not automatic failure. After Full Explanation, that attempt is remediation evidence; independent competence may be re-established with a short new-context Transfer check.

---

## 9. P0 boundary and earliest checkpoints

P0 is an integration surface, never a curriculum prerequisite. No P edge becomes H or S.

### 9.1 Learner-owned scope allowed in M00–M02

Learner-owned P0 scope may include:

- process-local data model;
- state transitions;
- representation/serialization;
- one application-level invariant;
- byte/growth size estimate.

The persistence boundary remains course-supplied and opaque. The learner may invoke save/load behavior if the fixture needs a restart-visible integration surface, but must not infer or be taught durability guarantees from it.

### 9.2 Design preference for the supplied persistence fixture

**Preference: a course-supplied simple-file persistence fixture behind a narrow opaque save/load adapter for the M00–M02 checkpoints.**

Justification: the accepted Research Dossier §11.2 explicitly identifies a simple file as the best fit when the checkpoint is about representation/bytes/restart behavior and when avoiding hidden database semantics reduces conceptual leakage. This preference minimizes the risk of teaching SQL, transactions, query planning, recovery, or SQLite internals before their canonical homes.

**Fallback decision rule for hidden SQLite:** use hidden SQLite only if implementation evidence shows the simple-file fixture creates more accidental complexity or weaker reproducibility than a fully opaque adapter. If SQLite is used, learners must not write SQL, inspect query plans, reason about transactions/journals/pages, or receive persistence/durability claims from the database mechanism. The adapter must make the mechanism deliberately opaque.

This Design preference does not alter the accepted later Mini Cloud App SQLite baseline and does not close OQ-BP-006.

### 9.3 Earliest P0 checkpoint use

- **M00:** map process-local state, interface boundaries, and supplied opaque persistence boundary; preserve one controlled change.
- **M01:** own the record representation/serialization and size estimate; test bounded round trip.
- **M02:** own one application-level invariant/state transition and make a workload/data-structure choice.
- **M03/M04:** optional/revisit only. A tiny P0 record may supply data to the machine trace or a size/locality discussion, but P0 must not become a prerequisite or distort the canonical M03/M04 mechanism case.

### 9.4 Explicitly deferred

Do not teach filesystem durability, fsync/writeback, database internals, SQL/query planning, transactions, recovery, or storage hierarchy in this slice. Persistence is not durability. Those mechanisms retain their later canonical homes.

---

## 10. Learner-validation preparation: first-pilot observation sheet

Learner validation has **not** happened. This section defines what the first pilot should observe and how signals route.

### 10.1 Observation fields

For each learner/session record:

- module/lesson/activity point;
- preflight status and environment reference;
- task attempt + highest support level used;
- prediction quality before reveal/run;
- observed evidence actually produced;
- misconception/error category;
- whether the tool/environment behaved as the activity specification expected;
- whether the learner could explain the mechanism after observation;
- whether a short transfer check succeeded;
- time lost to tooling versus reasoning, as observational context only;
- observer note: design / environment / support candidate;
- confidence and whether the pattern repeated across learners.

### 10.2 Signals that trigger **Design revision**

Escalate to Design revision when the environment works and reasonable support is available, but multiple learners still show a shared mental-model failure such as:

- M00 cannot distinguish observation from explanation after the evidence ladder;
- M01 repeatedly conflates information and representation despite correct tool execution;
- M02 cannot connect specification/invariant to a concrete state transition after bounded examples;
- M03 claim layers remain systematically conflated even when debugger/disassembly observations succeed;
- M04 experiment pattern leads learners to overclaim causality even with raw evidence/variation prompts;
- a visual consistently induces the wrong model;
- cognitive load arises from mechanism scope rather than incidental syntax/tooling.

Do not “repair” such signals by merely adding more commands or hints.

### 10.3 Signals that trigger **environment/preflight repair**

Route to implementation/environment repair when conceptual work is blocked by:

- clean Codespace/container preflight failure;
- architecture not matching the canonical M03 path;
- GCC/binutils/GDB missing or incompatible;
- GDB ptrace/register/memory observation blocked by hosted policy;
- source/disassembly anchors unstable enough to make the task non-reproducible;
- timer capability/resolution broken;
- M04 workload too slow, too short, or locality direction not robust across fresh hosted sessions;
- perf restriction incorrectly blocks Core work;
- reset/evidence paths are not writable/reproducible.

These are not learner competency failures and do not raise prerequisites.

### 10.4 Signals that trigger **hint/support improvement**

Improve scaffolding rather than redesign mechanism when:

- the same shell/Git/C syntax step stalls learners but, once named, they reason correctly;
- learners need vocabulary/diagram orientation but then make correct predictions;
- one command path is hard to discover but the mental model is sound;
- expected observation unblocks interpretation and a later transfer succeeds;
- learners understand the concept but cannot remember non-core tool syntax.

Support revisions must preserve the standard ladder and should not reveal the assessed conclusion before the learner has made a prediction.

### 10.5 Pilot stopping/decision rule

A single learner anecdote is evidence, not a design verdict. Review pilot notes for repeated patterns, environment common-mode failures, and support-sensitive versus support-insensitive misconceptions. The Lead decides whether the next task is direct lesson/activity refinement, environment repair, support improvement, or formal architecture escalation.

---

## 11. Architecture consistency and implementation handoff

### 11.1 Invariants preserved

This Design preserves:

- 7 Stages, 25 Modules, 70 preliminary Lessons;
- 40 hard + 22 soft Module edges;
- M00 L00-02 as first Core evidence/investigation home;
- M04 L04-02 as first assessed measurement-uncertainty / experiment-pattern home;
- exactly 8 competencies;
- 18 canonical concepts and all Concept Registry first homes;
- 15 Big Ideas;
- 5 Required / 5 Optional / 5 Source Expeditions;
- P0–P9 as project mapping, not curriculum DAG;
- existing Lab selection;
- OQ-BP-001/OQ-BP-003 RFC gates;
- OQ-BP-006 as open implementation-time work.

No Required Lab is invented. No runnable implementation or learner-facing Lesson prose is included.

### 11.2 Architecture escalations

**No architecture escalation is required for Design readiness.**

One non-blocking canonical wording inconsistency should be visible to the Web Lead: the preliminary Lesson map’s M04 wording can imply Locality is first-introduced at L04-01, while the Concept Registry canonically assigns EC-CON-012 Locality to M04 L04-02. This design follows the Concept Registry and treats L04-01 as preview/motivation. Per Review Policy, a later direct-fix of wording is preferable to silently changing architecture in Issue #27.

### 11.3 Implementation-specific decisions intentionally deferred

The Lesson/activity implementation task must decide and smoke-test:

- exact immutable Dev Container/Codespace image digest;
- exact package builds;
- exact GCC flags that keep the M03 trace pedagogically stable;
- exact M03 fixture identifiers/line anchors;
- exact M04 dimensions within the designed workload envelope;
- whether optional perf corroboration is exposed when capability exists;
- exact evidence-file formats and automated check scripts.

Those decisions must remain reproducible and current-source-backed, but they do not need architecture review unless they force a curriculum scope/dependency change.

### 11.4 Source/provenance rule for implementation

Every current/version-sensitive implementation claim must be rechecked against the authoritative/current source route already identified in the accepted Research Dossier. Stable principles should cite specification/textbook/classic-course anchors; compiler/debugger/container/timing/counter behavior should cite current official documentation and be smoke-tested in the pinned environment.

### 11.5 Readiness conditions passed by this Design

The Design is ready to hand off because it specifies, without implementing:

- a coherent M00–M04 capability progression;
- all existing preliminary Lesson mappings and canonical concept homes;
- prerequisites and hidden-prerequisite support;
- mechanism exposure and observation/activity contracts;
- required learner evidence and assessment modes;
- machine-checkable versus reviewer-required evidence;
- misconceptions, hint ladders, visuals, provenance, exits, and handoffs for each Module;
- a shared evidence packet with explicit S1 completion and partial-S2 status;
- an OQ-BP-006-safe preflight contract;
- the bounded native x86-64 M03 canonical path;
- the complete M04 locality experiment and implementation smoke-test obligations;
- the bounded P0 integration surface with opaque persistence;
- first-pilot learner-validation routing.

## 12. Readiness recommendation

READY FOR LESSON / ACTIVITY IMPLEMENTATION
