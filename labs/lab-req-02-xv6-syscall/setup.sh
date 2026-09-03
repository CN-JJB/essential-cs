#!/usr/bin/env bash
# Sets up the dedicated pinned xv6-riscv worktree for LAB-REQ-02.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKTREE_DIR="${SCRIPT_DIR}/worktree"
PINNED_COMMIT="35b088427ef37611c38afdeed5a52a278cae38f9"
UPSTREAM_REPO="https://github.com/mit-pdos/xv6-riscv.git"

echo "=== LAB-REQ-02 Setup ==="

if [ -d "${WORKTREE_DIR}/.git" ]; then
    echo "[*] Found existing dedicated worktree."
    ORIGIN=$(git -C "${WORKTREE_DIR}" remote get-url origin 2>/dev/null || true)
    if [ "${ORIGIN}" != "${UPSTREAM_REPO}" ] && [ "${ORIGIN}" != "https://github.com/mit-pdos/xv6-riscv" ]; then
        echo "[-] ERROR: Existing worktree origin is not the canonical upstream: ${ORIGIN}"
        exit 1
    fi
else
    echo "[*] Cloning official xv6-riscv repository..."
    git clone "${UPSTREAM_REPO}" "${WORKTREE_DIR}"
fi

if ! git -C "${WORKTREE_DIR}" cat-file -e "${PINNED_COMMIT}^{commit}" 2>/dev/null; then
    echo "[-] ERROR: Pinned commit is not available in the worktree."
    exit 1
fi

CURRENT_COMMIT=$(git -C "${WORKTREE_DIR}" rev-parse HEAD)
if [ "${CURRENT_COMMIT}" != "${PINNED_COMMIT}" ]; then
    echo "[*] Checking out pinned commit ${PINNED_COMMIT}..."
    git -C "${WORKTREE_DIR}" checkout --detach "${PINNED_COMMIT}"
fi

VERIFIED_COMMIT=$(git -C "${WORKTREE_DIR}" rev-parse HEAD)
if [ "${VERIFIED_COMMIT}" != "${PINNED_COMMIT}" ]; then
    echo "[-] ERROR: HEAD ${VERIFIED_COMMIT} does not match pinned ${PINNED_COMMIT}"
    exit 1
fi

if [ ! -f "${WORKTREE_DIR}/LICENSE" ]; then
    echo "[-] ERROR: xv6 LICENSE missing from pinned worktree."
    exit 1
fi

echo "[+] Pinned xv6 worktree: ${VERIFIED_COMMIT}"
echo "[+] Canonical origin: ${UPSTREAM_REPO}"
echo "[+] xv6 software license file present: ${WORKTREE_DIR}/LICENSE"
echo "=== Setup Complete ==="
