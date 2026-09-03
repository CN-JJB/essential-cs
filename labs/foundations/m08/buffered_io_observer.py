#!/usr/bin/env python3
"""Buffered I/O, Page Cache, and Durability Boundary observer for M08 L08-02.

Demonstrates:
1. Four-layer write path: Runtime Buffer -> Syscall Boundary -> Kernel Page Cache -> Storage Device.
2. User-space write batching via buffered I/O vs raw unbuffered os.write().
3. Live strace capability detection with truthful SKIP / NO LIVE SYSCALL TRACE when unavailable.
4. Directional, noisy /proc/meminfo Dirty/Writeback observation on Linux without fixed constants.
5. Static claim-boundary audit: ordinary buffered write/flush success must not be labeled as power-loss durability evidence.
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


MAX_USER_BUFFER_DEMO_BYTES = 1024 * 1024  # 1 MiB hard cap
MAX_DIRTY_OBSERVATION_MB = 8


def observe_user_space_buffering(work_dir: str | Path | None = None, num_chunks: int = 1024, chunk_size: int = 16) -> dict:
    """Compare user-space runtime buffering with unbuffered system call writes."""
    if num_chunks <= 0 or chunk_size <= 0:
        raise ValueError("num_chunks and chunk_size must be positive")
    total_expected_bytes = num_chunks * chunk_size
    if total_expected_bytes > MAX_USER_BUFFER_DEMO_BYTES:
        raise ValueError(
            f"buffering demo exceeds the {MAX_USER_BUFFER_DEMO_BYTES}-byte safety cap"
        )

    cleanup = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m08_buf_")
        work_path = Path(temp_obj.name)
        cleanup = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    buf_file = work_path / "buffered.dat"
    unbuf_file = work_path / "unbuffered.dat"
    chunk = b"X" * chunk_size

    report = {
        "num_app_writes": num_chunks,
        "chunk_size_bytes": chunk_size,
        "total_app_bytes": total_expected_bytes,
        "default_buffer_size": io.DEFAULT_BUFFER_SIZE,
    }

    try:
        # Part A: Python buffered writer
        with open(buf_file, "wb") as f:
            bytes_written_app = 0
            for _ in range(num_chunks):
                bytes_written_app += f.write(chunk)
            # Before explicit flush or close, data may reside in Python's user-space buffer
            report["buffered_stream_type"] = type(f).__name__
            f.flush()

        actual_buf_size = os.path.getsize(buf_file)
        report["buffered_file_bytes_on_disk"] = actual_buf_size

        # Part B: Low-level unbuffered os.write
        fd = os.open(unbuf_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        unbuf_bytes = 0
        try:
            for _ in range(num_chunks):
                unbuf_bytes += os.write(fd, chunk)
        finally:
            os.close(fd)

        actual_unbuf_size = os.path.getsize(unbuf_file)
        report["unbuffered_file_bytes_on_disk"] = actual_unbuf_size

        # Invariant checks
        report["verifications"] = {
            "buffered_bytes_match": actual_buf_size == total_expected_bytes,
            "unbuffered_bytes_match": actual_unbuf_size == total_expected_bytes,
            "buffering_layer_present": report["buffered_stream_type"] == "BufferedWriter",
            "syscall_batching_proven_here": False,
        }

    finally:
        if cleanup and temp_obj is not None:
            temp_obj.cleanup()

    return report


def check_durability_boundary_claim() -> dict:
    """Audit curriculum claim discipline; this is not an empirical durability test."""
    # Static curriculum invariant:
    # ordinary buffered write()/runtime flush()/close success is insufficient evidence
    # for the M09 durability claim. fsync/fdatasync are synchronization interfaces whose
    # exact failure-model guarantee is intentionally deferred to M09.
    durability_proven_by_ordinary_write = False
    return {
        "durability_proven_by_ordinary_write": durability_proven_by_ordinary_write,
        "canonical_home_module": "M09",
        "canonical_home_lesson": "L09-01",
        "canonical_concept_id": "EC-CON-016",
        "statement": "Ordinary buffered write()/runtime flush()/close success is insufficient to establish the M09 durability claim.",
        "durability_check_passed": (durability_proven_by_ordinary_write is False),
    }


def read_proc_meminfo() -> dict:
    """Read Linux /proc/meminfo Dirty and Writeback metrics."""
    meminfo_path = Path("/proc/meminfo")
    if not (meminfo_path.exists() and os.access(meminfo_path, os.R_OK)):
        return {"available": False, "dirty_kb": None, "writeback_kb": None}

    dirty_kb = None
    writeback_kb = None
    try:
        with open(meminfo_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Dirty:"):
                    parts = line.split()
                    dirty_kb = int(parts[1])
                elif line.startswith("Writeback:"):
                    parts = line.split()
                    writeback_kb = int(parts[1])
        return {
            "available": True,
            "dirty_kb": dirty_kb,
            "writeback_kb": writeback_kb,
        }
    except (OSError, ValueError, IndexError) as e:
        return {"available": False, "error": str(e), "dirty_kb": None, "writeback_kb": None}


def observe_dirty_pages_directional(work_dir: str | Path | None = None, size_mb: int = 8) -> dict:
    """Bounded, safe observation of Linux /proc/meminfo Dirty counter before and after writes."""
    if not isinstance(size_mb, int) or size_mb < 1 or size_mb > MAX_DIRTY_OBSERVATION_MB:
        raise ValueError(
            f"size_mb must be an integer from 1 to {MAX_DIRTY_OBSERVATION_MB}"
        )
    mem_before = read_proc_meminfo()
    if not mem_before["available"]:
        return {
            "status": "SKIP",
            "reason": "/proc/meminfo not available or unreadable on this host",
            "meminfo_available": False,
        }

    cleanup = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m08_dirty_")
        work_path = Path(temp_obj.name)
        cleanup = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    target_file = work_path / "dirty_test.dat"
    block_size = 64 * 1024  # 64 KiB blocks
    total_bytes = size_mb * 1024 * 1024
    payload = b"D" * block_size

    try:
        # Write bounded test file without fsync
        with open(target_file, "wb") as f:
            written = 0
            while written < total_bytes:
                f.write(payload)
                written += block_size
            f.flush()

        mem_after = read_proc_meminfo()

        # Capture values
        d_before = mem_before["dirty_kb"]
        d_after = mem_after["dirty_kb"]
        delta = (d_after - d_before) if (d_before is not None and d_after is not None) else None

        return {
            "status": "PASS",
            "meminfo_available": True,
            "size_written_mb": size_mb,
            "dirty_before_kb": d_before,
            "dirty_after_kb": d_after,
            "dirty_delta_kb": delta,
            "interpretation": "Directional Linux system-global observation. Dirty/Writeback counters are noisy and cannot prove that this process's exact bytes are still resident, nor establish a fixed writeback delay.",
        }
    finally:
        if cleanup and temp_obj is not None:
            temp_obj.cleanup()


def check_strace_capability() -> dict:
    """Check if strace is installed and able to trace unprivileged child processes."""
    strace_bin = shutil.which("strace")
    if not strace_bin:
        return {
            "status": "MISSING",
            "disposition": "NO LIVE SYSCALL TRACE",
            "reason": "strace binary not found in PATH",
        }

    try:
        res = subprocess.run(
            [strace_bin, "true"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if res.returncode == 0:
            return {
                "status": "PASS",
                "disposition": "CAPABLE",
                "path": strace_bin,
            }
        else:
            return {
                "status": "RESTRICTED",
                "disposition": "NO LIVE SYSCALL TRACE",
                "reason": f"strace execution failed with return code {res.returncode}: {res.stderr.strip()}",
            }
    except Exception as e:
        return {
            "status": "ERROR",
            "disposition": "NO LIVE SYSCALL TRACE",
            "reason": str(e),
        }


def trace_buffered_syscalls(work_dir: str | Path | None = None) -> dict:
    """Trace buffered write syscall batching if strace is available, else truthfully SKIP."""
    cap = check_strace_capability()
    if cap["status"] != "PASS":
        return {
            "status": "SKIP",
            "disposition": "NO LIVE SYSCALL TRACE",
            "reason": cap["disposition"],
            "detail": cap.get("reason", "strace not functional"),
        }

    cleanup = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m08_strace_")
        work_path = Path(temp_obj.name)
        cleanup = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    script_path = work_path / "_worker.py"
    target_path = work_path / "_out.dat"

    # Worker executes 1000 small 16-byte writes
    worker_code = f"""
