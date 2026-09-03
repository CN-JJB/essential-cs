# Foundations M08 Evidence Template

## A — Environment / Filesystem / Capability Preflight
- Dispatch / Working Commit:
- Operating System (uname / distribution):
- Kernel Version:
- Hardware Architecture:
- Python Implementation & Version:
- Filesystem Type for Hard-Link/Unlink Observations (e.g. ext4, tmpfs):
- Procfs FD Availability (`/proc/self/fd` directory readable?):
- Procfs Meminfo Availability (`/proc/meminfo` readable?):
- strace Installation & Live-Tracing Capability (`strace -V` / `strace true`):
- Preflight Summary:

---

## B — Pathname / Directory-Entry Evidence
- Command Run: `python3 file_identity.py`
- Target Pathname:
- Does the file metadata object (inode) store its own pathname inside itself?
- Role of Directory Entry (dentry):
- Why can multiple pathnames point to the same filesystem object?

---

## C — FD / Open-File-Description Evidence
- Integer File Descriptor Allocated (`fd`):
- Process-local FD Table Role (`task_struct->files->fdt`):
- Kernel Open File Description (`struct file`):
- Shared State inside Open File Description (file offset, status flags, reference count):
- `/proc/self/fd/<fd>` Target Link Observation:

---

## D — inode / File-Identity + Hard-Link Evidence
- Original File Stat (`st_ino`, `st_dev`, `st_nlink`):
- Hard Link Pathname:
- Hard Link Stat (`st_ino`, `st_dev`, `st_nlink`):
- Machine-Checked Inode Identity (`st_ino` equal?):
- Machine-Checked Device Identity (`st_dev` equal?):
- Link Count Delta after `os.link`:
- Why cannot hard links cross filesystem boundaries?

---

## E — open → unlink → Continued Descriptor Access
- Action: Unlink original pathname (`os.unlink`):
  - Remaining hard link `st_nlink`:
- Action: Unlink second pathname (`os.unlink`):
  - Inode `st_nlink`: 0
  - Directory existence (`os.path.exists`):
  - Observed `/proc/self/fd/<fd>` link target (e.g. `... (deleted)`):
- Continued Read via Open Descriptor:
  - Did read return original byte content?
- Continued Write via Open Descriptor:
  - Bytes successfully written to unlinked descriptor:
  - Total bytes readable through open descriptor:
- When are disk data blocks and inode truly reclaimed by the filesystem?

---

## F — POSIX vs Linux / Filesystem-Specific Boundaries
- POSIX Interface Contract:
  - What does POSIX specify regarding `open`, `unlink`, and open descriptor lifetimes?
- Linux VFS Implementation:
  - Role of `struct dentry`, `struct inode`, `struct file`, and `/proc/<pid>/fd`:
- Filesystem-Specific Variations:
  - Do FAT, NTFS, or object stores use Unix inode numbers?
  - What core architectural principle is universal across all filesystems (decoupling naming from physical block storage)?

---

## G — User / Runtime Buffering Evidence
- Command Run: `python3 buffered_io_observer.py`
- Application Write Operations:
- Chunk Size per Write:
- Total Application Bytes Written:
- Stream Implementation Type (`io.BufferedWriter`):
- Default Buffer Size (`io.DEFAULT_BUFFER_SIZE`):
- Disk File Size before vs after `flush()`:
- Unbuffered Comparison via `os.write()`:
- Why do user runtimes batch writes into buffers before issuing system calls?

---

## H — Linux Page-Cache / Dirty Evidence + Limits
- Bounded Write Size (MiB):
- `/proc/meminfo` Dirty Before Write (kB):
- `/proc/meminfo` Dirty After Write (kB):
- `/proc/meminfo` Writeback (kB):
- Observed Dirty Delta (kB):
- Why is `/proc/meminfo` Dirty evidence directional and subject to system noise?
- Why does Essential CS forbid teaching a fixed delay or constant delta for page cache writeback?

