import sqlite3
from flask import g
from werkzeug.security import generate_password_hash

DATABASE = 'meditrack.db'

def get_db():
    """
    Opens a connection to meditrack.db in the project root.
    Sets row_factory = sqlite3.Row and PRAGMA foreign_keys = ON.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def init_db():
    """
    Creates all three tables using CREATE TABLE IF NOT EXISTS.
    Safe to call multiple times.
    """
    db = sqlite3.connect(DATABASE)
    with db:
        # Users Table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Health Logs Table
        db.execute('''
            CREATE TABLE IF NOT EXISTS health_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_type TEXT NOT NULL CHECK (entry_type IN ('symptom', 'medication')),
                symptom TEXT,
                severity INTEGER CHECK (severity BETWEEN 1 AND 10),
                notes TEXT,
                logged_at TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')

        # Vitals Table
        db.execute('''
            CREATE TABLE IF NOT EXISTS vitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                metric TEXT NOT NULL CHECK (metric IN (
                    'sleep_hours',
                    'resting_hr',
                    'weight_kg',
                    'blood_pressure_systolic',
                    'blood_pressure_diastolic'
                )),
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                logged_at TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
    db.close()

def seed_db():
    """
    Populates the database with initial demo data if not already present.
    Prevents duplicate inserts.
    """
    db = sqlite3.connect(DATABASE)
    with db:
        # 1. Check if users table already contains data
        user = db.execute('SELECT id FROM users LIMIT 1').fetchone()
        if user:
            return # Return early to prevent duplication

        # 2. Insert demo user
        demo_password = generate_password_hash('demo123')
        cursor = db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            ('Demo User', 'demo@meditrack.com', demo_password)
        )
        user_id = cursor.lastrowid

        # 3. Insert 8 sample health logs (symptoms)
        # Fixed list: Headache, Fatigue, Nausea, Fever, Cough, Sore Throat, Muscle Pain, Other
        logs = [
            (user_id, 'symptom', 'Headache', 3, 'Mild tension', '2026-09-01'),
            (user_id, 'symptom', 'Headache', 5, None, '2026-09-05'),
            (user_id, 'symptom', 'Headache', 2, None, '2026-09-10'),
            (user_id, 'symptom', 'Fatigue', 5, 'After long shift', '2026-09-12'),
            (user_id, 'symptom', 'Cough', 4, None, '2026-09-14'),
            (user_id, 'symptom', 'Muscle Pain', 7, 'Lower back soreness', '2026-09-16'),
            (user_id, 'symptom', 'Nausea', 2, None, '2026-09-18'),
            (user_id, 'symptom', 'Fever', 6, None, '2026-09-20'),
        ]
        db.executemany(
            'INSERT INTO health_logs (user_id, entry_type, symptom, severity, notes, logged_at) VALUES (?, ?, ?, ?, ?, ?)',
            logs
        )

        # 4. Insert 4 sample vitals for Sleep (~7.2 avg) and Resting HR (~68 avg)
        vitals = [
            # Sleep hours: 7.0, 7.5, 7.0, 7.3 = Avg 7.2
            (user_id, 'sleep_hours', 7.0, 'h', '2026-09-17'),
            (user_id, 'sleep_hours', 7.5, 'h', '2026-09-18'),
            (user_id, 'sleep_hours', 7.0, 'h', '2026-09-19'),
            (user_id, 'sleep_hours', 7.3, 'h', '2026-09-20'),
            # Resting HR: 66, 68, 70, 68 = Avg 68
            (user_id, 'resting_hr', 66.0, 'bpm', '2026-09-17'),
            (user_id, 'resting_hr', 68.0, 'bpm', '2026-09-18'),
            (user_id, 'resting_hr', 70.0, 'bpm', '2026-09-19'),
            (user_id, 'resting_hr', 68.0, 'bpm', '2026-09-20'),
        ]
        db.executemany(
            'INSERT INTO vitals (user_id, metric, value, unit, logged_at) VALUES (?, ?, ?, ?, ?)',
            vitals
        )
    db.close()
