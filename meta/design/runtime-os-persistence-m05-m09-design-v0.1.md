# Runtime, OS & Persistence Design Dossier (M05–M09) v0.1

Status: **READY FOR LEAD REVIEW**
Issue: #50 — [Post-Blueprint] Runtime, OS & Persistence Design Dossier (M05–M09)
Base: `a5dabc0429a18022c60ab7f18495becd870cdca0`
Branch: `design/issue-50-m05-m09-runtime-os-persistence`
Role: Curriculum Design Agent — Module/Lesson/Activity/Evidence Designer
Scope: Design step only for M05–M09. This document is an instructional design contract; it is not learner-facing Lesson prose, runnable Lab code, or a curriculum architecture modification.

---

## 1. Design Status & Executive Recommendation

**Recommendation: READY FOR LESSON / ACTIVITY IMPLEMENTATION**

This Design Dossier translates the Lead-accepted and corrected Research Dossier (`research/runtime-os-persistence-m05-m09-v0.1.md`) into a concrete, implementation-ready blueprint for the five Modules spanning the second major Core sequence:

$$\text{M05 (Languages/Runtime)} \longrightarrow \text{M06 (Processes/Syscalls)} \longrightarrow \text{M07 (Virtual Memory)} \longrightarrow \text{M08 (Files/Filesystems)} \longrightarrow \text{M09 (Durable Storage)}$$

### Core Integrity & Boundary Confirmations
1. **Canonical Map Preserved:** All 5 Modules and all 15 preliminary Lessons are preserved without addition, deletion, or renaming.
2. **Concept Registry First Homes Preserved:**
   - M06 `L06-01`: **EC-CON-018 Process**
   - M07 `L07-01`: **EC-CON-013 Isolation**
   - M07 `L07-01`: **EC-CON-017 Trust Boundary**
   - M09 `L09-01`: **EC-CON-016 Durability**
3. **LAB-REQ-02 Current Path Specified:** Incorporates the Lead source correction: the user-level `sleep` utility invokes the existing xv6 `pause()` system call. The design traces `user/sleep.c` $\rightarrow$ `user/usys.S` (`SYS_pause` / `ecall`) $\rightarrow$ `sys_pause()`. M08 revisits xv6 strictly via code inspection without a second compilation lab.
4. **Environment & OQ-BP-006 Dispatched Safely:** OQ-BP-006 remains OPEN. Tools are classified into required, optional, and environment-sensitive. `strace` permissions are bounded with non-privileged procfs fallbacks. Interactive GDB is strictly decoupled to prevent M03 verification debt from blocking authoring.
5. **Durability & Security Rigor:** Durability is treated through explicit failure models and candidate write-path checkpoints rather than a false universal six-step stack. Isolation (visibility/interference limit) and Trust Boundary (authority/responsibility change) are strictly separated.

---

## 2. Scope, Constraints & Inherited Research Corrections

This design strictly incorporates the normative corrections from Section 20 of the accepted Research Dossier (`ad757ac`):

1. **Current MIT 6.1810 util Lab Route:** The Fall 2025 `sleep` exercise calls xv6 `pause()`. The design traces `pause/sys_pause`, abandoning stale `SYS_sleep/sys_sleep` nomenclature.
2. **Licensing Discipline:** xv6 source code is MIT-licensed (notices must be preserved). Current course assignment prose lacks an independently verified permissive license; all learner instructions, explanations, and prompts are 100% original Essential CS material. Assignment pages are link/reference only.
3. **Toolchain & Setup Expectations:** Standard packages (`git`, `build-essential`, `qemu-system-misc`, `gcc-riscv64-linux-gnu`, `binutils-riscv64-linux-gnu`) form the preflight baseline. No fixed setup/boot time constants are promised; exact times must be recorded during implementation smoke tests.
4. **ptrace / strace Permission Boundary:** `CAP_SYS_PTRACE` is not treated as a universal prerequisite. Tracing depends on UID matching, user namespaces, Yama LSM, and container security profiles. Non-ptrace inspection (procfs) is provided for restricted containers.
5. **Write-Path & Durability Checkpoints:** The write path is modeled as a set of possible checkpoints (language buffer, stdio buffer, kernel page cache, filesystem journal, device volatile cache, non-volatile media), not an invariant universal pipeline. Durability claims require naming the exact API, synchronization operation (`fsync`), and failure bound.
6. **CPython Implementation vs Python Specification:** Python Language Reference is the language specification; CPython bytecode and `dis` outputs are implementation-specific and version-sensitive. Activities must test structural relationships, not brittle opcode numbers or memory offsets.
7. **Storage Industry Evidence:** SNIA materials provide vendor-neutral conceptual evidence for FTL, wear leveling, and write amplification, not a universal hardware specification.

---

## 3. Cross-Module Capability Chain

The sequence takes the learner from source-level program execution down to persistent physical storage:

```
[M05: Languages & Runtime]
L05-01 (Source to Machine) -> L05-02 (Grammar/AST/Runtime) -> L05-03 (Types as Invariants)
  |
  | Program is compiled/packaged into an executable file on disk
  v
[M06: Processes & Syscalls]
L06-01 (Program to Process) -> L06-02 (Fork/Exec/Exit) -> L06-03 (CPU Scheduling Intuition)
  |  * Includes LAB-REQ-02 (xv6 sleep user program -> pause syscall route)
  |
  | Running process executes in an isolated memory space
  v
[M07: Virtual Memory & Isolation]
L07-01 (Virtual Memory & Isolation) -> L07-02 (Heap/Malloc/OOM) -> L07-03 (Page Faults & Errors)
  |  * Canonical definition of EC-CON-013 Isolation & EC-CON-017 Trust Boundary
  |
  | Process performs File I/O via operating system calls
  v
[M08: Files, Filesystems & System I/O]
L08-01 (File API/FD/Inode) -> L08-02 (Page Cache/Buffered I/O) -> L08-03 (I/O Failures & Permissions)
  |  * Short reading-only revisit of xv6 sysfile.c / file.c
  |
  | File writes must survive power loss and hardware failure
  v
[M09: Storage Engine & Durable Storage]
L09-01 (Durability & WAL) -> L09-02 (SSD vs HDD Mechanics) -> L09-03 (Storage Cost & Models)
     * Canonical definition of EC-CON-016 Durability
```

---

## 4. Module M05 Design — Languages, VM & Compiler Pipeline

### 4.1 Module-Level Specification
- **Title:** M05 — Languages, VM & Compiler Pipeline (Area 04)
- **Primary Competency:** Explain
- **Growth Competencies:** Trace, Learn-New-Tech, Observe
- **Module Prerequisites:** Hard: M03; Soft/Preferred: M04
- **Capability Transition:** Transition from believing programming languages run directly on hardware to understanding a language as a formal interface convention translated through intermediate representations (AST, bytecode, machine instructions) managed by a concrete runtime.

---

### 4.2 Lesson L05-01: “How does my Python become an instruction?”

1. **Learner Question:** How does my textual Python code actually get executed by the computer?
2. **Before / After Capability:**
   - *Before:* Believes Python directly "runs" source lines or that Python is entirely interpreted without compilation.
   - *After:* Can trace a Python function from source text through AST and CPython bytecode to VM stack evaluation, identifying where language semantics end and runtime implementation begins.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Hard prerequisite: `L03-02` / M03 (machine instructions and CPU execution).
   - Support: Provide simple Python standard library snippets (`ast`, `dis`); do not require installing third-party compilers.
4. **Concepts:** Revisits **Abstraction** (EC-CON-002), **Interface** (EC-CON-005), and **Representation** (EC-CON-003). No new first homes.
5. **Mental Model:** A programming language is an interface specification. The runtime engine translates human-readable syntax into intermediate structural representations before executing CPU instructions.
6. **Mechanism Sequence:**
   $$\text{Source Text} \xrightarrow{\text{Lexer/Parser}} \text{AST} \xrightarrow{\text{Compiler}} \text{Bytecode Instructions} \xrightarrow{\text{VM Eval Loop}} \text{Host Machine Instructions}$$
7. **Prediction-Before-Observation:** Before inspecting `dis.dis(func)`, predict whether Python evaluates `a + b` as a single CPU `ADD` instruction or as runtime virtual machine operations.
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Run `dis.dis()` on `def add(a, b): return a + b`. Observe `LOAD_FAST`, `BINARY_OP` (or `BINARY_ADD`), and `RETURN_VALUE`.
   - *Break:* Inspect bytecode of an un-optimizable loop; observe that Python re-evaluates dynamic lookups on each iteration.
   - *Explain:* Explain why CPython bytecode requires a software evaluation loop (`_PyEval_EvalFrameDefault`) running on the physical CPU.
9. **Required Commands / Tools:** Python 3.12 standard library (`dis`, `ast`).
10. **Machine-Checkable Evidence:** A test script that parses a function using `dis.Bytecode` and asserts the presence of binary operation and return opcodes without depending on exact numeric offsets.
11. **Reviewer-Required Evidence:** Reviewer checks that the learner explains the distinction between virtual bytecode and native machine code, avoiding claims that bytecode runs directly on CPU silicon.
12. **Misconceptions Addressed:**
    - "Python is interpreted line-by-line without compilation."
    - "CPython bytecode is machine code."
13. **What You Can Ignore—for Now:** CPython C source internals, adaptive inline cache internals (PEP 659), JIT compiler tiering.
14. **Progressive Support:**
    - *Question:* How does CPython represent `return x + 1` before running it?
    - *Hint 1:* Look at the `dis` module in Python's standard library.
    - *Hint 2:* The VM uses an evaluation stack: arguments are loaded before the operation executes.
    - *Expected Observation:* Bytecode showing `LOAD_FAST`, `LOAD_CONST`, and an addition opcode.
    - *Full Explanation:* Detailed walkthrough of the CPython evaluation stack.
15. **Visual Requirements:** Diagram showing Source Text $\rightarrow$ AST $\rightarrow$ Bytecode $\rightarrow$ VM Loop $\rightarrow$ CPU Registers/ALU.
16. **Exit Criteria:** Learner produces a 3-step trace of an expression from source to bytecode to VM action.
17. **Competency Mapping:** Trace (source $\rightarrow$ bytecode), Observe (`dis` inspection).
18. **Provenance / Source Anchors:** Python 3.12 Documentation — *dis — Disassembler for Python bytecode*.
19. **Failure / Inference Limits:** Bytecode opcodes vary across Python minor versions; observed opcodes represent CPython 3.12, not a universal Python standard.

