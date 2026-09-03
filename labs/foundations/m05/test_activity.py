"""Unit tests for M05 Runtime & Compiler Pipeline Activity.

Verifies:
1. Environment preflight capability detection.
2. AST structural and precedence relationships.
3. Bytecode semantic relationships without brittle offset or numeric opcode pinning.
4. Syntax error detection at parse time.
5. Dynamic type checking behavior in Python runtime.
6. Tiny AST evaluator correctness.
7. Static compiler diagnostic verification with C/GCC (when available).
"""

import ast
import dis
import shutil
import unittest
from pathlib import Path

from fixtures import (
    BROKEN_SYNTAX_SOURCE,
    EXPRESSION_PRECEDENCE,
    add,
    dynamic_type_mismatch,
    evaluate_simple_ast,
)
from inspect_runtime import (
    get_environment_info,
    inspect_ast,
    inspect_bytecode,
    verify_dynamic_type_error,
    verify_static_compiler_diagnostic,
    verify_syntax_error,
)


class EnvironmentPreflightTests(unittest.TestCase):
    """Verifies that the execution environment is properly recorded."""

    def test_environment_fields(self):
        info = get_environment_info()
        self.assertIn("os", info)
        self.assertIn("architecture", info)
        self.assertIn("python_implementation", info)
        self.assertIn("python_version", info)
        self.assertTrue(len(info["python_version"]) > 0)


class ASTStructureTests(unittest.TestCase):
    """Verifies AST parsing and precedence hierarchy (L05-01 & L05-02)."""

    def test_add_ast_structure(self):
        tree = ast.parse("def add(a, b):\n    return a + b\n")
        self.assertIsInstance(tree, ast.Module)
        func = tree.body[0]
        self.assertIsInstance(func, ast.FunctionDef)
        self.assertEqual(func.name, "add")
        ret = func.body[0]
        self.assertIsInstance(ret, ast.Return)
        self.assertIsInstance(ret.value, ast.BinOp)
        self.assertIsInstance(ret.value.op, ast.Add)

    def test_expression_precedence_ast(self):
        """(a + b) * c must place Mult at the root and Add in the left subtree."""
        tree = ast.parse(EXPRESSION_PRECEDENCE, mode="eval")
        self.assertIsInstance(tree, ast.Expression)
        root_op = tree.body
        self.assertIsInstance(root_op, ast.BinOp)
        self.assertIsInstance(root_op.op, ast.Mult)

        left_child = root_op.left
        self.assertIsInstance(left_child, ast.BinOp)
        self.assertIsInstance(left_child.op, ast.Add)

        self.assertIsInstance(root_op.right, ast.Name)
        self.assertEqual(root_op.right.id, "c")

    def test_tiny_ast_evaluator(self):
        tree = ast.parse(EXPRESSION_PRECEDENCE, mode="eval")
        env = {"a": 10, "b": 20, "c": 3}
        # (10 + 20) * 3 = 90
        result = evaluate_simple_ast(tree, env)
        self.assertEqual(result, 90)


class BytecodeSemanticRelationTests(unittest.TestCase):
    """Verifies bytecode structural/semantic relations without brittle offsets."""

    def test_bytecode_contains_semantic_operations(self):
        res = inspect_bytecode()
        # Must load arguments (either LOAD_FAST or superinstruction like LOAD_FAST_LOAD_FAST)
        self.assertTrue(
            res["has_load_args"],
            f"Expected argument loading opcode in {res['opnames']}",
        )
        # Must perform binary operation (e.g. BINARY_OP or BINARY_ADD)
        self.assertTrue(
            res["has_binary_op"],
            f"Expected binary operation opcode in {res['opnames']}",
        )
        # Must return value
        self.assertTrue(
            res["has_return"],
            f"Expected return opcode in {res['opnames']}",
        )

    def test_bytecode_does_not_assert_hardcoded_offsets(self):
        """Ensure test inspects instructions dynamically rather than checking fixed offsets."""
        instructions = list(dis.get_instructions(add))
        self.assertTrue(len(instructions) >= 3)
        # Verify the last instruction is a return operation
        self.assertIn("RETURN", instructions[-1].opname)


class LanguageVsRuntimeFailureTests(unittest.TestCase):
    """Verifies the distinction between parse-time syntax errors and runtime type errors."""

    def test_syntax_error_caught_at_parse_time(self):
        caught, msg = verify_syntax_error()
        self.assertTrue(caught)
        self.assertTrue(len(msg) > 0)

    def test_dynamic_type_error_caught_at_runtime(self):
        caught, msg = verify_dynamic_type_error()
        self.assertTrue(caught)
        self.assertIn("str", msg.lower())
        self.assertIn("int", msg.lower())


class StaticCompilerDiagnosticTests(unittest.TestCase):
    """Verifies C static typing diagnostic behavior if GCC is installed."""

    def test_static_diagnostic_if_gcc_present(self):
        if not shutil.which("gcc"):
            self.skipTest("gcc compiler not available in test environment")

        res = verify_static_compiler_diagnostic()
        self.assertTrue(res["tested"])
        # With -Werror, compilation must fail (non-zero exit)
        self.assertNotEqual(res["werror_exit"], 0)
        # Compiler diagnostic stderr should mention pointer/integer conversion
        diagnostic_text = res["default_stderr"] + res["werror_stderr"]
        self.assertTrue(
            "int" in diagnostic_text or "pointer" in diagnostic_text or "conversion" in diagnostic_text,
            f"Unexpected diagnostic text: {diagnostic_text}",
        )


if __name__ == "__main__":
    unittest.main()
