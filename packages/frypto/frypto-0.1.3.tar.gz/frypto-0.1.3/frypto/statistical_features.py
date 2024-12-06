import numpy as np
import pandas as pd

class StatisticalFeatures:
    """
    A class for computing rolling statistical features based on financial time series data,
    including rolling skewness, kurtosis, and z-scores.

    Parameters
    ----------
    close : np.ndarray
        A 1D numpy array of closing prices.

    Methods
    -------
    compute(window: int = 20) -> pd.DataFrame
        Computes rolling skewness, kurtosis, and z-scores for the given window size.
    """

    def __init__(self, close: np.ndarray) -> None:
        """
        Initialize the StatisticalFeatures class with closing price data.

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

    def compute(self, window: int = 20) -> pd.DataFrame:
        """
        Compute rolling statistical features including skewness, kurtosis, and z-score for the given window size.

        Parameters
        ----------
        window : int, optional
            The window size for the rolling calculations (default is 20).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing rolling skewness, kurtosis, and z-scores for the specified window.

        Examples
        --------
        >>> close_np = np.random.rand(100)
        >>> sf = StatisticalFeatures(close_np)
        >>> result = sf.compute(window=20)
        >>> print(result.tail())

                 Skew_20    kurtosis_20    zscore_20
        95      -0.378413    -0.755383   0.456289
        96      -0.558687    -0.543988   1.236031
        97      -0.672869    -0.011139   0.340689
        98      -0.569832     0.015443  -0.542069
        99      -0.548970    -0.300006  -1.926303
        """

        df = pd.DataFrame()

        rolling_skew = pd.Series(self.close).rolling(window=window).skew().values
        rolling_kurtosis = pd.Series(self.close).rolling(window=window).kurt().values
        df[f'Skew_{window}'] = rolling_skew
        df[f'Kurtosis_{window}'] = rolling_kurtosis

        window_view = np.lib.stride_tricks.sliding_window_view(self.close, window)
        rolling_mean = np.mean(window_view, axis=1)
        rolling_std = np.std(window_view, axis=1)

        zscore = (self.close - np.concatenate([[np.nan] * (window - 1), rolling_mean])) / np.where(
            np.concatenate([[np.nan] * (window - 1), rolling_std]) == 0, np.nan, 
            np.concatenate([[np.nan] * (window - 1), rolling_std])
        )
        df[f'ZScore_{window}'] = zscore

        return df