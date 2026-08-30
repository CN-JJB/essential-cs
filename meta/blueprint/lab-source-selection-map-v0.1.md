# Blueprint Lab and Source Expedition Selection Map v0.1

Status: **REWORK COMPLETE — READY FOR LEAD REVIEW**

Task: Issue #12, child of Issue #9
Date checked: 2026-08-30
Scope: Blueprint-level selection only. This document does not implement Labs,
copy third-party assignment material, or change the canonical curriculum maps.

## 1. Selection decision

This map selects **5 Required Labs**, **5 Optional Labs**, and **5 Source
Expeditions**. It intentionally does not assign one Lab to every Module. The
selection follows **Adopt → Adapt → Build**:

- Adopt one bounded, link-only OSTEP exercise as an optional external activity.
  It is not a Required Core dependency and its source remains at the
  authoritative location.
- Adapt six activities around exact sources while writing Essential CS-owned
  framing, prediction prompts, evidence requirements, safety boundaries, and
  stopping rules. Adaptation never means copying third-party prose, code,
  screenshots, tests, or grading infrastructure.
- Build three self-contained Required mechanism Labs where the researched
  course activities are either rights-blocked, course-sized, or do not provide
  the needed SQLite baseline: one POSIX-thread concurrency Lab and two SQLite
  database Labs. These are original activities using real canonical mechanisms,
  not toy simulations.

The first traversal should expose a small reusable set of mechanisms:
representation constraints, process/syscall boundaries, thread interleavings
and synchronization, HTTP interfaces/intermediaries, TCP byte-stream
semantics, real SQLite query/index trade-offs, transaction/isolation and
recovery boundaries, and evidence-oriented observability. Other Modules receive
short observations, project integration, or Source Expeditions rather than
another full Lab.

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

### 1.3 Required concurrency candidate investigation

The Required concurrency activity must be self-contained while exposing a race
created by real scheduling. A source link cannot be the learner's only required
instruction when Essential CS cannot redistribute or adapt the source.

| Candidate | Educational fit | Rights/setup result | Decision |
|---|---|---|---|
| OSTEP v1.10 *Threads / Semaphores* homework | The strongest direct match: small C programs expose interleavings, rendezvous, barriers, progress, and fairness questions. | The official `ostep-homework` repository has no declared license in the GitHub API; upstream issue #71 requests one. Public hosting is not reuse permission. | Keep as `LAB-OPT-05` link-only and as research inspiration; do not make it Required. |
| Allen Downey, *The Little Book of Semaphores* | Classic synchronization patterns and useful counter/rendezvous examples. | The book is CC BY-NC-SA 4.0. Its `Sync` simulator and examples are not a rights-compatible, canonical-Linux replacement for a real scheduling experiment in the Essential CS Core bundle. | Evidence and optional reading only; no adapted Required Lab. |
| Stanford Pintos Project 1: Threads | Real preemptible kernel threads, semaphores, locks, condition variables, scheduling, and explicit synchronization failures. | The official documentation includes a liberal MIT-style license, but the project is an x86 kernel/QEMU assignment with a large required context; the license also calls for file-level review of code derived from other projects. | Reject as Required. Its rights are better than OSTEP's, but its kernel/project load is disproportionate and not the canonical POSIX/Linux path. |
| MIT 6.1810 xv6 lock material | Real kernel locks and scheduling make synchronization visible. | xv6 software is MIT-licensed, but the RISC-V/QEMU toolchain and kernel context duplicate and enlarge the selected OS Lab. Course-material scope must be kept separate from source-code scope. | Do not add a second kernel Lab. Retain the narrow xv6 OS Lab and Source Expedition. |
| CS:APP Proxy Lab | Real threads, sockets, caching, and synchronization in a mature systems course. | Assignment/starter reuse rights were not established; networking, cache, and concurrency together create a course-sized load. | Reject as Required; retain only as a deferred candidate. |
| POSIX Issue 8 thread specifications plus Linux APIs | `pthread_mutex_lock` defines blocking ownership semantics; `pthread_cond_wait` defines atomic release/reacquire and predicate rechecking; scheduling policy, not the primitive, determines waiter order. | The specification is authoritative but copyrighted; the Lab will link and paraphrase it, while all Essential CS code, prompts, fixtures, and tests are original. Native Linux `gcc -pthread` is low-burden and canonical. | Use as the mechanism authority for a Build Lab. |

**Final decision:** Build `LAB-REQ-03` as an Essential CS original POSIX-thread
activity. It has two bounded real programs: (1) a shared-counter read/modify/
write race with a widened race window and a mutex repair, and (2) a two-party
condition-variable rendezvous with an explicit predicate and progress
invariant. A bounded watchdog variant may expose lock-order deadlock; the
learner must not treat repeated success as a fairness proof. `sched_yield()` or
a bounded delay may widen the race window, but the competing operations remain
real pthreads scheduled by Linux; no event-trace simulator controls the result.
The future implementation must smoke-test that the chosen workload produces a
real failing interleaving on the canonical image. A lock conflict may be
reported for the bounded deadlock/blocked variant, but it is not a substitute
for the required observed race; output must not be promised to be identical on
every host.

### 1.4 Required database candidate investigation

Database is a major Core area, so the first traversal needs independent,
reproducible real-database evidence. The Mini Cloud App cannot substitute for
this mechanism work.

| Candidate | Educational fit | Rights/setup/load result | Decision |
|---|---|---|---|
| CMU 15-445/645 BusTub assignments | The current assignment sequence explicitly separates SQL, storage, indexes, query planning, transactions, recovery, and concurrency control. | The sequence is a C++ database-engine implementation course with multiple projects; the checked assignment pages do not grant Essential CS redistribution/adaptation rights. | Use as sequence evidence; reject the full implementation as a Required Lab. |
| MIT 6.830 SimpleDB labs | Proven sequence from on-disk access and operators through transactions, query optimization, and rollback/recovery. | The OCW assignment page presents a multi-lab Java DB implementation and notes that some environments are not freely available; OCW material is CC BY-NC-SA 4.0 and assignment assets need item-level review. | Use as classic evidence; reject the full implementation and copied assignment route. |
| Berkeley CS186 RookieDB projects | Real B+ trees, query optimization, multigranularity locking, and ARIES-style recovery show the full mechanism chain. | The checked course/project sequence is a Java DB implementation track with multiple projects and private classroom repositories; it is too large for the shared traversal and is not a self-contained SQLite baseline. | Use as sequence evidence; reject the full implementation as a Required Lab. |
| PostgreSQL official `EXPLAIN` and transaction-isolation material | Strong server/MVCC comparison with plans, estimated versus actual rows, buffers, isolation anomalies, and retryable serialization failures. | PostgreSQL is reproducible locally but adds a server, roles, connections, version, and package/container burden. | Keep `LAB-OPT-03` as an Optional comparison after SQLite. |
| SQLite official CLI, query-planner, transaction, isolation, atomic-commit, WAL, and backup material | A real self-contained embedded engine exposes `SCAN` versus `SEARCH`, index trade-offs, committed-only visibility, one-writer behavior, rollback, journal/WAL boundaries, and backup snapshots without a server dependency. | SQLite's official copyright page dedicates its code and documentation to the public domain. There is no ready-made learner assignment to adopt, so the Essential CS wrapper and fixtures must be original; `EXPLAIN QUERY PLAN` output remains version-sensitive. | Build `LAB-REQ-04` and `LAB-REQ-05` around the official engine and docs. |

**Final decision:** Build two cohesive, self-contained SQLite Labs rather than
promoting PostgreSQL or compressing every database mechanism into the project:

- `LAB-REQ-04` owns query shape, scan versus index, plan inspection, workload
  and data-size assumptions, result equivalence, read/write/space trade-offs,
  and planner/measurement limits.
- `LAB-REQ-05` owns transaction boundaries, invariants, concurrent updates,
  observable conflict or anomaly, commit/rollback, SQLite isolation behavior,
  process-interruption recovery evidence, and the boundary between a backup and
  a durability claim.

