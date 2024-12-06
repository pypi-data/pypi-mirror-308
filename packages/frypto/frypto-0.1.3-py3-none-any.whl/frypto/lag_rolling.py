import numpy as np
import pandas as pd
from typing import List, Optional

class LagRollingFeatures:
    """
    A class for computing lagged values and rolling window statistics 
    for financial time series data (e.g., closing prices).

    Parameters
    ----------
    close : np.ndarray
        A 1D numpy array of closing prices or similar time series data.

    Methods
    -------
    compute(lags: List[int] = None, windows: List[int] = None) -> pd.DataFrame
        Computes lagged values and rolling window statistics (mean, max, min) 
        for the specified lags and windows.
    """

    def __init__(self, close: np.ndarray) -> None:
        """
        Initialize the LagRollingFeatures class with closing price data.

        Parameters
        ----------
        close : np.ndarray
            A 1D numpy array of closing prices.

        Raises
        ------
        ValueError
            If the input array is empty.
        """
        if len(close) == 0:
            raise ValueError("Close array can't be empty.")
        self.close = np.array(close).astype(np.float32)

    def compute(self, lags: Optional[List[int]] = None, windows: Optional[List[int]] = None) -> pd.DataFrame:
        """
        Compute lagged values and rolling window statistics for the provided lags and window sizes.

        Parameters
        ----------
        lags : List[int], optional
            A list of integers representing the lag periods to compute (default is [1, 2, 3]).
        windows : List[int], optional
            A list of integers representing the window sizes for rolling calculations 
            (default is [5, 10, 20]).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing lagged values and rolling window statistics (mean, max, min) 
            for the specified lags and windows.

        Examples
        --------
        >>> close_np = np.array([100, 101, 102, 103, 104])
        >>> LRF = LagRollingFeatures(close_np)
        >>> result = LRF.compute(lags=[1, 2], windows=[3])
        >>> print(result)

           lag_1   lag_2  rolling_mean_3  rolling_max_3  rolling_min_3
        0    NaN     NaN             NaN            NaN            NaN
        1  100.0     NaN             NaN            NaN            NaN
        2  101.0   100.0      101.000000     102.000000     100.000000
        3  102.0   101.0      102.000000     103.000000     101.000000
        4  103.0   102.0      103.000000     104.000000     102.000000
        """
        if lags is None:
            lags = [1, 2, 3]
        if windows is None:
            windows = [5, 10, 20]

        # Initialize the output DataFrame
        df = pd.DataFrame(index=np.arange(len(self.close)))

        # Lagged features
        for lag in lags:
            lagged_values = np.roll(self.close, lag)
            lagged_values[:lag] = np.nan  # Set the first `lag` values to NaN
            df[f'lag_{lag}'] = lagged_values

        # Rolling window statistics
        for window in windows:
            if len(self.close) < window:
                raise ValueError(f"Window size {window} is larger than the length of the input data ({len(self.close)}).")

            # Rolling mean, max, min
            rolling_mean = np.mean(np.lib.stride_tricks.sliding_window_view(self.close, window), axis=1)
            rolling_max = np.max(np.lib.stride_tricks.sliding_window_view(self.close, window), axis=1)
            rolling_min = np.min(np.lib.stride_tricks.sliding_window_view(self.close, window), axis=1)

            # Pad the start with NaNs to maintain the original array length
            df[f'rolling_mean_{window}'] = np.concatenate([[np.nan] * (window - 1), rolling_mean])
            df[f'rolling_max_{window}'] = np.concatenate([[np.nan] * (window - 1), rolling_max])
            df[f'rolling_min_{window}'] = np.concatenate([[np.nan] * (window - 1), rolling_min])

        return df