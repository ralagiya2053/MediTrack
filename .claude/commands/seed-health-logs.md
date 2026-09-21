---
description: Seed realistic dummy health logs for a specific user
argument-hint: "<user_id> <count> <days>"
allowed-tools: Read, Bash(python3:*)
---

Read database/db.py to understand the health_logs table schema, the
db connection pattern, and the DATABASE constant.

Note: get_db() in db.py uses Flask's g object, which requires an
application context. Since this command runs outside Flask, open a
direct sqlite3 connection using the DATABASE constant from db.py.
Do NOT hardcode the filename.

User input: $ARGUMENTS

## Step 1 — Parse arguments

Extract from $ARGUMENTS:
- user_id — integer
- count — integer, number of health logs to create
- days — integer, how many past days to spread them across

If any argument is missing or not a valid integer, stop and say:
"Usage: /seed-log <user_id> <count> <days>
Example: /seed-log 1 20 14"

## Step 2 — Verify user exists

Before generating anything, confirm the user_id exists in the
users table. If not, stop and say:
"No user found with id <user_id>."

## Step 3 — Generate and insert health logs

Write and run a Python script that:

1. Spreads logged_at dates randomly across the past <days> days.
   Format: YYYY-MM-DD.

2. Uses only these symptoms (from the fixed list):
   Headache, Fatigue, Nausea, Fever, Cough, Sore Throat, Muscle Pain, Other

3. Generates severity values STRICTLY within 1–10 inclusive.
   Distribution:
   - 60% of entries: severity in [1, 2, 3]
   - 30% of entries: severity in [4, 5, 6]
   - 10% of entries: severity in [7, 8, 9, 10]
   Never generate 0, 11, or any value outside 1–10.

4. Symptom frequency should be roughly proportional:
   - Headache and Fatigue most common
   - Fever, Nausea least common
   - Others fill the middle

5. Free-text notes:
   - ~40% of entries include a short realistic note
   - The rest have NULL notes

6. ALWAYS set entry_type = 'symptom' and ALWAYS set a non-null
   symptom value for every row. Never insert a symptom row with
   symptom = NULL.

7. Open the DB using the DATABASE constant imported from
   database.db. Use `import sqlite3` and `sqlite3.connect(DATABASE)`.
   Do not use get_db() — it requires a Flask app context.

8. Use parameterised queries only — no string formatting in SQL.

9. Insert all logs in a single transaction — roll back everything
   if any insert fails. Catch sqlite3.IntegrityError and print a
   clear message.

10. Before committing, assert that every generated severity is
    within 1–10 and every symptom is non-null. If not, raise and
    roll back — do not commit invalid data.

## Step 4 — Confirm

Print:
- How many health logs were inserted
- The date range they span
- A breakdown by symptom (count per symptom)
- A sample of 5 inserted records (symptom, severity, logged_at, notes)