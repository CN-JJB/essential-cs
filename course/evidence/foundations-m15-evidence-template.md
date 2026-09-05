# Foundations M15 Evidence Template — Concurrency: Threads, Races & Synchronization

Use this template for **one actual learner observation**. Do not prefill or copy another learner's tool version, thread scheduling order, race manifestation rate, watchdog timeout duration, child process return/signal, bytecode opcodes, GIL mode, benchmark speedup, or test pass markers.

---

## A — Host OS, Compiler, POSIX Thread & C11 Atomic Capabilities

- Execution commit / ref: `<actual HEAD commit SHA>`
- Host Operating System: `<actual OS>`
- Kernel / OS Release: `<actual release / kernel version>`
- Architecture: `<actual CPU architecture>`
- Compiler Path: `<actual compiler binary path>`
- Compiler Identity & Version: `<actual GCC/Clang version string>`
- C11 Compilation Flag: `<actual compiler flags>`
- C11 Atomics (`<stdatomic.h>`) Capability: `<PASS / FAIL / BLOCKED>`
- POSIX Pthread Capability: `<PASS / FAIL / BLOCKED>`
- POSIX Mutex & Condition Variable Capability: `<PASS / FAIL / BLOCKED>`
- Owned-Child Watchdog & Reaping Capability: `<PASS / FAIL / BLOCKED>`

---

## B — EC-CON-015 Concurrency Exact Canonical Definition

- Verbatim Canonical Definition:
  > **“Overlapping progress or interleaving of operations, whether or not they execute simultaneously on hardware. Concurrency creates ordering and shared-state obligations.”**
- Disambiguation Check:
  - Concurrency vs. Parallelism: `<Learner notes distinguishing interleaving/structure from physical multi-core execution>`
  - Single-Core Concurrency: `<Learner notes explaining preemptive time-slicing>`
  - Logical Race Condition vs. C Data Race: `<Learner notes explaining that ISO C11 §5.1.2.4 data race is UB, whereas logical race condition is an ordering flaw>`

---

## C — Broken Compound-Update Source Code Audit (No UB)

- Source File Audited: `labs/lab_req_03/broken_counter.c`
- Shared Variable Storage Type: `atomic_int` (`<stdatomic.h>`)
- Read Primitive: `atomic_load_explicit(&g_shared_counter, memory_order_relaxed)`
- Write Primitive: `atomic_store_explicit(&g_shared_counter, next, memory_order_relaxed)`
- Unsynchronized Plain Shared Non-Atomic Counter Present: `NO`
- Language-Level Undefined Behavior (UB) Present: `NO`
- Audit Disposition: `<CONFIRMED UB-FREE / REJECTED>`
- Audit Notes: `<Learner confirms that all concurrent memory accesses are defined atomic operations>`

---

## D — Observed Lost-Update Interleaving & Scheduler Disposition

### 1. Deterministic Coordinated Path
- Coordination Primitives: Course-controlled barrier coordination (Read Phase $\to$ Store Phase $\to$ Round End)
- Rounds Executed: `<actual rounds>`
- Expected Serial Invariant: `<actual expected serial value>`
- Observed Counter Value: `<actual value observed>`
- Missing / Lost Increments: `<actual lost count, e.g. 5>`
- Interleaving Proven Deterministically: `<YES / NO>`

### 2. Supplemental Natural Scheduler Observation
- Execution Command: `broken_counter --natural <iterations>`
- Iterations per Thread: `<actual iterations>`
- Expected Serial Total: `<actual expected>`
- Observed Counter Value: `<actual value observed>`
- Lost Updates Manifested: `<YES / NO>`
- Actual Observed Disparity: `<actual difference or 0>`
- Inference Limit: `<Learner acknowledges that absence of manifestation under natural scheduling is truthful evidence, not a test failure>`

---

## E — Mutex Repair Invariant Verification

- Source File: `labs/lab_req_03/mutex_counter.c`
- Synchronization Primitive: `pthread_mutex_t` (`pthread_mutex_lock` / `pthread_mutex_unlock`)
- Critical Section Scope: `<Learner identifies enclosed Read -> Compute -> Store operations>`
- Iterations per Thread: `<actual iterations>`
- Expected Invariant Total: `<actual expected, e.g. 20000>`
- Actual Counter Value: `<actual observed value>`
- Invariant Preserved Across Runs: `<YES / NO>`
- Mutex Fairness Limit: `<Learner notes that POSIX mutexes do not guarantee FIFO fairness or starvation freedom>`

---

## F — Condition-Variable Predicate Rendezvous Verification

- Source File: `labs/lab_req_03/cond_rendezvous.c`
- Synchronization Primitives: `pthread_cond_t` + associated `pthread_mutex_t`
- Predicate Variable: `buffer_ready`
- Wait Logic Loop Pattern:
  ```c
  pthread_mutex_lock(&g_rendezvous_mutex);
  while (!g_buffer_ready) {
      pthread_cond_wait(&g_rendezvous_cond, &g_rendezvous_mutex);
  }
  // Safe state consumption
  pthread_mutex_unlock(&g_rendezvous_mutex);
  ```
