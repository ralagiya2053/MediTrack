from flask import Flask, render_template, g, request, redirect, url_for, flash, session
from database.db import get_db, init_db, seed_db
import sqlite3
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

with app.app_context():
    init_db()
    seed_db()

# ------------------------------------------------------------------ #
# Public routes                                                       #
# ------------------------------------------------------------------ #

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")

        hashed_password = generate_password_hash(password)
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="An account with this email already exists.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.")
            return redirect(url_for("login"))

        db = get_db()
        user = db.execute(
            "SELECT id, password_hash FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            flash("Welcome back!", "success")
            return redirect(url_for("profile"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")


@app.route("/analytics")
def analytics():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("analytics.html")


# ------------------------------------------------------------------ #
# Placeholder routes — filled in as the course progresses             #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Date filter logic
    filter_val = request.args.get("filter", "all")
    today = date.today()

    filter_days = {"7": 7, "14": 14, "30": 30}
    days = filter_days.get(filter_val)

    if days:
        start_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
    else:
        start_date = "1900-01-01"

    db = get_db()
    user = db.execute(
        "SELECT name, email, created_at FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    vitals = db.execute(
        "SELECT metric, value, unit, logged_at FROM vitals WHERE user_id = ? AND logged_at >= ? ORDER BY logged_at DESC",
        (session["user_id"], start_date)
    ).fetchall()

    logs = db.execute(
        "SELECT symptom, severity, logged_at, notes FROM health_logs WHERE user_id = ? AND logged_at >= ? ORDER BY logged_at DESC",
        (session["user_id"], start_date)
    ).fetchall()

    return render_template("profile.html", user=user, vitals=vitals, logs=logs, current_filter=filter_val)


@app.route("/logs/add", methods=["GET", "POST"])
def add_log():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    if request.method == "POST":
        entry_type = request.form.get("entry_type")
        symptom = request.form.get("symptom")
        severity = request.form.get("severity")
        notes = request.form.get("notes")
        logged_at = request.form.get("logged_at")

        # Validation
        if not entry_type or not logged_at:
            flash("Entry type and date are required.", "error")
            return redirect(url_for("add_log"))

        if entry_type not in ('symptom', 'medication', 'health_log', 'vitals'):
            flash("Invalid entry type.", "error")
            return redirect(url_for("add_log"))

        # Convert severity to int if present, otherwise None
        try:
            severity_int = int(severity) if severity else None
            if severity_int is not None and not (1 <= severity_int <= 10):
                raise ValueError()
        except ValueError:
            flash("Severity must be a number between 1 and 10.", "error")
            return redirect(url_for("add_log"))

        db = get_db()
        try:
            if entry_type == 'vitals':
                # Vitals are stored in a separate table
                metric = symptom
                value = severity_int if severity_int else 0.0
                unit = 'unit' # Placeholder

                db.execute(
                    "INSERT INTO vitals (user_id, metric, value, unit, logged_at) VALUES (?, ?, ?, ?, ?)",
                    (session["user_id"], metric, value, unit, logged_at)
                )
            else:
                db_entry_type = 'symptom' if entry_type == 'health_log' else entry_type
                db.execute(
                    "INSERT INTO health_logs (user_id, entry_type, symptom, severity, notes, logged_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (session["user_id"], db_entry_type, symptom, severity_int, notes, logged_at)
                )
            db.commit()
            flash("Health log added successfully!", "success")
            return redirect(url_for("profile"))
        except sqlite3.Error as e:
            flash(f"An error occurred while saving: {e}", "error")
            return redirect(url_for("add_log"))

    return render_template("add_log.html", date=date)


@app.route("/logs/<int:id>/edit")
def edit_log(id):
    return "Edit health log — coming in Step 8"


@app.route("/logs/<int:id>/delete")
def delete_log(id):
    return "Delete health log — coming in Step 9"


@app.route("/vitals")
def vitals():
    return "Vitals dashboard — the MediTrack extension"


if __name__ == "__main__":
    app.run(debug=True, port=5001)