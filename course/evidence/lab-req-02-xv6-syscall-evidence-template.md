# LAB-REQ-02 xv6 Syscall Evidence Template

## A — Source Pin & Commit
- Upstream Repository: `https://github.com/mit-pdos/xv6-riscv.git`
- Pinned Commit: `35b088427ef37611c38afdeed5a52a278cae38f9`
- Pinned Commit Title: `test for nlink overflow`
- Worktree HEAD Verified:

---

## B — License & Provenance
- xv6 Software License: MIT License (confirmed in `worktree/LICENSE`)
- Notice Retention Verified: Yes / No
- MIT 6.1810 Lab Page License: Reusable license not independently established; treated as link-only reference
- Originality Declaration: All student guidance and rubrics are original Essential CS materials

---

## C — Toolchain Versions
- Host OS & Architecture:
- Git Version:
- RISC-V Cross GCC Version:
- QEMU Version:

---

## D — Setup Result
- Setup Command Run: `./setup.sh`
- Worktree Directory: `worktree/`
- Setup Status (PASS / BLOCKED):
- Notes:

---

## E — Learner Changes
- Added Files: `worktree/user/sleep.c`
- Modified Files: `worktree/Makefile` (added `$U/_sleep\` to `UPROGS`)
- Verified No Out-of-Scope Files Changed: Yes / No

---

## F — Source-Route Anchors Verified
- Command Run: `python3 verify_source_route.py worktree`
- Verification Status: PASS / FAIL
- Anchors Checked:
  1. `kernel/syscall.h`: defines `SYS_pause 13` (Confirmed `SYS_sleep` absent)
  2. `kernel/syscall.c`: defines `[SYS_pause] = sys_pause`
  3. `kernel/sysproc.c`: implements `sys_pause(void)`
  4. `user/user.h`: declares `int pause(int);`
  5. `user/usys.pl`: emits stub `pause: li a7, SYS_pause; ecall; ret`
  6. `kernel/trap.c`: routes `ecall` to `syscall()`

---

## G — Build Result
- Build Command: `make fs.img kernel/kernel`
- Build Outcome (PASS / FAIL / NOT RUN):
- Compiler Output Excerpt:

---

## H — QEMU Execution Result
- Command: `make qemu`
- Boot Outcome:
- Command Executed in xv6 Shell: `sleep 10`
- Observed Behavior:

---

## I — Grader Result
- Official Course Grader: (if applicable on course fork)
- Status: PASS / NOT RUN / NOT APPLICABLE
- Grader Output Excerpt:

---

## J — Missing-Argument Result
- Command Executed: `sleep` (no arguments)
- Output to Stderr (fd 2): `Usage: sleep ticks`
- Exit Code: 1

---

## K — Reset Result
- Reset Command: `./reset.sh`
- Worktree Restored to Clean Git State?
- QEMU Process Scoped Cleanup Verified?

---

## L — Actual Route Explanation
Trace the exact steps from `sleep.c` to `sys_pause`:
1. `user/sleep.c`: calls `pause(ticks)`
2. `user/usys.S`: loads `SYS_pause` (`13`) into `a7`, executes `ecall`
3. Hardware Trap: CPU switches from U-mode to S-mode, vectors to `kernel/trampoline.S`
4. `kernel/trap.c:usertrap()`: handles environment call (`r_scause() == 8`), advances `epc += 4`, calls `syscall()`
5. `kernel/syscall.c:syscall()`: dispatches to `sys_pause()` via syscall table
6. `kernel/sysproc.c:sys_pause()`: puts process to sleep waiting on ticks, returns in `a0`
7. `usertrapret()`: returns to user mode via `sret` in `trampoline.S`

---

## M — xv6 vs POSIX / Linux Boundary
- How does xv6 `pause(int ticks)` differ from POSIX `pause(2)`?
- How does RISC-V `ecall` differ from x86-64 `syscall`?
- How do xv6 timer ticks differ from real physical seconds?

---

## N — Fallback Usage & Non-Equivalence
- Was Fallback Trace Used? (Yes / No)
- If Yes, Reason (e.g. missing cross-compiler, cloud container restriction):
- Explicit Disclaimer: Confirmed that fallback study is non-equivalent to running LAB-REQ-02.

---

## O — Fact vs Inference / Blockers
- What was directly observed vs inferred from code inspection?
- Any unresolved toolchain or virtualization blockers?
