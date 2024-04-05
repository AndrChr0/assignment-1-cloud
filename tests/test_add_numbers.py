import unittest
from add_numbers.add_numbers import add_two_numbers

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_two_numbers(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add_two_numbers(-1, -1), -2)

    def test_add_floats(self):
        self.assertAlmostEqual(add_two_numbers(2.5, 3.1), 5.6)

    def test_add_zero(self):
        self.assertEqual(add_two_numbers(0, 0), 0)

    def test_add_positive_and_negative_numbers(self):
        self.assertEqual(add_two_numbers(2, -3), -1)
    
    def test_add_negative_and_positive_numbers(self):
        self.assertEqual(add_two_numbers(-2, 3), 1)


if __name__ == '__main__':
    unittest.main()