#!/usr/bin/env bash
# LAB-REQ-02 capability preflight. Does not install packages or weaken host security.
set -u

echo "=== LAB-REQ-02 xv6 Syscall Preflight ==="
STATUS="PASS"

check_cmd() {
    local label="$1"
    local cmd="$2"
    if command -v "${cmd}" >/dev/null 2>&1; then
        echo "[+] ${label}: $(${cmd} --version 2>/dev/null | head -n 1 || echo available)"
    else
        echo "[-] ${label}: NOT FOUND"
        STATUS="BLOCKED"
    fi
}

check_cmd "git" git
check_cmd "make" make
check_cmd "python3" python3
check_cmd "perl" perl
check_cmd "bc" bc

RISCV_GCC=""
RISCV_OBJDUMP=""
for prefix in riscv64-linux-gnu riscv64-unknown-elf; do
    if command -v "${prefix}-gcc" >/dev/null 2>&1 && command -v "${prefix}-objdump" >/dev/null 2>&1; then
        RISCV_GCC="${prefix}-gcc"
        RISCV_OBJDUMP="${prefix}-objdump"
        break
    fi
done

if [ -z "${RISCV_GCC}" ]; then
    echo "[-] RISC-V GCC + objdump pair: NOT FOUND"
    STATUS="BLOCKED"
else
    echo "[+] RISC-V GCC: $("${RISCV_GCC}" --version | head -n 1)"
    echo "[+] RISC-V objdump: $("${RISCV_OBJDUMP}" --version | head -n 1)"
fi

if command -v qemu-system-riscv64 >/dev/null 2>&1; then
    echo "[+] QEMU RISC-V: $(qemu-system-riscv64 --version | head -n 1)"
else
    echo "[-] QEMU RISC-V: NOT FOUND"
    STATUS="BLOCKED"
fi

echo "----------------------------------------"
if [ "${STATUS}" = "PASS" ]; then
    echo "STATUS: PASS — Required LAB-REQ-02 build/smoke capabilities are present."
    echo "NOTE: PASS means capability-present, not that xv6 build/QEMU execution has already succeeded."
    exit 0
fi

echo "STATUS: BLOCKED — One or more required build/smoke capabilities are missing."
echo "Source-route inspection may still be possible after setup, but it is not equivalent to runnable LAB completion."
exit 1
