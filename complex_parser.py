
import math


class ComplexParseError(ValueError):
    """복소수 입력 해석 중 발생하는 오류."""
    pass


def parse_complex(value: str) -> complex:
    """
    복소수 문자열을 Python complex 객체로 변환한다.

    지원 예시:
        "2+3i"
        "1-4j"
        "3"
        "i"
        "-i"
        "2i"
        "-2.5+0.3i"
    """

    if not isinstance(value, str):
        raise ComplexParseError("입력값은 문자열이어야 합니다.")

    # 공백 제거 및 소문자 변환
    text = value.strip().lower().replace(" ", "")

    if not text:
        raise ComplexParseError("복소수를 입력해야 합니다.")

    # i와 j를 동시에 사용하는 입력은 허용하지 않는다.
    if "i" in text and "j" in text:
        raise ComplexParseError("i와 j를 동시에 사용할 수 없습니다.")

    # 사용자가 쓰는 i를 Python이 사용하는 j로 변환
    text = text.replace("i", "j")

    # Python에서 지원하지 않는 단독 허수 표현 보정
    if text == "j" or text == "+j":
        text = "1j"
    elif text == "-j":
        text = "-1j"

    # 복소수 변환
    try:
        result = complex(text)
    except ValueError:
        raise ComplexParseError(
            f"올바르지 않은 복소수 입력입니다: {value}"
        )

    # 무한대와 NaN 방지
    if not math.isfinite(result.real) or not math.isfinite(result.imag):
        raise ComplexParseError("무한대 또는 NaN은 입력할 수 없습니다.")

    return result
