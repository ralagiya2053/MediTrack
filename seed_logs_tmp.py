import sqlite3
import random
from datetime import datetime, timedelta
from database.db import DATABASE

def seed_health_logs(user_id, count, days):
    # 1. Verify user exists
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        user = cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            print(f"No user found with id {user_id}.")
            return

        # 2. Generation Parameters
        symptoms_list = [
            'Headache', 'Fatigue', 'Nausea', 'Fever',
            'Cough', 'Sore Throat', 'Muscle Pain', 'Other'
        ]

        # Weighting for symptom frequency (Roughly proportional)
        # Headache/Fatigue most common, Fever/Nausea least common
        weights = [0.25, 0.25, 0.05, 0.05, 0.15, 0.10, 0.10, 0.05]

        # Severity distribution
        # 60% [1,2,3], 30% [4,5,6], 10% [7,8,9,10]
        def get_severity():
            r = random.random()
            if r < 0.60:
                return random.randint(1, 3)
            elif r < 0.90:
                return random.randint(4, 6)
            else:
                return random.randint(7, 10)

        notes_pool = [
            "Feels slightly better today",
            "Woke up feeling rough",
            "After a long day at work",
            "Started in the afternoon",
            "Persistent since morning",
            "Mild but annoying",
            "Getting worse",
            "Seems to be improving"
        ]

        logs_to_insert = []
        today = datetime.now()

        for _ in range(count):
            # Random date within past 'days'
            random_days_ago = random.randint(0, days - 1)
            logged_at = (today - timedelta(days=random_days_ago)).strftime('%Y-%m-%d')

            symptom = random.choices(symptoms_list, weights=weights)[0]
            severity = get_severity()

            # ~40% have notes
            note = random.choice(notes_pool) if random.random() < 0.4 else None

            logs_to_insert.append((
                user_id,
                'symptom',
                symptom,
                severity,
                note,
                logged_at
            ))

        # Validation before insert
        for log in logs_to_insert:
            severity = log[3]
            symptom = log[2]
            assert 1 <= severity <= 10, f"Severity {severity} out of range!"
            assert symptom is not None, "Symptom cannot be null!"

        # 3. Transactional Insert
        try:
            with conn:
                conn.executemany(
                    'INSERT INTO health_logs (user_id, entry_type, symptom, severity, notes, logged_at) VALUES (?, ?, ?, ?, ?, ?)',
                    logs_to_insert
                )

            # 4. Confirmation Report
            print(f"Successfully inserted {count} health logs for user {user_id}.")

            # Date range
            dates = [log[5] for log in logs_to_insert]
            print(f"Date range: {min(dates)} to {max(dates)}")

            # Breakdown by symptom
            symptom_counts = {}
            for log in logs_to_insert:
                s = log[2]
                symptom_counts[s] = symptom_counts.get(s, 0) + 1

            print("\nBreakdown by symptom:")
            for s in symptoms_list:
                print(f" - {s}: {symptom_counts.get(s, 0)}")

            # Sample 5 records
            print("\nSample records:")
            sample = random.sample(logs_to_insert, min(5, count))
            for s in sample:
                print(f"Symptom: {s[2]}, Severity: {s[3]}, Date: {s[5]}, Notes: {s[4]}")

        except sqlite3.IntegrityError as e:
            print(f"Database integrity error: {e}")
        except Exception as e:
            print(f"An error occurred during insertion: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Usage: python seed_logs_script.py <user_id> <count> <days>")
        print("Example: python seed_logs_script.py 1 20 14")
        sys.exit(1)

    try:
        uid = int(sys.argv[1])
        cnt = int(sys.argv[2])
        dys = int(sys.argv[3])
        seed_health_logs(uid, cnt, dys)
    except ValueError:
        print("Usage: python seed_logs_script.py <user_id> <count> <days>")
        print("Example: python seed_logs_script.py 1 20 14")
        sys.exit(1)
