import unittest
import numpy as np

from frypto.volatility import VolatilityFeatures

class TestVolatilityFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup common arrays for use in the test cases.
        """
        self.close = np.arange(5)
        self.high = np.arange(5)
        self.low = np.arange(5)

    def test_valid_input(self) -> None:
        """
        Test the VolatilityFeatures class with valid input arrays
        """
        VF = VolatilityFeatures(self.close, self.high, self.low)
        df = VF.compute(window=2)
        columns = df.columns
        expected_columns = ['rolling_std', 'upper_band', 'lower_band', 'ATR']

        # Verify the DataFrame contain the correct columns
        for col in expected_columns:
            self.assertIn(col, columns)

        # Verify the content of the DataFrame
        np.testing.assert_array_almost_equal(df.rolling_std, [np.nan, 0.5, 0.5, 0.5, 0.5])
        np.testing.assert_array_almost_equal(df.upper_band, [np.nan, 1.5, 2.5, 3.5, 4.5])
        np.testing.assert_array_almost_equal(df.lower_band, [np.nan, -0.5, 0.5, 1.5, 2.5])
        np.testing.assert_array_almost_equal(df.ATR, [np.nan, 0.5, 1.0, 1.0, 1.0])

    def test_empty_input(self) -> None:
        """
        Test the VolatilityFeatures class with empty input array.
        """
        with self.assertRaises(ValueError):
            VolatilityFeatures(np.array([]), np.array([]), np.array([]),)

    def test_greater_window(self) -> None:
        """
        Test the VolatilityFeatures class with a window larger than the input array.
        """
        arr = np.arange(14)
        with self.assertRaises(ValueError):
            VolatilityFeatures(arr, arr, arr).compute(window=15)

if __name__ == "__main__":
    unittest.main()