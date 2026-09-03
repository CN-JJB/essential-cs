# M06 Activity — Processes, Syscalls & Execution Context

This host activity supports Lessons `L06-01`, `L06-02`, and `L06-03`.

It provides bounded evidence for:
1. **Process & Syscall Boundary (L06-01):** process identity, Linux procfs metadata, and a live `write(2)` trace when `strace` works.
2. **Fork / Exec / Exit / Wait (L06-02):** parent/child return values, ordinary variable-copy separation, exec image replacement with PID preservation, exit status, and controlled zombie observation.
3. **Scheduling Intuition (L06-03):** bounded Linux `R` / `S` sampling for CPU-active vs sleeping children.

---

## File Structure

- `process_observer.py`: PID/procfs inspection and live `strace` capability check.
- `fork_exec_fixture.py`: fork, exec, exit/wait, and leak-free zombie fixture.
- `scheduler_fixture.py`: bounded process-state sampling with guaranteed child cleanup.
- `test_activity.py`: machine-checks stable relations and reports environment-sensitive non-observation as skip.
- `reset.py`: cleanup utility for local generated files.

---

## Activity Flow

### 1. Process Identity & Procfs (L06-01)

```bash
python3 process_observer.py
```

- Verify `os.getpid()` against Linux `/proc/self/status` when procfs exists.
- If `strace` works, record the actual `write(2)` trace.
- If `strace` is missing/restricted, the tool reports **NO LIVE SYSCALL TRACE**. Procfs is still process-state evidence but is not equivalent to syscall-entry evidence.

### 2. Fork → Exec → Exit → Wait (L06-02)

```bash
python3 fork_exec_fixture.py
```

Observe:
- parent receives child PID while child receives `0` from `fork()`;
- changing an ordinary Python variable in the child does not alter the parent's copy;
- an exec'd Python image reports the **same PID** as the fork child;
- parent collects the exec'd image's exit status with `waitpid()`;
- a Linux zombie may be observed as `Z` before wait/reap; if it is not observed in the bounded window, record **NOT OBSERVED**, while cleanup still must succeed.

This ordinary-variable fixture does **not** prove that processes can never share memory; explicit shared mappings/IPC are later/other mechanisms.

### 3. CPU Sharing & Linux Process States (L06-03)

```bash
python3 scheduler_fixture.py
```

The fixture polls for:
- `R` on a CPU-active child;
- `S` on a child blocked in `time.sleep()`.

These letters are Linux procfs observations, not a universal OS state machine. A heavily constrained environment may fail to expose the expected sample during the bounded window; record that as **NOT OBSERVED/SKIP**, not a fabricated PASS.

---

## Running Verification Tests

```bash
python3 -m unittest -v test_activity.py
```

Read the final `OK` line together with the **skipped** count. A skipped environment-sensitive observation is not evidence that the observation itself passed.

---

## Clean Reset

```bash
python3 reset.py
```