---

### 4.3 Lesson L05-02: “What is a language really?”

1. **Learner Question:** What makes a programming language a "language," and how does syntax differ from execution?
2. **Before / After Capability:**
   - *Before:* Equates a language with its syntax or with a single proprietary compiler/tool.
   - *After:* Can explain a language as a specification (grammar and semantics) separate from its implementations (interpreters, AOT compilers, JITs), tracing source text to an AST.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L05-01`.
   - Support: Use Python's `ast` module to render AST structures visually.
4. **Concepts:** Revisits **Representation** (EC-CON-003) and **Specification** (EC-CON-007).
5. **Mental Model:** Syntax is an on-wire textual representation of program intent. The AST is the structured, canonical tree representation used for analysis and translation.
6. **Mechanism Sequence:**
   $$\text{Source Code String} \xrightarrow{\text{Grammar Rules}} \text{Parse Tree} \xrightarrow{\text{Simplification}} \text{Abstract Syntax Tree (AST)} \xrightarrow{\text{Analysis}} \text{IR / Bytecode}$$
7. **Prediction-Before-Observation:** Predict the AST structure for nested arithmetic `(a + b) * c`: which operator forms the root node?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Parse `a + b * c` with `ast.parse` and print `ast.dump(tree)`. Observe operator precedence reflected in tree depth.
   - *Build:* Construct a tiny 20-line evaluator that traverses a small dictionary-based AST and computes results.
   - *Break:* Introduce a syntax error (e.g., mismatched parentheses); observe that parsing fails before any execution starts.
   - *Explain:* Explain why a language specification can have multiple independent implementations (e.g., CPython, PyPy, MicroPython).
9. **Required Commands / Tools:** Python 3.12 `ast` module.
10. **Machine-Checkable Evidence:** A test script asserting that `ast.parse` produces a `BinOp` with `Mult` at the root for `(a + b) * c`.
11. **Reviewer-Required Evidence:** Learner articulates why syntax errors are caught during parsing while semantic/runtime errors occur during evaluation.
12. **Misconceptions Addressed:**
    - "CPython is the Python language."
    - "Indentation in Python is evaluated at runtime."
13. **What You Can Ignore—for Now:** LALR/LL parser tables, context-free grammar formalisms, SSA (Static Single Assignment) form.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Tree diagram contrasting flat source code tokens with a hierarchical AST.
16. **Exit Criteria:** Learner identifies the AST representation of an expression and explains why language spec $\neq$ implementation.
17. **Competency Mapping:** Explain (grammar/AST role), Learn-New-Tech (navigating language reference).
18. **Provenance / Source Anchors:** Python Language Reference §2 (Lexical analysis) and §3 (Data model).
19. **Failure / Inference Limits:** The AST reflects Python grammar rules; other languages use different syntactic structures but share the tree-representation principle.

---

### 4.4 Lesson L05-03: “Why are types useful?”

1. **Learner Question:** Why do languages have type systems, and what problems do they actually solve?
2. **Before / After Capability:**
   - *Before:* Views types as annoying syntax rules or bureaucratic bookkeeping.
   - *After:* Understands types as **contracts and invariants** that prevent defined classes of execution failure, distinguishing static compile-time verification from dynamic runtime enforcement.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L05-02`, M02 (`L02-03` Invariant / Correctness).
   - Support: Use Python dynamic type tags vs minimal C compilation to contrast enforcement times.
4. **Concepts:** Revisits **Invariant** (EC-CON-008), **Correctness** (EC-CON-009), and **Trade-off** (EC-CON-006).
5. **Mental Model:** A type system is an invariant checker. Static typing checks invariants before running code; dynamic typing checks invariants at the moment an operation executes.
6. **Mechanism Sequence:**
   - *Static:* Source $\rightarrow$ Type Checker $\rightarrow$ Invariant holds? Yes: emit code; No: compile error.
   - *Dynamic:* Value boxed with Type Tag $\rightarrow$ Operation dispatch $\rightarrow$ Invariant holds? Yes: execute; No: raise `TypeError`.
7. **Prediction-Before-Observation:** Predict whether `"5" + 1` fails at compile time or runtime in Python vs C.
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* In Python, execute `"5" + 1` $\rightarrow$ observe `TypeError` at runtime.
   - *Observe:* In C, compile `int x = "5" + 1;` $\rightarrow$ observe compiler warning/error before execution.
   - *Break:* Pass an unexpected type to a Python function that only fails after several long-running steps.
   - *Explain:* Frame the trade-off: development flexibility vs early invariant verification.
9. **Required Commands / Tools:** Python 3.12, GCC 13 (minimal 5-line C file).
10. **Machine-Checkable Evidence:** Automated test verifying that a provided Python type-mismatch script raises `TypeError` and that a provided C snippet fails compilation under `-Werror`.
11. **Reviewer-Required Evidence:** Learner explains in writing when invariants are checked in static vs dynamic systems and why neither prevents all bugs.
12. **Misconceptions Addressed:**
    - "Dynamic typing means variables have no types."
    - "A program that compiles without type errors is mathematically bug-free."
13. **What You Can Ignore—for Now:** Hindley-Milner type inference, dependent types, category theory.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Comparison diagram: Static Invariant Gate (pre-execution) vs Dynamic Tag Check (at execution step).
16. **Exit Criteria:** Learner explains types as invariants and contrasts compile-time vs runtime enforcement.
17. **Competency Mapping:** Explain (types as invariants), Correctness (failure prevention).
18. **Provenance / Source Anchors:** ISO/IEC 9899 (C Types) & Python Data Model documentation.
19. **Failure / Inference Limits:** Types catch domain/representation mismatch; they do not prove overall algorithmic correctness.

---

## 5. Module M06 Design — Processes, Syscalls & Execution Context

### 5.1 Module-Level Specification
- **Title:** M06 — Processes, Syscalls & Execution Context (Area 05)
- **Primary Competency:** Trace
- **Growth Competencies:** Observe, Diagnose, Explain
- **Module Prerequisites:** Hard: M03; Soft/Preferred: M05
- **Canonical Concept First Home:** **EC-CON-018 Process (进程)** at `L06-01`.
- **Capability Transition:** Transition from viewing code as "controlling the machine" to understanding that a program executes as an unprivileged guest process inside an OS-managed execution context, crossing into privileged kernel space via system calls.

---

### 5.2 Lesson L06-01: “What is a process?”

1. **Learner Question:** What actually happens when an operating system runs a program?
2. **Before / After Capability:**
   - *Before:* Confuses the compiled program binary on disk with the active process running in memory.
   - *After:* Can define a process as an isolated execution context (PID, memory regions, open file table, registers), and trace user code crossing into the kernel via a system call.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: M03 (`L03-01` machine execution).
   - Support: Use `/proc` and `ps` on the host to make process state transparent.
4. **Concepts:** **EC-CON-018 Process (First Home)**. Revisits **Interface** (EC-CON-005), **State** (EC-CON-001).
5. **Mental Model:** A program is passive instructions on disk. A process is an active, living instance of that program with assigned resources, memory, and credentials, managed by the OS kernel.
6. **Mechanism Sequence:**
   $$\text{ELF Binary on Disk} \xrightarrow{\text{OS Loader}} \text{Allocated Address Space} + \text{Kernel PCB} \rightarrow \text{User Mode Execution} \xrightarrow{\text{Trap/Syscall}} \text{Kernel Mode Service}$$
7. **Prediction-Before-Observation:** When your program calls `getpid()` or `time()`, does the CPU stay in user mode or switch privilege levels?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Inspect `/proc/$$/status` and `/proc/$$/stat`. Identify `Pid`, `State`, `VmSize`, and `FDSize`.
   - *Observe:* Run `strace -e trace=getpid python3 -c "import os; print(os.getpid())"`. Observe the raw system call.
   - *Explain:* Articulate why a user process cannot directly read kernel tables: CPU privilege rings enforce the boundary.
9. **Required Commands / Tools:** `ps`, `/proc`, `strace` (with procfs fallback).
10. **Machine-Checkable Evidence:** A test script verifying that a learner's script reads `/proc/self/status`, parses the `Pid:`, and matches the return value of `os.getpid()`.
11. **Reviewer-Required Evidence:** Reviewer checks learner's explanation of Program vs Process and user/kernel dual-mode protection.
12. **Misconceptions Addressed:**
    - "A program and a process are the same thing."
    - "User programs interact with hardware only through system calls" (Correction: User code executes ordinary CPU instructions and accesses mapped user memory directly; only kernel-managed resources require syscalls).
13. **What You Can Ignore—for Now:** Task struct kernel C code, complex capability bitmaps, namespaces.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Diagram contrasting static ELF file on disk with live process structure in memory (PCB, memory maps, file descriptor table).
16. **Exit Criteria:** Learner defines Process and traces a basic system call from user to kernel mode.
17. **Competency Mapping:** Trace (syscall boundary), Observe (`ps` and `/proc`).
18. **Provenance / Source Anchors:** POSIX.1-2024 Base Definitions §3 (General Concepts: Process) & Linux `proc(5)` man page.
19. **Failure / Inference Limits:** The `/proc` filesystem is a Linux-specific interface; the Process concept is universal across modern operating systems.

---

### 5.3 Lesson L06-02: “How does a program start another?”

