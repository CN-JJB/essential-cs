# Foundations M05 Evidence Template

## A — Environment / Preflight
- Dispatch / Working Commit:
- Operating System:
- Hardware Architecture:
- Python Implementation:
- Python Version:
- Compiler & Version (if C fixture used):
- Git Version:
- Preflight Status (PASS / PARTIAL / BLOCKED):
- Preflight Notes:

---

## B — Source Prediction (Write before running inspection)
- For `def add(a, b): return a + b`:
  - Does Python execute `return a + b` directly as a native CPU `ADD` instruction?
  - Prediction:
  - Why:
- For `(a + b) * c`:
  - When parsed into an AST, which operator (`+` or `*`) do you expect at the root of the expression tree?
  - Prediction:
  - Why:
- For types:
  - When will `"5" + 1` fail in Python? (At parse time, bytecode compile time, or runtime?)
  - Prediction:
  - What do you expect when compiling an incompatible type assignment in C?
  - Prediction:

---

## C — AST Evidence
- Source Fixture:
- Command Run: `python inspect_runtime.py`
- Structural Relationship Observed:
  - Precedence tree structure for `(a + b) * c`:
- Actual Output Excerpt:
```text
[Paste excerpt of AST dump here]
```
- Interpretation (How does the AST reflect operator precedence and syntax structure?):

---

## D — Bytecode Evidence
- Python Implementation & Version Used:
- Observed Instructions / Operations:
```text
[Paste excerpt of dis output here]
```
- Operation Relationships Observed:
  - Loading of arguments:
  - Binary operation:
  - Return operation:
- Which Details are Version-Specific to Your Environment?
  - (e.g. `LOAD_FAST` vs `LOAD_FAST_LOAD_FAST`, `BINARY_OP` vs `BINARY_ADD`, line/offset numbering):
- What This Bytecode Evidence Does NOT Prove:
  - (Does not prove hardware execution, does not define the universal Python language specification):

---

## E — Language Specification vs Implementation Table
Classify each claim into its proper layer: `Python Language Specification`, `CPython Implementation`, or `Observed Version/Build`.

| Claim | Claim Layer | Justification |
|---|---|---|
| In `a + b * c`, multiplication has higher precedence than addition | | |
| Evaluating `"5" + 1` raises `TypeError` | | |
| `def add(a, b): return a + b` generates opcode `LOAD_FAST_LOAD_FAST` or `LOAD_FAST` | | |
| Bytecode is executed by a software loop (`_PyEval_EvalFrameDefault`) | | |
| Evaluating `add(10, 20)` produces integer `30` | | |
| Memory offset of the return instruction is offset `8` or `12` | | |

---

## F — Syntax Failure Evidence
- Fixture Run:
- Command / Method:
- Error Class Caught:
- When was the error caught? (Parse time before execution vs runtime during execution):
- Output / Traceback Excerpt:

---

## G — Dynamic Type Failure Evidence
- Fixture Run:
- Error Class Caught:
- Actual Exception Message:
- When was the type checked? (At compile time vs when the binary addition was dispatched):

---

## H — Static / Compiler Diagnostic Comparison
- C Fixture: `type_check.c`
- Compiler Used & Version:
- Flags Used & Result:
  - Default flags (`gcc -c type_check.c`):
    - Exit code:
    - Diagnostic status (warning / error):
  - With `-fpermissive` (if GCC 14+):
    - Exit code:
    - Diagnostic status:
  - With `-Werror`:
    - Exit code:
    - Diagnostic status:
- Diagnostic Text Excerpt:
- Explanation: Why is `-Werror` promoting a warning to an error different from a mandatory universal language-level compile error?

---

## I — Type / Invariant Explanation
- What invariant does the type system enforce in this example?
- Invariant definition:
- Enforcement point comparison (Dynamic / Python vs Static / C):
- Why does "passes static type checking" NOT guarantee that the program is completely correct?

---

## J — Authoritative Source Verification
- Selected Claim:
- Primary Source Cited (e.g. Python Language Reference §X, POSIX, ISO C):
- Why this source has authority over blog posts or tool output:
- Source Quote / Citation:

---

## K — Fact vs Inference / Limitations
- What facts did your inspection directly establish?
- What competing explanations or implementation variations exist?
- What are the limitations of your evidence? (e.g., Python minor version differences, compiler flag dependencies):
