import unittest
import numpy as np
from frypto.trend_features import TrendFeatures

class TestTrendFeatures(unittest.TestCase):
    """
    Setup common arrays for use in the test cases.
    """
    def setUp(self) -> None:
        self.close = np.array([10, 12, 13, 11, 14])
        self.high = np.array([11, 13, 14, 12, 15])
        self.low = np.array([9, 11, 12, 10, 13])
    
    def test_valid_input(self) -> None:
        """
        Test the TrendFeatures class with valid input arrays
        """
        TF = TrendFeatures(self.close, self.high, self.low)
        df = TF.compute(window=3)
        columns = df.columns
        expected_columns = ['+DI', '-DI', 'ADX', 'support_line', 'resistance_line', 'tenkan_sen',
       'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']
        # Verify the DataFrame contain the correct columns.
        for col in expected_columns:
            self.assertIn(col, columns)
        

    def test_empty_input(self) -> None:
        """
        Test the TrendFeatures class with empty input array.
        """
        with self.assertRaises(ValueError):
            TrendFeatures(np.array([]), np.array([]), np.array([]))

    def test_greater_window(self) -> None:
        """
        Test the TrendFeatures class with a window larger than the input array.
        """
        arr = np.arange(10)
        with self.assertRaises(ValueError):
            TrendFeatures(arr, arr, arr).compute(window=15)

if __name__ == "__main__":
    unittest.main()
