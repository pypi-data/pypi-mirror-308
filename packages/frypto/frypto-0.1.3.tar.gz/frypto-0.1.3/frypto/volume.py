import numpy as np
import pandas as pd

class VolumeFeatures:
    """
    A class for computing volume features based on time-series data, 
    including volume change and On-Balance Volume (OBV).
    
    Parameters
    ----------
    close : np.ndarray
        A 1D numpy array of close prices.
    
    volume : np.ndarray
        A 1D numpy array of trading volumes.
    
    Raises
    ------
    ValueError
        If input arrays do not have the same length or if they are empty.
    
    Methods
    -------
    compute() -> pd.DataFrame
        Computes volume-based features and returns them in a DataFrame.
    """
    
    def __init__(self, close: np.ndarray, volume: np.ndarray) -> None:
        """
        Initialize the VolumeFeatures class with price and volume data.

        Parameters
        ----------
        close : np.ndarray
            Array of close prices.
        volume : np.ndarray
            Array of trading volumes.

        Raises
        ------
        ValueError
            If input arrays are not of the same length or if they are empty.
        """
        if not (len(close) == len(volume) > 0):
            raise ValueError("Input arrays must be of the same length and non-empty.")
        
        self.close = close
        self.volume = volume

    def compute(self) -> pd.DataFrame:
        """
        Compute volume-based features including volume change and On-Balance Volume (OBV).

        Features
        --------
        - volume_change: The day-to-day change in trading volume.
        - OBV: On-Balance Volume (a cumulative measure based on price direction and volume).

        Returns
        -------
        pd.DataFrame
            DataFrame containing the computed volume features:
            - volume_change: np.ndarray
            - OBV: np.ndarray (starting at 0 for the first entry)

        Examples
        --------
        >>> close = np.array([100, 102, 101, 103, 105])
        >>> volume = np.array([1000, 1500, 1200, 1300, 1600])
        >>> vf = VolumeFeatures(close, volume)
        >>> vf.compute()
           volume_change     OBV
        0         0.0        0.0
        1       500.0     1500.0
        2      -300.0        0.0
        3       100.0     1300.0
        4       300.0     2900.0

        Notes
        -----
        - The OBV starts at 0 and accumulates based on the direction of price changes.
        - If the price increases, OBV adds the day's volume; if it decreases, OBV subtracts the day's volume.
        """
        
        df = pd.DataFrame()

        # Price change (used for OBV direction)
        price_change = np.diff(self.close, prepend=self.close[0])
        
        # Calculate direction (+1 for up, -1 for down, 0 for no change)
        direction = np.sign(price_change)
        
        # Volume change from the previous day
        df['volume_change'] = np.diff(self.volume, prepend=self.volume[0])
        
        # On-Balance Volume (OBV), starting at 0
        df['OBV'] = np.cumsum(direction * self.volume)
        
        return df