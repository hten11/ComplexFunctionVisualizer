"""Python complex를 이용한 안전한 수치 계산 엔진."""
from __future__ import annotations

import ast
import cmath
import math
from typing import Mapping

from complex_parser import parse_expression

_FUNCTIONS = {
    "sqrt": cmath.sqrt,
    "exp": cmath.exp,
    "log": cmath.log,
    "sin": cmath.sin,
    "cos": cmath.cos,
    "tan": cmath.tan,
}
_CONSTANTS = {"i": 1j, "pi": math.pi, "e": math.e}


class NumericEvaluationError(ValueError):
    """수치 계산을 수행할 수 없을 때 발생."""


def evaluate_numeric(
    expression: str,
    variables: Mapping[str, complex | float | int] | None = None,
) -> complex:
    """수식을 복소수로 계산한다. 변수 x, z를 지정할 수 있다."""
    tree = parse_expression(expression)
    env: dict[str, complex | float | int] = dict(_CONSTANTS)
    if variables:
        for name, value in variables.items():
            if name not in {"x", "z"}:
                raise NumericEvaluationError(f"지원하지 않는 변수: {name}")
            if isinstance(value, bool) or not isinstance(value, (int, float, complex)):
                raise NumericEvaluationError(f"{name}에는 숫자만 넣을 수 있어.")
            env[name] = value

    def visit(node: ast.AST) -> complex | float | int:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise NumericEvaluationError(f"변수 {node.id}의 값이 지정되지 않았어.")
            return env[node.id]
        if isinstance(node, ast.UnaryOp):
            value = visit(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +value
            if isinstance(node.op, ast.USub):
                return -value
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            try:
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
            except (ArithmeticError, ValueError, OverflowError) as exc:
                raise NumericEvaluationError(str(exc)) from exc
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            arg = visit(node.args[0])
            try:
                return _FUNCTIONS[node.func.id](arg)
            except (ArithmeticError, ValueError, OverflowError) as exc:
                raise NumericEvaluationError(str(exc)) from exc
        raise NumericEvaluationError(f"지원하지 않는 표현식 노드: {type(node).__name__}")

    try:
        result = visit(tree)
    except (ArithmeticError, ValueError, OverflowError) as exc:
        if isinstance(exc, NumericEvaluationError):
            raise
        raise NumericEvaluationError(str(exc)) from exc
    return complex(result)


def format_complex(value: complex) -> str:
    """복소수를 읽기 쉬운 i 표기로 변환한다."""
    real, imag = value.real, value.imag
    if imag == 0:
        return f"{real:g}"
    if real == 0:
        return f"{imag:g}i"
    return f"{real:g}{imag:+g}i"


# 호환용 짧은 함수명
calculate = evaluate_numeric
