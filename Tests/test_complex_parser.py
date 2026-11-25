
import unittest

from complex_parser import (
    normalize_expression,
    parse_expression,
    MathSyntaxError,
)


class TestComplexParser(unittest.TestCase):
    def test_power_symbols(self):
        self.assertEqual(
            normalize_expression("z^2"),
            "z**2",
        )
        self.assertEqual(
            normalize_expression("z**2"),
            "z**2",
        )

    def test_implicit_multiplication(self):
        self.assertEqual(
            normalize_expression("2z"),
            "2*z",
        )
        self.assertEqual(
            normalize_expression("3i"),
            "3*i",
        )
        self.assertEqual(
            normalize_expression("2(z+1)"),
            "2*(z+1)",
        )

    def test_function_call(self):
        self.assertEqual(
            normalize_expression("sin(z)"),
            "sin(z)",
        )

    def test_scientific_notation(self):
        self.assertEqual(
            normalize_expression("1e-3+2e-2i"),
            "1e-3+2e-2*i",
        )

    def test_reject_unknown_name(self):
        with self.assertRaises(MathSyntaxError):
            parse_expression("unknown(z)")

    def test_reject_python_code(self):
        with self.assertRaises(MathSyntaxError):
            parse_expression("__import__('os')")


if __name__ == "__main__":
    unittest.main()
