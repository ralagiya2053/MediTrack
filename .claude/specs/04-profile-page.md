# Spec: Profile Page

## Overview
The Profile Page provides a personalized view for the logged-in user, displaying their basic account information. At this stage, it serves as the central hub for user identity within MediTrack, ensuring that users can verify they are logged into the correct account and providing a foundation for future profile management features.

## Depends on
- 01-database-setup
- 02-registration
- 03-login-and-logout

## Routes
- `GET /profile` — Displays the user's profile information (name and email) — logged-in

## Database changes
No database changes.

## Templates
- **Create:** `templates/profile.html`
- **Modify:** `templates/base.html` (to add a link to the profile page in the navigation)

## Files to change
- `app.py`

## Files to create
- `templates/profile.html`

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
- Ensure the `/profile` route redirects to `/login` if no `user_id` is present in the session.

## Definition of done
- [ ] Navigating to `/profile` while logged out redirects to `/login`.
- [ ] Navigating to `/profile` while logged in displays the user's correct name and email from the database.
- [ ] The profile page extends `base.html` and maintains a consistent design.
- [ ] A "Profile" link is visible and functional in the navigation bar of `base.html`.
- [ ] Database verification: A query for the currently logged-in user's ID in the `users` table returns exactly one row matching the displayed name and email.
