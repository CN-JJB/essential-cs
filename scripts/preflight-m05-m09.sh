#!/usr/bin/env bash
# Shared capability detector for Essential CS M05–M09.
# Reports capabilities; it does not install packages, change security policy, or close OQ-BP-006.
set -u

echo "=== Essential CS Shared Preflight (M05–M09) ==="
DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date)
echo "Timestamp: ${DATE}"

OS_NAME=$(uname -s 2>/dev/null || echo "Unknown")
KERNEL_REV=$(uname -r 2>/dev/null || echo "Unknown")
ARCH=$(uname -m 2>/dev/null || echo "Unknown")
echo "Host OS: ${OS_NAME} ${KERNEL_REV} (${ARCH})"

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
FORK_STATUS="UNAVAILABLE"
RESOURCE_STATUS="UNAVAILABLE"
FSYNC_STATUS="UNAVAILABLE"
FDATASYNC_STATUS="UNAVAILABLE"
if [ -n "${PYTHON_BIN}" ]; then
    PYTHON_STATUS="PASS"
    PYTHON_VERSION=$("${PYTHON_BIN}" -c "import sys; print(sys.version.split()[0])" 2>/dev/null || echo "Error")
    PYTHON_IMPL=$("${PYTHON_BIN}" -c "import platform; print(platform.python_implementation())" 2>/dev/null || echo "Error")
    if "${PYTHON_BIN}" -c "import os,sys; sys.exit(0 if hasattr(os,'fork') else 1)" >/dev/null 2>&1; then
        FORK_STATUS="PASS"
    fi
    if "${PYTHON_BIN}" -c "import resource,sys; sys.exit(0)" >/dev/null 2>&1; then
        RESOURCE_STATUS="PASS"
    fi
    if "${PYTHON_BIN}" -c "import os,sys; sys.exit(0 if hasattr(os,'fsync') else 1)" >/dev/null 2>&1; then
        FSYNC_STATUS="PASS"
    fi
    if "${PYTHON_BIN}" -c "import os,sys; sys.exit(0 if hasattr(os,'fdatasync') else 1)" >/dev/null 2>&1; then
        FDATASYNC_STATUS="PASS"
    fi
fi
echo "Python: ${PYTHON_STATUS} (${PYTHON_IMPL} ${PYTHON_VERSION})"
echo "os.fork capability: ${FORK_STATUS}"
echo "resource module: ${RESOURCE_STATUS}"
echo "os.fsync capability: ${FSYNC_STATUS}"
echo "os.fdatasync capability: ${FDATASYNC_STATUS}"

cmd_status() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "PASS"
    else
        echo "MISSING"
    fi
}

GCC_STATUS=$(cmd_status gcc)
OBJDUMP_STATUS=$(cmd_status objdump)
PS_STATUS=$(cmd_status ps)
GIT_STATUS=$(cmd_status git)
MAKE_STATUS=$(cmd_status make)
PERL_STATUS=$(cmd_status perl)
BC_STATUS=$(cmd_status bc)
CURL_STATUS=$(cmd_status curl)

echo "Native GCC: ${GCC_STATUS} $([ "${GCC_STATUS}" = PASS ] && gcc --version 2>/dev/null | head -n1)"
echo "Native objdump: ${OBJDUMP_STATUS}"
echo "ps command: ${PS_STATUS}"
echo "git: ${GIT_STATUS} $([ "${GIT_STATUS}" = PASS ] && git --version 2>/dev/null)"
echo "make: ${MAKE_STATUS}"
echo "perl: ${PERL_STATUS}"
echo "bc: ${BC_STATUS}"
echo "curl: ${CURL_STATUS} $([ "${CURL_STATUS}" = PASS ] && curl --version 2>/dev/null | head -n1)"

PROCFS_STATUS="MISSING"
if [ -d "/proc/self" ] && [ -r "/proc/self/status" ]; then
    PROCFS_STATUS="PASS"
fi
echo "procfs (/proc/self): ${PROCFS_STATUS}"

MAPS_STATUS="MISSING"
if [ -d "/proc/self" ] && [ -r "/proc/self/maps" ]; then
    MAPS_STATUS="PASS"
fi
echo "procfs maps (/proc/self/maps): ${MAPS_STATUS}"

FD_STATUS="MISSING"
if [ -d "/proc/self/fd" ] && [ -r "/proc/self/fd" ]; then
    FD_STATUS="PASS"
fi
echo "procfs fd (/proc/self/fd): ${FD_STATUS}"

