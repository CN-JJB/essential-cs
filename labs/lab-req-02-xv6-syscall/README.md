# LAB-REQ-02 — xv6 Syscall Traversal (`sleep` -> `pause/sys_pause`)

This lab satisfies **LAB-REQ-02**, tracing a user-to-kernel crossing through xv6 on RISC-V.

- **Upstream:** MIT 6.1810 Operating System Engineering (Fall 2025).
- **Canonical Upstream Repository:** `https://github.com/mit-pdos/xv6-riscv.git`
- **Pinned Commit:** `35b088427ef37611c38afdeed5a52a278cae38f9`
- **Current Route:** The learner implements the `sleep` user utility which calls xv6 system call **`pause(int ticks)`** (`SYS_pause` / `sys_pause`).

---

## Bounded Learner Change Surface

The learner's implementation scope is strictly bounded:
1. Create `worktree/user/sleep.c`.
2. Register `$U/_sleep\` in `UPROGS` inside `worktree/Makefile`.
3. Do NOT modify kernel files, shell implementations, or scheduler algorithms.

---

## Workflow Steps

### Step 1: Toolchain Preflight
Check whether QEMU and the RISC-V cross-compiler are available:
```bash
./preflight.sh
```
If toolchain is present, preflight will report `PASS`. If missing, it will report `BLOCKED`.

### Step 2: Setup Pinned Worktree
Clone and initialize the pinned xv6-riscv source repository:
```bash
./setup.sh
```
This checks out commit `35b088427ef37611c38afdeed5a52a278cae38f9` into `worktree/`.

### Step 3: Verify the Syscall Source Route
Audit the source route anchors to understand how `pause` connects user space to kernel space:
```bash
python3 verify_source_route.py worktree
```
This verifies:
- `user/user.h`: declares `int pause(int);`
- `user/usys.pl`: emits stub loading `li a7, SYS_pause` and calling `ecall`
- `kernel/syscall.h`: defines `#define SYS_pause 13`
- `kernel/syscall.c`: dispatches `[SYS_pause] = sys_pause`
- `kernel/sysproc.c`: implements `sys_pause()`

### Step 4: Implement `user/sleep.c`
Create `worktree/user/sleep.c` with the following structure:
```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int
main(int argc, char *argv[])
{
  if(argc != 2){
    fprintf(2, "Usage: sleep ticks\n");
    exit(1);
  }
  int ticks = atoi(argv[1]);
  pause(ticks);
  exit(0);
}
```
Add `$U/_sleep\` to `UPROGS` in `worktree/Makefile`.

### Step 5: Smoke Test & Execution
Run the smoke test to build the kernel, inspect the disassembly of `user/_sleep`, and run QEMU:
```bash
./smoke.sh
```

### Step 6: Clean Reset
To restore the worktree to its clean state and terminate any background emulator instances:
```bash
./reset.sh
```

---

## Fallback Execution Mode

If your environment cannot run QEMU (e.g. cloud container restrictions), read:
- `fallback_trace.md` for verbatim recorded QEMU output and disassembly evidence;
- `verify_source_route.py` for static source auditing.

*Note: Fallback mode is classified as `source inspection / fallback`, not `RUNNABLE PASS`.*
