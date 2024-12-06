import pandas as pd
import numpy as np
from typing import Dict
from frypto.price import PriceFeatures
from frypto.volume import VolumeFeatures
from frypto.volatility import VolatilityFeatures
from frypto.momentum import MomentumFeatures
from frypto.lag_rolling import LagRollingFeatures
from frypto.statistical_features import StatisticalFeatures
from frypto.trend_features import TrendFeatures

class AllFeatures:
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize the AllFeatures class by extracting necessary columns from the DataFrame.

        Parameters
        ----------
        df: pd.DataFrame
            A DataFrame containing time series data with columns such as 'close', 'open', 'high', 'low', 'volume'.
        """
        if len(df) < 20:
            raise ValueError("Data Frame can't have less than 20 row.")

        # Check if columns are MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        columns = {col.lower(): col for col in df.columns}

        self.close = self.extract_feature(df, columns, 'close')
        self.open_ = self.extract_feature(df, columns, 'open')
        self.volume = self.extract_feature(df, columns, 'volume')
        self.high = self.extract_feature(df, columns, 'high')
        self.low = self.extract_feature(df, columns, 'low')

    def extract_feature(self, df: pd.DataFrame, columns: Dict, feature: str) -> np.ndarray:
        """
        Extract a specific feature column from the DataFrame if available.

        Parameters
        ----------
        df: pd.DataFrame
            The input DataFrame.
        columns: dict
            A dictionary mapping lower-cased column names to the original DataFrame columns.
        feature: str
            The feature name to extract (e.g., 'close', 'volume').

        Returns
        -------
        np.ndarray
            The extracted feature as a numpy array, or an empty array if the feature is missing.
        """
        if feature in columns:
            return df[columns[feature]].values.astype(np.float32)
        else:
            print(f"Warning: {feature.capitalize()} feature not found in the DataFrame.")
            return np.array([])

    def compute(self, price_window: int = 20, volatility_window: int = 15) -> pd.DataFrame:
        """
        Compute all essential features, including price change, volatility, momentum, volume, and more.

        Parameters
        ----------
        price_window: int, optional
            Window size for computing price-based features (default is 20).
        volatility_window: int, optional
            Window size for computing volatility features (default is 15).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing features from different modules, including price, volatility, momentum,
            statistical, and volume features.
        """
        # Initialize an empty DataFrame to hold results
        df = pd.DataFrame()

        # Compute Price features
        if len(self.close) > 0 and len(self.high) > 0 and len(self.low) > 0 and len(self.open_) > 0:
            pf = PriceFeatures(self.close, self.high, self.low, self.open_)
            df_price = pf.compute()
            df = pd.concat([df, df_price], axis=1)
        else:
            print("Warning: Price features could not be computed due to missing data.")

        # Compute Volatility features
        if len(self.close) > 0 and len(self.high) > 0 and len(self.low) > 0:
            vf = VolatilityFeatures(self.close, self.high, self.low)
            df_volatility = vf.compute(window=volatility_window)
            df = pd.concat([df, df_volatility], axis=1)
        else:
            print("Warning: Volatility features could not be computed due to missing data.")

        # Compute Momentum features
        if len(self.close) > 0:
            mf = MomentumFeatures(self.close)
            df_momentum = mf.compute(window=price_window)
            df = pd.concat([df, df_momentum], axis=1)
        else:
            print("Warning: Momentum features could not be computed due to missing data.")

        # Compute Statistical features
        if len(self.close) > 0:
            sf = StatisticalFeatures(self.close)
            df_stats = sf.compute(window=price_window)
            df = pd.concat([df, df_stats], axis=1)
        else:
            print("Warning: Statistical features could not be computed due to missing data.")

        # Compute Volume features if volume data is available
        if len(self.volume) > 0:
            volf = VolumeFeatures(self.close, self.volume)
            df_volume = volf.compute()
            df = pd.concat([df, df_volume], axis=1)
        else:
            print("Warning: Volume features could not be computed due to missing data.")

        # Compute Lag Rolling features
        if len(self.close) > 0:
            lf = LagRollingFeatures(self.close)
            df_lagrolling = lf.compute()
            df = pd.concat([df, df_lagrolling], axis=1)
        else:
            print("Warning: Lag Rolling features could not be computed due to missing data.")

        # Compute Trend features
        if len(self.close) > 0 and len(self.high) > 0 and len(self.low) > 0:
            tf = TrendFeatures(self.close, self.high, self.low)
            df_trend = tf.compute()
            df = pd.concat([df, df_trend], axis=1)
        else:
            print("Warning: Trend features could not be computed due to missing data.")

        return df

if __name__ == "__main__":
    np.random.seed(42)
    data = pd.DataFrame({
        'close': np.random.randint(1, 300, 50),
        'open': np.random.randint(1, 300, 50),
        'high': np.random.randint(1, 300, 50),
        'low': np.random.randint(1, 300, 50),
        'volume': np.random.randint(1, 300, 50)})
    df = AllFeatures(data).compute()
    columns = df.columns