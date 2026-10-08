import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load and Preprocess
def prepare_data(df):
    # Create Lag Features for Time-Series (as per EDA)
    df = df.sort_values('date')
    df['hr_lag1'] = df['resting_hr'].shift(1)
    df = df.dropna()

    X = df.drop(columns=['resting_hr', 'date', 'user_id'])
    y = df['resting_hr']

    # Define feature types
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()

    return X, y, numeric_features, categorical_features

# 2. Model Definitions
models = {
    "Ridge": Pipeline([
        ('preprocessor', ColumnTransformer([
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])),
        ('regressor', Ridge())
    ]),
    "RandomForest": Pipeline([
        ('preprocessor', ColumnTransformer([
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ]),
    "XGBoost": Pipeline([
        ('preprocessor', ColumnTransformer([
            ('num', 'passthrough', numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])),
        ('regressor', XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42))
    ])
}

# 3. Time-Based Split (As per EDA)
# Use the first 80% of data for training, last 20% for testing
split_idx = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

# 4. Train and Evaluate
results = {}
for name, pipeline in models.items():
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    results[name] = {
        "MAE": mean_absolute_error(y_test, preds),
        "R2": r2_score(y_test, preds)
    }

print(results)