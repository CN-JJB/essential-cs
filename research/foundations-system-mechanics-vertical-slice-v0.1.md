# Foundations / System Mechanics Vertical-Slice Research Dossier v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #25 — [Post-Blueprint] Foundations/System Mechanics Vertical-Slice Research Dossier v0.1
Repository state researched: `main @ dab37131627fbc09e187300d3235ff6c0a10c57c`
Checked date for current implementation/practice claims: **2026-08-31**
Role: Foundations / System Mechanics Research Architect and Evidence Researcher
Scope: Research step only; no Lesson prose, runnable Lab implementation, Mini Cloud App implementation, Blueprint redesign, or Open Question closure.

## Evidence-layer legend

This dossier uses the project-required evidence layers deliberately:

- **PRINCIPLE** — stable mechanism or reasoning pattern independent of one product/version.
- **SPECIFICATION** — a normative contract from a standard, language specification, ABI, protocol, or similarly authoritative interface definition.
- **IMPLEMENTATION** — behavior or constraint of a particular implementation/tool/environment.
- **CURRENT PRACTICE** — replaceable present-day convention, product choice, or operational pattern.

Confidence/context labels:

- **ESTABLISHED** — strongly supported by stable primary/authoritative evidence and broad systems practice.
- **IMPLEMENTATION-SPECIFIC** — valid only for the named implementation/version/environment.
- **CURRENT-PRACTICE** — useful now but expected to need periodic review.
- **CONTESTED** — credible sources/practices disagree under comparable assumptions.
- **UNCERTAIN** — evidence is incomplete or the design choice needs learner validation.

---

## 1. Executive Summary

This first post-Blueprint slice is well chosen because M00–M04 creates a complete, testable chain from **system-map reasoning → representation → computation → machine execution → memory/locality measurement** before the curriculum asks learners to reason about operating systems, persistence mechanisms, networking, databases, or distributed systems. The slice establishes the vocabulary and evidence habits that every later systems claim depends on, while remaining bounded enough for a first learner pilot.

The main research conclusion is **READY FOR DESIGN**. No architecture blocker was found. The canonical Module DAG, Stage structure, competency model, Concept Registry first homes, Lab architecture, P0–P9 architecture, and open-question states can all be preserved.

The most important design inputs are:

1. **M00 should teach investigation discipline, not tool mastery.** Its canonical contribution is a whole-system map plus the distinction `prediction → observation → explanation → bounded conclusion`. Shell, Git, debugger-light inspection, and environment records are evidence instruments, not course subjects.
2. **M01 should make representation observable.** The smallest accurate core is bits/bytes, binary/hex, bounded integers, two's-complement intuition, overflow boundaries, Unicode/UTF-8, byte order, serialization/encoding, size estimates, and round-trip correctness. Do not expand into digital logic or information theory.
3. **M02 should teach enough theory to support systems judgment, not an algorithms degree.** Count operations, compare growth, use a small set of data-structure interfaces, state specifications/invariants, reason about correctness, and gain bounded intuition for tractability/expressibility/decidability. Competitive-programming patterns and proof-heavy discrete math are outside the slice.
4. **M03 needs one machine case, not multi-ISA mastery.** ISA is the abstraction; registers, memory, program counter, calls/returns, stack frames, ABI intuition, source-to-machine observation, disassembly, and crash/address evidence are enough. For the first slice, native x86-64 in the canonical Linux environment is the lowest-burden implementation case. RISC-V remains valuable as a source/spec comparison and is already justified later for LAB-REQ-02, but QEMU/RISC-V should not be pulled into M03 merely for symmetry.
5. **M04 should establish the applied measurement toolkit through a real locality effect.** Repeated runs, workload/environment records, cold/warm distinctions, medians/percentiles when useful, variation, competing explanations, causal limits, and order-of-magnitude reasoning belong here. `perf` is optional enhancement only; a monotonic high-resolution timer plus controlled access-order experiment must be sufficient when hardware counters are unavailable or restricted.
6. **OQ-BP-006 becomes concrete but should remain open.** The first slice needs a bounded reproducible Linux image and a known Python/compiler/debugger/binutils surface. It does **not** yet need SQLite/PostgreSQL, QEMU/RISC-V cross-toolchains, browser pins, container/orchestration tools, or observability stacks. The recommended baseline is Ubuntu 24.04 LTS / Dev Container `noble`, Python 3.12, GCC 13-class distro toolchain, GNU binutils, GDB, Git, and simple shell utilities; pin the final container image by immutable digest when the runnable preflight is implemented.
7. **P0 must stop before durability/database teaching.** During M00–M04, learners may own the single-process domain model, identifiers, in-memory state transitions, representation/serialization boundary, size estimates, and round-trip/invariant checks. A durable collection may exist as an opaque or partially opaque fixture because P0 canonically includes one durable collection, but durability guarantees, file-system behavior, SQLite internals, transaction semantics, recovery, and database mechanisms must wait for M08/M09/M13/M14. Project order remains non-DAG.

No new Required Lab is recommended for M00–M04. The accepted 5/5/5 Lab architecture remains intact. Early hands-on work should be lightweight observations/checkpoints unless later Design work demonstrates a genuine Lab need without changing the canonical Lab selection.

---

## 2. Slice Contract

### 2.1 Purpose

**PRINCIPLE — ESTABLISHED.** The slice exists to give a non-CS learner an evidence-grounded answer to five linked questions:

1. What kind of system am I looking at, and what counts as evidence about it? (`M00`)
2. How is information represented in finite machine-readable forms? (`M01`)
3. What does it mean for a procedure to compute correctly and at what growth cost? (`M02`)
4. How does a real machine expose execution through an ISA and ABI? (`M03`)
5. Why does where/how data is accessed change observed time, and what can a measurement actually establish? (`M04`)

This is the first production/pilot slice because its outputs are reusable reasoning capabilities rather than narrow topic knowledge. Later Modules assume learners can distinguish interface from implementation, state from storage, observation from explanation, representation from information, rough estimate from measurement, and a machine-level fact from a guess.

### 2.2 Learner entry assumptions

Preserve the accepted Learner Profile exactly:

- understands variables, conditions, loops, functions, and basic data flow;
- can read and run a short Python or JavaScript program and make a small change;
- approximately high-school mathematics;
- no prior algorithms course, discrete mathematics, C, assembly, Linux administration, networking, databases, OS course, shell fluency, Git expertise, cloud platform, or professional engineering experience is assumed;
- Bridge is optional/skippable and outside the Core DAG;
- a sufficiently prepared learner may enter M00 directly without running a diagnostic.

M00 `L00-02` remains the first Core home for the practical evidence workflow. Difficulty with shell/Git/debugging during the slice is therefore a **design/support signal**, not evidence that entry prerequisites should be raised.

### 2.3 Capabilities gained by slice end

By the end of M04, the learner should be able to produce evidence that they can:

- trace a small local system and identify interface/state/representation boundaries;
- predict an observable result before running a tool;
- preserve enough environment/input/output evidence for another person to understand what was tested;
- encode/decode bounded values and text, inspect bytes, estimate size, and detect a failed representation round trip;
- count operations and compare asymptotic growth without confusing Big-O with a stopwatch result;
- state a small specification/invariant and construct a counterexample or boundary case;
- read a short machine-code trace, relate source to instructions/registers/memory/stack, and use disassembly/debugger evidence to update an explanation;
- run a controlled locality experiment, repeat measurements, summarize variation, separate measurement from estimate, and state causal limits.

### 2.4 Canonical concepts first introduced in this slice

Per the current Concept Registry and lesson map, preserve these first homes:

- M00 `L00-01`: **State** (`EC-CON-001`), **Abstraction** (`EC-CON-002`), **Indirection** (`EC-CON-004`), **Interface** (`EC-CON-005`).
- M01 `L01-01`: **Representation** (`EC-CON-003`).
- M02 `L02-02`: **Trade-off** (`EC-CON-006`).
- M02 `L02-03`: **Specification** (`EC-CON-007`), **Invariant** (`EC-CON-008`), **Correctness** (`EC-CON-009`).
- M03 `L03-03`: **Failure** (`EC-CON-010`) — M00 may preview that systems fail, but must not duplicate the canonical definition.
- M04 `L04-01`: **Caching** (`EC-CON-011`).
- M04 `L04-02`: **Locality** (`EC-CON-012`) and the first assessed applied measurement-uncertainty pattern.

### 2.5 Revisited, previewed, and deliberately deferred concepts

Within M00–M04:

- M01 may **apply** invariant/correctness language to round trips before M02 gives the canonical definitions; this must be framed as an intuitive check, not a second first-home.
- M03 revisits Representation/Interface in registers, memory, object files, and calls.
- M04 revisits Trade-off and Representation through layout/access order.
- Process, Isolation, Trust Boundary, Durability, Consistency, Concurrency, database transactions, networking, and distributed failure remain later canonical homes.

### 2.6 Where the slice begins and ends

The slice begins at M00's whole-system map and evidence discipline, after optional Bridge preparation. It ends when M04 has produced the first assessed measurement/locality evidence and a learner can explain what a measured difference **does and does not prove**.

It deliberately ends **before M05 language/runtime/compiler mechanisms** and before OS process/syscall teaching in M06. A source-to-machine observation in M03 is allowed; a compiler-construction or runtime-internals sequence is not.

---

## 3. M00 Research — System Map and Investigation Discipline

### 3.1 Target mental model

**PRINCIPLE — ESTABLISHED.** A useful opening model is not “a computer has CPU/RAM/disk/network” as a component inventory. It is a **path-and-boundary model**:

`input/request → interface → representation → executing state → lower interface(s) → observable output/state change`

At each boundary, ask:

- What is the representation here?
- What state can affect the next observation?
- Which interface/contract is being relied upon?
- Which details are hidden by the abstraction?
- Is there indirection between the name/reference I have and the resource/action I care about?
- What observation could distinguish two competing explanations?

This framing aligns with the canonical definitions of Abstraction, Interface, Indirection, and State while avoiding premature commitments to OS/network/database mechanisms.

### 3.2 Prediction, observation, explanation

The most important opening discipline should be:

`Question → prediction/hypothesis → baseline → observation → explanation candidate → competing explanation → bounded conclusion → preserved evidence`

**PRINCIPLE — ESTABLISHED.** Observation is a report of what a measurement/tool exposed under a stated setup. Causal explanation is a claim about why it happened. One observation can reject a prediction, but a matching observation does not automatically prove the causal story.

