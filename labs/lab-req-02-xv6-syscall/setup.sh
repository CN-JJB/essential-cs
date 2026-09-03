#!/usr/bin/env bash
# labs/lab-req-02-xv6-syscall/setup.sh
# Sets up the pinned xv6-riscv worktree for LAB-REQ-02.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKTREE_DIR="${SCRIPT_DIR}/worktree"
PINNED_COMMIT="35b088427ef37611c38afdeed5a52a278cae38f9"
UPSTREAM_REPO="https://github.com/mit-pdos/xv6-riscv.git"

echo "=== LAB-REQ-02 Setup ==="

if [ -d "${WORKTREE_DIR}/.git" ]; then
    echo "[*] Found existing worktree at ${WORKTREE_DIR}"
    CURRENT_COMMIT=$(cd "${WORKTREE_DIR}" && git rev-parse HEAD)
    if [ "${CURRENT_COMMIT}" = "${PINNED_COMMIT}" ]; then
        echo "[+] Worktree already at pinned commit: ${PINNED_COMMIT}"
        exit 0
    else
        echo "[*] Re-checking out pinned commit ${PINNED_COMMIT}..."
        (cd "${WORKTREE_DIR}" && git checkout "${PINNED_COMMIT}")
    fi
else
    echo "[*] Cloning official xv6-riscv repository into worktree..."
    git clone "${UPSTREAM_REPO}" "${WORKTREE_DIR}"
    (cd "${WORKTREE_DIR}" && git checkout "${PINNED_COMMIT}")
fi

VERIFIED_COMMIT=$(cd "${WORKTREE_DIR}" && git rev-parse HEAD)
if [ "${VERIFIED_COMMIT}" != "${PINNED_COMMIT}" ]; then
    echo "[-] ERROR: Worktree commit ${VERIFIED_COMMIT} does not match pinned ${PINNED_COMMIT}"
    exit 1
fi

echo "[+] Pinned xv6 worktree successfully initialized at commit: ${VERIFIED_COMMIT}"
echo "[+] License notice: MIT License preserved in ${WORKTREE_DIR}/LICENSE"
echo "=== Setup Complete ==="
