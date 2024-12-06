import unittest
import numpy as np
from frypto.price import PriceFeatures

class TestPriceFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup common arrays for use in the test cases.
        """
        self.close = np.array([10, 12, 13, 11, 14])
        self.high = np.array([11, 13, 14, 12, 15])
        self.low = np.array([9, 11, 12, 10, 13])
        self.open = np.array([9, 12, 12, 11, 13])

    def test_valid_input(self) -> None:
        """
        Test the PriceFeatures class with valid input arrays.
        """
        pf = PriceFeatures(self.close, self.high, self.low, self.open)
        df = pf.compute()
        columns = df.columns

        # Verify the DataFrame contains the correct columns
        self.assertIn('Price_change', columns)
        self.assertIn('next_log_return', columns)
        self.assertIn('high_low_spread', columns)
        self.assertIn('close_open_spread', columns)

        # Verify the content of the DataFrame
        expected_price_change = np.array([0, 2, 1, -2, 3])
        np.testing.assert_array_equal(df.Price_change, expected_price_change)

        expected_next_log_return = np.array([np.nan,  0.18232156,  0.08004271, -0.16705408,  0.24116206])
        np.testing.assert_array_almost_equal(df.next_log_return, expected_next_log_return, decimal=6)

        expected_high_low_spread = self.high - self.low
        np.testing.assert_array_equal(df.high_low_spread, expected_high_low_spread)

        expected_close_open_spread = self.close - self.open
        np.testing.assert_array_equal(df.close_open_spread, expected_close_open_spread)

    def test_invalid_input(self) -> None:
        """
        Test the PriceFeatures class with invalid input arrays of different lengths.
        """
        with self.assertRaises(ValueError):
            PriceFeatures(np.array([1, 2]), np.array([1]), np.array([1, 2]), np.array([1, 2]))

    def test_empty_input(self) -> None:
        """
        Test the PriceFeatures class with empty input arrays.
        """
        with self.assertRaises(ValueError):
            PriceFeatures(np.array([]), np.array([]), np.array([]), np.array([]))

if __name__ == '__main__':
    unittest.main()
