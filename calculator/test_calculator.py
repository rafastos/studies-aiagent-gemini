# test_calculator.py
import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):
    def test_expression(self):
        calculator = Calculator()
        result = calculator.evaluate("3 + 7 * 2")
        self.assertEqual(result, 17)

if __name__ == '__main__':
    unittest.main()