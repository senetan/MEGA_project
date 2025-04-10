import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler
from app.data import df_de_merged


def compress_df(df):
    """
compress df_de_merged
- downcasts numeric columns (int64/float64) to lower memory types, except datetime columns.
"""
    df_compressed = df.copy()
    for col in df_compressed.columns:
        # skip datetime columns
        if pd.api.types.is_datetime64_any_dtype(df_compressed[col]):
            continue
        if pd.api.types.is_numeric_dtype(df_compressed[col]):
            if pd.api.types.is_integer_dtype(df_compressed[col]):
                df_compressed[col] = pd.to_numeric(df_compressed[col], downcast='integer')
            elif pd.api.types.is_float_dtype(df_compressed[col]):
                df_compressed[col] = pd.to_numeric(df_compressed[col], downcast='float')
    return df_compressed

df_de_merged = compress_df(df_de_merged)
print("compressed dtypes:")
print(df_de_merged.dtypes)


def extract_time_energy_features(x):
    """
cell: feature extraction and normalization (stateless preprocessor)
- extracts time features (cyclical and one-hot encoded),
- extracts energy features,
- computes relative percentages for energy sources (each divided by the row sum),
- returns a fixed-order dataframe.
"""
    x = x.copy()
    # time features
    x['datetime'] = pd.to_datetime(x['datetime'])
    x['hour'] = x['datetime'].dt.hour
    x['weekday'] = x['datetime'].dt.weekday
    x['hour_sin'] = np.sin(2 * np.pi * x['hour'] / 24)
    x['hour_cos'] = np.cos(2 * np.pi * x['hour'] / 24)
    x['weekday_sin'] = np.sin(2 * np.pi * x['weekday'] / 7)
    x['weekday_cos'] = np.cos(2 * np.pi * x['weekday'] / 7)
    # one-hot encoding for time
    hour_dummies = pd.get_dummies(x['hour'], prefix='hour')
    weekday_dummies = pd.get_dummies(x['weekday'], prefix='weekday')
    expected_hour_cols = [f'hour_{i}' for i in range(24)]
    expected_weekday_cols = [f'weekday_{i}' for i in range(7)]
    hour_dummies = hour_dummies.reindex(columns=expected_hour_cols, fill_value=0)
    weekday_dummies = weekday_dummies.reindex(columns=expected_weekday_cols, fill_value=0)
    time_order = ['hour_sin', 'hour_cos', 'weekday_sin', 'weekday_cos'] + expected_hour_cols + expected_weekday_cols
    time_features = pd.concat([x[['hour_sin','hour_cos','weekday_sin','weekday_cos']], hour_dummies, weekday_dummies], axis=1)
    time_features = time_features[time_order]

    # energy features: from df_de_electricity_sources, keys assumed to be in x
    energy_cols = [
        "powerConsumptionBreakdown.nuclear",
        "powerConsumptionBreakdown.geothermal",
        "powerConsumptionBreakdown.biomass",
        "powerConsumptionBreakdown.coal",
        "powerConsumptionBreakdown.wind",
        "powerConsumptionBreakdown.solar",
        "powerConsumptionBreakdown.hydro",
        "powerConsumptionBreakdown.gas",
        "powerConsumptionBreakdown.oil"
    ]
    energy_features = x[energy_cols].copy()
    # compute the row-wise sum for energy sources
    energy_sum = energy_features.sum(axis=1).replace(0, np.nan)
    # compute relative percentage (0 to 1)
    energy_relative = energy_features.div(energy_sum, axis=0).fillna(0)

    final_order = time_order + energy_cols
    final_features = pd.concat([time_features, energy_relative], axis=1)
    final_features = final_features[final_order]
    return final_features

# pure transformer without state using function transformer
feature_transformer = FunctionTransformer(extract_time_energy_features, validate=False)

# build pipeline (stateless preprocessor)
features_pipeline = Pipeline([
    ('feature_extraction_and_normalization', feature_transformer)
])

# test on the merged dataframe (df_de_merged should have both 'datetime' and energy columns)
df_processed = features_pipeline.transform(df_de_merged)
print("preprocessed features shape:", df_processed.shape)

# Chronological split
split_ratio = 0.20
test_length = int(len(df_de_merged) * split_ratio)
val_length = int((len(df_de_merged) - test_length) * split_ratio)
train_length = len(df_de_merged) - val_length - test_length

df_train = df_de_merged.iloc[:train_length, :].copy()
df_val   = df_de_merged.iloc[train_length: train_length + val_length, :].copy()
df_test  = df_de_merged.iloc[train_length + val_length:, :].copy()

print("train shape:", df_train.shape)
print("validation shape:", df_val.shape)
print("test shape:", df_test.shape)

# Define target variables
y_train = df_train['carbonIntensity']
y_val   = df_val['carbonIntensity']
y_test  = df_test['carbonIntensity']

# define target scaler and transform target variables
target_scaler = MinMaxScaler()
y_train_scaled = target_scaler.fit_transform(y_train.values.reshape(-1, 1))
y_val_scaled   = target_scaler.transform(y_val.values.reshape(-1, 1))
y_test_scaled  = target_scaler.transform(y_test.values.reshape(-1, 1))

# preprocess the data splits using the state-less features pipeline
X_train_processed = features_pipeline.transform(df_train)
X_val_processed = features_pipeline.transform(df_val)
X_test_processed = features_pipeline.transform(df_test)

print("processed feature shapes:")
print("X_train_processed:", X_train_processed.shape)
print("X_val_processed:", X_val_processed.shape)
print("X_test_processed:", X_test_processed.shape)