For M00, the terms should stay lightweight:

- **Prediction:** a falsifiable expectation written before reveal/run.
- **Observation:** what the system/tool actually exposed.
- **Explanation:** mechanism-level account consistent with the observation and other evidence.
- **Evidence record:** enough context to inspect/reproduce the claim later.

Do not introduce formal statistics here. M04 owns the first assessed uncertainty toolkit.

### 3.3 Evidence preservation and reproducibility

Minimum useful evidence packet for M00:

- question / claim being checked;
- input or fixture identity;
- environment identifier (OS/container, architecture, relevant tool/runtime version when behavior can depend on it);
- command/task executed;
- relevant output/error (trimmed but not cosmetically rewritten);
- baseline vs changed condition when applicable;
- Git diff/commit reference when code/config was modified;
- one sentence separating observation from explanation;
- unresolved uncertainty / next check.

**IMPLEMENTATION — CURRENT-PRACTICE.** Git is useful here because `git diff` provides an exact view of working-tree/index/revision differences. That is evidence preservation, not Git mastery. Official Git documentation defines `git diff` as showing differences among working tree, index, trees, commits, or blobs. The educational stopping point is “use a diff/commit as a reproducible change record,” not branching strategy, rebasing, conflict archaeology, hooks, or advanced history manipulation.

### 3.4 Authoritative-source navigation

M00 should establish a simple evidence hierarchy already encoded in project policy:

1. standards/specifications when the question is about a normative contract;
2. official project/language/tool documentation for supported behavior;
3. implementation source when the question is about what this implementation actually does;
4. classic textbooks/courses/papers for stable explanatory framing;
5. experiments to test behavior in the learner's exact environment;
6. secondary/community material only when it adds interpretation and is cross-checked for important claims.

The learner should practice answering: **“What layer is this source evidence for?”** A standard can define an interface while saying little about one implementation's performance; source code can reveal implementation without defining the language/protocol contract.

### 3.5 Lightweight debugging/investigation workflow

M00 should not teach “the debugger.” It should teach a reusable workflow:

`reproduce → minimize/locate → inspect one boundary → form hypothesis → change one variable → rerun → preserve result → reset`

Allowed tools are whatever most directly answer the question: simple shell commands, file inspection, Python, a debugger-light view, Git diff, or a tiny script. Tool choice should be justified by the observation needed.

### 3.6 AI-generated output boundary

OQ-BP-001 remains open. Safe rule for this slice:

> AI-generated claim, code, configuration, explanation, or documentation is an **untrusted hypothesis** until checked by an authoritative source, test, measurement, or security review appropriate to the claim.

Do not teach prompt technique, model architecture, AI product usage, evaluation taxonomies, or agent workflows as Core content here.

### 3.7 Common M00 misconceptions

- “The diagram is the system.” → A diagram is a model with omitted detail; name its purpose and breaking point.
- “I ran the command, therefore I investigated.” → Tool execution without a question/prediction/interpretation is weak evidence.
- “The output says X, so X caused the problem.” → Observation and causal explanation are separate claims.
- “Reproducible means byte-for-byte identical everywhere.” → For this course, reproducibility means the relevant method/environment is sufficiently specified to repeat the intended observation; some outputs legitimately vary.
- “Git is required because developers use Git.” → Git is included only as a low-friction evidence/change-record mechanism.
- “Linux competence means knowing many commands.” → The course needs task execution and evidence preservation, not Linux administration.
- “Official docs are always the right source.” → They are authoritative for the claims they actually define; a spec, source tree, measurement, or paper may be the correct layer for another claim.

### 3.8 M00 design implication

Design should use a small real system/fixture and require one trace plus one evidence-preserving investigation. The payoff must be visible before introducing tool vocabulary. A learner who already has practical fluency should not be forced through a shell/Git tutorial disguised as Core content.

---

## 4. M01 Research — Information & Representation

### 4.1 Smallest accurate foundation

**PRINCIPLE — ESTABLISHED.** The central idea is: **information is not identical to its representation**. A finite machine carries information through concrete bit/byte sequences under an agreed interpretation. The same information can have several representations with different size, validity, ordering, and interoperability properties.

The necessary Core sequence is:

1. bit as a binary state/symbol in an encoding model;
2. byte as the common addressable/octet-sized unit in the canonical environment;
3. positional notation: binary ↔ hexadecimal ↔ decimal for bounded values;
4. unsigned integer range as a finite set;
5. signed integer representation, with two's-complement intuition and representable bounds;
6. overflow/boundary behavior distinguished by language/specification rather than assumed from hardware;
7. text: Unicode code points vs encoding forms, with UTF-8 as the main byte-oriented case;
8. serialization/encoding as a representation boundary;
9. byte order for multi-byte values;
10. size estimates and round-trip correctness.

### 4.2 Bits, bytes, binary, hexadecimal

The mathematics needed is only positional notation and powers of two:

- `n` bits distinguish up to `2^n` bit patterns;
- one hexadecimal digit corresponds exactly to four bits;
- two hex digits conveniently represent one 8-bit byte;
- ranges and size estimates should be done with powers of two and rough decimal equivalents when useful.

Avoid Boolean algebra, gates, Karnaugh maps, transistor logic, Shannon entropy, coding theory, or arbitrary base-conversion drill volume. The learner needs to **inspect and reason about bytes**, not become fast at hand conversion.

### 4.3 Signed integers and two's complement

**SPECIFICATION — ESTABLISHED for C23; version-sensitive for older language standards.** WG14's current home records C23 as ISO/IEC 9899:2024. C23 standardized two's-complement representation for signed integers. WG14 proposal history explicitly notes that C23 permits only two's complement as the signed representation.

Teaching implication:

- explain two's complement as the canonical modern signed-integer representation;
- use fixed-width examples (for example, 8-bit pedagogical integers) to make bounds visible;
- distinguish **representation** from **arithmetic semantics in a programming language**;
- do not teach “signed overflow always wraps.” In C, signed arithmetic overflow remains a language-semantics issue and must not be inferred simply from two's-complement hardware representation; unsigned arithmetic has modulo semantics under the language rules.

This distinction is a high-value early example of PRINCIPLE vs SPECIFICATION vs IMPLEMENTATION.

### 4.4 Unicode and UTF-8

**SPECIFICATION — ESTABLISHED.** Unicode 17.0 is the current published Unicode Standard at the checked date. Unicode defines code points and encoding forms; UTF-8 maps Unicode scalar values/code points (excluding surrogate code points as appropriate) to byte sequences. Unicode's official FAQ emphasizes that UTFs are reversible mappings and that UTF-8 is byte-oriented.

Bounded teaching requirements:

- “character” is overloaded; distinguish user-perceived grapheme, Unicode code point, and encoded bytes only as far as needed to avoid false assumptions;
- UTF-8 uses variable-length byte sequences;
- byte length is not the same as human-visible character count;
- valid byte sequences and decoding errors matter for correctness;
- UTF-8 has no multi-byte endianness problem because it is interpreted as a byte sequence;
- normalization/grapheme segmentation can be mentioned as a stopping-point warning, not taught in depth in this slice.

### 4.5 Serialization and encoding

**PRINCIPLE — ESTABLISHED.** Serialization makes an in-memory/logical structure into a representation suitable for storage/transmission and later interpretation. “Encoding,” “serialization,” and “schema” are related but not interchangeable.

Core learner questions:

- What information is preserved?
- What type/length/delimiter/version assumptions are needed to decode?
- Is the mapping injective/reversible for the permitted inputs?
- How are malformed/unknown inputs handled?
- What is the byte-size overhead?

JSON may be used as a familiar example, but JSON syntax/products must not become the concept. A simpler custom fixed fixture or Python standard-library encoding may be better for a round-trip observation.

### 4.6 Byte order / endianness

**PRINCIPLE — ESTABLISHED.** Endianness concerns the order in which bytes of a multi-byte value are arranged in memory or a byte stream under a given representation. It matters only after the representation has chosen a multi-byte unit/value layout.

Bounded activity: take a known integer, serialize/pack it in explicit little- and big-endian forms, inspect bytes, and round-trip decode. Do not expand into bus protocols or architecture history.

Python's official `struct` documentation is a practical implementation surface because it lets the format explicitly choose native, little-endian, or big-endian byte order, separating host implementation from the intended serialized format.

### 4.7 Representation correctness and round trips

A strong M01 correctness pattern is:

`value → encode → bytes → decode → value'`

Then ask which invariant should hold for the valid input domain. Useful failures include:

- value outside representable integer range;
- malformed UTF-8;
- using a different byte order on decode;
- ambiguous delimiter/length encoding;
- truncation;
- size estimate that ignores variable-length encoding.

Do not prematurely formalize the full Specification/Invariant/Correctness definitions; M02 is their canonical first home. M01 can say “round-trip property/check” and revisit the formal terms after M02.

### 4.8 Real observation mechanisms

Low-burden observation choices:

- Python `int.to_bytes` / `int.from_bytes` or `struct` with explicit byte order;
- `bytes.hex()` / a minimal hex dump;
- encode/decode UTF-8 and inspect byte sequences;
- file size via standard filesystem metadata;
- a tiny fixed-format binary fixture.

Avoid requiring `xxd`, `hexdump`, or one exact CLI unless the preflight provides it. The mechanism is byte inspection, not command memorization.

### 4.9 Likely misconceptions

- “Bits contain meaning by themselves.” → Meaning comes from interpretation/representation contract.
- “Hex is how memory stores numbers.” → Hex is a human notation for values/bytes; machine storage is not textual hex by default.
- “One character = one byte.” → False for UTF-8 in general.
- “One Unicode code point = one visible character.” → Often false; mention grapheme clusters as a boundary.
- “UTF-8 is little-endian on my laptop.” → UTF-8 is byte-oriented and not endian-swapped like UTF-16/32 code units.
- “Two's complement means every language's signed overflow wraps.” → Representation does not define all language arithmetic semantics.
- “Serialization is just converting to a string.” → It is a representation contract, which may be textual or binary.
- “If encode/decode works once, the format is correct.” → Boundary/malformed inputs and domain assumptions matter.

### 4.10 M01 source guidance

Use Unicode Standard/FAQ for Unicode/UTF-8 specification; WG14/C23 sources for signed representation/version distinctions; Python official docs only as an implementation surface; classic introductory courses such as CS50 for low-cognitive-load binary/hex visualization, without copying course prose/figures unless rights are explicitly cleared.

---

