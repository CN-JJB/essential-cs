# Runtime, OS & Persistence Research Dossier v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #47 — [Post-Blueprint] Runtime, OS & Persistence Research Dossier (M05–M09)
Repository state researched: `main @ 9e38e8f5540d68e64083315394233353fe757069`
Checked date for current implementation/practice claims: **2026-09-02**
Role: Research Agent — Curriculum Mechanism, Source & Implementation-Feasibility Researcher
Scope: Research step only; no Lesson prose, runnable Lab implementation, Mini Cloud App implementation, Blueprint redesign, or Open Question closure.

---

## Evidence-Layer Legend

This dossier strictly follows the repository source policy (`meta/RESEARCH_AND_SOURCE_POLICY.md`):

- **PRINCIPLE** — stable mechanism, theory, or reasoning pattern independent of a specific product or version.
- **SPECIFICATION** — normative or official contract from a formal standard, language specification, ABI, protocol, or system interface definition.
- **IMPLEMENTATION** — actual tool, runtime, compiler, or kernel behavior within a named environment.
- **CURRENT PRACTICE** — replaceable present-day convention, product choice, cost model, or operational pattern subject to periodic change.

Confidence and context labels:

- **ESTABLISHED** — strongly supported by stable primary/authoritative evidence and consensus systems practice.
- **IMPLEMENTATION-SPECIFIC** — valid only for the named implementation, toolchain, version, or environment.
- **CURRENT-PRACTICE** — useful at the checked date (2026-09-02) but expected to require scheduled review.
- **CONTESTED** — credible sources, specifications, or implementations disagree under comparable assumptions.
- **UNCERTAIN** — evidence is incomplete or the design choice requires empirical implementation testing.

---

## 1. Executive Recommendation / Readiness

**Recommendation: READY FOR DESIGN**

This Research Dossier provides the complete technical, pedagogical, tooling, environment, lab provenance, and boundary evidence required to design the five Modules of the second macro Core slice without guesswork:

$$\text{M05 (Languages/Runtime)} \longrightarrow \text{M06 (Processes/Syscalls)} \longrightarrow \text{M07 (Virtual Memory)} \longrightarrow \text{M08 (Files/Filesystems)} \longrightarrow \text{M09 (Durable Storage)}$$

### Key Findings and Invariant Alignment

1. **Architecture Integrity Preserved:** No new canonical concept IDs, no new Big Ideas, and no new competencies are introduced. All 4 canonical first homes are strictly preserved:
   - M06 `L06-01`: **EC-CON-018 Process**
   - M07 `L07-01`: **EC-CON-013 Isolation**
   - M07 `L07-01`: **EC-CON-017 Trust Boundary**
   - M09 `L09-01`: **EC-CON-016 Durability**
2. **LAB-REQ-02 Re-Audit Complete:** MIT 6.1810 `sleep` syscall exercise remains the best bounded Required Lab for user-to-kernel crossing. Licensing is verified (MIT License for xv6 software source; CC BY 3.0 US for lab page text). Setup burden in standard Linux Dev Containers requires only `qemu-system-misc` and `gcc-riscv64-linux-gnu`. A short non-compiling M08 revisit inspects xv6's `sysfile.c`/`file.c` to contrast VFS abstractions without duplicating the lab. A deterministic trace fallback is specified for constrained environments.
3. **Environment & OQ-BP-006 Baseline Feasible:** The canonical Linux toolchain (Python 3.12, GCC 13/14, GNU binutils, `strace`, `ps`/procfs, QEMU RISC-V) is feasible and unprivileged for nearly all exercises. Potential container restriction on `strace` (`SYS_PTRACE`) is documented with non-privileged fallback paths.
4. **M03 GDB Debt Decoupled:** The known verification debt from M03 (GDB unavailable in author/Lead environments) does not block M05–M09. M05 and M06 use disassembly, Python standard introspection (`dis`, `ast`), `strace`, and procfs rather than interactive GDB session stepping.
5. **Durability and Security Boundaries Hardened:**
   - *Security:* Isolation (limits visibility/interference) and Trust Boundary (marks changes in authority/enforcement responsibility) are strictly separated.
   - *Durability:* Durability is defined under explicit failure models. The dossier enforces a strict 5-layer buffer hierarchy (Language Runtime $\rightarrow$ libc Buffer $\rightarrow$ Kernel Page Cache $\rightarrow$ Filesystem Journal $\rightarrow$ Storage Controller Cache $\rightarrow$ Non-Volatile Media). No learner activity may claim `write()` success or file existence implies persistence across power failure.

---

## 2. Scope and Canonical Constraints

### 2.1 Scope Chain and Module Definitions

| Module | Canonical Name | Preliminary Lessons | Hard Prereqs | Soft/Pref Prereqs | Canonical Concept First Home | Primary Competency |
|---|---|---|---|---|---|---|
| **M05** | Languages, VM & Compiler Pipeline | L05-01: Source to Machine<br>L05-02: Grammar, AST & Runtime<br>L05-03: Types as Invariants | M03 | M04 | None (revisits Abstraction, Interface, Representation) | Explain (Trace, Learn-New-Tech, Observe) |
| **M06** | Processes, Syscalls & Execution Context | L06-01: Program to Process<br>L06-02: Fork, Exec & Exit<br>L06-03: Scheduling & CPU Sharing | M03 | M05 | **EC-CON-018 Process** | Trace (Observe, Diagnose, Explain) |
| **M07** | Virtual Memory & Isolation | L07-01: Virtual Memory & Page Tables<br>L07-02: Heap, Malloc & OOM<br>L07-03: Page Faults & Protection | M06, M04 | None | **EC-CON-013 Isolation**<br>**EC-CON-017 Trust Boundary** | Explain (Trace, Diagnose, Estimate) |
| **M08** | Files, Filesystems & System I/O | L08-01: File API, FD & Inode<br>L08-02: Page Cache & Buffered I/O<br>L08-03: I/O Failures & Permissions | M06 | M07 | None (revisits Interface, State, Caching, Locality) | Trace (Explain, Observe, Diagnose) |
| **M09** | Storage Engine & Durable Storage | L09-01: Durability, fsync & WAL<br>L09-02: SSD vs HDD Mechanics<br>L09-03: Storage Classes & Cost Model | M08 | M04 | **EC-CON-016 Durability** | Judge (Estimate, Explain, Diagnose) |

### 2.2 Canonical Concept Registry Constraints

No new concept IDs are permitted in this research slice. The canonical boundaries to preserve are:

- **EC-CON-018 Process (进程):** "A managed execution context with identity, resources, and normally an address-space boundary through which a program runs. It is not source code, a thread, a container image, or a virtual machine." Introduced in M06 `L06-01`.
- **EC-CON-013 Isolation (隔离):** "Limiting interference or visibility between executions, identities, resources, or fault domains. Isolation can support security or correctness but does not alone establish either." Introduced in M07 `L07-01`. M06 process boundaries serve as a concrete preview only.
- **EC-CON-017 Trust Boundary (信任边界):** "A boundary where authority, trust assumptions, or enforcement responsibility changes; inputs crossing it need explicit validation/authorization and outputs need bounded exposure." Introduced in M07 `L07-01`. Virtual memory/kernel privilege separation provides the first concrete protection boundary. Research must explicitly separate isolation from trust boundary.
- **EC-CON-016 Durability (持久性):** "A committed state survives a named restart or failure bound. Durability is a claim about a failure model, not a synonym for backup, replication, availability, or 'written to a file'." Introduced in M09 `L09-01`.

### 2.3 Competency Progression Constraints

Only the 8 canonical competencies (`meta/COMPETENCY_MATRIX.md`) are used:

- **M05:** Primary: **Explain** (compilation/interpretation pipeline). Growth: **Trace** (source $\rightarrow$ AST $\rightarrow$ bytecode/machine code), **Learn-New-Tech** (verify language/runtime claim from authoritative documentation or source), **Observe** (bytecode disassembly).
- **M06:** Primary: **Trace** (user code $\rightarrow$ libc stub $\rightarrow$ syscall trap $\rightarrow$ kernel dispatch $\rightarrow$ return). Growth: **Observe** (`strace`, `ps`, `/proc`), **Diagnose** (process exit status, zombie, blocked on I/O), **Explain** (scheduling intuition, PCB).
- **M07:** Primary: **Explain** (virtual address translation, why isolation works). Growth: **Trace** (virtual address $\rightarrow$ page table $\rightarrow$ physical frame), **Diagnose** (segmentation fault, OOM killer), **Estimate** (process memory layout/overhead).
- **M08:** Primary: **Trace** (file read/write path through fd, VFS, page cache, inode, block device). Growth: **Explain** (filesystem organization, page cache role), **Observe** (`strace` file operations, file descriptor tables in `/proc`), **Diagnose** (permission denied, disk full, missing path).
- **M09:** Primary: **Judge** (durability guarantees vs performance/cost trade-offs). Growth: **Estimate** (storage cost per GB, IOPS/latency orders of magnitude), **Explain** (journaling/WAL, write amplification, wear leveling), **Diagnose** (data loss scenarios upon crash/power loss).

