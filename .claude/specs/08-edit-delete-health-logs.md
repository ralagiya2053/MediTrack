# Spec: Edit and Delete Health Data

## Overview
This feature lets logged-in users edit or delete any health entry they
have previously added — whether it's a symptom entry (health_logs) or
a vital reading (vitals). It completes the CRUD lifecycle for both
tables and is the first step where ownership checks matter: a user
must only be able to edit or delete their own records.

## Depends on
- 05-db-connection-with-profile-page
- 07-add-health-data

## Routes
- `GET  /logs/<int:id>/edit`    — render edit form for a health_log — logged-in only
- `POST /logs/<int:id>/edit`    — persist health_log update — logged-in only
- `GET  /logs/<int:id>/delete`  — delete a health_log, redirect back — logged-in only
- `GET  /vitals/<int:id>/edit`   — render edit form for a vital — logged-in only
- `POST /vitals/<int:id>/edit`   — persist vital update — logged-in only
- `GET  /vitals/<int:id>/delete` — delete a vital, redirect back — logged-in only

Logged-out users hitting any of these must be redirected to `/login`.

Note on GET-for-delete: this app uses GET to trigger deletes, matching
the tutor's pattern. This is technically incorrect (GET should be
idempotent and safe) and opens a CSRF risk. A future step will convert
these to POST-with-form. For now, match the existing pattern; do NOT
introduce POST deletes in this step — the placeholder routes in app.py
already declare GET.

## Database changes
No database changes.

## Templates
- **Create:** `templates/edit_log.html` — edit form for a health_log
- **Create:** `templates/edit_vital.html` — edit form for a vital
- **Modify:** `templates/profile.html` — in the "Recent Health Logs"
  section, add Edit and Delete controls to each row; in the "Vitals"
  section, add Edit and Delete controls to each metric row
- **Modify:** `static/css/style.css` — add small `.row-actions`,
  `.row-action`, and `.row-action--danger` classes (in the existing
  section for profile-related styles, before Responsive)

## Files to change
- `app.py`
- `templates/profile.html`
- `static/css/style.css`

## Files to create
- `templates/edit_log.html`
- `templates/edit_vital.html`

## New dependencies
No new dependencies.

## Rules for implementation

### General
- No SQLAlchemy or ORMs — use raw sqlite3
- Use `get_db()` inside the request context
- Parameterised queries only — never string formatting in SQL
- All templates extend `base.html`
- No inline styles
- Use CSS variables — never hardcode hex values
- Reuse existing classes where possible: `.auth-section`,
  `.auth-container`, `.auth-card`, `.form-group`, `.form-input`,
  `.btn-submit`, `.auth-error`, `.vital-row`, `.vital-tag`

### Ownership (critical)
Every query — read, update, delete — must include `AND user_id = ?`
with `session['user_id']` as the value. Never trust the `id` in the
URL alone.

- For GET edit: `SELECT ... FROM health_logs WHERE id = ? AND user_id = ?`.
  If no row: `abort(404)`.
- For POST edit: `UPDATE health_logs SET ... WHERE id = ? AND user_id = ?`.
  If `cursor.rowcount == 0`: `abort(404)`.
- For GET delete: `DELETE FROM health_logs WHERE id = ? AND user_id = ?`.
  If `cursor.rowcount == 0`: `abort(404)`.

Same pattern for the vitals routes, against the `vitals` table.

A user must NEVER be able to read, edit, or delete another user's
records by guessing IDs. This is the highest-severity security concern
of this step and the security reviewer will specifically look for it.

### Edit form — health_log
The edit form posts to `/logs/<id>/edit` and contains the same fields
as the add form's symptom mode, but for one existing entry:

| Field | Type | Required | Notes |
|---|---|---|---|
| symptom | select | yes | Same eight fixed values as step 07 |
| severity | number input | yes | Integer 1–10 |
| notes | textarea | no | Max 500 chars after trim |
| logged_at | date input | yes | YYYY-MM-DD, not in the future |

The form is pre-populated with the row's current values. The
`entry_type` field is NOT editable — symptom entries stay symptom
entries.

Validation rules match step 07 exactly. On validation failure:
re-render `edit_log.html` with input preserved and a flash error.

On success: `flash('Entry updated.', 'success')` and redirect to
`url_for('profile')`.

### Edit form — vital
The edit form posts to `/vitals/<id>/edit` and contains:

| Field | Type | Required | Notes |
|---|---|---|---|
| metric | select | yes | Same five fixed metrics as step 07 |
| value | number input (step=0.1) | yes | Range depends on metric |
| unit | read-only text | yes | Auto-set from metric |
| logged_at | date input | yes | YYYY-MM-DD, not in the future |

Validation rules match step 07's vital mode. The unit is derived from
metric server-side — never trust the form value.