import sys
with open(r"{target_path}", "wb") as f:
    for _ in range(1000):
        f.write(b"0123456789abcdef")
"""
    script_path.write_text(worker_code, encoding="utf-8")

    try:
        cmd = [
            "strace",
            "-e", "trace=write",
            "-c",
            sys.executable,
            str(script_path),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        # Parse summary table from strace -c
        write_calls = None
        for line in res.stderr.splitlines():
            if "write" in line:
                parts = line.split()
                try:
                    # strace -c columns: % time, seconds, usecs/call, calls, errors, syscall
                    # find the integer corresponding to call count
                    for part in parts:
                        if part.isdigit():
                            write_calls = int(part)
                            break
                except ValueError:
                    pass

        return {
            "status": "PASS",
            "app_writes": 1000,
            "strace_summary": res.stderr.strip(),
            "detected_write_syscalls": write_calls,
            "batched_relation_confirmed": (write_calls is not None and write_calls < 1000),
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "disposition": "NO LIVE SYSCALL TRACE",
            "error": str(e),
        }
    finally:
        if cleanup and temp_obj is not None:
            temp_obj.cleanup()


def main() -> int:
    print("=== Essential CS M08 — Buffered I/O & Page Cache Observer ===")

    # 1. User space buffering
    b_rep = observe_user_space_buffering()
    print(f"[1] User-Space Buffering Demonstration:")
    print(f"    -> Application write calls: {b_rep['num_app_writes']} x {b_rep['chunk_size_bytes']} bytes")
    print(f"    -> Python stream type: {b_rep['buffered_stream_type']}")
    print(f"    -> Default buffer size: {b_rep['default_buffer_size']} bytes")
    print(f"    -> Buffered file size: {b_rep['buffered_file_bytes_on_disk']} bytes")
    print(f"    -> Unbuffered file size: {b_rep['unbuffered_file_bytes_on_disk']} bytes")

    # 2. Strace live trace capability check
    s_rep = trace_buffered_syscalls()
    print(f"[2] Live Syscall Trace Check:")
    if s_rep["status"] == "PASS":
        print(f"    -> strace verified: 1000 app writes -> {s_rep['detected_write_syscalls']} kernel write() syscalls")
    else:
        print(f"    -> Result: {s_rep['disposition']} ({s_rep.get('detail', s_rep.get('reason'))})")

    # 3. Kernel Page Cache Dirty pages
    d_rep = observe_dirty_pages_directional()
    print(f"[3] Linux Page Cache (Dirty Pages) Observation:")
    if d_rep["status"] == "PASS":
        print(f"    -> Bounded payload: {d_rep['size_written_mb']} MiB")
        print(f"    -> Dirty before: {d_rep['dirty_before_kb']} kB")
        print(f"    -> Dirty after:  {d_rep['dirty_after_kb']} kB")
        print(f"    -> Delta:        {d_rep['dirty_delta_kb']} kB (system-global, noisy)")
    else:
        print(f"    -> Result: {d_rep['status']} ({d_rep.get('reason')})")

    # 4. Durability boundary
    dur = check_durability_boundary_claim()
    print(f"[4] Durability Boundary Audit:")
    print(f"    -> Ordinary write success proves durability: {dur['durability_proven_by_ordinary_write']}")
    print(f"    -> Audit status: {'PASS' if dur['durability_check_passed'] else 'FAIL'}")
    print(f"    -> Note: Canonical Durability first home is {dur['canonical_home_module']} ({dur['canonical_home_lesson']}).")

    all_ok = b_rep["verifications"]["buffered_bytes_match"] and dur["durability_check_passed"]
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
