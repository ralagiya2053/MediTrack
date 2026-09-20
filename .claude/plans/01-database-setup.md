# Database Setup Implementation Plan

## Context
This change implements the database layer for MediTrack. The goal is to establish a reliable SQLite-based storage system for users and their health logs, integrated into the Flask application lifecycle. This forms the foundation for authentication, profile management, and health tracking features.

## Recommended Approach

### 1. Database Core Logic (`database/db.py`)
Implement the primary database interface:
- **`get_db()`**: 
  - Use Flask's `g` object to manage the connection per request.
  - Configure `sqlite3.Row` for named column access.
  - Enable `PRAGMA foreign_keys = ON` for referential integrity.
- **`init_db()`**: Create the following schema:
  - `users` table: `id` (PK), `username` (Unique), `password_hash`, `created_at`.
  - `health_logs` table: `id` (PK), `user_id` (FK), `symptom`, `severity` (int), `notes`, `logged_at`.
- **`seed_db()`**: Populate the database with a demo user and several sample health logs (e.g., "Headache", "Fatigue") to facilitate UI development.

### 2. Flask Integration (`app.py`)
Integrate the database layer into the application:
- **Connection Cleanup**: Add an `@app.teardown_appcontext` handler to close `g.db` at the end of every request.
- **Management Commands**: Register Flask CLI commands to allow easy setup from the terminal:
  - `flask init-db` $\rightarrow$ calls `init_db()`
  - `flask seed-db` $\rightarrow$ calls `seed_db()`

## Critical Files
- `database/db.py`: Core logic and schema.
- `app.py`: App lifecycle and CLI registration.
- `.claude/specs/01-database-setup.md`: Documentation of the final schema.

## Verification Plan
1. **CLI Setup**: Execute `flask init-db` and `flask seed-db`.
2. **Data Validation**: Verify via SQLite CLI that the `.db` file contains the `users` and `health_logs` tables with the expected demo data.
3. **Integration Test**: Create a temporary diagnostic route in `app.py` that queries the log count using `get_db()` to confirm the request-cycle connection management is working.
