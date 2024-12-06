import numpy as np
import pandas as pd


class PriceFeatures:
    """
    A class for computing price features based on financial 
    time series data, including price change, next log return, 
    high-low spread, and close-open spread.

    Parameters
    ----------
    close : np.ndarray
        A 1D numpy array of closing prices.
    high : np.ndarray
        A 1D numpy array of high prices.
    low : np.ndarray
        A 1D numpy array of low prices.
    open : np.ndarray
        A 1D numpy array of opening prices.
    
    Raises
    ------
    ValueError
        If the input arrays (`close`, `high`, `low`, `open`) do not have the same length or are empty.
    
    Methods
    -------
    compute()
        Computes price-based features and returns a DataFrame.
    """
    
    def __init__(self, close: np.ndarray, high: np.ndarray, low: np.ndarray, open: np.ndarray) -> None:
        """
        Initialize the PriceFeatures class with price data.
        
        Parameters
        ----------
        close : np.ndarray
            Array of closing prices.
        high : np.ndarray
            Array of high prices.
        low : np.ndarray
            Array of low prices.
        open : np.ndarray
            Array of opening prices.
        
        Raises
        ------
        ValueError
            If the input arrays are not of the same length or are empty.
        """
        if not (len(close) == len(high) == len(low) == len(open) > 0):
            raise ValueError("Input arrays must be of the same length and non-empty.")
        
        self.close = close
        self.high = high
        self.low = low
        self.open = open

    def compute(self) -> pd.DataFrame:
        """
        Compute price features based on financial time series data, including:
        - Price change: The difference in closing price compared to the previous day.
        - Next log return: The logarithmic return of closing prices from one day to the next.
        - High-low spread: The spread between the high and low prices of each day.
        - Close-open spread: The difference between the closing and opening prices of each day.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the computed price features:
            - Price_change: np.ndarray
            - next_log_return: np.ndarray (first value is NaN)
            - high_low_spread: np.ndarray
            - close_open_spread: np.ndarray

        Examples
        --------
        >>> close = np.random.rand(20)
        >>> high = np.random.rand(20)
        >>> low = np.random.rand(20)
        >>> open = np.random.rand(20)
        >>> pf = PriceFeatures(close, high, low, open)
        >>> pf.compute()
           Price_change  next_log_return  high_low_spread  close_open_spread
        0      0.000000              NaN        0.403473           0.241718
        1      0.129784         0.120421        0.100728          -0.467603
        2      0.113806        -0.124649        0.443221           0.100443
        3     -0.214335        -0.400601        0.584923          -0.059126
        4      0.324528         0.319745        0.774189           0.205833

        Notes
        -----
        - The first value in the `next_log_return` column is NaN since there's no previous day to compare.
        - The input arrays `close`, `high`, `low`, and `open` must all have the same length and be non-empty.
        """
        
        df = pd.DataFrame()

        # Price change from previous day
        df['Price_change'] = np.diff(self.close, prepend=self.close[0])

        # Logarithmic return, with the first value as NaN (no previous close for comparison)
        df['next_log_return'] = np.concatenate([[np.nan], np.log(self.close[1:] / self.close[:-1])])

        # High-low spread (difference between high and low prices of the day)
        df['high_low_spread'] = self.high - self.low

        # Close-open spread (difference between closing and opening prices of the day)
        df['close_open_spread'] = self.close - self.open

        return df