## 5. M02 Research — Computation & Algorithms

### 5.1 Bounded Core goal

M02 should give the learner the smallest theory needed to reason about later systems costs and correctness:

- algorithm = finite, specified procedure over representations/state under a model;
- count meaningful operations before measuring wall-clock time;
- compare asymptotic growth as input size changes;
- recognize a small set of essential data-structure interfaces and their operation costs;
- state a specification and invariant;
- reason about a simple correctness argument/counterexample;
- distinguish tractable growth from obviously explosive growth;
- understand that some desired computations/specifications cannot be solved generally, without taking a full computability course.

### 5.2 Counting operations and asymptotic growth

**PRINCIPLE — ESTABLISHED.** Big-O is an asymptotic upper-bound notation, not a stopwatch result and not automatically an exact/tight growth claim. Open Data Structures gives a formal definition and explicitly motivates asymptotic notation because exact instruction counts vary by machine and run.

For this learner, start with operation counts on transparent code:

- one pass over `n` items;
- nested loops over `n × n`;
- halving/doubling search;
- repeated append/search in a chosen container;
- compare two alternatives at small/medium/large `n` using order-of-growth reasoning.

Required mathematics:

- arithmetic and powers;
- logarithm intuition as “number of repeated halvings/doublings,” not log-law drill;
- inequalities/order of magnitude;
- optionally simple summation intuition for nested/repeated work.

Not required:

- recurrence-solving technique catalog;
- Master theorem;
- formal proof of asymptotic equivalence classes;
- amortized-analysis machinery beyond one intuitive example if needed for a dynamic array;
- combinatorics beyond a just-in-time example;
- graph algorithm survey.

### 5.3 Essential data structures

The bounded set should be selected by later systems relevance, not degree tradition:

- sequence / dynamic array;
- linked structure as a locality/indirection contrast, not as implementation craft;
- stack / queue as behavior/interface;
- hash table/dictionary;
- tree as hierarchy/search structure;
- priority queue only if a later dependency truly needs it in the first traversal.

The learner should compare **interface + workload + asymptotic cost + representation/layout consequence**, rather than implement every structure from scratch.

### 5.4 Specification, invariant, correctness

**PRINCIPLE — ESTABLISHED.** M02's canonical first home should make three distinctions explicit:

- **Specification:** what behavior is permitted/required under stated assumptions.
- **Invariant:** a property that remains true across permitted transitions under the model.
- **Correctness:** observable behavior conforms to the specification under stated assumptions.

Classic activity pattern: give a tiny algorithm or stateful structure, ask for a postcondition/invariant, then construct a boundary input or mutation that violates the claim. Loop invariants can be used in one bounded example because they connect program execution to correctness, but formal proof calculus is out of scope.

### 5.5 Tractability intuition

Learners need a practical ability to reject obviously explosive approaches. A useful bounded ladder is:

`constant / logarithmic / linear / n log n / quadratic / exponential`

Use concrete input growth and order-of-magnitude operation counts. The goal is not complexity-class taxonomy. `P`, `NP`, reductions, completeness, approximation algorithms, and randomized complexity are Deep Dive unless a later design task explicitly justifies a tiny Current Case.

### 5.6 Expression/representation limits and bounded decidability intuition

The project has already accepted an intuitive treatment of expressibility/decidability limits in M02. The minimum accurate statement is:

- an algorithm operates under a representation and computational model;
- some problems become impractical because required work grows too quickly;
- separately, there are well-specified general questions for which no algorithm can always return the desired answer for every program/input (halting is the canonical intuition);
- this is a **limit of general computation**, not “computers are too slow.”

Do not teach Turing-machine construction, mapping reductions, Rice's theorem, formal-language hierarchy, or undecidability proofs in this slice. A one-page intuition/counterexample-style discussion is sufficient for later humility about static analysis, testing, and automated reasoning.

### 5.7 Classic source/exercise pattern

Useful candidates:

- **Open Data Structures** — bounded asymptotic-notation introduction plus selected sequence/hash/tree interfaces. Explicit CC BY license makes adaptation comparatively safe, but the full book is far beyond Core scope.
- **Cornell CS2110** — classic sequence of searching/asymptotic complexity and loop invariants. Good pedagogical reference; course materials should be treated as link/reference unless item-level reuse rights are explicit.
- **MIT Mathematics for Computer Science** — strong source for invariants/asymptotic/discrete foundations, but too broad/math-heavy to adopt wholesale for this target learner; use as designer evidence/reference, not learner prerequisite.
- **Software Foundations / university computability notes** — bounded halting/decidability intuition only; avoid turning proof-assistant/formal-logic machinery into the activity.

### 5.8 Likely misconceptions

- “Big-O tells me how many milliseconds.” → It describes growth under an operation/model abstraction.
- “O(n) is always faster than O(n²).” → Constants, input range, representation, locality, and implementation matter; asymptotic comparison is not a universal measured-time ranking.
- “Hash table lookup is O(1), therefore free.” → Expected/amortized assumptions and representation/locality costs remain.
- “Correct = tests passed.” → Tests are evidence for cases, not a complete specification proof.
- “Invariant means a condition that is usually true.” → It must hold across permitted transitions under the stated model.
- “Exponential means impossible.” → Input size and constraints matter; the point is scaling risk.
- “Undecidable means no useful tool can analyze programs.” → It means no general algorithm solves the stated problem for every allowed input; bounded/approximate/conservative analyses can still be useful.

---

## 6. M03 Research — Machine / ISA / Execution

### 6.1 Minimal machine model

**PRINCIPLE — ESTABLISHED.** An ISA is an abstraction/interface between software-visible machine operations and an implementation. The learner needs a programmer-visible execution model, not microarchitecture specialization.

Required elements:

- instruction as encoded operation over architectural state;
- registers as small named architectural storage locations;
- memory as byte-addressed state accessed through addresses in the canonical case;
- program counter / instruction pointer;
- load/store or memory-operand intuition depending on selected ISA;
- compare/branch/control flow;
- stack as a conventionally managed memory region used by calls/locals/spills in the selected ABI;
- call/return and stack-frame intuition;
- ABI as a contract/convention for calling, register roles, stack alignment, object format/interface boundaries;
- source → compiler → object/executable → disassembly observation;
- invalid address / crash as evidence hook, while the canonical Failure definition remains M03 `L03-03`.

### 6.2 ISA vs microarchitecture

Teach explicitly:

- **SPECIFICATION:** ISA defines software-visible instructions/state/semantics.
- **IMPLEMENTATION:** a CPU microarchitecture decides how instructions are fetched/decoded/executed internally, with caches/pipelines/speculation etc.
- **CURRENT PRACTICE:** compilers choose instruction sequences under optimization/version/flags.

Do not imply one assembly listing is “what C means” or one processor pipeline is “the ISA.”

### 6.3 Representative ISA/tool choice

#### Candidate A — native x86-64 Linux

**Recommendation for first-slice implementation case: SELECT as default, subject to Web Lead review.**

Why:

- lowest setup burden in typical Codespace/Dev Container Linux environments;
- GNU compiler/binutils/GDB are directly available on Ubuntu;
- System V AMD64 ABI is mature and widely documented;
- learners can compile and inspect a tiny C function without emulator/cross-toolchain setup;
- address-invalidity/stack traces are directly observable on the canonical environment.

Costs:

- x86-64 instruction syntax/encoding is less regular than RISC-V;
- optimizers can produce visually complex code;
- host architecture assumptions need an explicit preflight.

Mitigation: choose tiny functions, compile with debug information and conservative optimization settings for the first observation, and teach only the handful of instructions/registers required by the trace.

#### Candidate B — RISC-V RV64I (+ basic ABI)

**Strong conceptual/spec source; do not require for M03 baseline.** RISC-V International's ratified specification library lists the latest stable unprivileged ISA publication as version `v20260120` at the checked date. RISC-V is attractive pedagogically because the base ISA is regular and specification access is excellent.

However, requiring RISC-V now adds QEMU/cross-toolchain/emulation burden before the accepted LAB-REQ-02 at M06, where that burden already has an explicit curriculum purpose. Use a small RISC-V excerpt as a **transfer/spec comparison** if desired, not as a second mastery target.

#### Candidate C — ARM64/AArch64

Relevant for Apple Silicon and modern servers, but not needed as a second Core ISA. AArch64 can appear as convenience-path observation when the learner runs native Linux/ARM64, provided the design keeps the same machine concepts and avoids architecture-specific assessment drift.

### 6.4 Source-to-machine observation

GNU `objdump` official documentation specifies `-d/--disassemble` for displaying assembler mnemonics from machine instructions and `-S/--source` for source intermix when debug information permits. GDB official documentation supports `info line`, `disassemble`, and instruction examination to map source and machine addresses.

A minimal activity can therefore:

1. compile a tiny C function with debug info;
2. predict where arguments/result must live conceptually;
3. inspect disassembly;
4. single-step a few instructions or inspect registers/memory;
5. map a call/return and one stack/local value;
6. trigger a safe local invalid-memory case only if the Design task can keep C undefined-behavior teaching bounded and avoid implying portable semantics from a crash.

### 6.5 Minimal C requirement

C is an observation medium, not a prerequisite course. The learner only needs:

- integer variables;
- function definition/call;
- local variable;
- pointer/address notation only where needed for an address observation;
- array or small struct only if it exposes layout clearly;
- compile/run commands supplied by the activity.

Do not require manual allocation, strings library mastery, complex pointers, preprocessor knowledge, build systems, or multi-file C design.

### 6.6 ABI/interface intuition

The learner should be able to say:

- “The language source does not itself name these registers.”
- “The compiler emits code that follows an ABI/calling convention so separately compiled code can interoperate.”
- “Arguments, return values, caller/callee-saved registers, stack alignment, and object/link conventions are interface rules of the platform ABI, not universal facts about all machines.”

Full ELF format, linking/relocation, dynamic loader behavior, and compiler pipeline belong later (primarily M05 and beyond).

### 6.7 Common M03 misconceptions

- “Assembly is the CPU hardware.” → Assembly is a textual representation of machine instructions for an ISA.
- “One C line equals one instruction.” → Compiler decisions, optimization, ABI, and language semantics break that model.
- “A register is a variable.” → Compiler allocation changes; architectural register contents are execution state, not source identity.
- “The stack is a hardware stack data structure.” → In the selected ABI it is a convention over memory plus a stack pointer and call conventions.
- “Function calls always push all arguments on the stack.” → ABI-specific; modern x86-64 passes initial arguments in registers.
- “A segfault means the address doesn't exist physically.” → The observed fault is about the process's permitted virtual address access under later OS mechanisms; M03 should use it only as an evidence hook and defer virtual-memory explanation to M07.
- “x86-64 behavior is how all CPUs work.” → One implementation case exposes stable ISA/ABI concepts; transfer later checks what changes.

