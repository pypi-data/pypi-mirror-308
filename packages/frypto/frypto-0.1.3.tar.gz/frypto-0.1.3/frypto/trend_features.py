import numpy as np
import pandas as pd
from frypto.helpers import _calculate_dmi, _calculate_trend_lines, _calculate_ichimoku_cloud

# Ignore devision by 0 error
np.seterr(divide="ignore", invalid="ignore")

class TrendFeatures:
    """
    A class for computing trend-based features from financial time series data,
    including Directional Movement Index (DMI), support and resistance lines, 
    and Ichimoku Cloud indicators.

    Parameters
    ----------
    close: np.ndarray
        A 1D numpy array of closing prices.
    high: np.ndarray
        A 1D numpy array of high prices.
    low : np.ndarray
        A 1D numpy array of low prices.

    Raises
    ------
    ValueError
        If the input arrays (`close`, `high`, `low`) do not have the same length or are empty.

    Methods
    -------
    compute(window: int) -> pd.DataFrame
        Computes trend-based features, including DMI (+DI, -DI, ADX), support and resistance lines,
        and Ichimoku Cloud values, and returns them in a DataFrame.
    """
    
    def __init__(self, close: np.ndarray, high: np.ndarray, low: np.ndarray) -> None:
        """
        Initialize the TrendFeatures class with closing, high, and low price data.

        Parameters
        ----------
        close: np.ndarray
            A 1D numpy array of closing prices.
        high: np.ndarray
            A 1D numpy array of high prices.
        low : np.ndarray
            A 1D numpy array of low prices.

        Raises
        ------
        ValueError
            If the input arrays do not have the same length or are empty.
        """
        if len(close) == 0 or len(close) != len(high) or len(close) != len(low):
            raise ValueError("Input arrays must be non-empty and of the same length.")
        
        # Convert inputs to 32-bit float for consistency
        self.close = close.astype(np.float32)
        self.high = high.astype(np.float32)
        self.low = low.astype(np.float32)

    def compute(self, window: int = 15) -> pd.DataFrame:
        """
        Compute trend-based features including DMI, support/resistance lines, and Ichimoku Cloud.

        Parameters
        ----------
        window : int, optional
            The window size used for calculating trend indicators (e.g., DMI, support, and resistance).
            Defaults to 15.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the computed trend features:
            
            - +DI: Plus Directional Indicator
            - -DI: Minus Directional Indicator
            - ADX: Average Directional Index
            - support_line: Calculated support line based on price data
            - resistance_line: Calculated resistance line based on price data
            - Ichimoku Cloud columns:
                - Tenkan-sen: Short-term trend indicator
                - Kijun-sen: Medium-term trend indicator
                - Senkou Span A: Leading span 1
                - Senkou Span B: Leading span 2
                - Chikou Span: Lagging span

        Raises
        ------
        ValueError
            If the window size is larger than the input array length.

        Examples
        --------
        >>> from trend_features import TrendFeatures
        >>> import numpy as np
        >>> import yfinance as yf

        >>> data = yf.download('BTC-USD', period='max', interval='1d')
        >>> close_np = data['Close'].values
        >>> high_np = data['High'].values
        >>> low_np = data['Low'].values

        >>> tf = TrendFeatures(close_np, high_np, low_np)
        >>> result = tf.compute()

        >>> print(result.head())
            +DI     -DI     ADX     support_line    resistance_line   tenkan_sen   kijun_sen   senkou_span_a   senkou_span_b   chikou_span
            11.45   17.15   28.34   NaN             NaN               61991.02     59539.70   59944.59        60533.85        NaN
            13.39   15.44   27.31   NaN             NaN               62054.38     59539.70   59175.97        60533.85        NaN
            16.64   15.04   26.66   NaN             NaN               62849.47     59539.70   59175.97        60533.85        NaN
            14.46   15.46   26.01   NaN             NaN               63179.75     59539.70   59175.97        60533.85        NaN
        """

        if len(self.close) < window:
            raise ValueError(f"Window size must be smaller than or equal to the length of the input arrays ({len(self.close)}).")
        
        df = pd.DataFrame()

        # DMI (+DI, -DI, ADX) Calculation
        df['+DI'], df['-DI'], df['ADX'] = _calculate_dmi(self.high, self.low, window)

        # Support and Resistance Lines Calculation
        support_line, resistance_line = _calculate_trend_lines(self.close, window)
        df['support_line'] = support_line.reindex(df.index)
        df['resistance_line'] = resistance_line.reindex(df.index)

        # Ichimoku Cloud Calculation
        ichimoku_df = _calculate_ichimoku_cloud(self.high, self.low, self.close)
        df = pd.concat([df, ichimoku_df], axis=1)

        return df