# M08 — Files, Filesystems & System I/O Lab Packet

This lab packet provides safe, bounded, machine-checkable experiments illustrating file identity, directory entry decoupling, open-file descriptor lifetimes, buffered write layering, kernel page cache dirty metrics, and POSIX error handling on Linux hosts.

## Included Fixtures & Tools

1. **`file_identity.py`** (Supports `L08-01`)
   - Demonstrates the decoupling between pathnames/directory entries, process file descriptors, kernel open file descriptions, and filesystem inodes.
   - Shows that hard links on the same filesystem share identical inode numbers (`st_ino`) and device IDs (`st_dev`), with link count incrementing (`st_nlink = 2`).
   - Demonstrates the reference-lifetime invariant: unlinking all directory entries removes the names from the filesystem, but already-open file descriptors retain access to file data until closed.
   - Inspects `/proc/self/fd/<fd>` on Linux to reveal kernel file-handle resolution (showing `(deleted)` when unlinked).
   - **Key Invariant**: A filename is stored in a directory entry, not inside the file itself; disk blocks are freed only when link count is 0 *and* all open references are closed.

2. **`buffered_io_observer.py`** (Supports `L08-02`)
   - Traces the four-layer write path: Runtime Buffer $\rightarrow$ Syscall Boundary (`write`) $\rightarrow$ Linux Page Cache (Dirty RAM) $\rightarrow$ Block Device.
   - Compares user-space buffered I/O batching with raw unbuffered `os.write()`.
   - Probes live `strace` capability truthfully; if strace is missing or restricted, reports `NO LIVE SYSCALL TRACE` without synthesizing fake output.
   - Observes `/proc/meminfo` Dirty and Writeback metrics directionally for bounded files, explicitly noting system-global concurrency and noise.
   - **Key Invariant**: Calling `write()` or `flush()` returns success when the OS accepts data into memory; it does **not** prove power-loss durability. Durability is canonically established in M09 (`L09-01`).

3. **`io_failure_fixture.py`** (Supports `L08-03`)
   - Deterministically reproduces `ENOENT` on non-existent path resolution.
   - Implements capability gating for `EACCES`: under unprivileged users, reproduces `PermissionError` on read-only mode bits; under root (`uid=0`), records truthful `ENVIRONMENT-LIMITED` disposition because `CAP_DAC_OVERRIDE` bypasses mode bits.
   - Models storage capacity exhaustion (`ENOSPC`) and POSIX partial writes via a safe, course-owned bounded in-memory abstraction (`BoundedSpaceWriter`), strictly preventing host root filesystem exhaustion.
   - Provides diagnostic triage mapping symptoms, error codes, and subsystems.

4. **`test_activity.py`**
   - Automated unit test suite verifying all invariants across `L08-01`, `L08-02`, and `L08-03`.

5. **`reset.py`**
   - Deterministically cleans up all temporary run artifacts, test files, and bytecode caches.

## Preflight & Prerequisites

- **Host OS**: Linux (native, container, or WSL2).
- **Python**: Python 3.10+ (tested on CPython 3.12.3).
- **procfs**: `/proc/self/fd` (directory) and `/proc/meminfo` (readable).
- **Tracing (Optional)**: `strace` with ptrace capability (if absent, tools truthfully report `NO LIVE SYSCALL TRACE`).

## Execution Commands

Run each tool individually:

```bash
cd labs/foundations/m08

# 1. Observe file identity, hard links, and open-unlink reference lifetimes
python3 file_identity.py

# 2. Observe buffered write batching, page cache dirty metrics, and durability boundary
python3 buffered_io_observer.py

# 3. Observe POSIX failure reproduction, capability gating, and safe ENOSPC model
python3 io_failure_fixture.py
```

Run automated verification:

```bash
python3 test_activity.py
```

Clean up all temporary artifacts:

```bash
python3 reset.py
```

## Safety Guarantees

- **No Root / Sudo Required**: All tools run safely as an unprivileged user.
- **No Host Exhaustion**: Capacity limits are demonstrated via a bounded course-owned in-memory model (`BoundedSpaceWriter`). No host filesystem or partition is filled.
- **No Raw Block Devices**: Zero manipulation of raw disks, partitions, mount tables, or system quotas.
- **Deterministic Cleanup**: All temporary files reside in scoped directories and are cleaned up immediately.
- **Zero Synthetic Traces**: Never fabricates `strace` output when tracing is unavailable.
