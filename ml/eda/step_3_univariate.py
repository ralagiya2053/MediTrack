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
    logs_df = pd.read_sql_query("SELECT * FROM health_logs", conn)
    vitals_df = pd.read_sql_query("SELECT * FROM vitals", conn)
    conn.close()

    os.makedirs('ml/eda/plots', exist_ok=True)
    sns.set_theme(style="whitegrid")

    # --- 1. Health Logs Analysis ---
    # Numeric: severity
    if 'severity' in logs_df.columns:
        sev = logs_df['severity'].dropna()
        print("\n--- Severity Stats ---")
        print(sev.describe())

        plt.figure(figsize=(8, 4))
        sns.histplot(sev, bins=10, kde=True, color='skyblue')
        plt.title('Distribution of Symptom Severity')
        plt.xlabel('Severity (1-10)')
        plt.savefig('ml/eda/plots/step_3_severity_hist.png')
        plt.close()

        plt.figure(figsize=(8, 2))
        sns.boxplot(x=sev, color='skyblue')
        plt.title('Severity Boxplot')
        plt.savefig('ml/eda/plots/step_3_severity_box.png')
        plt.close()

    # Categorical: symptom
    if 'symptom' in logs_df.columns:
        print("\n--- Symptom Counts ---")
        print(logs_df['symptom'].value_counts())

        plt.figure(figsize=(10, 6))
        sns.countplot(data=logs_df, y='symptom', order=logs_df['symptom'].value_counts().index, palette='viridis')
        plt.title('Symptom Frequency')
        plt.savefig('ml/eda/plots/step_3_symptom_counts.png')
        plt.close()

    # --- 2. Vitals Analysis ---
    # Numeric: value (analyzed per metric)
    metrics = vitals_df['metric'].unique()
    for m in metrics:
        m_df = vitals_df[vitals_df['metric'] == m]
        val = m_df['value']
        print(f"\n--- {m} Stats ---")
        print(val.describe())

        plt.figure(figsize=(8, 4))
        sns.histplot(val, bins=15, kde=True, color='salmon')
        plt.title(f'Distribution of {m}')
        plt.xlabel(f'Value ({m_df["unit"].iloc[0] if not m_df.empty else ""})')
        plt.savefig(f'ml/eda/plots/step_3_{m}_hist.png')
        plt.close()

        plt.figure(figsize=(8, 2))
        sns.boxplot(x=val, color='salmon')
        plt.title(f'{m} Boxplot')
        plt.savefig(f'ml/eda/plots/step_3_{m}_box.png')
        plt.close()

if __name__ == "__main__":
    main()
