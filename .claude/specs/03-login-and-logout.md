# Spec: Login and Logout

## Overview
This feature implements the authentication flow for MediTrack, allowing users to securely access their personal health journals. By introducing session management via Flask's `session` object, we can protect sensitive health data and provide a personalized experience. This is a critical step in the roadmap to transition the app from a public landing page to a private, user-centric health journal.

## Depends on

- 01 Database set up - (`users` table must exist)
- 02 Registration (`'create-user` and password hashing must be in place; a user must exist to login against)

## Routes
- `GET /login` — Display login form — public
- `POST /login` — Authenticate user and start session — public
- `GET /logout` — Terminate user session and redirect to landing — logged-in

## Database changes
No database changes.

## Templates
- **Create:**
    - `templates/login.html` (though a placeholder exists, it needs to be a full form)
- **Modify:**
    - `templates/base.html` — Add conditional navigation links (Login/Logout) based on session state.

## Files to change
- `app.py` — Implement login/logout logic and session handling.

## Files to create
- None (templates are considered part of the UI layer).

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3
- Parameterised queries only — never string formatting in SQL
- Passwords hashed with werkzeug's generate_password_hash (and verified with `check_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Reuse existing layout classes (.auth-section, .auth-container, .legal-card where appropriate)
- Slash-command scripts must use sqlite3.connect(DATABASE) from database.db — do NOT use get_db() outside a Flask request context
- health_logs rows must respect the CHECK constraints on entry_type ('symptom' or 'medication') and severity (1–10)
- vitals rows must respect the CHECK constraint on metric (sleep_hours, resting_hr, weight_kg, blood_pressure_systolic, blood_pressure_diastolic)
- Dates stored as YYYY-MM-DD strings
- Use `flask.session` to store the `user_id` upon successful login.
- Use `flask.flash` to provide feedback for failed login attempts.

## Definition of done
- [ ] User can successfully log in with valid credentials and is redirected to the profile or landing page.
- [ ] User sees an error message when attempting to log in with an invalid email or password.
- [ ] Navigation bar in `base.html` updates to show "Logout" instead of "Login" when a session is active.
- [ ] User is successfully logged out when clicking "Logout", and the session is cleared.
- [ ] Verify database state: Logged-in user's ID in `session` matches the `id` of the corresponding row in the `users` table.
