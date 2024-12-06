import pandas as pd
import numpy as np
from typing import List


class Features:
    """ """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        
        # Convert essential columns to NumPy arrays for efficient processing
        self.close_np = self.df['Close'].astype(np.float32).values
        self.open_np = self.df['Open'].astype(np.float32).values
        self.high_np = self.df['High'].astype(np.float32).values
        self.low_np = self.df['Low'].astype(np.float32).values
        self.volume_np = self.df['Volume'].astype(np.float32).values

    def _convert_to_float32(self) -> pd.DataFrame:
        """Convert numerical columns to float32 to save memory."""
        float_cols = [col for col in self.df.columns if self.df[col].dtype in ['float64', 'float32']]
        self.df[float_cols] = self.df[float_cols].astype('float32')
        return self.df

    # def price_based_features(self) -> pd.DataFrame:
    #     """Compute price-based features and return the updated DataFrame."""
    #     self.df['Price_change'] = np.diff(self.close_np, prepend=self.close_np[0])
    #     self.df['next_log_return'] = np.log(self.close_np / np.roll(self.close_np, 1))
    #     self.df['high_low_spread'] = self.high_np - self.low_np
    #     self.df['close_open_spread'] = self.close_np - self.open_np
        
    #     return self._convert_to_float32()

    # def volume_based_features(self) -> pd.DataFrame:
    #     """Compute volume-based features and return the updated DataFrame."""
    #     price_change = np.diff(self.close_np, prepend=self.close_np[0])
    #     direction = np.sign(price_change)
        
    #     self.df['volume_change'] = np.diff(self.volume_np, prepend=self.volume_np[0])
    #     self.df['OBV'] = np.cumsum(direction * self.volume_np)
        
    #     return self._convert_to_float32()

    # def volatility_features(self, window: int = 15) -> pd.DataFrame:
    
    #     window_view = np.lib.stride_tricks.sliding_window_view(self.close_np, window)
    #     rolling_std = np.std(window_view, axis=1)
    #     rolling_mean = np.mean(window_view, axis=1)

    #     self.df['rolling_std'] = np.concatenate([[np.nan] * (window - 1), rolling_std])
    #     self.df['upper_band'] = np.concatenate([[np.nan] * (window - 1), rolling_mean + 2 * rolling_std])
    #     self.df['lower_band'] = np.concatenate([[np.nan] * (window - 1), rolling_mean - 2 * rolling_std])

    #     # ATR (Average True Range)
    #     true_range = self.high_np - self.low_np
    #     atr = np.mean(np.lib.stride_tricks.sliding_window_view(true_range, window), axis=1)
    #     self.df['ATR'] = np.concatenate([[np.nan] * (window - 1), atr])

    #     return self._convert_to_float32()

    # def momentum_features(self, window: int = 15, rsi_window: int = 14, macd_windows: tuple = (12, 26, 9)) -> pd.DataFrame:
    
    #     # RSI Calculation
    #     self.df['RSI'] = self._calculate_rsi(self.close_np, rsi_window)

    #     # MACD and Signal Line
    #     macd, signal_line = self._calculate_macd(self.close_np, macd_windows[0], macd_windows[1], macd_windows[2])
    #     self.df['MACD'] = macd
    #     self.df['Signal_Line'] = signal_line

    #     # SMA and EMA
    #     sma = np.mean(np.lib.stride_tricks.sliding_window_view(self.close_np, window), axis=1)
    #     self.df['SMA'] = np.concatenate([[np.nan] * (window - 1), sma])
    #     self.df['EMA'] = self.df['Close'].ewm(span=window, adjust=False).mean()

    #     # Rate of Change (ROC)
    #     self.df['ROC'] = self._calculate_roc(self.close_np, window)

    #     return self._convert_to_float32()

    # def trend_features(self, window: int = 14) -> pd.DataFrame:
    
    #     plus_di, minus_di, adx = self._calculate_dmi(window)
    #     self.df['+DI'] = plus_di
    #     self.df['-DI'] = minus_di
    #     self.df['ADX'] = adx

    #     support_line, resistance_line = self._calculate_trend_lines(self.close_np, window)
    #     self.df['support_line'] = support_line.reindex(self.df.index)
    #     self.df['resistance_line'] = resistance_line.reindex(self.df.index)

    #     self._calculate_ichimoku_cloud()

    #     return self._convert_to_float32()

    # def lag_rolling_features(self, lags: List[int] | None = None, windows: List[int]| None = None) -> pd.DataFrame:
        # """"""
        # lags = lags or [1, 2, 3]
        # windows = windows or [5, 10, 20]

        # # Lag features
        # for lag in lags:
        #     self.df[f'lag_{lag}'] = np.roll(self.close_np, lag)

        # # Rolling statistics
        # for window in windows:
        #     rolling_mean = np.mean(np.lib.stride_tricks.sliding_window_view(self.close_np, window), axis=1)
        #     rolling_max = np.max(np.lib.stride_tricks.sliding_window_view(self.close_np, window), axis=1)
        #     rolling_min = np.min(np.lib.stride_tricks.sliding_window_view(self.close_np, window), axis=1)

        #     self.df[f'rolling_mean_{window}'] = np.concatenate([[np.nan] * (window - 1), rolling_mean])
        #     self.df[f'rolling_max_{window}'] = np.concatenate([[np.nan] * (window - 1), rolling_max])
        #     self.df[f'rolling_min_{window}'] = np.concatenate([[np.nan] * (window - 1), rolling_min])

        # return self._convert_to_float32()

    # def statistical_features(self, window: int = 20) -> pd.DataFrame:
    #     """Compute statistical features (Skew, Kurtosis, Z-score) and return the updated DataFrame.

    #     Parameters
    #     ----------
    #     window: int :
    #          (Default value = 20)

    #     Returns
    #     -------

    #     """
    #     rolling_skew = pd.Series(self.close_np).rolling(window=window).skew().values
    #     rolling_kurtosis = pd.Series(self.close_np).rolling(window=window).kurt().values
    #     self.df[f'Skew_{window}'] = rolling_skew
    #     self.df[f'kurtosis_{window}'] = rolling_kurtosis

    #     rolling_mean = np.mean(np.lib.stride_tricks.sliding_window_view(self.close_np, window), axis=1)
    #     rolling_std = np.std(np.lib.stride_tricks.sliding_window_view(self.close_np, window), axis=1)
    #     self.df[f'zscore_{window}'] = (self.close_np - np.concatenate([[np.nan] * (window - 1), rolling_mean])) / np.concatenate([[np.nan] * (window - 1), rolling_std])

    #     return self._convert_to_float32()

    def time_based_features(self) -> pd.DataFrame:
        """Compute time-based features and return the updated DataFrame."""
        self.df['Date'] = pd.to_datetime(self.df['timestamp'], unit='s')
        self.df['day_of_week'] = self.df['Date'].dt.dayofweek
        self.df['hour_of_day'] = self.df['Date'].dt.hour
        self.df.drop(columns=['Date'], inplace=True)

        return self._convert_to_float32()

   
 


    def fill(self, ffill: bool, bfill: bool) -> pd.DataFrame:
        """Fill NaNs with forward and/or backward fill for numeric columns, keeping float16 where possible.

        Parameters
        ----------
        ffill: bool :
            
        bfill: bool :
            

        Returns
        -------

        """
        # Select numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        # Identify float16 columns separately to handle them differently
        float16_cols = self.df.select_dtypes(include=['float16']).columns
        other_numeric_cols = numeric_cols.difference(float16_cols)

        # Apply forward fill (ffill) if specified
        if ffill:
            if not float16_cols.empty:
                # Temporarily convert float16 columns to float32 for fill, then convert back
                self.df[float16_cols] = self.df[float16_cols].astype('float32').ffill().astype('float16')
            if not other_numeric_cols.empty:
                self.df[other_numeric_cols] = self.df[other_numeric_cols].ffill()

        # Apply backward fill (bfill) if specified
        if bfill:
            if not float16_cols.empty:
                # Temporarily convert float16 columns to float32 for fill, then convert back
                self.df[float16_cols] = self.df[float16_cols].astype('float32').bfill().astype('float16')
            if not other_numeric_cols.empty:
                self.df[other_numeric_cols] = self.df[other_numeric_cols].bfill()

        return self.df