# M05 Activity — Languages, VM & Compiler Pipeline

This hands-on activity supports Lessons `L05-01`, `L05-02`, and `L05-03`.

It provides tools and fixtures to inspect:
1. **Source to Machine Boundary (L05-01):** How Python source is converted to an AST, compiled to CPython bytecode, and executed by a virtual machine.
2. **Grammar & Structured Syntax (L05-02):** How parsing produces hierarchical ASTs that reflect operator precedence, and how syntax errors halt translation before runtime.
3. **Type Systems as Invariants (L05-03):** The operational difference between runtime dynamic type checks in Python and pre-execution static compiler diagnostics in C.

---

## File Structure

- `fixtures.py`: Source code fixtures, including arithmetic functions, precedence expressions, and a tiny AST evaluator.
- `type_check.c`: Minimal C program demonstrating compile-time type mismatch diagnostics.
- `inspect_runtime.py`: Inspection runner that logs environment preflight, AST dumps, bytecode instructions, and diagnostic outputs.
- `test_activity.py`: Unit tests validating structural relationships, error handling, and compiler diagnostics.
- `reset.py`: Cleanup utility to remove temporary compiled files and caches.

---

## Activity Flow

### 1. Preflight & Environment Check
Run the inspector to record your exact execution environment:
```bash
python inspect_runtime.py
```
Observe:
- Operating system and architecture.
- Python implementation (e.g. `CPython`) and exact version.
- Native C compiler version (e.g. `gcc`).

### 2. AST Inspection (L05-01 & L05-02)
Examine how Python represents code structurally:
- Notice that `def add(a, b): return a + b` becomes a `FunctionDef` containing a `Return` with a `BinOp` (`Add`).
- Notice that `(a + b) * c` has `Mult` at the tree root and `Add` in the left child node, proving that parsing resolves operator precedence into tree depth.

### 3. Bytecode Disassembly (L05-01)
Inspect the generated CPython bytecode:
- Notice instructions for loading arguments, performing a binary operation, and returning.
- **Important:** Exact opcodes are implementation details of your specific Python version (e.g., Python 3.13 introduces superinstructions like `LOAD_FAST_LOAD_FAST`, whereas Python 3.11/3.12 uses `LOAD_FAST`, and Python 3.10 uses `BINARY_ADD` instead of `BINARY_OP`).
- Bytecode is **not** CPU machine code; it is interpreted by CPython's software evaluation loop.

### 4. Syntax Error Check (L05-02)
Attempt to parse broken source syntax:
- Notice that `SyntaxError` is raised at parse time before any bytecode is executed.

### 5. Type Checking Comparison (L05-03)
- **Dynamic typing (Python):** Evaluating `"5" + 1` raises a runtime `TypeError` when the addition operation is dispatched.
- **Static typing (C):** Compiling `type_check.c` with GCC produces a compiler diagnostic warning or error before execution. With `-Werror`, the build halts without generating an executable.

---

## Running Verification Tests

Run the automated test suite:
```bash
python -m unittest -v test_activity.py
```

---

## Resetting the Environment

To clean up any compiled artifacts (`.o`, `__pycache__`):
```bash
python reset.py
```
