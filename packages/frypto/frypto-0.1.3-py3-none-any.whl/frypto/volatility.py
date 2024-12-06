import numpy as np
import pandas as pd
from frypto.helpers import _pad_nan
class VolatilityFeatures:
    """
    A class for computing rolling volatility features based on financial time series data,
    including rolling standard deviation, Bollinger Bands, and Average True Range (ATR).

    Parameters
    ----------
    close: np.ndarray    
        A 1D numpy array of closing prices.

    high : np.ndarray
        A 1D numpy array of high prices.

    low : np.ndarray
        A 1D numpy array of low prices.
    
    Raises
    ------
    ValueError
        If the input arrays (`close`, `high`, `low`) do not have the same length.
    
    Methods
    -------
    compute(window=15)
        Computes rolling volatility features over the specified window size and returns a DataFrame.

    """
    def __init__(self, close: np.ndarray, high: np.ndarray, low: np.ndarray) -> None:
        if not(len(close) == len(high) == len(low) > 0):
            raise ValueError("Input arrays must be of the same length and non-empty.")
        self.close = close
        self.high = high
        self.low = low

    

    def compute(self, window: int = 15) -> pd.DataFrame:
        """
        Compute rolling volatility features, including rolling standard deviation, Bollinger Bands,
        and Average True Range (ATR), for the given window size.

        Parameters
        ----------
        window : int, optional
            Size of the rolling window to compute features. Defaults to 15.
            The window size must be smaller than the length of the array.

        Returns
        -------
        pd.DataFrame
            A DataFrame with computed volatility features:
            - rolling_std: Rolling standard deviation of the `close` over the window.
            - upper_band: Upper Bollinger band (mean + 2*std).
            - lower_band: Lower Bollinger band (mean - 2*std).
            - ATR: Average True Range, calculated using the high, low, and close prices.

        Examples
        --------
        >>> close = np.arange(1, 20)
        >>> high = np.arange(1, 20)
        >>> low = np.arange(1, 20)
        >>> features = VolatilityFeatures(close, high, low)
        >>> features.compute(window=2)
           rolling_std  upper_band  lower_band  ATR
        0          NaN         NaN         NaN  NaN
        1          0.5         2.5         0.5  0.0
        2          0.5         3.5         1.5  0.0
        3          0.5         4.5         2.5  0.0
        4          0.5         5.5         3.5  0.0
        ...
        """
        if len(self.close) < window:
            raise ValueError("Window size must be smaller than the length of the input arrays.")
        
        df = pd.DataFrame()

        # Rolling statistics for close price
        window_view = np.lib.stride_tricks.sliding_window_view(self.close, window)
        rolling_std = np.std(window_view, axis=1)
        rolling_mean = np.mean(window_view, axis=1)

        df['rolling_std'] = _pad_nan(rolling_std, window)
        df['upper_band'] = _pad_nan(rolling_mean + 2 * rolling_std, window)
        df['lower_band'] = _pad_nan(rolling_mean - 2 * rolling_std, window)

        # ATR (Average True Range)
        true_range = np.maximum(self.high[1:] - self.low[1:], 
                        np.maximum(np.abs(self.high[1:] - self.close[:-1]),
                                   np.abs(self.low[1:] - self.close[:-1])))
        true_range = np.insert(true_range, 0, 0)  # Insert a 0 for the first true range
        atr = pd.Series(true_range).rolling(window).mean().values
        df['ATR'] = _pad_nan(atr[window-1:], window)

        return df