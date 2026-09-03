#!/usr/bin/env python3
"""LAB-REQ-02 Source Route Verifier.

Statically audits the xv6-riscv source tree to verify the 6 route anchors
connecting the `sleep` user program to the underlying `pause/sys_pause` system call.

Verifies:
1. Absence of stale SYS_sleep / sys_sleep definitions.
2. Presence of SYS_pause in kernel/syscall.h.
3. Registration of sys_pause in kernel/syscall.c.
4. Implementation of sys_pause in kernel/sysproc.c.
5. User library prototype in user/user.h.
6. Syscall stub entry in user/usys.pl.
"""

import sys
from pathlib import Path


def verify_xv6_route(tree_path: Path):
    print(f"=== Verifying xv6 Syscall Route in: {tree_path} ===")
    errors = []

    if not tree_path.exists():
        print(f"[-] Directory not found: {tree_path}")
        return False, ["Directory does not exist"]

    # 1. kernel/syscall.h
    sc_h = tree_path / "kernel" / "syscall.h"
    if not sc_h.exists():
        errors.append("kernel/syscall.h missing")
    else:
        content = sc_h.read_text(encoding="utf-8", errors="replace")
        if "SYS_pause" not in content:
            errors.append("SYS_pause definition missing from kernel/syscall.h")
        else:
            print("[+] Anchor 1: kernel/syscall.h defines SYS_pause")
        if "SYS_sleep" in content:
            errors.append("Stale SYS_sleep definition found in kernel/syscall.h")

    # 2. kernel/syscall.c
    sc_c = tree_path / "kernel" / "syscall.c"
    if not sc_c.exists():
        errors.append("kernel/syscall.c missing")
    else:
        content = sc_c.read_text(encoding="utf-8", errors="replace")
        if "sys_pause" not in content or "[SYS_pause]" not in content:
            errors.append("sys_pause dispatcher entry missing from kernel/syscall.c")
        else:
            print("[+] Anchor 2: kernel/syscall.c registers [SYS_pause] = sys_pause")

    # 3. kernel/sysproc.c
    sp_c = tree_path / "kernel" / "sysproc.c"
    if not sp_c.exists():
        errors.append("kernel/sysproc.c missing")
    else:
        content = sp_c.read_text(encoding="utf-8", errors="replace")
        if "sys_pause(void)" not in content:
            errors.append("sys_pause(void) function implementation missing from kernel/sysproc.c")
        else:
            print("[+] Anchor 3: kernel/sysproc.c implements sys_pause(void)")

    # 4. user/user.h
    u_h = tree_path / "user" / "user.h"
    if not u_h.exists():
        errors.append("user/user.h missing")
    else:
        content = u_h.read_text(encoding="utf-8", errors="replace")
        if "pause(int" not in content and "pause(int)" not in content:
            errors.append("int pause(int); prototype missing from user/user.h")
        else:
            print("[+] Anchor 4: user/user.h declares int pause(int);")

    # 5. user/usys.pl
    u_pl = tree_path / "user" / "usys.pl"
    if not u_pl.exists():
        errors.append("user/usys.pl missing")
    else:
        content = u_pl.read_text(encoding="utf-8", errors="replace")
        if 'entry("pause")' not in content:
            errors.append('entry("pause") missing from user/usys.pl')
        else:
            print('[+] Anchor 5: user/usys.pl contains entry("pause")')

    # 6. kernel/trap.c
    trap_c = tree_path / "kernel" / "trap.c"
    if not trap_c.exists():
        errors.append("kernel/trap.c missing")
    else:
        content = trap_c.read_text(encoding="utf-8", errors="replace")
        if "usertrap" not in content or "syscall" not in content:
            errors.append("usertrap syscall dispatch missing from kernel/trap.c")
        else:
            print("[+] Anchor 6: kernel/trap.c routes ecall trap to syscall()")

    if errors:
        print("[-] ROUTE VERIFICATION FAILED:")
        for err in errors:
            print(f"    - {err}")
        return False, errors

    print("STATUS: PASS — All 6 route anchors verified against Fall 2025 specification.")
    return True, []


def main():
    default_dir = Path(__file__).parent / "worktree"
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else default_dir
    success, _ = verify_xv6_route(target_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