---

## 3. Cross-Module Mechanism Chain M05 $\rightarrow$ M09

The five modules form a continuous, cohesive systems journey tracing an application operation from high-level source text down to non-volatile physical storage:

```
+-------------------------------------------------------------------------+
| M05: Language & Runtime                                                 |
| Python/C Source Text -> Parser -> AST -> Bytecode/Machine Instructions  |
| Runtime VM execution loop & Memory allocation request                   |
+------------------------------------+------------------------------------+
                                     | Execution triggers OS service
                                     v
+------------------------------------+------------------------------------+
| M06: Process & Syscalls                                                 |
| Process context (PID, PCB, State) -> libc stub -> SYSCALL instruction   |
| CPU Privilege Transition: User Mode (Ring 3) -> Kernel Mode (Ring 0)    |
+------------------------------------+------------------------------------+
                                     | System runs under Virtual Memory
                                     v
+------------------------------------+------------------------------------+
| M07: Virtual Memory & Isolation                                         |
| Linear Virtual Address Space -> MMU & Page Table Walk -> Physical Frame |
| Protection Bits (R/W/X) -> Isolation & Trust Boundary Enforcement       |
+------------------------------------+------------------------------------+
                                     | Syscall performs File I/O
                                     v
+------------------------------------+------------------------------------+
| M08: Files & System I/O                                                |
| File Descriptor -> Kernel Struct File -> VFS -> Inode Resolution        |
| Page Cache Buffering (Dirty Pages in RAM) -> Block Device Queue         |
+------------------------------------+------------------------------------+
                                     | Data must survive Power Failure
                                     v
+------------------------------------+------------------------------------+
| M09: Durable Storage                                                    |
| fsync / WAL commit -> Flush Controller Cache -> Physical Media (SSD/HDD)|
| Wear Leveling, FTL, Crash Consistency Bound & Storage Cost Model        |
+-------------------------------------------------------------------------+
```

---

## 4. M05 Research — Languages, VM & Compiler Pipeline

### 4.1 Capability Transition
Learners transition from viewing a programming language as "magic instructions executed directly by the computer" to understanding a language as a formal interface convention translated through a structured pipeline into execution representations (AST, IR, bytecode, machine instructions) managed by a concrete runtime.

### 4.2 Minimum Mechanism Model
1. **Language as Interface Convention:** Syntax and semantics defined by a specification (e.g., Python Language Reference, ISO C Standard), distinct from any execution engine.
2. **Translation Pipeline:**
   $$\text{Source Code Text} \xrightarrow{\text{Lexer}} \text{Tokens} \xrightarrow{\text{Parser}} \text{AST} \xrightarrow{\text{Compiler/Emitter}} \text{Target Code (Bytecode or Native)}$$
3. **AST (Abstract Syntax Tree):** A structural tree representation of source code expressing hierarchy, operations, and operands without concrete punctuation artifacts.
4. **Interpreter / VM Execution Loop:** A software loop (e.g., CPython `_PyEval_EvalFrameDefault` in `Python/ceval.c`) fetching opcodes, decoding operands, manipulating an evaluation stack or virtual registers, and invoking runtime primitives.
5. **Ahead-of-Time (AOT) vs Interpreted/JIT Execution:** AOT compilers (e.g., GCC) emit hardware machine instructions directly following the platform ABI; interpreted runtimes (e.g., CPython) execute a virtual instruction set over an abstract machine.
6. **Types as Invariants:** A type system is an enforcement mechanism for state invariants. Static types verify conformance at compile time before execution; dynamic types check tags and invariants at runtime, failing with explicit errors (`TypeError`) when invariants are violated.

