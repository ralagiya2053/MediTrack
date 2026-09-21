---
description: Create a single dummy user in the MediTrack database
allowed-tools: Read, Bash(python3:*)
---

Read database/db.py to understand the users table schema and the
DATABASE constant.

Then write and run a Python script using Bash that:

1. Generates a realistic random user using your own knowledge
   of common names across regions:
   - Name: a realistic Indian first + last name
   - Email: derived from the name with a random 2-3 digit number suffix
     (e.g. ananya.iyer47@gmail.com)
   - Password: "password123" hashed with werkzeug's
     generate_password_hash
   - created_at: current datetime

2. Checks if the generated email already exists in the users table.
   If it does, regenerate until unique.

3. Opens the DB using the DATABASE constant from db.py:
import sqlite3; conn = sqlite3.connect(DATABASE).
Do NOT use get_db() — it requires a Flask app context.
Use parameterised queries only.

4. Prints confirmation:
   - id
   - name
   - email