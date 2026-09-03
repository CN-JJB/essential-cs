# LAB-REQ-02 — xv6 Syscall Traversal (`sleep` → `pause/sys_pause`)

This Required Lab traces a user-to-kernel crossing through the pinned Fall 2025 xv6 RISC-V tree.

- Upstream: MIT 6.1810 Operating System Engineering (Fall 2025)
- Repository: `https://github.com/mit-pdos/xv6-riscv.git`
- Pin: `35b088427ef37611c38afdeed5a52a278cae38f9`
- Current route: learner `sleep` utility calls xv6 `pause(int ticks)` → generated syscall stub → RISC-V `ecall` → trap/dispatcher → `sys_pause()`
- xv6 software: MIT-style license in upstream `LICENSE`
- MIT lab-page prose: link/reference only; do not copy/adapt it as course prose without separately verified reuse rights

## Learner change surface

Only:

1. `worktree/user/sleep.c`
2. `$U/_sleep` registration in `worktree/Makefile`

No new kernel syscall, scheduler change, shell rewrite, or grader implementation.

## Workflow

### 1. Capability preflight

```bash
./preflight.sh
```

`PASS` means required local commands are present. It does **not** mean build/QEMU execution has passed.

### 2. Setup exact source pin

```bash
./setup.sh
```

The script verifies canonical origin, exact HEAD, and upstream license file.

### 3. Inspect the current route

```bash
python3 verify_source_route.py worktree
```

The verifier checks the exact git pin plus the current `pause/sys_pause` source anchors. If learner/generated files already exist, their route is checked too.

### 4. Implement `user/sleep.c`

Use original Essential CS guidance; a minimal structure should validate one tick argument, convert it, call xv6 `pause(ticks)`, and exit. Register `$U/_sleep` in `UPROGS`.

### 5. Run machine-checkable smoke

```bash
./smoke.sh
```

PASS requires:

- exact source pin;
- xv6 build success;
- disassembly relation `main -> pause -> ecall`;
- QEMU reaches the xv6 shell;
- missing-argument usage output is observed;
- `sleep 10` returns and `LAB_REQ_02_OK` is observed within the bounded window.

The pinned base repo does not contain MIT's course-fork `grade-lab-util`, so that grader is **NOT RUN** unless a separately provenance-verified grader source is intentionally introduced later.

### 6. Reset

```bash
./reset.sh
```

Reset is scoped to this dedicated worktree/process group and returns the tree to the exact clean pin.

## Fallback

If QEMU or the cross-toolchain is unavailable, use `verify_source_route.py` plus `fallback_trace.md`.

**Fallback != runnable Required Lab completion.** Report build/QEMU/grader separately as PASS / FAIL / NOT RUN / BLOCKED.
