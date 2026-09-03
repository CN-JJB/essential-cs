# M07 — Virtual Memory & Isolation Lab Packet

This lab packet provides safe, bounded, machine-checkable experiments illustrating virtual memory mappings, demand paging, and hardware/OS memory fault handling on Linux hosts.

## Included Fixtures & Tools

1. **`maps_observer.py`**
   - Inspects and parses `/proc/self/maps` dynamically.
   - Categorizes virtual memory regions: executable code segments (`r-xp`), writable data/heap/stack segments (`rw-p`), read-only segments, and anonymous mappings.
   - **Key Invariant**: Mappings show virtual address space intervals and access permissions; they do **not** expose physical RAM page frames (PFNs) and do not prove whether physical frames are allocated.

2. **`residency_fixture.py`**
   - Demonstrates the distinction between address-space reservation (`VmSize`) and physical memory residency (`VmRSS`).
   - Uses a safe, bounded 16 MiB anonymous mapping (`mmap`).
   - Touches pages incrementally (first half, then full) and records before/after metrics from `/proc/self/status` and `resource.getrusage()` (`ru_minflt`).
   - **Key Invariant**: Virtual reservation is cheap and lazy; physical frames are committed on first write (demand paging via minor page faults).

3. **`bad_address.c` & `fault_runner.py`**
   - Safe observation of invalid memory access.
   - Compiles a minimal C fixture under `-O0 -Wall -Wextra` and executes it inside a bounded child process with a 5-second timeout.
   - Analyzes child termination using `subprocess` signal semantics (negative return code `-11` / `SIGSEGV`).
   - **Key Invariant**: Null pointer dereference is **Undefined Behavior (UB)** at the C language specification layer. The observed `SIGSEGV` is a hosted operating system and MMU hardware response, not a language-level guarantee.

4. **`test_activity.py`**
   - Automated unit test suite verifying map parsing, residency directional metrics, fault runner execution, and cleanup.

5. **`reset.py`**
   - Cleans up compiled binaries (`bad_address`), object files, and Python bytecode caches.

## Preflight & Prerequisites

- **Host OS**: Linux (native, container, or WSL2).
- **Python**: Python 3.10+ (tested on Python 3.12).
- **Compiler**: GCC 11+ or Clang (tested on GCC 13.3).
- **Filesystem**: procfs (`/proc/self/maps` and `/proc/self/status` readable).

## Execution Commands

Run each tool individually:

```bash
cd labs/foundations/m07

# 1. Observe virtual memory mappings and permissions
python3 maps_observer.py

# 2. Observe lazy reservation vs physical residency
python3 residency_fixture.py

# 3. Observe safe child-process memory fault handling
python3 fault_runner.py
```

Run automated verification:

```bash
python3 test_activity.py
```

Clean up all build artifacts:

```bash
python3 reset.py
```

## Safety Guarantees

- **No Root / Sudo**: All scripts run as an unprivileged user.
- **No Host Exhaustion**: Memory allocation is strictly bounded to 16 MiB; no OOM killer is triggered.
- **Child Process Isolation**: Invalid memory access runs strictly in a child process bounded by timeout.
- **No Network**: Zero external network requests.
