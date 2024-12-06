# import time
# import pandas as pd
# import numpy as np
# from functools import wraps
# from sklearn.metrics import mean_squared_error

# # from .feature_engineering import Features

# def read_data(data_folder, path):
#     """

#     Parameters
#     ----------
#     data_folder :
        
#     path :
        

#     Returns
#     -------

#     """
#     return pd.read_csv(data_folder + path)


# def get_asset(df, id):
#     """

#     Parameters
#     ----------
#     df :
        
#     id :
        

#     Returns
#     -------

#     """
#     asset_df = df[df["Asset_ID"]==id].set_index("timestamp")
#     asset_df = asset_df.sort_index()
#     return asset_df

# def reduce_memory_usage(df):
#     """Reduces memory usage of a DataFrame by downcasting numeric columns.

#     Parameters
#     ----------
#     df :
        

#     Returns
#     -------

#     """
#     start_mem = df.memory_usage().sum() / 1024**2
#     print(f'Memory usage of dataframe is {start_mem:.2f} MB')

#     for col in df.columns:
#         col_type = df[col].dtype

#         if col_type != object and not pd.api.types.is_categorical_dtype(col_type):
#             c_min = df[col].min()
#             c_max = df[col].max()
#             if str(col_type).startswith('int'):
#                 if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
#                     df[col] = df[col].astype(np.int8)
#                 elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
#                     df[col] = df[col].astype(np.int16)
#                 elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
#                     df[col] = df[col].astype(np.int32)
#             else:
#                 if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
#                     df[col] = df[col].astype(np.float16)
#                 elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
#                     df[col] = df[col].astype(np.float32)
#     end_mem = df.memory_usage().sum() / 1024**2
#     print(f'Memory usage after optimization is: {end_mem:.2f} MB')
#     print(f'Decreased by {100 * (start_mem - end_mem) / start_mem:.1f}%')

#     return df


# def fill_timestamps(df, asset_id):
#     """

#     Parameters
#     ----------
#     df :
        
#     asset_id :
        

#     Returns
#     -------

#     """
#     asset_df = get_asset(df, asset_id)
#     full_time_range = range(asset_df.index[0],asset_df.index[-1]+60,60)
#     asset_df = asset_df.reindex(full_time_range, method='pad')
#     asset_df = asset_df.ffill(axis=1)
#     asset_df = asset_df.bfill(axis=1)
#     return asset_df

# # def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
#     """

#     Parameters
#     ----------
#     df :
#         pd.DataFrame:
#     df: pd.DataFrame :
        

#     Returns
#     -------

#     """
#     features = Features(df)

#     # Apply all the feature engineering methods
#     df = features.price_based_features()
#     df = features.volume_based_features()
#     df = features.volatility_features()
#     df = features.momentum_features()
#     df = features.trend_features()
#     df = features.lag_rolling_features()
#     df = features.statistical_features()
#     df = features.time_based_features()
#     df = features.fill(ffill=True, bfill=True)

#     return df

# def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
#     """

#     Parameters
#     ----------
#     df :
#         pd.DataFrame:
#     df: pd.DataFrame :
        

#     Returns
#     -------

#     """
#     for col in df.columns:
#         col_type = df[col].dtype
#         if col_type != object:
#             if 'int' in str(col_type):
#                 df[col] = pd.to_numeric(df[col], downcast='integer')
#             elif 'float' in str(col_type):
#                 df[col] = pd.to_numeric(df[col], downcast='float')
#         else:
#             df[col] = df[col].astype('category')
#     return df


# # Evaluate performance for each asset using the original 'Target' and 'Prediction'
# def evaluate_predictions(df):
#     """

#     Parameters
#     ----------
#     df :
        

#     Returns
#     -------

#     """
    
#     df = df.dropna(subset=['Target', 'Prediction'])

#     if df.empty:
#         return np.nan, np.nan
#     df['Target'] = pd.to_numeric(df['Target'], errors='coerce')
#     df['Prediction'] = pd.to_numeric(df['Prediction'], errors='coerce')
#     rmse = np.sqrt(mean_squared_error(df['Target'], df['Prediction']))
#     correlation = np.corrcoef(df['Target'], df['Prediction'])[0, 1]
#     return rmse, correlation

# # Define the weighted correlation function if not already defined
# def weighted_correlation(x, y, w):
#     """Compute the weighted Pearson correlation coefficient between x and y.

#     Parameters
#     ----------
#     x :
        
#     y :
        
#     w :
        

#     Returns
#     -------

#     """
#     w_sum = np.sum(w)
#     w_mean_x = np.sum(w * x) / w_sum
#     w_mean_y = np.sum(w * y) / w_sum
#     cov_xy = np.sum(w * (x - w_mean_x) * (y - w_mean_y)) / w_sum
#     var_x = np.sum(w * (x - w_mean_x) ** 2) / w_sum
#     var_y = np.sum(w * (y - w_mean_y) ** 2) / w_sum
#     corr = cov_xy / (np.sqrt(var_x) * np.sqrt(var_y))
#     return corr

# def get_time_series_splits(data, n_splits=5):
#     """

#     Parameters
#     ----------
#     data :
        
#     n_splits :
#         (Default value = 5)

#     Returns
#     -------

#     """
#     times = data['timestamp'].unique()
#     times.sort()
#     n_samples = len(times)

#     if n_samples < n_splits + 1:
#         n_splits = n_samples - 1
#         print(f"Adjusted number of splits to {n_splits} due to insufficient timestamps.")

#     fold_size = n_samples // (n_splits + 1)
#     splits = []

#     for i in range(n_splits):
#         train_end = (i + 1) * fold_size
#         test_start = train_end
#         test_end = test_start + fold_size

#         train_times = times[:train_end]
#         if i == n_splits - 1:
#             test_times = times[test_start:]
#         else:
#             test_times = times[test_start:test_end]

#         train_idx = data[data['timestamp'].isin(train_times)].index
#         test_idx = data[data['timestamp'].isin(test_times)].index

#         splits.append((train_idx, test_idx))

#     return splits


# def timeit(func):
#     @wraps(func)
#     def time_wrapper(*args, **kwargs):
#         start_time = time.perf_counter()
#         result = func(*args, **kwargs)
#         end_time = time.perf_counter()
#         total_time = end_time - start_time
#         print(f'function {func.__name__} {args} {kwargs} took {total_time:.4f} seconds to run')
#         return result
#     return time_wrapper