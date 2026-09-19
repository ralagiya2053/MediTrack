# database/db.py
#
# Step 1 — Database Setup (to be implemented while following the course)
#
# This module will own all SQLite access for MediTrack.
#
# Planned functions:
#   get_db()   -> sqlite3.Connection
#                 - row_factory = sqlite3.Row
#                 - PRAGMA foreign_keys = ON
#
#   init_db()  -> None
#                 - CREATE TABLE IF NOT EXISTS users
#                 - CREATE TABLE IF NOT EXISTS health_logs
#                   (id, user_id, symptom, severity, notes, logged_at)
#
#   seed_db()  -> None
#                 - insert a demo user + a handful of sample health logs
#                   so the dashboard has something to render during dev
#
# Nothing is implemented yet on purpose — the course builds this next.