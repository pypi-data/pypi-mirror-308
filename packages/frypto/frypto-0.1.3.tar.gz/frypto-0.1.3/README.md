# Frypto: Feature Engineering for Financial Time Series (Crypto)

Frypto is a Python package designed to compute a set of financial time series features, including price-based, volume-based, volatility, momentum, trend, and statistical features.

---

## Table of Contents
- [Why Frypto?](#why-frypto)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Jupyter Notebooks](#jupyter-notebooks)
- [Contributing](#contributing)
- [License](#license)

---

## Why Frypto?
- In the G-Research competition, the top 3 winners demonstrated the critical role feature engineering plays in predicting real-world crypto market data.
- **Frypto saves over 100 hours** of manual feature creation and uses memory optimization tools to handle large datasets smoothly.

---

## Quick Start

### Install with pip

```bash
pip install frypto
```

### Running Frypto
Load your cryptocurrency data (or download data with yfinance as shown below).

```python
from frypto import AllFeatures
import yfinance as yf

# Download BTC-USD data from Yahoo Finance (or use your dataset)
data = yf.download('BTC-USD', period='max', interval='1d')

# Initialize Frypto and compute features
allfeatures = AllFeatures(data)
features = allfeatures.compute()  # Returns a pd.DataFrame with the new features

# View the top rows of the generated features
print(features.head())  # New DataFrame with 41 features
```

---

## Usage

Frypto computes a range of financial time series features, including **price changes, spreads, rolling statistics, momentum indicators, trend indicators, volatility measures, volume-based features, and lagged features.**

- **Price and Spread Features**: `Price_change`, `next_log_return`, `high_low_spread`, `close_open_spread`
- **Volatility Features**: `rolling_std`, `upper_band`, `lower_band`, `ATR`
- **Momentum Indicators**: `RSI`, `MACD`, `Signal_Line`, `SMA`, `EMA`, `ROC`
- **Statistical Features**: `Skew_20`, `Kurtosis_20`, `ZScore_20`
- **Volume-Based Features**: `volume_change`, `OBV`
- **Lagged and Rolling Features**: `lag_1`, `lag_2`, `lag_3`, `rolling_mean`, `rolling_max`, `rolling_min` (for windows 5, 10, and 20)
- **Trend Indicators**: `+DI`, `-DI`, `ADX`, `support_line`, `resistance_line`, `tenkan_sen`, `kijun_sen`, `senkou_span_a`, `senkou_span_b`, `chikou_span`
```python
import numpy as np
import pandas as pd
import yfinance as yf
from price import PriceFeatures
from volatility import VolatilityFeatures
from momentum import MomentumFeatures
from statistical_features import StatisticalFeatures
from volume import VolumeFeatures
from trend_features import TrendFeatures
from lag_rolling import LagRollingFeatures

# Download historical BTC-USD data
data = yf.download('BTC-USD', period='max', interval='1d')
close = data['Close'].values
high = data['High'].values
low = data['Low'].values
volume = data['Volume'].values
open_ = data['Open'].values

# Initialize and compute Price Features
price_features = PriceFeatures(close=close, high=high, low=low, open=open_)
price_df = price_features.compute()
print("Price Features:\n", price_df.head())

# Initialize and compute Volatility Features with a specified window
volatility_features = VolatilityFeatures(close=close, high=high, low=low)
volatility_df = volatility_features.compute(window=15)
print("Volatility Features:\n", volatility_df.head())

# Initialize and compute Momentum Features, with specified windows for RSI and MACD
momentum_features = MomentumFeatures(close=close)
momentum_df = momentum_features.compute(window=15, rsi_window=14, macd_windows=(12, 26, 9))
print("Momentum Features:\n", momentum_df.head())

# Initialize and compute Statistical Features with a specified rolling window
statistical_features = StatisticalFeatures(close=close)
statistical_df = statistical_features.compute(window=20)
print("Statistical Features:\n", statistical_df.head())

# Initialize and compute Volume Features
volume_features = VolumeFeatures(close=close, volume=volume)
volume_df = volume_features.compute()
print("Volume Features:\n", volume_df.head())

# Initialize and compute Trend Indicators with a specified window
trend_features = TrendFeatures(close=close, high=high, low=low)
trend_df = trend_features.compute(window=15)
print("Trend Features:\n", trend_df.head())

# Initialize and compute Lagged and Rolling Statistics with specified lags and windows
lag_rolling_features = LagRollingFeatures(close=close)
lag_rolling_df = lag_rolling_features.compute(lags=[1, 2, 3], windows=[5, 10, 20])
print("Lag and Rolling Features:\n", lag_rolling_df.head())

# Combine all computed features into a single DataFrame
all_features_df = pd.concat([
    price_df, 
    volatility_df, 
    momentum_df, 
    statistical_df, 
    volume_df, 
    trend_df, 
    lag_rolling_df
], axis=1)

print("All Computed Features:\n", all_features_df.head())
```

---

## Jupyter Notebooks

Explore the example notebooks to learn more about Frypto:

- [Getting Started with Frypto](notebooks/Getting_Started_with_Frypto.ipynb): Step-by-step guide to setting up and using Frypto.
- [Exploring Individual Feature Types](notebooks/Exploring_Individual_Features.ipynb): Detailed exploration of each feature type and its applications.

---

## Contributing

### Clone the repo

```bash
git clone https://github.com/NotAbdelrahmanelsayed/frypto
cd frypto
```

### Create the environment

Ensure `virtualenv` is installed:

```bash
pip install virtualenv
```

Then, create and activate a virtual environment:

**Linux**
```bash
virtualenv venv
source venv/bin/activate
```

**Windows Powershell**
```bash
virtualenv venv
.\venv\Scripts\Activate.ps1
```

### Install the requirements

```bash
pip install -r requirements.txt
```

### Run the tests

To run unit tests:

```bash
pytest
```

To test multiple Python versions (3.7, 3.8, 3.9, 3.10, 3.11, 3.12):

```bash
tox
```

### Submit a pull request

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.

---

## License
This project is licensed under the MIT License.