Both use synthetic local data and the real SQLite engine. They do not require
PostgreSQL, Redis, Kafka, a cloud account, or a database engine implementation.

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
- **Learning goal:** Trace one real request through an interface and
  intermediary, then judge method, cache, authority, and failure semantics
  without treating HTTP as a framework API.
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
- **Smoke test:** A future implementation must start the local origin and
  adapter, complete one bounded request trace, and prove that reset removes the
  listener and temporary fixture without contacting a public endpoint.
- **Approximate runtime class:** Execution is **seconds to low minutes** for
  the trace and reset; no long-running measurement is required.
- **Prediction step:** Before running the commands, predict which party knows
  the request target, which headers survive forwarding, whether the
  intermediary can answer without contacting the origin, and whether a
  repeated GET differs in retry safety from a mutation.
- **Expected observation:** The learner can distinguish direct and forwarded
  connection paths, observe the origin/cache response difference, and identify
  at least one claim the trace cannot establish.
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
- **Exit criteria:** The learner submits direct and forwarded request evidence,
  one controlled origin/cache failure, a retry/cache judgment with stated
  limits, and a clean local reset showing that no listener or fixture remains.
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
- **Learning goal:** Trace one user operation across a real user/kernel API
  boundary and use the evidence to distinguish source calls, syscalls, guest
  time, and host/toolchain behavior.
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
- **Smoke test:** A future implementation must build the pinned tree, boot a
  clean guest, run the unmodified syscall route and the learner utility, and
  exit/reset without host privilege or network access.
- **Approximate runtime class:** Guest build and a short `sleep` run are
  **low minutes** after setup; cross-toolchain installation is the dominant
  setup cost, not execution time.
- **Prediction step:** Before opening the source route, predict which files
  must change, whether `sleep` can call the kernel implementation directly,
  what happens when the argument is absent, and why a guest tick is not the
  same thing as a host wall-clock measurement.
- **Expected observation:** The learner can show the user-to-kernel route,
  run the utility in QEMU, and classify missing-argument, compile, guest, and
  host-toolchain failures without claiming a host timing guarantee.
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
- **License status:** The xv6 software at the checked revision has its own MIT
  license, which requires the copyright and permission notices in copies or
  substantial portions. The exact MIT 6.1810 Fall 2025 `labs/util.html` page
  carries a `rel="license"` footer linking to CC BY 3.0 US:
  <https://creativecommons.org/licenses/by/3.0/us/>. This verifies the page's
  published lab material as marked by MIT PDOS, subject to attribution, a link
  to the license, and an indication of changes. It does not automatically
  license the separately linked xv6 book PDFs, lab repository, generated files,
  K&R text, or any third-party asset.
- **Redistribution/adaptation status:** **Adaptation is permitted for the
  marked lab-page material and the checked MIT-licensed xv6 software, subject
  to their separate notices and release review.** Essential CS keeps all
  learner instructions and evidence prompts independently authored and does not
  copy assignment prose. Pin the exact lab tree/source commit actually used;
  audit every bundled file rather than treating the page footer as a license
  for linked assets.
- **Maintenance/version risk:** High. The upstream xv6 `riscv` branch changes;
  the annual 6.1810 lab page and lab tree can change independently; QEMU and
  cross-toolchain compatibility matters. Pin the lab tree, source revision,
  toolchain, and QEMU in the implementation dossier.
- **Mini Cloud App relationship:** P1/P3 can later inspect the app server's
  native Linux process and syscall boundary. The app does not replace this
  guest-kernel mechanism lab.
- **Exit criteria:** The learner boots the pinned lab tree, produces the
  user-to-kernel source route and a working `sleep`, explains one compile or
  runtime failure boundary, and resets QEMU/build artifacts without affecting
  the host.
- **Original Build gap:** **No OS mechanism gap.** A small app process trace
  remains useful as integration, but a custom teaching kernel is not justified.

### LAB-REQ-03 — POSIX threads race, rendezvous, and progress boundaries

- **Proposed Lab ID:** `LAB-REQ-03`.
- **Macro area:** `10` Concurrency.
- **Module placement:** M15 Concurrency: Threads, Races & Synchronization;
  M14 database isolation is a motivating comparison, not a hidden prerequisite.
- **Required vs Optional:** **Required**.
- **Adopt vs Adapt:** **Build — Essential CS original**.
- **Decision:** Build a small self-contained activity after the classic-source
  search documented in §1.3. Use the POSIX mechanism and source-backed
  semantics, but do not copy an OSTEP, Pintos, or other assignment skeleton.
- **Exact source/course/project:** The Open Group Base Specifications Issue 8,
  IEEE Std 1003.1-2024, `pthread_mutex_lock` and `pthread_cond_wait`:
  <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html>
  and
  <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_wait.html>.
  OSTEP v1.10 *Threads / Semaphores* remains a provenance and optional
  external-exercise source at `LAB-OPT-05`; no OSTEP file is a dependency here.
- **Exact exercise or bounded slice:** Provide an Essential CS-owned C
  program with two bounded scenarios. First, two real pthread workers perform
  a deliberately non-atomic **compound** update using C11 atomic load and store
  operations on a shared counter (for example, relaxed `atomic_load` → bounded
  `sched_yield()`/short delay → `atomic_store(value + 1)`). Individual memory
  accesses therefore remain defined, while the read/modify/write as a whole can
  still lose an update under real scheduling. The learner observes that logical
  race, then protects the compound update with a mutex (and may compare a true
  atomic RMW such as `atomic_fetch_add` as a bounded extension). Second, the
  workers implement a two-party condition-variable rendezvous: the shared
  `ready` predicate and event record are protected by a mutex, and each worker
  waits in a `while` loop with `pthread_cond_wait` before recording `after`. A
  bounded child-process
  watchdog may be used for a deliberately reversed two-lock variant so a
  deadlock break cannot hang the learner's shell. No event-trace simulator,
  unbounded stress loop, or web framework is used.
- **Learning goal:** Make shared-state correctness and scheduling-dependent
  failure observable in real POSIX threads, then connect safety, progress,
  deadlock, and fairness claims to evidence and limits.
- **Mechanism revealed:** Shared state is updated by interleaved operations;
  individually atomic accesses do not make a multi-step state transition
  atomic; a mutex excludes conflicting critical sections; a condition variable
  is a wait/notification mechanism whose predicate remains the correctness
  rule; real scheduling can produce both a logical race and a correct-looking
  run. The Required evidence path deliberately avoids relying on a C/C++ data
  race (undefined behavior), so the observed lost update can be interpreted as
  an atomicity/interleaving failure. Lock
  ordering, progress, deadlock, and scheduler-dependent fairness are distinct
  claims.
- **Learner outcome:** The learner can draw an observed interleaving, state the
  counter and rendezvous invariants, reproduce a defined lost-update race on
  the canonical image, repair it with a suitable synchronization primitive,
  distinguish a logical race condition from a C/C++ data race/undefined
  behavior, and explain why one
  passing run is evidence rather than proof. The learner can also state what
  the bounded activity does not establish about starvation or fairness.
- **Mapped competencies:** Correctness, Trace, Diagnose, Explain, Judge.
- **Prerequisites:** M06 process/thread distinction; M03 shared-memory and
  call-level basics; M15 introductory interleaving and synchronization
  vocabulary; shell/Git reset habits; ability to compile a small C program.
  No database, broker, or distributed system is required.
- **Cognitive load:** Medium. The activity has one race invariant, one
  condition predicate, and one optional deadlock boundary. Memory-model
  formalism, lock-free algorithms, scheduler implementation, reader-writer
  policy, and starvation proofs are out of scope.
- **Linux/environment requirements:** Canonical Linux, `gcc` or a compatible C
  compiler, POSIX `pthread` support, shell, and a normal unprivileged account.
  No network or special kernel module is required.
- **Setup burden:** Low. The future Lab supplies the original source, a
  bounded runner/watchdog, a smoke test, and a resettable output directory.
- **Smoke test:** A future implementation must compile the original program,
  observe a failing interleaving within a bounded attempt budget on the
  canonical image, verify the repaired invariant, and terminate all local
  children during reset.
- **Approximate runtime class:** Each run is **sub-second to seconds**; the
  bounded repetition and observation record take **low minutes**. Repetition
  increases the chance of observing an interleaving but never proves its
  absence.
