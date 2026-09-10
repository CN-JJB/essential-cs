#!/usr/bin/env bash
# Canonical environment version capture + D-032 floor gate.
# Runs INSIDE the candidate canonical Ubuntu 24.04 environment (or a Noble-class host
# for comparison). Prints a machine-readable snapshot, then enforces D-032 floors.
# Exit 0: snapshot printed and every REQUIRED floor/architecture condition met.
# Exit 3: snapshot printed but a REQUIRED condition is violated (fail-closed).
set -u

fail=0
floor_fail() { printf 'FLOOR FAIL %s\n' "$1"; fail=1; }
floor_pass() { printf 'FLOOR PASS %s\n' "$1"; }
version_ge() {
    # Numeric dotted versions used here are compared with GNU sort -V so future major
    # versions (for example Python 4.0 or curl 9.0) do not incorrectly fail a floor.
    [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -n 1)" = "$2" ]
}

printf 'CANONICAL_ENV_CAPTURE version=2\n'
printf 'os=%s\n' "$(cat /etc/os-release 2>/dev/null | grep '^PRETTY_NAME=' | cut -d= -f2 | tr -d '"')"
printf 'kernel=%s\n' "$(uname -r 2>/dev/null || echo unknown)"
ARCH=$(uname -m 2>/dev/null || echo unknown)
printf 'arch=%s\n' "$ARCH"
if [ "$ARCH" = "x86_64" ]; then
    floor_pass "canonical-arch=x86_64"
else
    floor_fail "canonical-arch=x86_64 (got $ARCH)"
fi

PY_IMPL=$(python3 -c "import platform; print(platform.python_implementation())" 2>/dev/null || echo missing)
PY_VER=$(python3 -c "import platform; print(platform.python_version())" 2>/dev/null || echo 0.0.0)
printf 'python_impl=%s\n' "$PY_IMPL"
printf 'python_version=%s\n' "$PY_VER"
if [ "$PY_IMPL" = "CPython" ] && version_ge "$PY_VER" "3.12"; then
    floor_pass "python>=3.12 ($PY_IMPL $PY_VER)"
else
    floor_fail "python>=3.12 (got $PY_IMPL $PY_VER)"
fi

EMBED_SQLITE=$(python3 -c "import sqlite3; print(sqlite3.sqlite_version)" 2>/dev/null || echo 0.0.0)
printf 'sqlite_embedded=%s\n' "$EMBED_SQLITE"
if version_ge "$EMBED_SQLITE" "3.45"; then
    floor_pass "sqlite-engine>=3.45 ($EMBED_SQLITE)"
else
    floor_fail "sqlite-engine>=3.45 (got $EMBED_SQLITE)"
fi

if command -v sqlite3 >/dev/null 2>&1; then
    CLI_VER=$(sqlite3 --version 2>/dev/null | awk '{print $1}')
    printf 'sqlite_cli=%s\n' "$CLI_VER"
    if version_ge "$CLI_VER" "3.45"; then
        floor_pass "sqlite3-cli>=3.45 ($CLI_VER)"
    else
        floor_fail "sqlite3-cli>=3.45 (got $CLI_VER)"
    fi
else
    printf 'sqlite_cli=missing\n'
    floor_fail "sqlite3-cli>=3.45 (binary missing; REQUIRED learner gate)"
fi

if command -v gcc >/dev/null 2>&1; then
    GCC_LINE=$(gcc --version 2>/dev/null | head -n 1)
    GCC_VER=$(printf '%s\n' "$GCC_LINE" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n 1)
    printf 'gcc=%s\n' "$GCC_VER"
    if version_ge "$GCC_VER" "13.0"; then
        floor_pass "gcc>=13 ($GCC_VER)"
    else
        floor_fail "gcc>=13 (got $GCC_VER)"
    fi
    if printf 'int main(void){return 0;}\n' | gcc -std=c11 -x c -o /dev/null - 2>/dev/null; then
        floor_pass "gcc-c11-surface"
    else
        floor_fail "gcc-c11-surface"
    fi
else
    printf 'gcc=missing\n'
    floor_fail "gcc>=13 (binary missing)"
fi

