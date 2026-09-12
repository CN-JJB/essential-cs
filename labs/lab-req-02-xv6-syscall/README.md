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
- missing-argument usage output (`Usage: sleep ticks`) is observed as command output;
- `sleep 10` returns to a subsequent shell prompt;
- `echo LAB_REQ_02_OK` produces an execution-only output line exactly `LAB_REQ_02_OK`, not merely the echoed command text, followed by the next prompt;
- the owned QEMU process group is terminated/reaped and the PID marker is removed.

The pinned base repo does not contain MIT's course-fork `grade-lab-util`, so that grader is **NOT RUN** unless a separately provenance-verified grader source is intentionally introduced later.

### 6. Reset

```bash
./reset.sh
```

Reset is scoped to this dedicated worktree/process group and returns the tree to the exact clean pin.

## Prerequisites

- Hard prerequisites: M06 (`L06-01` syscall boundaries & execution contexts, `L06-02` trap handling).
- Toolchain: RISC-V cross-compiler (`riscv64-unknown-elf-gcc` or `riscv64-linux-gnu-gcc`), QEMU (`qemu-system-riscv64`), git (checked by `./preflight.sh`).

## Prediction-Before-Observation

1. Does `user/sleep.c` invoke the kernel function `sys_pause` directly across memory space? Predict how user-space transitions into supervisor mode via `ecall`.
2. If `sleep` is invoked without arguments, predict the program's output and exit status.

## Exit Criteria

- `./preflight.sh` passes or truthfully records missing host tools.
- `python3 verify_source_route.py worktree` verifies source anchors for `pause`/`sys_pause`/`ecall`.
- `./smoke.sh` completes successfully: xv6 compiles, boots in QEMU, executes `sleep 10`, reaps QEMU process group cleanly.
- Record evidence in `course/evidence/lab-req-02-evidence-template.md`.

## Provenance & Attribution

- Upstream: MIT 6.1810 Operating System Engineering (Fall 2025).
- Upstream repo: `https://github.com/mit-pdos/xv6-riscv.git` @ `35b088427ef37611c38afdeed5a52a278cae38f9`.
- License: MIT license in upstream `LICENSE`. All guidance and smoke scripts are Essential CS originals.

## Fallback

If QEMU or the cross-toolchain is unavailable, use `verify_source_route.py` plus `fallback_trace.md`.

**Fallback != runnable Required Lab completion.** Report build/QEMU/grader separately as PASS / FAIL / NOT RUN / BLOCKED.
