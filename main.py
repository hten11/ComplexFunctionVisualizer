
"""복소수 기초 계산기 실행 파일."""

import math
import sympy as sp
from complex_parser import MathSyntaxError
from numeric_engine import calculate, format_complex
from symbolic_engine import calculate_symbolic, sp


def read_complex_component(prompt: str) -> float:
    text = input(prompt).strip()

    if not text:
        return 0.0

    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(
            "실수부와 허수부에는 유한한 실수만 입력해 줘."
        ) from exc


def read_complex() -> complex:
    real = read_complex_component("실수부: ")
    imag = read_complex_component("허수부: ")

    value = complex(real, imag)

    if not (
        __import__("math").isfinite(real)
        and __import__("math").isfinite(imag)
    ):
        raise ValueError("무한대와 NaN은 입력할 수 없어.")

    return value


def main() -> None:
    print("복소수 기초 계산기")
    print("모드: numeric / symbolic")
    print("종료하려면 quit을 입력해.")
    print("예시: 3+4i, z^2+1, sqrt(2), sin(pi/2)")

    while True:
        mode = input("\n계산 모드: ").strip().lower()

        if mode == "quit":
            break

        if mode not in {"numeric", "symbolic"}:
            print("numeric 또는 symbolic을 입력해 줘.")
            continue

        expression = input("수학식: ").strip()

        if expression.lower() == "quit":
            break

        try:
            if mode == "symbolic":
                result = calculate_symbolic(expression)
                print("기호 결과:", result)
                print("간소화:", sp.simplify(result))

            else:
                # 식에 z가 포함되면 복소수 값을 입력받는다.
                variables = {}
                if "z" in expression:
                    variables["z"] = read_complex()

                result = calculate(expression, variables)
                print("수치 결과:", format_complex(result))

        except (
            MathSyntaxError,
            ValueError,
            ArithmeticError,
        ) as exc:
            print("오류:", exc)


if __name__ == "__main__":
    main()