---

## I — Live strace Evidence or Truthful NO LIVE SYSCALL TRACE
- strace Capability Status:
- If Capable:
  - Command: `strace -e trace=write -c python3 ...`
  - Total Application Writes:
  - Observed `write(2)` System Calls from strace summary:
  - Batching Ratio Confirmed:
- If Unavailable / Restricted:
  - Status: `SKIP`
  - Disposition: `NO LIVE SYSCALL TRACE`
  - Reason (e.g. strace not installed or ptrace blocked):
  - Confirmation: No synthetic or fabricated trace included.

---

## J — Write-Success vs Durability-Preview Boundary
- Machine-Checked Claim: Does ordinary `write()` success prove power-loss durability?
- Machine-Checked Claim: Does `f.close()` issue `fsync()` to force disk synchronization?
- Physical Risk: What happens to page cache dirty pages if power is lost before writeback?
- Durability Concept First Home Audit:
  - Canonical Concept ID: `EC-CON-016`
  - Primary First Home: M09 `L09-01`
  - Status in M08: Previewed only (distinguishing OS write acceptance from power-loss durability). No canonical definition established in M08.

---

## K — ENOENT Evidence
- Command Run: `python3 io_failure_fixture.py`
- Non-Existent Path Tested:
- Exception Caught (`FileNotFoundError`):
- Observed Errno Number & Name (e.g. `2`, `ENOENT`):
- Subsystem & Broken Invariant:

---

## L — Permission Evidence or Environment-Limited Disposition
- Process Privileges (`is_privileged_user()` / `os.geteuid()`):
- If Unprivileged:
  - Read-Only Mode Tested (`0444`):
  - Exception Caught (`PermissionError`):
  - Observed Errno Number & Name (e.g. `13`, `EACCES`):
- If Privileged (`root` / `uid 0`):
  - Disposition: `ENVIRONMENT-LIMITED`
  - Reason: Superuser processes possess `CAP_DAC_OVERRIDE` and bypass DAC mode bit checks. Live `EACCES` reproduction requires an unprivileged execution context.

---

## M — Bounded ENOSPC / Live-vs-Model Evidence
- Evidence Type: `DETERMINISTIC_MODEL_EVIDENCE`
- Abstraction Used: `BoundedSpaceWriter` (Course-owned in-memory model)
- Bounded Capacity Tested (bytes):
- Initial Write Bytes Accepted:
- Second Write Bytes Requested vs Accepted (Partial Write Demonstration):
- Subsequent Write Result:
- Observed Errno Number & Name (e.g. `28`, `ENOSPC`):
- Safety Confirmation: No host root filesystem filled; no raw block devices manipulated; host partition exhaustion strictly prevented.

---

## N — Cleanup / Safety / Fact-vs-Inference
- Reset Command: `python3 reset.py`
- Cleanup Verification: All temporary run directories, `.dat`, `.tmp`, and `__pycache__` artifacts removed.
- Host Safety: No root required, memory bounded, zero disk exhaustion risk.
- Fact vs Inference:
  - Direct Host Observations (Facts):
  - Inferences & Linux-Specific Implementation Details:

---

## O — Canonical Concept Audit
- Canonical Concepts Touched:
  - `EC-CON-005 Interface` (Revisit)
  - `EC-CON-004 Indirection` (Revisit)
  - `EC-CON-001 State` (Revisit)
  - `EC-CON-011 Caching` (Revisit)
  - `EC-CON-012 Locality` (Revisit)
  - `EC-CON-006 Trade-off` (Revisit)
  - `EC-CON-010 Failure` (Revisit)
  - `EC-CON-007 Specification` (Revisit)
  - `EC-CON-009 Correctness` (Revisit)
- Canonical Concept First Home:
  - `EC-CON-016 Durability` -> Preserved for M09 `L09-01` [AUDIT: CONFIRMED]
  - New Concept IDs Created: NONE [AUDIT: CONFIRMED]