- **Prediction step:** Before running, enumerate a counter interleaving in
  which both threads read the same value and one write is lost; predict the
  final count range. Predict the rendezvous output and identify the predicate
  that must be rechecked after a condition wait. Predict what the reversed
  lock order can do and what the watchdog can and cannot establish.
- **Expected observation:** A bounded canonical-image run produces at least one
  real lost-update race, the mutex repair preserves the counter invariant, and
  the rendezvous enforces both `before` events before either `after` event.
- **Observation:** Record the source version, compiler/platform details,
  correct and broken outputs, a run that actually exhibits the defined
  lost-update race, the interleaving table, atomic-access and lock/condition
  wait locations, final invariant checks,
  and whether the deadlock watchdog fired. Label scheduler observations as
  observations, not universal guarantees.
- **Controlled break/failure:** Run the defined atomic-load/store compound
  update without the mutex, remove or move one predicate wait/notification,
  use `if` instead of a predicate loop as a bounded teaching
  break, or reverse lock acquisition in a disposable child. Cap repetitions,
  enforce a watchdog timeout, and terminate only the learner-owned child.
- **Explanation/judgment:** Explain logical race/atomicity failure versus a
  language-level data race, shared-state interleaving versus mutual exclusion,
  condition predicates versus notifications, evidence versus a
  proof of all schedules, and progress versus safety. Judge mutex/condition
  variable choices against a simpler join or sequential path. State that POSIX
  leaves waiter selection to scheduling policy and does not make this Lab a
  fairness or starvation proof.
- **Cleanup/reset requirements:** Join or terminate only learner-owned local
  threads/processes; remove binaries, logs, and watchdog output; restore the
  original Essential CS-owned starter; cap and clean all repetition wrappers after
  interruption. A reset recreates the same fixture from scratch.
- **Safety boundary:** Local POSIX threads and learner-owned processes only;
  no privileged synchronization, kernel exploit, external target, public
  service, or offensive security task.
- **Provenance:** The stable synchronization semantics are checked against
  POSIX Issue 8. OSTEP, Pintos, xv6, and classic synchronization texts inform
  the design and comparison but contribute no copied code, prose, tests, or
  grading infrastructure. All Lab instructions, fixture code, prompts, and
  tests are Essential CS-authored. The Required broken-counter path is designed
  to stay within defined C semantics rather than using undefined behavior as
  the teaching mechanism.
- **License status:** The Open Group/POSIX specification is copyrighted and
  will be linked and paraphrased only. The future Lab's original instructions,
  C code, fixtures, and tests are Essential CS-authored; code/tests follow the
  repository's Apache-2.0 policy while learner-facing instructional prose follows
  the educational-content license policy. No third-party source
  is bundled.
- **Redistribution/adaptation status:** **Self-contained and rights-clear for
  the original activity**, subject to the normal release review of Essential
  CS-authored files. The POSIX pages are evidence/specification links, not
  copied Lab material. OSTEP remains link-only and optional until its source
  license or permission is recorded.
- **Maintenance/version risk:** Medium. The POSIX primitives are stable, but
  compiler/glibc scheduling behavior, race reproduction rate, and watchdog
  timing vary by host. Pin the canonical Linux image and tune the smoke test
  against it; never promise identical output on every host.
- **Mini Cloud App relationship:** P5 may later integrate the same invariant
  into a project-specific transaction/request exercise. The project must not
  replace this independent mechanism Lab with a web-framework race demo.
- **Exit criteria:** The learner submits one real failing interleaving, the
  invariant and corrected result, a predicate-based rendezvous explanation,
  one controlled break record, a limits/fairness statement, and a clean reset
  transcript.
- **Original Build gap:** **No concurrency mechanism gap.** A small
  app-specific race/transaction harness remains a conditional P5 integration
  gap, not a replacement for this Lab.

### LAB-REQ-04 — SQLite query plans, indexing, and workload evidence

- **Proposed Lab ID:** `LAB-REQ-04`.
- **Macro area:** `09` Databases.
- **Module placement:** M13 Databases: Storage & Indexing; revisit in M23 for
  measurement and technology judgment.
- **Required vs Optional:** **Required**.
- **Adopt vs Adapt:** **Build — Essential CS original**.
- **Decision:** Build a small self-contained query/index activity after the
  classic database-course search in §1.4. It uses the official SQLite engine
  and documentation, but does not copy a CMU, MIT, or Berkeley assignment.
- **Exact source/course/project:** SQLite official documentation: `EXPLAIN
  QUERY PLAN`, <https://sqlite.org/eqp.html>; query planning,
  <https://sqlite.org/queryplanner.html>; command-line shell,
  <https://sqlite.org/cli.html>; and the SQLite copyright statement,
  <https://sqlite.org/copyright.html>.
- **Exact exercise or bounded slice:** Use an Essential CS-owned deterministic
  fixture with real rows at two bounded data sizes. Run one selective query
  and one less-selective variant before and after adding a single index (for
  example, an owner/time index). Capture the result set and plan, compare
  `SCAN` versus `SEARCH` where the planner chooses differently, and measure
  repeated read cost and database size/write cost. If a small or low-selectivity
  fixture makes a scan cheaper, record that outcome instead of forcing an
  index. Do not implement a B-tree or tune every planner setting.
- **Learning goal:** Connect a real SQL result to the engine's chosen access
  path and judge an index using workload, correctness, measurement, and space
  assumptions rather than product habit.
- **Mechanism revealed:** SQL states the desired result while the planner
  chooses an access path; a table scan and index search visit different data
  structures/pages; an index can reduce read work while adding storage and
  write maintenance; a plan is an implementation choice and not a proof of
  performance or causality.
- **Learner outcome:** The learner can trace one query to a plan and access
  path, predict when an index might help, verify that indexed and unindexed
  results are equivalent, measure a stated workload, and explain why a planner
  estimate or one timing does not settle the decision.
- **Mapped competencies:** Observe, Trace, Explain, Correctness, Diagnose,
  Estimate, Judge.
- **Prerequisites:** M02 data structures and complexity; M08/M09 files and
  storage; M04 measurement basics; M13 SQL/schema and query-plan vocabulary.
  No PostgreSQL, web framework, or database-engine implementation is required.
- **Cognitive load:** Medium. One table family, one query shape, one index, two
  bounded data sizes, and one correctness comparison are in scope. Joins,
  distributed planners, LSM engines, vector indexes, and optimizer folklore
  are out of scope.
- **Linux/environment requirements:** Canonical Linux, the pinned `sqlite3`
  CLI, Python standard library or shell for the fixture generator, and a
  writable temporary directory. Synthetic data only; no server or network.
- **Setup burden:** Low. The future Lab supplies SQL/scripts, the deterministic
  fixture generator, a smoke test that checks semantic plan categories rather
  than unstable output formatting, and a reset command.
- **Smoke test:** A future implementation must create the fixture, run the
  selected query before and after index creation, verify result equivalence,
  capture a parseable plan category, and reset all database side files.
- **Approximate runtime class:** Fixture creation and query runs are
  **seconds**; repeated measurements and analysis are **low minutes**. No
  production-scale benchmark is implied.
- **Prediction step:** Predict the result set, whether each query will use a
  scan or search, how selectivity and data size may change the plan, and which
  read/write/space costs the index introduces. Predict what remains unknown
  without controlled repetitions.
- **Expected observation:** The learner can compare a real full scan with an
  index search when the pinned planner chooses one, verify equal results, and
  explain a case where a scan remains reasonable or the plan does not change.
- **Observation:** Record SQLite version, schema and data generator, query and
  parameters, data-size/distribution assumptions, plan before and after,
  result equality, cold/warm state, warmup, repetitions, timing distribution,
  database size, write cost, and the limit of the inference. Treat
  `EXPLAIN QUERY PLAN` as interactive evidence because SQLite warns that its
  output format can change between releases.
- **Controlled break/failure:** Drop the index; change selectivity or data
  size; use a query expression that cannot use the chosen index; compare cold
  and warm runs; or omit warmup/repetitions as a deliberately invalid
  measurement. Verify that a plan change does not change the result. Do not
  fill a host filesystem or run uncontrolled load.
- **Explanation/judgment:** Explain planner choice, data locality, result
  equivalence, index write/space cost, measurement noise, and the difference
  between a plan, an observation, and a causal claim. Judge the index against a
  full scan, a query-shape change, or a schema change for the stated workload.
