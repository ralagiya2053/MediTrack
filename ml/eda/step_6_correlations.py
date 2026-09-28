import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

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

    # Pivot vitals
    vitals_pivot = vitals_df.pivot_table(
        index=['user_id', 'logged_at'],
        columns='metric',
        values='value',
        aggfunc='mean'
    ).reset_index()

    # Pivot symptoms: average severity per day
    logs_pivot = logs_df.pivot_table(
        index=['user_id', 'logged_at'],
        columns='symptom',
        values='severity',
        aggfunc='mean'
    ).reset_index()

    # Merge
    df = pd.merge(vitals_pivot, logs_pivot, on=['user_id', 'logged_at'], how='inner').fillna(0)

    # Select only numeric columns for correlation
    numeric_df = df.drop(columns=['user_id', 'logged_at'])

    # Pearson Correlation
    corr_matrix = numeric_df.corr(method='pearson')

    print("\n--- Pearson Correlation Matrix ---")
    print(corr_matrix)

    # Heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Heatmap: Vitals vs Symptoms')
    plt.tight_layout()
    plt.savefig('ml/eda/plots/step_6_correlation_heatmap.png')
    plt.close()

    # Flag high correlations (> 0.85)
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > 0.85:
                high_corr.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

    if high_corr:
        print("\n--- High Multicollinearity Warning ---")
        for pair in high_corr:
            print(f"{pair[0]} and {pair[1]}: {pair[2]:.2f}")
    else:
        print("\nNo extreme multicollinearity detected (> 0.85).")

if __name__ == "__main__":
    main()