---

## 7. M04 Research — Memory Hierarchy / Locality / Measurement

### 7.1 Stable mental model

**PRINCIPLE — ESTABLISHED.** Memory/storage systems trade capacity, latency, bandwidth, cost, volatility, and placement. A hierarchy exploits locality by retaining/moving data across levels so common accesses can often be served from a faster/smaller level.

Minimum Core:

- registers/cache/RAM/storage as a qualitative hierarchy;
- cache line/block as transfer/granularity concept;
- temporal and spatial locality;
- layout and access order affect observed performance;
- RAM vs durable storage boundary: RAM hierarchy teaching must not imply persistence/durability;
- latency values are approximate/current, not timeless constants;
- measurement can establish an effect under a workload/environment, not universal causality.

### 7.2 Cache and cache line

M04 `L04-01` is the canonical Caching first home. The definition must emphasize a retained prior copy/result under a validity policy; hardware cache is the first context, not the universal definition.

Cache line size, cache capacity, associativity, replacement policy, prefetcher behavior, and hardware counters are **implementation facts**. The first traversal needs enough of cache-line granularity to explain why sequential accesses can exploit spatial locality and why strided/pointer-chasing access may behave differently.

Do not require cache-index arithmetic, coherence protocol details, MESI, prefetcher internals, DRAM row-buffer design, or memory-controller scheduling.

### 7.3 Applied measurement-uncertainty toolkit

M04 `L04-02` remains the first assessed home. The accepted pattern should be instantiated as:

`question/hypothesis → baseline → controlled change → metric + environment + workload → warmup/cold-state decision → repetitions → summarize distribution/variation → observation → competing explanation → bounded conclusion`

This is an **applied measurement toolkit, not a statistics course**.

Minimum statistics language:

- repeat because runs vary;
- keep raw observations;
- median as a robust summary for skew/noise when appropriate;
- percentiles only when the question is distribution/tail behavior and enough samples exist to make them meaningful;
- range/IQR or similarly simple variation description if useful;
- avoid false precision;
- say when sample count/workload is too small for a strong percentile claim;
- use order-of-magnitude comparisons before arguing about small percentage changes.

No probability distributions, confidence-interval derivations, hypothesis tests, p-values, regression, or statistical inference course is required here.

### 7.4 Timing tool baseline

**IMPLEMENTATION — ESTABLISHED for Python 3.12.** Python's official `time.perf_counter()` is a high-resolution performance counter for measuring short durations; only differences between readings are meaningful. `perf_counter_ns()` avoids float precision loss.

For the canonical first-slice activity, this is a reliable fallback because it requires no privileged kernel counters. The activity should measure enough work per trial to dominate timer overhead, and it should record the Python/runtime/environment version.

### 7.5 `perf` as optional enhancement, not dependency

**IMPLEMENTATION — ENVIRONMENT-SENSITIVE.** Linux kernel documentation explains that access to `perf_events` for unprivileged users is controlled by `perf_event_paranoid`, because performance counters can expose sensitive data. Container/Codespace environments may therefore restrict hardware counter access or capabilities.

Design rule:

- primary M04 evidence must remain achievable with wall/monotonic timing and controlled access-order changes;
- if `perf stat` works, hardware/cache events may strengthen the explanation;
- if `perf` is unavailable/restricted, this is an environment/tool limitation, not learner conceptual failure;
- do not ask learners to weaken host security settings or require privileged containers merely to complete Core.

### 7.6 Cold/warm state

The design must state what “cold” and “warm” mean for the exact experiment. Avoid pretending a user process can perfectly flush all hardware cache state portably.

Safer first-slice approach:

- use warmup iterations to reach a reasonably repeatable steady condition;
- compare two access patterns on the same allocated data with randomized/counterbalanced trial order when practical;
- record that caches, CPU frequency, scheduler activity, virtualization, allocator placement, and prefetchers are possible competing explanations;
- use a dataset/access pattern large enough to expose a robust locality difference, verified in the canonical image during later implementation.

A “cold cache” claim should only be made if the implementation has a defensible method for the relevant level. Otherwise call it “first run after setup” or “warmup vs steady repeated runs.”

### 7.7 Practical classic experiment

A classic **memory mountain / stride / sequential-vs-nonsequential access** experiment is pedagogically appropriate because it exposes locality through real timing. CS:APP popularized mature versions of this family. However, existing CS:APP assignment/material rights are already rights-gated in the accepted Lab map. Therefore:

- use the classic mechanism/activity pattern as research evidence;
- link to the source/course where allowed;
- do not copy assignment text/code/graphs;
- future Design may create an original small fixture if no license-cleared bounded activity fits.

A simple sequential array traversal vs a deliberately locality-poor traversal is preferable to complex profiler work for the first pilot.

### 7.8 Latency hierarchy and false precision

Teach latency as a **CURRENT-PRACTICE approximate ladder**, never a fixed table of sacred numbers. Hardware-dependent constants should be refreshed under OQ-BP-006/R11 maintenance. The learner should reason in orders of magnitude and then measure the actual canonical environment where needed.

Do not make statements such as “RAM is 100 ns” without context. Better: “on contemporary hardware, cache, DRAM, local storage, and network/storage paths often differ by large orders of magnitude; use current measured/reference values for the actual decision.”

### 7.9 Common M04 misconceptions

- “Memory = storage.” → RAM hierarchy and durable storage have different semantics; durability waits for M09.
- “Cache is a faster database.” → Cache is a retained copy/result under a validity policy and may not be authoritative/durable.
- “Sequential is always faster.” → It is a hypothesis under a workload/hardware implementation, not a universal rule.
- “One benchmark proves the cause.” → A measured difference supports a claim under the setup; hardware counters/source/additional controls may be needed to distinguish causes.
- “Median removes noise.” → It summarizes; it does not eliminate variation or confounding.
- “A p99 from 20 samples is meaningful.” → Tail percentiles require enough observations and a question that needs them.
- “`perf` failing means I cannot do the Lab.” → Hardware counters are optional; timing fallback is canonical.
- “Warm means every cache line is resident.” → Warmup is an operational condition, not omniscience about all hierarchy state.

---

## 8. Cross-Module Concept / Prerequisite Check

The M00–M04 slice is internally coherent under the authoritative DAG:

- `M00 → M01` hard;
- `M00 → M02` hard;
- `M01 → M02` soft;
- `M01 → M03` hard;
- `M02 → M03` hard;
- `M03 → M04` hard.

No new edge is needed.

Potential hidden-prerequisite checks for Design:

| Risk | Canonical handling |
|---|---|
| Shell/task execution | Taught/practiced at M00 `L00-02`; optional Bridge can remediate; not an entry prerequisite. |
| Git evidence | Minimal diff/commit/evidence use at M00 `L00-02`; no Git mastery. |
| C syntax | Introduce only the tiny subset needed in M03; not a prerequisite. |
| Assembly | Read a bounded trace; no assembly programming prerequisite. |
| Statistics | M04 `L04-02` just-in-time applied toolkit; no math gate. |
| Hardware architecture | M03 introduces machine/ISA model; no digital-logic prerequisite. |
| Compiler knowledge | Only “compiler produces machine/object code” as observation bridge; M05 owns language/runtime/compiler mechanism. |
| Virtual memory | Do not use as explanation for addresses/crashes yet; M07 owns it. |
| Durability/storage | P0 durable collection may be opaque; mechanism waits M08/M09/M13. |

Architecture finding: none. If later implementation cannot produce a robust locality effect without adding privileged tooling or large setup burden, the response should be to simplify the activity/measurement, not to add a new prerequisite or Module edge.

---

## 9. Classic Source & Activity Evaluation — Adopt → Adapt → Build

The table evaluates serious candidates for M00–M04. “Link/reference” means use as designer/learner source without copying protected material. Licensing statements are intentionally conservative.

