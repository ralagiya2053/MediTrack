---
description: Seed realistic dummy vitals for a specific user
argument-hint: "<user_id> <days> [metric]"
allowed-tools: Read, Bash(python3:*)
---

Read database/db.py to understand the vitals table schema, the db
connection pattern, and the database file name.

User input: $ARGUMENTS

## Step 1 — Parse arguments

Extract from $ARGUMENTS:
- user_id — integer
- days — integer, how many past days to cover
- metric — optional; one of: sleep_hours, resting_hr, weight_kg,
  blood_pressure_systolic, blood_pressure_diastolic
  If omitted, seed sleep_hours and resting_hr only.

If user_id or days is missing, or not a valid integer, stop and say:
"Usage: /seed-vitals <user_id> <days> [metric]
Examples:
  /seed-vitals 1 14
  /seed-vitals 1 14 sleep_hours"

If metric is provided but not in the allowed list, stop and say:
"Unknown metric '<metric>'. Allowed: sleep_hours, resting_hr,
weight_kg, blood_pressure_systolic, blood_pressure_diastolic."

## Step 2 — Verify user exists

Confirm the user_id exists in the users table. If not, stop and say:
"No user found with id <user_id>."

## Step 3 — Generate and insert vitals

Write and run a Python script that:

1. For each requested metric, generates one reading per day across
   the past <days> days. logged_at format: YYYY-MM-DD.

2. Metric ranges and units (values should fluctuate naturally
   day-to-day, not be constant):
   - sleep_hours: 5.5–8.5, unit 'h', one decimal place
   - resting_hr: 60–80, unit 'bpm', integer
   - weight_kg: 55–85, unit 'kg', one decimal place
   - blood_pressure_systolic: 110–135, unit 'mmHg', integer
   - blood_pressure_diastolic: 70–88, unit 'mmHg', integer

3. Use a small day-to-day walk (e.g. previous value ± small delta)
   rather than fully independent random draws, so the resulting
   series has a realistic shape when plotted.

4. Store value as REAL (not INTEGER) even for whole-number readings,
   matching the schema.

5. Opens the DB using the DATABASE constant imported from
database.db: import sqlite3; conn = sqlite3.connect(DATABASE).
Do NOT use get_db() — it requires a Flask app context.
Do not hardcode the database filename.

6. Uses parameterised queries only — no string formatting in SQL.

7. Inserts all readings in a single transaction — roll back
   everything if any insert fails.

8. Every inserted row must satisfy the CHECK constraint on metric
   (only the five allowed values above).

## Step 4 — Confirm

Print:
- How many vitals rows were inserted
- A breakdown by metric (count per metric)
- For each metric: min, max, average value
- A sample of 5 inserted records (metric, value, unit, logged_at)