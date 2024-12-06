import unittest
import numpy as np
from frypto.momentum import MomentumFeatures

class TestMomentumFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup common arrays for use in the test case.
        """
        self.close = np.array([100, 101, 102, 103, 104])
    
    def test_valid_input(self) -> None:
        """
        Test the MomentumFeatures class with valid input arrays
        """
        VF = MomentumFeatures(self.close)
        df = VF.compute(window=3, rsi_window=2, macd_windows=(3, 6, 2))
        columns = df.columns
        expected_columns = ['RSI', 'MACD', 'Signal_Line', 'SMA', 'EMA', 'ROC']

        # Verify the DataFrame contain the correct columns.
        for col in expected_columns:
            self.assertIn(col, columns)
        
        # Verify the content of the DataFrame
        np.testing.assert_array_almost_equal(df.RSI, [np.nan, np.nan, np.nan, np.nan, np.nan])
        np.testing.assert_array_almost_equal(df.MACD, [0.0, 0.0833282470703125, 0.2083892822265625, 0.3590087890625, 0.5192794799804688])
        np.testing.assert_array_almost_equal(df.Signal_Line, [0.0, 0.062496185302734375, 0.16349910199642181, 0.29546815156936646, 0.44529226422309875])
        np.testing.assert_array_almost_equal(df.SMA, [np.nan, np.nan, 101.0, 102.0, 103.0])
        np.testing.assert_array_almost_equal(df.EMA, [100.0, 100.66666412353516, 101.42857360839844, 102.26667022705078, 103.16129302978516])
        np.testing.assert_array_almost_equal(df.ROC, [-1.9607844352722168, -1.9417475461959839, -1.9230769872665405, 3.0, 2.97029709815979])

    
    def test_empty_input(self) -> None:
        """
        Test the MomentumFeatures class with empty input array.
        """
        with self.assertRaises(ValueError):
            MomentumFeatures(np.array([]))

    def test_greater_window(self) -> None:
        """
        Test the MomentumFeatures class with a window larger than the input array.
        """
        with self.assertRaises(ValueError):
            MomentumFeatures(np.arange(10)).compute(window=15)

if __name__ == "__main__":
    unittest.main()