1. **Learner Question:** How does one program launch and manage another program in an operating system?
2. **Before / After Capability:**
   - *Before:* Thinks launching a program is a single atomic action that instantly replaces everything.
   - *After:* Can trace the two-stage POSIX process creation model (`fork` clones execution context, `execve` replaces binary image), explain process exit status, and diagnose zombie processes.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L06-01`.
   - Support: Provide a small 15-line Python script utilizing `os.fork()`, `os.execv()`, and `os.waitpid()`.
4. **Concepts:** Revisits **Process** (EC-CON-018), **State** (EC-CON-001), **Failure** (EC-CON-010).
5. **Mental Model:** Creation is split into cloning (`fork`) and re-initialization (`exec`). This separation allows the parent or child to configure I/O, file descriptors, and credentials before the new program begins.
6. **Mechanism Sequence:**
   $$\text{Parent Process} \xrightarrow{\text{fork()}} \text{Parent + Child (identical state)} \xrightarrow[\text{in child}]{\text{execve()}} \text{New Program Image Loaded} \xrightarrow{\text{exit()}} \text{Zombie} \xrightarrow[\text{in parent}]{\text{waitpid()}} \text{Reaped}$$
7. **Prediction-Before-Observation:** If a child process modifies variable `x = 42` after `fork()`, does the parent's `x` change?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Build:* Run a script that forks: child mutates variable, sleeps, and exits with code `7`. Parent waits and checks its own variable and the child's exit code.
   - *Observe:* Observe distinct PIDs and unshared variables.
   - *Break:* Create an intentional **zombie process** by having child exit while parent sleeps without calling `wait()`. Inspect `ps aux | grep Z`.
   - *Explain:* Explain why a zombie exists: the kernel preserves the exit code until the parent reads it.
9. **Required Commands / Tools:** Python 3.12 (`os.fork`, `os.waitpid`), `ps`.
10. **Machine-Checkable Evidence:** Script creates a child process with a specific exit code ($42$), parent reaps it, and asserts `os.WEXITSTATUS(status) == 42`.
11. **Reviewer-Required Evidence:** Reviewer validates the learner's explanation of why POSIX splits process creation into `fork` and `exec` rather than a single `spawn` call.
12. **Misconceptions Addressed:**
    - "`fork` means running a new program."
    - "A zombie process eats CPU and memory."
13. **What You Can Ignore—for Now:** Copy-on-write page table manipulation details, vfork, signal handler race conditions.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Sequence diagram showing Fork (state duplication), Exec (image replacement), Exit (zombie state), and Wait (reaping).
16. **Exit Criteria:** Learner traces `fork` $\rightarrow$ `exec` $\rightarrow$ `exit` $\rightarrow$ `wait` and diagnoses a zombie process.
17. **Competency Mapping:** Trace (process lifecycle), Diagnose (zombie/exit codes).
18. **Provenance / Source Anchors:** POSIX.1-2024 `fork(2)`, `execve(2)`, `waitpid(2)` specifications.
19. **Failure / Inference Limits:** POSIX `fork` semantics specify logical cloning; modern Linux optimizes this with Copy-on-Write (COW), which is an implementation optimization, not the POSIX interface definition.

---

### 5.4 Lesson L06-03: “How does the CPU get shared?”

1. **Learner Question:** How can multiple programs run at the same time if my computer has a limited number of CPU cores?
2. **Before / After Capability:**
   - *Before:* Assumes programs run continuously until they voluntarily decide to quit or yield.
   - *After:* Understands preemptive time-slicing driven by timer interrupts, classifies process states (Running, Runnable, Blocked), and explains CPU vs I/O bound behavior.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L06-01`, M03 (`L03-01`).
   - Support: Use simple CLI observation (`top` or `/proc/<pid>/stat`) to observe process state transitions.
4. **Concepts:** Revisits **Process** (EC-CON-018), **Trade-off** (EC-CON-006). Previews **Isolation** (EC-CON-013).
5. **Mental Model:** The CPU is a multiplexed resource. The OS scheduler switches execution between runnable processes hundreds of times per second, giving each the illusion of continuous progress.
6. **Mechanism Sequence:**
   $$\text{Running Process} \xrightarrow{\text{Timer Interrupt}} \text{Kernel Scheduler} \xrightarrow{\text{Save State to PCB}} \xrightarrow{\text{Context Switch}} \text{Restore State of Next Process} \rightarrow \text{User Mode}$$
7. **Prediction-Before-Observation:** When a process calls `sleep(5)` or waits for keyboard input, does it consume 100% of a CPU core?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Run a tight infinite loop (`while True: pass`) vs a sleeping loop (`while True: time.sleep(1)`). Compare CPU usage in `top` or `/proc/<pid>/stat` (State `R` vs `S`).
   - *Explain:* Explain why the scheduler moves the sleeping process from the *run queue* to the *wait queue* until the timer expires.
   - *Judge:* Discuss fairness vs latency trade-offs in scheduling policies.
9. **Required Commands / Tools:** Python 3.12, `ps`, `top`.
10. **Machine-Checkable Evidence:** Automated test checking that a process executing `time.sleep` transitions its state in `/proc/<pid>/stat` from `R` (Running) to `S` (Sleeping/Waiting).
11. **Reviewer-Required Evidence:** Learner articulates the role of hardware timer interrupts in preventing a runaway program from locking up the entire system.
12. **Misconceptions Addressed:**
    - "Multi-tasking requires multiple physical CPUs."
    - "A sleeping program wastes CPU cycles checking the clock."
13. **What You Can Ignore—for Now:** Completely Fair Scheduler (CFS) red-black tree algorithms, real-time scheduling classes (SCHED_FIFO/SCHED_RR), NUMA balancing.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** State transition diagram: Created $\rightarrow$ Ready/Runnable $\leftrightarrow$ Running $\rightarrow$ Blocked/Waiting $\rightarrow$ Terminated.
16. **Exit Criteria:** Learner explains preemptive time-slicing and distinguishes CPU-bound from I/O-blocked states.
17. **Competency Mapping:** Explain (scheduling intuition), Observe (process states in procfs).
18. **Provenance / Source Anchors:** OSTEP Chapter 7 (Scheduling: Introduction) & Linux `sched(7)`.
19. **Failure / Inference Limits:** Observed CPU percentages are sampled over time windows; short-lived context switches are smoothed by operating system monitoring tools.

---

## 6. Required Lab LAB-REQ-02 Design — xv6 `sleep` Syscall Traversal

### 6.1 Lab Overview & Upstream Realignment
- **Lab ID:** `LAB-REQ-02`
- **Location:** Integrated with M06 (Lesson `L06-01` / `L06-02`), revisited conceptually in M08.
- **Upstream Source:** MIT 6.1810 Operating System Engineering (Fall 2025).
  - Software Repository: `https://github.com/mit-pdos/xv6-riscv` (pinned commit `35b088427ef37611c38afdeed5a52a278cae38f9`).
  - Lab Page: `https://pdos.csail.mit.edu/6.1810/2025/labs/util.html`.
- **Current Route Realignment (Lead Correction):** In the Fall 2025 xv6 lab tree, the user-level utility is `sleep`, but the underlying system call in the kernel is **`pause(int ticks)`** (system call number `SYS_pause`).
  $$\text{user/sleep.c} \xrightarrow{\text{calls}} \text{pause(n)} \xrightarrow{\text{user/usys.S}} \text{li a7, SYS\_pause; ecall} \xrightarrow{\text{kernel trap}} \text{sys\_pause()} \xrightarrow{\text{sleep on ticks}}$$
- **Licensing Contract:**
  - `xv6-riscv` software source is covered by its MIT License. Retain the MIT copyright notice in any bundled software template.
  - MIT 6.1810 lab assignment web text is treated as link/reference only. All learner guidance, explanations, step-by-step tasks, and evidence collection rubrics must be independently authored by Essential CS.

---

### 6.2 Pedagogical Contract & Scope Boundary
- **Core Learning Goal:** Trace an operation from user-space C source through assembly trap generation (`ecall`), across the CPU privilege boundary, into kernel dispatch, and back.
- **Strictly Bounded Scope:**
  - The learner implements **only** the user program `user/sleep.c`.
  - The learner registers `$U/_sleep` in `UPROGS` in `Makefile`.
  - The learner runs `sleep 10` inside xv6 in QEMU.
  - **Forbidden:** No kernel-level modifications, no implementing new kernel subsystems, no shell modifications, no grading server scripts.

---

### 6.3 Technical Toolchain & Preflight
- **Required Packages (Ubuntu Noble Baseline):**
  `build-essential`, `qemu-system-misc`, `gcc-riscv64-linux-gnu`, `binutils-riscv64-linux-gnu`, `git`.
- **Preflight Check Command:**
  ```bash
  riscv64-linux-gnu-gcc --version && qemu-system-riscv64 --version
  ```