### 4.3 Explicit Non-Goals
- Formal language theory, Chomsky hierarchy, context-free grammar mathematical proofs.
- Implementing a full lexer/parser generator (Lex/Yacc, ANTLR).
- Writing a full production compiler from scratch.
- Deep Garbage Collection algorithm implementations (mark-sweep, Cheney's copying, generational GC math).
- JIT compiler optimization passes (tracing JIT, deoptimization bails, SSA form).
- Multi-language survey.

### 4.4 Likely Learner Hidden Prerequisites and Support
- *Prerequisite Gap:* Learner may confuse Python language syntax with CPython binary behavior.
- *Support Needed:* Provide transparent, standard-library tools (`ast`, `dis`) that let the learner see intermediate representations directly without installing complex external compilers.

### 4.5 Candidate Real Observation / Activity
- **AST Inspection:**
  ```python
  import ast
  tree = ast.parse("total = price * 1.08")
  print(ast.dump(tree, indent=2))
  ```
- **Bytecode Disassembly & Tracing:**
  ```python
  import dis
  def calculate(price):
      return price * 1.08
  dis.dis(calculate)
  ```
  Observe `LOAD_FAST`, `LOAD_CONST`, `BINARY_OP`, and `RETURN_VALUE`.
- **Type-as-Invariant Enforcement Check:** Compare how C rejects `int x = "hello";` at compile time (static invariant check) vs Python raising `TypeError` at runtime during evaluation (dynamic invariant check).
- **Authoritative Source Verification:** Verify one documented claim from Python's official data model (e.g., object header overhead, immutable integer caching, or opcode evaluation) against live runtime inspection.

### 4.6 Required Learner Evidence
- Trace an arithmetic expression from source text to AST nodes, and to bytecode or machine instructions.
- State the difference between language syntax specification and interpreter implementation.
- Produce one verified claim from Python official documentation supported by real runtime output.

### 4.7 Evidence Layers
- **PRINCIPLE (ESTABLISHED):** Translation pipeline stages; AST as structural representation; types as invariants; interpreter evaluation loop.
- **SPECIFICATION (ESTABLISHED):** Python Language Reference (syntax, data model); ISO/IEC 9899 (C language standard).
- **IMPLEMENTATION (IMPLEMENTATION-SPECIFIC):** CPython bytecode instruction set and stack evaluation; GCC optimization flags (`-O0` vs `-O2`).
- **CURRENT PRACTICE (CURRENT-PRACTICE):** CPython 3.12/3.13 specializing adaptive interpreter (PEP 659) inserting `CACHE` entries; `dis` display format updates.

### 4.8 Authoritative Sources
- *Python Language Reference & Python Execution Model:* Python Software Foundation (checked 2026-09-02; https://docs.python.org/3/reference/executionmodel.html).
- *Python `dis` — Disassembler for Python bytecode:* Python Software Foundation (checked 2026-09-02; https://docs.python.org/3/library/dis.html).
- *Python `ast` — Abstract Syntax Tree:* Python Software Foundation (checked 2026-09-02; https://docs.python.org/3/library/ast.html).
- *Aho, Lam, Sethi, Ullman (Dragon Book):* Compilers: Principles, Techniques, and Tools (Classic reference for translation pipeline).

### 4.9 Likely Misconceptions
- *"Python executes source code directly."* $\rightarrow$ Python always compiles source text to an AST and then to bytecode before execution.
- *"Bytecode is machine code."* $\rightarrow$ Bytecode is instruction data for a software virtual machine, not executable by CPU hardware.
- *"Dynamic typing means variables don't have types."* $\rightarrow$ In Python, names reference values, and values carry concrete type tags enforced at runtime.
- *"CPython bytecode is a standard."* $\rightarrow$ Bytecode opcodes change between Python minor releases and are an implementation detail.

### 4.10 Environment & Tool Constraints
- Python 3.12/3.13 standard library (`ast`, `dis`, `sys`) requires zero external dependencies. Fully unprivileged, 100% reproducible across all Linux environments.

---

## 5. M06 Research — Processes, Syscalls & Execution Context

### 5.1 Capability Transition
Learners transition from thinking that their code "runs the computer" to realizing that a running program is an unprivileged guest process managed, isolated, and scheduled by the operating system kernel, interacting with hardware exclusively through system calls.

### 5.2 Minimum Mechanism Model
1. **Program vs Process:**
   - *Program:* Passive binary file on disk (ELF format) containing machine code, initial data, and headers.
   - *Process:* Active OS execution entity with an address space, PID, execution state (registers, program counter), open file descriptors, user credentials, and lifecycle state.
2. **CPU Execution Modes (Privilege Rings):**
   - User Mode (Ring 3 / RISC-V U-mode): Restricted instructions, memory access bounded to mapped address space.
   - Kernel Mode (Ring 0 / RISC-V S-mode): Full hardware access, control over MMU, device registers, interrupt controllers.
3. **System Call Traversal:**
   $$\text{User Code} \xrightarrow{\text{call}} \text{libc stub} \xrightarrow{\text{trap/syscall/ecall}} \text{Kernel Trap Handler} \xrightarrow{\text{table lookup}} \text{sys\_call()} \xrightarrow{\text{sysret/sret}} \text{User Code}$$
4. **Process Lifecycle Primitives:**
   - `fork()`: Duplicates the caller's execution state and address space (conceptually cloned; in Linux implemented via Copy-On-Write). Returns 0 to child, child PID to parent.
   - `execve()`: Overwrites current process address space with a new program binary, preserving PID and file descriptors (unless `O_CLOEXEC` set).
   - `exit()`: Terminates process, cleans up memory, retains exit status in Process Control Block (PCB) until reaped.
   - `waitpid()`: Parent blocks/queries child status, reaps zombie process.
5. **Scheduling Intuition:**
   - CPU multiplexing: Time-slicing via timer interrupts.
   - Process states: Ready $\rightarrow$ Running $\rightarrow$ Blocked/Waiting (on I/O, sleep, or lock).
6. **Bounded Isolation Preview:**
   - Processes cannot read or write each other's memory directly. (Canonical definition of Isolation is in M07).

### 5.3 Explicit Non-Goals
- Full kernel scheduler implementation (Linux CFS red-black trees, real-time deadlines, cgroups CPU shares).
- Kernel module programming or device driver development.
- POSIX signal mask and reentrant asynchronous signal handling deep dive.
- Multi-threaded synchronization (owned by M15).

### 5.4 Likely Learner Hidden Prerequisites and Support
- *Prerequisite Gap:* Understanding how CPU privilege transitions happen without hardware magic.
- *Support Needed:* Provide a clear, trace-focused walkthrough showing that `syscall` is just an instruction that raises the CPU privilege level and jumps to a pre-configured kernel vector table.

### 5.5 Candidate Real Observation / Activity
- **`strace` Observation of Minimal Utilities:**
  ```bash
  strace -f -e trace=process,write echo "hello"
  ```
  Observe the exact sequence: `execve`, `brk`/`mmap`, `write(1, "hello\n", 6)`, `exit_group(0)`.
- **Procfs Process Inspection:**
  Inspect `/proc/$$/status` and `/proc/$$/stat` to observe State (`R`/`S`), PPID, FD count, and memory counters.
- **Process Lifecycle Demonstration (Python or Minimal C):**
  Write a 15-line script calling `os.fork()`, printing child/parent PIDs, showing independent variable mutation, and observing zombie state before `os.wait()`.
- **LAB-REQ-02 (xv6 `sleep`):** Detailed in Section 10.

### 5.6 Required Learner Evidence
- Trace an operation crossing the user/kernel boundary, identifying user-mode code, libc wrapper, trap instruction, kernel dispatch, and return.
- Classify process states (running, blocked, zombie) from real CLI observation (`ps` / `/proc`).
- Successfully complete the bounded LAB-REQ-02 user utility and trace its kernel path.

### 5.7 Evidence Layers
- **PRINCIPLE (ESTABLISHED):** Process abstraction; user/kernel dual-mode protection; trap-based syscall boundary; time-sliced CPU multiplexing.
- **SPECIFICATION (ESTABLISHED):** POSIX.1-2024 (IEEE Std 1003.1-2024) definitions of `fork()`, `execve()`, `waitpid()`, `_exit()`.
- **IMPLEMENTATION (IMPLEMENTATION-SPECIFIC):** Linux `clone()` syscall underlying `fork()`; Linux `/proc` filesystem format; xv6 RISC-V `ecall` trap handling.
- **CURRENT PRACTICE (CURRENT-PRACTICE):** `strace` output conventions and modern glibc syscall stubs.

### 5.8 Authoritative Sources
- *POSIX.1-2024 System Interfaces (IEEE Std 1003.1-2024 / The Open Group Base Specifications Issue 8):* Austin Group (published June 14, 2024; checked 2026-09-02; https://pubs.opengroup.org/onlinepubs/9799919799/).
- *Linux Programmer's Manual — syscalls(2), fork(2), execve(2), wait(2):* Michael Kerrisk et al. (checked 2026-09-02; https://man7.org/linux/man-pages/dir_section_2.html).
- *xv6: a simple, Unix-like teaching operating system:* Russ Cox, Frans Kaashoek, Robert Morris (MIT PDOS; checked 2026-09-02; https://pdos.csail.mit.edu/6.1810/).

### 5.9 Likely Misconceptions
- *"A program and a process are the same thing."* $\rightarrow$ A program is dead bytes on disk; a process is live state in memory and kernel tables.
- *"A process runs alone on its CPU core."* $\rightarrow$ Time-slicing preempts processes hundreds of times per second via hardware timer interrupts.
- *"System calls are ordinary library functions."* $\rightarrow$ Library functions execute in user space; syscalls switch CPU hardware privilege to kernel mode.
- *"Zombie processes consume heavy CPU and RAM."* $\rightarrow$ A zombie has released all user memory; it is merely an uncollected entry in the kernel process table retaining an exit code.

### 5.10 Environment & Tool Constraints
- `strace` requires `ptrace` capability. In unprivileged Docker containers without `--cap-add=SYS_PTRACE`, `strace` may fail with `EPERM`. Fallback: trace user/kernel behavior in QEMU (xv6) or inspect `/proc/<pid>/syscall`.

---

## 6. M07 Research — Virtual Memory & Isolation

### 6.1 Capability Transition
Learners transition from a flat, naive physical memory model to understanding that all application pointers are *virtual addresses* translated on-the-fly by CPU hardware (MMU) via page tables. They discover how this mechanism provides memory protection, transparent sharing, and the foundational boundary for system isolation.

### 6.2 Minimum Mechanism Model
1. **Virtual Address Space Illusion:** Every 64-bit process sees an enormous, private, contiguous address space (e.g., $2^{48}$ bytes on typical x86-64/RISC-V architectures). Addresses 0x0000... do not point to physical RAM chip pin 0.
2. **Paging & Hardware MMU Translation:**
   - Memory is divided into fixed-size units: *Pages* (virtual, typically 4 KiB) and *Page Frames* (physical, 4 KiB).
   - *Memory Management Unit (MMU):* Hardware on the CPU that intercepts every instruction fetch and memory load/store to translate virtual page numbers (VPN) to physical frame numbers (PFN).
   - *Page Table:* Kernel-managed in-memory radix tree. Translation Lookaside Buffer (TLB) acts as a hardware cache for recent translations.
3. **Protection Bits & Permissions:**
   - Each page table entry carries permission flags: Read ($R$), Write ($W$), Execute ($X$), and User/Supervisor ($U/S$).
   - Writing to an $R\text{-only}$ page or executing an $NX$ (No-Execute) page triggers a CPU hardware exception.
4. **Page Fault Exception:**
   - When translation fails or permissions are violated, the MMU halts the instruction and triggers a Page Fault interrupt.
   - *Minor / Soft Fault:* Address is legally mapped (e.g., lazy allocation, zero-page demand allocation, Copy-On-Write), kernel allocates physical frame, updates PTE, and restarts instruction.
   - *Major / Hard Fault:* Data must be fetched from disk (swapped page or file-backed mmap).
   - *Invalid Fault:* Address not mapped or violates permissions $\rightarrow$ kernel delivers `SIGSEGV` (Segmentation Fault).
5. **Address Space Layout:**
   $$\text{Text (Code: r-x)} \;\vert\; \text{Data/BSS (rw-)} \;\vert\; \text{Heap (grows up)} \;\vert\; \dots \;\vert\; \text{Memory Mapped (mmap)} \;\vert\; \dots \;\vert\; \text{Stack (grows down)}$$
6. **Heap Allocation & OOM:**
   - `malloc()` in user space manages memory chunks over coarse kernel pages requested via `brk()` or `mmap()`.
   - Memory leaks exhaust address space or physical RAM/swap.
   - When RAM + swap are exhausted, the Linux Out-Of-Memory (OOM) killer selects and terminates a process based on heuristic badness scores.

### 6.3 Security Boundary: Isolation vs Trust Boundary
This module hosts the canonical first homes for two related but distinct concepts:
- **EC-CON-013 Isolation:** Limiting interference or visibility between executions or resources.
  *Mechanism:* Separate page tables ensure Process A physically cannot reference or alter Process B's memory.
- **EC-CON-017 Trust Boundary:** A boundary marking a change in authority, trust assumptions, or enforcement responsibility.
  *Mechanism:* User space vs Kernel space. The kernel does not trust user pointers; every syscall input must be validated before dereference.
- **Crucial Distinction:**
  - *Isolation $\neq$ Trust Boundary:* Two processes running under the same user account (e.g., two tabs or background tasks) are memory-isolated by page tables, but they may share the same trust boundary (one can send signals, inspect the other via procfs, or attach a debugger if permitted). Conversely, kernel and user process share the same physical computer, but a strict trust boundary governs all parameter passing across syscall entry.

### 6.4 Explicit Non-Goals
- Exploitation techniques (stack smashing, ROP gadgets, ASLR bypasses).
- Hand-implementing 4-level or 5-level page table walks (CR3, PGD, P4D, PUD, PMD, PTE math).
- In-depth virtual memory replacement policy algorithms (LRU clock hand, active/inactive lists).
- Container isolation mechanisms (namespaces, cgroups — reserved for M19).

### 6.5 Candidate Real Observation / Activity
- **Inspecting Process Memory Maps:**
  ```bash
  cat /proc/self/maps
  ```
  Examine readable, writable, executable segments, stack, heap, and shared library mappings.
- **Triggering and Classifying a Safe Page Fault:**
  Run a small C program or Python ctypes script that attempts to write to a string literal or NULL pointer, observing the resulting `SIGSEGV` and examining `dmesg` or exit status.
- **Minor vs Major Page Fault Observation:**
  Use Python `resource.getrusage(resource.RUSAGE_SELF)` to observe `ru_minflt` increasing as a large array is allocated and written for the first time (demand zero-paging).
- **Safe Heap Allocation Observation:**
  Observe virtual memory allocation (`VSZ`) vs resident set size (`RSS`) via `ps` or `/proc/<pid>/status` during incremental memory allocation.

### 6.6 Required Learner Evidence
- Read a real `/proc/<pid>/maps` output and identify the text, heap, stack, and dynamic library regions with their permissions.
- Explain the causal chain from a bad address dereference to MMU hardware fault, kernel signal delivery, and process termination.
- Explain in writing why memory isolation between two processes does not automatically mean they have different trust boundaries.

### 6.7 Evidence Layers
- **PRINCIPLE (ESTABLISHED):** Virtual memory abstraction; page-based address translation; page fault mechanism; isolation vs trust boundary distinction.
- **SPECIFICATION (ESTABLISHED):** POSIX `mmap()`, `mprotect()`, `munmap()`; SysV ABI process memory layout conventions.
- **IMPLEMENTATION (IMPLEMENTATION-SPECIFIC):** Linux 48-bit virtual address split; Linux `/proc/<pid>/maps` schema; Linux OOM killer heuristics (`/proc/<pid>/oom_score`).
- **CURRENT PRACTICE (CURRENT-PRACTICE):** 4 KiB standard page size on x86-64 and RISC-V (with Transparent Huge Pages as optional kernel behavior).

### 6.8 Authoritative Sources
- *Linux Kernel Documentation — Page Table Management & Overcommit Accounting:* (checked 2026-09-02; https://docs.kernel.org/admin-guide/mm/index.html).
- *Intel 64 and IA-32 Architectures Software Developer's Manual, Volume 3A: System Programming Guide (Paging & Protection):* Intel Corporation.
- *OSTEP (Operating Systems: Three Easy Pieces) Chapters 13–20:* Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau (Virtualization of Memory).

### 6.9 Likely Misconceptions
- *"Pointers hold physical RAM addresses."* $\rightarrow$ All user-space pointers are virtual addresses.
- *"Allocating 1 GB with malloc immediately claims 1 GB of physical RAM."* $\rightarrow$ Kernel uses optimistic demand paging; physical memory is allocated only when pages are first touched (minor page fault).
- *"Isolation is the same as security."* $\rightarrow$ Isolation prevents accidental or unauthorized memory sharing, but without proper trust-boundary parameter validation, privileged services can be tricked into performing unauthorized actions.
- *"A segmentation fault means physical memory is corrupted."* $\rightarrow$ A segfault is a software protection event triggered by the MMU catching an illegal virtual address translation.

---

## 7. M08 Research — Files, Filesystems & System I/O

### 7.1 Capability Transition
Learners transition from thinking that `file.write()` directly writes bytes to disk platters/flash chips to understanding the layered POSIX I/O architecture: user-space buffering $\rightarrow$ file descriptors $\rightarrow$ kernel VFS $\rightarrow$ inodes/metadata $\rightarrow$ kernel page cache $\rightarrow$ block device abstraction.

### 7.2 Minimum Mechanism Model
1. **File as an Abstraction:** A linear, byte-addressable stream of data managed by an interface (`open`, `read`, `write`, `lseek`, `close`, `stat`).
2. **File Descriptors and Kernel Tables:**
   - *File Descriptor (FD):* A small non-negative integer indexing a process-local file descriptor table.
   - *Open File Description (Kernel Table):* Holds file status flags (e.g., `O_RDONLY`, `O_APPEND`), current byte offset, and a reference count.
   - *Inode / Vnode:* Filesystem metadata object holding file size, permissions, owner, timestamps, and block location pointers.
   - *Decoupling:* Multiple FDs (via `dup()` or `fork()`) can point to the same open file description; multiple file descriptions can point to the same underlying inode.
3. **Directory and Path Resolution:**
   - A directory is a file containing directory entries (`dirent`: filename $\rightarrow$ inode number mapping).
   - Hard links: multiple directory entries referencing the same inode number.
   - Path resolution traverses root `/` or current working directory inode-by-inode.
4. **Linux Page Cache:**
   - The kernel caches file blocks in unused physical RAM.
   - On `read()`: if page is in cache (cache hit), data is copied directly to user buffer without disk I/O.
   - On `write()`: data is copied from user space to kernel page cache, and the page is marked **dirty**. The `write()` syscall returns immediately!
   - Writeback: background kernel flusher threads periodically flush dirty pages to the block device.
5. **Buffered I/O (User Space) vs System I/O:**
   - Standard C library `FILE*` (`fread`, `fwrite`, `fflush`) and Python's `io.BufferedWriter` maintain an in-process buffer (e.g., 4 KiB or 8 KiB) to minimize expensive syscall transitions.
6. **Block Device Boundary:**
   - The filesystem interacts with block devices in fixed sector/block sizes (e.g., 512 bytes or 4 KiB).
7. **I/O Failures and Invariants:**
   - Permission failure (`EACCES`), missing path (`ENOENT`), disk full (`ENOSPC`), file table exhaustion (`EMFILE`/`ENFILE`).

### 7.3 Explicit Non-Goals
- Full on-disk filesystem layout implementation (ext4 block groups, extent trees, inode tables from scratch).
- Implementing FUSE (Filesystem in Userspace) drivers.
- Linux `io_uring` advanced kernel asynchronous ring buffers.
- Durability claims (M08 ends at the block device boundary; durability guarantees belong strictly to M09).

### 7.4 Candidate Real Observation / Activity
- **Tracing File I/O Syscalls:**
  ```bash
  strace -e trace=openat,read,write,close,fstat python3 -c '
  with open("test.txt", "w") as f:
      f.write("hello world\n")
  '
  ```
  Observe `openat`, user-buffer accumulation, `write`, and `close`.
- **Inspecting File Descriptors via Procfs:**
  Inspect `/proc/$$/fd/` to see open file descriptors and their target files/pipes/sockets.
- **Inode & Hard Link Inspection:**
  Use `stat` and `ls -li` to inspect inode numbers, link counts, and demonstrate that deleting (`unlink`) one path does not destroy file data if another hard link exists.
- **Observing the Page Cache with `vmstat`:**
  Observe `cache` and `dirty` memory counters changing in `/proc/meminfo` or `vmstat` during large file writes.
- **Revisit LAB-REQ-02:** Short code inspection of xv6's `sysfile.c` and `file.c` to see how a minimal OS handles file descriptors and inodes (details in Section 10).

### 7.5 Required Learner Evidence
- Trace a file write operation through the five layers: language buffer $\rightarrow$ syscall $\rightarrow$ file descriptor $\rightarrow$ page cache $\rightarrow$ block device.
- Diagnose three distinct I/O errors (`EACCES`, `ENOENT`, `ENOSPC`) from error codes and system logs.
- Distinguish between a file descriptor, an open file description, and an inode.

### 7.6 Evidence Layers
- **PRINCIPLE (ESTABLISHED):** File descriptor indirection; inode metadata decoupling; directory path resolution; page cache read/write buffering.
- **SPECIFICATION (ESTABLISHED):** POSIX.1-2024 Base Definitions & System Interfaces for file I/O (`open`, `read`, `write`, `close`, `lseek`, `stat`, `unlink`).
- **IMPLEMENTATION (IMPLEMENTATION-SPECIFIC):** Linux Virtual File System (VFS); Linux page cache page/folio dirtying and writeback algorithms; Ext4 extent tree structures.
- **CURRENT PRACTICE (CURRENT-PRACTICE):** Default Linux glibc 8 KiB buffer size for `stdio`; modern `openat()` replacing legacy `open()`.

### 7.7 Authoritative Sources
- *POSIX.1-2024 System Interfaces (openat, read, write, close, stat):* IEEE Std 1003.1-2024 (checked 2026-09-02; https://pubs.opengroup.org/onlinepubs/9799919799/).
- *Linux Kernel Documentation — The Virtual Filesystem (VFS):* (checked 2026-09-02; https://docs.kernel.org/filesystems/vfs.html).
- *Linux Kernel Documentation — Page Cache and Writeback:* (checked 2026-09-02; https://docs.kernel.org/admin-guide/mm/index.html).
- *OSTEP Chapters 39–41:* Files and Directories, File System Implementation, Locality and FFS.

### 7.8 Likely Misconceptions
- *"Calling `write()` writes bytes to the disk drive."* $\rightarrow$ `write()` copies bytes into the Linux kernel page cache; physical writeback happens asynchronously seconds later.
- *"A file's name is stored in its inode."* $\rightarrow$ Inodes store file metadata and data block pointers; filenames live in directory entries (`dirent`).
- *"Deleting a file immediately frees its disk blocks."* $\rightarrow$ Deleting unlinks the name from a directory; blocks are freed only when the inode's link count reaches zero AND all open file descriptors referencing it are closed.
- *"File descriptors are global across all programs."* $\rightarrow$ FDs are process-local integers indexing a per-process descriptor table.

---

## 8. M09 Research — Storage Engine & Durable Storage

### 8.1 Capability Transition
Learners transition from naively assuming that "saved to a file means permanent" to exercising rigorous technical judgment regarding what constitutes **Durability** under explicit crash and power-loss failure models, navigating the trade-offs between sync overhead, storage media physics (SSD vs HDD), and storage architectures.

### 8.2 Minimum Mechanism Model
1. **EC-CON-016 Durability Defined Under Failure Bounds:**
   - Durability is a guarantee that committed state survives a named failure bound (e.g., process crash, OS kernel panic, sudden power loss).
   - Durability is NOT a synonym for backup, replication, or high availability.
2. **The Durability Journey (The 5-Layer Buffer Stack):**
   ```
   [ Application Runtime Buffer (e.g. Python io.BufferedWriter) ]
        |  1. flush()
        v
   [ C Standard Library Buffer (libc stdio) ]
        |  2. fflush() -> write() syscall
        v
   [ Operating System Page Cache (Dirty RAM Pages) ]
        |  3. fsync() / fdatasync()
        v
   [ Storage Controller Volatile Cache (DRAM on SSD/HDD) ]
        |  4. SYNCHRONIZE CACHE / NVMe Flush command
        v
   [ Non-Volatile Storage Media (NAND Flash / Magnetic Platters) ]
   ```
   *Failure Consequence:*
   - Power loss at Stage 1, 2, or 3: Data in RAM is completely lost.
   - Power loss at Stage 4: Data in drive controller DRAM is lost unless the drive possesses Power Loss Protection (PLP) hardware capacitors.
   - Only upon Stage 5 completion is physical persistence achieved.
3. **Synchronization Primitives:**
   - `fsync(fd)`: Forces dirty page-cache pages and file metadata (size, modification time, inode updates) to be written out to the storage device and issues a device cache flush command.
   - `fdatasync(fd)`: Flushes file data and only the metadata strictly necessary to retrieve the data (e.g., file size change), omitting non-critical attributes like `mtime` to save an extra disk write.
4. **Crash Consistency & The Multi-Block Problem:**
   - Updating a file involves writing user data blocks, updating the inode, and updating the filesystem allocation bitmap.
   - These writes cannot occur simultaneously on physical hardware. A crash midway leaves the filesystem corrupted.
   - *Journaling (WAL - Write-Ahead Logging):* Transactions are appended sequentially to a dedicated log region, committed with a checksum, and then lazily checkpointed to final on-disk locations. On reboot after crash, the journal is replayed.
5. **Storage Media Mechanics (SSD vs HDD):**
   - *HDD (Hard Disk Drive):* Mechanical platters, moving heads. Random access incurs seek time ($\sim 5\text{--}10\text{ ms}$) and rotational latency. Sequential access is orders of magnitude faster than random access.
   - *SSD (Solid State Drive / NAND Flash):* Semiconductor flash memory. No moving parts.
     - *Asymmetry:* Reads and writes occur in **pages** ($4\text{--}16\text{ KiB}$); erases occur only in **blocks** (e.g., $128\text{--}512\text{ pages}$, several MiB). Cannot overwrite in place!
     - *Flash Translation Layer (FTL):* Controller firmware managing dynamic Logical Block Address (LBA) to physical flash page mappings.
     - *Garbage Collection & Write Amplification Factor (WAF):*
       $$\text{WAF} = \frac{\text{Bytes Written to NAND Flash}}{\text{Bytes Written by Host}}$$
     - *Wear Leveling:* NAND flash cells tolerate a finite number of Program/Erase (P/E) cycles before oxide breakdown (e.g., TLC: $\sim 1{,}000\text{--}3{,}000$ cycles). The FTL distributes writes across all physical blocks to prevent premature drive failure.
6. **Storage Architecture Taxonomy:**
   - *Block Storage:* Raw LBA-indexed blocks (e.g., local NVMe, AWS EBS). Mounted by filesystems. Low latency, high IOPS, single-host attachment.
   - *File Storage:* Hierarchical files and directories via POSIX interface (e.g., local filesystem, NFS). Managed metadata.
   - *Object Storage:* Flat key-value store accessed over HTTP/REST (e.g., AWS S3, MinIO). Immutable objects, eventual consistency models historically, highly scalable, higher per-request latency ($\sim 10\text{--}50\text{ ms}$), significantly lower cost per GB.
7. **Storage Cost & Latency Model (CURRENT PRACTICE):**
   - Latency and pricing figures are illustrative current practice, not permanent constants:
     - Register/L1 cache: $\sim 1\text{ ns}$
     - RAM: $\sim 50\text{--}100\text{ ns}$
     - NVMe SSD random read: $\sim 10\text{--}50\ \mu\text{s}$
     - HDD random seek: $\sim 5\text{--}10\text{ ms}$ ($\sim 100{,}000\times$ slower than RAM)
     - Object storage HTTP GET: $\sim 20\text{--}100\text{ ms}$
     - Cost per GB: NVMe SSD ($\sim \$0.10\text{--}\$0.20/\text{GB}$) vs HDD ($\sim \$0.015\text{--}\$0.025/\text{GB}$) vs S3 Standard ($\sim \$0.023/\text{GB}$) vs Glacier Deep Archive ($\sim \$0.00099/\text{GB}$).

### 8.3 Durability Boundary: Inflexible Research Rules
Under no circumstances may any lesson or activity claim:
1. That `write()` returning success guarantees data is safe on non-volatile media.
2. That closing a file (`close()`) guarantees durability across power failure (it flushes user buffers to kernel page cache, not to physical disk).
3. That `fsync` is a substitute for backup (a disk head crash or catastrophic sector failure destroys an fsync'd file).
4. That replication across nodes provides durability under every failure (correlated power loss, shared software bugs, or network partitions can violate naive assumptions).
5. That SSDs and HDDs exhibit identical failure modes or access latency profiles.

### 8.4 Explicit Non-Goals
- Building a full database storage engine (B-Tree, LSM-Tree) from scratch (deferred to M13/M14).
- Detailed FTL firmware design or custom wear-leveling algorithm implementation.
- RAID controller hardware implementation or Reed-Solomon erasure coding math proofs.
- Commercial cloud vendor certification or product sales pitches.

### 8.5 Measurement Reuse from M04
M09 revisits the measurement discipline established in M04 `L04-02`:
- Controlled workload and explicit environment record.
- Repeated measurements when comparing I/O latencies (e.g., `fsync` overhead).
- Reporting raw numbers, medians, and variation rather than single-run flukes.
- Strict inference limits: a measured write latency on a local VM reflects that exact virtualization and host storage layer, not a universal law of hardware physics.

### 8.6 Candidate Real Observation / Activity
- **`fsync` vs Unbuffered Write Latency Measurement:**
  Write a script performing 1,000 appends with `write()` alone vs with `os.fsync()` after each write. Observe the $100\times$ to $1{,}000\times$ elapsed time penalty, demonstrating the cost of forcing physical durability.
- **Simulated Crash/Kill Observation:**
  Demonstrate a process crash (`kill -9`) vs simulated power-loss boundary using a test fixture, showing that un-`fsync`'d buffered data disappears while `fsync`'d data survives process termination.
- **Object Storage vs File I/O Interface Comparison:**
  Inspect a minimal local S3-compatible mock or public object store endpoint (HTTP PUT/GET headers, etags, immutable metadata) to contrast with POSIX byte-range file operations.

### 8.7 Required Learner Evidence
- Formulate a written judgment comparing `fsync` on every write vs batching vs periodic sync for a specified application constraint (loss tolerance vs throughput).
- Explain the difference in physical mechanism between an HDD random seek and an SSD block erase / write amplification.
- Calculate an order-of-magnitude back-of-the-envelope monthly storage cost comparing SSD, HDD, and Object Storage for a 10 TB dataset.

### 8.8 Evidence Layers
- **PRINCIPLE (ESTABLISHED):** Durability definition under explicit failure bounds; WAL/journaling atomicity; FTL wear leveling and write amplification; storage hierarchy trade-offs.
- **SPECIFICATION (ESTABLISHED):** POSIX.1-2024 `fsync()` and `fdatasync()` system interfaces; JEDEC Solid-State Drive Standards (JESD218/JESD219).
- **IMPLEMENTATION (IMPLEMENTATION-SPECIFIC):** Linux Ext4 journaling modes (`data=ordered` vs `data=journal`); NVMe controller flush commands.
- **CURRENT PRACTICE (CURRENT-PRACTICE):** Cloud storage pricing tiers (AWS EBS vs S3 Standard vs Glacier) and typical NVMe SSD latencies at the checked date (2026-09-02).

### 8.9 Authoritative Sources
- *POSIX.1-2024 System Interfaces — fsync, fdatasync:* IEEE Std 1003.1-2024 (checked 2026-09-02; https://pubs.opengroup.org/onlinepubs/9799919799/).
- *Pillai et al. (OSDI '14):* "All File Systems Are Not Created Equal: On the Complexity of Crafting Crash-Consistent Applications" (Seminal paper on fsync and crash consistency).
- *SNIA (Storage Networking Industry Association) Solid State Storage Technical Working Group:* Flash Translation Layer and Solid State Storage Architecture (checked 2026-09-02; https://www.snia.org/).
- *OSTEP Chapters 42–44:* Crash Consistency: FSCK and Journaling, Log-structured File Systems, Flash-based SSDs.

### 8.10 Likely Misconceptions
- *"If the file is visible in `ls`, it is safely on disk."* $\rightarrow$ The directory entry and inode may reside exclusively in kernel RAM cache.
- *"SSDs don't wear out because they have no moving parts."* $\rightarrow$ Flash memory cells degrade with every Program/Erase cycle due to physical oxide breakdown.
- *"Object storage is just a filesystem accessible via HTTP."* $\rightarrow$ Object storage provides a flat, key-based immutable blob store with very different latency, consistency, and cost characteristics.
- *"Cloud replication means we don't need backups."* $\rightarrow$ Replication immediately copies accidental deletions, data corruption, and ransomware to all replicas.

---

## 9. Canonical Concept First-Home Evidence

This section confirms that the four canonical first homes in this slice have complete, rigorous evidentiary backing and will not drift or conflict:

```
+-------------------------------------------------------------------------------+
| Canonical Concept First Homes in M05-M09 Slice                                |
+-------------------------------------------------------------------------------+
| M06 L06-01: EC-CON-018 Process (进程)                                         |
| -> Managed execution context (PID, PCB, address space, credentials)           |
| -> Distinct from static program code, thread, or VM container                 |
+-------------------------------------------------------------------------------+
| M07 L07-01: EC-CON-013 Isolation (隔离)                                       |
| -> Limits interference or visibility between execution/fault domains          |
| -> Enforced via hardware page tables & MMU translations                       |
+-------------------------------------------------------------------------------+
| M07 L07-01: EC-CON-017 Trust Boundary (信任边界)                               |
| -> Change in authority, trust assumptions, or enforcement responsibility      |
| -> Enforced via User/Kernel privilege transitions & strict syscall validation|
| -> Distinct from Isolation: Isolation != Trust Boundary                       |
+-------------------------------------------------------------------------------+
| M09 L09-01: EC-CON-016 Durability (持久性)                                     |
| -> Committed state survives a named restart or failure bound                  |
| -> Enforced via fsync, WAL, device cache flushes, and non-volatile media      |
| -> Distinct from availability, backup, replication, or write() success        |
+-------------------------------------------------------------------------------+
```

---

## 10. Required Lab / Activity Source Selection: LAB-REQ-02 Re-Audit

### 10.1 Obligation Summary
Per Issue #47 and `meta/blueprint/lab-source-selection-map-v0.1.md`, this dossier explicitly re-audits **LAB-REQ-02: xv6 `sleep` (User program through syscall entry)** before any Design work begins.

### 10.2 Audit Matrix

| Item | Status / Audit Finding |
|---|---|
| **Exact Official Upstream** | MIT 6.1810 Operating System Engineering (Fall 2025).<br>Course Lab Page: `https://pdos.csail.mit.edu/6.1810/2025/labs/util.html`.<br>Software Repository: `https://github.com/mit-pdos/xv6-riscv` (checked commit `35b088427ef37611c38afdeed5a52a278cae38f9`) and `git://g.csail.mit.edu/xv6-labs-2025`. |
| **Current Accessible Version / Date** | Fall 2025 course materials verified active and accessible at checked date **2026-09-02**. |
| **Licensing Boundary** | **xv6 software source:** Covered by its own MIT License. Permissive reuse/adaptation allowed provided the MIT copyright and permission notices are retained in copies.<br>**MIT 6.1810 Lab Page (`util.html`):** Carries a `rel="license"` footer to **CC BY 3.0 US**. Permits adaptation with attribution, license link, and change indication.<br>**Essential CS Rule:** All learner instructions, pedagogical explanations, and evidence prompts must be independently authored. No course prose is copied. Any bundled software retains the MIT notice. |
| **Required Architecture / Toolchain** | Architecture: RISC-V 64-bit (RV64G).<br>Toolchain: `gcc-riscv64-linux-gnu` (or `riscv64-unknown-elf-gcc`), `binutils-riscv64-linux-gnu`, `qemu-system-misc` (provides `qemu-system-riscv64`). |
| **Expected Setup Burden** | In standard Ubuntu/Debian Dev Container: `apt-get install -y qemu-system-misc gcc-riscv64-linux-gnu`. Clean build and boot time is under 15 seconds. Minimal setup friction when provided in pre-built image. |
| **Bounded Scope** | Implement ONLY user program `user/sleep.c` using the existing kernel `sleep(int ticks)` system call. Add `$U/_sleep` to `UPROGS` in `Makefile`. Run `sleep 10` in xv6 shell. Do not implement a kernel subsystem, grade server, or shell extension. |
| **Deterministic Smoke Path** | 1. Clone pinned xv6 tree.<br>2. Add `user/sleep.c` (validates argc == 2, calls `atoi(argv[1])`, invokes `sleep(n)`, calls `exit(0)`).<br>3. Add `$U/_sleep\` to `Makefile`.<br>4. Run `make qemu` or `./grade-lab-util sleep`.<br>5. Verification passes deterministically in $< 30$ seconds without network. |
| **What is Machine-Checkable** | - `make qemu` compiles without errors.<br>- Executing `sleep` with no arguments prints usage and exits with non-zero status.<br>- Executing `sleep 10` pauses process and exits with 0.<br>- Official grading script `./grade-lab-util sleep` outputs `== Test sleep, correct: OK`. |
| **What Must Be Reviewer-Judged** | - Learner's understanding of the source route: `user/sleep.c` $\rightarrow$ `user/user.h` $\rightarrow$ `user/usys.S` (sets `a7` to `SYS_sleep`, executes `ecall`) $\rightarrow$ `kernel/trampoline.S` $\rightarrow$ `kernel/trap.c:usertrap()` $\rightarrow$ `kernel/syscall.c:syscall()` $\rightarrow$ `kernel/sysproc.c:sys_sleep()`.<br>- Distinction between guest CPU ticks (timer interrupts) and host wall-clock time.<br>- Failure classification: compile error vs missing argument vs guest crash. |
| **Reset / Cleanup** | `Ctrl-A X` cleanly terminates QEMU. `make clean` or `git checkout -- .` removes generated binaries and disk image `fs.img`. Host environment state is untouched. |
| **Selection Verdict** | **CONFIRMED: The existing `sleep` syscall path remains the best bounded Required Lab.** It exposes the complete user-to-kernel trap traversal with minimal accidental complexity (no complex memory allocation or multi-page management). |
| **M08 Revisit (No Duplicate Lab)** | In M08, xv6 is revisited strictly as a **reading expedition (Source Inspection)** of `kernel/sysfile.c` and `kernel/file.c`. Learners observe how `sys_read()` and `sys_write()` map file descriptors to inodes. **No new lab or second xv6 compilation is introduced.** |
| **Fallback Evidence for Constrained Environments** | If QEMU cannot be launched (e.g., heavily restricted nested virtualization), the learner records a Linux native `strace -e trace=nanosleep` execution trace alongside a pre-recorded xv6 execution transcript, analyzing the identical user-to-kernel boundary crossing. |

---

## 11. Environment / Tool / Reproducibility Matrix (OQ-BP-006 Evidence)

### 11.1 Status of OQ-BP-006
**OQ-BP-006 remains OPEN.** This Research Dossier gathers concrete tooling feasibility evidence across M05–M09 but does not silently close or pin the canonical environment decision.

### 11.2 Tool Feasibility Matrix across M05–M09

| Tool / Component | Modules | Required for Core vs Optional | Environment-Sensitive | Privileged / Restricted | Current Version / Source Evidence | Implementation Smoke Test Required |
|---|---|---|---|---|---|---|
| **Python 3.12 / 3.13** | M05, M06, M08, M09 | **Required for Core** | No | Unprivileged | Python 3.12.3 in Ubuntu 24.04 LTS Noble; standard library `ast`, `dis`, `os`, `struct`, `time` | Yes: verify `ast.parse` and `dis.dis` work across standard scripts |
| **GCC (Native x86-64 / ARM64)** | M05, M06, M07 | **Required for Core** | Architecture-dependent | Unprivileged | GCC 13.2.0 in Ubuntu Noble; `-O0` and `-O2` code generation | Yes: compile 15-line C test programs |
| **GNU Binutils (`objdump`, `readelf`)** | M05, M06, M07 | **Required for Core** | Architecture-dependent | Unprivileged | GNU binutils 2.42 in Ubuntu Noble; disassembles native binaries | Yes: verify `objdump -d` output |
| **`strace`** | M06, M08 | **Required for Core** | Yes (Container security policy) | Restricted (requires `ptrace` or `SYS_PTRACE`) | strace 6.8 in Ubuntu Noble; traces syscalls | **Critical:** Must test in canonical Dev Container. If blocked, provide procfs fallback |
| **procfs (`/proc`) & Core CLI (`ps`, `stat`, `vmstat`, `df`)** | M06, M07, M08 | **Required for Core** | No (standard Linux) | Unprivileged | Linux kernel procfs; procps 4.0.4 | Yes: verify `/proc/self/maps` and `/proc/self/status` access |
| **QEMU & RISC-V Cross-Toolchain** | M06 (LAB-REQ-02) | **Required for Core** | Toolchain installation needed | Unprivileged (runs in user space) | `qemu-system-misc` (8.2.2), `gcc-riscv64-linux-gnu` (13.2.0) | **Critical:** Test xv6 build and QEMU boot inside container |
| **GDB** | Optional / Revisit | **Optional / Avoid Dependency** | High | Restricted (`ptrace`) | Explicit technical debt from M03 (BLOCKED/NOT RUN in author/Lead env) | Not required for M05-M09 Core path; do not introduce new GDB gates |
| **Raw Block Device Tools (`debugfs`, `fdisk`)** | M08, M09 | **Forbidden for Core** (Optional case study only) | Yes | **Requires Root/Sudo** | N/A | Use loopback file images or standard filesystem APIs instead |

### 11.3 Interaction with M03 GDB Technical Debt
During M03 verification, GDB runtime verification failed due to missing packages and container ptrace restrictions. **This dossier explicitly prevents M03's debt from propagating into M05–M09.** No Core checkpoint in M05–M09 requires interactive GDB stepping. All execution inspection is performed via static disassembly (`objdump`, `dis`), non-interactive system tracing (`strace`), or procfs introspection.

---

## 12. Source Authority Register

All sources were re-verified for availability, normative status, and version accuracy as of **2026-09-02**.

| Source / Document | Authority Class | Owner / Maintainer | Exact URL / Route | Supported Claims | Limitations & Notes |
|---|---|---|---|---|---|
| **POSIX.1-2024 (IEEE Std 1003.1-2024 / Issue 8)** | SPECIFICATION | IEEE & The Open Group (Austin Group) | `https://pubs.opengroup.org/onlinepubs/9799919799/` | Normative definitions of `fork`, `execve`, `waitpid`, `exit`, `openat`, `read`, `write`, `fsync`, `fdatasync` | Published June 14, 2024; replaces POSIX.1-2008. Focuses on interface contracts, not kernel internals. |
| **Python 3.12 / 3.13 Language Reference & Library** | SPECIFICATION & IMPLEMENTATION | Python Software Foundation | `https://docs.python.org/3/reference/` and `https://docs.python.org/3/library/` | Language execution model, AST specification, `dis` module bytecode representation | Language Reference is SPECIFICATION; `dis` opcode layout is CPython IMPLEMENTATION. |
| **Linux Kernel Documentation (v6.8 / current)** | IMPLEMENTATION / SPEC-LIKE | Linux Kernel Organization | `https://docs.kernel.org/` | VFS architecture, page cache writeback, MMU memory management, OOM killer, procfs formats | Kernel documentation reflects Linux implementation; do not generalize to all Unix/BSD/Windows kernels. |
| **MIT 6.1810 xv6 RISC-V Source & Lab Materials** | TEACHING MECHANISM & IMPLEMENTATION | MIT PDOS (Frans Kaashoek, Robert Morris, Russ Cox) | `https://pdos.csail.mit.edu/6.1810/2025/labs/util.html` and `https://github.com/mit-pdos/xv6-riscv` | LAB-REQ-02 user program through syscall route (`sleep`) | Simplified educational OS; hides modern complexity (e.g., page cache, VFS, dynamic linking). |
| **All File Systems Are Not Created Equal (OSDI '14)** | CLASSIC RESEARCH PAPER | UW-Madison (Pillai, Chidambaram, Alagappan, Arpaci-Dusseau) | USENIX OSDI 2014 proceedings | Durability vulnerabilities, fsync ordering semantics, crash consistency guarantees | Empirical study across ext3/ext4/btrfs/xfs. Demonstrates why naive file writing fails under crash. |
| **Solid State Storage Architecture & FTL Guidelines** | INDUSTRY SPECIFICATION & PRINCIPLE | SNIA (Storage Networking Industry Association) | `https://www.snia.org/education` | Flash Translation Layer (FTL), page-write/block-erase asymmetry, wear leveling, write amplification | Authoritative hardware storage industry reference. |
| **Operating Systems: Three Easy Pieces (OSTEP)** | CLASSIC TEXTBOOK | Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau | `https://pages.cs.wisc.edu/~remzi/OSTEP/` | Virtual memory paging/translation, filesystems, crash consistency, SSD mechanisms | Freely accessible online chapters; used for conceptual framing and pedagogy. |
| **Ubuntu 24.04 LTS (Noble Numbat) Package Manifest** | CURRENT PRACTICE | Canonical Ltd. | `https://packages.ubuntu.com/` | GCC 13, Python 3.12, QEMU 8.2, binutils 2.42 versions | Subject to periodic security patches; record exact digest at preflight. |

---

## 13. Licensing, Redistribution & Adaptation Constraints

1. **MIT 6.1810 xv6 Lab Material:**
   - *Software Code:* MIT License (`xv6-riscv` repo). Permitted to adapt and bundle provided copyright notices are preserved.
   - *Course Web Text:* CC BY 3.0 US (`labs/util.html`). Permitted to adapt with attribution.
   - *Essential CS Constraint:* Do NOT copy MIT assignment text. Author 100% original Essential CS instructions and evidence prompts.
2. **xv6 Book (`xv6-riscv-book`):**
   - *Constraint:* Copyright MIT / Kaashoek, Morris, Cox. Not licensed under open Creative Commons for bulk text reproduction. Cite and link only; do not copy book diagrams or text verbatim.
3. **OSTEP Textbook:**
   - *Constraint:* Available freely online for individual study; copyright Remzi and Andrea Arpaci-Dusseau. Commercial/bulk reproduction restricted. Cite as an external reference and adapt principles through original explanations and diagrams.
4. **POSIX / IEEE Standards:**
   - *Constraint:* Formal standard text is copyrighted by IEEE/The Open Group. System interface names, signatures, and semantics are fair use; do not quote large normative paragraphs. Paraphrase and cite the official Austin Group public specification URLs.
5. **Original Visuals and Diagrams:**
   - All architecture diagrams for the 5-layer buffer stack, user-to-kernel trap route, virtual address translation radix tree, and SSD flash blocks must be 100% original Essential CS SVGs/Mermaid diagrams released under CC BY-SA 4.0.

---

## 14. Misconceptions and Inference Boundaries

| Misconception | What the Learner Assumes | Technical Truth & Mechanism Boundary |
|---|---|---|
| **"Python executes without compilation"** | Code is interpreted line-by-line directly from textual source. | Python always lexes, parses to an AST, and compiles to bytecode before execution begins. |
| **"Syscall is just a library call"** | Calling `read()` is just invoking a function written by someone else. | A library call executes in user mode on the user stack; a syscall triggers a hardware trap that elevates CPU privilege to kernel mode. |
| **"Processes own physical RAM"** | Pointers in C/Python are physical wire addresses on motherboard RAM chips. | All user pointers are virtual addresses translated dynamically by the hardware MMU via kernel page tables. |
| **"Isolation equals trust"** | If two processes cannot read each other's memory, they are safe from each other. | Memory isolation limits visibility/interference; a trust boundary governs authority. Isolated processes sharing IPC or a user ID still require authorization validation. |
| **"write() means saved to disk"** | When `write()` or `f.write()` completes, the data is physically safe on SSD/HDD. | `write()` only places data in the volatile kernel page cache in RAM. It will vanish upon power failure unless flushed with `fsync()`. |
| **"close() flushes to storage"** | Calling `f.close()` forces physical disk persistence. | `close()` flushes user-space buffers to the kernel page cache and releases the FD; it does NOT force physical writeback to storage. |
| **"SSDs overwrite data like RAM"** | Writing to an SSD block replaces the old data in-place. | NAND flash requires erasing entire multi-megabyte blocks before re-writing pages. Updates are out-of-place, handled dynamically by the FTL. |
| **"Replication is durability"** | Having three copies in cloud storage guarantees data will never be lost. | Naive replication duplicates corruptions, software bugs, and malicious drops instantly; durability requires crash-consistent non-volatile storage and failure-boundary analysis. |

---

## 15. Machine-Checkable vs Reviewer-Required Evidence Candidates

| Module | Machine-Checkable Evidence Candidates | Reviewer-Required Evidence Candidates |
|---|---|---|
| **M05** | - Python script parses source and asserts expected AST node types.<br>- Script inspects `dis.Bytecode` and asserts presence of specific opcodes.<br>- Python unit test verifying `TypeError` raised on invalid dynamic type operation. | - Quality of learner explanation tracing source text through AST to machine behavior.<br>- Rigor of authoritative claim verified against Python documentation. |
| **M06** | - LAB-REQ-02 `./grade-lab-util sleep` outputs `OK`.<br>- Automated test verifying process exit code and zombie cleanup.<br>- `strace` log artifact verifying presence of `execve` and `write`. | - Explanation of the user-to-kernel trap traversal route.<br>- Distinction between guest emulation ticks and host wall-clock time.<br>- Classification of process failure modes. |
| **M07** | - Script reading `/proc/self/maps` and asserting expected segment permissions.<br>- Automated check demonstrating `ru_minflt` increment on initial array page touch.<br>- Program catching `SIGSEGV` or testing allocation limits. | - Conceptual clarity in distinguishing Memory Isolation from Trust Boundary.<br>- Explanation of how the MMU and page tables prevent cross-process memory interference. |
| **M08** | - Script opening file, querying `/proc/self/fd/`, asserting FD presence and targets.<br>- Script asserting `stat().st_ino` equality across hard links.<br>- Test reproducing and catching `EACCES`, `ENOENT`, `ENOSPC`. | - Completeness of the 5-layer write traversal explanation.<br>- Explanation of why directory unlinking does not immediately free open file disk blocks. |
| **M09** | - Benchmark script recording raw timing distribution of `write()` vs `fsync()`.<br>- Test verifying data persistence across process termination.<br>- Automated calculation check for back-of-the-envelope storage cost model. | - Soundness of durability judgment under specified failure bounds.<br>- Correct mechanism explanation of SSD write amplification, block erases, and wear leveling. |

---

## 16. Design Handoff Requirements

The subsequent Design Agent may safely rely on the following verified specifications:

1. **Lesson Structure:** Design 3 lessons per Module according to the canonical map:
   - M05: L05-01 (Source to Machine), L05-02 (Grammar/AST/Runtime), L05-03 (Types as Invariants).
   - M06: L06-01 (Program to Process), L06-02 (Fork/Exec/Exit), L06-03 (Scheduling Intuition).
   - M07: L07-01 (Virtual Memory & Isolation), L07-02 (Heap/Malloc/OOM), L07-03 (Page Faults & Protection).
   - M08: L08-01 (File API/FD/Inode), L08-02 (Page Cache/Buffered I/O), L08-03 (I/O Failures & Permissions).
   - M09: L09-01 (Durability/fsync/WAL), L09-02 (SSD vs HDD Mechanics), L09-03 (Storage Classes & Cost).
2. **Canonical Concept Homes:**
   - M06 `L06-01` introduces `EC-CON-018 Process`.
   - M07 `L07-01` introduces `EC-CON-013 Isolation` and `EC-CON-017 Trust Boundary`.
   - M09 `L09-01` introduces `EC-CON-016 Durability`.
   - No second definitions elsewhere.
3. **Lab Design Guidance:**
   - M06 implements **LAB-REQ-02** (xv6 `sleep` syscall route) following the exact bounded specification in Section 10.
   - M08 conducts a short reading-only revisit of xv6 `sysfile.c`/`file.c` to contrast with Linux VFS. Do not design a second xv6 lab.
4. **Mini Cloud App (P0–P9) Alignment:**
   - P0/P1 may connect to M05 (data validation/runtime), M06 (process entry/CLI), M07 (in-memory state bounds), M08 (local state file persistence), and M09 (durability check on restart).
   - Milestone order is NOT a curriculum DAG prerequisite.
5. **Tone and Pedagogical Loop:**
   - Strictly follow `Question -> Mental Model -> Mechanism -> Observe -> Build -> Break -> Explain -> Judge -> Project`.

---

## 17. Open Risks / Open Question Interactions

- **OQ-BP-001 (Bounded AI Literacy):** Remains OPEN. This slice maintains the safe interim rule: AI-generated code or explanations are untrusted hypotheses requiring source/test verification. No AI Core modules introduced.
- **OQ-BP-003 (Human-Facing System Boundary):** Remains OPEN. M05–M09 deal with core systems mechanics; human-facing boundaries (UI/accessibility) are not implicated.
- **OQ-BP-006 (Canonical Versions & Toolchain Pinning):** Remains OPEN. This dossier provides the tooling matrix (Ubuntu Noble, Python 3.12, GCC 13, QEMU 8.2, RISC-V GCC 13). Pinned container image digest will be finalized when runnable lab preflight is implemented.
- **M03 GDB Verification Debt:** Remains OPEN as known technical debt. M05–M09 avoid interactive GDB dependencies to prevent blocking production.

---

## 18. Final Recommendation

**READY FOR DESIGN**

The technical mechanisms, primary source routes, educational boundaries, lab specifications, licensing statuses, and environment constraints for M05 through M09 are fully established. The next task may proceed directly to the **Design Dossier for M05–M09**.

---

## 19. Completion Report

### Status
**READY FOR LEAD REVIEW**

### Deliverable
`research/runtime-os-persistence-m05-m09-v0.1.md`

### Exact Base
`9e38e8f5540d68e64083315394233353fe757069` (Assigned branch: `research/issue-47-m05-m09-runtime-os-persistence`)

### Exact Files Changed
- `research/runtime-os-persistence-m05-m09-v0.1.md` (new file)

Expected content-file count: **1**.

### Research Method
1. Re-read and reconciled all core project governance, invariants, decisions, competency matrices, concept registries, blueprint maps, and preceding research dossiers.
2. Verified primary specifications and documentation as of 2026-09-02:
   - IEEE Std 1003.1-2024 (POSIX.1-2024 / Issue 8).
   - Python 3.12/3.13 Language Reference, `ast`, and `dis` library documentation.
   - Linux Kernel Documentation (VFS, mm, writeback, overcommit).
   - MIT 6.1810 xv6 RISC-V course and repository sources.
   - SNIA flash memory and FTL technical documentation.
   - Seminal systems research papers (OSDI '14 crash consistency).
3. Conducted a complete re-audit of LAB-REQ-02 (xv6 `sleep`) confirming licensing, setup feasibility, machine-checkable criteria, and deterministic fallback.
4. Evaluated environment feasibility against OQ-BP-006, resolving interactions with M03's GDB debt.

### Authority-Class Summary
- **PRINCIPLE:** Translation pipeline, process isolation, virtual address translation, dual-mode execution, write-ahead logging, SSD write amplification.
- **SPECIFICATION:** POSIX.1-2024 system interfaces; Python language specification; C23 language specification; JEDEC solid-state drive standards.
- **IMPLEMENTATION:** CPython bytecode evaluation loop; Linux page cache dirty writeback; Linux procfs; xv6 trap handler.
- **CURRENT PRACTICE:** Ubuntu 24.04 package versions; modern cloud storage cost models; NVMe latency ranges.

### Licensing Findings
- xv6 software source: MIT License (requires copyright/permission notices).
- MIT 6.1810 lab HTML: CC BY 3.0 US (requires attribution, link, changes indicated).
- Essential CS policy: 100% original instructional prose, diagrams, and evidence prompts; software notices preserved.

### LAB-REQ-02 Feasibility Finding
- FEASIBLE and CONFIRMED as the optimal bounded Required Lab for user-to-kernel crossing.
- Toolchain requirements (`qemu-system-misc`, `gcc-riscv64-linux-gnu`) are standard packages in Ubuntu/Debian.
- M08 revisits xv6 via code inspection without duplicating the lab.

### Environment / Tool Feasibility Summary
- Canonical tools (Python 3.12, GCC, binutils, procfs) are standard and unprivileged.
- `strace` requires container `ptrace` capability; procfs fallback provided.
- GDB is decoupled from M05–M09 Core path.

### Canonical Concept First-Home Check
- M06 `L06-01`: `EC-CON-018 Process` (First home preserved).
- M07 `L07-01`: `EC-CON-013 Isolation` & `EC-CON-017 Trust Boundary` (First homes preserved; distinction enforced).
- M09 `L09-01`: `EC-CON-016 Durability` (First home preserved; strict 5-layer buffer boundary enforced).
- No new concept IDs introduced.

### M03 GDB Debt Interaction
- Preserved as explicit technical debt; M05–M09 do not add new GDB dependencies or convert M03 to PASS.

### OQ-BP-006 Status
- Remains OPEN. Feasibility evidence gathered; formal pinning deferred.

### Unresolved Factual Uncertainty
- Container `ptrace` permission policy varies across commercial hosted container providers; non-privileged fallback paths are documented.

### Routing Recommendation
- Classification: **SIMPLE RESEARCH FIX** / No architectural blockers found.
- Recommended Lead Focus:
  1. Confirm LAB-REQ-02 scope and M08 inspection-only revisit.
  2. Confirm decoupling of M05–M09 from GDB interactive debugging debt.
  3. Validate the 5-layer durability buffer stack and security boundary definitions.
- Final Dossier Recommendation: **READY FOR DESIGN**
