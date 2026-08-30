# Blueprint Lab and Source Expedition Selection Map v0.1

Status: **PROPOSED — READY FOR LEAD RECONCILIATION**

Task: Issue #12, child of Issue #9
Date checked: 2026-08-30
Scope: Blueprint-level selection only. This document does not implement Labs,
copy third-party assignment material, or change the canonical curriculum maps.

## 1. Selection decision

This map selects **3 Required Labs**, **4 Optional Labs**, and **5 Source
Expeditions**. It intentionally does not assign one Lab to every Module. The
selection follows **Adopt → Adapt → Build**:

- Adopt one bounded, link-only OSTEP exercise whose original instructions and
  code remain at the authoritative source.
- Adapt six activities around exact sources while writing Essential CS-owned
  framing, prediction prompts, evidence requirements, safety boundaries, and
  stopping rules. Adaptation never means copying third-party prose, code,
  screenshots, tests, or grading infrastructure.
- Build no standalone mechanism Lab in this artifact. Conditional project
  integration gaps are recorded rather than filled with invented toy demos.

The first traversal should expose a small reusable set of mechanisms:
representation constraints, process/syscall boundaries, synchronization and
progress, HTTP interfaces/intermediaries, TCP byte-stream semantics, query
planning/index trade-offs, and evidence-oriented observability. Other Modules
receive short observations, project integration, or Source Expeditions rather
than another full Lab.

### 1.1 Status and license vocabulary

- **Adopt — link-only:** the source activity is used as published through a
  narrow route. Essential CS does not redistribute or adapt the source until
  rights are confirmed.
- **Adapt — rights-cleared or rights-gated:** Essential CS retains the
  mechanism and bounded activity pattern but supplies original framing and
  changes the scope. Bundling waits for the stated license gate.
- **License-cleared for the proposed use:** the checked source license permits
  the proposed redistribution/adaptation subject to notices and conditions;
  this is not a substitute for a release-time legal/provenance check.
- **Rights unresolved:** a public page, Git repository, or educational access
  path was found, but that fact is not permission to copy, adapt, or bundle.
- **Build gap:** an original Essential CS project fixture may still be needed
  for integration. It is not a reason to replace a classic mechanism Lab.

### 1.2 Measurement rule for selected activities

Where a selection measures behavior, the learner records the question,
platform/kernel/tool versions, dataset or traffic scale, baseline, warmup or
cold/warm state, repetitions, distribution or uncertainty, and the limit of
the causal claim. A local result is not an Internet result, and a profiler or
tracing tool can add overhead. The exact method is part of the future Lab
implementation and is not silently specified here as a final protocol.

## 2. Selected Lab map

### LAB-REQ-01 — HTTP interface, origin, and intermediary trace

- **Proposed Lab ID:** `LAB-REQ-01`.
- **Macro area:** `07` Networking; `08` Web & Browser Platform.
- **Module placement:** M11 Networking II: TLS, HTTP, CDN & Proxies; revisit in
  M12 Web & Browser integrated case.
- **Required vs Optional:** **Required**.
- **Adopt vs Adapt:** **Adapt**.
- **Decision:** Adapt the source specification and inspection activity.
- **Exact source/course/project:** IETF RFC 9110, *HTTP Semantics*, Sections
  1.1–1.3 (uniform interface and representations), 3.3–3.8 (clients,
  servers, origins, intermediaries, caches), 6 (message abstraction), and
  9.2.1 (idempotent methods); local `curl` and a learner-run localhost HTTP
  server. Source: <https://www.rfc-editor.org/rfc/rfc9110.html>.
- **Exact exercise or bounded slice:** Run one learner-owned localhost
  origin; capture one request/response with `curl -v`; inspect method, target,
  headers, status, representation, and framing; place a deliberately bounded
  localhost forwarding adapter between client and origin; compare direct and
  forwarded traces; perform one conditional-cache request with an explicit
  validator if the local server supports it. Do not reproduce RFC text or
  implement HTTP.
- **Mechanism revealed:** An HTTP client communicates with an origin through
  self-describing request/response messages; an intermediary changes the
  connection path and may satisfy a request from a cached representation;
  method semantics and retry safety are not the same as transport success.
- **Learner outcome:** The learner can trace one request across client,
  intermediary, and origin, distinguish resource from representation, explain
  what the response establishes and does not establish, and justify whether a
  retry is safe for the selected method.
- **Mapped competencies:** Trace, Explain, Observe, Correctness, Judge.
- **Prerequisites:** M00 shell and evidence habits; M06 process/interface
  basics; M10 basic sockets/transport; M11 lesson-level HTTP vocabulary before
  the Lab. `curl` command literacy is a lab prerequisite, not a new HTTP
  concept.
- **Cognitive load:** Medium. The bounded route uses one origin, one
  intermediary, and one cache distinction; ABNF, HTTP/2/3 wire formats, CDN
  internals, and browser implementation are excluded.
- **Linux/environment requirements:** Canonical Linux shell, Python standard
  library or another already-approved local HTTP server, `curl`, localhost
  only, and a writable temporary directory. No DNS, external network, cloud
  account, or browser automation is required.
- **Setup burden:** Low. The future implementation should provide a resettable
  temporary directory and a small command wrapper rather than a web framework.
- **Approximate runtime class:** Execution is **seconds to low minutes** for
  the trace and reset; no long-running measurement is required.
- **Prediction step:** Before running the commands, predict which party knows
  the request target, which headers survive forwarding, whether the
  intermediary can answer without contacting the origin, and whether a
  repeated GET differs in retry safety from a mutation.
- **Observation:** Preserve the direct and forwarded `curl -v` transcripts,
  the response status/headers/body hash or short fixture identifier, and a
  path diagram showing each connection.
- **Controlled break/failure:** Stop the origin, send a malformed or
  unsupported request to localhost, and change the cache validator so the
  conditional request no longer matches. Do not send malformed traffic to a
  public service.
- **Explanation/judgment:** Explain interface semantics versus implementation,
  identify where authority and failure move when an intermediary is added,
  state what the trace cannot prove, and judge whether the intermediary buys
  anything for this tiny workload.
- **Cleanup/reset requirements:** Kill only learner-owned local processes;
  delete the temporary fixture and cache directory; restore the origin port;
  verify no listener remains. A reset must recreate the same fixture from
  scratch.
- **Safety boundary:** Localhost and course-owned processes only. No public
  proxy, public cache, credential, third-party endpoint, traffic generation,
  or certificate bypass.
- **Provenance:** RFC 9110 is the normative source; the local server and
  prompts are original Essential CS framing. The RFC's Sections 3.3–3.8 and
  6.2–6.6 are the source route, not copied course text.
- **License status:** RFC 9110 is subject to the IETF Trust Legal Provisions;
  code components extracted from it require the Revised BSD License notice.
  The Lab should paraphrase and link. No RFC code or substantial text should
  be bundled without the required notice and review.
- **Redistribution/adaptation status:** **Adaptation is limited to an
  Essential CS-owned activity wrapper and local fixture.** Bundling RFC text,
  figures, or extracted code is blocked until the IETF terms are reviewed for
  the exact use.
- **Maintenance/version risk:** Low for HTTP semantics; medium for local
  `curl` output, server defaults, and cache behavior. Recheck the RFC errata,
  command output, and the chosen local server before release.
- **Mini Cloud App relationship:** P1/P3 can use the app's local interface as
  a later integration surface, but this Lab remains a separate protocol
  mechanism activity. It exposes the app's boundary without making the app
  the HTTP lesson.
- **Original Build gap:** **No mechanism gap.** A project-specific P1/P3
  request trace remains an integration checkpoint, not a second HTTP Lab.

### LAB-REQ-02 — xv6 `sleep`: user program through syscall entry

- **Proposed Lab ID:** `LAB-REQ-02`.
- **Macro area:** `05` Operating Systems.
- **Module placement:** M06 Processes, Syscalls & Execution Context; short
  revisit in M08 Files, Filesystems & System I/O.
- **Required vs Optional:** **Required**.
- **Adopt vs Adapt:** **Adapt**.
- **Decision:** Adapt one official MIT 6.1810 exercise and its source
  route; do not assign the full xv6 sequence.