if command -v curl >/dev/null 2>&1; then
    CURL_VER=$(curl --version 2>/dev/null | head -n 1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n 1)
    printf 'curl=%s\n' "$CURL_VER"
    if version_ge "$CURL_VER" "8.5"; then
        floor_pass "curl>=8.5 ($CURL_VER)"
    else
        floor_fail "curl>=8.5 (got $CURL_VER)"
    fi
else
    printf 'curl=missing\n'
    floor_fail "curl>=8.5 (binary missing)"
fi

if command -v gdb >/dev/null 2>&1; then
    GDB_VER=$(gdb --version 2>/dev/null | head -n 1 | grep -oE '[0-9]+\.[0-9]+' | head -n 1)
    printf 'gdb=%s\n' "$GDB_VER"
    if version_ge "$GDB_VER" "15.0"; then
        floor_pass "gdb>=15.0 ($GDB_VER) REQUIRED-present"
    else
        floor_fail "gdb>=15.0 (got $GDB_VER; REQUIRED for canonical M03 evidence)"
    fi
else
    printf 'gdb=missing\n'
    floor_fail "gdb>=15.0 (binary missing; REQUIRED for canonical M03 evidence)"
fi

printf 'qemu_riscv=%s\n' "$(qemu-system-riscv64 --version 2>/dev/null | head -n 1 || echo missing)"
printf 'riscv_unknown_elf_gcc=%s\n' "$(riscv64-unknown-elf-gcc --version 2>/dev/null | head -n 1 || echo missing)"
printf 'riscv_gnu_gcc=%s\n' "$(riscv64-linux-gnu-gcc --version 2>/dev/null | head -n 1 || echo missing)"
printf 'binutils=%s\n' "$(objdump --version 2>/dev/null | head -n 1 || echo missing)"
printf 'git=%s\n' "$(git --version 2>/dev/null || echo missing)"
printf 'strace=%s\n' "$(command -v strace >/dev/null 2>&1 && echo present-capability-gated || echo missing-capability-gated)"
printf 'bash=%s\n' "$(bash --version 2>/dev/null | head -n 1)"

if command -v dpkg-query >/dev/null 2>&1; then
    QEMU_PKG=$(dpkg-query -W -f='${Version}' qemu-system-misc 2>/dev/null || echo missing)
    UNKNOWN_ELF_PKG=$(dpkg-query -W -f='${Version}' gcc-riscv64-unknown-elf 2>/dev/null || echo missing)
    RISCV_GNU_PKG=$(dpkg-query -W -f='${Version}' gcc-riscv64-linux-gnu 2>/dev/null || echo missing)
    printf 'qemu_system_misc_package=%s\n' "$QEMU_PKG"
    printf 'gcc_riscv64_unknown_elf_package=%s\n' "$UNKNOWN_ELF_PKG"
    printf 'gcc_riscv64_linux_gnu_package=%s\n' "$RISCV_GNU_PKG"
    [ "$QEMU_PKG" = "1:8.2.2+ds-0ubuntu1.18" ] \
      && floor_pass "qemu-system-misc exact package identity" \
      || floor_fail "qemu-system-misc exact package identity (got $QEMU_PKG)"
    [ "$UNKNOWN_ELF_PKG" = "13.2.0-11ubuntu1+12" ] \
      && floor_pass "gcc-riscv64-unknown-elf exact package identity" \
      || floor_fail "gcc-riscv64-unknown-elf exact package identity (got $UNKNOWN_ELF_PKG)"

    printf 'dpkg_lane_identities_BEGIN\n'
    dpkg -l qemu-system-misc qemu-system-common qemu-system-data gcc-riscv64-unknown-elf gcc-riscv64-linux-gnu binutils-riscv64-unknown-elf binutils-riscv64-linux-gnu gdb sqlite3 python3 curl git make binutils perl bc bash ca-certificates strace build-essential 2>/dev/null | grep '^ii' || true
    printf 'dpkg_lane_identities_END\n'
else
    floor_fail "dpkg-query missing; cannot verify canonical distro package identities"
fi

if [ "$fail" -eq 0 ]; then
    printf 'CANONICAL_ENV_CAPTURE result=PASS\n'
    exit 0
else
    printf 'CANONICAL_ENV_CAPTURE result=FLOOR_VIOLATION\n'
    exit 3
fi