On success: `flash('Vital updated.', 'success')` and redirect to
`url_for('profile')`.

### Delete flow
`GET /logs/<id>/delete` and `GET /vitals/<id>/delete` perform the
delete directly — no confirmation page. After a successful delete:

    flash('Entry deleted.', 'success')
    return redirect(url_for('profile'))

If the row doesn't exist or doesn't belong to the current user:
`abort(404)`.

Note: for this step, no browser-side confirmation dialog is required.
A future step can add a `confirm()` or a modal. The `.row-action--danger`
class should still visually distinguish the delete control in red.

### Profile page — action controls
In the "Recent Health Logs" section, each row gets two small actions
on the right:

    Edit   Delete

In the "Vitals" section, each metric row gets the same two actions:

    Edit   Delete

Both use the new `.row-action` class. The Delete control additionally
gets `.row-action--danger`. They render as small links
(`<a href="...">`), not buttons — since both actions are navigation,
not form submission.

The Edit link points at `url_for('edit_log', id=log.id)` or
`url_for('edit_vital', id=vital.id)` as appropriate. The Delete link
points at `url_for('delete_log', id=log.id)` or
`url_for('delete_vital', id=vital.id)`.

Icons are optional. If used, follow the meditrack-ui-designer skill
(pencil for edit, trash-2 for delete).

### Health-domain language
- Success messages are neutral: "Entry updated." / "Entry deleted."
- Never apologize ("Oops, something went wrong"), never celebrate
  ("Nice work!"), never reassure ("All good now!").
- 404 responses follow Flask's default — no custom error page is
  required in this step.

## Definition of done

**Authorization**
- [ ] Logged-out user visiting any of the six routes redirects to
      `/login`
- [ ] Logged-in user A cannot GET `/logs/<id>/edit` for a health_log
      belonging to user B — returns 404
- [ ] Logged-in user A cannot POST to `/logs/<id>/edit` for a
      health_log belonging to user B — returns 404, no DB write
- [ ] Logged-in user A cannot GET `/logs/<id>/delete` for a
      health_log belonging to user B — returns 404, no DB delete
- [ ] Same three checks apply to the vitals routes
- [ ] Database verification: after user A attempts to delete user B's
      log and receives 404, `SELECT COUNT(*) FROM health_logs WHERE
      id = <b_log_id>` is still 1

**Edit — health_log**
- [ ] Visiting `/logs/<id>/edit` renders a form pre-populated with the
      row's symptom, severity, notes, and logged_at
- [ ] Submitting a valid edit updates exactly one row
- [ ] The updated values appear on `/profile` after redirect
- [ ] Submitting severity 0 or 11 shows the validation message and
      does not update the row
- [ ] Submitting a future date shows the date validation message and
      does not update the row
- [ ] Submitting notes >500 chars shows the notes validation message
      and does not update the row
- [ ] A success flash "Entry updated." appears on `/profile`
- [ ] The `entry_type` field is not user-editable in the form

**Edit — vital**
- [ ] Visiting `/vitals/<id>/edit` renders a form pre-populated with
      the row's metric, value, unit, and logged_at
- [ ] Submitting a valid edit updates exactly one row
- [ ] The updated value appears on `/profile` after redirect
- [ ] Submitting a value out of the metric's plausible range shows a
      validation message and does not update the row
- [ ] Submitting a spoofed `unit` field via browser devtools does NOT
      affect the stored unit (server derives it from metric)
- [ ] A success flash "Vital updated." appears on `/profile`

**Delete — health_log**
- [ ] Clicking Delete on a row removes exactly that row
- [ ] After delete, the row no longer appears on `/profile`
- [ ] A success flash "Entry deleted." appears on `/profile`
- [ ] Database verification: `SELECT COUNT(*) FROM health_logs WHERE
      user_id = <uid>` decreases by exactly 1 after one successful
      delete

**Delete — vital**
- [ ] Clicking Delete on a vitals row removes exactly that row
- [ ] After delete, the row no longer appears on the Vitals section
- [ ] A success flash "Entry deleted." appears on `/profile`
- [ ] Database verification: `SELECT COUNT(*) FROM vitals WHERE
      user_id = <uid>` decreases by exactly 1 after one successful
      delete

**UI**
- [ ] Edit and Delete controls appear on every health log row and
      every vitals row
- [ ] Delete controls use `.row-action--danger` and appear visually
      distinct from Edit controls
- [ ] No hardcoded hex values added to `edit_log.html`,
      `edit_vital.html`, or new CSS
- [ ] No new pip packages

**Cross-checks**
- [ ] Editing a symptom never touches `vitals`, and editing a vital
      never touches `health_logs`
- [ ] Deleting a health_log does not affect vitals for the same user,
      and vice versa