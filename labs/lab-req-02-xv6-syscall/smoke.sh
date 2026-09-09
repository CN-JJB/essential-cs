#!/usr/bin/env bash
# Machine-checkable smoke test for LAB-REQ-02 user/sleep implementation.
#
# QEMU interaction is prompt-paced (no burst write). The execution marker is
# accepted only as a standalone output line exactly equal to LAB_REQ_02_OK,
# not as a substring of the echoed command `echo LAB_REQ_02_OK`.
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

echo "[+] Step 3: Marker predicate self-check (echo-only must not PASS)..."
python3 - <<'PY'
import sys

# Keep this predicate identical to the QEMU waiter below.
MARKER = "LAB_REQ_02_OK"


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def has_prompt(text: str) -> bool:
    return normalize(text).endswith("$ ")


def has_execution_marker(text: str) -> bool:
    for line in normalize(text).split("\n"):
        if line.strip() == MARKER:
            return True
    return False


def execution_marker_satisfied(text: str) -> bool:
    return has_execution_marker(text) and has_prompt(text)


failures = []


def expect(name, cond):
    if not cond:
        failures.append(name)


echo_only = "init: starting sh\n$ echo LAB_REQ_02_OK\n"
expect("echo-only command line is not execution", not has_execution_marker(echo_only))
expect("echo-only with prompt is not execution", not execution_marker_satisfied(echo_only + "$ "))
expect(
    "prompt-prefixed echoed command is not execution",
    not has_execution_marker("$ echo LAB_REQ_02_OK\n"),
)
real_output = "$ echo LAB_REQ_02_OK\necho LAB_REQ_02_OK\nLAB_REQ_02_OK\n$ "
expect("standalone output line plus prompt is execution", execution_marker_satisfied(real_output))
expect(
    "output line without following prompt is incomplete",
    not execution_marker_satisfied("$ echo LAB_REQ_02_OK\nLAB_REQ_02_OK\n"),
)
expect("usage line is not a false marker", not has_execution_marker("Usage: sleep ticks\n$ "))

if failures:
    print("MARKER_SELF_CHECK: FAIL")
    for item in failures:
        print(f"  - {item}")
    sys.exit(1)
print("MARKER_SELF_CHECK: PASS")
print("Echoed command text alone cannot satisfy the execution-marker predicate.")
PY

echo "[+] Step 4: Run bounded, prompt-paced QEMU shell test..."
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
MARKER = "LAB_REQ_02_OK"
USAGE = "Usage: sleep ticks"


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def has_prompt(text: str) -> bool:
    return normalize(text).endswith("$ ")


def has_execution_marker(text: str) -> bool:
    for line in normalize(text).split("\n"):
        if line.strip() == MARKER:
            return True
    return False


p = subprocess.Popen(
    ["make", "qemu"],
    cwd=worktree,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    bufsize=0,
    start_new_session=True,
)
pid_file.write_text(str(p.pid), encoding="utf-8")
buf = ""
reaped = False


def append_available(timeout):
    global buf
    if p.stdout is None:
        return False
    ready, _, _ = select.select([p.stdout], [], [], timeout)
    if not ready:
        return True
    chunk = os.read(p.stdout.fileno(), 4096)
    if chunk == b"":
        return False
    buf += chunk.decode("utf-8", errors="replace")
    return True


def wait_until(predicate, timeout, label):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        remaining = max(0.0, deadline - time.monotonic())
        if not append_available(min(0.25, remaining)):
            break
        if predicate(buf):
            return
        if p.poll() is not None:
            break
    raise RuntimeError(
        f"{label} not observed within {timeout}s; last output:\n{buf[-2000:]}"
    )


def send_command(command):
    if p.stdin is None:
        raise RuntimeError("QEMU stdin is unavailable")
    p.stdin.write((command + "\n").encode("utf-8"))
    p.stdin.flush()


def cleanup():
    global reaped
    if p.stdin is not None:
        try:
            p.stdin.close()
        except OSError:
            pass
    if p.poll() is None:
        try:
            os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            p.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                p.wait(timeout=3)
            except subprocess.TimeoutExpired as exc:
                raise RuntimeError("owned QEMU process group was not reaped") from exc
    if p.poll() is None:
        raise RuntimeError("owned QEMU process group was not reaped")
    reaped = True
    pid_file.unlink(missing_ok=True)


try:
    wait_until(lambda text: "init: starting sh" in text, 20, "xv6 shell start (init: starting sh)")
    wait_until(has_prompt, 10, "initial xv6 shell prompt")

    before_sleep = len(buf)
    send_command("sleep")

    def sleep_usage_complete(text):
        new = text[before_sleep:]
        return USAGE in new and has_prompt(text)

    wait_until(sleep_usage_complete, 10, "no-argument sleep usage output and next prompt")

    before_sleep10 = len(buf)
    send_command("sleep 10")

    def sleep10_returned(text):
        new = text[before_sleep10:]
        return has_prompt(text) and "$ " in normalize(new)

    wait_until(sleep10_returned, 15, "sleep 10 return to shell prompt")

    before_marker = len(buf)
    send_command("echo " + MARKER)

    def marker_executed(text):
        new = text[before_marker:]
        if has_execution_marker(new) and has_prompt(text):
            # Reject the case where the only match is still just the command echo.
            # has_execution_marker already requires a standalone line == MARKER.
            return True
        return False

    wait_until(marker_executed, 10, "execution-only LAB_REQ_02_OK output line and next prompt")

    if "exec sleep failed" in buf:
        raise RuntimeError("xv6 shell reported that sleep could not be executed")
    if USAGE not in buf:
        raise RuntimeError("missing-argument sleep usage output was not observed")
    if not has_execution_marker(buf[before_marker:]):
        raise RuntimeError("execution-only marker was not observed")

    print(buf[-1600:])
    print("QEMU_SMOKE_STATUS: PASS")
    print("USAGE_OUTPUT_OBSERVED: YES")
    print("SLEEP10_RETURNED: YES")
    print("EXECUTION_MARKER_OBSERVED: YES")
finally:
    cleanup()
    print(f"QEMU_REAPED: {str(reaped).upper()}")
    if pid_file.exists():
        raise RuntimeError("PID marker file remained after cleanup")
    print("PID_MARKER_CLEAN: YES")
PY

echo "=== LAB-REQ-02 Smoke Test PASS ==="
