import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
from frypto.allfeatures import AllFeatures

class TestAllFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup mock data for testing the AllFeatures class.
        """
        # Sample DataFrame similar to what yfinance would return
        self.data = pd.DataFrame({
            'close': np.random.randint(1, 300, 50),
            'open': np.random.randint(1, 300, 50),
            'high': np.random.randint(1, 300, 50),
            'low': np.random.randint(1, 300, 50),
            'volume': np.random.randint(1, 300, 50)
        })

    def test_valid_input(self) -> None:
        """
        Test the AllFeatures class with valid input data.
        """
        df = AllFeatures(self.data).compute()
        columns = df.columns

        # Expected columns categorized by feature type
        expected_columns = {
            'price_features': ['Price_change', 'next_log_return', 'high_low_spread', 'close_open_spread'],
            'volatility_features': ['rolling_std', 'upper_band', 'lower_band', 'ATR'],
            'momentum_features': ['RSI', 'MACD', 'Signal_Line', 'SMA', 'EMA', 'ROC'],
            'statistical_features': ['Skew_20', 'Kurtosis_20', 'ZScore_20'],
            'volume_features': ['volume_change', 'OBV'],
            'lag_rolling_features': ['lag_1', 'lag_2', 'lag_3', 'rolling_mean_5', 'rolling_max_5', 'rolling_min_5',
                                     'rolling_mean_10', 'rolling_max_10', 'rolling_min_10', 'rolling_mean_20', 
                                     'rolling_max_20', 'rolling_min_20'],
            'trend_features': ['+DI', '-DI', 'ADX', 'support_line', 'resistance_line', 
                               'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']
        }

        # Verify that each feature category's columns are present
        for feature_set, cols in expected_columns.items():
            for col in cols:
                self.assertIn(col, columns, f"{col} missing in output for {feature_set}")

    def test_empty_dataframe(self) -> None:
        """
        Test the AllFeatures class with an empty DataFrame to verify handling.
        """
        empty_data = pd.DataFrame()
        with self.assertRaises(ValueError):
            AllFeatures(empty_data).compute()

    def test_incomplete_data(self) -> None:
        """
        Test the AllFeatures class with missing columns, e.g., no volume.
        """
        data_no_volume = self.data.drop(columns=['volume'])
        df = AllFeatures(data_no_volume).compute()

        # Check that volume-related columns are missing
        for col in ['volume_change', 'OBV']:
            self.assertNotIn(col, df.columns, f"{col} should not be in output when volume data is missing.")

    def test_output_shape(self) -> None:
        """
        Verify that the output DataFrame has the same number of rows as the input.
        """
        df = AllFeatures(self.data).compute()
        self.assertEqual(len(df), len(self.data), "Output DataFrame should have the same number of rows as input.")

if __name__ == "__main__":
    unittest.main()
