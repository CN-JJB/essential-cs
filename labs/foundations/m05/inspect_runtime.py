#!/usr/bin/env python3
"""M05 Runtime & Compiler Pipeline Inspector.

Demonstrates:
1. Environment preflight (Python implementation, version, OS, compiler).
2. AST structure analysis (L05-01 & L05-02).
3. Bytecode disassembly with version-sensitive annotations (L05-01).
4. Parse-time syntax error verification (L05-02).
5. Runtime dynamic type checking (L05-03).
6. Static type checking diagnostics with C compiler (L05-03).
"""

import ast
import dis
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from fixtures import (
    BROKEN_SYNTAX_SOURCE,
    EXPRESSION_PRECEDENCE,
    add,
    dynamic_type_mismatch,
    evaluate_simple_ast,
)


def get_environment_info():
    """Captures the exact local environment metadata."""
    info = {
        "os": platform.platform(),
        "architecture": platform.machine(),
        "python_implementation": platform.python_implementation(),
        "python_version": sys.version.split()[0],
        "cpython_build": sys.version,
        "gcc_available": False,
        "gcc_version": "Not available",
    }
    gcc_path = shutil.which("gcc")
    if gcc_path:
        try:
            res = subprocess.run(
                ["gcc", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0:
                info["gcc_available"] = True
                info["gcc_version"] = res.stdout.splitlines()[0].strip()
        except Exception:
            pass
    return info


def inspect_ast():
    """Inspects AST structure for the arithmetic fixture and precedence expression."""
    tree_add = ast.parse(
        "def add(a, b):\n    return a + b\n"
    )
    dump_add = ast.dump(tree_add, indent=2)

    tree_expr = ast.parse(EXPRESSION_PRECEDENCE, mode="eval")
    dump_expr = ast.dump(tree_expr, indent=2)

    return {
        "tree_add": tree_add,
        "dump_add": dump_add,
        "tree_expr": tree_expr,
        "dump_expr": dump_expr,
    }


def inspect_bytecode():
    """Inspects CPython bytecode for the `add` function.

    Identifies operations by semantic class rather than brittle exact offsets.
    The activity's bytecode contract is CPython-specific.
    """
    if platform.python_implementation() != "CPython":
        return {
            "supported": False,
            "reason": "CPython is required for this bytecode inspection activity",
            "instructions": [],
            "opnames": [],
            "has_load_args": False,
            "has_binary_op": False,
            "has_return": False,
        }

    instructions = list(dis.get_instructions(add))
    opnames = [instr.opname for instr in instructions]

    # Check for argument loading operations (e.g. LOAD_FAST or Python 3.13 superinstruction LOAD_FAST_LOAD_FAST)
    has_load_args = any("LOAD_FAST" in name for name in opnames)

    # Check for binary operation (e.g. BINARY_OP in 3.11+, or BINARY_ADD in 3.10 and earlier)
    has_binary_op = any("BINARY" in name for name in opnames)

    # Check for return operation
    has_return = any("RETURN" in name for name in opnames)

    return {
        "supported": True,
        "reason": "",
        "instructions": instructions,
        "opnames": opnames,
        "has_load_args": has_load_args,
        "has_binary_op": has_binary_op,
        "has_return": has_return,
    }


def verify_syntax_error():
    """Verifies that syntax errors are caught at parse time before execution."""
    caught = False
    error_msg = ""
    try:
        ast.parse(BROKEN_SYNTAX_SOURCE)
    except SyntaxError as e:
        caught = True
        error_msg = str(e)
    return caught, error_msg


def verify_dynamic_type_error():
    """Verifies that dynamic type mismatches raise TypeError at runtime."""
    caught = False
    error_msg = ""
    try:
        dynamic_type_mismatch()
    except TypeError as e:
        caught = True
        error_msg = str(e)
    return caught, error_msg


def verify_static_compiler_diagnostic(script_dir=None):
    """Verifies static type diagnostic behavior in C using GCC if available."""
    if not shutil.which("gcc"):
        return {
            "tested": False,
            "reason": "gcc not found in PATH",
        }

    if script_dir is None:
        script_dir = Path(__file__).parent

    c_file = script_dir / "type_check.c"
    obj_file = script_dir / "type_check.o"

    results = {"tested": True}

    try:
        # Test default/strict compilation
        res_default = subprocess.run(
            ["gcc", "-c", str(c_file), "-o", str(obj_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        results["default_exit"] = res_default.returncode
        results["default_stderr"] = res_default.stderr

        # Test with -fpermissive (shows it as a warning on GCC 14)
        res_permissive = subprocess.run(
            ["gcc", "-c", "-fpermissive", str(c_file), "-o", str(obj_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        results["permissive_exit"] = res_permissive.returncode
        results["permissive_stderr"] = res_permissive.stderr

        # Test with -Werror (promotes warning to error)
        res_werror = subprocess.run(
            ["gcc", "-c", "-Werror", str(c_file), "-o", str(obj_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        results["werror_exit"] = res_werror.returncode
        results["werror_stderr"] = res_werror.stderr

    finally:
        if obj_file.exists():
            obj_file.unlink()

    return results


def run_all_inspections():
    """Runs all inspections and prints formatted summary."""
    env = get_environment_info()
    print("=== M05 Runtime & Compiler Pipeline Preflight ===")
    print(f"OS: {env['os']}")
    print(f"Arch: {env['architecture']}")
    print(f"Python Implementation: {env['python_implementation']} {env['python_version']}")
    print(f"Compiler: {env['gcc_version']}")
    print()

    print("=== 1. AST Inspection (L05-01 & L05-02) ===")
    ast_res = inspect_ast()
    print("AST for def add(a, b): return a + b:")
    print(ast_res["dump_add"])
    print("\nAST for '(a + b) * c' (Precedence structure):")
    print(ast_res["dump_expr"])
    print()

    print("=== 2. CPython Bytecode Inspection (L05-01) ===")
    bc_res = inspect_bytecode()
    if bc_res["supported"]:
        print(f"Observed opcodes ({env['python_implementation']} {env['python_version']}):")
        for instr in bc_res["instructions"]:
            print(f"  {instr.opname:<22} arg={instr.argval}")
    else:
        print(f"Bytecode inspection skipped: {bc_res['reason']}")
    print()

    print("=== 3. Syntax Error Verification (L05-02) ===")
    syn_ok, syn_msg = verify_syntax_error()
    print(f"Syntax error caught at parse time? {syn_ok} ({syn_msg})")
    print()

    print("=== 4. Dynamic Type Error Verification (L05-03) ===")
    dyn_ok, dyn_msg = verify_dynamic_type_error()
    print(f"Runtime TypeError raised on '5' + 1? {dyn_ok} ({dyn_msg})")
    print()

    print("=== 5. Static Compiler Diagnostic Verification (L05-03) ===")
    static_res = verify_static_compiler_diagnostic()
    if static_res["tested"]:
        print("GCC static type checking:")
        print(f"  Default flags exit code: {static_res['default_exit']}")
        print(f"  With -fpermissive exit code: {static_res['permissive_exit']}")
        print(f"  With -Werror exit code: {static_res['werror_exit']}")
        print("  Diagnostic snippet:", static_res['default_stderr'].splitlines()[0] if static_res['default_stderr'] else "")
    else:
        print(f"  Skipped: {static_res['reason']}")
    print()

    print("=== 6. Tiny AST Tree Evaluator (L05-02 Build Step) ===")
    test_env = {"a": 2, "b": 3, "c": 4}
    res_val = evaluate_simple_ast(ast_res["tree_expr"], test_env)
    print(f"Evaluated '(a + b) * c' with {test_env} -> {res_val} (expected: 20)")
    print()


if __name__ == "__main__":
    run_all_inspections()