- Predicate Re-evaluation Count Observed: `<actual evaluation count>`
- Spurious Wakeup Defense Explained: `<Learner notes that a wait return does not imply predicate truth; predicate re-evaluation is required, and the course uses a while-loop idiom>`
- Rendezvous Success Verified: `<YES / NO>`

---

## G — Controlled Deadlock Preconditions & Watchdog Reaping Record

- Source File: `labs/lab_req_03/deadlock_preconditions.c`
- Execution Environment: Owned child process managed by parent watchdog
- Child Process PID: `<actual child PID>`
- Circular Wait Preconditions Observed:
  - Thread 1 First Lock Acquired: `<actual lock name, e.g. Lock A>`
  - Thread 2 First Lock Acquired: `<actual lock name, e.g. Lock B>`
  - Thread 1 Second Lock Attempted: `<actual lock name, e.g. Lock B>`
  - Thread 2 Second Lock Attempted: `<actual lock name, e.g. Lock A>`
- Watchdog Timeout Parameter: `<actual configured duration>`
- Watchdog Triggered: `<YES / NO>`
- Child Termination Action: `proc.terminate()` / `proc.kill()`
- Child Reaped Returncode / Signal: `<actual exit code or signal>`
- Inference Boundary: `<Learner confirms timeout alone does NOT prove deadlock; deadlock is proven because circular wait preconditions were verified before timeout>`

---

## H — Fairness & Scheduler Progress Inference Limits

- Lock Starvation Observation: `<Learner notes on POSIX mutex scheduling>`
- OS Preemption Scope: `<Learner notes on thread preemption boundaries>`
- Host Independence: `<Learner notes that thread execution order cannot be guaranteed across host platforms>`

---

## I — Thread vs. Async Architectural Evaluation

- Evaluation Matrix Label: **NO UNIVERSAL WINNER — WORKLOAD/RUNTIME DRIVEN**
- Workload 1 (High-Concurrency Network I/O):
  - Recommended Model: `<OS Threads / Cooperative Async Event Loop>`
  - Architectural Rationale: `<Learner explanation referencing memory per task and non-blocking I/O multiplexing>`
- Workload 2 (CPU-Bound Multiprocessor Parallelism):
  - Recommended Model: `<Preemptive Threads / Multiprocessing>`
  - Architectural Rationale: `<Learner explanation referencing core utilization and runtime GIL constraints>`
- Workload 3 (Mixed I/O with Blocking Legacy Library):
  - Recommended Model: `<Async Event Loop with Thread/Process Executor Delegation>`
  - Architectural Rationale: `<Learner explanation referencing loop stalling avoidance>`

---

## J — Named CPython Runtime, Disassembly & GIL/Free-Threading Observation

- Python Implementation: `<actual implementation, e.g. CPython>`
- Python Version: `<actual version string>`
- `Py_GIL_DISABLED` Configuration Value: `<actual value, e.g. 0, 1, or NOT AVAILABLE>`
- `_is_gil_enabled()` Runtime Return: `<actual True, False, or NOT APPLICABLE>`
- Bytecode Disassembly of `x += 1`:
  - Disassembly Output Captured:
    ```
    <actual output of dis.dis('x += 1') for current runtime>
    ```
  - Total Opcode Count: `<actual opcode count>`
  - Individual Opcode Names Observed: `<actual opcode names from this runtime>`
- Multi-step Interpretation: `<Learner explains why the GIL does not make x += 1 atomic in application logic>`
- Official Free-Threading Currentness Citation:
  - Source Authority: `https://docs.python.org/3.14/howto/free-threading-python.html & PEP 779`
  - Recheck Date: `2026-09-05`
  - Status: `Supported Phase II (Optional Build)`

---

## K — Concepts, Competencies, Visuals, Support & Cleanup Audit

- Primary Competency: `Diagnose`
- Secondary Competencies: `Trace`, `Correctness`, `Explain`, `Judge`
- Canonical Concepts Verified:
  - `EC-CON-015 Concurrency`: Canonical First Home in L15-01 with exact verbatim definition
  - `EC-CON-001 State`: Thread private vs shared address-space state
  - `EC-CON-007 Specification`: ISO C11 memory model & POSIX.1-2024 thread specification
  - `EC-CON-008 Invariant`: Mutex-protected critical section invariant
  - `EC-CON-009 Correctness`: Verification of deterministic state transitions
  - `EC-CON-013 Isolation`: Synchronization scope in thread vs async architectures
  - `EC-CON-018 Process`: Checked — NOT claimed as an authorized Concept Revisit in M15
- Visuals Verified:
  - L15-01: Concurrency vs Parallelism & Interleaving (with verbatim EC-CON-015 definition)
  - L15-02: Mutex Invariant & Condition Rendezvous (with mandatory predicate recheck guard)
  - L15-03: Concurrency Execution Models (with mandatory NO UNIVERSAL WINNER label)
- Progressive Support Ladder Verified: All 5 tiers present, no `<details open>` tags
- Cleanup Verified: Idempotent reset executed twice, 0 residual compiled binaries or temp artifacts
