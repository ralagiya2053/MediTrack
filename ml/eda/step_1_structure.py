import sqlite3
import pandas as pd
import sys
import os

# Ensure project root is in path to import database.db
sys.path.append(os.getcwd())
try:
    from database.db import DATABASE
except ImportError:
    DATABASE = 'meditrack.db'


def main():
    conn = sqlite3.connect(DATABASE)

    # Load tables
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    logs_df = pd.read_sql_query("SELECT * FROM health_logs", conn)
    vitals_df = pd.read_sql_query("SELECT * FROM vitals", conn)

    conn.close()

    results = {}
    for name, df in [("users", users_df), ("health_logs", logs_df), ("vitals", vitals_df)]:
        results[name] = {
            "shape": df.shape,
            "dtypes": df.dtypes.to_dict(),
            "memory": df.memory_usage(deep=True).sum(),
            "head": df.head(5).to_dict(orient='records'),
            "tail": df.tail(5).to_dict(orient='records')
        }

    # Print summary for the agent/user
    for name, res in results.items():
        print(f"--- {name} ---")
        print(f"Shape: {res['shape']}")
        print(f"Columns: {list(res['dtypes'].keys())}")
        print(f"Memory: {res['memory']} bytes\n")

if __name__ == "__main__":
    main()
