"""SymPy 기반 정확한 기호 계산 엔진."""
from __future__ import annotations

import ast
import sympy as sp

from complex_parser import parse_expression

_FUNCTIONS = {
    "sqrt": sp.sqrt,
    "exp": sp.exp,
    "log": sp.log,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
}
_CONSTANTS = {"i": sp.I, "pi": sp.pi, "e": sp.E}


class SymbolicEvaluationError(ValueError):
    """기호 수식 변환/계산 중 발생한 오류."""


def evaluate_symbolic(expression: str, simplify: bool = True) -> sp.Expr:
    """입력 수식을 SymPy 표현식으로 변환한다."""
    tree = parse_expression(expression)
    variables = {"x": sp.Symbol("x"), "z": sp.Symbol("z")}

    def visit(node: ast.AST) -> sp.Expr:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant):
            # 유한 소수는 부동소수점이 아닌 정확한 유리수로 보존한다.
            if isinstance(node.value, int):
                return sp.Integer(node.value)
            return sp.Rational(str(node.value))
        if isinstance(node, ast.Name):
            if node.id in _CONSTANTS:
                return _CONSTANTS[node.id]
            if node.id in variables:
                return variables[node.id]
            raise SymbolicEvaluationError(f"지원하지 않는 이름: {node.id}")
        if isinstance(node, ast.UnaryOp):
            value = visit(node.operand)
            if isinstance(node.op, ast.UAdd):
                return value
            if isinstance(node.op, ast.USub):
                return -value
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            return _FUNCTIONS[node.func.id](visit(node.args[0]))
        raise SymbolicEvaluationError(f"지원하지 않는 표현식 노드: {type(node).__name__}")

    try:
        result = visit(tree)
        return sp.simplify(result) if simplify else result
    except Exception as exc:
        if isinstance(exc, SymbolicEvaluationError):
            raise
        raise SymbolicEvaluationError(str(exc)) from exc


def substitute(expression: str, **values: complex | float | int) -> sp.Expr:
    """기호식의 x/z 변수에 값을 대입한다."""
    expr = evaluate_symbolic(expression)
    replacements = {}
    for name, value in values.items():
        if name not in {"x", "z"}:
            raise SymbolicEvaluationError(f"지원하지 않는 변수: {name}")
        replacements[sp.Symbol(name)] = value
    return sp.simplify(expr.subs(replacements))


# 호환용 짧은 함수명
calculate_symbolic = evaluate_symbolic
