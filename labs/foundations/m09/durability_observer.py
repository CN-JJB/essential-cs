#!/usr/bin/env python3
"""Durability, Synchronization Boundaries, and Latency Observer for M09 L09-01.

Demonstrates:
1. Canonical Definition (EC-CON-016 First Home):
   "A committed state survives a named restart or failure bound."
2. Bounded comparison between ordinary buffered writes and synchronized writes (os.fsync).
3. Machine-observable synchronization call counting and repeated raw sample timing.
4. File-data vs parent directory-metadata synchronization boundaries.
5. Invariant: Ordinary write/flush success does NOT establish power-loss durability.
   fsync latency depends on OS, filesystem, and storage device; no fixed ratio is universal.
"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path

# Machine-checked safety caps
MAX_SAFE_RECORDS = 500
MAX_SAFE_RECORD_SIZE = 1024
MAX_SAFE_TOTAL_BYTES = 64 * 1024


def get_canonical_durability_concept() -> dict:
    """Return the canonical definition and named failure bounds for EC-CON-016."""
    return {
        "concept_id": "EC-CON-016",
        "concept_name_en": "Durability",
        "concept_name_zh": "持久性",
        "first_home_module": "M09",
        "first_home_lesson": "L09-01",
        "canonical_definition": "A committed state survives a named restart or failure bound.",
        "named_failure_bounds": [
            "process_crash",
            "kernel_panic_os_crash",
            "clean_machine_restart",
            "sudden_power_loss",
            "storage_media_destruction",
        ],
        "checkpoint_flow": (
            "Application/Runtime Buffer? -> "
            "OS Buffered State (Page Cache)? -> "
            "Filesystem Data & Metadata Handling -> "
            "Device Volatile Cache? -> "
            "Non-Volatile Media"
        ),
    }


def validate_workload_bounds(num_records: int, record_size: int) -> None:
    """Ensure workload remains strictly bounded and safe for host storage."""
    if num_records <= 0 or record_size <= 0:
        raise ValueError("num_records and record_size must be positive integers")
    if num_records > MAX_SAFE_RECORDS:
        raise ValueError(f"num_records ({num_records}) exceeds MAX_SAFE_RECORDS ({MAX_SAFE_RECORDS})")
    if record_size > MAX_SAFE_RECORD_SIZE:
        raise ValueError(f"record_size ({record_size}) exceeds MAX_SAFE_RECORD_SIZE ({MAX_SAFE_RECORD_SIZE})")
    if (num_records * record_size) > MAX_SAFE_TOTAL_BYTES:
        raise ValueError(
            f"Total payload ({num_records * record_size} bytes) exceeds MAX_SAFE_TOTAL_BYTES ({MAX_SAFE_TOTAL_BYTES})"
        )


def measure_sync_vs_buffered(
    work_dir: str | Path | None = None,
    num_records: int = 50,
    record_size: int = 64,
    trials: int = 5,
) -> dict:
    """Measure raw latency samples comparing ordinary buffered writes with per-write fsync.

    Both modes write the exact same logical payload under identical record sizes.
    Repeated raw timing samples are recorded. No universal latency ratio is asserted.
    """
    validate_workload_bounds(num_records, record_size)
    if trials <= 0 or trials > 50:
        raise ValueError("trials must be between 1 and 50")

    cleanup_temp = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m09_durable_")
        work_path = Path(temp_obj.name)
        cleanup_temp = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    payload = b"D" * record_size
    total_expected_bytes = num_records * record_size

    buffered_samples_ns = []
    synced_samples_ns = []
    sync_calls_observed = 0

    try:
        # 1. Measure Ordinary Buffered Writes (no fsync)
        for t in range(trials):
            target_path = work_path / f"buffered_trial_{t}.dat"
            t0 = time.perf_counter_ns()
            with open(target_path, "wb") as f:
                for _ in range(num_records):
                    f.write(payload)
                f.flush()
            t1 = time.perf_counter_ns()
            buffered_samples_ns.append(t1 - t0)
            if target_path.stat().st_size != total_expected_bytes:
                raise RuntimeError("Buffered file size mismatch")

        # 2. Measure Synchronized Writes (os.fsync after each record)
        for t in range(trials):
            target_path = work_path / f"synced_trial_{t}.dat"
            t0 = time.perf_counter_ns()
            fd = os.open(target_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
            try:
                for _ in range(num_records):
                    written = 0
                    while written < record_size:
                        n = os.write(fd, payload[written:])
                        written += n
                    os.fsync(fd)
                    sync_calls_observed += 1
            finally:
                os.close(fd)
            t1 = time.perf_counter_ns()
            synced_samples_ns.append(t1 - t0)
            if target_path.stat().st_size != total_expected_bytes:
                raise RuntimeError("Synced file size mismatch")

    finally:
        if cleanup_temp and temp_obj is not None:
            temp_obj.cleanup()

    # Calculate basic summary statistics
    buf_mean_ms = (sum(buffered_samples_ns) / len(buffered_samples_ns)) / 1e6
    sync_mean_ms = (sum(synced_samples_ns) / len(synced_samples_ns)) / 1e6

    return {
        "num_records": num_records,
        "record_size_bytes": record_size,
        "total_logical_bytes": total_expected_bytes,
        "trials": trials,
        "buffered_samples_ns": buffered_samples_ns,
        "synced_samples_ns": synced_samples_ns,
        "buffered_mean_ms": round(buf_mean_ms, 4),
        "synced_mean_ms": round(sync_mean_ms, 4),
        "total_sync_calls_executed": sync_calls_observed,
        "expected_sync_calls": trials * num_records,
        "host_evidence_note": (
            "Observed raw timing reflects this specific host, kernel, filesystem, and device load. "
            "Essential CS strictly forbids asserting a universal latency ratio or claiming fsync "
            "must always be slower by a fixed constant factor."
        ),
    }


def demonstrate_file_and_directory_sync(work_dir: str | Path | None = None) -> dict:
    """Demonstrate Linux file-data vs parent-directory synchronization objects.

    A successful fsync(file_fd) does not necessarily synchronize the containing directory
    entry.  When a named failure model requires a newly created pathname to survive, Linux
    applications commonly fsync the containing directory as a separate step.  Rename across
    directories requires reasoning about both source and destination directories.
    """
    cleanup_temp = False
    if work_dir is None:
        temp_obj = tempfile.TemporaryDirectory(prefix="_run_m09_dirsync_")
        work_path = Path(temp_obj.name)
        cleanup_temp = True
    else:
        work_path = Path(work_dir)
        work_path.mkdir(parents=True, exist_ok=True)
        temp_obj = None

    file_path = work_path / "durable_new_file.txt"
    report = {
        "work_dir": str(work_path),
        "file_path": str(file_path),
        "file_data_synced": False,
        "parent_dir_synced": False,
        "parent_dir_sync_disposition": "NOT_ATTEMPTED",
    }

    try:
        # Step 1: Write file and sync file descriptor
        fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
        try:
            os.write(fd, b"Committed transactional entry\n")
            os.fsync(fd)
            report["file_data_synced"] = True
        finally:
            os.close(fd)

        # Step 2: Linux example: open and sync the containing directory.
        # Directory-fsync support is an OS/filesystem capability, not a universal POSIX promise.
        try:
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            dir_fd = os.open(work_path, flags)
            try:
                os.fsync(dir_fd)
                report["parent_dir_synced"] = True
                report["parent_dir_sync_disposition"] = "PASS"
            finally:
                os.close(dir_fd)
        except OSError as e:
            report["parent_dir_sync_disposition"] = "ENVIRONMENT_LIMITED"
            report["parent_dir_sync_error"] = str(e)

    finally:
        if cleanup_temp and temp_obj is not None:
            temp_obj.cleanup()

    return report


def main() -> int:
    print("=== Essential CS M09 — Durability Observer (L09-01) ===")
    concept = get_canonical_durability_concept()
    print(f"[1] Canonical Concept: {concept['concept_id']} {concept['concept_name_en']} ({concept['concept_name_zh']})")
    print(f"    First Home: {concept['first_home_module']} / {concept['first_home_lesson']}")
    print(f"    Definition: \"{concept['canonical_definition']}\"")
    print(f"    Named Bounds: {', '.join(concept['named_failure_bounds'])}")

    print("\n[2] Bounded Raw Latency Measurement (50 records x 64 B, 5 trials):")
    res = measure_sync_vs_buffered(num_records=50, record_size=64, trials=5)
    print(f"    -> Logical Payload: {res['total_logical_bytes']} bytes per trial")
    print(f"    -> Buffered Mean:   {res['buffered_mean_ms']} ms")
    print(f"    -> Synced Mean:     {res['synced_mean_ms']} ms")
    print(f"    -> Sync Calls Made: {res['total_sync_calls_executed']} (expected {res['expected_sync_calls']})")
    print(f"    -> Note: {res['host_evidence_note']}")

    print("\n[3] File vs Directory Metadata Synchronization:")
    dir_sync = demonstrate_file_and_directory_sync()
    print(f"    -> File data synced: {dir_sync['file_data_synced']}")
    print(f"    -> Parent dir synced: {dir_sync['parent_dir_synced']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
