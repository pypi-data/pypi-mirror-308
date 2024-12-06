import unittest
import numpy as np
from frypto.statistical_features import StatisticalFeatures

class TestStatisticalFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup common arrays for use in the test case.
        """
        self.close = np.array([90, 91, 102, 103, 21])

    def test_valid_input(self) -> None:
        """
        Test the StatisticalFeatures class with valid input arrays.
        """
        SF = StatisticalFeatures(self.close)
        df = SF.compute(window=4)
        columns = df.columns
        expected_columns = ['Skew_4', 'Kurtosis_4', 'ZScore_4']

        # Verfy the DataFrame contain the correct columns.
        for col in columns:
            self.assertIn(col, columns)
        
        # Verify the content of the DataFrame
        np.testing.assert_array_almost_equal(df.Skew_4, [np.nan, np.nan, np.nan, 0.0, -1.8891759251356406])
        np.testing.assert_array_almost_equal(df.Kurtosis_4, [np.nan, np.nan, np.nan, -5.7945303210463734, 3.58564420103653])
        np.testing.assert_array_almost_equal(df.ZScore_4, [np.nan, np.nan, np.nan, 1.0795912446866822, -1.7153232284664415])
    
    def test_empty_input(self) -> None:
        """
        Test the StatisticalFeatures class with empty input array.
        """
        with self.assertRaises(ValueError):
            StatisticalFeatures(np.array([]))

    def test_greater_window(self) -> None:
        """
        Test the StatisticalFeatures class with a window larger than the input array.
        """
        with self.assertRaises(ValueError):
            StatisticalFeatures(np.arange(10)).compute(window=20)
        
if __name__ == "__main__":
    unittest.main()