| Candidate | Exact bounded slice | Mechanism exposed | Cognitive load | Setup burden | Provenance / license status | Adopt/Adapt/Build decision | Maintenance risk / fit |
|---|---|---|---|---|---|---|---|
| **CS50 2026 / 2025 Memory & Hexadecimal notes** — Harvard CS50 | Binary/hex visualization; bytes/addresses; overflow examples only | Human-readable bridge from bits/hex to memory representation | Low | Low | Public course pages; redistribution/adaptation rights not assumed here; link/reference unless item-level terms are cleared | **Reference / adapt concept pattern only** | Low mechanism risk; course framing may assume CS50's C progression, so Essential CS must remove programming-course dependencies |
| **Unicode Standard 17.0 + Unicode UTF FAQ** — Unicode Consortium | Encoding forms / UTF-8 well-formed byte sequences; round-trip and byte-oriented behavior | Unicode code point ↔ UTF-8 representation | Medium | None | Official standard/docs; copyrighted; quote minimally, link and paraphrase; follow Unicode terms | **Adopt specification as authority; build original observation prompts** | Stable specification; version changes should be checked on maintenance cadence |
| **WG14 C23 / two's-complement papers** — ISO C WG14 | Signed integer representation and overflow distinction | Representation vs language arithmetic semantics | Medium | None | Official standards-workgroup materials; individual papers may state licenses; standard text itself is not freely redistributable by default | **Adopt as specification evidence; no copied standard prose** | Low mechanism risk, medium version-semantic risk if examples claim older C behavior |
| **Open Data Structures** — Pat Morin | §1 asymptotic notation plus selected array/list/hash/tree interface slices | Growth analysis and container trade-offs | Medium | None/Python optional | Explicitly CC BY; text/source may be adapted with attribution | **Adapt narrowly** | Low; full text is much broader than M02 and must be cut aggressively |
| **Cornell CS2110 searching/asymptotic complexity + loop invariants** | One searching comparison + one invariant exercise pattern | Count work, asymptotic intuition, invariant-based correctness | Medium | Low | Public university course material; rights not inferred from access | **Reference; build original prompts unless terms cleared** | Pedagogically classic; Java-course context adds incidental load if copied directly |
| **MIT Mathematics for Computer Science** | Selected invariant/asymptotic background for designers | Formal grounding of invariants/growth | High for target learner | None | OCW/item licensing must be checked for exact edition/material | **Designer source; not learner prerequisite** | Stable theory, but too math-heavy for first traversal |
| **CMU CS:APP Data Lab narrow representation slice** | Existing accepted `LAB-OPT-01` only | Bit-level integer representation | High-medium | Toolchain | Existing Blueprint already marks rights-gated/link-only until cleared | **Do not promote; preserve Optional rights gate** | Strong mechanism fit but programming/bit-trick load can distort M01 goals |
| **CS:APP machine-code exercises / bomb-like patterns** | Only simple source→assembly tracing patterns, not Bomb/Attack Lab | ABI, control flow, stack | Medium-high | GCC/GDB | Text/course assets are copyrighted; no redistribution assumed | **Reference pattern; build original tiny source case** | Mature pedagogy; avoid puzzle/reverse-engineering load and security-adjacent framing |
| **RISC-V Ratified Unprivileged ISA v20260120** — RISC-V International | RV64I register/instruction/call examples only | ISA as specification | Medium | None for reading; high if emulated | Official ratified specification; terms must be respected; link/reference is safe baseline | **Adopt as spec/reference; not required runtime** | Stable and excellent transfer case; version should be checked when cited |
| **GNU binutils `objdump` + GDB official docs** | `objdump -d/-S`; GDB `disassemble`, register/memory inspection | Real source→machine observation | Medium | Low on canonical Linux | GNU documentation/software licensing applies; commands/examples should be original | **Adopt tools; build original bounded activity** | Output changes with compiler/binutils/architecture; pin environment for assessed observations |
| **CS:APP memory mountain / stride family** | Sequential/strided/locality comparison only | Cache/locality and measurement | Medium | Low-medium | Assignment/code rights not assumed; accepted project already treats CS:APP material cautiously | **Adapt mechanism pattern, do not copy; Build original fixture if needed** | Excellent fit; hardware variance requires canonical-image smoke testing |
| **Linux `perf` docs** | Optional `perf stat` counters when allowed | Counter evidence for cache/CPU events | Medium | Environment-dependent | Kernel/GNU tooling documentation; normal open-source licenses, but exact docs/tool versions vary | **Optional enhancement only** | High portability/security-constraint risk in containers/Codespaces |
| **Python `time.perf_counter_ns`** | Primary timing fallback | Monotonic/high-resolution elapsed-time measurement | Low | Very low | Python docs/software under PSF terms | **Adopt implementation surface** | Low; timer does not identify cause, which is pedagogically useful to state |

### 9.1 Source-selection conclusion

For the first slice, the strongest Adopt/Adapt pattern is:

- **Adopt authoritative specifications/documentation** for representation, Unicode, ISA, ABI/tool behavior.
- **Adapt classic pedagogical patterns** for hex/bytes, operation counting/invariants, source→assembly tracing, and locality experiments.
- **Build only small Essential CS-owned fixtures/prompts** where rights, cognitive load, or reproducibility make direct adoption unsuitable.

This does **not** justify a new Required Lab. The M00–M04 activities can remain lesson/module evidence/checkpoints within the accepted assessment architecture.

---

## 10. Environment / OQ-BP-006 Proposal

OQ-BP-006 remains **OPEN — implementation-time pin**. This dossier narrows what the first runnable slice actually needs.

### 10.1 Candidate baseline matrix

| Surface | Why needed now? | Proposed first-slice choice | Pin now? | Authoritative/current evidence | Portability / maintenance notes |
|---|---|---|---|---|---|
| Linux base | Canonical environment for all M00–M04 observations | **Ubuntu 24.04 LTS (`noble`)** | **Pin release now; immutable image digest at implementation** | Ubuntu LTS / Dev Containers support records show Noble supported through 2029; Dev Containers provides `base:noble`/`cpp:noble` | Mature and supported. Ubuntu 26.04 is newer but not required; moving would add freshness without a learning benefit. |
| Dev Container | Reproducible one-click path / Codespaces | Dev Container based on Noble | **Yes at environment family level; digest later** | GitHub Codespaces docs recommend a repository dev-container configuration for a reproducible environment | Tag alone can move with security updates. Final runnable baseline should record immutable digest + rebuild cadence. |
| CPU ISA for M03 | Disassembly/debugger evidence | **x86-64 when canonical Codespace/image reports x86-64; same conceptual activity may adapt to AArch64 convenience path** | **Preflight must record architecture; do not pin cross-ISA emulator** | GNU tools + platform ABI docs | If Codespace architecture offering changes, Design must keep one canonical case and treat others as supported variants, not second curricula. |
| Python | Main lab language, byte/serialization/timing observations | **Python 3.12.x** | **Pin minor (3.12); allow security/patch updates within environment rebuild unless an observation is patch-sensitive** | Dev Containers support table lists Python 3.12 through Oct 2028; Python 3.12 docs define `perf_counter`/`perf_counter_ns` | Avoid third-party packages in first slice; stdlib suffices. |
| C compiler | M03 source→machine case | **GCC 13 from Ubuntu Noble** | **Pin distro/toolchain family; exact package build captured in evidence, not hardcoded in curriculum prose** | Ubuntu package index currently exposes GCC 13 packages (e.g. 13.3.0 Noble updates/security) | Compiler output is version/flags sensitive. Assessed activity should record exact `gcc --version`. |
| Binutils | `objdump`, object inspection | Noble GNU binutils | **Same approach as GCC** | GNU binutils official docs + Ubuntu package dependency | Record exact version in preflight. Do not teach output formatting as stable. |
| GDB | debugger-light M03 observation | Noble GDB | **Tool present; exact version recorded, not curriculum-semantic pin** | GDB official docs | Some ptrace/debug capabilities can be container-sensitive; smoke test canonical path. |
| Git | M00 evidence preservation | distro Git | **Do not pin semantic version now** | Git official docs | Required use is basic diff/status/commit evidence, stable across supported versions. Record version in preflight only. |
| Shell/core utilities | task execution/file inspection | POSIX-ish shell + GNU coreutils available in image | **Do not individually pin** | Ubuntu base | Commands should be minimal and wrappers can reduce shell assumptions. |
| `perf` | optional M04 hardware counters | **Optional only** | **Do not pin / do not require** | Linux kernel perf security docs | `perf_event_paranoid`/capabilities may block access. Canonical fallback must succeed without it. |
| Timing | required M04 measurement | Python `perf_counter_ns()` and/or `/usr/bin/time` for coarse tasks | **Python surface sufficient** | Python official docs | Monotonic elapsed timing does not identify causal mechanism; this is an explicit inference limit. |
| QEMU/RISC-V cross-toolchain | not required until M06 LAB-REQ-02 | **Deferred** | **Do not pin now** | Canonical Lab map already owns this later | Avoid pulling M06 setup into M03. |
| SQLite/PostgreSQL | P0 durable fixture may exist, DB mechanisms later | **Deferred for teaching baseline** | **Do not pin now for M00–M04** | Canonical Lab/project maps own SQLite in later Modules | If a supplied P0 fixture uses SQLite internally, its version belongs to fixture implementation metadata, not learner-required DB surface yet. |
| Browser / DevTools | not required in slice | Deferred | **Do not pin** | M11/M12 later | No browser dependency for first runnable slice. |
| Containers/orchestration/observability stack | not needed | Deferred | **Do not pin** | M19/M20 later | Explicitly avoid “systems course tool accumulation.” |

### 10.2 Why Ubuntu 24.04 rather than 26.04

**IMPLEMENTATION recommendation, not architecture decision.** As of the checked date, newer Ubuntu 26.04 LTS exists and current Dev Containers support material has begun tracking `resolute`. The first slice does not need a newest-possible OS; it needs a mature reproducible baseline with stable compiler/debugger packages and low learner friction. Noble remains under standard support through 2029 and has a mature Dev Container image family. Therefore 24.04 is the lower-risk first production baseline.

This is a **CURRENT-PRACTICE** choice, not a statement that 24.04 has better systems semantics.

### 10.3 Dev Container / Codespace constraints

- custom repository dev-container configuration is preferred over the platform default because the course needs a reproducible tool set;
- the final implementation should pin the image by immutable digest or similarly immutable build identifier, while retaining a documented refresh process for security updates;
- privileged containers must not be required for M00–M04;
- `ptrace`/GDB and performance-counter behavior must be smoke-tested in the actual Codespace/container configuration;
- if hardware counters are unavailable, `perf` is skipped rather than “fixed” by granting broad host privileges.

### 10.4 macOS / WSL convenience paths

- **WSL2:** strong convenience path because learner can run a Linux userspace close to canonical. Still record kernel/tool versions; do not assume performance equivalence to Codespaces.
- **macOS Intel:** native toolchain differs (Clang/LLDB/Mach-O). Prefer the Dev Container for canonical assessed output.
- **macOS Apple Silicon:** native AArch64 is pedagogically valid but changes ISA/ABI/disassembly. Prefer the Dev Container/canonical hosted environment for shared assessed evidence; native path may be an optional transfer case.
- do not require users to install low-level packages manually if the one-click container path can provide them.

### 10.5 Proposed first-slice environment baseline — Web Lead review proposal only

> **PROPOSAL — does not close OQ-BP-006.** Use a repository Dev Container/Codespace based on Ubuntu 24.04 LTS (`noble`). Provide Python 3.12, GCC 13-class Noble compiler, GNU binutils (`objdump`/`readelf` as needed), GDB, Git, and minimal shell/core utilities. Require the preflight to record OS image/build, CPU architecture, Python, GCC, binutils, GDB, and Git versions. Use Python standard library for byte/serialization/timing work. Treat `perf` as optional and non-blocking. Do not install/pin QEMU/RISC-V, SQLite/PostgreSQL, browsers, containers/orchestrators, or observability stacks for this slice. At implementation, pin the Dev Container base by immutable digest and document a controlled refresh cadence rather than freezing security updates indefinitely.

The Web Lead may accept, amend, or defer this proposal. OQ-BP-006 remains formally open until handled through the project's designated follow-up process.

---

## 11. P0 Mini Cloud App Boundary

Canonical P0 remains **one process, one durable collection**. The risk is that “durable collection” becomes a hidden database/storage course before M08/M09/M13.

### 11.1 What learners may build themselves during M00–M04

Safe learner-owned surface:

