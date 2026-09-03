# M06 Activity — Processes, Syscalls & Execution Context

This host activity supports Lessons `L06-01`, `L06-02`, and `L06-03`.

It provides tools and fixtures to explore:
1. **Process Abstraction & Syscall Interface (L06-01):** Inspecting process identity, reading kernel `/proc/self` process attributes, and observing system calls.
2. **Process Lifecycle & Exit Status (L06-02):** Using `os.fork()`, observing unshared memory across parent/child contexts, checking exit codes with `waitpid`, and diagnosing zombie processes.
3. **Scheduling Intuition & Process States (L06-03):** Observing active running (`R`) vs waiting/sleeping (`S`) states in Linux procfs without CPU starvation.

---

## File Structure

- `process_observer.py`: Inspects PID, parent PID, `/proc/self/status`, and system calls via `strace` (with deterministic fallback).
- `fork_exec_fixture.py`: Demonstrates `fork`, child address-space mutation, exit code collection, and safe zombie observation.
- `scheduler_fixture.py`: Demonstrates running vs sleeping states with strictly timed child processes.
- `test_activity.py`: Automated test suite for process identity, lifecycle, and procfs attributes.
- `reset.py`: Cleanup utility to safely terminate any lingering processes and remove temporary files.

---

## Activity Flow

### 1. Process Identity & Procfs (L06-01)
Run the process observer:
```bash
python3 process_observer.py
```
- Observe `os.getpid()`.
- On Linux, observe that `/proc/self/status` contains matching `Pid:`, process `Name:`, and execution `State:`.
- Observe whether `strace` is functional or whether ptrace restrictions trigger the fallback evidence.

### 2. Fork, Memory Isolation & Exit Status (L06-02)
Run the fork lifecycle fixture:
```bash
python3 fork_exec_fixture.py
```
- Observe that `fork()` returns different values in the parent (child PID) and child ($0$).
- Observe that when the child mutates `test_var = 999`, the parent's variable remains $100$.
- Observe that `os.waitpid()` reaps the child and extracts exit code $42$.
- Observe that an un-reaped terminated child temporarily shows state `Z` (Zombie) in `/proc/<pid>/stat`, and is cleanly reaped in the `finally` block.

### 3. CPU Sharing & Scheduler States (L06-03)
Run the scheduler state observer:
```bash
python3 scheduler_fixture.py
```
- Observe that a CPU-bound worker shows state `R` (Running/Runnable).
- Observe that a worker sleeping in `time.sleep()` shows state `S` (Interruptible Sleep / Waiting on timer).

---

## Running Verification Tests

Run the automated test suite:
```bash
python3 -m unittest -v test_activity.py
```

---

## Clean Reset

To ensure no lingering child processes or temporary files remain:
```bash
python3 reset.py
```
