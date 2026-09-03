# LAB-REQ-02 Fallback / Recorded Evidence

> **Boundary:** This file is fallback/reference evidence. Reading it is **not equivalent** to successfully running LAB-REQ-02. A completion report using only this path must say `source inspection / fallback`, with build/QEMU/grader listed separately as NOT RUN or BLOCKED.

## Provenance

The xv6 portions below are tied to:

- Upstream: `https://github.com/mit-pdos/xv6-riscv.git`
- Pinned commit: `35b088427ef37611c38afdeed5a52a278cae38f9`
- Author runtime used for the recorded xv6 build/QEMU evidence: WSL2 Linux x86-64
- Cross compiler: `riscv64-linux-gnu-gcc 13.3.0`
- QEMU: `qemu-system-riscv64 8.2.2`

The absolute instruction addresses from any disassembly are **recorded build output, not curriculum constants**.

## Recorded xv6 disassembly relation

The author build of `user/_sleep` showed the relation:

```text
main
  ...
  jal ... <pause>
  ...

<pause>:
  li a7, 13
  ecall
  ret
```

At the pinned source, `kernel/syscall.h` defines `SYS_pause 13`. The stable lesson evidence is the **relation** `main -> pause stub -> SYS_pause -> ecall`, not an absolute address.

RISC-V `ecall` raises an environment-call exception. In xv6, before returning to user mode, `stvec` is configured to the trampoline `uservec` entry; the trap path then reaches `usertrap()` and `syscall()`.

## Recorded QEMU execution shape

The author's WSL/QEMU run reached the xv6 shell and exercised both the missing-argument and bounded-tick paths:

```text
xv6 kernel is booting
...
init: starting sh
$ sleep
Usage: sleep ticks
$ sleep 10
$ echo done
done
```

`sleep 10` means **10 xv6 timer ticks**. Do not convert that to a universal wall-clock duration; QEMU scheduling and host load affect elapsed wall time.

## Native Linux comparison — not observed in the author environment

The author environment for this PR did **not** have `strace`. Therefore this file does not present a native Linux trace as “observed”.

If your environment has functional `strace`, run and record the actual sleep-related syscall(s), for example:

```bash
strace -e trace=nanosleep,clock_nanosleep sleep 1
```

Depending on libc/kernel/tooling, you may observe `clock_nanosleep`, `nanosleep`, or a different implementation path. Record what actually occurred. This comparison is transfer evidence, not a substitute for the xv6 Required Lab.