- one small process/command path supplied or minimally scaffolded in Python;
- domain record shape (e.g. note/bookmark identifier + small payload) at a level needed for Representation;
- input → representation/serialization → in-process state transition → returned/read representation trace;
- stable identifier generation only if the mechanism is trivial and does not introduce distributed uniqueness claims;
- encode/decode / round-trip checks;
- simple ownership/schema-like invariant phrased as application correctness, not database constraint teaching;
- byte-size / growth estimate for `N` records under stated representation assumptions;
- compare an in-memory representation with serialized bytes;
- inspect that durable bytes/state exist after a supplied “save” operation **without explaining why they survive a failure**;
- measure local representation/layout operations only if M04 needs an integration transfer case, not as a database benchmark.

### 11.2 What should be supplied as opaque or partially opaque fixture

During M00–M04, the persistence adapter should be **course-supplied**. Two honest fixture options are acceptable:

#### Option A — simple file fixture

Best when the checkpoint only needs representation, byte size, serialization, and observable state before/after process restart. It minimizes hidden DB semantics. The learner may inspect file bytes and see that a later process invocation can read them, while the course says explicitly:

> “We are using a file as a supplied persistence surface. We are not yet making a durability guarantee or teaching filesystem mechanisms.”

#### Option B — SQLite-backed adapter hidden behind a tiny interface

Acceptable because canonical P0 later uses SQLite as a baseline, but only if the learner-facing activity treats SQLite as an implementation surface:

- learner calls `save(record)` / `load(id)` or a similarly narrow supplied boundary;
- learner may inspect that the adapter uses SQLite and may record the implementation/version metadata;
- learner does **not** need SQL, query planner, transactions, journal modes, WAL, locking, fsync, recovery, or storage-engine concepts;
- Design must state “SQLite is present, but database mechanisms are intentionally deferred to M13/M14; durability mechanisms to M08/M09/M14.”

### 11.3 Which P0 questions are legitimate now

M00–M04 may ask:

- Where is state before/after this operation?
- Which boundary is an interface vs an implementation detail?
- What byte representation is used for a record?
- Can the representation round-trip?
- What inputs are invalid or ambiguous?
- Approximately how many bytes will `N` records require under this representation?
- Which invariant should hold after create/read/update/delete-like local operations, if such operations exist?
- What evidence shows a new process invocation can retrieve the supplied fixture's state?
- Which claims about “durable” are **not yet justified** by that observation?

### 11.4 What must explicitly wait

Do not explain/assess during M00–M04:

- filesystem caching/page cache;
- writeback/fsync/barriers;
- crash/power-loss durability;
- SSD/HDD persistence mechanics;
- SQLite page format/B-tree;
- query plans/indexing;
- transaction isolation;
- WAL/rollback journal;
- backup/recovery;
- database locks/concurrency;
- schema migration framework;
- server database vs embedded database trade-offs.

Those are owned by M08/M09/M13/M14 and selected Required Labs.

### 11.5 Recommended checkpoint sequence

- **M00:** use P0 as a supplied local “one process, one collection” map. Trace input → interface → in-process state → persistence adapter → response, with persistence adapter explicitly opaque.
- **M01:** inspect one record's representation/bytes and perform a round trip; estimate collection size.
- **M02:** state an application-level invariant/spec for a small operation and reason about a data-structure/workload choice inside the process. Do not infer database guarantees.
- **M03:** P0 is optional/revisit only. A tiny pure function from the app may be compiled as a machine case if it reduces transfer distance, but avoid forcing Python app internals into C.
- **M04:** optional transfer: measure a local in-memory layout/access pattern derived from record data, not the durable store. Do not benchmark SQLite and call it “database performance.”

### 11.6 P0 stopping boundary

> **P0 stopping boundary for this slice:** by the end of M04, the learner may own the process-local data model, representation/serialization, application-level invariant, and size estimate, and may observe a supplied persistence adapter retaining state across a bounded restart. The learner must **not** be expected to explain or modify the persistence mechanism, database engine, durability guarantee, transaction behavior, recovery path, or storage hierarchy. Those mechanisms remain later canonical teaching homes.

Project order is not the curriculum DAG. P0 is an integration surface and evidence reuse opportunity; completing or extending P0 must never become a hidden prerequisite for M01–M04.

---

## 12. Assessment / Evidence Hooks

No numeric grading is proposed. Reuse the accepted primary modes **Explain / Predict / Break / Judge** and cumulative **Recall / Connect / Transfer**.

### 12.1 Potential evidence by Module

| Module | Primary evidence hooks | Modes | Machine-checkable portion | Reviewer-required portion |
|---|---|---|---|---|
| M00 | prediction before inspection; one local system trace; environment/source/evidence record; observation vs explanation statement | Predict, Explain, Judge; Connect | file exists/commands ran/version record present; trace references valid fixture | whether source layer fits the claim; whether explanation exceeds observation; whether uncertainty is bounded |
| M01 | binary/hex/byte trace; encode/decode; UTF-8 byte inspection; endianness case; size estimate; broken round trip | Predict, Break, Explain; Transfer | round-trip tests; exact byte sequences for fixed fixtures; range checks | whether learner distinguishes information/representation and states boundary assumptions |
| M02 | operation count; growth comparison; data-structure choice under workload; specification/invariant; counterexample; bounded undecidability/tractability explanation | Predict, Break, Judge; Recall/Transfer | operation-count fixtures and test cases can verify form/results | correctness reasoning, model assumptions, trade-off and limitation quality |
| M03 | source/disassembly record; register/memory/call-frame trace; debugger observation; one intentionally changed input or safe failure hook | Predict, Explain, Break; Transfer | compile/run success; expected symbols/trace anchors; artifact presence | source↔machine explanation; ABI-vs-language distinction; unsupported causal claims |
| M04 | stated hypothesis; repeated locality measurements; environment/workload; warmup policy; raw values; median/percentile only when justified; uncertainty/competing explanations | Predict, Break, Judge; Connect/Transfer | script runs; repetitions present; summaries reproducible | experimental fairness, causal limits, false precision, whether conclusion matches evidence |

### 12.2 Reuse, not one administrative artifact per Module

A single compact slice evidence packet can contain:

- M00 investigation header/environment record;
- M01 representation trace;
- M02 spec/invariant + estimate attached to the same fixture;
- M03 machine trace from one bounded compiled example;
- M04 measurement record.

The Stage S1/S2 checkpoint may reuse these sections rather than rerun the same experiments for administrative completeness.

### 12.3 Suggested transfer prompts

- M01 transfer: decode an unfamiliar but documented fixed-width field/byte order and state what must be checked before interpreting it.
- M02 transfer: given a new workload and two container interfaces, estimate dominant operation growth and identify which missing constants/measurements matter.
- M03 transfer: show a tiny RISC-V or AArch64 excerpt after x86-64 and ask what machine concepts remain invariant vs architecture-specific.
- M04 transfer: given benchmark output from an unfamiliar environment, identify what additional environment/workload/repetition evidence is needed before accepting a performance claim.

---

## 13. Learner-Validation Risks

The first pilot should prioritize **failure-mode observation** over completion time alone.

| Risk | Observable failure signal | Design-change evidence | What would NOT justify raising prerequisites |
|---|---|---|---|
| Hidden shell/Git assumptions | learner spends more time locating files/remembering commands than reasoning about evidence; cannot distinguish command failure from concept failure | repeated failures across otherwise programming-capable learners at the same setup step; hint ladder fixes performance | one learner unfamiliar with a flag; slow typing; preference for GUI |
| Fear of C/assembly | learner treats M03 as a new programming language course; cannot answer concept questions despite mechanically stepping | consistent drop in prediction/explanation quality when syntax volume rises; comprehension improves when trace is shortened | discomfort alone, or needing a supplied cheat sheet |
| Representation = information confusion | says UTF-8 bytes “are the character”; assumes value has one universal byte layout | repeated wrong transfer to different encoding/endianness after successful rote exercise | one arithmetic conversion mistake |
| Memory = storage confusion | calls RAM “persistent storage”; interprets P0 restart behavior as proof of durability | same confusion persists after explicit state-location prompt and causes M04/P0 reasoning errors | vocabulary hesitation on “memory” in natural language |
| Big-O without intuition | can recite `O(n)`/`O(n²)` but cannot predict scaling or count operations | learners pass recall but fail operation-count/transfer tasks; redesign around concrete growth examples | algebra mistakes that do not affect order-of-growth reasoning |
| False precision in latency | reports many decimal places or memorized “100 ns RAM” as universal fact | repeated unsupported precision/production extrapolation despite prompts | approximate order-of-magnitude values differing by a factor of 2–3 |
| One benchmark = proof | declares locality cause solely from one timing run; ignores variation/confounders | repeated causal overclaim survives hinting; requires stronger explicit competing-explanation step | noisy runs themselves; machine variance is expected |
| Tool/environment failure mistaken for concept failure | debugger/perf/container issue blocks learner and they self-report “I don't understand caches/assembly” | same environment failure reproduces across learners/machines; canonical preflight fails | learner needs one targeted setup hint |
| Too much theory before payoff | disengagement or inability to explain why an abstraction matters before any observation | prediction/explanation quality improves materially when observation is moved earlier | learner asks for additional examples/theory after succeeding |
| P0 becomes Web/database training | learner discusses SQL/framework/storage implementation rather than representation/state/spec questions | time-on-task and errors dominated by persistence/framework details; removing them improves targeted evidence | learner notices SQLite/file name and asks how it works later |

### 13.1 Pilot observation plan

For the first real learner pilot, capture:

- time-to-first-successful preflight and number/type of environment interventions;
- number of hints needed, categorized as environment/tool vs concept;
- pre-activity prediction and post-activity explanation quality;
- whether the learner can state observation separately from causal explanation;
- whether M01 transfer changes representation while preserving information;
- whether M02 transfer uses workload/operation growth rather than memorized labels;
- whether M03 fear decreases after a short source↔instruction trace and whether syntax load remains bounded;
- whether M04 learner reports raw/repeated values, acknowledges variation, and refuses a stronger causal claim than evidence permits;
- whether P0 is perceived as an integration surface or as a hidden web/database assignment.

### 13.2 Evidence threshold for design change

Change the Design when multiple target-profile learners independently fail for the **same accidental reason** despite appropriate hints, especially if the failure is environment/tooling or wording rather than the intended mechanism.

Do not raise entry prerequisites merely because learners need targeted support in shell/Git/C/assembly. The accepted Learner Profile explicitly excludes prior fluency in those areas; the course owns that support burden.

### 13.3 Stopping points / explicit exclusions

