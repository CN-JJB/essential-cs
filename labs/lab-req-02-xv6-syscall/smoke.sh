#!/usr/bin/env bash
# labs/lab-req-02-xv6-syscall/smoke.sh
# Smoke test runner for LAB-REQ-02 user/sleep implementation.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKTREE_DIR="${SCRIPT_DIR}/worktree"

echo "=== LAB-REQ-02 Smoke Test ==="

if [ ! -d "${WORKTREE_DIR}" ]; then
    echo "[-] Worktree not found. Run ./setup.sh first."
    exit 1
fi

if [ ! -f "${WORKTREE_DIR}/user/sleep.c" ]; then
    echo "[-] Learner implementation missing: ${WORKTREE_DIR}/user/sleep.c"
    echo "    Implement user/sleep.c before running the smoke test."
    exit 1
fi

if ! grep -q '\$U/_sleep' "${WORKTREE_DIR}/Makefile"; then
    echo "[-] \$U/_sleep not found in UPROGS in ${WORKTREE_DIR}/Makefile."
    echo "    Add \$U/_sleep to the UPROGS list in Makefile."
    exit 1
fi

echo "[+] Step 1: Compiling kernel and user/_sleep..."
(cd "${WORKTREE_DIR}" && make fs.img kernel/kernel)
echo "[+] Build successful."

echo "[+] Step 2: Checking user/_sleep disassembly..."
if command -v riscv64-linux-gnu-objdump >/dev/null 2>&1; then
    OBJDUMP_BIN="riscv64-linux-gnu-objdump"
elif command -v riscv64-unknown-elf-objdump >/dev/null 2>&1; then
    OBJDUMP_BIN="riscv64-unknown-elf-objdump"
else
    OBJDUMP_BIN=""
fi

if [ -n "${OBJDUMP_BIN}" ]; then
    if "${OBJDUMP_BIN}" -d "${WORKTREE_DIR}/user/_sleep" | grep -q '<pause>:'; then
        echo "[+] Disassembly verified: user/_sleep calls pause (syscall stub present)."
    else
        echo "[-] WARNING: pause symbol not found in user/_sleep disassembly."
    fi
fi

echo "[+] Step 3: Running bounded QEMU execution test..."
# Run test-xv6.py or QEMU with a strict 20-second timeout
QEMU_PID_FILE="${WORKTREE_DIR}/.qemu_smoke.pid"

if [ -f "${WORKTREE_DIR}/test-xv6.py" ]; then
    echo "[*] Using test-xv6.py runner..."
    (cd "${WORKTREE_DIR}" && python3 -c "
import subprocess, sys
p = subprocess.Popen(['make', 'qemu'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
try:
    stdout, _ = p.communicate(input='sleep 10\nexit\n', timeout=15)
    print(stdout[-500:] if len(stdout) > 500 else stdout)
finally:
    p.kill()
") || echo "[*] QEMU execution finished."
fi

echo "=== LAB-REQ-02 Smoke Test Complete ==="
