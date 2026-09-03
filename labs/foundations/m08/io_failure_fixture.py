#!/usr/bin/env python3
"""POSIX File I/O failure reproduction, capability gating, and diagnostic triage for M08 L08-03.

Demonstrates:
1. Deterministic ENOENT reproduction via non-existent path resolution failure.
2. Behavior-gated EACCES handling:
   - The tool probes a temporary course-owned 0444 file.
   - PermissionError/EACCES is recorded only when actually reproduced.
   - A successful overwrite is truthfully labeled SKIP / ENVIRONMENT-LIMITED.
   - euid==0 is diagnostic metadata, not a capability proof in container/user namespaces.
3. Safe, host-bounded ENOSPC modeling via a course-owned capacity abstraction:
   - Demonstrates POSIX partial-write semantics.
   - Strictly forbids and avoids host disk/partition exhaustion.
   - Labeled explicitly as DETERMINISTIC MODEL EVIDENCE.
4. Error classification diagnostic triage matching symptoms, error codes, and subsystems.
"""

import errno
import json
import os
import stat
import sys
import tempfile
import uuid
from pathlib import Path


def reproduce_enoent(work_dir: str | Path | None = None) -> dict:
    """Deterministically reproduce ENOENT by attempting to open a non-existent path without O_CREAT."""
    cleanup = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m08_enoent_")
        work_path = Path(temp_obj.name)
        cleanup = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    non_existent = work_path / f"absent_file_{uuid.uuid4().hex[:8]}.txt"
    report = {
        "target_path": str(non_existent),
        "path_existed_before": non_existent.exists(),
    }

    try:
        with open(non_existent, "r", encoding="utf-8") as f:
            f.read()
        report["status"] = "UNEXPECTED_SUCCESS"
    except FileNotFoundError as e:
        report["status"] = "PASS"
        report["exception_type"] = type(e).__name__
        report["errno"] = e.errno
        report["errno_name"] = errno.errorcode.get(e.errno, "UNKNOWN")
        report["message"] = str(e)
        report["broken_invariant"] = "Path lookup invariant: directory entry lookup failed to find target pathname."
    except Exception as e:
        report["status"] = "UNEXPECTED_EXCEPTION"
        report["exception_type"] = type(e).__name__
        report["error"] = str(e)
    finally:
        if cleanup and temp_obj is not None:
            temp_obj.cleanup()

    return report


def is_privileged_user() -> bool:
    """Return whether effective UID is 0.

    This is diagnostic metadata only. In Linux containers/user namespaces, euid==0
    is not by itself proof that CAP_DAC_OVERRIDE is effective for a particular file.
    """
    if hasattr(os, "geteuid"):
        return os.geteuid() == 0
    return False


