# CLAUDE.md - MediTrack Project Guide

## Project Overview
MediTrack is a personal health journal designed to log symptoms, medications, and daily vitals to help users identify health patterns over time.

## Tech Stack
- **Backend:** Flask 3.x
- **Database:** SQLite (raw `sqlite3`, no ORM)
- **Templating:** Jinja2
- **Frontend:** Vanilla HTML/CSS/JS
- **Testing:** pytest + pytest-flask

## Development Standards
- **Code Style:** PEP 8 for Python.
- **Database Access:**
  - No ORMs; use parameterized queries only.
  - Connection management handled via Flask's `g` object.
  - `PRAGMA foreign_keys = ON` must be enabled on every connection.
  - Connection is closed via `@app.teardown_appcontext`.
- **Schema Design:**
  - `users`: Basic identity and authentication (Step 02: Registration).
  - `health_logs`: Symptom and medication tracking with severity checks (1-10).
  - `vitals`: Numeric reading tracking (sleep, HR, weight, etc.).

## Common Commands
- **Run App:** `python app.py`
- **Initialize DB:** `flask init-db` (if CLI command is present) or handled automatically at startup.
- **Seed DB:** `flask seed-db` (if CLI command is present) or handled automatically at startup.

## Project Structure
- `app.py`: Main application entry point and route definitions.
- `database/db.py`: Database connection logic, schema definitions, and seeding.
- `.claude/specs/`: Detailed specifications for each implementation step.
- `.claude/plans/`: Implementation plans for approved features.
