
import unittest

from complex_parser import parse_complex, ComplexParseError


class TestComplexParser(unittest.TestCase):

    def test_normal_complex(self):
        self.assertEqual(parse_complex("2+3i"), 2 + 3j)
        self.assertEqual(parse_complex("1-4j"), 1 - 4j)

    def test_real_number(self):
        self.assertEqual(parse_complex("3"), 3 + 0j)

    def test_imaginary_number(self):
        self.assertEqual(parse_complex("i"), 1j)
        self.assertEqual(parse_complex("-i"), -1j)
        self.assertEqual(parse_complex("2i"), 2j)

    def test_decimal(self):
        self.assertEqual(
            parse_complex("-2.5+0.3i"),
            -2.5 + 0.3j
        )

    def test_spaces(self):
        self.assertEqual(parse_complex(" 2 + 3i "), 2 + 3j)

    def test_invalid_input(self):
        invalid_inputs = [
            "",
            "hello",
            "2++3i",
            "2+i+3j",
            "nan",
            "inf"
        ]

        for value in invalid_inputs:
            with self.subTest(value=value):
                with self.assertRaises(ComplexParseError):
                    parse_complex(value)


if __name__ == "__main__":
    unittest.main()