def reproduce_eacces(work_dir: str | Path | None = None) -> dict:
    """Probe the actual 0444 write result and classify it truthfully.

    The fixture is course-owned and temporary. A successful overwrite means this
    environment bypassed the mode-bit denial for this file, so live EACCES evidence
    is ENVIRONMENT-LIMITED. PermissionError/EACCES is recorded only when reproduced.
    """
    cleanup = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m08_eacces_")
        work_path = Path(temp_obj.name)
        cleanup = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    ro_file = work_path / "readonly_test.txt"
    report = {
        "target_path": str(ro_file),
        "euid": os.geteuid() if hasattr(os, "geteuid") else None,
        "euid_is_zero": is_privileged_user(),
    }

    try:
        # Create file and mark read-only (0o444)
        ro_file.write_text("read-only fixture content\n", encoding="utf-8")
        os.chmod(ro_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        try:
            with open(ro_file, "w", encoding="utf-8") as f:
                f.write("capability-or-environment-bypassed-mode-bits\n")
            report["status"] = "SKIP"
            report["disposition"] = "ENVIRONMENT-LIMITED"
            report["mode_bit_denial_bypassed"] = True
            report["reason"] = (
                "This process successfully overwrote the course-owned 0444 fixture. "
                "Therefore this environment cannot provide live EACCES evidence from "
                "mode bits alone. On Linux this can occur when the process has effective "
                "CAP_DAC_OVERRIDE for the file (often, but not universally, in root contexts). "
                "Container/user-namespace root must not be inferred from euid==0 alone."
            )
        except PermissionError as e:
            report["status"] = "PASS"
            report["disposition"] = "REPRODUCED"
            report["mode_bit_denial_bypassed"] = False
            report["exception_type"] = type(e).__name__
            report["errno"] = e.errno
            report["errno_name"] = errno.errorcode.get(e.errno, "UNKNOWN")
            report["message"] = str(e)
            report["broken_invariant"] = "Discretionary Access Control (DAC) invariant: requested write access denied by inode mode bits."
        finally:
            # Restore write permission so cleanup can remove it cleanly
            try:
                os.chmod(ro_file, stat.S_IRUSR | stat.S_IWUSR)
            except OSError:
                pass
    finally:
        if cleanup and temp_obj is not None:
            temp_obj.cleanup()

    return report


MAX_MODEL_CAPACITY_BYTES = 1024 * 1024  # 1 MiB hard safety cap


class BoundedSpaceWriter:
    """Course-owned bounded capacity abstraction modeling storage exhaustion safely.

    Simulates block device capacity limits and exposes POSIX partial write behavior
    without modifying, mounting, or risking host filesystem exhaustion.
    """

    def __init__(self, capacity_bytes: int = 512):
        if capacity_bytes <= 0:
            raise ValueError("capacity_bytes must be strictly positive")
        if capacity_bytes > MAX_MODEL_CAPACITY_BYTES:
            raise ValueError(
                f"capacity_bytes exceeds the {MAX_MODEL_CAPACITY_BYTES}-byte course safety cap"
            )
        self.capacity_bytes = capacity_bytes
        self.bytes_written = 0
        self.storage_buffer = bytearray()

    @property
    def remaining_bytes(self) -> int:
        return max(0, self.capacity_bytes - self.bytes_written)

    def write_raw(self, chunk: bytes) -> int:
        """Low-level write mimicking POSIX write(2) semantics.

        Returns number of bytes accepted. May perform a partial write if space
        is insufficient for the entire chunk. Raises ENOSPC when no space remains.
        """
        if self.remaining_bytes == 0:
            raise OSError(errno.ENOSPC, os.strerror(errno.ENOSPC))

        acceptable = min(len(chunk), self.remaining_bytes)
        self.storage_buffer.extend(chunk[:acceptable])
        self.bytes_written += acceptable
        return acceptable

    def write_high_level(self, chunk: bytes) -> int:
        """High-level write mimicking language buffered write loops.

        Attempts to push all bytes. If space exhausts mid-write, records partial bytes
        and raises OSError with errno.ENOSPC.
        """
        total_pushed = 0
        while total_pushed < len(chunk):
            slice_to_write = chunk[total_pushed:]
            try:
                n = self.write_raw(slice_to_write)
                total_pushed += n
            except OSError as e:
                if e.errno == errno.ENOSPC:
                    # In a high-level API, partial data was written before exception
                    raise OSError(
                        errno.ENOSPC,
                        f"{os.strerror(errno.ENOSPC)} (partial write: {total_pushed}/{len(chunk)} bytes accepted)",
                    ) from e
                raise
        return total_pushed


def reproduce_bounded_enospc(capacity_bytes: int = 512) -> dict:
    """Demonstrate one deterministic, POSIX-compatible partial-write/ENOSPC model.

    This is model evidence, not a claim that every real filesystem must return the
    same partial-write sequence.
    """
    device = BoundedSpaceWriter(capacity_bytes=capacity_bytes)

    # Phase 1: Write first chunk (consumes 75% of capacity)
    chunk1_size = int(capacity_bytes * 0.75)
    chunk1 = b"A" * chunk1_size
    n1 = device.write_raw(chunk1)

    # Phase 2: Attempt to write second chunk exceeding remaining capacity
    chunk2_size = int(capacity_bytes * 0.50)
    chunk2 = b"B" * chunk2_size
    space_before_chunk2 = device.remaining_bytes

    # Observe raw partial write
    partial_bytes = device.write_raw(chunk2)

    # Phase 3: Device is now 100% full; next write raises ENOSPC
    enospc_raised = False
    observed_errno = None
    try:
        device.write_raw(b"C")
    except OSError as e:
        enospc_raised = True
        observed_errno = e.errno

    return {
        "status": "PASS",
        "evidence_type": "DETERMINISTIC_MODEL_EVIDENCE",
        "host_safety_guarantee": "No host filesystem capacity is consumed by this ENOSPC model; in-memory capacity is hard-capped at 1 MiB",
        "capacity_bytes": capacity_bytes,
        "chunk1_requested": chunk1_size,
        "chunk1_accepted": n1,
        "space_before_chunk2": space_before_chunk2,
        "chunk2_requested": chunk2_size,
        "chunk2_partial_accepted": partial_bytes,
        "partial_write_occurred": (partial_bytes < chunk2_size),
        "total_bytes_stored": device.bytes_written,
        "enospc_raised_when_full": enospc_raised,
        "observed_errno": observed_errno,
        "errno_name": errno.errorcode.get(observed_errno, "UNKNOWN") if observed_errno else None,
        "broken_invariant": "Storage capacity invariant: available block allocation pool exhausted.",
    }


def classify_io_failure(code_or_exc: int | Exception) -> dict:
    """Triage file I/O failure into subsystem cause and recommended diagnostic action."""
    if isinstance(code_or_exc, int):
        err = code_or_exc
    elif hasattr(code_or_exc, "errno") and code_or_exc.errno is not None:
        err = code_or_exc.errno
    else:
        err = getattr(errno, str(code_or_exc), None)

    tax = {
        errno.ENOENT: {
            "name": "ENOENT",
            "errno": errno.ENOENT,
            "subsystem": "VFS / Directory Naming",
            "invariant": "Target pathname dentry must exist in directory structure unless O_CREAT is specified.",
            "diagnostic_steps": "Check path spelling, verify working directory (os.getcwd()), ensure parent directories exist.",
        },
        errno.EACCES: {
            "name": "EACCES",
            "errno": errno.EACCES,
            "subsystem": "VFS / Security & DAC",
            "invariant": "Process credentials must satisfy file/directory permission mode bits (rwx) and mount options.",
            "diagnostic_steps": "Inspect ls -l permissions, check file ownership (UID/GID), verify parent directory execute bits, check if process is root.",
        },
        errno.ENOSPC: {
            "name": "ENOSPC",
            "errno": errno.ENOSPC,
            "subsystem": "Block Allocation / Filesystem Capacity",
            "invariant": "Filesystem must have sufficient free data blocks AND free inode slots to allocate.",
            "diagnostic_steps": "Check df -h (data block capacity) AND df -i (inode count capacity); identify unlinked files held open by active processes.",
        },
        errno.EBADF: {
            "name": "EBADF",
            "errno": errno.EBADF,
            "subsystem": "Process File Descriptor Table",
            "invariant": "The requested integer file descriptor must correspond to an active open file description.",
            "diagnostic_steps": "Check for double-close, inspect descriptor lifecycle, verify descriptor is not used after close().",
        },
        errno.EROFS: {
            "name": "EROFS",
            "errno": errno.EROFS,
            "subsystem": "Mount / VFS Policy",
            "invariant": "Filesystem must be mounted with write privileges to accept modifications.",
            "diagnostic_steps": "Check mount options with findmnt or mount; verify underlying volume is not write-protected.",
        },
    }

    return tax.get(
        err,
        {
            "name": errno.errorcode.get(err, "UNKNOWN"),
            "errno": err,
            "subsystem": "General POSIX I/O",
            "invariant": "Operating system invariant violated.",
            "diagnostic_steps": f"Consult man 2 intro or errno manual for code {err}.",
        },
    )


def main() -> int:
    print("=== Essential CS M08 — File I/O Failure Fixture & Diagnostic Triage ===")

    # 1. ENOENT
    enoent_res = reproduce_enoent()
    print(f"[1] Deterministic ENOENT Reproduction:")
    print(f"    -> Status: {enoent_res['status']}")
    print(f"    -> Errno: {enoent_res.get('errno')} ({enoent_res.get('errno_name')})")
    print(f"    -> Invariant: {enoent_res.get('broken_invariant')}")

    # 2. EACCES
    eacces_res = reproduce_eacces()
    print(f"[2] Capability-Gated EACCES Handling:")
    print(f"    -> Status: {eacces_res['status']} ({eacces_res.get('disposition')})")
    if eacces_res["status"] == "SKIP":
        print(f"    -> Reason: {eacces_res.get('reason')}")
    else:
        print(f"    -> Errno: {eacces_res.get('errno')} ({eacces_res.get('errno_name')})")

    # 3. Safe Bounded ENOSPC
    enospc_res = reproduce_bounded_enospc(capacity_bytes=512)
    print(f"[3] Bounded Safe ENOSPC & Partial Write Model:")
    print(f"    -> Evidence Type: {enospc_res['evidence_type']}")
    print(f"    -> Capacity: {enospc_res['capacity_bytes']} bytes")
    print(f"    -> Chunk 1 accepted: {enospc_res['chunk1_accepted']} bytes")
    print(f"    -> Chunk 2 requested: {enospc_res['chunk2_requested']} bytes, accepted: {enospc_res['chunk2_partial_accepted']} bytes (Partial Write!)")
    print(f"    -> Subsequent write raised ENOSPC: {enospc_res['enospc_raised_when_full']} (errno={enospc_res['observed_errno']})")
    print(f"    -> Host safety: {enospc_res['host_safety_guarantee']}")

    # 4. Diagnostic Triage Example
    triage = classify_io_failure(errno.ENOSPC)
    print(f"[4] Diagnostic Triage Mapping Sample:")
    print(f"    -> Code: {triage['name']} ({triage['errno']}) | Subsystem: {triage['subsystem']}")
    print(f"    -> Invariant: {triage['invariant']}")
    print(f"    -> Triage: {triage['diagnostic_steps']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
