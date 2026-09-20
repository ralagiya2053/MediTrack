Spec Document — Step 1: Database Setup

## 1. Overview
Replace the stub in database/db.py with a working SQLite implementation. This step establishes the data layer foundation for the MediTrack application. All future features (authentication, profile, health-log tracking, vitals tracking, dashboard, pattern detection) depend on this being correctly implemented.

## 2. Depends on
Nothing — this is the first step.

## 3. Routes
No new routes.

Existing placeholder routes in app.py remain unchanged.

## 4. Database Schema
A. users

Column	Type	Constraints
id	INTEGER	Primary key, autoincrement
name	TEXT	Not null
email	TEXT	Unique, not null
password_hash	TEXT	Not null
created_at	TEXT	Default datetime('now')
B. health_logs

Stores user-reported symptoms and medications.

Column	Type	Constraints
id	INTEGER	Primary key, autoincrement
user_id	INTEGER	Foreign key → users.id, not null
entry_type	TEXT	Not null, CHECK IN ('symptom','medication')
symptom	TEXT	Not null when entry_type='symptom' (from fixed list, section 10)
severity	INTEGER	Nullable, CHECK between 1 and 10 when present
notes	TEXT	Nullable
logged_at	TEXT	Not null (YYYY-MM-DD format)
created_at	TEXT	Default datetime('now')
C. vitals

Stores numeric readings like sleep hours, resting HR, blood pressure.

Column	Type	Constraints
id	INTEGER	Primary key, autoincrement
user_id	INTEGER	Foreign key → users.id, not null
metric	TEXT	Not null, CHECK IN ('sleep_hours','resting_hr','weight_kg','blood_pressure_systolic','blood_pressure_diastolic')
value	REAL	Not null
unit	TEXT	Not null (e.g. 'h', 'bpm', 'kg', 'mmHg')
logged_at	TEXT	Not null (YYYY-MM-DD format)
created_at	TEXT	Default datetime('now')

## 5. Functions to Implement (database/db.py)
A. get_db()

Opens a connection to meditrack.db in the project root.

Sets:

row_factory = sqlite3.Row

PRAGMA foreign_keys = ON

Returns the connection.

B. init_db()

Creates all three tables using CREATE TABLE IF NOT EXISTS.

Safe to call multiple times.

Ensures schema is ready before app usage.

C. seed_db()

Checks if users table already contains data.

If yes → return early (no duplication).

Inserts one demo user:

name: Demo User

email: demo@meditrack.com

password: demo123 (hashed using Werkzeug)

Inserts 8 sample health logs (symptoms):

All linked to the demo user.

Cover multiple symptoms from the fixed list (section 10).

Dates spread across the current month.

Severity values varied across the 1–10 range.

At least two entries should include free-text notes.

Inserts 4 sample vitals (numeric readings):

Sleep hours for 4 different days, values around 6.5–7.5.

Resting HR for 4 different days, values around 62–72 bpm.

Dates spread across the current month.

Values should reflect the mock hero panel (see section 10b for target values).

## 6. Changes to app.py
Import:

get_db

init_db

seed_db

Call init_db() and seed_db() inside app.app_context() on startup.

Ensure the DB is ready before routes are used.

## 7. Files to Change
database/db.py → implement all functions.

app.py → add imports and startup calls.

## 8. Files to Create
None.

## 9. Dependencies
No new pip packages.

Use:

sqlite3 (standard library)

werkzeug.security (already installed)

## 10. Fixed Lists
10a. Symptoms (values for health_logs.symptom):

Headache

Fatigue

Nausea

Fever

Cough

Sore Throat

Muscle Pain

Other

Severity scale reference (convention, enforced as CHECK 1–10):

Value	Meaning
1–3	Mild
4–6	Moderate
7–10	Severe

10b. Vitals metrics (values for vitals.metric) with canonical units:

Metric	Unit	Plausible range
sleep_hours	h	0–24
resting_hr	bpm	30–200
weight_kg	kg	20–300
blood_pressure_systolic	mmHg	60–250
blood_pressure_diastolic	mmHg	30–150
Important: the seed data must produce a hero panel that matches what the landing page shows today. Target values for the demo user's last 7 days:

Headache: 3 episodes → 3 symptom rows with symptom='Headache'

Sleep: 7.2 h/night average → 4 vitals rows averaging ~7.2

Resting HR: 68 bpm average → 4 vitals rows averaging ~68

Fatigue: 5/10 → 1 symptom row with symptom='Fatigue', severity=5

This keeps the marketing mock and the database in agreement — when you eventually wire the real dashboard, it will produce the same view the landing page promises.

## 11. Rules for Implementation
No ORMs (no SQLAlchemy).

Use parameterized queries only.

Never use string formatting in SQL.

Enable PRAGMA foreign_keys = ON on every connection.

Store severity as INTEGER (not TEXT).

Store vitals value as REAL (not INTEGER — sleep can be 7.2).

Hash passwords using:
from werkzeug.security import generate_password_hash

seed_db() must prevent duplicate inserts.

Dates must follow YYYY-MM-DD format consistently.

Use CHECK constraints for enum-like columns (entry_type, metric, severity).

Do not enforce severity on medication rows — leave it NULL for those.

## 12. Expected Behavior
get_db() returns a working connection with:

dictionary-like row access

foreign key enforcement enabled

init_db():

creates tables safely

does not fail on repeated runs

seed_db():

inserts demo data only once

does not duplicate records on multiple runs

Database enforces:

unique email constraint

valid foreign key relationships

valid entry_type values

valid metric values

severity between 1 and 10

## 13. Error Handling Expectations
Inserting duplicate email → fails (UNIQUE constraint).

Inserting a health log with invalid user_id → fails (foreign key constraint).

Inserting entry_type='invalid' → fails (CHECK constraint).

Inserting severity=15 → fails (CHECK constraint).

Inserting metric='invalid' → fails (CHECK constraint).

Invalid queries → raise clear errors for debugging.

## 14. Definition of Done
□ Database file (meditrack.db) is created on app startup.
□ All three tables (users, health_logs, vitals) exist with correct schema and constraints.
□ Demo user exists with hashed password.
□ 8 sample health logs exist across symptoms.
□ 4 sample vitals exist (sleep + resting HR).
□ Severity values span the 1–10 range.
□ At least two logs include non-null notes.
□ No duplicate seed data on repeated runs.
□ App starts without errors.
□ Foreign key enforcement works (test with a bad user_id).
□ CHECK constraints work (test with severity=15 and metric='invalid').
□ All queries use parameterized SQL.