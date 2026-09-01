# Foundations M03 — learner evidence template

> 核心纪律：**Do not let an observation silently become a guarantee.** 每个重要 claim 都标明它来自 C semantics / x86-64 ISA / System V AMD64 ABI / compiler-build observation / hosted Linux observation 中哪一层。

## A — Preflight

- Commit / branch / context:
- Date:
- OS (`uname -a`):
- Architecture (`uname -m`):
- Compiler + version:
- objdump/binutils + version:
- GDB + version:
- Git + version:
- Python + version（若使用）:
- Shell/runtime:
- Build flags:
- Preflight result: `PASS / PARTIAL / BLOCKED`
- Environment limitation（若有）:

## B — Source ↔ instruction mapping

- Exact source operation / line:
- Named function:
- Instruction range（本次 build 的地址，不是 universal address）:
- Relevant instruction(s):
- Observed register value(s):
- Observed pointee/memory value:
- State transition I can support from evidence:
- Claim layer(s):
- **What this evidence supports:**
- **What it does not establish:**

## C — Before call / in callee / after return

### C1 — Caller before call
- `$rip`:
- argument registers relevant here (`$rdi/$rsi/$rdx`):
- `$rsp`:
- `$rbp` / observed frame-region note:
- pointee address + memory value:
- interpretation:
- claim layer:

### C2 — Callee after entry
- `$rip`:
- observed `a`, `b`, `item`:
- `$rsp`:
- `$rbp` / observed frame-region note:
- `item->value`:
- `local` after its assignment:
- interpretation:
- claim layer:

### C3 — Caller after return
- `$rip`:
- `$rax` (return result observation point):
- `$rsp`:
- `$rbp`:
- relevant memory value:
- interpretation:
- claim layer:

## D — Call-frame sketch

Draw/fill the addresses and values you actually observed. Include caller/callee boundary, instruction pointer, stack pointer, frame pointer/region, arguments/result, and one local or pointee.

> **Required boundary statement:** observed build-specific layout, not universal ABI frame shape.

```text
higher address
+-------------------------------+
| observed caller region        |
+-------------------------------+
| ...                           |
| observed callee frame region  |  <- fill actual addresses/values
| ...                           |
+-------------------------------+
lower address
```

## E — Failure evidence

- Prediction before run:
- Invalid source operation:
- C semantics status (`defined / undefined behavior / other`):
- Exact command:
- Observed signal/stop/exit:
- GDB evidence excerpt / location:
- Bounded conclusion:
- **NOT PROVEN:**
  - complete root cause?
  - virtual-memory mechanism?
  - exact protection rule?
  - Process/Isolation semantics?
  - same signal on every C implementation/build?

## F — Claim-layer table

| My claim | Layer: C / ISA / ABI / compiler-build / hosted Linux | Evidence / authority |
|---|---|---|
| | | |
| | | |
| | | |
| | | |
| | | |

## G — Fact vs guess

- **Fact from evidence:**
- **Current hypothesis / guess:**
- **Additional evidence needed to distinguish it:**

## H — RISC-V transfer

Using only the supplied ratified-spec transfer card:

- One ISA-generic observation:
- One x86-64-specific item:
- One ABI/compiler-specific item:
- Why this does **not** require a RISC-V toolchain now:

## Support metadata

Highest support used: `Independent / Hint 1 / Hint 2 / Expected Observation / Full Explanation`

If Full Explanation was used, record a short new-context transfer check before claiming independent competence.