- **Cleanup/reset requirements:** Remove the database, journal/WAL side files,
  generated fixture, query output, and timing records; restore the no-index
  seed state; terminate no process other than learner-owned local commands. A
  reset must reproduce the same schema and data.
- **Safety boundary:** Local SQLite file, synthetic data, bounded queries, and
  learner-owned processes only. No public database, real personal data, or
  destructive operation outside the temporary directory.
- **Provenance:** SQLite's official query-planner and CLI documentation supply
  the mechanism descriptions and observable commands. The fixture, scripts,
  prompts, evidence template, and tests are Essential CS-authored. CMU
  15-445, MIT 6.830, and Berkeley CS186 supply sequence evidence only; no
  assignment prose or code is copied.
- **License status:** SQLite's official copyright page states that its code
  and documentation are dedicated to the public domain. The Lab should still
  link the documentation rather than copy substantial text or figures, and
  later audit any package/build-script material separately.
- **Redistribution/adaptation status:** **Self-contained and rights-clear for
  the original activity**, subject to release-time version and dependency
  review. No third-party assignment asset is bundled.
- **Maintenance/version risk:** Medium. SQLite behavior is stable, but planner
  choices, statistics, CLI output, and `EXPLAIN QUERY PLAN` formatting are
  version-sensitive. Pin the image/SQLite version and assert semantic evidence,
  not exact ASCII output.
- **Mini Cloud App relationship:** P4 may later reuse the app's item-list
  workload and result-equivalence evidence. The project remains an integration
  surface and does not replace this independent query/index Lab.
- **Exit criteria:** The learner submits a reproducible no-index/index plan
  comparison, equivalent-result check, workload and measurement record,
  read/write/space judgment, one invalidation/break observation, and a
  statement of planner and causal limits.
- **Original Build gap:** **No database query/index mechanism gap.** A P4 app
  measurement remains a conditional integration checkpoint, not a second
  query-planning Lab.

### LAB-REQ-05 — SQLite transactions, isolation, rollback, and recovery boundary

- **Proposed Lab ID:** `LAB-REQ-05`.
- **Macro area:** `09` Databases; supporting `06` Storage Systems and `10`
  Concurrency.
- **Module placement:** M14 Databases: Transactions, Recovery & Isolation;
  revisit M09 durability and M15 concurrency, and integrate with P5/P6 only
  after the mechanism is understood.
- **Required vs Optional:** **Required**.
- **Adopt vs Adapt:** **Build — Essential CS original**.
- **Decision:** Build a bounded real-database activity from official SQLite
  mechanisms after evaluating the course-sized SimpleDB/BusTub/RookieDB
  alternatives in §1.4. The activity is self-contained and does not outsource
  transaction or recovery teaching to a linked assignment.
- **Exact source/course/project:** SQLite official documentation: transaction
  control, <https://sqlite.org/lang_transaction.html>; isolation,
  <https://sqlite.org/isolation.html>; atomic commit and rollback,
  <https://sqlite.org/atomiccommit.html>; WAL,
  <https://sqlite.org/wal.html>; and the backup API,
  <https://sqlite.org/backup.html>.
- **Exact exercise or bounded slice:** Start with a two-account or inventory
  fixture whose invariant is explicit (for example, a transfer preserves the
  total balance). First compare an application-level read/modify/write split
  across two real SQLite connections with an atomic transaction/update. Then
  hold one bounded transaction open while a second connection observes
  committed-only visibility and the single-writer conflict or wait. Use the
  default rollback-journal mode as the baseline and one small WAL/snapshot
  comparison only if the pinned environment supports it. Inject a failure
  between multi-step writes and verify `ROLLBACK`; interrupt a learner-owned
  child process during an uncommitted transaction, reopen the database, and
  inspect what recovered. Create a local backup and restore it into a clean
  file. No power is cut, no host filesystem is filled, and no recovery engine
  is implemented.
- **Learning goal:** Connect transaction boundaries and database isolation to
  a real invariant, then distinguish rollback, process-crash recovery,
  backup, and physical-durability claims.
- **Mechanism revealed:** A transaction defines an atomic state transition;
  separate SQLite connections do not see uncommitted changes by default;
  SQLite serializes writers and reports bounded lock/snapshot conflicts;
  rollback journals and WAL arrange different commit/recovery paths; a backup
  is a consistent copy, not replication or proof against every physical
  failure.
- **Learner outcome:** The learner can state a transaction invariant, draw an
  interleaving or connection timeline, reproduce a lost update or lock/snapshot
  conflict, distinguish application synchronization from database guarantees,
  verify commit versus rollback, reason about when a busy/conflicted
  transaction must be rolled back and retried as a whole, and state exactly
  which interruption and SQLite configuration the recovery observation covers.
- **Mapped competencies:** Correctness, Trace, Observe, Diagnose, Explain,
  Judge, Estimate.
- **Prerequisites:** M08 files/I/O and M09 durability; M13 SQL/schema/query
  basics; M14 transaction and isolation vocabulary; M06 process basics for
  separate local connections. M15's generic thread Lab is a parallel companion,
  not a hidden hard prerequisite. No PostgreSQL or distributed system is
  required.
- **Cognitive load:** Medium-high but bounded: one invariant, two connections,
  one conflict/anomaly, one rollback, one process-interruption recovery check,
  and one backup/restore. MVCC internals, ARIES, distributed transactions,
  multi-region recovery, and managed backup systems are out of scope.
- **Linux/environment requirements:** Canonical Linux, pinned `sqlite3` and
  Python standard-library `sqlite3`, two learner-owned local processes or
  connections, and a writable temporary directory. Use synthetic data and a
  local rollback-journal baseline; no server, cloud, or network filesystem.
- **Setup burden:** Low-medium. The future Lab supplies schema/data scripts,
  a bounded two-connection coordinator, a child-process interruption harness,
  a backup/restore check, a smoke test, and cleanup instructions. It must not
  depend on a particular race outcome without accepting a documented lock
  conflict as valid evidence.
- **Smoke test:** A future implementation must create two local connections,
  observe committed-only visibility or a bounded writer conflict, verify a
  rollback and a clean restore after child interruption, and remove all side
  files during reset.
- **Approximate runtime class:** Each transaction scenario is **seconds**;
  reset, interruption, backup, and repeated observations take **low minutes**.
  No crash or recovery claim is made beyond the named local configuration.
- **Prediction step:** Predict which rows each connection can see before and
  after commit, whether the second writer waits or returns a bounded busy/error
  result, how an unguarded read/modify/write can lose an update, which transfer
  states survive `ROLLBACK`, and what the restored backup should contain.
- **Expected observation:** The learner observes no uncommitted cross-connection
  data by default, a bounded writer/reader conflict or snapshot effect, no
  partial committed transfer after rollback/interruption, and an equivalent
  restored backup for the declared snapshot.
- **Observation:** Record SQLite version, journal mode, synchronous setting,
  connection/process IDs, transaction boundaries, lock/busy results, visible
  snapshots, before/after rows, invariant checks, commit/rollback result,
  interruption point, journal/WAL files, backup/restore comparison, and
  whether the result is an observed process-crash behavior rather than proof of
  physical power-loss durability.
- **Controlled break/failure:** Remove the transaction around a multi-step
  update; interrupt after the first statement; force a bounded writer conflict;
  compare rollback-journal and WAL visibility; restore an old or deliberately
  missing backup; or close a connection without commit. Keep all failures in a
  disposable directory and use timeouts so no learner process can hang.
- **Explanation/judgment:** Explain transaction boundary, invariant,
  committed-only visibility, writer serialization or snapshot behavior,
  rollback, journal/WAL commit path, backup versus replication, and the limits
  of an interruption test. Explain why a retry after a busy or serialization
  conflict must respect transaction boundaries and effect idempotency. Judge
  SQLite's simple single-node model against a manual file copy and the optional
  PostgreSQL comparison; do not treat ACID as acronym memorization.
- **Cleanup/reset requirements:** Terminate only learner-owned child
  processes; remove the database, `-journal`, `-wal`, `-shm`, backup, and
  output files; restore the seed fixture and journal mode; verify no child or
  lock-holding process remains. A reset starts from a clean directory.
