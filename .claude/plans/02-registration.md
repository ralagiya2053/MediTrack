 Implementation Plan: User Registration

 Context

 The MediTrack app currently consists of static landing pages and a database schema. To make the app functional, we need a way for users to create accounts. This plan implements the registration flow, allowing users to sign up with a name, email, and password, which are then stored securely in the users table.

 Critical Files

 - app.py: Implement POST /register route logic.
 - templates/register.html: Ensure the registration form is correctly wired for POST submission.
 - database/db.py: Reuse get_db() for database connectivity.

 Implementation Steps

 1. Update templates/register.html

 - Verify the <form> element has method="POST" and action="/register".
 - Ensure input fields have correct name attributes: name="name", name="email", and name="password".
 - Ensure there is a placeholder/block to display error messages passed from the Flask route.

 2. Implement POST /register in app.py

 - Modify the @app.route("/register") to accept POST methods: @app.route("/register", methods=["GET", "POST"]).
 - POST Logic:
   - Extract name, email, and password from request.form.
   - Hash the password using werkzeug.security.generate_password_hash.
   - Use get_db() to obtain a connection.
   - Execute the insertion: INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?) using parameterized queries.
   - Error Handling: Wrap the DB call in a try...except sqlite3.IntegrityError block to catch duplicate emails.
   - Response:
     - On error: Re-render register.html with a specific error message.
     - On success: Redirect to /login with a success notification.

 Verification Plan

 - Success Path:
   - Register a new user with a unique email.
   - Verify redirection to /login.
   - Verify the users table row count increased by 1.
 - Duplicate Email Path:
   - Attempt to register again with the same email.
   - Verify the user stays on /register and sees the "account with this email already exists" error.
 - Security Check:
   - Inspect the users table in meditrack.db to confirm the password_hash is encrypted and not stored in plain text.