- **Exact source/course/project:** MIT 6.1810 Fall 2025, *Lab: Xv6 and Unix
  utilities*, the `sleep` exercise. Official lab page:
  <https://pdos.csail.mit.edu/6.1810/2025/labs/util.html>. Upstream xv6
  software source: <https://github.com/mit-pdos/xv6-riscv>, `riscv` head
  checked at `35b088427ef37611c38afdeed5a52a278cae38f9`.
- **Exact exercise or bounded slice:** Boot the official xv6 lab tree in
  QEMU; implement only the user-level `sleep` program using the existing
  `pause()` system call; trace the path through `user/sleep.c`, the user API
  declaration, generated user syscall stub, syscall dispatch, and
  `kernel/sysproc.c`; run `sleep` with valid and missing arguments. Do not
  implement a new kernel subsystem, grade server, shell extension, or later
  lab.
- **Mechanism revealed:** A user request crosses a user/kernel boundary through
  an API, generated entry stub, syscall dispatch, and kernel implementation;
  a process observes kernel-defined time rather than directly controlling the
  timer device.
- **Learner outcome:** The learner can trace a small operation from a user
  program to the kernel and back, distinguish source-level function calls from
  syscalls, and explain the process/toolchain/emulator boundaries.
- **Mapped competencies:** Trace, Explain, Observe, Diagnose, Learn-New-Tech.
- **Prerequisites:** M00 shell/Git and reset discipline; M03 minimal C,
  pointers, and call/return; M06 process vocabulary; a prior explanation of
  user mode, kernel mode, and system-call interfaces. The Lab teaches the
  route, not RISC-V assembly in depth.
- **Cognitive load:** Medium-high. The mechanism is small, but C, QEMU, a
  RISC-V cross-compiler, and generated syscall code create accidental load.
  The route is one utility and one syscall only.
- **Linux/environment requirements:** Canonical Linux with QEMU and the
  RISC-V `newlib` cross-toolchain required by the official xv6 README; the
  official sample uses a 128 MiB QEMU guest. Dev Container/Codespace is the
  preferred reproducibility path. Native Windows is not canonical; WSL or a
  Linux container is a convenience route only if QEMU/toolchain behavior is
  verified.
- **Setup burden:** Medium-high. The toolchain is the main risk; future
  course packaging should pin a known-compatible QEMU/toolchain combination
  and provide a smoke test before the learner starts.
- **Approximate runtime class:** Guest build and a short `sleep` run are
  **low minutes** after setup; cross-toolchain installation is the dominant
  setup cost, not execution time.
- **Prediction step:** Before opening the source route, predict which files
  must change, whether `sleep` can call the kernel implementation directly,
  what happens when the argument is absent, and why a guest tick is not the
  same thing as a host wall-clock measurement.
- **Observation:** Save the source-route diagram, the xv6 shell transcript,
  the syscall-related diff, and one comparison between requested ticks and
  observed host elapsed time labeled as an emulator observation rather than a
  timing guarantee.
- **Controlled break/failure:** Omit the argument, pass an invalid argument,
  temporarily remove the user program from the build list, or trace the
  existing syscall before the student implementation. Do not alter host
  kernel code, device state, or any external system.
- **Explanation/judgment:** Explain why the syscall API is an interface and
  why the user program cannot assume the kernel implementation's layout;
  identify which failures are compile-time, guest-runtime, or host-toolchain
  failures; judge what xv6 reveals and what it hides compared with Linux.
- **Cleanup/reset requirements:** Exit QEMU with its documented local escape;
  discard or reset the learner's xv6 working tree to the official lab
  starting point; remove generated disk images and build artifacts when
  resetting; preserve only the learner's evidence outside the source tree.
- **Safety boundary:** QEMU guest and learner-owned source tree only. No
  kernel modules, host device access, privileged experiments, network target,
  gradescope account, or public service. The future Lab must not include
  submission or grading-server instructions.
- **Provenance:** MIT 6.1810 Fall 2025 lab page supplies the exact exercise;
  MIT PDOS supplies xv6 source and book links. The Lab retains the official
  exercise's mechanism and narrows its scope; all instructions and evidence
  prompts are Essential CS-authored.
- **License status:** The xv6 software repository includes an MIT license
  requiring copyright and permission notices. The Fall 2025 lab page displays
  CC BY 3.0 US. Attribution and license notices must travel with any bundled
  source or adapted lab material.
- **Redistribution/adaptation status:** **License-cleared in principle for
  the checked xv6 software and CC BY lab page, subject to attribution and
  release review.** Pin the exact lab tree/commit actually used. Do not
  assume the public course page alone covers every linked book, generated
  file, or future lab repository asset.
- **Maintenance/version risk:** High. The upstream xv6 `riscv` branch changes;
  the annual 6.1810 lab page and lab tree can change independently; QEMU and
  cross-toolchain compatibility matters. Pin the lab tree, source revision,
  toolchain, and QEMU in the implementation dossier.
- **Mini Cloud App relationship:** P1/P3 can later inspect the app server's
  native Linux process and syscall boundary. The app does not replace this
  guest-kernel mechanism lab.
- **Original Build gap:** **No OS mechanism gap.** A small app process trace
  remains useful as integration, but a custom teaching kernel is not justified.

### LAB-REQ-03 — OSTEP semaphore rendezvous

- **Proposed Lab ID:** `LAB-REQ-03`.
- **Macro area:** `10` Concurrency.
- **Module placement:** M15 Concurrency: Threads, Races & Synchronization;
  the database isolation material in M14 is a motivating revisit, not a
  prerequisite to the source code itself.
- **Required vs Optional:** **Required**.
- **Adopt vs Adapt:** **Adopt — link-only**.
- **Decision:** Use the exact upstream skeleton and instructions through a
  stable permalink; Essential CS supplies a short original prediction/evidence
  wrapper but does not copy or modify the source in this repository.
- **Exact source/course/project:** OSTEP v1.10, *Threads / Semaphores*
  homework, official index:
  <https://pages.cs.wisc.edu/~remzi/OSTEP/Homework/homework.html>. Exact
  source repository commit checked: `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`.
  Bounded files: `threads-sema/README.md`, `threads-sema/rendezvous.c`, and
  optionally the structurally similar `threads-sema/barrier.c` at the same
  commit. Permalinks:
  <https://github.com/remzi-arpacidusseau/ostep-homework/blob/afb36ca8ddbf81d847d18f6bd18a87f0a18667f2/threads-sema/README.md>,
  <https://github.com/remzi-arpacidusseau/ostep-homework/blob/afb36ca8ddbf81d847d18f6bd18a87f0a18667f2/threads-sema/rendezvous.c>.
