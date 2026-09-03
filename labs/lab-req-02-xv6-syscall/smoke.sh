#!/usr/bin/env bash
# Machine-checkable smoke test for LAB-REQ-02 user/sleep implementation.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKTREE_DIR="${SCRIPT_DIR}/worktree"
PINNED_COMMIT="35b088427ef37611c38afdeed5a52a278cae38f9"

echo "=== LAB-REQ-02 Smoke Test ==="

if [ ! -d "${WORKTREE_DIR}/.git" ]; then
    echo "[-] Worktree not found. Run ./setup.sh first."
    exit 1
fi

if [ "$(git -C "${WORKTREE_DIR}" rev-parse HEAD)" != "${PINNED_COMMIT}" ]; then
    echo "[-] Worktree is not at the pinned commit."
    exit 1
fi

if [ ! -f "${WORKTREE_DIR}/user/sleep.c" ]; then
    echo "[-] Learner implementation missing: user/sleep.c"
    exit 1
fi

if ! grep -q 'pause[[:space:]]*(' "${WORKTREE_DIR}/user/sleep.c"; then
    echo "[-] user/sleep.c does not visibly call xv6 pause(ticks)."
    exit 1
fi

if ! grep -q '\$U/_sleep' "${WORKTREE_DIR}/Makefile"; then
    echo "[-] \$U/_sleep is not registered in UPROGS."
    exit 1
fi

echo "[+] Step 1: Build kernel, filesystem image, and user/_sleep..."
(cd "${WORKTREE_DIR}" && make fs.img kernel/kernel)

if command -v riscv64-linux-gnu-objdump >/dev/null 2>&1; then
    OBJDUMP_BIN="riscv64-linux-gnu-objdump"
elif command -v riscv64-unknown-elf-objdump >/dev/null 2>&1; then
    OBJDUMP_BIN="riscv64-unknown-elf-objdump"
else
    echo "[-] RISC-V objdump not found."
    exit 1
fi

echo "[+] Step 2: Verify disassembly relations..."
DISASM=$("${OBJDUMP_BIN}" -d "${WORKTREE_DIR}/user/_sleep")
if ! grep -q '<pause>:' <<<"${DISASM}"; then
    echo "[-] pause syscall stub symbol not found."
    exit 1
fi
if ! grep -Eq 'jal[[:space:]].*<pause>' <<<"${DISASM}"; then
    echo "[-] main-to-pause call relation not found in disassembly."
    exit 1
fi
if ! grep -q 'ecall' <<<"${DISASM}"; then
    echo "[-] ecall not found in user/_sleep disassembly."
    exit 1
fi
echo "[+] Disassembly relation verified: main -> pause stub -> ecall."

echo "[+] Step 3: Run bounded QEMU shell test..."
QEMU_PID_FILE="${WORKTREE_DIR}/.qemu_smoke.pid"
export WORKTREE_DIR QEMU_PID_FILE

python3 <<'PY'
import os
import select
import signal
import subprocess
import time
from pathlib import Path

worktree = Path(os.environ["WORKTREE_DIR"])
pid_file = Path(os.environ["QEMU_PID_FILE"])
p = subprocess.Popen(
    ["make", "qemu"],
    cwd=worktree,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    start_new_session=True,
)
pid_file.write_text(str(p.pid), encoding="utf-8")
lines = []

def read_until(needle, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        ready, _, _ = select.select([p.stdout], [], [], 0.25)
        if ready:
            line = p.stdout.readline()
            if line == "":
                break
            lines.append(line)
            if needle in "".join(lines[-20:]):
                return True
        if p.poll() is not None:
            break
    return False

try:
    if not read_until("init: starting sh", 15):
        raise RuntimeError("xv6 shell did not reach 'init: starting sh' within timeout")

    p.stdin.write("sleep\n")
    p.stdin.write("sleep 10\n")
    p.stdin.write("echo LAB_REQ_02_OK\n")
    p.stdin.flush()

    if not read_until("LAB_REQ_02_OK", 15):
        raise RuntimeError("sleep 10 did not return to the shell marker within timeout")

    output = "".join(lines)
    if "Usage: sleep ticks" not in output:
        raise RuntimeError("missing-argument sleep usage output was not observed")
    if "exec sleep failed" in output:
        raise RuntimeError("xv6 shell reported that sleep could not be executed")

    print(output[-1200:])
    print("QEMU_SMOKE_STATUS: PASS")
finally:
    try:
        os.killpg(p.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        p.wait(timeout=1)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait(timeout=2)
    pid_file.unlink(missing_ok=True)
PY

echo "=== LAB-REQ-02 Smoke Test PASS ==="