- **Safety boundary:** Disposable local SQLite files, synthetic balances/items,
  bounded transactions, and learner-owned processes only. No real accounts,
  public database, power-cut test, host-wide resource exhaustion, or cloud
  backup.
- **Provenance:** The official SQLite transaction, isolation, atomic-commit,
  WAL, and backup documentation provides mechanism authority. The schema,
  coordinator, fixture, prompts, evidence checks, and tests are Essential
  CS-authored. CMU 15-445, MIT 6.830, Berkeley CS186, and PostgreSQL provide
  sequence/comparison evidence only.
- **License status:** SQLite's official copyright page states that its code
  and documentation are dedicated to the public domain. The Lab uses the
  installed engine and paraphrases/link the documentation; any future bundled
  SQLite binary or build dependency still requires version/provenance review.
- **Redistribution/adaptation status:** **Self-contained and rights-clear for
  the original activity**, subject to the normal release review of original
  code and the pinned SQLite/package provenance. No course assignment text,
  code, tests, or recovery implementation is copied.
- **Maintenance/version risk:** Medium-high. Lock timing, rollback/WAL details,
  `synchronous` defaults, busy errors, and recovery artifacts depend on SQLite
  version, VFS, filesystem, and process timing. Pin the baseline and report
  implementation-specific results; recheck the official docs at release.
- **Mini Cloud App relationship:** P5/P6 may integrate the same ownership,
  atomic-write, backup, and restore evidence into the app. The project does not
  replace this database mechanism Lab and must not make PostgreSQL mandatory.
- **Exit criteria:** The learner submits an invariant and transaction timeline,
  one observed anomaly or bounded conflict, correct commit/rollback evidence,
  a process-interruption and backup/restore record with explicit limits, one
  controlled break, and a judgment separating SQLite guarantees from
  application code and physical-durability assumptions.
- **Original Build gap:** **No database transaction/recovery mechanism gap.**
  A P5/P6 app-specific integration remains conditional and cannot substitute
  for this Lab.

## 3. Optional Lab map

Optional Labs are not required for the first shared traversal. They are
selected because they expose useful mechanisms, but their setup, architecture,
maintenance, or rights burden makes them poor universal prerequisites.

### LAB-OPT-05 — OSTEP semaphore rendezvous, learner-directed external exercise

- **Proposed Lab ID:** `LAB-OPT-05`.
- **Macro area:** `10` Concurrency.
- **Module placement:** M15 Concurrency: Threads, Races & Synchronization.
- **Required vs Optional:** **Optional** external activity; it is not part of
  the self-contained Required Core path.
- **Adopt vs Adapt:** **Adopt — link-only**.
- **Decision:** Retain the strongest classic direct-fit activity as an
  independently obtained, learner-directed option. Essential CS supplies no
  copied instructions, source, tests, solution, or grading infrastructure.
- **Exact source/course/project:** OSTEP v1.10 *Threads / Semaphores* homework,
  official index: <https://pages.cs.wisc.edu/~remzi/OSTEP/Homework/homework.html>.
  Exact source repository commit checked: `afb36ca8ddbf81d847d18f6bd18a87f0a18667f2`.
  Bounded upstream files: `threads-sema/README.md`, `threads-sema/rendezvous.c`,
  and optionally `threads-sema/barrier.c` at that commit.
- **Exact exercise or bounded slice:** Follow only the upstream rendezvous
  exercise, where both `before` events precede both `after` events; a barrier
  may be an optional extension. Use the upstream source route and local Linux
  compiler, not an Essential CS bundle.
- **Mechanism revealed:** Semaphores express ordering and blocking; mutual
  exclusion alone does not establish a rendezvous or progress invariant; an
  incorrect run may depend on scheduling.
- **Learner outcome:** State an ordering invariant, predict an invalid
  interleaving, repair the external exercise, and distinguish an observed run
  from a proof. Fairness, starvation, and the full homework directory remain
  outside the bounded route.
- **Mapped competencies:** Correctness, Trace, Diagnose, Explain, Judge.
- **Prerequisites:** M06 process/thread distinction, M15 shared-state and
  semaphore vocabulary, POSIX thread compilation, and shell/Git reset habits.
- **Cognitive load:** Medium for the rendezvous slice; the source's wider
  reader-writer, barrier, and starvation set is optional depth.
- **Linux/environment requirements:** Canonical Linux, `gcc` or compatible C
  compiler, POSIX `pthread` support, and a normal user account. No network is
  needed after the learner obtains the source.
- **Setup burden:** Low for the bounded source directory, but acquisition and
  exact-file availability remain external to Essential CS.
- **Approximate runtime class:** **Sub-second to seconds** per run; repeated
  runs should expose scheduling variation without being treated as proof.
- **Prediction step:** Predict an invalid `after` ordering, semaphore wait/post
  locations, and why one semaphore does not automatically establish both
  directions of a rendezvous.
- **Observation:** Record the upstream revision, correct and incomplete
  outputs, a small interleaving table, and uncertainty when the broken version
  happens to look correct.
- **Controlled break/failure:** Remove one wait/post or add bounded local
  delays. Never create an unbounded thread storm or use a remote target.
- **Explanation/judgment:** Compare ordering with mutual exclusion, evidence
  with proof, and the semaphore activity with the Required POSIX Lab and a
  simpler join where appropriate.
- **Cleanup/reset requirements:** Remove local binaries/output and restore the
  upstream checkout before another attempt; cap and clean any repetition
  wrapper.
- **Safety boundary:** Learner-owned local processes and threads only; no
  privileged synchronization, external target, or offensive security task.
- **Provenance:** OSTEP authors' official homework index and the pinned
  `ostep-homework` files. This entry preserves provenance and an external route,
  not Essential CS adaptation.
- **License status:** The GitHub API reports no repository license, and upstream
  issue #71 requests one. Educational availability and public hosting do not
  establish redistribution or adaptation rights.
- **Redistribution/adaptation status:** **Link-only; bundling, copying, and
  adapting are blocked.** The learner obtains and follows the authoritative
  source independently. The self-contained Required concurrency activity is
  `LAB-REQ-03`, not this entry.
- **Maintenance/version risk:** Medium-high. Recheck the commit, file list,
  compiler behavior, and rights before recommending it; no upstream change is
  silently bundled into Essential CS.
- **Mini Cloud App relationship:** P5 may compare the generic rendezvous
  invariant with the project's ownership-aware transaction exercise, but the
  project and this external option do not replace `LAB-REQ-03`.
- **Exit criteria:** Optional work is complete when the learner records the
  source revision, one predicted/observed interleaving, one controlled break,
  and a statement of what the external activity does not prove.
- **Original Build gap:** No; `LAB-REQ-03` supplies the self-contained
  mechanism path. A project-specific P5 integration remains conditional.

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
- **Decision:** Adapt official documentation into a small local comparison
  after `LAB-REQ-04` and `LAB-REQ-05`; PostgreSQL is not the Required baseline.
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
  plans, M14 transaction vocabulary, the measurement methodology above, and
  the Required SQLite Labs as the baseline comparison. PostgreSQL setup is not
  a prerequisite for the Core path.
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
- **License/provenance:** The checked xv6 software is MIT-licensed. The exact
  Fall 2025 `labs/util.html` page carries a `rel="license"` footer to CC BY
  3.0 US, covering the page material as marked; retain attribution, the license
  link, and change indication. This does not cover the linked book, lab tree,
  generated files, or third-party material. Retain notices and do not copy
  course prose; any adaptation follows LAB-REQ-02's separate-scope gate.
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
  depth after `LAB-REQ-04` or an equivalent plan exercise. PostgreSQL itself
  is not a prerequisite.
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
| Thread shared state, race, ordering, synchronization, progress | LAB-REQ-03 POSIX threads activity; LAB-OPT-05 OSTEP rendezvous | Required self-contained real-thread mechanism; OSTEP remains optional link-only evidence |
| HTTP interface, origin, intermediary, cache | LAB-REQ-01; EXP-03 browser case | Required local protocol trace |
| TCP byte stream, sequence space, flow control | LAB-OPT-02 CS144 receiver | Optional because implementation load and rights risk are high |
| Query planning, scan/index choice, workload, result equivalence | LAB-REQ-04 SQLite query/index activity; EXP-02 | Required real database mechanism; planner output and measurement limits explicit |
| Transactions, isolation, concurrent update, rollback, recovery boundary | LAB-REQ-05 SQLite transaction/recovery activity; LAB-OPT-03 PostgreSQL comparison | Required SQLite baseline; PostgreSQL remains optional server/MVCC comparison |
| Durability, commit, interruption, backup/restore | LAB-REQ-05; EXP-05 recovery judgment | Required local recovery evidence; no claim that a process test proves every power-loss behavior |
| Observability and evidence limits | LAB-OPT-04; EXP-04 | Optional trace path; logs/timers remain simpler baseline |
| Replication, coordination, logging, recovery judgment | EXP-05 | Source Expedition only; no full distributed implementation |
| Browser process/site isolation | EXP-03 | Source Expedition only; production C++ is too large for a Core Lab |

