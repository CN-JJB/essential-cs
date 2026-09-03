# LAB-REQ-02 Source Pin & Route Specification

## Canonical Upstream
- **Upstream Course:** MIT 6.1810 Operating System Engineering (Fall 2025)
- **Official Repository:** `https://github.com/mit-pdos/xv6-riscv.git`
- **Pinned Commit:** `35b088427ef37611c38afdeed5a52a278cae38f9`
- **Commit Date:** Thu Nov 20 20:03:04 2025 -0500
- **Commit Title:** `test for nlink overflow`

---

## Licensing & Provenance Contract
- **xv6 Software Code:** Covered by the MIT License (see `LICENSE` in the official repository). The copyright and permission notice must be retained in any source distribution.
- **MIT 6.1810 Lab Page:** (`https://pdos.csail.mit.edu/6.1810/2025/labs/util.html`). Reusable license is not independently verified in Lead review. The assignment web page is treated as **link/reference only**.
- **Essential CS Originality:** All instructional text, explanations, step-by-step tasks, and evidence rubrics in Essential CS are 100% original prose and diagrams authored for this curriculum.

---

## The Verified Fall 2025 Syscall Route

In the Fall 2025 xv6-riscv repository, the user-level utility is `sleep`, but the underlying system call implemented in the kernel is named **`pause(int ticks)`**.

### Exact Source Route Anchors

1. **User Space Program (`user/sleep.c`):**
   The learner-authored utility parses arguments and calls `pause(ticks)`.

2. **User Space Library Declaration (`user/user.h`):**
   ```c
   int pause(int);
   ```

3. **Syscall Stub Generator (`user/usys.pl`):**
   ```perl
   entry("pause");
   ```
   Generates assembly stub in `user/usys.S`:
   ```assembly
   .global pause
   pause:
    li a7, SYS_pause
    ecall
    ret
   ```
   Loads system call number into register `a7` and executes RISC-V `ecall`.

4. **System Call Number Definition (`kernel/syscall.h`):**
   ```c
   #define SYS_pause  13
   ```
   *(Note: The stale `SYS_sleep` does not exist in this tree).*

5. **Kernel Dispatcher Table (`kernel/syscall.c`):**
   ```c
   extern uint64 sys_pause(void);
   ...
   [SYS_pause]   = sys_pause,
   ```

6. **Trap Entry & Return (`kernel/trampoline.S` & `kernel/trap.c`):**
   - `trampoline.S` saves user registers into `p->trapframe` and switches to kernel page table.
   - `usertrap()` in `kernel/trap.c` checks `r_scause() == 8` (Environment call from U-mode).
   - Increments program counter: `p->trapframe->epc += 4;`.
   - Invokes `syscall()` in `kernel/syscall.c`.

7. **Kernel Implementation (`kernel/sysproc.c`):**
   ```c
   uint64
   sys_pause(void)
   {
     int n;
     argint(0, &n);
     sleep_prepare(&ticks);
     while(ticks - ticks0 < n){
       if(killed(myproc())){
         sleep_finish();
         return -1;
       }
       sleep();
     }
     sleep_finish();
     return 0;
   }
   ```
   Puts the process to sleep waiting on timer ticks, then returns $0$ in register `a0`.

---

## Important Architectural Distinctions
- **xv6 `pause(ticks)` vs POSIX `pause(2)`:** In POSIX, `pause()` takes no arguments and sleeps until a signal is received. In xv6, `pause(ticks)` takes an integer parameter and pauses for that number of timer clock ticks.
- **RISC-V `ecall` vs x86 `syscall`:** `ecall` raises a RISC-V environment-call exception. In the pinned xv6 path, the configured supervisor trap vector/handler receives that U-mode exception and the kernel handles it in S-mode. Do not teach `ecall` as a universal OS syscall instruction.
- **Ticks vs Wall-Clock Time:** xv6 `ticks` count timer interrupts in the teaching OS. Under QEMU, observed wall-clock duration depends on the emulator and host scheduling; do not equate a tick count with a universal number of real seconds.
