import sqlite3
import random
from datetime import datetime, timedelta
from database.db import DATABASE

def seed_vitals(user_id, days, metric=None):
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

        # Determine which metrics to seed
        metrics_to_seed = [metric] if metric else ['sleep_hours', 'resting_hr']

        vitals_to_insert = []
        today = datetime.now()

        for m_name in metrics_to_seed:
            cfg = metric_configs[m_name]
            # Start with a random value in range
            current_val = random.uniform(*cfg['range'])

            for d in range(days):
                logged_at = (today - timedelta(days=d)).strftime('%Y-%m-%d')

                # Random walk
                delta = random.uniform(-cfg['delta'], cfg['delta'])
                current_val += delta

                # Clamp to range
                current_val = max(cfg['range'][0], min(cfg['range'][1], current_val))

                # Apply precision
                if cfg['decimal'] == 0:
                    val = float(round(current_val))
                else:
                    val = round(current_val, cfg['decimal'])

                vitals_to_insert.append((
                    user_id,
                    m_name,
                    val,
                    cfg['unit'],
                    logged_at
                ))

        # 3. Transactional Insert
        try:
            with conn:
                conn.executemany(
                    'INSERT INTO vitals (user_id, metric, value, unit, logged_at) VALUES (?, ?, ?, ?, ?)',
                    vitals_to_insert
                )

            # 4. Confirmation Report
            print(f"Successfully inserted {len(vitals_to_insert)} vitals rows for user {user_id}.")

            # Breakdown and Stats
            breakdown = {}
            for m_name in metrics_to_seed:
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

            # Sample 5 records
            print("\nSample records:")
            sample = random.sample(vitals_to_insert, min(5, len(vitals_to_insert)))
            for s in sample:
                print(f"Metric: {s[1]}, Value: {s[2]}, Unit: {s[3]}, Date: {s[4]}")

        except sqlite3.Error as e:
            print(f"Database error: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python seed_vitals_script.py <user_id> <days> [metric]")
        print("Examples:\n  python seed_vitals_script.py 1 14\n  python seed_vitals_script.py 1 14 sleep_hours")
        sys.exit(1)

    try:
        uid = int(sys.argv[1])
        dys = int(sys.argv[2])
        met = sys.argv[3] if len(sys.argv) > 3 else None

        # Validate metric if provided
        allowed = ['sleep_hours', 'resting_hr', 'weight_kg', 'blood_pressure_systolic', 'blood_pressure_diastolic']
        if met and met not in allowed:
            print(f"Unknown metric '{met}'. Allowed: {', '.join(allowed)}.")
            sys.exit(1)

        seed_vitals(uid, dys, met)
    except ValueError:
        print("Usage: python seed_vitals_script.py <user_id> <days> [metric]")
        sys.exit(1)