### 5.2 Intentional Lab count

Five Required Labs make the first traversal active across OS, concurrency,
network/interface, and the two distinct database mechanism boundaries without
turning the curriculum into full xv6, CS144, CS:APP, or database-engine
courses. Two database Labs are deliberate rather than one Lab per Module:
query/index measurement and transaction/isolation/recovery require different
evidence, failure controls, and correctness claims. Optional Labs are
branchable. Every Module not represented by a selected Lab still requires an
observation, project checkpoint, Source Expedition, or a documented reason
that a separate Lab would add little transfer.

### 5.3 Mini Cloud App boundary

The Mini Cloud App remains an integration surface, not a Lab replacement:

- P1/P3 can reuse LAB-REQ-01's boundary and failure questions.
- P5 can reuse LAB-REQ-03's invariant after the independent thread mechanism is
  understood, and LAB-REQ-05 can supply the database-side transaction and
  isolation evidence.
- P4 can use LAB-REQ-04's query/index result and workload evidence; P5/P6 can
  use LAB-REQ-05's transaction, rollback, and recovery evidence. LAB-OPT-03 is
  a PostgreSQL comparison only and does not make PostgreSQL mandatory.
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
- **OSTEP rendezvous as a Required Lab:** do not make a link-only external
  assignment a Core dependency while its repository license is unresolved.
  Retain the exact activity as optional `LAB-OPT-05` and use the original
  POSIX-thread `LAB-REQ-03` for self-contained Core teaching.
- **Pintos Project 1 as a Required concurrency Lab:** do not import its x86
  kernel, scheduler, or multi-part project merely because its documentation is
  permissively licensed. Its synchronization evidence informed the search, but
  the setup and project scope exceed the needed POSIX mechanism slice.
- **MIT 6.830 SimpleDB, CMU 15-445/645 BusTub, and Berkeley CS186 RookieDB
  implementation sequences:** reject as Required Labs. They are valuable
  database-engine traditions covering storage, indexes, query execution,
  transactions, concurrency, and recovery, but their multi-project Java/C++
  implementation load and assignment-specific rights do not provide a small
  self-contained SQLite baseline. Use their sequence evidence to inform
  `LAB-REQ-04` and `LAB-REQ-05`, not copied tasks or code.
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
| MIT xv6 / 6.1810 | Checked xv6 software is MIT-licensed. The exact Fall 2025 `labs/util.html` page has a `rel="license"` footer to CC BY 3.0 US; this scope is the page material as marked, not its linked book/repository/generated assets | Keep MIT and CC BY notices separate; attribute, link the license, indicate changes, pin the lab tree/toolchain, and audit every linked/bundled asset |
| OSTEP homework | Exact repository/file/commit verified; repository license not verified | Link-only. No source copy, adaptation, or bundle until license/permission is recorded |
| CS:APP labs | Exact public lab pages and Data Lab README verified; redistribution terms not established | Link-only until CMU/author permission or explicit license is obtained |
| Stanford CS144 | Exact Fall 2025 checkpoint PDFs verified; assignment/starter reuse rights not established | Link-only until rights are confirmed; no copied handout/code/tests |
| POSIX Issue 8 | Authoritative thread semantics; specification text is copyrighted and the custom Lab uses links/paraphrase only | Keep the POSIX pages as evidence; bundle only Essential CS-authored code/prompts under the repository code policy |
| SQLite | Official SQLite page states that its code and documentation are dedicated to the public domain; planner output and runtime behavior remain version-sensitive | Pin SQLite/CLI and image versions; assert semantic plan categories, preserve source provenance, and audit package/build-script dependencies |
| PostgreSQL | Project states PostgreSQL License for server/documentation | Preserve notices; pin PostgreSQL version and inspect transitive image/package licenses |
| OpenTelemetry docs/Python | Docs CC BY 4.0; Python repository Apache-2.0 | Preserve CC attribution/change notice and Apache LICENSE/NOTICE; pin dependencies |
| Chromium | Source license includes BSD-style notice conditions; current implementation is fast-changing | Link/paraphrase by default; preserve source notices for excerpts; recheck source paths and branch |
| MIT OCW 6.033 | OCW terms CC BY-NC-SA 4.0; possible third-party rights remain | Link/paraphrase by default; any adaptation must retain NC/SA terms and pass compatibility review |

No unresolved license issue authorizes bundling. If an unresolved source is
kept as an Optional link-only activity, the learner-facing route must state
that the learner follows the authoritative source independently and that
Essential CS provides no copied handout, solution, test, or asset. No Required
Lab in this map depends on an unresolved third-party assignment bundle.

## 8. Completion report

### Status

**REWORK COMPLETE — READY FOR LEAD REVIEW**

### Counts

- **Required Labs:** 5 (`LAB-REQ-01` through `LAB-REQ-05`).
- **Optional Labs:** 5 (`LAB-OPT-01` through `LAB-OPT-05`).
- **Source Expeditions:** 5 (`EXP-01` through `EXP-05`).
- **Lab Adopt count:** 1 — OSTEP rendezvous, link-only.
- **Lab Adapt count:** 6 — HTTP/RFC local trace, xv6 utility slice, CS:APP
  Data Lab, CS144 receiver, PostgreSQL comparison, and OpenTelemetry trace.
- **Build selections:** 3 standalone mechanism Labs — POSIX-thread
  concurrency, SQLite query/index, and SQLite transaction/recovery. Conditional
  project integration gaps remain explicitly listed.

### Blocking findings resolved

#### 1. Required concurrency self-containment

- **Previous state:** `LAB-REQ-03` was an OSTEP semaphore rendezvous marked
  Required, while the `ostep-homework` repository license was unverified and
  Essential CS could neither bundle nor adapt the linked source.
- **Research performed:** Compared OSTEP's real C semaphore exercises with the
  POSIX Issue 8 mutex/condition-variable specifications, Stanford Pintos
  Project 1, Allen Downey's *Little Book of Semaphores*, MIT xv6 lock material,
  and the CS:APP Proxy Lab. The comparison covered real scheduling, shared
  state, ordering/race evidence, progress/deadlock/fairness boundaries, setup
  burden, and course-material rights. OSTEP remains the strongest direct-fit
  source, but GitHub reports no repository license and upstream issue #71 asks
  for one. Pintos is permissively licensed but is an x86 kernel project; the
  Little Book is CC BY-NC-SA 4.0 and its simulator is not the canonical real
  scheduling mechanism; xv6 overlaps the OS Lab; Proxy Lab is rights-uncertain
  and combines too many mechanisms.
- **Final selection:** `LAB-REQ-03` is now **Build — Essential CS original**:
  a small native Linux POSIX-thread activity with a real shared-counter race,
  mutex repair, condition-variable rendezvous, and a bounded deadlock/watchdog
  boundary. The race window may use `sched_yield()` or a bounded delay, but
  Linux scheduling produces the observed interleaving; no simulator dictates
  it. OSTEP is retained as optional `LAB-OPT-05` link-only evidence.
- **Adopt / Adapt / Build rationale:** Adopt OSTEP only as an optional
  external activity; use POSIX as the stable specification and mechanism
  authority; Build the self-contained Required activity because no researched
  classic candidate satisfies rights, canonical Linux, cognitive-load, and
  self-containment requirements together. This is not a shallow replacement:
  it preserves the real mechanism and requires a canonical-image smoke test
  that produces an actual failing interleaving.
