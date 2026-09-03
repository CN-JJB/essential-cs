# Foundations M06 Evidence Template

## A — Environment / Preflight
- Dispatch / Working Commit:
- Operating System:
- Kernel Version:
- Hardware Architecture:
- Python Implementation & Version:
- Native Compiler & Version:
- Process Tools (`ps`, `/proc` availability):
- `strace` Capability Status (PASS / RESTRICTED / MISSING):
- Preflight Summary:

---

## B — Program vs Process Explanation
- Program Artifact Definition (What is on storage?):
- Process Execution Context Definition (What is in memory/OS?):
- Key State Elements of a Running Process:
- Why is a program file NOT a process?

---

## C — PID & Procfs Evidence
- Command Run: `python3 process_observer.py`
- Current Process ID (`os.getpid()`):
- Parent Process ID (`os.getppid()`):
- Procfs Status File: `/proc/self/status`
  - `Pid:` extracted:
  - Does `Pid:` match `os.getpid()`?
  - `State:` extracted:
  - `VmSize:` extracted:
  - `FDSize:` extracted:
- Procfs Stat Raw Excerpt:

---

## D — System Call Observation / Fallback Limitation
- `strace` Availability in Current Environment:
- If `strace` functional:
  - Command run:
  - Syscall excerpt (`write` / `getpid`):
- If `strace` restricted or missing:
  - Exact restriction reported (e.g. ptrace seccomp policy / not installed):
  - Fallback deterministic trace observed:
  - Limitation note (Why procfs state is not equivalent to tracing syscall entry):

---

## E — Fork Evidence
- Command Run: `python3 fork_exec_fixture.py`
- Parent PID:
- `os.fork()` Return Value in Parent:
- `os.fork()` Return Value in Child:
- Variable Mutation Isolation Evidence:
  - Parent variable before/after fork:
  - Child variable after mutation:
  - Did the child's mutation affect the parent?

---

## F — Exec Evidence
- How does `execve` change the process execution context?
- Does `exec` create a new PID?
- What happens to the memory image during `exec`?

---

## G — Exit & Wait Status
- Child Exit Code Called (`os._exit(42)`):
- Parent `os.waitpid()` Raw Status:
- `os.WIFEXITED(status)`:
- `os.WEXITSTATUS(status)` extracted:
- Does extracted exit code match 42?

---

## H — Zombie Observation & Cleanup
- How was the zombie process created?
- Observed State in `/proc/<child_pid>/stat` prior to `wait()`:
- Did the state reflect `Z` (Zombie)?
- Cleanup Verification: How was the child process reaped in the `finally` block?
- Why do zombie processes NOT eat CPU cycles?

---

## I — Scheduling: Runnable vs Waiting Evidence
- Command Run: `python3 scheduler_fixture.py`
- CPU-Active Worker PID:
  - Observed States:
  - Did worker show `R` (Running/Runnable)?
- Sleeping Worker PID:
  - Observed States:
  - Did worker show `S` (Interruptible Sleep)?
- Explanation of Timer Preemption & Wait Queues:

---

## J — POSIX Contract vs Linux Implementation vs Actual Observation Table
Classify each claim into: `POSIX Contract`, `Linux Implementation Detail`, or `Actual Observation`.

| Claim | Layer | Justification |
|---|---|---|
| `fork()` creates a new process with an identical logical memory image | | |
| Linux uses Copy-on-Write (COW) page sharing after `fork()` | | |
| Process state letters `R`, `S`, `Z` in `/proc/<pid>/stat` | | |
| `waitpid()` suspends calling process until child status changes | | |
| Child exit code observed was 42 | | |
| Process virtual size was `18628 kB` | | |

---

## K — Process Canonical Definition Check
- Verify that **EC-CON-018 Process** is defined as:
  > A managed execution context with identity, resources, and normally an address-space boundary through which a program runs. It is not source code, a thread, a container image, or a virtual machine.
- Verify that **EC-CON-013 Isolation** is NOT canonically defined here (deferred to M07).

---

## L — Fact vs Inference / Limitations
- What facts did your observation directly establish?
- What competing explanations exist (e.g. scheduler timing jitter)?
- What are the limitations of your evidence?