- **Execution & Smoke Path:**
  1. Clone pinned repository: `git clone https://github.com/mit-pdos/xv6-riscv.git`
  2. Checkout pinned commit: `git checkout 35b088427ef37611c38afdeed5a52a278cae38f9`
  3. Create `user/sleep.c`:
     ```c
     #include "kernel/types.h"
     #include "kernel/stat.h"
     #include "user/user.h"

     int main(int argc, char *argv[]) {
       if (argc != 2) {
         fprintf(2, "Usage: sleep <ticks>\n");
         exit(1);
       }
       int ticks = atoi(argv[1]);
       pause(ticks);
       exit(0);
     }
     ```
  4. Edit `Makefile`: add `$U/_sleep\` to `UPROGS`.
  5. Compile and test: `make qemu` $\rightarrow$ inside xv6 shell: `sleep 10`.
  6. Automated grade check: `./grade-lab-util sleep` outputs `== Test sleep, correct: OK`.

---

### 6.4 Clean Reset & Recovery
- **Exiting QEMU:** Press `Ctrl-A` then `X`.
- **Stuck / Hanging Process Recovery:** Run `pkill -9 qemu-system-riscv64`.
- **Resetting Repository:**
  ```bash
  git checkout -- Makefile && rm -f user/sleep.c && make clean
  ```

---

### 6.5 Hosted Environment Fallback Strategy
If QEMU cannot execute due to container policy restrictions:
1. **Source Inspection Walkthrough:** Learner inspects `user/user.h`, `user/usys.pl`, `kernel/syscall.c`, and `kernel/sysproc.c` in the pinned repository.
2. **Deterministic Prerecorded Execution:** Learner replays a verified recorded transcript of QEMU running `sleep 10` and answers boundary questions.
3. **Linux Native Equivalent:** Learner traces Linux native sleep using `strace -e trace=nanosleep sleep 1`.

---

### 6.6 Evidence Rubric
- **Machine-Checkable:**
  - Code compiles without error in xv6 build.
  - `./grade-lab-util sleep` outputs `OK`.
  - Calling `sleep` with no arguments outputs error message to stderr (file descriptor 2) and returns exit code 1.
- **Reviewer-Required:**
  - Learner provides a written trace identifying the role of `user/usys.S`, register `a7`, instruction `ecall`, and kernel function `sys_pause`.
  - Learner correctly explains why xv6 timer ticks differ from real host wall-clock time.

---

## 7. Module M07 Design — Virtual Memory & Isolation

### 7.1 Module-Level Specification
- **Title:** M07 — Virtual Memory & Isolation (Area 05)
- **Primary Competency:** Explain
- **Growth Competencies:** Trace, Diagnose, Estimate
- **Module Prerequisites:** Hard: M06, M04; Soft/Preferred: None
- **Canonical Concept First Homes:**
  - **EC-CON-013 Isolation (隔离)** at `L07-01`.
  - **EC-CON-017 Trust Boundary (信任边界)** at `L07-01`.
- **Capability Transition:** Transition from a flat, naive physical memory model to understanding that all application pointers are *virtual addresses* dynamically translated by hardware MMUs via page tables, recognizing how this mechanism enforces memory isolation and establishes the first concrete trust boundary.

---

### 7.2 Lesson L07-01: “How do two programs both use memory without simply sharing everything?”

1. **Learner Question:** Why don't two running programs overwrite each other's variables, and why can both have a variable at the exact same memory address?
2. **Before / After Capability:**
   - *Before:* Believes processes share one large pool of physical RAM addresses directly.
   - *After:* Can explain virtual address translation (pages $\rightarrow$ page frames via page tables and MMU), define **Isolation**, define **Trust Boundary**, and explain why Isolation $\neq$ Trust Boundary.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: M06 (`L06-01` process context), M04 (`L04-01` caching/hardware hierarchy).
   - Support: Inspect `/proc/self/maps` to show real virtual address segments.
4. **Concepts:**
   - **EC-CON-013 Isolation (First Home)**: Limiting interference or visibility between executions or resources.
   - **EC-CON-017 Trust Boundary (First Home)**: A boundary where authority, trust assumptions, or enforcement responsibility changes.
5. **Mental Model:** The CPU MMU sits between the program and physical RAM. Every address emitted by software is virtual. Page tables map each process's virtual pages to separate physical frames, isolating their memory completely.
6. **Mechanism Sequence:**
   $$\text{Virtual Address (VPN + Offset)} \xrightarrow{\text{MMU + TLB Lookup}} \text{Page Table Entry (PFN + Flags)} \xrightarrow{\text{Protection Check}} \text{Physical RAM Address}$$
7. **Prediction-Before-Observation:** If two independent Python processes print the address of a variable, can the hexadecimal numbers be identical? Do they point to the same physical memory?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Run two separate processes printing `/proc/self/maps`. Notice both have identical stack/code virtual address ranges.
   - *Observe:* Inspect permission bits (`r-xp`, `rw-p`, `r--p`) in `/proc/self/maps`.
   - *Explain:* **The Isolation vs Trust Boundary Distinction:**
     - *Isolation:* Process A cannot read/write Process B's memory because their page tables point to different physical frames.
     - *Trust Boundary:* The kernel mode / user mode split is a trust boundary: the kernel must validate every pointer passed in a syscall because user space is untrusted. Two processes under the same user UID are memory-isolated, but share a trust boundary (can ptrace/kill each other).
9. **Required Commands / Tools:** `/proc/self/maps`, Python 3.12.
10. **Machine-Checkable Evidence:** Automated test checking that a script parses `/proc/self/maps` and identifies at least one read-only executable segment (`r-xp`) and one readable-writable segment (`rw-p`).
11. **Reviewer-Required Evidence:** Learner provides an explanation distinguishing Isolation from Trust Boundary using a concrete example.
12. **Misconceptions Addressed:**
    - "Pointers are physical wire addresses on motherboard RAM chips."
    - "Isolation and Trust Boundary are synonyms."
13. **What You Can Ignore—for Now:** Multi-level page table tree walking math (PML4/PML5), page table entry bit-level layout, TLB shootdown interrupts.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:**
    - Diagram 1: Two virtual address spaces mapping to disjoint physical RAM frames via separate page tables.
    - Diagram 2: Matrix contrasting Isolation Boundary vs Trust Boundary.
16. **Exit Criteria:** Learner explains virtual-to-physical translation and accurately contrasts Isolation with Trust Boundary.
17. **Competency Mapping:** Explain (virtual memory & isolation), Trace (address translation).
18. **Provenance / Source Anchors:** OSTEP Chapters 13–15 (Address Spaces, Paging) & Intel SDM Vol 3A (Paging).
19. **Failure / Inference Limits:** Modern OSes support shared memory regions (`mmap` with `MAP_SHARED`); memory isolation is the default rule, not an absolute prohibition of explicit sharing.

---

### 7.3 Lesson L07-02: “Why is my program out of memory?”

1. **Learner Question:** What actually happens when a program allocates more memory than the computer has, and why does my process crash with "Out of Memory"?
2. **Before / After Capability:**
   - *Before:* Assumes `malloc()` or creating a list immediately consumes that exact amount of physical RAM, and that running out of memory simply returns `NULL`.
   - *After:* Can distinguish Virtual Memory Size (`VSZ`) from Resident Set Size (`RSS`), explain lazy demand-paging, and describe the Linux OOM killer mechanism without destabilizing the host.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L07-01`.
   - Support: Use Python `resource.getrusage` to safely observe page allocation without crashing the system.
4. **Concepts:** Revisits **State** (EC-CON-001), **Failure** (EC-CON-010), **Trade-off** (EC-CON-006).
5. **Mental Model:** Allocating memory is a two-step process: reserving virtual address space (cheap and fast) vs binding physical RAM frames upon first touch (demand paging via minor page faults).
6. **Mechanism Sequence:**
   $$\text{malloc() / brk()} \xrightarrow{\text{VMA updated (VSZ increases)}} \text{First Write to Page} \xrightarrow{\text{Minor Page Fault}} \text{Kernel allocates physical frame (RSS increases)}$$
7. **Prediction-Before-Observation:** If you allocate a 1 GB array in Python or C but never write to it, does your computer's free RAM drop by 1 GB?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Run a script allocating a large block. Track `VmSize` vs `VmRSS` in `/proc/self/status`.
   - *Observe:* Observe `ru_minflt` in `resource.getrusage()` jump when the memory is written in a loop.
   - *Explain:* Explain why the Linux kernel allows memory overcommit and how the Out-of-Memory (OOM) killer selects a process to terminate when physical RAM + swap are exhausted.
   - *Safety Guard:* Do not trigger a real host-wide OOM; use a simulated quota or inspect simulated `/proc/<pid>/oom_score` output.
9. **Required Commands / Tools:** Python 3.12 (`resource`), `/proc/self/status`.
10. **Machine-Checkable Evidence:** Automated test verifying that allocating memory without writing results in $\text{VSZ} \gg \text{RSS}$, and writing to it causes $\text{RSS}$ and `ru_minflt` to increase proportionally.
11. **Reviewer-Required Evidence:** Learner explains the difference between an allocation request and physical RAM commitment.
12. **Misconceptions Addressed:**
    - "Allocating memory immediately fills physical RAM."
    - "Running out of memory always results in a clean error return."
13. **What You Can Ignore—for Now:** Slab/slub kernel allocators, huge pages (THP), memory compaction algorithms.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Diagram contrasting Virtual Address Allocation (VSZ) with Physical Frame Commitment (RSS) upon first write.
16. **Exit Criteria:** Learner explains demand paging and distinguishes virtual reservation from physical RAM exhaustion.
17. **Competency Mapping:** Diagnose (memory growth), Estimate (memory footprint).
18. **Provenance / Source Anchors:** Linux Kernel Documentation — *Overcommit Accounting* & `proc(5)`.
19. **Failure / Inference Limits:** Memory overcommit policies vary across operating systems (Linux default vs Windows/macOS strict allocation).

---

### 7.4 Lesson L07-03: “What happens when I touch a bad address?”

