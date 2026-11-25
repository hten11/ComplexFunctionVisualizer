
from complex_parser import parse_complex, ComplexParseError


def main():
    print("=== 복소수 입력 테스트 프로그램 ===")
    print("종료하려면 q를 입력하세요.")

    while True:
        user_input = input("\n복소수 입력: ")

        if user_input.strip().lower() == "q":
            print("프로그램을 종료합니다.")
            break

        try:
            z = parse_complex(user_input)

            print(f"변환 결과: {z}")
            print(f"실수부: {z.real}")
            print(f"허수부: {z.imag}")

        except ComplexParseError as error:
            print(f"입력 오류: {error}")


if __name__ == "__main__":
    main()