- **License/self-containment result:** The Required Lab contains only
  Essential CS-authored instructions, C code, fixtures, prompts, tests, and
  reset tooling, under the repository's original-code policy. POSIX pages are
  linked/paraphrased, not copied. No unresolved third-party assignment is a
  learner-facing Required dependency.

#### 2. Required Database mechanism coverage

- **Selected Required Labs:** `LAB-REQ-04` covers SQLite query shape, scan
  versus index, plan inspection, workload/data-size assumptions, result
  equivalence, read/write/space trade-offs, and planner/measurement limits.
  `LAB-REQ-05` covers transaction boundaries, invariants, concurrent updates,
  committed-only visibility, writer conflicts or snapshot behavior,
  commit/rollback, process-interruption recovery evidence, and backup/restore
  boundaries.
- **SQLite role:** SQLite is the canonical Required baseline because the real
  embedded engine is self-contained, local, reproducible, and sufficient to
  expose storage/index, transaction, isolation, and journal/WAL mechanisms
  without a server prerequisite. The Labs use synthetic data, separate local
  connections/processes, bounded failures, and explicit evidence artifacts.
- **PostgreSQL role:** `LAB-OPT-03` remains an Optional comparison after both
  SQLite Labs. Its server process, MVCC/isolation behavior, `EXPLAIN`, buffers,
  and serialization-failure/retry behavior add educational value only when a
  stated comparison constraint justifies the setup. PostgreSQL is not required
  by the Core path or by the Mini Cloud App.
- **Why this is sufficient for Core:** The two Required activities keep the
  query/index and transaction/recovery claims separate enough to measure and
  explain accurately, while together giving the first shared traversal real
  database observation rather than project-only exposure. The project may
  revisit these mechanisms at P4-P6 but cannot substitute for them. Full
  BusTub/SimpleDB/RookieDB implementation, PostgreSQL clusters, distributed
  transactions, and specialized index families remain Optional/Deep Dive.

#### 3. xv6 licensing

- **Evidence found:** The exact MIT PDOS Fall 2025 page used by `LAB-REQ-02`,
  <https://pdos.csail.mit.edu/6.1810/2025/labs/util.html>, contains a footer
  with `rel="license"` linking to CC BY 3.0 US,
  <https://creativecommons.org/licenses/by/3.0/us/>. The CC deed permits
  sharing and adaptation with appropriate credit, a license link, and change
  indication.
- **Scope:** This verifies the page's own published lab material as marked by
  MIT PDOS. It does not extend automatically to the separately linked xv6
  book PDFs, `xv6-labs-2025` repository, generated files, K&R text, or other
  third-party assets.
- **Resulting reuse policy:** The checked xv6 software source is separately
  covered by its MIT `LICENSE`, so software copies retain the MIT copyright
  and permission notice. Essential CS instructions remain independently
  authored and assignment prose is not copied. Any bundled lab-page material
  carries CC BY attribution, license link, and change indication; every linked
  or generated asset receives its own file-level audit before release.

### Unresolved license issues

- OSTEP `ostep-homework`: no repository license or explicit reuse terms were
  verified; optional use is link-only and bundling/adaptation is blocked.
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
- POSIX Issue 8: the specification text is copyrighted; the Required
  concurrency Lab uses only links/paraphrase and original Essential CS code.
- xv6: the exact `labs/util.html` page is marked CC BY 3.0 US and the checked
  xv6 software is MIT-licensed, but linked books, lab repositories, generated
  files, and third-party assets remain separate file-level checks.

### Unresolved environment/setup risks

- xv6 requires a pinned RISC-V cross-toolchain, QEMU, and a canonical Linux
  path; the annual lab tree and upstream source can diverge.
- The Required POSIX concurrency Lab needs a canonical-image smoke test for a
  real failing interleaving; scheduler timing varies, so the Lab must not
  promise identical output on every host.
- CS:APP Data Lab has `bison`/`flex`, x86/Linux, handout-access, and binary
  portability risks.
- CS144 requires C++, CMake, sanitizers, a multi-checkpoint starter tree, and
  a pinned authorized source; it is optional for this reason.
- SQLite query-plan formatting, planner choices, journal/WAL behavior, busy
  errors, and recovery artifacts vary with SQLite version, VFS, filesystem,
  configuration, and timing. Pin the baseline and test semantic evidence.
- PostgreSQL adds a server/package/container and version surface; it remains an
  Optional comparison and SQLite is the Required/Mini Cloud App baseline.
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
3. **Concurrency-to-application integration:** `LAB-REQ-03` and `LAB-REQ-05`
    teach generic thread/database mechanisms; the app may still need a narrow
    race/transaction harness to connect those invariants to ownership and
    durable state. Do not build it until the project integration is designed,
    and do not use it to replace either Required Lab.
4. **Cross-layer observability integration:** OpenTelemetry is optional and
   structured local evidence is simpler. An original fixture is justified only
   if the Mini Cloud App cannot demonstrate one bounded timeout/latency/storage
   failure with local logs/timers and state inspection.

These are integration gaps, not permission to add Redis, Kubernetes, replicas,
public systems, offensive security tasks, or a fake distributed simulator.

### Deliverables

- Reworked the Required/Optional selection decision and counts.
- Added the classic-source investigation and final Build decision for a
  self-contained POSIX-thread concurrency Lab; retained OSTEP as optional
  link-only evidence.
- Added Required SQLite query/index and transaction/isolation/recovery Labs;
  kept PostgreSQL as an Optional comparison.
- Added explicit learning goals, expected observations, smoke-test boundaries,
  and exit criteria to the Required Lab set.
- Updated the Core coverage table, Mini Cloud App boundary, rejected/deferred
  candidates, Build gaps, license/provenance gates, assumptions, open
  questions, source index, and #9 review focus.

### Files changed

- `meta/blueprint/lab-source-selection-map-v0.1.md`

### Verification performed

- Fetched `origin` and cleanly rebased onto `origin/main` at
  `a13d6cebb84621742c4a0a14941a24a7a2b7c86f`.
- `git diff --check` passed.
- `git diff --name-status origin/main...HEAD` and the worktree status confirm
  that the only tracked task change is the permitted blueprint file; unrelated
  pre-existing untracked workspace artifacts were not modified.
- Counted the actual headings: 5 Required Labs, 5 Optional Labs, and 5 Source
  Expeditions, matching the stated counts; all ten Lab IDs and five Expedition
  IDs are unique.
- Reviewed every Required Lab for the policy fields: learning goal,
  prerequisites, exact source/slice, environment/setup, prediction, expected
  observation, steps/scope, controlled break, cleanup/reset, safety,
  provenance/license, maintenance, Mini Cloud App relationship, smoke test,
  and exit criteria.
- Counted five explicit Source Expedition stopping points and scanned for stale
  three-Required, Required-OSTEP, mandatory-PostgreSQL, and unresolved-rights
  claims. Historical previous-state wording appears only in the Completion
  Report; the current selection is explicit.
- Confirmed the Core coverage table names Required SQLite query/index and
  transaction/isolation/recovery work, while PostgreSQL remains Optional and
  project checkpoints remain integration rather than replacement Labs.
- No runnable Lab code was implemented or tested; implementation smoke tests
  remain future Lab-dossier work.

### Research performed

- Fetched `origin`, inspected Issue #12, PR #16, and the Web Lead review, and
  rebased this branch cleanly onto current `origin/main`
  `a13d6cebb84621742c4a0a14941a24a7a2b7c86f`.
- Read `AGENTS.md`, curriculum invariants, lab/research/DoD/review policies,
  project status, decisions, open questions, competency/concept scaffolds,
  Issue #9, Issue #12, the detailed Stage/Module/Lesson map, dependency graph,
  Mini Cloud App evolution map, candidate inventory, and external audit.
- Rechecked concurrency alternatives: OSTEP's exact repository/file/commit
  and open license issue, POSIX Issue 8 mutex/condition-variable semantics,
  Stanford Pintos Project 1 and its license, *The Little Book of Semaphores*
  license/simulator scope, MIT xv6 lock context, and CS:APP Proxy Lab scope.
