import unittest

import sympy as sp

from complex_parser import ExpressionSyntaxError, parse_expression # type: ignore
from numeric_engine import NumericEvaluationError, evaluate_numeric
from symbolic_engine import evaluate_symbolic, substitute


class TestComplexParser(unittest.TestCase):
    def test_power_operator(self):
        self.assertEqual(evaluate_numeric("2^3"), 8 + 0j)
        self.assertEqual(evaluate_numeric("2**3"), 8 + 0j)

    def test_implicit_multiplication(self):
        self.assertEqual(evaluate_numeric("2i"), 2j)
        self.assertEqual(evaluate_numeric("2(3+1)"), 8 + 0j)
        self.assertEqual(evaluate_numeric("(x+1)(x-1)", {"x": 3}), 8 + 0j)

    def test_complex_functions(self):
        self.assertAlmostEqual(evaluate_numeric("sin(pi/2)").real, 1.0)
        self.assertAlmostEqual(evaluate_numeric("sqrt(-1)").imag, 1.0)

    def test_unknown_name_rejected(self):
        with self.assertRaises(ExpressionSyntaxError):
            parse_expression("__import__('os')")

    def test_missing_variable(self):
        with self.assertRaises(NumericEvaluationError):
            evaluate_numeric("x+1")


class TestSymbolicEngine(unittest.TestCase):
    def test_exact_arithmetic(self):
        self.assertEqual(evaluate_symbolic("1/3 + 1/6"), sp.Rational(1, 2))

    def test_symbolic_simplification(self):
        expected = sp.Add(sp.Pow(sp.Symbol("x"), 2), sp.Integer(-1))
        self.assertEqual(evaluate_symbolic("(x+1)(x-1)"), expected)

    def test_substitution(self):
        self.assertEqual(substitute("x^2+1", x=3), 10)

    def test_constants_and_functions(self):
        self.assertEqual(evaluate_symbolic("sqrt(-1)"), sp.I)
        self.assertEqual(evaluate_symbolic("sin(pi/2)"), sp.Integer(1))


if __name__ == "__main__":
    unittest.main()
