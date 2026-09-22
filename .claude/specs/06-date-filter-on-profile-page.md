# Spec: Date Filter on Profile Page

## Overview
Currently, the profile page displays a hard-coded limit of the 5 most recent health logs and vitals for the logged-in user. As the user's health journal grows, this limited view becomes insufficient. This feature introduces date-based filtering, allowing users to view their health data within a specific time range (e.g., last 7 days, last 30 days, or a custom range), helping them identify patterns and trends over time.

## Depends on
- 05-db-connection-with-profile-page

## Routes
No new routes. The existing `/profile` route will be modified to handle filter parameters.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/profile.html` - Add a filter UI (dropdown or date inputs) and update the data display to reflect the filtered results.

## Files to change
- `app.py` - Update the `/profile` route to extract filter parameters from the request and apply them to the SQL queries.
- `templates/profile.html` - Add the filtering interface.

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
- Use `request.args.get()` to retrieve filter parameters (e.g., `start_date`, `end_date`).
- Default view should remain "Last 30 Days" or "All Time" if no filter is specified, but the "Last 5" limit should be replaced by the date filter.

## Definition of done
- [ ] The profile page displays a filter UI (e.g., a dropdown for "Last 7 Days", "Last 30 Days", "All Time").
- [ ] Selecting a filter updates the list of vitals and health logs displayed.
- [ ] The SQL queries in `/profile` use `WHERE logged_at BETWEEN ? AND ?` (or similar) based on the selected filter.
- [ ] Verifiable database state: when a filter for "Last 7 Days" is active, only rows with `logged_at` within the last 7 days are returned from the database.
- [ ] The page handles cases where no data exists for the selected date range gracefully (e.g., "No logs found for this period").