1. **Learner Question:** What actually causes a "Segmentation Fault," and what does the hardware do when an illegal memory address is accessed?
2. **Before / After Capability:**
   - *Before:* Views a segfault as an arbitrary, mysterious software crash.
   - *After:* Can trace an illegal address access from CPU MMU fault detection to kernel interrupt handling and `SIGSEGV` delivery, distinguishing minor, major, and invalid page faults.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L07-01`, `L07-02`.
   - Support: Use a safe, contained C or Python script that deliberately triggers a fault in a child process.
4. **Concepts:** Revisits **Failure** (EC-CON-010), **Interface** (EC-CON-005).
5. **Mental Model:** A segmentation fault is not a software crash routine; it is a hardware protection event. The CPU MMU detects an invalid translation or permission violation and triggers a hardware trap that transfers control to the OS kernel.
6. **Mechanism Sequence:**
   $$\text{Instruction executes bad address} \xrightarrow{\text{MMU detects invalid PTE}} \text{CPU Page Fault Trap} \xrightarrow{\text{Kernel Fault Handler}} \text{Deliver SIGSEGV} \rightarrow \text{Process Terminates}$$
7. **Prediction-Before-Observation:** If a program attempts to write to memory address `0x0`, who stops it: the compiler, the CPU hardware, or the kernel?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Build / Break:* Run a minimal 5-line C program that attempts to write to address `NULL` (`*(int*)0 = 1;`) or write to a string literal in `.rodata`.
   - *Observe:* The shell reports `Segmentation fault (core dumped)` with exit code 139 ($128 + 11$).
   - *Explain:* Categorize page fault types:
     1. *Minor:* Valid mapping, physical page allocated on demand (normal operation).
     2. *Major:* Valid mapping, page swapped or file-backed, requires disk read.
     3. *Invalid:* Unmapped address or permission violation $\rightarrow$ `SIGSEGV`.
9. **Required Commands / Tools:** GCC 13, Python 3.12 (subprocess runner).
10. **Machine-Checkable Evidence:** Test runs the bad-pointer child executable and asserts child exit status is terminated by signal 11 (`SIGSEGV`).
11. **Reviewer-Required Evidence:** Learner articulates the 4-step fault sequence: CPU instruction $\rightarrow$ MMU exception $\rightarrow$ kernel fault handler $\rightarrow$ process signal.
12. **Misconceptions Addressed:**
    - "A segfault means physical memory is damaged."
    - "Every bad pointer immediately crashes the program" (unmapped pages crash; wild pointers hitting other valid user pages cause silent data corruption).
13. **What You Can Ignore—for Now:** Custom signal handler recovery with `sigaction` and `siglongjmp`, stack guard pages, ASLR implementation.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Flowchart showing MMU Page Fault evaluation: Valid page? $\rightarrow$ Permission check? $\rightarrow$ Normal Minor/Major Fault vs Invalid SIGSEGV.
16. **Exit Criteria:** Learner explains the hardware/OS sequence behind a segmentation fault and categorizes the three fault types.
17. **Competency Mapping:** Diagnose (bad address failures), Trace (fault handler path).
18. **Provenance / Source Anchors:** POSIX.1-2024 Signal Concepts (`SIGSEGV`) & OSTEP Chapter 19 (Paging: Faster Translations).
19. **Failure / Inference Limits:** A segmentation fault occurs when an address violates the current page table mapping; reading an out-of-bounds array element that still falls inside a mapped page will NOT trigger a segfault.

---

## 8. Module M08 Design — Files, Filesystems & System I/O

### 8.1 Module-Level Specification
- **Title:** M08 — Files, Filesystems & System I/O (Area 05/06)
- **Primary Competency:** Trace
- **Growth Competencies:** Explain, Observe, Diagnose
- **Module Prerequisites:** Hard: M06; Soft/Preferred: M07
- **Canonical Concept First Home:** None (Revisits Interface, State, Caching, Locality).
- **Capability Transition:** Transition from viewing file I/O as directly writing bytes to physical disk to understanding the layered POSIX I/O architecture: user-space buffering $\rightarrow$ file descriptors $\rightarrow$ VFS $\rightarrow$ inodes/metadata $\rightarrow$ kernel page cache $\rightarrow$ block device boundary.

---

### 8.2 Lesson L08-01: “What is a file, underneath?”

1. **Learner Question:** What actually is a file to the operating system, and how does a filename lead to bytes on storage?
2. **Before / After Capability:**
   - *Before:* Believes a file is simply a named container on disk and that the filename is stored inside the file itself.
   - *After:* Can trace the decoupling between human-readable pathnames (directory entries), process handles (file descriptors), kernel open file descriptions, and filesystem metadata objects (inodes).
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: M06 (`L06-01` syscalls and process resources).
   - Support: Use `ls -i`, `stat`, and `/proc/<pid>/fd` to expose kernel and filesystem handles.
4. **Concepts:** Revisits **Interface** (EC-CON-005), **Indirection** (EC-CON-004), **State** (EC-CON-001).
5. **Mental Model:** A path is a directory entry pointing to an inode. A file descriptor is an integer handle pointing to an open file description. Inodes store metadata and block pointers, completely independent of the filenames that reference them.
6. **Mechanism Sequence:**
   $$\text{Path String} \xrightarrow{\text{Directory Lookup}} \text{Inode Number} \xrightarrow{\text{open()}} \text{File Descriptor (Process Table)} \rightarrow \text{Open File Description (Offset)} \rightarrow \text{Inode}$$
7. **Prediction-Before-Observation:** If you create two hard links to the same file and delete one, does the file disappear? Does its inode number change?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Create a file, inspect with `stat`. Create a hard link (`ln file link1`). Observe identical inode numbers and link count increasing to 2.
   - *Observe:* Inspect `/proc/self/fd/` to see integer file descriptors mapping to target files.
   - *Break:* Open a file in a long-running process, delete the file from disk using `rm`, and observe that the process can still read and write to it via its open file descriptor!
   - *Explain:* Explain why: the inode and data blocks are only freed when the link count reaches 0 AND all open file descriptors referencing it are closed.
9. **Required Commands / Tools:** `stat`, `ls -li`, `ln`, `rm`, `/proc/self/fd`.
10. **Machine-Checkable Evidence:** Automated test creating a file and a hard link, asserting `os.stat("file").st_ino == os.stat("link1").st_ino`, deleting the first, and asserting data remains readable through the link.
11. **Reviewer-Required Evidence:** Learner explains the structural difference between a File Descriptor, an Open File Description, a Directory Entry, and an Inode.
12. **Misconceptions Addressed:**
    - "A file's name is stored inside the file itself."
    - "Deleting a file immediately frees its disk blocks."
    - "A file descriptor is a global filename."
13. **What You Can Ignore—for Now:** Ext4 extent tree on-disk B-tree math, superblock backup blocks, extended attributes (xattrs).
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Architectural diagram linking Process FD Table $\rightarrow$ Open File Table (with offsets) $\rightarrow$ Inodes $\rightarrow$ Directory Entries.
16. **Exit Criteria:** Learner explains the 4-way separation of Path, FD, Open File Description, and Inode.
17. **Competency Mapping:** Trace (path $\rightarrow$ inode resolution), Observe (`stat` / `/proc`).
18. **Provenance / Source Anchors:** POSIX.1-2024 Base Definitions §3 (File, Inode, Directory) & `stat(2)`.
19. **Failure / Inference Limits:** Inodes are a concept from Unix/POSIX filesystems; other architectures (e.g., FAT32 or specialized object stores) structure metadata differently, but all decouple naming from physical data location.

---

### 8.3 Lesson L08-02: “Where does my file's data actually live?”

1. **Learner Question:** When my code calls `write()`, where do the bytes go, and why does writing a file feel instantaneous even on slow disks?
2. **Before / After Capability:**
   - *Before:* Assumes `write()` immediately deposits bytes onto non-volatile storage media.
   - *After:* Can trace the buffered write path through user-space runtime buffers, kernel page cache, and block device boundaries, understanding that a successful `write()` does NOT guarantee durability across power loss.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L08-01`, M04 (`L04-01` Caching).
   - Support: Use `strace` and `/proc/meminfo` (Dirty pages) to make caching visible.
4. **Concepts:** Revisits **Caching** (EC-CON-011), **Locality** (EC-CON-012), **Trade-off** (EC-CON-006). Previews **Durability** (EC-CON-016).
5. **Mental Model:** Write operations are aggressively cached. The kernel copies data into unused RAM (Page Cache) and marks it "dirty." Disk writing happens asynchronously in the background.
6. **Mechanism Sequence (Possible Write-Path Checkpoints):**
   $$\text{User Code} \xrightarrow{\text{1. Runtime Buffer}} \text{libc/stdio buffer} \xrightarrow{\text{2. write() syscall}} \text{Kernel Page Cache (Dirty RAM)} \xrightarrow{\text{3. Flusher Thread}} \text{Block Device}$$
7. **Prediction-Before-Observation:** If you write 100 MB of data to a file in Python without calling `flush()` or `fsync()`, has it reached the storage disk when `file.write()` returns?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Observe:* Write a loop calling `file.write("x")` 10,000 times in Python. Use `strace` to observe that Python's `BufferedWriter` batches these into a few 8 KiB `write()` system calls.
   - *Observe:* Monitor `Dirty` memory in `/proc/meminfo` or `vmstat 1` while generating a 200 MB temporary file; watch dirty pages spike in RAM and slowly drain.
   - *Explain:* Explain why `write()` returning success is an operating system guarantee that the kernel accepted the data, NOT a guarantee that it survived to non-volatile media.
9. **Required Commands / Tools:** Python 3.12, `strace`, `/proc/meminfo`, `vmstat`.
10. **Machine-Checkable Evidence:** Test script traces file writes with `strace` and asserts that 1,000 small application write calls result in substantially fewer underlying `write()` syscalls due to buffering.
11. **Reviewer-Required Evidence:** Learner explicitly states in writing that ordinary buffered `write()` success does NOT prove power-loss durability.
12. **Misconceptions Addressed:**
    - "`write()` writes bytes directly to the physical drive."
    - "Page cache is persistent storage."
    - "`f.close()` forces physical disk synchronization."
13. **What You Can Ignore—for Now:** Dirty background ratio sysctl tuning math, direct I/O (`O_DIRECT`), async I/O rings.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Diagram illustrating the write path: User Application Buffer $\rightarrow$ Kernel Page Cache (RAM) $\rightarrow$ Block Queue $\rightarrow$ Disk Controller.
16. **Exit Criteria:** Learner traces write buffering across user and kernel space and states the durability limitation of buffered I/O.
17. **Competency Mapping:** Trace (write path), Explain (page cache role).
18. **Provenance / Source Anchors:** Linux Kernel Documentation — *Page Cache and Writeback* & POSIX.1-2024 `write(2)`.
19. **Failure / Inference Limits:** The page cache writeback delay is an operating system implementation policy (typically 5 to 30 seconds on Linux); it is not a fixed hardware constant.

---

### 8.4 Inspection-Only Revisit: xv6 Filesystem Mechanics (M08 Context)
- **Design Intent:** Contrast Linux's multi-layered VFS/page-cache architecture with a clean, minimal operating system implementation without assigning a second lab.
- **Activity:** Code reading expedition (Source Inspection) in the pinned `xv6-riscv` tree:
  - Inspect `kernel/sysfile.c` (`sys_read`, `sys_write`): observe how the kernel retrieves the `struct file` from the current process's `proc->ofile[fd]`.
  - Inspect `kernel/file.c`: observe how file descriptors map directly to an in-memory inode (`struct inode`).
  - Observe that xv6 has a simple buffer cache (`kernel/bio.c`) without a full-blown Linux page cache or dynamic VFS abstraction.
- **Evidence:** Learner answers three structured comprehension questions contrasting xv6's direct file-to-inode mapping with Linux VFS indirection. No compilation or QEMU boot required.

---

### 8.5 Lesson L08-03: “Why did my file I/O fail?”

