#!/usr/bin/env bash
# Restores only the dedicated LAB-REQ-02 xv6 worktree and its recorded QEMU process group.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKTREE_DIR="${SCRIPT_DIR}/worktree"
PID_FILE="${WORKTREE_DIR}/.qemu_smoke.pid"
PINNED_COMMIT="35b088427ef37611c38afdeed5a52a278cae38f9"

echo "=== LAB-REQ-02 Reset ==="

if [ -f "${PID_FILE}" ]; then
    QEMU_GROUP_LEADER=$(cat "${PID_FILE}" 2>/dev/null || true)
    if [[ "${QEMU_GROUP_LEADER}" =~ ^[0-9]+$ ]] && kill -0 "${QEMU_GROUP_LEADER}" 2>/dev/null; then
        echo "[*] Terminating recorded course-owned QEMU process group ${QEMU_GROUP_LEADER}..."
        kill -TERM -- "-${QEMU_GROUP_LEADER}" 2>/dev/null || true
        sleep 0.2
        kill -KILL -- "-${QEMU_GROUP_LEADER}" 2>/dev/null || true
    fi
    rm -f "${PID_FILE}"
fi

if [ -d "${WORKTREE_DIR}/.git" ]; then
    echo "[*] Restoring dedicated xv6 worktree to exact pinned commit..."
    git -C "${WORKTREE_DIR}" reset --hard "${PINNED_COMMIT}"
    git -C "${WORKTREE_DIR}" clean -fdx

    HEAD_NOW=$(git -C "${WORKTREE_DIR}" rev-parse HEAD)
    DIRTY=$(git -C "${WORKTREE_DIR}" status --porcelain)
    if [ "${HEAD_NOW}" != "${PINNED_COMMIT}" ] || [ -n "${DIRTY}" ]; then
        echo "[-] ERROR: Reset did not restore the exact clean pin."
        exit 1
    fi
    echo "[+] Worktree restored to clean pin ${PINNED_COMMIT}."
else
    echo "[*] No dedicated worktree found; nothing to reset."
fi

echo "=== Reset Complete ==="
