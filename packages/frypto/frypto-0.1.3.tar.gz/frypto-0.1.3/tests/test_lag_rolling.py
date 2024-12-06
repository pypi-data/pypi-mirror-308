import unittest
import numpy as np
from frypto.lag_rolling import LagRollingFeatures

class TestLagRollingFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup common arrays for use in the test cases.
        """
        self.close = np.array([100, 101, 102, 103, 104])

    def test_valid_input(self) -> None:
        """
        Test the LagRollingFeatures class with valid input arrays.
        """
        pf = LagRollingFeatures(self.close)
        df = pf.compute(lags=[1, 2], windows=[3])
        columns = df.columns
        expected_columns = ['lag_1', 'lag_2', 'rolling_mean_3', 'rolling_max_3', 'rolling_min_3']
        
        # Verify the DataFrame contain the correct columns.
        for col in expected_columns:
            self.assertIn(col, columns)

        # Verify the content of the dataframe
        np.testing.assert_array_almost_equal(df.lag_1, [np.nan, 100.0, 101.0, 102.0, 103.0])
        np.testing.assert_array_almost_equal(df.lag_2, [np.nan, np.nan, 100.0, 101.0, 102.0])
        np.testing.assert_array_almost_equal(df.rolling_mean_3, [np.nan, np.nan, 101.0, 102.0, 103.0])
        np.testing.assert_array_almost_equal(df.rolling_max_3, [np.nan, np.nan, 102.0, 103.0, 104.0])
        np.testing.assert_array_almost_equal(df.rolling_min_3, [np.nan, np.nan, 100.0, 101.0, 102.0])

    def test_invalid_input(self) -> None:
        """
        Test the LagRollingFeatures class with invalid input arrays of different lengths.
        """
        with self.assertRaises(ValueError):
            LagRollingFeatures(np.array([1, 2, 3])).compute(lags=[1, 2, 3, 4, 5])

    def test_empty_input(self) -> None:
        """
        Test the LagRollingFeatures class with empty input arrays.
        """
        with self.assertRaises(ValueError):
            LagRollingFeatures(np.array([]))

if __name__ == '__main__':
    unittest.main()