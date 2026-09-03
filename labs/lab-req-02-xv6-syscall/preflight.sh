#!/usr/bin/env bash
# labs/lab-req-02-xv6-syscall/preflight.sh
# Verifies toolchain availability for LAB-REQ-02.

set -u

echo "=== LAB-REQ-02 xv6 Syscall Preflight ==="

TOOLCHAIN_STATUS="PASS"

# Check Git
if ! command -v git >/dev/null 2>&1; then
    echo "[-] git: NOT FOUND"
    TOOLCHAIN_STATUS="BLOCKED"
else
    echo "[+] git: $(git --version)"
fi

# Check RISC-V GCC
RISCV_GCC=""
for candidate in riscv64-linux-gnu-gcc riscv64-unknown-elf-gcc; do
    if command -v "${candidate}" >/dev/null 2>&1; then
        RISCV_GCC="${candidate}"
        break
    fi
done

if [ -z "${RISCV_GCC}" ]; then
    echo "[-] riscv64-gcc: NOT FOUND"
    TOOLCHAIN_STATUS="BLOCKED"
else
    echo "[+] riscv64-gcc: $("${RISCV_GCC}" --version | head -n 1)"
fi

# Check QEMU
if ! command -v qemu-system-riscv64 >/dev/null 2>&1; then
    echo "[-] qemu-system-riscv64: NOT FOUND"
    TOOLCHAIN_STATUS="BLOCKED"
else
    echo "[+] qemu-system-riscv64: $(qemu-system-riscv64 --version | head -n 1)"
fi

echo "----------------------------------------"
if [ "${TOOLCHAIN_STATUS}" = "PASS" ]; then
    echo "STATUS: PASS — Environment is capable of compiling and running xv6 in QEMU."
    exit 0
else
    echo "STATUS: BLOCKED — Missing required cross-toolchain or emulator."
    echo "        You may still perform static source-route inspection via verify_source_route.py,"
    echo "        and study fallback_trace.md for deterministic execution evidence."
    exit 1
fi
