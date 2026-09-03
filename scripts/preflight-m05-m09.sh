#!/usr/bin/env bash
# scripts/preflight-m05-m09.sh
# Shared environment capability detector for Essential CS M05–M09.
#
# Inspects:
# 1. Host OS / Kernel / Architecture
# 2. Python 3 implementation & version
# 3. Native compiler & binutils (gcc, objdump)
# 4. Process inspection tools (ps, /proc filesystem)
# 5. Syscall tracing capabilities (strace)
# 6. RISC-V cross-toolchain (riscv64-linux-gnu-gcc, riscv64-linux-gnu-objdump)
# 7. QEMU RISC-V system emulator (qemu-system-riscv64)
# 8. Git version control

set -u

echo "=== Essential CS Shared Preflight (M05–M09) ==="
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date)
echo "Timestamp: ${DATE}"

# 1. OS / Kernel / Architecture
OS_NAME=$(uname -s 2>/dev/null || echo "Unknown")
KERNEL_REV=$(uname -r 2>/dev/null || echo "Unknown")
ARCH=$(uname -m 2>/dev/null || echo "Unknown")
echo "Host OS: ${OS_NAME} ${KERNEL_REV} (${ARCH})"

# 2. Python
PYTHON_BIN=""
for candidate in python3 python; do
    if command -v "${candidate}" >/dev/null 2>&1; then
        PYTHON_BIN="${candidate}"
        break
    fi
done

PYTHON_STATUS="MISSING"
PYTHON_VERSION="None"
PYTHON_IMPL="None"
if [ -n "${PYTHON_BIN}" ]; then
    PYTHON_STATUS="PASS"
    PYTHON_VERSION=$("${PYTHON_BIN}" -c "import sys; print(sys.version.split()[0])" 2>/dev/null || echo "Error")
    PYTHON_IMPL=$("${PYTHON_BIN}" -c "import platform; print(platform.python_implementation())" 2>/dev/null || echo "Error")
fi
echo "Python: ${PYTHON_STATUS} (${PYTHON_IMPL} ${PYTHON_VERSION})"

# 3. Native C Compiler & binutils
GCC_STATUS="MISSING"
GCC_VERSION="None"
if command -v gcc >/dev/null 2>&1; then
    GCC_STATUS="PASS"
    GCC_VERSION=$(gcc --version 2>/dev/null | head -n 1)
fi
echo "Native GCC: ${GCC_STATUS} (${GCC_VERSION})"

OBJDUMP_STATUS="MISSING"
if command -v objdump >/dev/null 2>&1; then
    OBJDUMP_STATUS="PASS"
fi
echo "Native objdump: ${OBJDUMP_STATUS}"

# 4. Process inspection (ps, /proc)
PS_STATUS="MISSING"
if command -v ps >/dev/null 2>&1; then
    PS_STATUS="PASS"
fi
echo "ps command: ${PS_STATUS}"

PROCFS_STATUS="MISSING"
if [ -d "/proc/self" ] && [ -r "/proc/self/status" ]; then
    PROCFS_STATUS="PASS"
fi
echo "procfs (/proc/self): ${PROCFS_STATUS}"

# 5. strace
STRACE_STATUS="MISSING"
STRACE_DETAIL="not installed"
if command -v strace >/dev/null 2>&1; then
    if strace true >/dev/null 2>&1; then
        STRACE_STATUS="PASS"
        STRACE_DETAIL="functional"
    else
        STRACE_STATUS="RESTRICTED"
        STRACE_DETAIL="installed but blocked by ptrace security policy"
    fi
fi
echo "strace: ${STRACE_STATUS} (${STRACE_DETAIL})"

# 6. RISC-V cross-toolchain
RISCV_GCC_STATUS="MISSING"
RISCV_GCC_BIN=""
for candidate in riscv64-linux-gnu-gcc riscv64-unknown-elf-gcc; do
    if command -v "${candidate}" >/dev/null 2>&1; then
        RISCV_GCC_STATUS="PASS"
        RISCV_GCC_BIN="${candidate}"
        break
    fi
done
echo "RISC-V cross GCC: ${RISCV_GCC_STATUS} (${RISCV_GCC_BIN:-none})"

# 7. QEMU RISC-V
QEMU_STATUS="MISSING"
QEMU_VERSION="None"
if command -v qemu-system-riscv64 >/dev/null 2>&1; then
    QEMU_STATUS="PASS"
    QEMU_VERSION=$(qemu-system-riscv64 --version 2>/dev/null | head -n 1)
fi
echo "QEMU RISC-V: ${QEMU_STATUS} (${QEMU_VERSION})"

# 8. Git
GIT_STATUS="MISSING"
GIT_VERSION="None"
if command -v git >/dev/null 2>&1; then
    GIT_STATUS="PASS"
    GIT_VERSION=$(git --version 2>/dev/null)
fi
echo "Git: ${GIT_STATUS} (${GIT_VERSION})"

echo "------------------------------------------------"
# Determine overall M06 / LAB-REQ-02 execution status
M06_HOST_STATUS="PARTIAL"
if [ "${PYTHON_STATUS}" = "PASS" ] && [ "${PROCFS_STATUS}" = "PASS" ]; then
    M06_HOST_STATUS="PASS"
fi

LAB_REQ_02_STATUS="BLOCKED"
if [ "${RISCV_GCC_STATUS}" = "PASS" ] && [ "${QEMU_STATUS}" = "PASS" ] && [ "${GIT_STATUS}" = "PASS" ]; then
    LAB_REQ_02_STATUS="RUNNABLE"
fi

echo "Summary:"
echo "  M06 Host Activity Capability: ${M06_HOST_STATUS}"
echo "  LAB-REQ-02 Runnable Capability: ${LAB_REQ_02_STATUS}"
if [ "${LAB_REQ_02_STATUS}" = "BLOCKED" ]; then
    echo "  Notice: LAB-REQ-02 runnable execution is BLOCKED due to missing cross-toolchain or QEMU."
    echo "          Source inspection & deterministic recorded fallback will be used."
fi
echo "=== Preflight Complete ==="