- Rechecked database alternatives and authority: CMU 15-445/645 Fall 2026
  assignment sequence, MIT 6.830 SimpleDB assignments, Berkeley CS186
  RookieDB sequence, SQLite official CLI/query-planner/transaction/isolation/
  atomic-commit/WAL/backup/copyright pages, and PostgreSQL 18 `EXPLAIN`,
  transaction-isolation, and license pages.
- Live-checked the MIT 6.1810 Fall 2025 utility page's exact HTML footer and
  its CC BY 3.0 US deed, the MIT-licensed xv6 source at the checked revision,
  OSTEP homework index and exact `threads-sema` files/current revision,
  CS:APP lab/Data Lab pages, Stanford CS144 Fall 2025 Checkpoint 2 and
  Checkpoint 4, OpenTelemetry docs/Python repository/licenses/current
  revisions, Chromium process-model documentation, RFC 9110 and IETF terms,
  MIT OCW 6.033 resources and terms, and Nand2Tetris Project 1/software pages.
- Recorded current revisions where the authoritative API/repository made them
  available; branch names alone are not treated as immutable pins.

### Assumptions

- The Issue #1 Module IDs and dependency graph are proposals used for
  placement, not final canonical IDs.
- “Required” means required activity in the future Core path, not permission
  to bundle unresolved third-party source.
- A link-only activity can remain selected while its reuse rights are unresolved
  only as an Optional external activity; the learner follows the original
  authoritative source directly and Essential CS does not copy, adapt, or
  redistribute it.
- The three Build selections are Blueprint-level designs only. Their future
  code, fixtures, smoke tests, and learner instructions must be authored and
  released as Essential CS content; this task does not implement them.
- The exact MIT 6.1810 `labs/util.html` footer is treated as evidence for the
  page material it marks, not as a blanket license for linked or generated
  assets.
- Runtime classes describe execution/setup burden classes, not a promise of
  learner completion time or a benchmark result.
- SQLite, PostgreSQL, OpenTelemetry, Chromium, and current course branches are
  implementation/current-practice evidence and require release-time rechecks.

### Open questions

- What canonical Linux image, compiler/glibc versions, race-window parameters,
  and smoke-test threshold will make the original POSIX concurrency Lab
  reliably expose a real failing interleaving without promising a universal
  scheduler outcome?
- Can permission be obtained for a redistributable/adaptable CS:APP Data Lab
  and Stanford CS144 slice, or should both remain external learner-directed
  options?
- What exact canonical Linux image, QEMU, RISC-V toolchain, Python, SQLite,
  optional PostgreSQL, and optional OpenTelemetry versions will the later
  dossier pin?
- Which SQLite journal mode and `synchronous` setting define the Required
  transaction/recovery baseline, and which WAL comparison is worth its added
  state and maintenance cost?
- Does the exact MIT 6.1810 page-scope evidence remain sufficient for every
  future bundled lab-page excerpt, or should linked books/lab repositories stay
  external until separately audited?
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

- Reconcile the five Required Labs with the final Module/Lesson dependency
  graph without assigning a Lab to every Module; verify that the two Database
  Labs are justified by distinct mechanism/evidence boundaries.
- Review `LAB-REQ-03` as a genuinely self-contained POSIX-thread Build: its
  smoke test must produce a real failing interleaving on the canonical image,
  while its claims remain bounded for evidence, deadlock, and fairness.
- Treat OSTEP as optional link-only until its license is recorded; treat
  unresolved CS:APP/CS144 rights as hard bundling/adaptation gates, not as
  administrative footnotes.
- Confirm xv6 setup is plausible in the canonical Linux environment and audit
  the exact CC BY page scope separately from the MIT xv6 software, linked book,
  lab repository, and generated assets before promotion.
- Review `LAB-REQ-04` and `LAB-REQ-05` for real SQLite query/index,
  transaction/isolation, rollback, interruption, and backup/recovery evidence;
  keep PostgreSQL as an optional comparison rather than a hidden prerequisite.
- Keep OpenTelemetry, Chromium, CS144, and CS:APP as optional or source-routed
  cases unless a concrete learning requirement clears their complexity and
  maintenance cost.
- Map P1/P3/P4/P5/P6/P8 project checkpoints to selected mechanisms without
  making the Mini Cloud App the teaching vehicle.
- Require future Lab dossiers to add runnable smoke tests, exact reset steps,
  learner-facing exit criteria, and final license/attribution records.
- Do not mark this artifact `VERIFIED`; independent technical, pedagogical,
  lab-quality, and curriculum-integration review remains required.

## 9. Research source index

- [IETF RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [IETF Trust Legal Provisions](https://trustee.ietf.org/documents/trust-legal-provisions/)
- [MIT 6.1810 Fall 2025 xv6 Unix utilities lab](https://pdos.csail.mit.edu/6.1810/2025/labs/util.html)
- [MIT PDOS xv6-riscv at checked revision](https://github.com/mit-pdos/xv6-riscv/tree/35b088427ef37611c38afdeed5a52a278cae38f9)
- [MIT PDOS xv6 software MIT license at checked revision](https://raw.githubusercontent.com/mit-pdos/xv6-riscv/35b088427ef37611c38afdeed5a52a278cae38f9/LICENSE)
- [OSTEP official homework index](https://pages.cs.wisc.edu/~remzi/OSTEP/Homework/homework.html)
- [OSTEP threads-sema README at checked revision](https://github.com/remzi-arpacidusseau/ostep-homework/blob/afb36ca8ddbf81d847d18f6bd18a87f0a18667f2/threads-sema/README.md)
- [OSTEP rendezvous source at checked revision](https://github.com/remzi-arpacidusseau/ostep-homework/blob/afb36ca8ddbf81d847d18f6bd18a87f0a18667f2/threads-sema/rendezvous.c)
- [OSTEP homework license issue #71](https://github.com/remzi-arpacidusseau/ostep-homework/issues/71)
- [POSIX `pthread_mutex_lock`, IEEE/Open Group Issue 8](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_lock.html)
- [POSIX `pthread_cond_wait`, IEEE/Open Group Issue 8](https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_wait.html)
- [Allen Downey, The Little Book of Semaphores](https://greenteapress.com/wp/semaphores/)
- [Stanford Pintos Project 1: Threads](https://web.stanford.edu/class/cs140/projects/pintos/pintos_2.html)
- [Stanford Pintos documentation and license](https://web.stanford.edu/class/cs140/projects/pintos/pintos.pdf)
- [CS:APP3e lab assignments](https://csapp.cs.cmu.edu/3e/labs.html)
- [CS:APP3e Data Lab README](https://csapp.cs.cmu.edu/3e/README-datalab)
- [Stanford CS144 Fall 2025](https://cs144.github.io/)
- [Stanford CS144 Checkpoint 2](https://cs144.github.io/assignments/check2.pdf)
- [Stanford CS144 Checkpoint 4](https://cs144.github.io/assignments/check4.pdf)
- [CMU 15-445/645 Fall 2026 assignments](https://15445.courses.cs.cmu.edu/fall2026/assignments.html)
- [MIT 6.830 Database Systems assignments](https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/pages/assignments/)
- [UC Berkeley CS186 Spring 2026 course/project overview](https://cs186berkeley.net/)
- [SQLite EXPLAIN QUERY PLAN](https://sqlite.org/eqp.html)
- [SQLite query planning](https://sqlite.org/queryplanner.html)
- [SQLite command-line shell](https://sqlite.org/cli.html)
- [SQLite transaction control](https://sqlite.org/lang_transaction.html)
- [SQLite isolation](https://sqlite.org/isolation.html)
- [SQLite atomic commit](https://sqlite.org/atomiccommit.html)
- [SQLite write-ahead logging](https://sqlite.org/wal.html)
- [SQLite backup API](https://sqlite.org/backup.html)
- [SQLite public-domain statement](https://sqlite.org/copyright.html)
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
- [Creative Commons Attribution 3.0 US deed](https://creativecommons.org/licenses/by/3.0/us/)
- [Nand2Tetris Project 1: Boolean Logic](https://www.nand2tetris.org/project01)
- [Nand2Tetris software](https://www.nand2tetris.org/software)
