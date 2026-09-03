# Foundations M07 Evidence Template

## A — Environment / Preflight
- Dispatch / Working Commit:
- Operating System (uname / distribution):
- Kernel Version:
- Hardware Architecture:
- Python Implementation & Version:
- Native Compiler & Version:
- Procfs Maps Availability (`/proc/self/maps` readable?):
- Procfs Status Availability (`/proc/self/status` readable?):
- Resource Module (`resource.getrusage` available?):
- Preflight Summary:

---

## B — Virtual Mapping Evidence
- Command Run: `python3 maps_observer.py`
- Current Process ID (`os.getpid()`):
- Total Virtual Mappings Parsed:
- Total Virtual Address Space Spanned (KiB):
- Sample Executable Mapping Range:
- Sample Writable Mapping Range:
- Is the reported address process-local virtual or physical?
- Why do base addresses differ across independent runs (ASLR)?

---

## C — Permissions Evidence
- Distinct Permissions Observed in Maps (e.g. `r--p`, `r--s`, `r-xp`, `rw-p`):
- Executable Segment Characteristics (e.g. `/usr/bin/python3.12`, `r-xp`):
- Writable Segment Characteristics (e.g. `[heap]`, `rw-p`):
- How does the CPU MMU enforce these permissions during instruction execution?

---

## D — What maps Does NOT Prove
- Does `/proc/self/maps` expose physical page frame numbers (PFNs)?
- Does the existence of a mapping range prove physical RAM frame allocation (residency)?
- If two processes report identical virtual addresses, does maps prove they share physical memory?
- Evidence Boundary Summary:

---

## E — Isolation Definition
- Canonical Concept ID: `EC-CON-013`
- Registry Definition:
- Key Operational Meaning (Limiting interference or visibility between executions, identities, resources, or fault domains):
- Why Isolation is NOT synonymous with process, encryption, or absolute security:

---

## F — Trust Boundary Definition
- Canonical Concept ID: `EC-CON-017`
- Registry Definition:
- Key Operational Meaning (Boundary where authority, trust assumptions, or enforcement responsibility changes):
- Requirements for crossing a trust boundary (explicit input validation, bounded output exposure):

---

## G — Isolation vs Trust Boundary Example
- Example 1 (Memory Isolation without Trust Equivalence):
  - Description:
  - Why Isolation does not imply a shared trust boundary:
- Example 2 (Explicit Shared Memory without Dissolving Trust Boundary):
  - Description:
  - How memory isolation is intentionally bypassed (`MAP_SHARED`) while input validation remains mandatory:
- Core Distinction Summary:

---

## H — Reservation / Touch / Residency Evidence
- Command Run: `python3 residency_fixture.py`
- Bounded Target Size:
- Stage 0 (Baseline):
  - `VmSize`:
  - `VmRSS`:
- Stage 1 (Reserved via `mmap`):
  - `VmSize`:
  - `VmRSS`:
  - `VmSize` Delta from Baseline:
  - `VmRSS` Delta from Baseline:
  - Observed `VmRSS` relation after reservation (do not assume it must remain unchanged):
- Stage 2 (Half Touched):
  - `VmRSS`:
  - `VmRSS` Delta:
- Stage 3 (Fully Touched):
  - `VmRSS`:
  - Total `VmRSS` Delta across all touched pages:
- Stage 4 (Cleaned Up):
  - `VmSize` after unmap:
  - `VmRSS` after unmap:
- Core Takeaway on Demand Paging (Reservation vs Residency):

---

## I — Page-Fault / Resource Counters + Limits
- Baseline `ru_minflt`:
- Reserved `ru_minflt`:
- Half Touched `ru_minflt`:
- Fully Touched `ru_minflt`:
- Observed `ru_minflt` Delta During Touching:
- Why `ru_minflt` is Unix/Linux-family accounting evidence, not universal hardware semantics:
- Limitations (zero-page optimizations, runtime allocator caching):

---

## J — OOM / Overcommit Explanation Without Destructive Experiment
- Linux Overcommit Policy Configuration (`/proc/sys/vm/overcommit_memory` modes 0, 1, 2):
- Why `malloc` / `mmap` can succeed (return non-NULL) even if physical RAM cannot fulfill future writes:
- Bounded Linux OOM behavior (memory domain/cgroup, reclaim, candidate selection, possible `SIGKILL`; avoid fixed victim rules):
- Safety Boundary Statement (Why destructive host exhaustion tests are forbidden):

---

## K — Bad-Address Fixture Compile / Run
- Fixture File: `bad_address.c`
- Compiler Command & Flags:
- Compiler Version:
- Compilation Exit Code:
- Runner Tool: `fault_runner.py`
- Execution Method (child process with bounded timeout):
- Timeout Limit:
- Raw Subprocess Return Code:
- Was Child Terminated by Signal?
- Observed Signal Number & Name:

---

## L — Language UB vs Hosted Signal Result
- ISO C Standard Layer (ISO/IEC 9899 Undefined Behavior):
  - Does the C language standard guarantee a signal or termination?
- Hosted OS / MMU Layer:
  - Why does the tested Linux/x86-64 host deliver `SIGSEGV`?
- Shell Representation Layer:
  - Why does a shell report exit code 139? (`128 + 11`)
  - Why is exit 139 a shell convention rather than universal OS kernel semantics?

---

## M — Fault Handler Resolve-vs-Fail Explanation
- CPU Hardware Event (architecture-specific translation/protection fault; record x86 `#PF` only when that architecture is in scope):
- OS Kernel Decision Tree:
  - How benign faults are resolved and retried transparently (demand allocation, COW, swap-in):
  - How an unresolved/protection-invalid user access may become a user-visible failure; record `SIGSEGV` only as hosted observation when reproduced:
- Correction of the Fault Taxonomy:
  - Distinguish hardware fault events from OS recovery policies and Linux accounting (Minor/Major):

---

## N — Fact vs Inference / Environment Limitations
- Direct Host Observations (Facts):
- Inferences & OS-Specific Policies:
- Cross-Platform Differences (Windows commit charge, macOS, RTOS):
- Safety Confirmations (No root required, memory bounded to 16 MiB, no hanging processes, clean directory state):

---

## O — Canonical First-Home Audit
- `EC-CON-013 Isolation` -> First Home in `L07-01` [AUDIT: CONFIRMED]
- `EC-CON-017 Trust Boundary` -> First Home in `L07-01` [AUDIT: CONFIRMED]
- `EC-CON-018 Process` -> Revisit only (First Home in M06 `L06-01` preserved) [AUDIT: CONFIRMED]
- New Concept IDs Created: NONE [AUDIT: CONFIRMED]
