import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
from statsmodels.tsa.stattools import acf

sys.path.append(os.getcwd())
try:
    from database.db import DATABASE
except ImportError:
    DATABASE = 'meditrack.db'

def main():
    conn = sqlite3.connect(DATABASE)
    logs_df = pd.read_sql_query("SELECT user_id, symptom, severity, logged_at FROM health_logs", conn)
    vitals_df = pd.read_sql_query("SELECT user_id, metric, value, logged_at FROM vitals", conn)
    conn.close()

    # Pivot vitals to wide format: one row per user per day
    vitals_pivot = vitals_df.pivot_table(
        index=['user_id', 'logged_at'],
        columns='metric',
        values='value',
        aggfunc='mean'
    ).reset_index()

    # Pivot symptoms to wide format: count of symptoms per day
    logs_pivot = logs_df.pivot_table(
        index=['user_id', 'logged_at'],
        columns='symptom',
        values='severity',
        aggfunc='count',
        fill_value=0
    ).reset_index()

    # Merge them
    df = pd.merge(vitals_pivot, logs_pivot, on=['user_id', 'logged_at'], how='outer').fillna(0)
    df['logged_at'] = pd.to_datetime(df['logged_at'])
    df = df.sort_values(['user_id', 'logged_at'])

    os.makedirs('ml/eda/plots', exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Time Series Plots
    numeric_cols = [col for col in df.columns if col not in ['user_id', 'logged_at']]
    for col in numeric_cols:
        plt.figure(figsize=(12, 4))
        sns.lineplot(data=df, x='logged_at', y=col, hue='user_id', marker='o')
        plt.title(f'Trend of {col} over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'ml/eda/plots/step_5_{col}_time.png')
        plt.close()

    # 2. Autocorrelation for a sample vital (e.g., sleep_hours)
    if 'sleep_hours' in df.columns:
        # Use one user's data for ACF to avoid mixing users
        sample_user = df['user_id'].unique()[0]
        user_data = df[df['user_id'] == sample_user].set_index('logged_at')['sleep_hours'].fillna(0)

        if len(user_data) > 10:
            # Calculate ACF for lag 1 and lag 7
            res = acf(user_data, nlags=14)
            print(f"\n--- ACF for sleep_hours (User {sample_user}) ---")
            print(f"Lag 1: {res[1]:.3f}")
            print(f"Lag 7: {res[7]:.3f}")

            plt.figure(figsize=(8, 4))
            plt.stem(range(len(res)), res)
            plt.title(f'Autocorrelation of sleep_hours (User {sample_user})')
            plt.xlabel('Lag')
            plt.ylabel('Correlation')
            plt.savefig('ml/eda/plots/step_5_sleep_acf.png')
            plt.close()

    print(f"Analyzed {len(df)} unique user-day records.")

if __name__ == "__main__":
    main()
