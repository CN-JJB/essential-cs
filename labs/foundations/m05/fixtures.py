"""M05 Fixtures: Source snippets and minimal evaluation fixtures.

Provides small, deterministic Python functions and AST nodes used to explore:
1. Source to bytecode translation (L05-01).
2. AST structure and tree evaluation (L05-02).
3. Runtime dynamic type checking (L05-03).
"""

import ast


def add(a, b):
    """Minimal arithmetic fixture with two local parameters."""
    return a + b


EXPRESSION_PRECEDENCE = "(a + b) * c"

BROKEN_SYNTAX_SOURCE = "def broken(\n"


def dynamic_type_mismatch():
    """Triggers a runtime TypeError when evaluated."""
    return "5" + 1


def evaluate_simple_ast(node, env):
    """Tiny tree evaluator for basic arithmetic ASTs (L05-02 Build step).

    Demonstrates that evaluation operates on structured trees, not raw text.
    Supports: ast.Expression, ast.BinOp (Add, Mult), ast.Constant, ast.Name.
    """
    if isinstance(node, ast.Expression):
        return evaluate_simple_ast(node.body, env)
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise NameError(f"Variable '{node.id}' not found in environment.")
    if isinstance(node, ast.BinOp):
        left_val = evaluate_simple_ast(node.left, env)
        right_val = evaluate_simple_ast(node.right, env)
        if isinstance(node.op, ast.Add):
            return left_val + right_val
        if isinstance(node.op, ast.Mult):
            return left_val * right_val
        raise NotImplementedError(f"Unsupported operator: {type(node.op).__name__}")
    raise NotImplementedError(f"Unsupported AST node: {type(node).__name__}")
