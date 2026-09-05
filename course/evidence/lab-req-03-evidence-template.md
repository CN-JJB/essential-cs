# LAB-REQ-03 Evidence Template — POSIX Threads Race, Rendezvous & Progress Boundaries

Use this template for **one actual learner run of LAB-REQ-03**. Do not prefill or copy values. Record observed engineering facts truthfully.

---

## 1. Exact Canonical Environment & Compiler

- Execution Timestamp: `<actual ISO 8601 timestamp>`
- Host Operating System & Distro: `<actual Linux distribution, kernel release, and arch, or non-Linux host disposition>`
- Canonical Environment Gate: `<CANONICAL LINUX / NON-CANONICAL CAPABLE HOST>`
- Compiler Path: `<actual path to gcc>`
- Compiler Version: `<actual gcc --version first line>`
- Canonical GCC Gate: `<GCC CONFIRMED / CLANG NON-CANONICAL / OTHER>`
- Compilation Command:
  ```bash
  gcc -std=c11 -pthread <source>.c -o <binary>
  ```
- Compilation Outcome: `<PASS / FAIL>`
- Build Log / Warnings: `<actual compiler output or clean>`

---

## 2. Source Safety & UB-Free Audit

- Source File: `labs/lab_req_03/broken_counter.c`
- Atomic Types Used: `atomic_int` from `<stdatomic.h>`
- Read Access: `atomic_load_explicit(&g_shared_counter, memory_order_relaxed)`
- Write Access: `atomic_store_explicit(&g_shared_counter, computed, memory_order_relaxed)`
- C-Language Data-Race UB in the Required shared-counter path: `<YES / NO>`
- Concurrency Bug Nature: **Logical race condition on compound state transition (Read $\to$ Compute $\to$ Store)**, NOT memory-level undefined access.
- Audit Status: `<CONFIRMED REQUIRED SHARED-COUNTER PATH USES DEFINED ATOMIC ACCESSES / REJECTED>`

---

## 3. Checkpoint 1: Deterministic Broken-Path Interleaving Trace

- Command: `python labs/lab_req_03/runner.py` (Checkpoint 1)
- Rounds Executed: `<actual rounds>`
- Phase Trace Summary:
  - `<one row per actual configured round: round id, each worker's observed value, computed value, and phase ordering>`
- Expected Serial Total: `<actual expected serial value>`
- Actual Final Counter: `<actual observed value>`
- Lost Updates Count: `<actual lost count>`
- Deterministic Interleaving Proven: `<YES / NO>`

---

## 4. Checkpoint 2: Supplemental Natural Scheduler Disposition

- Command: `broken_counter --natural <iterations>`
- Iterations per Thread: `<actual iterations>`
- Expected Serial Total: `<actual expected value>`
- Observed Counter Value: `<actual value observed>`
- Lost Updates Manifested: `<YES / NO>`
- Actual Disparity: `<actual lost count>`
- Disposition: `<MANIFESTED / NO MANIFESTATION OBSERVED>`
- Natural Run Inference Limit: Supplemental evidence only; lack of manifestation does not invalidate the race condition.

---

## 5. Checkpoint 3: Mutex Repair Invariant Verification

- Command: `mutex_counter <iterations>`
- Synchronization Primitive: `pthread_mutex_t`
- Iterations per Thread: `<actual iterations>`
- Expected Total: `<actual expected value>`
- Observed Total: `<actual observed value>`
- Invariant Preserved: `<YES / NO>`
- State Transitions Protected: Read $\to$ Compute $\to$ Store serialized atomically under mutual exclusion.

---

## 6. Checkpoint 4: Condition-Variable Rendezvous Verification

- Command: `cond_rendezvous`
- Synchronization Primitives: `pthread_cond_t` + `pthread_mutex_t`
- Predicate Re-evaluation Guard: `while (!g_buffer_ready) pthread_cond_wait(...)`
- Consumed Data: `<actual value, e.g. 42>`
- Predicate Evaluation Count: `<actual count, e.g. 2>`
- Event Sequence Observed:
  1. `COND_WAIT_ENTER` (predicate: false)
  2. `PRODUCER_READY` (produced: 42)
  3. `COND_WAIT_RETURN` (predicate: true)
  4. `COND_CONSUMED` (consumed: 42)
- Rendezvous Verified: `<YES / NO>`

---

## 7. Checkpoint 5: Controlled Deadlock Preconditions & Watchdog Reaping

- Command: `deadlock_preconditions` under parent watchdog
- Child PID: `<actual PID>`
- Circular Wait Preconditions Logged:
  - Thread 1 acquired Lock A: `<CONFIRMED>`
  - Thread 2 acquired Lock B: `<CONFIRMED>`
  - Thread 1 attempting Lock B: `<CONFIRMED>`
  - Thread 2 attempting Lock A: `<CONFIRMED>`
- Watchdog Timeout Parameter: `<actual configured timeout>`
- Watchdog Triggered: `<YES / NO>`
- Child Termination: Process terminated via `proc.terminate()` / `proc.kill()`
- Child Reaped Returncode: `<actual returncode / signal>`
- Circular Deadlock Proven: `<YES / NO>` (proven because preconditions verified prior to timeout)

---

## 8. Binary & Scratch Cleanup Verification

- Reset Command: `python labs/lab_req_03/reset.py`
- Run 1 Removed Count: `<actual count>`
- Run 2 Removed Count: `0` (Idempotence verified)
- Clean Working Tree Confirmed: `git status --porcelain` shows 0 untracked binaries

---

## 9. Residual Risks & Environment Blockers

- Non-Linux Host Disposition: `<NOT APPLICABLE / BLOCKED NOTE>`
- Compiler Caveats: `<any environment-specific notes>`
- ThreadSanitizer Availability: `<AVAILABLE / OPTIONAL TOOL SKIPPED>`