This slice must not expand into any of the following. A bounded example is allowed only up to the stated stopping point:

- **Programming 101:** stop at the already-assumed ability to read/run small programs; Bridge may remediate practical setup, not teach programming fundamentals.
- **Full discrete mathematics:** introduce only powers/log intuition, simple counting, and just-in-time invariant reasoning needed by M01–M04.
- **Full algorithms course:** stop at operation counting, asymptotic-growth intuition, a small systems-relevant data-structure set, and bounded correctness/tractability/decidability intuition.
- **Competitive programming:** no puzzle repertoire, contest optimization tricks, or speed-solving skill target.
- **Digital logic → ALU → CPU construction:** bits are representation substrate; M03 begins from the ISA/programmer-visible machine. Gate/circuit/CPU construction is outside this slice.
- **Full compiler construction:** M03 may observe source → object/machine code; parsing, IR design, optimization passes, code generation, linking internals, and compiler implementation are deferred/out of scope.
- **Linux administration:** shell/process/file commands are evidence instruments only; no service administration, package-management mastery, kernel tuning, or privilege-management syllabus.
- **Git mastery:** stop at minimal status/diff/commit/evidence preservation needed for reproducibility.
- **Full C programming course:** introduce only syntax needed to expose machine/ABI behavior; no ownership of broad C language/library/build-system proficiency.
- **Database internals:** P0 persistence remains opaque/partially opaque; query planning, indexes, transactions, journals/WAL, recovery, and database-engine mechanisms wait for M13/M14 (with storage/durability foundations in M08/M09).
- **Networking:** no sockets/protocol/HTTP teaching in M00–M04; network terms may appear only as later-system-map landmarks.
- **Distributed systems:** no partial failure, replication, consensus, queues, or distributed consistency in this slice.
- **Cloud/vendor training:** Dev Container/Codespace is an environment convenience, not a cloud-platform or vendor-operations curriculum.
- **AI/ML Core expansion:** only the accepted verification rule for AI-generated output is used; no model/LLM/agent track is introduced while OQ-BP-001 remains open.

---

## 14. Provenance / Licensing Risks

1. **CS:APP materials:** strong classic pedagogical source, but existing Blueprint work already marks Data Lab use rights-gated. Treat course/text assignments, code, diagrams, and prose as link/reference unless explicit permission covers the exact adaptation. Do not copy Memory Mountain or other assignment assets by default.
2. **University course pages (CS50, Cornell, MIT, Berkeley/CMU):** public accessibility is not reuse permission. Record item-level license before redistributing slides, code, figures, tests, or substantial prose.
3. **Open Data Structures:** explicit CC BY license is a favorable candidate for narrow adaptation; preserve author/title/source/license attribution and state changes.
4. **Unicode materials:** use the standard/FAQ as normative/authoritative references; paraphrase and link, and check Unicode terms for any redistributed tables/figures/data.
5. **ISO C standard:** standards text is copyrighted; use WG14 public materials to support claims and link to official standard information. Do not reproduce substantial ISO text.
6. **RISC-V specifications:** official standards are appropriate authority; verify applicable license/terms before bundling excerpts/figures. Original Essential CS diagrams are preferable.
7. **GNU/Python/Linux documentation:** open-source documentation licenses still require attribution/compliance for copied/adapted material. Prefer original instructions that cite official docs.
8. **System V ABI materials:** location/maintainer can change; verify the exact published ABI source and license before reproducing tables. Use short paraphrases and original diagrams for calling-convention teaching.
9. **Generated code/diagrams:** original Essential CS code/visuals may use project licensing intent, but factual mechanisms still require cited sources; AI generation does not remove provenance obligations.

No licensing uncertainty in this dossier should be interpreted as permission. Where status is uncertain, the default is **link/paraphrase only** pending item-level review.

---

## 15. Open Questions / Uncertainty

### 15.1 Research uncertainty

- **M04 experiment robustness — UNCERTAIN until implementation smoke test.** A sequential-vs-locality-poor experiment is well established pedagogically, but exact dataset/access pattern/repetition count must be tested in the final container to ensure a visible yet honest effect across hosted hardware.
- **M03 canonical architecture portability — IMPLEMENTATION-SPECIFIC.** x86-64 is the lowest-burden default if the canonical Codespace/image is x86-64. The preflight must verify this rather than assume it forever. If hosted architecture changes, preserve concepts and choose one canonical ISA case; do not add multi-ISA mastery.
- **GDB/ptrace in hosted container — IMPLEMENTATION-SPECIFIC.** Must be verified in the final Dev Container/Codespace configuration. This is an implementation test, not an architecture question.
- **Exact immutable container digest — implementation-time.** It cannot be responsibly frozen before the runnable dev-container configuration exists. The Design/implementation task should select and record it.

### 15.2 Open Questions intentionally unresolved

- **OQ-BP-001 bounded AI literacy:** remains open. This slice uses only the accepted safe rule that AI output is an untrusted hypothesis requiring verification.
- **OQ-BP-003 human-facing/accessibility boundary:** remains open and is not implicated enough by M00–M04 to force a Core-scope decision.
- **OQ-BP-006 environment/version baseline:** remains open. This dossier provides a first-slice proposal, not a formal closure or Decision.

### 15.3 Architecture escalation

No architecture escalation is required by current research. If later implementation demonstrates that a canonical M03/M04 capability cannot be produced reproducibly in a non-privileged Dev Container without changing the learning objective, escalate that concrete finding. Do not preemptively change Modules, edges, competencies, Lab selection, or environment policy.

---

## 16. Recommended Design Inputs

The next Design Agent may safely assume:

1. M00–M04 boundaries and canonical Concept first homes remain unchanged.
2. Bridge remains optional/skippable and cannot absorb M00's canonical evidence workflow.
3. The learner has basic programming but not shell/Git/C/assembly/Linux expertise.
4. The default reasoning loop for the slice is `predict → observe → explain → bound claim`, with evidence preservation introduced in M00 and applied uncertainty assessed first in M04.
5. M01 may use Python standard-library byte/encoding tools and should center representation round trips, size, Unicode/UTF-8, and endianness.
6. M02 should use concrete operation counting, a deliberately small data-structure set, one bounded invariant/correctness pattern, and an intuitive tractability/decidability stopping point.
7. M03 should use **one** canonical ISA/ABI implementation case; native x86-64 GNU tooling is the recommended first implementation, while RISC-V is a transfer/spec reference and later M06 Lab environment concern.
8. M04's core measurement must work without `perf`; monotonic/high-resolution timing plus repeated controlled runs is sufficient. Hardware counters are optional corroboration.
9. No new Required Lab is implied. Use local checks/module evidence and reuse the Stage evidence packet.
10. P0 may expose representation/state/size/correctness while persistence is supplied/opaque. Storage/database/durability mechanisms remain deferred.
11. The first-slice environment should be minimal and reproducible; avoid adding tools solely because systems courses commonly use them.

Implementation-time decisions still to make:

- exact Dev Container Dockerfile/image digest;
- exact preflight commands and smoke tests;
- whether canonical hosted M03 reports x86-64 and the exact ABI reference used in learner-facing design;
- exact GCC/binutils/GDB package builds captured by the image;
- final M04 dataset/access-order fixture and repetition/warmup protocol after smoke testing;
- whether P0's opaque persistence adapter uses a simple file or hidden SQLite at each checkpoint.

---

## 17. Source Register

All current/version-sensitive claims below were checked **2026-08-31**. Classic sources are included for mechanism/pedagogy even when not version-sensitive.

| Source | Institution / project / author | Exact URL / reference | Supports | Evidence layer | Limitations / notes |
|---|---|---|---|---|---|
| The Unicode Standard, Version 17.0 | Unicode Consortium | https://www.unicode.org/versions/Unicode17.0.0/ | Current Unicode version; encoding forms and conformance context | SPECIFICATION | Large standard; learner-facing use must be bounded and paraphrased |
| Unicode UTF-8/UTF-16/UTF-32 & BOM FAQ | Unicode Consortium | https://www.unicode.org/faq/utf_bom.html | UTF-8 byte-oriented encoding, reversibility/round trip, no endian issue for UTF-8 byte sequence | SPECIFICATION / explanatory | FAQ is explanatory companion; normative details reside in Standard |
| WG14 official home | ISO/IEC JTC1/SC22/WG14 | https://open-std.org/jtc1/sc22/wg14/ | Current C standard status: C23 / ISO/IEC 9899 adopted 2024 | SPECIFICATION metadata | Full ISO standard text not freely redistributable by default |
| N2872 / N2888 exact-width integer proposals | WG14 / Jens Gustedt | https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2872.htm ; https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2888.htm | Explicit historical/committee statement that C23 uses two's complement signed representation | SPECIFICATION history | Proposal history, not substitute for final standard wording |
| Python `struct` docs | Python Software Foundation | https://docs.python.org/3/library/struct.html | Explicit byte-order/size/alignment control for observation surface | IMPLEMENTATION | Python-specific teaching surface, not representation principle |
| Python 3.12 `time` docs | Python Software Foundation | https://docs.python.org/3.12/library/time.html | `perf_counter` / `perf_counter_ns` measurement semantics | IMPLEMENTATION | Timer does not identify causal mechanism |
| GNU Binary Utilities `objdump` | GNU / Sourceware | https://sourceware.org/binutils/docs/binutils/objdump.html | `-d` disassembly and `-S` source/disassembly observation | IMPLEMENTATION | Output and syntax vary by architecture/version |
| GDB Source and Machine Code | GNU / Sourceware | https://www.sourceware.org/gdb/current/onlinedocs/gdb.html/Machine-Code.html | Source-line ↔ address mapping, disassemble, instruction inspection | IMPLEMENTATION | Container ptrace capability must be smoke-tested |
| RISC-V Ratified Specifications Library | RISC-V International | https://docs.riscv.org/reference/home/index.html | Current ratified ISA library; unprivileged spec v20260120 at check date | SPECIFICATION | Not recommended as required runtime toolchain for M03 slice |
| Linux perf events and tool security | Linux kernel documentation | https://docs.kernel.org/admin-guide/perf-security.html (mirrors may render from kernel.org CDN) | `perf_event_paranoid`, unprivileged counter restrictions/security rationale | IMPLEMENTATION / SPEC-like kernel interface docs | Host/container policy varies; reason `perf` cannot be mandatory |
| Git `git diff` documentation | Git project | https://git-scm.com/docs/git-diff | Diff as exact change/evidence mechanism | IMPLEMENTATION | Git workflow beyond minimal evidence is out of scope |
| GitHub Codespaces dev-container setup docs | GitHub | https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration | Repository-specific dev container supports reproducible Codespaces environment | CURRENT PRACTICE / IMPLEMENTATION | UI/product details may change; principle is reproducible environment declaration |
| Dev Containers image support/EOL tracking | Dev Containers project | https://github.com/devcontainers/images/discussions/1464 | Ubuntu 24.04 Noble and Python 3.12 supported image families; current image lifecycle | CURRENT PRACTICE | Community/project support table can change; recheck during implementation |
| Ubuntu package `gcc-13` in Noble | Ubuntu | https://packages.ubuntu.com/noble/gcc-13 | Noble GCC 13 package family/current update information | IMPLEMENTATION | Exact package revision moves with security/updates; record in image, don't teach as semantic truth |
| Open Data Structures | Pat Morin / open textbook project | https://opendatastructures.org/ | Asymptotic notation; selected data structures; explicit CC BY license | PRINCIPLE / classic teaching | Much broader than Core; adapt only bounded slices |
| Cornell CS2110 lecture notes index | Cornell University | https://www.cs.cornell.edu/courses/cs2110/2014sp/lecturenotes.html | Classic pairing of searching/asymptotic complexity and loop invariants | Classic teaching | Older course; public availability does not establish adaptation rights |
| Harvard CS50 current/near-current Memory notes | Harvard CS50 | https://cs50.harvard.edu/extension/2026/spring/notes/4/ | Low-cognitive-load hex/memory visualization pattern | Classic/current teaching | C-course sequence differs from Essential CS; rights must be checked before reuse |
| CMU CS:APP course/book ecosystem | Carnegie Mellon / Bryant & O'Hallaron | https://csapp.cs.cmu.edu/ | Classic systems sequence; Data Lab/machine/memory-hierarchy activity families | Classic teaching | Assignment/book rights are restricted/unclear for redistribution; existing Blueprint keeps Data Lab rights-gated |
| NIST/SEMATECH Measurement Process Characterization | NIST / Croarkin | https://www.nist.gov/publications/nistsematech-engineering-statistics-handbook-chapter-2-measurement-process | Repeatability, reproducibility, stability, uncertainty as measurement concepts | PRINCIPLE / statistics authority | Far deeper than M04; designer evidence only, not a statistics syllabus |
| NIST Numerical Reproducibility | NIST | https://www.nist.gov/programs-projects/numerical-reproducibility | Environment/order/precision can affect reproducibility of computation | PRINCIPLE / CURRENT research context | Focused on numerical computation, not a direct lab template |
| Essential CS canonical Blueprint maps/policies | CN-JJB/essential-cs | Repository `main @ dab37131627fbc09e187300d3235ff6c0a10c57c` | Slice boundaries, first homes, competencies, DAG, Lab set, P0 mapping, policy constraints | Architecture authority | Internal project authority; not external technical evidence |

