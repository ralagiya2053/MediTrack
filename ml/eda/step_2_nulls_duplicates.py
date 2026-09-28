import sqlite3
import pandas as pd
import sys
import os

sys.path.append(os.getcwd())
try:
    from database.db import DATABASE
except ImportError:
    DATABASE = 'meditrack.db'

def analyze_nulls(df, name):
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100

    print(f"\n--- Null Analysis: {name} ---")
    summary = pd.DataFrame({'Count': null_counts, 'Percentage (%)': null_pct})
    print(summary[summary['Count'] > 0])
    return summary

def main():
    conn = sqlite3.connect(DATABASE)
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    logs_df = pd.read_sql_query("SELECT * FROM health_logs", conn)
    vitals_df = pd.read_sql_query("SELECT * FROM vitals", conn)
    conn.close()

    for name, df in [("users", users_df), ("health_logs", logs_df), ("vitals", vitals_df)]:
        analyze_nulls(df, name)

        # Duplicates
        dupes = df.duplicated().sum()
        print(f"Fully duplicated rows in {name}: {dupes}")

        # ID duplicates
        id_dupes = df.duplicated(subset=['id']).sum()
        print(f"Duplicates on 'id' in {name}: {id_dupes}")

if __name__ == "__main__":
    main()
