# Spec: DB Connection with Profile Page

## Overview
This feature connects the profile page to the database so that a logged-in
user sees their own real data — account information, recent health logs,
and vitals — instead of hardcoded placeholder values. It bridges the
authentication system and the profile UI by reading the user's id from
the session and querying the users, health_logs, and vitals tables for
that user. After this step, seeding new health_logs or vitals for a user
will immediately be reflected on their profile page.

## Depends on
- 01-database-setup
- 02-registration
- 03-login-and-logout
- 04-profile-page

## Routes
- `GET /profile` — Displays the logged-in user's account info, recent
  health logs, and vitals — logged-in only (redirect to /login if not
  authenticated)

## Database changes
No database changes. The existing users, health_logs, and vitals tables
are sufficient.

## Templates
- **Modify:** `templates/profile.html` — Replace all hardcoded placeholder
  values with data passed from the route. The page renders up to four
  sections:
    1. **User info card** — name, email, member-since date (from users)
    2. **Summary stats row** — total symptom entries, average sleep over
       the last 7 days (if any), average resting HR over the last 7 days
       (if any)
    3. **Recent health logs table** — up to 10 most recent rows, ordered
       by logged_at descending, with columns for date, symptom, severity,
       and notes
    4. **Vitals summary** — one row per metric that has data, showing the
       latest reading and its unit

## Files to change
- `app.py`
- `templates/profile.html`

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3
- Use `get_db()` inside the Flask request context (this is a route, not
  a standalone script) — do NOT use `sqlite3.connect(DATABASE)` directly,
  since `get_db()` is the canonical request-scoped connection
- Parameterised queries only — never string formatting in SQL
- Read `user_id` from `session.get("user_id")`; if absent, redirect to
  `/login`
- Query users, health_logs, and vitals filtered by that user_id
- Recent health logs: `LIMIT 10`, ordered by `logged_at DESC`
- Summary stats:
    - Total symptom entries: `COUNT(*)` from health_logs where the user
      matches
    - Average sleep (7d): average of `vitals.value` where
      `metric = 'sleep_hours'` and `logged_at >= date('now', '-7 days')`
    - Average resting HR (7d): same pattern with `metric = 'resting_hr'`
    - If a given average has no data, omit that stat (do not show zero)
- Vitals section: render only metrics that have at least one reading for
  this user. Do not display empty placeholders for metrics the user has
  not logged.
- If the user has no health logs, show a neutral empty state:
  "No entries yet." Do not use celebratory, apologetic, or reassuring
  language.
- Severity is rendered with its plain qualifier:
  1–3 → Mild, 4–6 → Moderate, 7–10 → Severe. Do not invent other labels.
- Dates rendered as YYYY-MM-DD to match the database convention.
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- No inline styles.
- Reuse existing layout classes where appropriate:
  `.auth-section`, `.auth-container`, `.auth-container--wide`,
  `.legal-card`, `.vital-panel`, `.vital-row`, `.vital-tag`.
- Category / symptom / status badges must use CSS classes, not inline
  colour styles.

## Definition of done
- [ ] Logging in and visiting `/profile` shows the correct name and
      email for the authenticated user (matches the users row for
      `session['user_id']`)
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] The page shows a summary of the user's health logs (total count
      and/or recent entries)
- [ ] If the user has seeded health_logs, at least three of them appear
      in the recent entries table, ordered most recent first
- [ ] If the user has seeded vitals, the latest reading for each metric
      the user has logged appears on the page with its correct unit
- [ ] If a metric has no readings, it does not appear on the page
      (no empty placeholder rows)
- [ ] If the user has no logs or vitals, the page renders without errors
      and shows the neutral empty state ("No entries yet.")
- [ ] No hardcoded user, log, or vitals data remains in `app.py` or
      `templates/profile.html`
- [ ] No hex colour values appear in `templates/profile.html` — only
      CSS variables
- [ ] Database verification: `SELECT * FROM users WHERE id = <session_user_id>`
      returns the row the page displays
- [ ] Database verification: `SELECT * FROM health_logs WHERE user_id = <session_user_id>
      ORDER BY logged_at DESC LIMIT 10` returns the rows shown in the
      recent entries table
- [ ] Database verification: `SELECT metric, value, unit, MAX(logged_at)
      FROM vitals WHERE user_id = <session_user_id> GROUP BY metric`
      returns the rows shown in the vitals summary