### 17.1 Sources intentionally not used as authority

- AI/model memory or generated summaries;
- blogs for current compiler/kernel/tool-version claims;
- benchmark-number lists as fixed constants;
- vendor marketing for architecture/tool selection;
- rights-unclear assignment mirrors as adaptation permission.

---

## 18. Readiness Recommendation

**READY FOR DESIGN**

The next Design task may safely assume that M00–M04 can be designed without changing the canonical curriculum architecture; that the key stable mechanisms, misconceptions, evidence patterns, source routes, environment constraints, and P0 stopping boundary above are sufficient to avoid rediscovering foundational research.

The Design task should preserve the proposed minimal-environment direction but treat exact container digest, exact tool package builds, M03 hosted architecture verification, M04 measurement fixture/protocol, and P0 file-vs-hidden-SQLite fixture choice as implementation-time decisions requiring smoke tests.

OQ-BP-001, OQ-BP-003, and OQ-BP-006 remain intentionally unresolved in their canonical states. This dossier proposes a bounded OQ-BP-006 first-slice baseline but does not close it or create a Decision.

---

## 19. Completion Report

### Status

**READY FOR LEAD REVIEW**

### Deliverable

`research/foundations-system-mechanics-vertical-slice-v0.1.md`

### Files changed

- `research/foundations-system-mechanics-vertical-slice-v0.1.md`

Expected content-file count: **1**.

### Research performed

Read current GitHub canonical state at `main @ dab37131627fbc09e187300d3235ff6c0a10c57c`, including AGENTS, project status, invariants, decisions, open questions, Blueprint exit audit, charter, learner profile, learning outcomes, Curriculum Map, Competency Matrix, Concept Registry, lesson map, dependency graph, final reconciliation, assessment architecture, Lab/source selection, modern technology cases, research/source policy, Lab policy, review policy, Definition of Done, and Issue #25.

External research prioritized current/primary evidence: Unicode Standard 17.0 and UTF FAQ; WG14/C23 materials; RISC-V ratified ISA library; GNU binutils/GDB documentation; Linux kernel `perf` security documentation; Python timing/representation documentation; Git/GitHub Codespaces documentation; Dev Containers lifecycle data; Ubuntu Noble package data; and classic course/textbook references including Open Data Structures, CS50, Cornell, CS:APP, and NIST measurement references.

### Evidence summary

- **PRINCIPLE:** representation is distinct from information; asymptotic growth is distinct from measured time; ISA is a software-visible abstraction; locality/hierarchy explain large performance effects; observation is distinct from causal explanation; measurement conclusions require workload/environment/variation limits.
- **SPECIFICATION:** Unicode/UTF-8 rules; C23 signed representation context; ISA/ABI contracts; normative/official tool interface behavior where applicable.
- **IMPLEMENTATION:** GNU compiler/disassembler/debugger output; Python timing API; Linux performance-counter access; host ISA/container restrictions.
- **CURRENT PRACTICE:** Ubuntu/Dev Container/Python/toolchain baseline; current supported version families; `perf` availability; hosted-environment behavior.

Sources that differ were separated by layer/version/environment rather than flattened. In particular, two's-complement representation does not imply identical signed-overflow semantics across languages, and `perf` capability depends on Linux/container security configuration rather than the cache/locality principle.

### Environment / OQ-BP-006 proposal

Recommend for Web Lead review: Ubuntu 24.04 LTS Noble Dev Container/Codespace, Python 3.12, Noble GCC 13-class GNU toolchain, binutils, GDB, Git, and minimal shell/core utilities. Record exact versions in preflight; pin the final container by immutable digest at runnable implementation time. Treat `perf` as optional. Defer QEMU/RISC-V cross-toolchain, SQLite/PostgreSQL teaching pins, browser, orchestration, and observability-tool pins until affected Modules/Labs. This is a proposal only; OQ-BP-006 remains open.

### P0 boundary

During M00–M04, learner-owned P0 work stops at process-local data model/state transitions, representation/serialization, round-trip/application invariant, and size estimation. A simple file or hidden SQLite persistence adapter may be supplied; the learner may observe state surviving a bounded restart but must not be expected to explain durability, filesystem, database engine, transaction, recovery, query/index, or storage mechanisms. Those wait for M08/M09/M13/M14. P0 is not a curriculum prerequisite.

### Risks / open questions

- **Research uncertainty:** exact M04 locality fixture/repetition design must be canonical-image smoke-tested; current source evidence does not determine one universally best microbenchmark.
- **Implementation-time questions:** immutable Dev Container digest, exact package builds, hosted architecture, GDB capability, file-vs-hidden-SQLite P0 fixture.
- **Architecture escalation:** none currently. OQ-BP-001/003 stay RFC-gated; OQ-BP-006 stays implementation-time/open.

### Verification performed

Repository-level state/actions performed through GitHub connector:

- confirmed `main` head is `dab37131627fbc09e187300d3235ff6c0a10c57c`;
- created branch `vertical-slice/issue-25-foundations-system-mechanics-research` from that exact SHA;
- rechecked `main` before PR preparation and confirmed it remains at that SHA;
- compared `main...vertical-slice/issue-25-foundations-system-mechanics-research`: branch is ahead by one commit, behind by zero, and the merge base is current `main`;
- compare reports exactly one changed file, `research/foundations-system-mechanics-vertical-slice-v0.1.md`, status `added`;
- no canonical meta file, Lesson, Lab implementation, project implementation, Stage/Module/Lesson ID, H/S edge, competency, Concept Registry, Lab-selection artifact, P0–P9 mapping, or Open Question file was modified;
- explicit scope review confirms no ninth competency is introduced, Open Questions remain open, and P0 is not a curriculum prerequisite;
- current implementation/version claims are dated 2026-08-31 and tied to authoritative/primary sources in the Source Register;
- licensing/provenance uncertainty is marked rather than inferred as permission.

A literal local `git diff --check` is not available through the connected GitHub execution surface because no authenticated/networked local repository clone is exposed. The one-file GitHub compare and final patch/whitespace inspection are therefore used as the available diff-equivalent check; this limitation is reported rather than falsely claiming a command was run.

### Assumptions

- GitHub connector state is authoritative because the local container cannot resolve GitHub network access; repository reads/writes/compare operations are therefore performed through the connected GitHub API.
- `research/` accepts the new dossier path without additional directory-level `AGENTS.md`; no conflicting directory instruction was found in the required project-state reading.
- learner-facing canonical language remains Chinese, but this Research Dossier is written in English technical prose consistent with existing meta/research artifacts and is not Lesson prose.

### Prompt deviations

- Literal `git diff --check` could not be executed because the available GitHub connection does not expose a local authenticated clone; an API compare plus patch/whitespace inspection is used instead. No content-scope deviation.

### Out-of-scope necessary fixes

None identified. No canonical architecture edit is required by this research.

### Recommended Web Lead review focus

1. Accept/reject the proposed Noble/Python 3.12/GNU toolchain first-slice baseline and the rule to pin the immutable image digest only at runnable preflight implementation.
2. Confirm native x86-64 as the preferred M03 first implementation case versus selecting RISC-V earlier despite the extra setup burden.
3. Confirm the M04 rule that `perf` is optional and timer-based repeated measurement is sufficient for Core evidence.
4. Confirm P0 persistence opacity boundary, especially whether early checkpoints should prefer a simple file fixture before a hidden SQLite adapter.
5. Review rights-sensitive classic-source candidates (CS:APP/course materials) and keep all unresolved items link/reference-only.

Do not merge this PR, do not edit `main`, and do not self-mark this work `VERIFIED`.
