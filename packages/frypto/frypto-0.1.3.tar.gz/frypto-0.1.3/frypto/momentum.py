import pandas as pd
import numpy as np
from frypto.helpers import _calculate_roc, _calculate_rsi, _calculate_macd, _ewma

class MomentumFeatures:
    """
    A class for computing momentum indicators based on financial time series data, 
    including Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), 
    Simple Moving Average (SMA), Exponential Moving Average (EMA), and Rate of Change (ROC).

    Parameters
    ----------
    close : np.ndarray
        A 1D numpy array of closing prices.
    
    Methods
    -------
    compute(window=15, rsi_window=14, macd_windows=(12, 26, 9)) -> pd.DataFrame
        Computes various momentum indicators over specified window sizes and returns them in a DataFrame.
    """
    def __init__(self, close: np.ndarray) -> None:
        """
        Initialize the MomentumFeatures class with closing price data.

        Parameters
        ----------
        close : np.ndarray
            A 1D array of closing prices.
        
        Raises
        ------
        ValueError
            If the input array is empty.
        """
        if len(close) == 0:
            raise ValueError("Close array can't be empty.")
        self.close = close.astype(np.float32)
        
    def compute(self, window: int = 15, rsi_window: int = 14, macd_windows: tuple = (12, 26, 9)) -> pd.DataFrame:
        """
        Compute momentum indicators, including RSI, MACD, SMA, EMA, and ROC, for the given window sizes.

        Parameters
        ----------
        window : int, optional
            Window size for SMA, EMA, and ROC. Defaults to 15.
        rsi_window : int, optional
            Window size for RSI calculation. Defaults to 14.
        macd_windows : tuple, optional
            A tuple containing three integers representing MACD short window, long window, 
            and signal line window respectively. Defaults to (12, 26, 9).

        Returns
        -------
        pd.DataFrame
            A DataFrame with computed momentum indicators:
            - RSI: Relative Strength Index
            - MACD: Moving Average Convergence Divergence
            - Signal_Line: Signal line of the MACD
            - SMA: Simple Moving Average
            - EMA: Exponential Moving Average
            - ROC: Rate of Change
            
        Examples
        --------
        >>> from momentum import MomentumFeatures
        >>> import numpy as np
        >>> close_np = np.arange(200)
        >>> vf = MomentumFeatures(close_np)
        >>> vf.compute()
            RSI       MACD    Signal_Line         SMA     EMA          ROC
        0   NaN     0.000000       0.000000       NaN  0.000000  -100.000000
        1   NaN     0.022436       0.012464       NaN  0.533333   -99.462364
        2   NaN     0.059598       0.031781       NaN  1.088757   -98.930481
        3   NaN     0.111144       0.058666       NaN  1.666077   -98.404251
        4   NaN     0.176605       0.093750       NaN  2.265021   -97.883598

        Raises
        ------
        ValueError
            If the input array is smaller than the required window size for any of the indicators.
        """        
        if len(self.close) < min(window, rsi_window, min(macd_windows)):
            raise ValueError("close array can't be smaller than the windows")
        df = pd.DataFrame()
        
        # RSI Calculation
        df['RSI'] = _calculate_rsi(self.close, rsi_window)

        # MACD and Signal Line
        macd, signal_line = _calculate_macd(self.close, macd_windows[0], macd_windows[1], macd_windows[2])
        df['MACD'] = macd
        df['Signal_Line'] = signal_line

        # SMA and EMA
        sma = np.mean(np.lib.stride_tricks.sliding_window_view(self.close, window), axis=1)
        df['SMA'] = np.concatenate([[np.nan] * (window - 1), sma])
        df['EMA'] = _ewma(self.close, window)

        # Rate of Change (ROC)
        df['ROC'] = _calculate_roc(self.close, window)

        return df
    
