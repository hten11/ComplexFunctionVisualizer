
"""복소수 수학식의 토큰화와 안전한 문법 분석."""

import ast
import re
from dataclasses import dataclass


FUNCTION_NAMES = {"sqrt", "exp", "log", "sin", "cos", "tan"}
CONSTANT_NAMES = {"i", "pi", "e"}
VARIABLE_NAMES = {"z", "x", "y"}
ALLOWED_NAMES = FUNCTION_NAMES | CONSTANT_NAMES | VARIABLE_NAMES

TOKEN_PATTERN = re.compile(
    r"""
    (?P<NUMBER>
        (?:(?:\d+(?:\.\d*)?)|(?:\.\d+))
        (?:[eE][+-]?\d+)?
    )
    |(?P<NAME>[A-Za-z_]\w*)
    |(?P<OP>\*\*|[+\-*/^(),])
    |(?P<SPACE>\s+)
    |(?P<INVALID>.)
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Token:
    kind: str
    value: str


class MathSyntaxError(ValueError):
    """지원하지 않는 수학 문법."""


def tokenize(expression: str) -> list[Token]:
    tokens = []

    for match in TOKEN_PATTERN.finditer(expression):
        kind = match.lastgroup
        if kind is None:
            raise MathSyntaxError("수학식의 토큰을 확인할 수 없어.")

        value = match.group()

        if kind == "SPACE":
            continue

        if kind == "INVALID":
            raise MathSyntaxError(
                f"허용하지 않는 문자: {value}"
            )

        if kind == "NAME" and value not in ALLOWED_NAMES:
            raise MathSyntaxError(
                f"허용하지 않는 이름: {value}"
            )

        tokens.append(Token(kind, value))

    if not tokens:
        raise MathSyntaxError("수학식을 입력해 줘.")

    return tokens


def insert_implicit_multiplication(
    tokens: list[Token],
) -> list[Token]:
    """2z, 3i, 2(z+1), (z+1)(z-1) 등을 처리한다."""
    result = []

    can_end = {"NUMBER", "NAME", ")"}
    can_start = {"NUMBER", "NAME", "("}

    for index, token in enumerate(tokens):
        if result:
            previous = result[-1]

            left_end = (
                previous.kind in {"NUMBER", "NAME"}
                or previous.value == ")"
            )
            right_start = (
                token.kind in {"NUMBER", "NAME"}
                or token.value == "("
            )

            function_call = (
                previous.kind == "NAME"
                and previous.value in FUNCTION_NAMES
                and token.value == "("
            )

            if (
                left_end
                and right_start
                and not function_call
            ):
                result.append(Token("OP", "*"))

        result.append(token)

    return result


def normalize_expression(expression: str) -> str:
    """지원 문법을 Python AST가 읽을 수 있는 형태로 정규화한다."""
    tokens = insert_implicit_multiplication(tokenize(expression))

    parts = []
    for token in tokens:
        if token.kind == "NAME" and token.value == "i":
            parts.append("i")
        elif token.value == "^":
            parts.append("**")
        else:
            parts.append(token.value)

    normalized = "".join(parts)

    try:
        tree = ast.parse(normalized, mode="eval")
    except SyntaxError as exc:
        raise MathSyntaxError(
            "수학식의 문법이 올바르지 않아."
        ) from exc

    validate_ast(tree)
    return normalized


def validate_ast(tree: ast.AST) -> None:
    """허용한 수학 연산만 AST에 존재하는지 확인한다."""
    allowed_nodes = (
        ast.Expression,
        ast.Constant,
        ast.Name,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.UAdd,
        ast.USub,
        ast.Call,
        ast.Load,
    )

    for node in ast.walk(tree):
        if not isinstance(node, allowed_nodes):
            raise MathSyntaxError(
                f"허용하지 않는 문법 요소: "
                f"{type(node).__name__}"
            )

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise MathSyntaxError("숫자 상수만 허용해.")

        if isinstance(node, ast.Name):
            if node.id not in ALLOWED_NAMES:
                raise MathSyntaxError(
                    f"허용하지 않는 이름: {node.id}"
                )

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise MathSyntaxError(
                    "함수 이름을 직접 입력해 줘."
                )
            if node.func.id not in FUNCTION_NAMES:
                raise MathSyntaxError(
                    f"허용하지 않는 함수: {node.func.id}"
                )
            if len(node.args) != 1 or node.keywords:
                raise MathSyntaxError(
                    "함수는 인자 하나만 받을 수 있어."
                )


def parse_expression(expression: str) -> ast.Expression:
    """검증된 수학식을 AST로 반환한다."""
    normalized = normalize_expression(expression)
    return ast.parse(normalized, mode="eval")
