#!/usr/bin/env python3
"""Verify the pinned Fall-2025 xv6 sleep -> pause/sys_pause route."""

import re
import subprocess
import sys
from pathlib import Path

PINNED_COMMIT = "35b088427ef37611c38afdeed5a52a278cae38f9"


def read(path: Path):
    return path.read_text(encoding="utf-8", errors="replace")


def verify_xv6_route(tree_path: Path):
    print(f"=== Verifying pinned xv6 syscall route in: {tree_path} ===")
    errors = []

    if not (tree_path / ".git").exists():
        return False, ["tree is not a Git checkout; exact source pin cannot be verified"]

    head = subprocess.run(
        ["git", "-C", str(tree_path), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if head.returncode != 0 or head.stdout.strip() != PINNED_COMMIT:
        errors.append(
            f"HEAD is not exact pin {PINNED_COMMIT}: {head.stdout.strip() or 'unresolved'}"
        )
    else:
        print(f"[+] Pin: HEAD == {PINNED_COMMIT}")

    required = {
        "kernel/syscall.h": tree_path / "kernel" / "syscall.h",
        "kernel/syscall.c": tree_path / "kernel" / "syscall.c",
        "kernel/sysproc.c": tree_path / "kernel" / "sysproc.c",
        "kernel/trap.c": tree_path / "kernel" / "trap.c",
        "kernel/trampoline.S": tree_path / "kernel" / "trampoline.S",
        "user/user.h": tree_path / "user" / "user.h",
        "user/usys.pl": tree_path / "user" / "usys.pl",
    }
    for label, path in required.items():
        if not path.exists():
            errors.append(f"{label} missing")

    if errors:
        return False, errors

    sc_h = read(required["kernel/syscall.h"])
    sc_c = read(required["kernel/syscall.c"])
    sp_c = read(required["kernel/sysproc.c"])
    trap_c = read(required["kernel/trap.c"])
    tramp_s = read(required["kernel/trampoline.S"])
    user_h = read(required["user/user.h"])
    usys_pl = read(required["user/usys.pl"])

    if not re.search(r"#define\s+SYS_pause\s+13\b", sc_h):
        errors.append("kernel/syscall.h does not define pinned SYS_pause 13")
    else:
        print("[+] syscall number: SYS_pause == 13")

    stale_blob = "\n".join((sc_h, sc_c, sp_c, usys_pl))
    if "SYS_sleep" in stale_blob or re.search(r"\bsys_sleep\b", stale_blob):
        errors.append("stale SYS_sleep/sys_sleep route found")

    if "[SYS_pause]" not in sc_c or "sys_pause" not in sc_c:
        errors.append("kernel/syscall.c pause dispatcher mapping missing")
    else:
        print("[+] dispatcher: [SYS_pause] -> sys_pause")

    if not re.search(r"\bsys_pause\s*\(\s*void\s*\)", sp_c):
        errors.append("kernel/sysproc.c sys_pause(void) implementation missing")
    else:
        print("[+] kernel implementation: sys_pause(void)")

    if not re.search(r"\bint\s+pause\s*\(\s*int\s*\)\s*;", user_h):
        errors.append("user/user.h int pause(int); declaration missing")
    else:
        print("[+] user declaration: int pause(int);")

    for needle, description in (
        ('entry("pause")', 'entry("pause")'),
        ('li a7, SYS_${name}', "generator loads a7 from SYS_<name>"),
        ("ecall", "generator emits ecall"),
        ("ret", "generator emits ret"),
    ):
        if needle not in usys_pl:
            errors.append(f"user/usys.pl missing {description}")
    if not any("user/usys.pl" in e for e in errors):
        print("[+] stub generator: pause entry -> a7 syscall number -> ecall -> ret")

    if "usertrap" not in trap_c or "r_scause() == 8" not in trap_c or "syscall();" not in trap_c:
        errors.append("kernel/trap.c U-mode ecall -> syscall() path not verified")
    else:
        print("[+] trap: U-mode ecall scause 8 -> syscall()")

    if "uservec:" not in tramp_s:
        errors.append("kernel/trampoline.S uservec entry missing")
    else:
        print("[+] trampoline: uservec entry present")

    sleep_c = tree_path / "user" / "sleep.c"
    if sleep_c.exists():
        sleep_src = read(sleep_c)
        if not re.search(r"\bpause\s*\(", sleep_src):
            errors.append("learner user/sleep.c exists but does not call pause(...)")
        else:
            print("[+] learner utility: user/sleep.c calls pause(...)")
    else:
        print("[*] learner user/sleep.c not present yet; upstream route still checked")

    generated = tree_path / "user" / "usys.S"
    if generated.exists():
        generated_text = read(generated)
        if not re.search(r"(?ms)^pause:\s*.*?li\s+a7,\s*SYS_pause\s*.*?ecall\s*.*?ret", generated_text):
            errors.append("generated user/usys.S pause stub does not match expected pinned relation")
        else:
            print("[+] generated stub: pause -> SYS_pause -> ecall -> ret")

    if errors:
        print("[-] ROUTE VERIFICATION FAILED:")
        for err in errors:
            print(f"    - {err}")
        return False, errors

    print("STATUS: PASS — Exact pin and current pause/sys_pause route verified.")
    return True, []


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "worktree"
    ok, _ = verify_xv6_route(target)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
