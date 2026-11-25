
import unittest

from numeric_engine import calculate, format_complex


class TestNumericEngine(unittest.TestCase):
    def test_complex_square(self):
        result = calculate("(1+2i)^2")
        self.assertAlmostEqual(result.real, -3)
        self.assertAlmostEqual(result.imag, 4)

    def test_implicit_multiplication(self):
        self.assertEqual(calculate("3i"), 3j)

    def test_fraction(self):
        self.assertAlmostEqual(
            calculate("1/3").real,
            1 / 3,
        )

    def test_variable(self):
        result = calculate("z^2+1", {"z": 1+2j})
        self.assertAlmostEqual(result.real, -2)
        self.assertAlmostEqual(result.imag, 4)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            calculate("1/0")

    def test_format_complex(self):
        self.assertEqual(format_complex(3+4j), "3+4i")
        self.assertEqual(format_complex(3-4j), "3-4i")
        self.assertEqual(format_complex(3+0j), "3")


if __name__ == "__main__":
    unittest.main()
