#!/usr/bin/env bash
# labs/lab-req-02-xv6-syscall/reset.sh
# Safely cleans up the xv6 worktree and terminates course-owned QEMU instances.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKTREE_DIR="${SCRIPT_DIR}/worktree"
PID_FILE="${WORKTREE_DIR}/.qemu_smoke.pid"

echo "=== LAB-REQ-02 Reset ==="

# 1. Scoped process cleanup: check for PID file if recorded
if [ -f "${PID_FILE}" ]; then
    QEMU_PID=$(cat "${PID_FILE}")
    if [ -n "${QEMU_PID}" ] && kill -0 "${QEMU_PID}" 2>/dev/null; then
        echo "[*] Terminating recorded QEMU process (PID ${QEMU_PID})..."
        kill -9 "${QEMU_PID}" 2>/dev/null || true
    fi
    rm -f "${PID_FILE}"
fi

# 2. Reset worktree repository if present
if [ -d "${WORKTREE_DIR}/.git" ]; then
    echo "[*] Restoring xv6 worktree to clean pinned state..."
    (cd "${WORKTREE_DIR}" && git checkout -f && git clean -fd)
    echo "[+] Worktree restored to clean pinned commit."
else
    echo "[*] No worktree found to reset."
fi

echo "=== Reset Complete ==="
