# Spec: Registration

## Overview
This feature implements the user registration flow, allowing new users to create an account by providing their name, email, and password. This is a foundational step in the MediTrack roadmap, transitioning the app from a static set of landing pages to a functional personal health journal where data is associated with specific user identities.

## Depends on
- 01-database-setup

## Routes
- `GET /register` — Display the registration form — public
- `POST /register` — Process registration form and create user account — public

## Database changes
No database changes. The `users` table defined in Step 01 already contains the necessary columns (`name`, `email`, `password_hash`).

## Templates
- **Modify:** `templates/register.html` — Update the static HTML form to be a functional Flask form with proper `name` attributes and a POST method.

## Files to change
- `app.py` — Implement the `POST /register` route logic.
- `templates/register.html` — Update form for submission.

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
- [ ] Navigating to `/register` displays the registration form.
- [ ] Submitting the form with valid data redirects the user (e.g., to login or landing) and shows a success message.
- [ ] Attempting to register with an email that already exists in the database results in a clear error message.
- [ ] Password submitted via the form is stored as a hash in the database, not as plain text.
- [ ] Database verification: The row count in the `users` table increases by 1 after a successful registration.
