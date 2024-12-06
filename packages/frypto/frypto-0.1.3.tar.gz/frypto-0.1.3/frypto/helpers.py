import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from typing import Tuple
from numba import njit, float32, int64
from frypto.ewma import _ewma

def _pad_nan(values: np.ndarray, window: int) -> np.ndarray:
        """Pad the array with NaN values at the beginning to match the original array length."""
        return np.concatenate([np.full(window - 1, np.nan), values])


def _calculate_roc(close: np.ndarray, window: int) -> np.ndarray:
        prev_close = np.roll(close, window)
        with np.errstate(divide="ignore", invalid="ignore"):
                return np.where(prev_close != 0, ((close - prev_close) / prev_close) * 100, np.nan)

#
def _calculate_rsi(close: np.ndarray, window: int) -> np.ndarray:
        """Relative Strength Index (RSI) Calculation."""
        delta = diff_with_prepend(close)
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)

        avg_gain = np.convolve(gain, np.ones(window)/window, mode="valid")
        avg_loss = np.convolve(loss, np.ones(window)/window, mode="valid")
        with np.errstate(divide="ignore", invalid="ignore"):
                rs = np.where(avg_loss != 0, avg_gain / avg_loss, np.nan)
                rsi = 100 - (100 / (1 + rs))

        return np.concatenate([[np.nan] * (window - 1), rsi])


@njit
def diff_with_prepend(x: np.ndarray) -> np.ndarray:
    """Alternative to numpy.diff"""
    res = np.empty_like(x)
    res[0] = x[0] - x[0] # set first elemnt to zero
    res[1:] = x[1:] - x[:-1]
    return res

def _calculate_dmi(high_np: np.ndarray, low_np: np.ndarray, window: int = 14) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Directional Movement Index (DMI) Calculation."""
    delta_high = diff_with_prepend(high_np)
    delta_low = diff_with_prepend(low_np)

    plus_dm = np.where((delta_high > delta_low) & (delta_high > 0), delta_high, 0)
    minus_dm = np.where((delta_low > delta_high) & (delta_low > 0), delta_low, 0)

    # Calculate True Range
    true_range = high_np - low_np
    atr = np.mean(np.lib.stride_tricks.sliding_window_view(true_range, window), axis=1)
    atr = np.concatenate([[np.nan] * (window - 1), atr])

    # Calculate Plus and Minus Directional Indicators
    plus_di = 100 * (np.convolve(plus_dm, np.ones(window) / window, mode="valid") / atr[window - 1:])
    minus_di = 100 * (np.convolve(minus_dm, np.ones(window) / window, mode="valid") / atr[window - 1:])

    # Calculate Directional Movement Index (DX)
    dx = 100 * np.abs((plus_di - minus_di) / (plus_di + minus_di))
    adx = np.convolve(dx, np.ones(window) / window, mode="valid")

    # Concatenate NaN values for alignment
    plus_di = np.concatenate([[np.nan] * (window - 1), plus_di])
    minus_di = np.concatenate([[np.nan] * (window - 1), minus_di])
    adx = np.concatenate([[np.nan] * (window * 2 - 2), adx])

    return plus_di, minus_di, adx

def _calculate_trend_lines(close: np.ndarray, window: int = 20) -> Tuple[pd.Series, pd.Series]:
        """Support and Resistance Lines Calculation."""
        local_min = argrelextrema(close, np.less_equal, order=window)[0]
        support_line = pd.Series(close[local_min], index=local_min)

        local_max = argrelextrema(close, np.greater_equal, order=window)[0]
        resistance_line = pd.Series(close[local_max], index=local_max)

        return support_line, resistance_line

def _calculate_ichimoku_cloud(high_np: np.ndarray, low_np: np.ndarray, close_np: np.ndarray) -> pd.DataFrame:
    """Ichimoku Cloud Calculation."""
    # Ichimoku parameters
    tenkan_window = 20
    kijun_window = 60
    senkou_span_b_window = 120
    cloud_displacement = 30
    chikou_shift = -30

    # Convert arrays to Series
    high_series = pd.Series(high_np)
    low_series = pd.Series(low_np)
    close_series = pd.Series(close_np)

    df = pd.DataFrame()

    # Tenkan-sen
    tenkan_sen = (high_series.rolling(window=tenkan_window).max() +
                  low_series.rolling(window=tenkan_window).min()) / 2
    df["tenkan_sen"] = tenkan_sen

    # Kijun-sen
    kijun_sen = (high_series.rolling(window=kijun_window).max() +
                 low_series.rolling(window=kijun_window).min()) / 2
    df["kijun_sen"] = kijun_sen

    # Senkou Span A
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(cloud_displacement)
    df["senkou_span_a"] = senkou_span_a

    # Senkou Span B
    senkou_span_b = (high_series.rolling(window=senkou_span_b_window).max() +
                     low_series.rolling(window=senkou_span_b_window).min()) / 2
    senkou_span_b = senkou_span_b.shift(cloud_displacement)
    df["senkou_span_b"] = senkou_span_b

    # Chikou Span
    chikou_span = close_series.shift(chikou_shift)
    df["chikou_span"] = chikou_span

    return df

#
def _calculate_macd(
                close: np.ndarray, short_window: int = 12,\
                long_window: int = 26, signal_window: int = 9
) -> Tuple[np.ndarray, np.ndarray]:
        
        """MACD Calculation."""
        ema_12 = _ewma(close, short_window)
        ema_26 = _ewma(close, long_window)
        macd = ema_12 - ema_26
        signal_line = _ewma(macd, signal_window)
        return macd, signal_line
