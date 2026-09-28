import sqlite3
import random
from datetime import datetime, timedelta
from database.db import DATABASE

def seed_vitals_multi(user_id, days, metrics):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 1. Verify user exists
        user = cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            print(f"No user found with id {user_id}.")
            return

        # 2. Metric Configuration
        metric_configs = {
            'sleep_hours': {'range': (5.5, 8.5), 'unit': 'h', 'decimal': 1, 'delta': 0.5},
            'resting_hr': {'range': (60, 80), 'unit': 'bpm', 'decimal': 0, 'delta': 3},
            'weight_kg': {'range': (55, 85), 'unit': 'kg', 'decimal': 1, 'delta': 0.3},
            'blood_pressure_systolic': {'range': (110, 135), 'unit': 'mmHg', 'decimal': 0, 'delta': 5},
            'blood_pressure_diastolic': {'range': (70, 88), 'unit': 'mmHg', 'decimal': 0, 'delta': 3},
        }

        vitals_to_insert = []
        today = datetime.now()

        for m_name in metrics:
            if m_name not in metric_configs:
                print(f"Skipping unknown metric: {m_name}")
                continue

            cfg = metric_configs[m_name]
            current_val = random.uniform(*cfg['range'])

            for d in range(days):
                logged_at = (today - timedelta(days=d)).strftime('%Y-%m-%d')
                delta = random.uniform(-cfg['delta'], cfg['delta'])
                current_val += delta
                current_val = max(cfg['range'][0], min(cfg['range'][1], current_val))

                if cfg['decimal'] == 0:
                    val = float(round(current_val))
                else:
                    val = round(current_val, cfg['decimal'])

                vitals_to_insert.append((user_id, m_name, val, cfg['unit'], logged_at))

        # 3. Transactional Insert
        try:
            with conn:
                conn.executemany(
                    'INSERT INTO vitals (user_id, metric, value, unit, logged_at) VALUES (?, ?, ?, ?, ?)',
                    vitals_to_insert
                )

            print(f"Successfully inserted {len(vitals_to_insert)} vitals rows for user {user_id}.")

            breakdown = {}
            for m_name in metrics:
                if m_name not in metric_configs: continue
                vals = [v[2] for v in vitals_to_insert if v[1] == m_name]
                if vals:
                    breakdown[m_name] = {
                        'count': len(vals),
                        'min': min(vals),
                        'max': max(vals),
                        'avg': round(sum(vals)/len(vals), 2)
                    }

            print("\nBreakdown by metric:")
            for m, stats in breakdown.items():
                print(f" - {m}: {stats['count']} records (Min: {stats['min']}, Max: {stats['max']}, Avg: {stats['avg']})")

            print("\nSample records:")
            sample = random.sample(vitals_to_insert, min(5, len(vitals_to_insert)))
            for s in sample:
                print(f"Metric: {s[1]}, Value: {s[2]}, Unit: {s[3]}, Date: {s[4]}")

        except sqlite3.Error as e:
            print(f"Database error: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    # For this specific request: user_id=2, days=60, metrics=['weight_kg', 'blood_pressure_systolic', 'blood_pressure_diastolic']
    seed_vitals_multi(2, 60, ['weight_kg', 'blood_pressure_systolic', 'blood_pressure_diastolic'])