1. **Learner Question:** Why do file operations fail, and how do I diagnose missing files, permission denials, and disk full errors?
2. **Before / After Capability:**
   - *Before:* Treats all file errors as generic crashes or uncaught exceptions.
   - *After:* Can diagnose and handle specific POSIX file error codes (`ENOENT`, `EACCES`, `ENOSPC`), explaining how permissions and filesystem capacity bounds cause failures.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L08-01`.
   - Support: Use temporary directories and loopback/tmpfs mounts for safe, isolated failure testing.
4. **Concepts:** Revisits **Failure** (EC-CON-010), **Specification** (EC-CON-007), **Correctness** (EC-CON-009).
5. **Mental Model:** System calls indicate failure via well-defined integer error numbers (`errno`). Each error code corresponds to a broken invariant at a specific layer of the file subsystem.
6. **Mechanism Sequence:**
   $$\text{User Syscall} \xrightarrow{\text{Kernel Invariant Check}} \text{Fails (e.g. Permission / Capacity)} \xrightarrow{\text{Return -1}} \text{Set errno in libc} \rightarrow \text{Raise Language Exception}$$
7. **Prediction-Before-Observation:** If a non-root user tries to write to a file with permissions `r--r--r--` ($0444$), which error code is returned?
8. **Hands-on Progression (Observe / Build / Break / Explain):**
   - *Break:* Reproduce `ENOENT` (open non-existent path without `O_CREAT`).
   - *Break:* Reproduce `EACCES` (modify permissions with `chmod 400` and attempt to write).
   - *Break (Safe ENOSPC):* In a bounded small temporary directory or tmpfs with a tight size limit, write until `ENOSPC` (No space left on device) is triggered.
   - *Explain:* Explain how an application must handle partial writes when space is exhausted.
   - *Safety Guard:* Strictly forbid manipulating host raw block devices or filling the main root filesystem.
9. **Required Commands / Tools:** Python 3.12, `chmod`, standard Linux CLI.
10. **Machine-Checkable Evidence:** Automated test script verifying that attempting to open a read-only file in write mode raises `PermissionError` (errno 13 / `EACCES`) and captures the exact error code.
11. **Reviewer-Required Evidence:** Learner demonstrates correct diagnostic triage matching observed symptoms to the underlying operating system error code.
12. **Misconceptions Addressed:**
    - "A file error is just a programming syntax mistake."
    - "Disk full errors always crash the program immediately."
13. **What You Can Ignore—for Now:** Quota management daemons, distributed filesystem network timeouts, SELinux/AppArmor MAC policy debugging.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Decision tree diagram: Syscall failed $\rightarrow$ Check `errno` $\rightarrow$ Map to subsystem cause (`ENOENT`, `EACCES`, `ENOSPC`).
16. **Exit Criteria:** Learner reproduces and diagnoses `ENOENT`, `EACCES`, and `ENOSPC` using standard tools.
17. **Competency Mapping:** Diagnose (I/O failures), Observe (`errno` / exceptions).
18. **Provenance / Source Anchors:** POSIX.1-2024 Base Definitions §2.3 (Error Numbers: `errno.h`).
19. **Failure / Inference Limits:** The `errno` value is set by the C library wrapper from the negative return value of the Linux syscall; multi-threaded code must access thread-local `errno`.

---

## 9. Module M09 Design — Storage Engine & Durable Storage

### 9.1 Module-Level Specification
- **Title:** M09 — Storage Engine & Durable Storage (Area 06)
- **Primary Competency:** Judge
- **Growth Competencies:** Estimate, Explain, Diagnose
- **Module Prerequisites:** Hard: M08; Soft/Preferred: M04
- **Canonical Concept First Home:** **EC-CON-016 Durability (持久性)** at `L09-01`.
- **Capability Transition:** Transition from naively assuming that saving to a file guarantees permanence to exercising rigorous technical judgment regarding what constitutes **Durability** under explicit crash and power-loss failure models, navigating trade-offs between sync overhead, storage media physics (SSD vs HDD), and storage architectures.

---

### 9.2 Lesson L09-01: “What does durable actually mean?”

1. **Learner Question:** When can I honestly claim that my data is safe, and what happens to written files if the power cuts out?
2. **Before / After Capability:**
   - *Before:* Believes that once `file.write()` completes or the file appears in `ls`, it is permanently saved.
   - *After:* Can define **Durability** under a named failure model, explain the role of `fsync()` and write-ahead logging (WAL), and distinguish user buffers, kernel page cache, and non-volatile media.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: M08 (`L08-02` page cache).
   - Support: Use small Python scripts comparing `write()` with and without `os.fsync()`.
4. **Concepts:** **EC-CON-016 Durability (First Home)**: A committed state survives a named restart or failure bound. Revisits **Trade-off** (EC-CON-006), **Failure** (EC-CON-010).
5. **Mental Model:** Durability is not a property of a file; it is a contract about surviving specific failure events. True power-loss durability requires explicitly synchronizing dirty page-cache data and metadata to non-volatile physical storage media.
6. **Mechanism Sequence (The Durability Sync Journey):**
   $$\text{User Buffer} \xrightarrow{\text{flush()}} \text{Page Cache} \xrightarrow{\text{fsync()}} \text{Disk Controller Volatile RAM} \xrightarrow{\text{Device Cache Flush}} \text{Non-Volatile Flash / Platters}$$
7. **Prediction-Before-Observation:** If you call `fsync()` after every single write of 100 bytes, what will happen to write throughput compared to ordinary buffered writes?
8. **Hands-on Progression (Observe / Build / Break / Explain / Judge):**
   - *Build / Observe:* Measure the elapsed time of 1,000 small writes without `fsync` vs with `os.fsync()` after each write; observe that calling `fsync` may introduce substantial latency overhead depending on workload and storage environment.
   - *Explain:* Explain why: `fsync` requests synchronization according to OS, filesystem, and storage contracts, halting execution until the synchronization request is completed.
   - *Explain (Concept):* Introduce Write-Ahead Logging (WAL) as a technique to achieve durability without random disk seek/rewrite overhead.
   - *Judge:* Formulate a trade-off judgment: when should an application call `fsync` immediately (financial transactions) vs periodically (document auto-save)?
9. **Required Commands / Tools:** Python 3.12 (`os.fsync`, `time.perf_counter`).
10. **Machine-Checkable Evidence:** Automated test script measuring and asserting that 100 writes with `os.fsync()` take measurably longer than 100 purely buffered writes.
11. **Reviewer-Required Evidence:** Learner formulates a defensible durability policy for a hypothetical service, explicitly naming the failure bound, sync point, and acceptable data loss window.
12. **Misconceptions Addressed:**
    - "`write()` success means data is safe from power loss."
    - "`close()` guarantees durability."
    - "`fsync` is a substitute for backups."
    - "Replication solves all durability problems."
13. **What You Can Ignore—for Now:** Database ACID transaction manager code, full B-Tree recovery algorithms, battery-backed RAID controller write cache configurations.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Diagram contrasting un-synchronized writes (lost on power failure) with `fsync` forcing data into non-volatile media, plus a conceptual WAL timeline.
16. **Exit Criteria:** Learner defines Durability under a named failure bound and demonstrates the latency cost of `fsync`.
17. **Competency Mapping:** Judge (durability vs throughput trade-off), Explain (WAL concept).
18. **Provenance / Source Anchors:** POSIX.1-2024 `fsync(2)`, `fdatasync(2)` & Pillai et al. (OSDI '14).
19. **Failure / Inference Limits:** `fsync()` requests synchronization according to OS, filesystem, and storage contracts; the resulting durability guarantee depends on the named failure model and the behavior of the storage stack. It does not protect against physical disk destruction or catastrophic hardware failure.

---

### 9.3 Lesson L09-02: “Why are SSD and HDD behavior different?”

1. **Learner Question:** Why do Solid State Drives (SSDs) and Hard Disk Drives (HDDs) behave so differently, and why does how I write data change their performance and lifespan?
2. **Before / After Capability:**
   - *Before:* Assumes SSDs are just "super fast hard drives" with identical internal behavior.
   - *After:* Can contrast mechanical seek/rotation physics of HDDs with semiconductor NAND flash physics of SSDs, explaining out-of-place updates, the Flash Translation Layer (FTL), garbage collection, wear leveling, and write amplification.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: M04 (`L04-02` Locality and measurement discipline).
   - Support: Provide conceptual calculation templates for write amplification; do not require raw disk hardware tests.
4. **Concepts:** Revisits **Locality** (EC-CON-012), **Trade-off** (EC-CON-006), **Representation** (EC-CON-003).
5. **Mental Model:** HDDs are mechanical: random I/O requires physical arm movement (slow), while sequential I/O is fast. SSDs are electronic: reads/writes occur in pages, but erases occur only in large blocks. SSDs cannot overwrite in place, requiring an internal controller (FTL) to shuffle and rewrite data.
6. **Mechanism Sequence (SSD Flash Translation):**
   $$\text{Host Writes Page} \xrightarrow{\text{FTL remaps LBA to new physical page}} \text{Old physical page marked invalid} \xrightarrow{\text{Garbage Collection}} \text{Read valid pages + Erase Block + Rewrite}$$
7. **Prediction-Before-Observation:** If you overwrite a 4 KiB file on an SSD 1,000 times, does the flash memory write exactly 4 MB of data?
8. **Hands-on Progression (Observe / Explain / Judge):**
   - *Observe / Calculate:* Work through an FTL garbage collection scenario: updating a single 4 KiB page in a block where 63 other pages are valid forces reading and rewriting the entire 256 KiB block.
   - *Explain:* Define Write Amplification Factor ($\text{WAF} = \frac{\text{Bytes Written to Flash}}{\text{Bytes Written by Host}}$). Explain why random small writes degrade SSD performance and lifespan.
   - *Explain:* Explain Wear Leveling: why the FTL dynamically distributes writes across all physical flash blocks to prevent uneven cell wear.
   - *Judge:* Judge why append-only logs (WAL) are structurally friendly to both HDDs (sequential heads) and SSDs (sequential page writes minimizing GC).
9. **Required Commands / Tools:** Calculation worksheet / Python simulation script.
10. **Machine-Checkable Evidence:** Automated test verifying that a learner's calculation function correctly computes WAF and estimated drive write endurance under varying workload patterns.
11. **Reviewer-Required Evidence:** Learner provides a mechanism-level comparison contrasting why random writes hurt HDDs (mechanical seek time) vs why they hurt SSDs (garbage collection and write amplification).
12. **Misconceptions Addressed:**
    - "SSDs overwrite data in place like RAM."
    - "SSDs have infinite lifespan because they have no moving parts."
    - "Sequential access only matters for mechanical disks."
13. **What You Can Ignore—for Now:** NAND cell voltage levels (SLC/MLC/TLC/QLC physics), charge-trap transistor chemistry, specific vendor controller algorithms.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Comparison diagram: HDD mechanical arm/platter seek vs SSD NAND Flash Block (Pages, Invalidation, Garbage Collection, Erase).
16. **Exit Criteria:** Learner explains FTL, wear leveling, and write amplification, contrasting HDD and SSD physical constraints.
17. **Competency Mapping:** Explain (storage media mechanics), Judge (workload fit).
18. **Provenance / Source Anchors:** SNIA Solid State Storage Technical Working Group & OSTEP Chapters 40, 44.
19. **Failure / Inference Limits:** Drive endurance specifications (TBW - Terabytes Written) are probabilistic manufacturer warranties based on standardized test workloads (JESD218/219); real-world lifespan varies by temperature and access pattern.

---

### 9.4 Lesson L09-03: “Where should data live?”

1. **Learner Question:** When should data be stored in a local file, on a block volume, or in cloud object storage, and how do I estimate the cost?
2. **Before / After Capability:**
   - *Before:* Views storage options as arbitrary brand names (AWS EBS vs S3) without architectural understanding.
   - *After:* Can evaluate and compare Block Storage, File Storage, and Object Storage using the Technology Evaluation Framework, performing order-of-magnitude cost, latency, and throughput estimates.
3. **Prerequisites & Hidden-Prerequisite Support:**
   - Prerequisite: `L09-01`, `L09-02`.
   - Support: Provide transparent reference cost and latency tables clearly labeled as CURRENT PRACTICE.
4. **Concepts:** Revisits **Trade-off** (EC-CON-006), **Abstraction** (EC-CON-002), **Interface** (EC-CON-005).
5. **Mental Model:** Storage architectures trade latency and interface flexibility for scale and cost. Block storage provides low-latency raw bytes for filesystems; file storage provides managed POSIX hierarchies; object storage provides massive, low-cost, immutable key-value blobs over HTTP.
6. **Mechanism Comparison:**
   - *Block Storage:* Raw LBA sectors $\rightarrow$ single-host attached $\rightarrow$ sub-millisecond latency $\rightarrow$ higher cost ($\sim \$0.10/\text{GB-month}$).
   - *File Storage:* Hierarchical POSIX tree $\rightarrow$ multi-client shared $\rightarrow$ low-to-medium latency $\rightarrow$ medium cost.
   - *Object Storage:* Flat key/blob namespace over HTTP REST $\rightarrow$ unlimited scale $\rightarrow$ higher latency ($20\text{--}100\text{ ms}$) $\rightarrow$ lowest cost ($\sim \$0.02/\text{GB-month}$).
7. **Prediction-Before-Observation:** For storing 50 million user profile images, why is a standard local POSIX directory a poor choice compared to an object store?
8. **Hands-on Progression (Estimate / Judge):**
   - *Estimate:* Calculate the monthly storage and request cost for a 10 TB dataset accessed 1,000,000 times a month across Block, File, and Object storage using provided current reference pricing.
   - *Judge:* Apply the Technology Evaluation Framework: Problem, Constraints, Mechanism, Gains, Costs, Failure Modes, and When-not-to-use.
   - *Observe:* Inspect a simulated or public object storage endpoint: HTTP PUT/GET, metadata headers, etag immutability.
9. **Required Commands / Tools:** Python 3.12 calculation script, `curl` or `requests`.
10. **Machine-Checkable Evidence:** Automated evaluation verifying that the learner's cost-estimation function correctly models storage capacity cost + request/egress cost within order-of-magnitude bounds.
11. **Reviewer-Required Evidence:** Learner defends an architectural storage selection for a concrete system scenario, identifying trade-offs and when the chosen solution should NOT be used.
12. **Misconceptions Addressed:**
    - "Object storage is just a normal filesystem on the web."
    - "Cloud storage pricing is permanent and fixed."
13. **What You Can Ignore—for Now:** Multi-region bucket replication consistency math, AWS IAM policy syntax, custom S3 lifecycle rule scripting.
14. **Progressive Support:** Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation.
15. **Visual Requirements:** Storage Architecture Comparison Matrix (Block vs File vs Object: Interface, Unit, Latency, Scalability, Cost per GB).
16. **Exit Criteria:** Learner compares Block, File, and Object storage and produces an order-of-magnitude cost/latency estimate.
17. **Competency Mapping:** Judge (storage architecture selection), Estimate (storage economics).
18. **Provenance / Source Anchors:** SNIA Storage Architecture Models & Current Public Cloud Storage Documentation.
19. **Failure / Inference Limits:** Pricing and latency numbers are illustrative current practice (checked 2026-09-02); they are not permanent computing constants and must be re-verified for production decisions.

---

## 10. Shared Environment & Preflight Contract

### 10.1 Status of OQ-BP-006
**OQ-BP-006 remains OPEN.** This design defines the toolchain requirements and preflight verification checks for M05–M09, but deliberately leaves immutable digest pinning to the implementation preflight phase.

### 10.2 Preflight Capabilities Matrix

| Tool / Subsystem | Required for Core? | Environment-Sensitive? | Privileged / Security Context | Fallback Path |
|---|---|---|---|---|
| **Python 3.12+** | Yes (M05, M06, M08, M09) | No | Unprivileged | None (Mandatory Core tool) |
| **GCC 13+ (Native)** | Yes (M05, M06, M07) | Architecture-specific | Unprivileged | None (Standard toolchain) |
| **GNU Binutils (`objdump`)** | Yes (M05, M06, M07) | Architecture-specific | Unprivileged | Python `dis` for bytecode; recorded disassembly for native |
| **`ps` & `/proc`** | Yes (M06, M07, M08) | Standard Linux | Unprivileged | Standard POSIX utilities |
| **`strace`** | Yes (M06, M08) | **Yes** (ptrace policy) | Restricted in some containers | `/proc/<pid>/status` & non-tracing observation fixtures |
| **QEMU & RISC-V GCC** | Yes (LAB-REQ-02) | Yes (Package presence) | Unprivileged user process | Source-reading expedition + recorded deterministic trace |
| **GDB** | **No (Optional only)** | High (ptrace policy) | Restricted | Decoupled; zero GDB dependencies in Core M05–M09 |
| **Raw Block Tools (`debugfs`)** | **Forbidden for Core** | Yes | **Requires Root/Sudo** | Loopback file images and standard filesystem APIs |

### 10.3 Preflight Verification Script Contract
Implementation must supply a deterministic preflight script (`scripts/preflight-m05-m09.sh`) that checks and records:
1. Linux distribution and kernel version (`uname -a`).
2. Python version (`python3 --version`).
3. Native C compiler and binutils (`gcc --version`, `objdump --version`).
4. ptrace tracing capability (`strace true >/dev/null 2>&1`). If restricted, report warning and activate procfs fallback mode without failing the preflight.
5. RISC-V toolchain and QEMU emulator (`qemu-system-riscv64 --version`, `riscv64-linux-gnu-gcc --version`).

---

## 11. Evidence & Assessment Matrix

| Module / Activity | Primary Evidence Produced | Assessment Mode | Machine-Checkable Portion | Reviewer-Required Portion |
|---|---|---|---|---|
| **M05** (L05-01..03) | AST dump, bytecode trace, type invariant test | Explain, Trace, Break | AST node assertions, bytecode operation class matching, type error raising | Accuracy of source-to-machine explanation; distinction between Python spec and CPython implementation |
| **M06** (L06-01..03) | Procfs status parse, fork/exec lifecycle log, zombie diagnosis | Trace, Observe, Diagnose | PID matching, exit code parsing ($42$), zombie status verification in procfs | Explanation of user/kernel boundary and scheduling preemption intuition |
| **LAB-REQ-02** (xv6) | `user/sleep.c`, modified `Makefile`, grade transcript | Trace, Observe, Diagnose | `./grade-lab-util sleep` outputs `OK`, error exit on missing argument | Understanding of `pause/sys_pause` trap route; explanation of tick vs wall-clock time |
| **M07** (L07-01..03) | `/proc/self/maps` breakdown, VSZ vs RSS test, SIGSEGV signal record | Explain, Diagnose, Trace | Segment permission matching, `ru_minflt` growth assertion, signal 11 termination | Distinction between Isolation and Trust Boundary; explanation of MMU page fault sequence |
| **M08** (L08-01..03) | Inode link count log, buffered I/O trace, POSIX error reproduction | Trace, Observe, Diagnose | Inode equality check across links, `write()` batching ratio, `EACCES`/`ENOENT` errno capture | Explanation of write-path checkpoints and durability boundary; explanation of why `write()` success $\neq$ durability |
| **M09** (L09-01..03) | `fsync` latency timing distribution, WAF calculation, storage cost model | Judge, Estimate, Explain | `fsync` timing delta assertion, WAF formula execution, cost arithmetic verification | Defensibility of durability policy under named failure bound; mechanism contrast of SSD vs HDD |

---

## 12. Canonical Concept First-Home Audit

This design guarantees that the four canonical first homes in this scope are strictly introduced and never duplicated:

1. **EC-CON-018 Process (进程):**
   - *First Home:* M06 `L06-01`.
   - *Audit Check:* M00 and M05 use the term "process" as an informal execution context; neither provides the canonical definition. M07, M08, and M09 revisit Process as an established concept.
2. **EC-CON-013 Isolation (隔离):**
   - *First Home:* M07 `L07-01`.
   - *Audit Check:* M06 `L06-03` previews that processes are separated by OS protection, but explicitly defers the formal definition of Isolation to M07.
3. **EC-CON-017 Trust Boundary (信任边界):**
   - *First Home:* M07 `L07-01`.
   - *Audit Check:* M06 introduces user/kernel dual-mode privilege as a mechanism; M07 `L07-01` formally introduces Trust Boundary as the conceptual contract and explicitly contrasts it with Isolation.
4. **EC-CON-016 Durability (持久性):**
   - *First Home:* M09 `L09-01`.
   - *Audit Check:* M08 `L08-02` explicitly discusses the page cache and notes that `write()` does not guarantee persistence, but deliberately defers the formal definition of Durability to M09 `L09-01`.

---

## 13. Visual System Requirements

Implementation must supply clean, mobile-readable, vendor-neutral Mermaid or SVG diagrams satisfying these exact roles:

1. **M05 Visuals:**
   - *Diagram 5.1:* The Language Pipeline: Source Text $\rightarrow$ Tokens $\rightarrow$ AST $\rightarrow$ Bytecode $\rightarrow$ Virtual Machine Execution Loop.
   - *Diagram 5.2:* Invariant Gates: Static Type Checking (pre-execution) vs Dynamic Type Checking (in-flight dispatch).
2. **M06 Visuals:**
   - *Diagram 6.1:* Program on Disk (ELF) vs Active Process in Memory (PCB, Address Space, File Tables).
   - *Diagram 6.2:* The System Call Trap: User Mode (Ring 3) $\rightarrow$ Trap Instruction (`ecall`/`syscall`) $\rightarrow$ Kernel Vector Table $\rightarrow$ Kernel Mode (Ring 0) $\rightarrow$ Return.
   - *Diagram 6.3:* Process Lifecycle State Machine (Created, Ready, Running, Blocked, Zombie, Terminated).
3. **M07 Visuals:**
   - *Diagram 7.1:* Virtual Address Space Translation: VPN + Offset $\rightarrow$ MMU/Page Table $\rightarrow$ PFN + Offset.
   - *Diagram 7.2:* Two-Process Address Space Isolation (disjoint physical frames).
   - *Diagram 7.3:* Conceptual Venn Diagram / Matrix: Isolation Boundary vs Trust Boundary.
   - *Diagram 7.4:* Hardware Page Fault Evaluation Flowchart (Valid? Permitted? $\rightarrow$ Minor/Major/SIGSEGV).
4. **M08 Visuals:**
   - *Diagram 8.1:* POSIX File Indirection Architecture: Process FD Table $\rightarrow$ Open File Table $\rightarrow$ Inode Table $\rightarrow$ Directory Entries.
   - *Diagram 8.2:* Write-Path Checkpoints: User Buffer $\rightarrow$ Kernel Page Cache $\rightarrow$ Block Device Queue.
5. **M09 Visuals:**
   - *Diagram 9.1:* Durability Synchronization Stack: Volatile Caches vs Non-Volatile Media under Power-Loss Bounds.
   - *Diagram 9.2:* Write-Ahead Logging (WAL) Timeline: Sequential Log Commit before Lazy In-Place Checkpointing.
   - *Diagram 9.3:* HDD Seek/Rotation vs SSD Flash Block Erase & Garbage Collection.

---

## 14. Progressive-Support Requirements

All 15 Lessons must implement the strict collapsed progressive disclosure structure. `<details open>` is **forbidden**.

```markdown
### Checkpoint Investigation

