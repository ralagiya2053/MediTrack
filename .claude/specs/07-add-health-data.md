# Spec: Add Health Log

## Overview
This feature implements the functionality for users to add new health logs (symptoms or medications) to their journal. This is a critical part of the MediTrack roadmap, moving from a read-only profile view to an interactive health journal where users can actively track their health patterns.

## Depends on
- 01-database-setup
- 03-login-and-logout
- 05-db-connection-with-profile-page

## Routes
- `GET /logs/add` — Displays the form to add a new health log — logged-in
- `POST /logs/add` — Processes and saves the new health log to the database — logged-in

## Database changes
No database changes.

## Templates
- **Create:** `templates/add_log.html`
- **Modify:** `templates/base.html` (if navigation needs updating to link to the add log page)

## Files to change
- `app.py`

## Files to create
- `templates/add_log.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3
- Parameterised queries only — never string formatting in SQL
- Passwords hashed with werkzeug's generate_password_hash
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Reuse existing layout classes (.auth-section, .auth-container, .legal-card where appropriate)
- Slash-command scripts must use sqlite3.connect(DATABASE) from database.db — do NOT use get_db() outside a Flask request context
- health_logs rows must respect the CHECK constraints on entry_type ('symptom' or 'medication') and severity (1–10)
- vitals rows must respect the CHECK constraint on metric (sleep_hours, resting_hr, weight_kg, blood_pressure_systolic, blood_pressure_diastolic)
- Dates stored as YYYY-MM-DD strings

## Definition of done
- [ ] `GET /logs/add` renders a form with fields for entry type (symptom/medication), symptom name (if applicable), severity (1-10), notes, and date.
- [ ] `POST /logs/add` correctly validates inputs and inserts a record into the `health_logs` table for the current `session["user_id"]`.
- [ ] Attempting to submit a severity outside 1-10 results in a validation error.
- [ ] Attempting to submit an invalid entry type results in a validation error.
- [ ] After successful submission, the user is redirected to the profile page with a success flash message.
- [ ] Database verification: Row count in `health_logs` increases by 1 after a successful submission.
