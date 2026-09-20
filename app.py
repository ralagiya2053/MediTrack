from flask import Flask, render_template

app = Flask(__name__)


# ------------------------------------------------------------------ #
# Public routes                                                       #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


# ------------------------------------------------------------------ #
# Placeholder routes — filled in as the course progresses             #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/logs/add")
def add_log():
    return "Add health log — coming in Step 7"


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