#### Question
[Clear, falsifiable prompt requiring prediction or investigation]

<details>
<summary>Hint 1</summary>
[Guidance on which tool, command, or file boundary to inspect]
</details>

<details>
<summary>Hint 2</summary>
[Specific syntax, expected parameter, or flags to use]
</details>

<details>
<summary>Expected Observation</summary>
[Pattern, relationship, or structural outcome to verify — no brittle hard-coded offsets or timestamps]
</details>

<details>
<summary>Full Explanation</summary>
[Comprehensive mechanism explanation connecting the observation to the underlying mental model]
</details>
```

---

## 15. Source & Provenance Rules

1. **Normative References:**
   - System interfaces must cite **POSIX.1-2024** (IEEE Std 1003.1-2024 / Issue 8).
   - Python mechanics must cite official **Python 3.12/3.13 Documentation**.
   - Linux kernel mechanisms must cite **Linux Kernel Documentation** (`docs.kernel.org`).
   - Storage mechanics must cite **SNIA Solid State Storage Technical Guidelines**.
2. **Licensing & Adaptation Rules:**
   - xv6 code adapted for LAB-REQ-02 must preserve the original MIT copyright notice in source files.
   - Do NOT copy MIT 6.1810 assignment HTML text or textbook diagrams. All instructional text and diagrams must be original Essential CS creations licensed under CC BY-SA 4.0.
   - OSTEP and research papers (OSDI '14) are referenced for explanatory models; do not reproduce large text excerpts.

---

## 16. Cross-Module Handoffs & Mini Cloud App Hooks

### 16.1 Handoff Chain
- **M05 $\rightarrow$ M06:** M05 ends with bytecode executing in a VM runtime; M06 starts by wrapping that runtime inside an operating system process.
- **M06 $\rightarrow$ M07:** M06 establishes that processes are distinct execution contexts; M07 explains the virtual memory mechanism that makes memory isolation possible.
- **M07 $\rightarrow$ M08:** M07 establishes address spaces and memory-mapped pages; M08 introduces files and the page cache that bridges memory with storage.
- **M08 $\rightarrow$ M09:** M08 traces file I/O up to the kernel page cache and block device boundary; M09 introduces the durability guarantees needed to survive crashes and power failure.

### 16.2 Mini Cloud App (P0–P9) Revisit Hooks
*Note: Project milestone order is an application spine, NOT a curriculum DAG dependency.*
- **P0 Revisit (M08/M09):** The single-process local collection now receives concrete persistence reasoning: state files can be inspected via file descriptors, and the restart survival claim is evaluated under explicit durability failure bounds.
- **P1 Hook (M05/M06):** The CLI boundary is explained as an OS process invocation taking `argv` through `execve`.
- **P7 Hook (M05/M07):** Previews native Linux processes vs containerized environments without prematurely teaching container runtime internals.

---

## 17. Explicit Non-Goals & Later-Module Boundaries

To prevent cognitive bloat and premature curriculum expansion, the following topics are strictly forbidden in M05–M09:
- **Full Compiler Construction:** No grammar writing, parser generators, or AST optimization passes (reserved for Deep Dives).
- **Formal Type Theory:** No lambda calculus, Hindley-Milner algorithms, or proof systems.
- **Scheduler Internals:** No Linux CFS red-black tree math, real-time deadlines, or cgroups CPU shares.
- **Signal Programming Deep Dive:** No complex async-signal-safe reentrancy puzzles.
- **Page Table Implementation:** No writing custom OS page-table allocators or assembly page walks.
- **Exploitation & Security Attacks:** No buffer overflows, ROP gadget chaining, or shellcode injection (Security Synthesis belongs in M21/M22).
- **Container Internals:** No Linux namespaces, cgroups, or overlayfs (belongs in M19).
- **Filesystem Internals:** No Ext4 on-disk superblock or extent-tree programming.
- **Full Storage Engine:** No custom B-Tree or LSM-Tree implementation (belongs in M13/M14).
- **Cloud Vendor Certifications:** No proprietary AWS/GCP/Azure operational tool tutorials.

---

## 18. Implementation Handoff

The subsequent Implementation Agent may proceed directly to drafting Lessons, activities, and tests, adhering to:
1. **Directory Locations:**
   - Lessons: `book/m05-.../`, `book/m06-.../`, etc.
   - Lab Code: `labs/lab-req-02-xv6-syscall/`
   - Preflight Script: `scripts/preflight-m05-m09.sh`
2. **File Structure:**
   - Each Lesson in its own Markdown file following the standard pedagogical loop.
   - Progressive disclosure using strictly collapsed `<details>` blocks.
3. **Verification Obligation:**
   - Implementation must run the automated preflight script and record real tool output in the author evidence record.

---

## 19. Risks & Design Blockers

- **Container Tracing Restrictions:** `strace` may fail in heavily restricted Docker containers without `SYS_PTRACE`. *Mitigation:* The design specifies non-privileged procfs observation as an approved alternative.
- **QEMU Emulation Overhead:** Nested virtualization may slow QEMU boot on low-end cloud hosts. *Mitigation:* Bounded smoke-test timing should be recorded during implementation and a deterministic fallback trace provided.
- **M03 GDB Debt:** GDB interactive verification remains open. *Mitigation:* GDB is completely excluded from the critical path of M05–M09.

---

## 20. Final Recommendation

**READY FOR LESSON / ACTIVITY IMPLEMENTATION**

The module architectures, lesson specifications, activity contracts, assessment matrices, visual roles, and provenance boundaries for M05 through M09 are fully established and aligned with repository invariants.

---

## 21. Completion Report

### Status
**READY FOR LEAD REVIEW**

### Exact Base
`a5dabc0429a18022c60ab7f18495becd870cdca0` (Assigned branch: `design/issue-50-m05-m09-runtime-os-persistence`)

### Exact Files Changed
- `meta/design/runtime-os-persistence-m05-m09-design-v0.1.md` (1 new file)

### Research Dependency
Accepted Research Dossier (`research/runtime-os-persistence-m05-m09-v0.1.md` via Issue #47 / PR #48), including Web Lead normative source-recheck corrections (`ad757ac`), served as the authoritative basis.

### Module Design Summary
- M05: Languages as interface specifications, translation pipeline (source $\rightarrow$ AST $\rightarrow$ bytecode $\rightarrow$ VM), types as invariants.
- M06: Process context, user/kernel privilege rings, syscall boundary, process lifecycle (`fork`/`exec`/`wait`/`exit`), scheduling intuition.
- M07: Virtual memory address translation, demand paging, memory allocation boundaries (VSZ vs RSS), page fault mechanisms (minor, major, SIGSEGV), Isolation vs Trust Boundary.
- M08: File descriptors, open file table, inodes, path resolution, page cache buffering, write-path checkpoints, I/O failure triage (`ENOENT`, `EACCES`, `ENOSPC`).
- M09: Durability defined under named failure bounds, `fsync` overhead, WAL concept, SSD vs HDD physical mechanisms (seek vs FTL/wear leveling/WAF), storage architecture comparison (Block vs File vs Object).

### Lesson Contracts
All 15 canonical preliminary Lesson IDs are strictly preserved (`L05-01` through `L09-03`).

### Canonical First-Home Check
- `EC-CON-018 Process`: M06 `L06-01` (Preserved).
- `EC-CON-013 Isolation`: M07 `L07-01` (Preserved).
- `EC-CON-017 Trust Boundary`: M07 `L07-01` (Preserved; Isolation $\neq$ Trust Boundary enforced).
- `EC-CON-016 Durability`: M09 `L09-01` (Preserved; write-path checkpoints and failure bounds enforced).

### LAB-REQ-02 Check
- Current Fall 2025 xv6 `sleep` user program $\rightarrow$ `pause/sys_pause` syscall route specified.
- MIT License notices preserved; assignment prose treated as link-only.
- M08 inspection-only revisit of `sysfile.c`/`file.c` specified without duplicate lab.
- Deterministic fallback path provided for restricted environments.

### Environment Check
- OQ-BP-006 remains OPEN.
- Tooling categorized (Core, Optional, Environment-Sensitive).
- `strace` bounded with procfs fallback.
- GDB decoupled from Core path.

### Evidence Matrix
Complete machine-checkable vs reviewer-required evidence rubric specified for all modules.

### Visual & Progressive Support
12 distinct visual diagram specifications and standard collapsed progressive support ladders (`Question $\rightarrow$ Hint 1 $\rightarrow$ Hint 2 $\rightarrow$ Expected Observation $\rightarrow$ Full Explanation`) mandated.

### Provenance
Grounded in POSIX.1-2024, Python 3.12 documentation, Linux Kernel Documentation, MIT 6.1810, SNIA, and OSTEP.

### Risks & Limitations
Container ptrace limitations and QEMU emulation overhead are identified with explicit non-privileged fallbacks.

### Routing Classification
**SIMPLE DESIGN FIX** / No architectural blockers or escalations.

### Recommended Lead Focus
1. Confirm realignment of LAB-REQ-02 to the `pause/sys_pause` syscall route.
2. Confirm the 4-way separation of Path, FD, Open File Description, and Inode in M08.
3. Validate the Isolation vs Trust Boundary conceptual distinction in M07.
4. Review the write-path checkpoints and durability failure-model framing in M09.

### Final Dossier Recommendation
**READY FOR LESSON / ACTIVITY IMPLEMENTATION**
