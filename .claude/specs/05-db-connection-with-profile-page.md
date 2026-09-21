# Spec: DB Connection with Profile Page

## Overview
This feature ensures that the profile page is fully integrated with the database, allowing logged-in users to view their own personalized account details. It bridges the gap between the authentication system and the user interface by fetching the current user's information from the `users` table using the session ID.

## Depends on
- 01-database-setup
- 02-registration
- 03-login-and-logout
- 04-profile-page

## Routes
- `GET /profile` — Displays the logged-in user's name and email — logged-in

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` — Ensure it correctly displays the `user` object passed from the route.

## Files to change
- `app.py`
- `templates/profile.html`

## Files to create
No new files.

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
- [ ] Logging in and navigating to `/profile` displays the correct name and email for the authenticated user.
- [ ] Accessing `/profile` without being logged in redirects the user to the login page.
- [ ] Database verification: A `SELECT` query for the `user_id` in the session returns the expected row from the `users` table.
