#!/usr/bin/env python3
"""fault_runner.py - Essential CS M07 Safe Memory Fault Observation Runner.

Compiles and safely executes bad_address.c as a bounded child process,
recording actual hosted process termination, signal delivery, and environment
details without relying on shell-specific exit 139 conventions.

Educational Invariant:
- Invalid memory access in C is Undefined Behavior (UB) at the language layer.
- The C standard does NOT guarantee SIGSEGV or any particular signal.
- The observed SIGSEGV is a hosted observation produced by the CPU MMU
  hardware trap and Linux kernel page fault handler.
"""

from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


SCRIPT_DIR = Path(__file__).resolve().parent
C_SOURCE_PATH = SCRIPT_DIR / "bad_address.c"
BINARY_PATH = SCRIPT_DIR / "bad_address"
DEFAULT_TIMEOUT_SEC = 5.0


@dataclass
class CompilerInfo:
    compiler_path: str
    version_str: str


@dataclass
class FaultRunResult:
    compiled: bool
    compiler_info: Optional[CompilerInfo]
    binary_path: str
    returncode: int
    terminated_by_signal: bool
    signal_number: Optional[int]
    signal_name: Optional[str]
    timed_out: bool
    stdout: str
    stderr: str


def find_native_compiler() -> Optional[CompilerInfo]:
    """Finds an available native C compiler (gcc or clang)."""
    candidates = ["gcc", "clang", "cc"]
    for cand in candidates:
        cand_path = shutil.which(cand)
        if cand_path:
            try:
                proc = subprocess.run(
                    [cand_path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5.0,
                    check=False,
                )
                version_line = proc.stdout.splitlines()[0] if proc.stdout else "unknown version"
                return CompilerInfo(compiler_path=cand_path, version_str=version_line)
            except Exception:
                continue
    return None


def compile_fixture(compiler: str, source: Path, output: Path) -> subprocess.CompletedProcess:
    """Compiles the bad_address C fixture under strict warning flags."""
    cmd = [compiler, "-O0", "-Wall", "-Wextra", "-o", str(output), str(source)]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=10.0,
        check=False,
    )


def run_fault_child(
    binary: Path, timeout: float = DEFAULT_TIMEOUT_SEC
) -> FaultRunResult:
    """Runs the compiled binary in a bounded child process and captures results."""
    compiler_info = find_native_compiler()
    if not compiler_info:
        raise RuntimeError("No native C compiler found to compile fixture.")

    if not binary.exists():
        comp_res = compile_fixture(compiler_info.compiler_path, C_SOURCE_PATH, binary)
        if comp_res.returncode != 0:
            return FaultRunResult(
                compiled=False,
                compiler_info=compiler_info,
                binary_path=str(binary),
                returncode=comp_res.returncode,
                terminated_by_signal=False,
                signal_number=None,
                signal_name=None,
                timed_out=False,
                stdout=comp_res.stdout,
                stderr=comp_res.stderr,
            )

    # Execute child under timeout
    timed_out = False
    try:
        proc = subprocess.run(
            [str(binary)],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        rc = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        rc = -1
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""

    # Decode signal semantics:
    # In Python subprocess on POSIX, a negative returncode -N means terminated by signal N
    terminated_by_signal = False
    sig_num = None
    sig_name = None

    if rc < 0:
        terminated_by_signal = True
        sig_num = -rc
        try:
            sig_name = signal.Signals(sig_num).name
        except ValueError:
            sig_name = f"SIGNAL_{sig_num}"

    return FaultRunResult(
        compiled=True,
        compiler_info=compiler_info,
        binary_path=str(binary),
        returncode=rc,
        terminated_by_signal=terminated_by_signal,
        signal_number=sig_num,
        signal_name=sig_name,
        timed_out=timed_out,
        stdout=stdout,
        stderr=stderr,
    )


def cleanup_binary(binary: Path = BINARY_PATH) -> None:
    """Removes compiled binary artifacts."""
    if binary.exists():
        try:
            binary.unlink()
        except OSError:
            pass


def main() -> int:
    print("=== M07 Safe Memory Fault Observation Runner ===")
    print(f"Platform: {sys.platform}")
    print(f"Parent Process PID: {os.getpid()}")

    compiler_info = find_native_compiler()
    if not compiler_info:
        print("ERROR: No native C compiler (gcc/clang) found.")
        print("A native compiler is required to compile bad_address.c.")
        return 1

    print(f"Compiler: {compiler_info.compiler_path}")
    print(f"Compiler Version: {compiler_info.version_str}")
    print(f"Compiling fixture: {C_SOURCE_PATH.name} -> {BINARY_PATH.name}")

    comp_res = compile_fixture(compiler_info.compiler_path, C_SOURCE_PATH, BINARY_PATH)
    if comp_res.returncode != 0:
        print(f"Compilation failed with exit code {comp_res.returncode}:")
        print(comp_res.stderr)
        return 1
    print("Compilation succeeded (-O0 -Wall -Wextra).")

    print(f"\nExecuting child process under bounded timeout ({DEFAULT_TIMEOUT_SEC}s)...")
    result = run_fault_child(BINARY_PATH, timeout=DEFAULT_TIMEOUT_SEC)

    print("\n--- Hosted Observation Results ---")
    print(f"Raw Subprocess Returncode: {result.returncode}")
    print(f"Terminated by Signal: {result.terminated_by_signal}")
    if result.terminated_by_signal:
        print(f"Observed Signal Number: {result.signal_number}")
        print(f"Observed Signal Name: {result.signal_name}")
    print(f"Timed Out: {result.timed_out}")

    print("\n--- Architectural Layer Separation ---")
    print("1. C Language Specification Layer (ISO/IEC 9899):")
    print("   Dereferencing a null/bad pointer is UNDEFINED BEHAVIOR (UB).")
    print("   The C language standard guarantees NOTHING (no signal, no exit status).")
    print("2. CPU / MMU Hardware Layer:")
    print("   Attempted access to unmapped address 0x0 triggers a Page Fault exception.")
    print("3. Operating System Kernel Layer (Linux):")
    print("   Page fault handler detects invalid access and sends SIGSEGV to the process.")
    print("4. Shell / Environment Representation:")
    print("   Shells (like bash) often report 128 + Signal = 139, but this is a shell convention,")
    print("   not a universal operating system exit status.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