- **Exact exercise or bounded slice:** Complete only `rendezvous.c`: make
  each child print its `before` message before either child prints its `after`
  message using semaphores; compile with the source README's `gcc -o foo
  foo.c -Wall -pthread` pattern; test by inserting local sleeps at different
  points. `barrier.c` is an optional extension, not part of the Required Lab.
- **Mechanism revealed:** A semaphore can express ordering between threads;
  mutual exclusion alone does not establish a rendezvous or progress
  invariant. Scheduling nondeterminism makes an incorrect ordering observable.
- **Learner outcome:** The learner can state a cross-thread ordering invariant,
  predict an invalid interleaving, repair the synchronization, and explain
  why the repair does not merely make one observed run look correct.
- **Mapped competencies:** Correctness, Trace, Diagnose, Explain, Judge.
- **Prerequisites:** M06 process/thread distinction; M15 basic shared-state,
  interleaving, mutex, and semaphore vocabulary; POSIX thread compilation;
  shell/Git reset habits. No database, broker, or distributed system is
  required.
- **Cognitive load:** Medium. The skeleton is small and the task has one
  progress/order invariant. Reader-writer fairness, starvation, condition
  variables, and the full homework directory are out of scope.
- **Linux/environment requirements:** Canonical Linux, `gcc` or compatible C
  compiler, POSIX `pthread` support, shell, and no network. A normal user
  account is sufficient.
- **Setup burden:** Low. A clean checkout of the pinned directory and a local
  compile are sufficient.
- **Approximate runtime class:** Execution is **sub-second to seconds**; the
  learner should repeat enough runs to expose scheduling variation, without
  treating repetition count as a proof of correctness.
- **Prediction step:** Before editing, enumerate an interleaving in which one
  child prints `after` too early; state the invariant “both `before` events
  precede both `after` events”; predict where each semaphore wait/post must
  occur and why one semaphore is insufficient for both directions.
- **Observation:** Record output from correct and intentionally incomplete
  versions, source changes made locally, the invariant, and a small
  interleaving table. If the incorrect version sometimes appears correct,
  record that uncertainty rather than claiming the bug is absent.
- **Controlled break/failure:** Remove one wait/post, insert `usleep` at
  different local points, or run with a small bounded repetition wrapper.
  Never create an unbounded thread storm or run this against a remote system.
- **Explanation/judgment:** Explain ordering versus mutual exclusion,
  distinguish empirical evidence from a proof argument, identify starvation
  and fairness as not solved by this bounded rendezvous, and judge whether a
  semaphore or a simpler join is the right abstraction for this requirement.
- **Cleanup/reset requirements:** Terminate only local child processes; remove
  binaries and local output; restore the exact pinned source skeleton before a
  fresh attempt; cap all repetition wrappers and clean them on interruption.
- **Safety boundary:** Local POSIX threads and learner-owned processes only.
  No privileged synchronization, kernel exploit, external target, or
  offensive security task.
- **Provenance:** OSTEP authors' official homework index and the authors'
  `ostep-homework` repository. The selected file names and current commit were
  live-checked on 2026-08-30.
- **License status:** The GitHub API reports no repository license for
  `remzi-arpacidusseau/ostep-homework`, and no explicit reuse license was
  verified in the checked repository evidence. Educational availability and
  public hosting are not permission to redistribute or adapt.
- **Redistribution/adaptation status:** **Bundling, copying, and adapting the
  source are blocked.** Required use is link-only to the pinned upstream
  files, with original Essential CS prompts kept separate. Before any
  handout or code bundle is produced, obtain a repository license or direct
  permission and record it in the attribution register.
- **Maintenance/version risk:** Medium-high. The repository is active enough
  to have a 2026 commit, but the default branch is `master`, the repository
  license is unresolved, and the exact code can change. Recheck the commit,
  file list, compiler behavior, and rights before release.
- **Mini Cloud App relationship:** P5 may later reuse the same invariant in a
  project-specific concurrent request or transaction exercise. The project
  must not replace this generic synchronization mechanism with a web-framework
  race demo.
- **Original Build gap:** **Yes, conditional P5 integration gap.** A small
  app-specific race/transaction harness may be needed to connect the invariant
  to ownership and durable state, but only after this mechanism is adopted
  and only if the Mini Cloud App cannot supply the integration naturally.

## 3. Optional Lab map

Optional Labs are not required for the first shared traversal. They are
selected because they expose useful mechanisms, but their setup, architecture,
maintenance, or rights burden makes them poor universal prerequisites.

### LAB-OPT-01 — CS:APP Data Lab, narrowed bit-representation slice

- **Proposed Lab ID:** `LAB-OPT-01`.
- **Macro area:** `01` Information & Representation; supporting `03` Machine.
- **Module placement:** M01 Bits, Bytes & Representation; optional revisit in
  M03 Machine: ISA & Execution.
- **Required vs Optional:** **Optional**.
- **Adopt vs Adapt:** **Adapt — rights-gated**.
- **Decision:** Adapt — rights-gated.
- **Exact source/course/project:** CMU CS:APP3e *Data Lab*. Official lab
  index: <https://csapp.cs.cmu.edu/3e/labs.html>. Exact instructor README:
  <https://csapp.cs.cmu.edu/3e/README-datalab>.
- **Exact exercise or bounded slice:** Use a handout authorized for the
  learner's use and select a small set of integer puzzles from the official
  `bits.c`/`src/selections.c` mechanism, centered on bit masking, two's
  complement, and one boundary case. Retain the restricted operator contract
  and correctness checker; omit floating-point breadth, `dlc` portability
  assumptions, the contest, grading server, and the 15-puzzle default. If
  rights are not cleared, use the official link only and do not redistribute
  any handout or code.
- **Mechanism revealed:** A representation contract and operator restriction
  make bit-level behavior and edge cases explicit; correctness testing is
  distinct from satisfying the syntactic restriction.
- **Learner outcome:** The learner predicts integer boundary behavior, traces
  a bit-level expression, and explains why a passing sample is not enough for
  a representation function.
- **Mapped competencies:** Trace, Explain, Correctness, Diagnose, Estimate.
- **Prerequisites:** M01 binary arithmetic and signed/unsigned values; basic C
  expressions; test output reading.
- **Cognitive load:** Medium-high. The narrow slice is manageable, but C and
  the custom checker add load; floating representation and the full puzzle set
  are out of scope.
- **Linux/environment requirements:** Canonical Linux, C compiler, and the
  source's `bison`/`flex` requirement if the official `dlc` is built. The
  official page states that binary portability and x86/Linux assumptions can
  matter.
- **Setup burden:** Medium-high and rights-dependent. A future dossier must
  validate the exact handout, toolchain, and binary portability before
  offering it.
- **Approximate runtime class:** Checker execution is **seconds**; setup and
  debugging are the significant cost.
- **Prediction step:** Predict the result for zero, sign-bit, and minimum
  signed integer cases before running the supplied checker.
- **Observation:** Preserve checker output for selected edge cases and a
  table separating mathematical result, permitted operators, and observed
  test coverage.
- **Controlled break/failure:** Change one mask or shift, run edge cases, and
  compare checker failure with the intended invariant. No memory corruption,
  exploit, or network component is used.
- **Explanation/judgment:** Explain why bit patterns are not inherently signed
  or unsigned, how the contract narrows implementation choices, and judge
  whether this concentrated C exercise buys more transfer than a simpler
  Python byte observation at this point.
- **Cleanup/reset requirements:** Remove generated handout/build files; reset
  to the authorized starter; do not retain instructor solutions or grading
  assets.
- **Safety boundary:** Local code and checker only; no contest endpoint and no
  exploit lab. The optional activity is not Attack Lab.
- **Provenance:** Bryant and O'Hallaron, CMU CS:APP3e lab pages and Data Lab
  README; checked 2026-08-30.
- **License status:** The official page identifies authorship and distributes
  student handouts through an account, but the checked pages do not establish
  a redistribution/adaptation license for the lab handout, checker, or
  puzzles.
- **Redistribution/adaptation status:** **Bundling/adaptation blocked pending
  permission or an explicit license.** Link-only self-study is the fallback.
- **Maintenance/version risk:** High. The README records an old 2011/2018
  provenance, a 2019 update on the lab index, and Linux binary portability
  concerns; future toolchains may change behavior.
- **Mini Cloud App relationship:** The app can revisit representation and
  identifier correctness, but Data Lab should remain independent from app
  feature work.
- **Original Build gap:** No. The selected mechanism is already covered by an
  authoritative classic activity; do not build a Python imitation merely to
  avoid the rights gate.

### LAB-OPT-02 — Stanford CS144 Checkpoint 2, TCP receiver slice

- **Proposed Lab ID:** `LAB-OPT-02`.
- **Macro area:** `07` Networking.
- **Module placement:** M10 Networking I: IP, DNS & Transport; optional revisit
  in M16 Distributed Systems Foundations: Partial Failure & RPC.
- **Required vs Optional:** **Optional**.
- **Adopt vs Adapt:** **Adapt — rights-gated**.
- **Decision:** Adapt — rights-gated.
- **Exact source/course/project:** Stanford CS144 Fall 2025, *Checkpoint 2:
  the TCP receiver*, exact assignment:
  <https://cs144.github.io/assignments/check2.pdf>. Course home and checkpoint
  index: <https://cs144.github.io/>.
- **Exact exercise or bounded slice:** Retain only the `Wrap32` conversion and
  `TCPReceiver` receive/send behavior: sequence-number wrapping, reassembly,
  acknowledgment number, and advertised window. Use the supplied local tests
  and starter architecture if authorized; omit Checkpoints 0–1, sender,
  network interface, router, Internet capstone, Gradescope, and course
  submission instructions.
- **Mechanism revealed:** A TCP receiver turns wrapped sequence numbers and
  segments into an ordered byte stream while advertising the next required
  byte and available capacity; protocol correctness is an invariant over
  out-of-order and duplicate input.
- **Learner outcome:** The learner can trace a segment into receiver state,
  predict acknowledgment/window behavior, and explain why a 32-bit sequence
  number needs an absolute checkpoint.
- **Mapped competencies:** Trace, Explain, Correctness, Diagnose, Judge.
- **Prerequisites:** M10 transport vocabulary, byte streams and reassembly,
  integer wrapping, C++ reading, and test-driven debugging. This is not an
  early networking Lab.
- **Cognitive load:** High. The exact checkpoint assumes prior Minnow modules,
  CMake, C++, and a multi-checkpoint codebase. It is optional precisely to
  protect the Core traversal.
- **Linux/environment requirements:** Canonical Linux, C++ compiler, CMake,
  sanitizers where available, and the authorized Minnow repository. Local
  tests only; no public network path is needed.
- **Setup burden:** High. The future implementation must pin the course
  starter branch/commit and verify CMake/compiler/sanitizer behavior on the
  canonical Linux image.
- **Approximate runtime class:** Local test execution is **seconds to minutes**;
  build/debug cycles are the dominant cost.
- **Prediction step:** Before tests, predict `ackno` and window size for an
  initial SYN, an out-of-order payload, duplicate data, wrapped sequence
  numbers, and a FIN at the stream boundary.
- **Observation:** Preserve test names/output, one segment-state trace, and a
  table mapping sequence number, absolute sequence number, and stream index.
- **Controlled break/failure:** Use only local test fixtures to omit a segment,
  duplicate a segment, wrap near `2^32`, or advertise an incorrect window.
  Do not send malformed packets to an external host.
- **Explanation/judgment:** Explain sequence-space ambiguity, reassembly
  invariants, and flow control; judge why the checkpoint is valuable but too
  implementation-heavy for Required status.
- **Cleanup/reset requirements:** Remove build directories and generated
  reports; reset to the authorized starter branch; terminate no process other
  than learner-owned local test/build processes.
- **Safety boundary:** Local code, local tests, and optionally a local network
  namespace only. No public scanning, packet injection, or Internet target.
- **Provenance:** Stanford CS144 Fall 2025 course and Checkpoint 2 document;
  checked 2026-08-30.
- **License status:** The public course page and assignment PDF establish the
  exercise, but the checked sources do not establish permission to redistribute
  or adapt assignment text, starter code, tests, or Minnow code.
- **Redistribution/adaptation status:** **Bundling/adaptation blocked pending
  rights confirmation.** Until then, link to the exact PDF and require the
  learner to obtain the authorized starter independently; Essential CS may
  provide original conceptual prompts only.
- **Maintenance/version risk:** High. The checked course is Fall 2025; future
  branches, starter code, C++ requirements, and test APIs can change.
- **Mini Cloud App relationship:** P3 timeout/retry reasoning can reuse the
  receiver's acknowledgment concept, but the Mini Cloud App must not grow a
  custom TCP stack.
- **Original Build gap:** No TCP mechanism gap. A local app timeout exercise
  may remain as project integration, not a replacement for this optional
  protocol implementation.

### LAB-OPT-03 — PostgreSQL `EXPLAIN` and transaction-isolation comparison

- **Proposed Lab ID:** `LAB-OPT-03`.
- **Macro area:** `09` Databases; supporting `10` Concurrency.
- **Module placement:** M13 Databases: Storage & Indexing and M14 Databases:
  Transactions, Recovery & Isolation.
- **Required vs Optional:** **Optional** comparison Lab after SQLite fundamentals.
- **Adopt vs Adapt:** **Adapt**.
- **Decision:** Adapt official documentation into a small local comparison.
- **Exact source/course/project:** PostgreSQL current documentation, PostgreSQL
  18 at the check date: `EXPLAIN`,
  <https://www.postgresql.org/docs/current/sql-explain.html>, and transaction
  isolation, <https://www.postgresql.org/docs/current/transaction-iso.html>.
  PostgreSQL source tree for later inspection is pinned to current `master`
  head `2fb8da5a245661287833b05a1b2e275ddf83bbd7`.
- **Exact exercise or bounded slice:** On a disposable local PostgreSQL
  instance, load one deterministic table at two bounded scales; capture a
  baseline `EXPLAIN` and `EXPLAIN ANALYZE` for one selective query; add one
  index and compare plan, result equality, execution distribution, and write
  effect; run two local transactions that demonstrate one documented
  isolation behavior and rollback. Do not tune every planner setting, run a
  production benchmark, or replace SQLite as the project baseline.
- **Mechanism revealed:** A query planner estimates costs and chooses access
  paths; an index trades write/storage work for possible read behavior; a
  transaction isolation guarantee constrains concurrent outcomes rather than
  making all workloads fast.
- **Learner outcome:** The learner can form a workload hypothesis, read a
  sequential versus index plan, distinguish estimated from measured values,
  reproduce one isolation outcome, and judge PostgreSQL as an optional
  client/server comparison rather than a default dependency.
- **Mapped competencies:** Observe, Diagnose, Estimate, Correctness, Judge,
  Explain.
- **Prerequisites:** M08 files/storage, M13 SQL/data modeling and basic query
  plans, M14 transaction vocabulary, and the measurement methodology above.
- **Cognitive load:** Medium-high. Server process, roles, connection state,
  planner estimates, and transaction sessions are more than the baseline
  SQLite path; the dataset and query must remain small.
- **Linux/environment requirements:** Canonical Linux, a local PostgreSQL 18
  installation or pinned container, `psql`, and a disposable data directory.
  No cloud database or real learner data.
- **Setup burden:** Medium-high. A container may be a convenience path but
  cannot become a hidden Docker prerequisite; a native local package path
  must be documented if this remains selected.
- **Approximate runtime class:** Query runs are **seconds**; setup/reset and
  repeated controlled measurements are **minutes**. No claim is made about
  production performance.
- **Prediction step:** Predict when the planner should prefer a sequential
  scan, what adding the index costs, whether `EXPLAIN ANALYZE` changes the
  statement's side effects, and which transaction outcome is permitted under
  the selected isolation level.
- **Observation:** Record PostgreSQL version, schema/data generator, query,
  cold/warm state, plan estimates, actual rows/time, repetitions and
  distribution, buffer option if used, and the result-equality check.
- **Controlled break/failure:** Drop the index, change data selectivity, use a
  cold versus warm reset, deliberately roll back a transaction, and use a
  bounded serialization conflict if the selected isolation scenario supports
  it. Do not fill a host filesystem or use unbounded load.
- **Explanation/judgment:** Explain planner estimates versus causes, profiling
  overhead, index write cost, and isolation guarantees; judge whether the
  measured workload justifies a server database over the SQLite baseline.
- **Cleanup/reset requirements:** Stop the local instance; remove the
  disposable data directory/container; revoke or avoid persistent credentials;
  restore the seed dataset; delete dumps containing learner data.
- **Safety boundary:** Local disposable database, synthetic data, bounded
  queries, and no network exposure. Never run `EXPLAIN ANALYZE` on a mutation
  without an explicit transaction/rollback plan.
- **Provenance:** PostgreSQL official documentation and PostgreSQL project
  source; documentation and source were live-checked 2026-08-30.
- **License status:** PostgreSQL states that the server and documentation are
  released under the PostgreSQL License, subject to retaining the required
  notices. Documentation excerpts should still be paraphrased and linked;
  any bundled source must retain notices.
- **Redistribution/adaptation status:** **Adaptation is permitted in principle
  with attribution/notices**, but the exact documentation snippets, container
  image, dependency set, and future SQL fixtures require release review.
- **Maintenance/version risk:** Medium-high. Current documentation is
  PostgreSQL 18.6 and plans/behavior can vary across releases, statistics,
  hardware, and settings. Pin the version and record the review date.
- **Mini Cloud App relationship:** P4 can use the app's item-list query as a
  later integration measurement after a SQLite baseline. The Lab must not
  promote PostgreSQL, cache, queue, or replicas without a measured constraint.
- **Original Build gap:** No database mechanism gap. A project-specific
  SQLite/app measurement remains an integration checkpoint and may be kept
  even if PostgreSQL is not installed.

### LAB-OPT-04 — Local OpenTelemetry trace and signal comparison

- **Proposed Lab ID:** `LAB-OPT-04`.
- **Macro area:** `12` Modern Infrastructure; `14` Systems Thinking & Judgment.
- **Module placement:** M20 Observability & Reliability Engineering, after M16
  partial failure and M19 deployment/reproducibility basics.
- **Required vs Optional:** **Optional**. Structured local logs and timers remain the
  simpler Core path; this Lab is the bounded trace comparison.
- **Adopt vs Adapt:** **Adapt**.
- **Decision:** Adapt official documentation and maintained Python
  implementation examples without copying a vendor backend or requiring one.
- **Exact source/course/project:** OpenTelemetry *Observability primer*,
  <https://opentelemetry.io/docs/concepts/observability-primer/>; maintained
  Python implementation repository
  <https://github.com/open-telemetry/opentelemetry-python>, checked at head
  `251d01a9b65b9a9386c8483de5a8065d9abce4de`; source route may inspect the
  API `opentelemetry-api/src/opentelemetry/trace/span.py` and SDK
  `opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py`.
- **Exact exercise or bounded slice:** Instrument one local Python request
  path with a root span and one child operation; export to a local console or
  file-style exporter; inject one bounded local delay and one local error;
  compare structured log, timer, and trace evidence. Do not install a vendor
  dashboard, collector fleet, cloud exporter, auto-instrumentation survey, or
  production telemetry backend.
- **Mechanism revealed:** Logs, metrics, spans, and traces are evidence emitted
  by a system; a trace correlates work across boundaries but does not by
  itself prove root cause. Telemetry has overhead, missingness, cardinality,
  retention, and privacy constraints.
- **Learner outcome:** The learner selects a signal for a diagnostic question,
  follows one correlation path, identifies missing evidence, and judges the
  value and cost of instrumentation.
- **Mapped competencies:** Observe, Diagnose, Explain, Correctness, Judge,
  Estimate, Learn-New-Tech.
- **Prerequisites:** M04 measurement, M16 boundary/failure model, M19
  reproducible environment, and M20 logs/metrics vocabulary. The learner
  must know not to put secrets or private content in telemetry.
- **Cognitive load:** Medium. The activity has one request and one injected
  delay; exporter internals, sampling algorithms, and backend operations are
  excluded.
- **Linux/environment requirements:** Canonical Linux, pinned Python package
  versions in an isolated environment, a local Python service or script, and
  a local output sink. No network collector or account.
- **Setup burden:** Medium. Package/API churn and exporter selection require a
  pinned environment and a smoke test; structured logs/timers must remain the
  fallback if the trace path fails.
- **Approximate runtime class:** Execution is **seconds**; repeated local
  evidence collection is **minutes**.
- **Prediction step:** Predict which question logs, a metric, and a span can
  answer; identify the parent/child span relationship; predict what evidence
  disappears when export is disabled and what overhead the instrumentation may
  add.
- **Observation:** Record package versions, one request ID/trace ID, span
  boundaries, injected delay/error, log/timer counterpart, export success or
  loss, and a short note on causality limits.
- **Controlled break/failure:** Disable export, drop one local span, inject a
  bounded delay, create one high-cardinality mistake in a disposable fixture,
  and verify that secrets/private note text are not emitted. Do not send
  telemetry to a public backend.
- **Explanation/judgment:** Explain signal differences, distinguish
  correlation from causation, identify telemetry cost/privacy failure modes,
  and judge whether the Mini Cloud App needs a trace or only structured local
  evidence for the question at hand.
- **Cleanup/reset requirements:** Stop the local process; remove trace/log
  output and virtual environment if disposable; rotate no real credentials
  because none may be used; restore redaction and exporter defaults.
- **Safety boundary:** Local synthetic requests and local sinks only; no
  credential, personal data, public collector, or third-party endpoint.
- **Provenance:** OpenTelemetry documentation is maintained under CC BY 4.0;
  the OpenTelemetry Python repository is Apache-2.0. The documentation page
  was last modified 2026-04-23 and the repositories were checked 2026-08-30.
- **License status:** CC BY 4.0 documentation requires attribution, link,
  and change indication; Apache-2.0 source requires license/notice retention
  and changed-file notices for modified files.
- **Redistribution/adaptation status:** **Adaptation is license-cleared in
  principle** with attribution, Apache notices, version pins, and a review of
  transitive dependencies. No OpenTelemetry documentation page or source file
  should be copied into the course without those notices.
- **Maintenance/version risk:** High. The implementation repository is active,
  APIs and dependency versions move, and documentation/current practice can
  change. The conceptual signal distinction is stable; the package route is
  CURRENT and must be rechecked.
- **Mini Cloud App relationship:** P8 naturally uses the app's one request path
  and failure path after the learner has a diagnostic question. The app's
  minimal logs/timers should remain the baseline, not be replaced by a
  backend stack.
- **Original Build gap:** **Yes, conditional cross-layer gap.** If the app's
  own local path cannot demonstrate one correlated failure without adding an
  unneeded backend, build only a small course-owned fixture around the app;
  otherwise do not build another observability Lab.

## 4. Source Expedition map

Every expedition is a short, inspect-only route after the relevant principle
has been taught. The learner must follow the listed locations in order, write
one comparison with the mental model, and stop at the stated point. “Explore
the repository” is not an acceptable instruction.

### EXP-01 — xv6 utility-to-kernel path

- **Mature repo/source:** MIT PDOS `xv6-riscv`, `riscv` revision
  `35b088427ef37611c38afdeed5a52a278cae38f9`;
  <https://github.com/mit-pdos/xv6-riscv/tree/35b088427ef37611c38afdeed5a52a278cae38f9>.
  Course context: MIT 6.1810 Fall 2025 utility lab,
  <https://pdos.csail.mit.edu/6.1810/2025/labs/util.html>.
- **Stable principle already taught:** A process invokes an OS interface;
  user/kernel boundaries and file/process abstractions are mechanisms, not
  magic function calls.
- **Exact locations to inspect:**
  1. `user/ls.c` for one user-level file operation path;
  2. `user/usys.pl` for the generated syscall stubs;
  3. `kernel/sysfile.c` for the corresponding `open`/`read`/`fstat` implementations.
- **What implementation reality becomes visible:** A tiny user command is
  connected to generated entry code, syscall numbering/dispatch, process
  state, and kernel policy; the source organization is part of the interface
  story.
- **What the learner should ignore:** All other user programs, scheduler
  internals, traps/page tables, filesystem implementation, network driver,
  later labs, and every file not needed for the selected utility path.
- **Explicit stopping point:** Stop after drawing one source-to-kernel-to-result
  path and identifying one place where the implementation is more complicated
  than the learner's interface model. Do not open a second subsystem.
- **Cognitive load:** Medium-high; three locations and one utility only.
- **Maturity/maintenance status:** Mature teaching OS with active upstream
  changes and annual course branches; pin the revision and recheck the route
  before release.
- **License/provenance:** xv6 software MIT; Fall 2025 lab page CC BY 3.0 US;
  retain notices and do not copy course prose. Adaptation and bundling follow
  LAB-REQ-02's gate.
- **Module location:** M06 Processes, Syscalls & Execution Context.

### EXP-02 — PostgreSQL planner and buffer route

- **Mature repo/source:** PostgreSQL source repository, `master` revision
  `2fb8da5a245661287833b05a1b2e275ddf83bbd7`;
  <https://github.com/postgres/postgres/tree/2fb8da5a245661287833b05a1b2e275ddf83bbd7>.
  Pre-reading: official `EXPLAIN` documentation,
  <https://www.postgresql.org/docs/current/sql-explain.html>.
- **Stable principle already taught:** A query plan is an implementation
  choice based on estimates; storage and memory locality affect cost; a
  database interface hides mechanisms without eliminating their trade-offs.
- **Exact locations to inspect:**
  1. `src/backend/optimizer/plan/README`;
  2. `src/backend/optimizer/path/costsize.c`;
  3. `src/backend/storage/buffer/README`.
- **What implementation reality becomes visible:** Planner cost functions,
  path selection, and buffer management are separate mechanisms behind a
  single `EXPLAIN` result; the implementation is much larger than the one
  query-plan mental model.
- **What the learner should ignore:** Most executor code, every access method,
  planner GUC, statistics catalog detail, WAL/recovery internals, extension
  APIs, and performance tuning folklore.
- **Explicit stopping point:** Stop after locating where a path cost is
  estimated, where a plan is assembled, and where buffer management is
  described; write one paragraph connecting those locations to one captured
  local plan. Do not trace a query through the whole server.
- **Cognitive load:** High; C code and large-system navigation are optional
  depth after the PostgreSQL Lab or an equivalent plan exercise.
- **Maturity/maintenance status:** Mature, actively maintained database;
  source changes continuously and the route is implementation-specific.
- **License/provenance:** PostgreSQL License; preserve notices for any copied
  source, and prefer links plus a learner-authored map. Source tree and
  official docs checked 2026-08-30.
- **Module location:** M13 Databases: Storage & Indexing, with a short M14
  revisit for transaction/storage boundaries.

### EXP-03 — Chromium process and site-isolation path

- **Mature repo/source:** Chromium source and official design document;
  <https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md>.
  The document is current-practice evidence and should be rechecked at each
  release review rather than treated as a timeless specification.
- **Stable principle already taught:** Process isolation is a resource,
  failure, and security boundary; browser architecture is an integrated case,
  not a web-framework curriculum.
- **Exact locations to inspect:**
  1. `docs/process_model_and_site_isolation.md`, sections “Goals” and
     “Abstractions and Implementations”;
  2. `content/browser/site_instance_impl.cc`, the `SiteInstance` process
     decision implementation;
  3. `content/browser/security/cpsp/child_process_security_policy_impl.cc`,
     one browser-side access-control path.
- **What implementation reality becomes visible:** Chromium tracks security
  principals, process locks, browsing context groups, and browser-enforced
  restrictions; the production implementation uses more state and policy
  than the simple “one tab, one process” story.
- **What the learner should ignore:** Blink/rendering internals, JavaScript
  engine code, GPU process details, platform-specific Android branches,
  historical modes, extensions, WebUI, build tooling, and security exploit
  research.
- **Explicit stopping point:** Stop after identifying one document claim, one
  `SiteInstance` process-selection location, and one browser policy check; add
  one “mental model / implementation difference / why it matters” row. Do not
  follow callees or browse the source tree beyond the three locations.
- **Cognitive load:** High; large C++ repository and current implementation.
- **Maturity/maintenance status:** Mature, actively maintained, fast-changing
  production source. The document itself states platform and mode variation;
  all claims need a review date.
- **License/provenance:** Chromium source uses a BSD-style license with
  required notices; the documentation and source tree contain broader
  provenance that must be preserved if excerpts are reused. Link and
  paraphrase by default.
- **Module location:** M12 Web & Browser: The Integrated Case.

### EXP-04 — OpenTelemetry trace object path

- **Mature repo/source:** OpenTelemetry documentation and Python API/SDK;
  documentation head checked through repository commit
  `12862017e85a7b88fbd194241af00f4dbd4ee75c`; Python head
  `251d01a9b65b9a9386c8483de5a8065d9abce4de`.
  Sources: <https://opentelemetry.io/docs/concepts/observability-primer/>
  and <https://github.com/open-telemetry/opentelemetry-python>.
- **Stable principle already taught:** Observability is evidence design;
  spans correlate units of work but do not automatically establish causation.
- **Exact locations to inspect:**
  1. Documentation sections “Reliability and metrics” and “Understanding
     distributed tracing”;
  2. `opentelemetry-api/src/opentelemetry/trace/span.py`;
  3. `opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py`.
- **What implementation reality becomes visible:** The API-level span
  contract is separated from SDK behavior, context/attributes/status are
  represented explicitly, and the implementation has lifecycle/state details
  hidden by the simple trace diagram.
- **What the learner should ignore:** Exporter protocols, collector internals,
  vendor backends, sampling implementation, metrics/logs packages, generated
  code, and experimental directories.
- **Explicit stopping point:** Stop after mapping one documented span field to
  one API definition and one SDK lifecycle implementation; record one thing
  the source confirms and one thing the source makes more conditional. Do not
  follow imports or inspect more than the three locations.
- **Cognitive load:** Medium-high; Python source is readable but package
  layering and current API churn add load.
- **Maturity/maintenance status:** Active, maintained, current project with
  frequent dependency and documentation changes. Pin the revision for a Lab
  handout and recheck the route at review.
- **License/provenance:** OpenTelemetry documentation CC BY 4.0; Python
  implementation Apache-2.0; preserve attribution, license, NOTICE, and
  changed-file requirements if material is redistributed.
- **Module location:** M20 Observability & Reliability Engineering.

### EXP-05 — MIT 6.033 replication, transactions, and logging case

- **Mature repo/source:** MIT OpenCourseWare, *6.033 Computer System
  Engineering*, Spring 2018, lecture-note and project resources:
  <https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/lecture-notes/>.
- **Stable principle already taught:** Distributed state adds partial failure,
  coordination, atomicity, recovery, and availability trade-offs; preserving
  an invariant does not make a design free of cost or failure.
- **Exact locations to inspect:**
  1. Lecture 14, *Fault Tolerance: Reliability via Replication*:
     <https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf>;
  2. Lecture 15, *Fault Tolerance: Introduction to Transactions*:
     <https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/df1526408e3ec6f7e43aadfa1ce5f944_MIT6_033S18lec15.pdf>;
  3. Lecture 16, *Atomicity via Logging*:
     <https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/76fa216e8e5a4c4722c315a84b8e09a8c_MIT6_033S18lec16.pdf>.
- **What implementation reality becomes visible:** Replication, transaction
  coordination, and logging solve different failure problems and move
  complexity to coordinators, backups, logs, and recovery; a diagram can
  preserve an invariant while still exposing availability and operational
  costs.
- **What the learner should ignore:** All other lectures, Bitcoin/Tor, full
  design-project requirements, unrelated assignments, and any attempt to
  reproduce the original course assessment.
- **Explicit stopping point:** Stop after annotating one coordinator/
  primary/backup or logging diagram with state, message, failure, recovery,
  and invariant labels, then compare one simpler single-node alternative. Do
  not read the complete course packet.
- **Cognitive load:** High conceptual, low runtime; use only after M16/M17 and
  transaction/recovery principles are established.
- **Maturity/maintenance status:** Mature historical university course source,
  not a current implementation recommendation. The stable mechanisms remain
  useful; current system practice must be checked separately.
- **License/provenance:** MIT OCW terms provide CC BY-NC-SA 4.0 for OCW
  materials, with attribution, noncommercial, and ShareAlike conditions; the
  terms also warn that third-party rights may still apply. Link and
  paraphrase by default; do not put adapted OCW material under Essential CS's
  CC BY-SA license without a compatibility/legal review.
- **Module location:** M17 Replication, Consistency & Consensus; revisit M23
  Systems Thinking & Judgment and M24 Final System Defense.

## 5. Core coverage and restraint check

### 5.1 Selected mechanism coverage

| Mechanism / judgment | Primary selected activity | Coverage decision |
|---|---|---|
| Representation and edge-case correctness | LAB-OPT-01 Data Lab | Optional; no custom substitute if rights remain blocked |
| Process, syscall, user/kernel boundary | LAB-REQ-02 xv6 `sleep`; EXP-01 | Required real mechanism, narrowed to one path |
| Synchronization, ordering, progress | LAB-REQ-03 OSTEP rendezvous | Required link-only until rights are cleared |
| HTTP interface, origin, intermediary, cache | LAB-REQ-01; EXP-03 browser case | Required local protocol trace |
| TCP byte stream, sequence space, flow control | LAB-OPT-02 CS144 receiver | Optional because implementation load and rights risk are high |
| Query planning, indexing, transaction isolation | LAB-OPT-03 PostgreSQL | Optional comparison after SQLite; no PostgreSQL baseline promotion |
| Observability and evidence limits | LAB-OPT-04; EXP-04 | Optional trace path; logs/timers remain simpler baseline |
| Replication, coordination, logging, recovery judgment | EXP-05 | Source Expedition only; no full distributed implementation |
| Browser process/site isolation | EXP-03 | Source Expedition only; production C++ is too large for a Core Lab |

### 5.2 Intentional Lab count

Three Required Labs are enough to make the first traversal active across OS,
concurrency, and network/interface mechanisms without turning the curriculum
into full xv6, CS144, or CS:APP courses. Optional Labs are deliberately
branchable. Every Module not represented by a selected Lab still requires an
observation, project checkpoint, Source Expedition, or a documented reason
that a separate Lab would add little transfer.

### 5.3 Mini Cloud App boundary

The Mini Cloud App remains an integration surface, not a Lab replacement:

- P1/P3 can reuse LAB-REQ-01's boundary and failure questions.
- P5 can reuse LAB-REQ-03's invariant after the generic synchronization
  mechanism is understood.
- P4/P6 can use LAB-OPT-03's plan, durability, and recovery judgment without
  making PostgreSQL mandatory.
- P8 can use LAB-OPT-04's local evidence pattern without adding a telemetry
  backend by reflex.
- P9 remains a design/defense exercise; no queue, cache, replica, proxy,
  Kubernetes, or cloud deployment becomes mandatory through this map.

## 6. Candidates explicitly rejected or deferred

- **CS:APP Attack Lab:** reject from Core. It teaches real memory-corruption
  mechanics through exploit construction, but that is not necessary for the
  defense-first security boundary and adds safety, architecture, target, and
  rights burdens.
- **CS:APP Bomb Lab:** reject as a Core Lab. It is a strong debugger/source
  exercise, but its unique-binary, x86-64, handout-access, and maintenance
  assumptions are a poor Required dependency. A future machine Source
  Expedition may reconsider a safe offline phase only after rights review.
- **CS:APP Cache Lab, Malloc Lab, Proxy Lab, and full Data Lab:** do not make
  Required. Cache/malloc/proxy remain valuable optional or later dossier
  candidates; Data Lab is retained only as the narrow optional candidate
  above. No full CS:APP lab suite is selected.
- **Full xv6 lab sequence:** reject as Core. Use one utility/syscall path and
  one Source Expedition; full kernel work belongs in Deep Dive.
- **Full Stanford CS144 checkpoint sequence:** reject as Core. The selected
  receiver slice is optional; the rest would become a networking-stack course.
- **CS144 Checkpoint 4's public Internet measurement protocol:** reject in its
  original form for this project because it requires uncontrolled public paths,
  long data collection, and traffic to external systems. A local network
  namespace or explicitly authorized course-owned target is the only possible
  adapted path, and it remains optional.
- **Nand2Tetris full sequence and Project 1 as a Required Lab:** reject from
  this map's Required set. It is a strong construction tradition, but digital
  logic/HDL adds a separate build track before the shared machine model. Keep
  it as Deep Dive or a later source/learner-selected excursion; do not invent a
  replacement logic simulator.
- **Full MIT 6.5840 MapReduce/replication/consensus labs:** reject as Core.
  Partial failure, replication, consistency, and coordination are covered by
  bounded observations and EXP-05; full distributed implementation requires a
  graduate-course prerequisite chain.
- **Generic “bounded-buffer,” Redis, Kafka, Kubernetes, or cloud demos:** reject
  unless a later requirement identifies a concrete mechanism and a mature,
  rights-clear source. Product presence is not a learning requirement.
- **Course-owned vulnerable app as a current Required Lab:** defer. A safe
  authorization/privacy Build gap remains conditional on a security dossier
  that specifies original provenance/license, local binding, reset, synthetic
  data, and defense-first framing. No offensive task is selected here.
- **Uncontrolled public benchmark, public cache/proxy, public telemetry
  collector, or penetration target:** reject for reproducibility, privacy,
  safety, and causal-validity reasons.
- **Custom fake distributed simulator:** reject. The current map has local
  process, database, network, and source-case mechanisms that should be used
  first.

## 7. License, provenance, and maintenance gates

| Source family | Current conclusion | Release gate |
|---|---|---|
| IETF RFC 9110 | Normative source; link/paraphrase is preferred; extracted code has Revised BSD requirements | Review IETF Trust terms and notices before any excerpt, figure, or code is bundled |
| MIT xv6 / 6.1810 | xv6 software MIT; Fall 2025 lab page CC BY 3.0 US | Pin the exact lab tree and toolchain; retain notices; audit linked book/generated assets |
| OSTEP homework | Exact repository/file/commit verified; repository license not verified | Link-only. No source copy, adaptation, or bundle until license/permission is recorded |
| CS:APP labs | Exact public lab pages and Data Lab README verified; redistribution terms not established | Link-only until CMU/author permission or explicit license is obtained |
| Stanford CS144 | Exact Fall 2025 checkpoint PDFs verified; assignment/starter reuse rights not established | Link-only until rights are confirmed; no copied handout/code/tests |
| PostgreSQL | Project states PostgreSQL License for server/documentation | Preserve notices; pin PostgreSQL version and inspect transitive image/package licenses |
| OpenTelemetry docs/Python | Docs CC BY 4.0; Python repository Apache-2.0 | Preserve CC attribution/change notice and Apache LICENSE/NOTICE; pin dependencies |
| Chromium | Source license includes BSD-style notice conditions; current implementation is fast-changing | Link/paraphrase by default; preserve source notices for excerpts; recheck source paths and branch |
| MIT OCW 6.033 | OCW terms CC BY-NC-SA 4.0; possible third-party rights remain | Link/paraphrase by default; any adaptation must retain NC/SA terms and pass compatibility review |

No unresolved license issue authorizes bundling. If an unresolved source is
kept as a Required or Optional link-only activity, the learner-facing route
must state that the learner follows the authoritative source independently and
that Essential CS provides no copied handout, solution, test, or asset.

## 8. Completion report

### Counts

- **Required Labs:** 3 (`LAB-REQ-01` through `LAB-REQ-03`).
- **Optional Labs:** 4 (`LAB-OPT-01` through `LAB-OPT-04`).
- **Source Expeditions:** 5 (`EXP-01` through `EXP-05`).
- **Lab Adopt count:** 1 — OSTEP rendezvous, link-only.
- **Lab Adapt count:** 6 — HTTP/RFC local trace, xv6 utility slice, CS:APP
  Data Lab, CS144 receiver, PostgreSQL comparison, and OpenTelemetry trace.
- **Build selections:** 0 standalone mechanism Labs. Conditional project
  integration gaps remain explicitly listed.

### Unresolved license issues

- OSTEP `ostep-homework`: no repository license or explicit reuse terms were
  verified; Required use is link-only and bundling/adaptation is blocked.
- CS:APP3e labs: the public pages establish authorship, student handouts, and
  account-controlled distribution, but do not establish redistribution or
  adaptation rights; optional use is link-only until permission is obtained.
- Stanford CS144: the exact course/checkpoint material is public, but the
  checked pages do not establish redistribution/adaptation rights for
  assignment text, starter code, tests, or Minnow; optional use is link-only
  until rights are obtained.
- MIT OCW 6.033: CC BY-NC-SA 4.0 applies to OCW material, but third-party
  material and compatibility with Essential CS's intended CC BY-SA content
  still require review before adaptation.
- IETF RFC 9110: IETF Trust terms and Revised BSD requirements apply to
  extracted code; the selection uses paraphrase/linkage only.

### Unresolved environment/setup risks

- xv6 requires a pinned RISC-V cross-toolchain, QEMU, and a canonical Linux
  path; the annual lab tree and upstream source can diverge.
- CS:APP Data Lab has `bison`/`flex`, x86/Linux, handout-access, and binary
  portability risks.
- CS144 requires C++, CMake, sanitizers, a multi-checkpoint starter tree, and
  a pinned authorized source; it is optional for this reason.
- PostgreSQL adds a server/package/container and version surface; SQLite
  remains the Mini Cloud App baseline unless a measured requirement says
  otherwise.
- OpenTelemetry package/API/exporter churn requires pinned versions and a
  local fallback to structured logs/timers.
- Chromium and PostgreSQL Source Expeditions have high source-navigation load;
  exact stopping points are mandatory and source paths require rechecking.

### Remaining Build gaps

1. **Mini Cloud App integration boundary:** Classic labs teach the pieces, not
   the deliberate P0–P9 app evolution. P1/P3/P5/P8 can initially be app
   checkpoints; build a small original integration fixture only if the app
   cannot expose the selected mechanism without becoming a second curriculum.
2. **Safe authorization/privacy experiment:** No security Lab is selected in
   this map because the inspected candidates either use offensive framing or
   lack a sufficiently clear safe-target/reuse boundary. A course-owned,
   local, synthetic-data target remains conditional on a security dossier.
3. **Concurrency-to-application integration:** OSTEP teaches generic ordering;
   the app may still need a narrow race/transaction harness to connect that
   invariant to ownership and durable state. Do not build it until the project
   integration is designed and the generic Lab is accepted.
4. **Cross-layer observability integration:** OpenTelemetry is optional and
   structured local evidence is simpler. An original fixture is justified only
   if the Mini Cloud App cannot demonstrate one bounded timeout/latency/storage
   failure with local logs/timers and state inspection.

These are integration gaps, not permission to add Redis, Kubernetes, replicas,
public systems, offensive security tasks, or a fake distributed simulator.

### Files changed

- `meta/blueprint/lab-source-selection-map-v0.1.md`

### Research performed

- Compared freshly fetched `origin/main` with dispatch snapshot
  `271c44e18db98da0501bc3ab99046b1a98d7340d`; they matched exactly.
- Read `AGENTS.md`, curriculum invariants, lab/research/DoD/review policies,
  project status, decisions, open questions, competency/concept scaffolds,
  Issue #9, Issue #12, the detailed Stage/Module/Lesson map, dependency graph,
  Mini Cloud App evolution map, candidate inventory, and external audit.
- Live-checked the official MIT 6.1810 Fall 2025 utility lab, xv6 upstream
  repository/license/current revision, OSTEP homework index and exact
  `threads-sema` files/current revision, CS:APP lab/Data Lab pages, Stanford
  CS144 Fall 2025 Checkpoint 2 and Checkpoint 4, PostgreSQL current
  `EXPLAIN`/isolation docs/license/source tree, OpenTelemetry docs/Python
  repository/licenses/current revisions, Chromium process-model source
  documentation, RFC 9110 and IETF copyright terms, MIT OCW 6.033 resources
  and terms, and Nand2Tetris Project 1/software pages.
- Recorded current revisions where the authoritative API/repository made them
  available; branch names alone are not treated as immutable pins.

### Assumptions

- The Issue #1 Module IDs and dependency graph are proposals used for
  placement, not final canonical IDs.
- “Required” means required activity in the future Core path, not permission
  to bundle unresolved third-party source.
- A link-only activity can remain selected while its reuse rights are unresolved
  only when the learner follows the original authoritative source directly and
  Essential CS does not copy, adapt, or redistribute it.
- Runtime classes describe execution/setup burden classes, not a promise of
  learner completion time or a benchmark result.
- PostgreSQL, OpenTelemetry, Chromium, and current course branches are
  implementation/current-practice evidence and require release-time rechecks.

### Open questions

- Can the project accept OSTEP rendezvous as a Required link-only activity, or
  must a rights-cleared alternative be found before Required status?
- Can permission be obtained for a redistributable/adaptable CS:APP Data Lab
  and Stanford CS144 slice, or should both remain external learner-directed
  options?
- What exact canonical Linux image, QEMU, RISC-V toolchain, Python, SQLite,
  optional PostgreSQL, and optional OpenTelemetry versions will the later
  dossier pin?
- Will the Mini Cloud App naturally provide the P5 and P8 integration evidence,
  or are the conditional Build gaps necessary?
- Does the security dossier identify a rights-clear, local, defense-first
  target, or should security remain source/case analysis plus project review?

### Prompt deviations

- None. This artifact creates only the requested selection map and does not
  edit canonical curriculum maps, candidate inventory, status, decisions,
  competency matrix, or concept registry.

### Out-of-scope necessary fixes

- None.

### #9 Integrator focus

- Reconcile the three Required Labs with the final Module/Lesson dependency
  graph without assigning a Lab to every Module.
- Treat unresolved OSTEP/CS:APP/CS144 rights as hard bundling/adaptation
  gates, not as administrative footnotes.
- Confirm that xv6 setup is plausible in the canonical Linux environment and
  pin the exact lab tree/toolchain before promoting it to a runnable Core Lab.
- Keep PostgreSQL, OpenTelemetry, Chromium, CS144, and CS:APP as optional or
  source-routed cases unless a concrete learning requirement clears their
  complexity and maintenance cost.
- Map P1/P3/P5/P8 project checkpoints to selected mechanisms without making the
  Mini Cloud App the teaching vehicle.
- Require future Lab dossiers to add runnable smoke tests, exact reset steps,
  learner-facing exit criteria, and final license/attribution records.
- Do not mark this artifact `VERIFIED`; independent technical, pedagogical,
  lab-quality, and curriculum-integration review remains required.

## 9. Research source index

- [IETF RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [IETF Trust Legal Provisions](https://trustee.ietf.org/documents/trust-legal-provisions/)
- [MIT 6.1810 Fall 2025 xv6 Unix utilities lab](https://pdos.csail.mit.edu/6.1810/2025/labs/util.html)
- [MIT PDOS xv6-riscv at checked revision](https://github.com/mit-pdos/xv6-riscv/tree/35b088427ef37611c38afdeed5a52a278cae38f9)
- [OSTEP official homework index](https://pages.cs.wisc.edu/~remzi/OSTEP/Homework/homework.html)
- [OSTEP threads-sema README at checked revision](https://github.com/remzi-arpacidusseau/ostep-homework/blob/afb36ca8ddbf81d847d18f6bd18a87f0a18667f2/threads-sema/README.md)
- [OSTEP rendezvous source at checked revision](https://github.com/remzi-arpacidusseau/ostep-homework/blob/afb36ca8ddbf81d847d18f6bd18a87f0a18667f2/threads-sema/rendezvous.c)
- [CS:APP3e lab assignments](https://csapp.cs.cmu.edu/3e/labs.html)
- [CS:APP3e Data Lab README](https://csapp.cs.cmu.edu/3e/README-datalab)
- [Stanford CS144 Fall 2025](https://cs144.github.io/)
- [Stanford CS144 Checkpoint 2](https://cs144.github.io/assignments/check2.pdf)
- [Stanford CS144 Checkpoint 4](https://cs144.github.io/assignments/check4.pdf)
- [PostgreSQL current EXPLAIN documentation](https://www.postgresql.org/docs/current/sql-explain.html)
- [PostgreSQL current transaction isolation documentation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [PostgreSQL source at checked revision](https://github.com/postgres/postgres/tree/2fb8da5a245661287833b05a1b2e275ddf83bbd7)
- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry Python repository](https://github.com/open-telemetry/opentelemetry-python)
- [Chromium process model and site isolation](https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md)
- [Chromium source license](https://raw.githubusercontent.com/chromium/chromium/main/LICENSE)
- [MIT OCW 6.033 Computer System Engineering](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/)
- [MIT OCW 6.033 lecture notes](https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/lecture-notes/)
- [MIT OCW privacy and terms of use](https://ocw.mit.edu/pages/privacy-and-terms-of-use/)
- [Nand2Tetris Project 1: Boolean Logic](https://www.nand2tetris.org/project01)
- [Nand2Tetris software](https://www.nand2tetris.org/software)