MEMINFO_STATUS="MISSING"
if [ -f "/proc/meminfo" ] && [ -r "/proc/meminfo" ]; then
    MEMINFO_STATUS="PASS"
fi
echo "procfs meminfo (/proc/meminfo): ${MEMINFO_STATUS}"

STRACE_STATUS="MISSING"
STRACE_DETAIL="not installed"
if command -v strace >/dev/null 2>&1; then
    if strace true >/dev/null 2>&1; then
        STRACE_STATUS="PASS"
        STRACE_DETAIL="functional bounded probe"
    else
        STRACE_STATUS="RESTRICTED"
        STRACE_DETAIL="installed but live tracing probe failed/was blocked"
    fi
fi
echo "strace: ${STRACE_STATUS} (${STRACE_DETAIL})"

RISCV_GCC_STATUS="MISSING"
RISCV_OBJDUMP_STATUS="MISSING"
RISCV_PREFIX=""
for prefix in riscv64-linux-gnu riscv64-unknown-elf; do
    if command -v "${prefix}-gcc" >/dev/null 2>&1 && command -v "${prefix}-objdump" >/dev/null 2>&1; then
        RISCV_GCC_STATUS="PASS"
        RISCV_OBJDUMP_STATUS="PASS"
        RISCV_PREFIX="${prefix}"
        break
    fi
done
echo "RISC-V cross GCC: ${RISCV_GCC_STATUS} (${RISCV_PREFIX:-none})"
echo "RISC-V objdump: ${RISCV_OBJDUMP_STATUS}"

QEMU_STATUS="MISSING"
QEMU_VERSION="None"
if command -v qemu-system-riscv64 >/dev/null 2>&1; then
    QEMU_STATUS="PASS"
    QEMU_VERSION=$(qemu-system-riscv64 --version 2>/dev/null | head -n1)
fi
echo "QEMU RISC-V: ${QEMU_STATUS} (${QEMU_VERSION})"

echo "------------------------------------------------"
M06_HOST_STATUS="PARTIAL"
if [ "${PYTHON_STATUS}" = "PASS" ] && [ "${FORK_STATUS}" = "PASS" ] && [ "${PROCFS_STATUS}" = "PASS" ]; then
    M06_HOST_STATUS="PASS"
fi

M07_HOST_STATUS="PARTIAL"
if [ "${PYTHON_STATUS}" = "PASS" ] && [ "${GCC_STATUS}" = "PASS" ] && [ "${MAPS_STATUS}" = "PASS" ] && [ "${RESOURCE_STATUS}" = "PASS" ]; then
    M07_HOST_STATUS="PASS"
fi

M08_HOST_STATUS="PARTIAL"
if [ "${PYTHON_STATUS}" = "PASS" ] && [ "${FD_STATUS}" = "PASS" ] && [ "${MEMINFO_STATUS}" = "PASS" ]; then
    M08_HOST_STATUS="PASS"
fi

M09_HOST_STATUS="PARTIAL"
if [ "${PYTHON_STATUS}" = "PASS" ] && [ "${FSYNC_STATUS}" = "PASS" ]; then
    M09_HOST_STATUS="PASS"
fi

LAB_REQ_02_STATUS="BLOCKED"
if [ "${GIT_STATUS}" = "PASS" ] &&
   [ "${MAKE_STATUS}" = "PASS" ] &&
   [ "${PERL_STATUS}" = "PASS" ] &&
   [ "${BC_STATUS}" = "PASS" ] &&
   [ "${PYTHON_STATUS}" = "PASS" ] &&
   [ "${RISCV_GCC_STATUS}" = "PASS" ] &&
   [ "${RISCV_OBJDUMP_STATUS}" = "PASS" ] &&
   [ "${QEMU_STATUS}" = "PASS" ]; then
    LAB_REQ_02_STATUS="RUNNABLE"
fi

echo "Summary:"
echo "  M06 Host Activity Capability: ${M06_HOST_STATUS}"
echo "  M06 Live strace Capability: ${STRACE_STATUS}"
echo "  M07 Host Activity Capability: ${M07_HOST_STATUS}"
echo "  M08 Host Activity Capability: ${M08_HOST_STATUS}"
echo "  M08 Live strace Capability: ${STRACE_STATUS}"
echo "  M09 Host Activity Capability: ${M09_HOST_STATUS}"
echo "  M09 Network/Curl Capability: ${CURL_STATUS}"
echo "  LAB-REQ-02 Runnable Capability: ${LAB_REQ_02_STATUS}"
echo "  NOTE: RUNNABLE means capability-present; build/QEMU smoke still must run and pass separately."
echo "=== Preflight Complete ==="
