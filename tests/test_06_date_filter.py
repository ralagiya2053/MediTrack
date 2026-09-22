import pytest
from app import app as flask_app
from database.db import init_db
import sqlite3
from datetime import date, timedelta

@pytest.fixture
def app(tmp_path, monkeypatch):
    # Use a temp file DB so PRAGMA foreign_keys and file-based
    # connections behave the same as production
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("database.db.DATABASE", str(db_path))
    flask_app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
    })
    with flask_app.app_context():
        init_db()
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seeded_user(app):
    """Insert a single user directly and return their id."""
    import database.db
    conn = sqlite3.connect(database.db.DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Test User", "test@example.com", "hashed")
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

@pytest.fixture
def auth_client(client, seeded_user):
    """A test client already logged in as the seeded user."""
    with client.session_transaction() as sess:
        sess['user_id'] = seeded_user
    return client

@pytest.fixture
def seeded_data(seeded_user):
    """
    Insert health logs and vitals with specific dates to test filtering.
    Dates are relative to today.
    """
    import database.db
    conn = sqlite3.connect(database.db.DATABASE)
    today = date.today()

    # Dates: 2 days ago (within all), 10 days ago (within 14/30), 40 days ago (only All)
    dates = {
        "recent": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        "mid": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
        "old": (today - timedelta(days=40)).strftime("%Y-%m-%d"),
    }

    # Health Logs
    logs = [
        (seeded_user, 'symptom', 'Headache', 3, 'Recent', dates["recent"]),
        (seeded_user, 'symptom', 'Fatigue', 5, 'Mid', dates["mid"]),
        (seeded_user, 'symptom', 'Nausea', 2, 'Old', dates["old"]),
    ]
    conn.executemany(
        "INSERT INTO health_logs (user_id, entry_type, symptom, severity, notes, logged_at) VALUES (?, ?, ?, ?, ?, ?)",
        logs
    )

    # Vitals
    vitals = [
        (seeded_user, 'sleep_hours', 8.0, 'h', dates["recent"]),
        (seeded_user, 'sleep_hours', 7.0, 'h', dates["mid"]),
        (seeded_user, 'sleep_hours', 6.0, 'h', dates["old"]),
    ]
    conn.executemany(
        "INSERT INTO vitals (user_id, metric, value, unit, logged_at) VALUES (?, ?, ?, ?, ?)",
        vitals
    )

    conn.commit()
    conn.close()
    return dates

class TestDateFilter:
    def test_profile_auth_guard(self, client):
        """Ensure /profile redirects to /login if the user is not logged in."""
        response = client.get("/profile")
        assert response.status_code == 302
        assert "/login" in response.location

    def test_filter_all_returns_everything(self, auth_client, seeded_data):
        """Verify that ?filter=all returns all records."""
        response = auth_client.get("/profile?filter=all")
        assert response.status_code == 200
        # Should see all 3 logs and 3 vitals
        assert b"Recent" in response.data
        assert b"Mid" in response.data
        assert b"Old" in response.data
        assert b"8.0" in response.data
        assert b"7.0" in response.data
        assert b"6.0" in response.data

    def test_filter_7_days(self, auth_client, seeded_data):
        """Verify that ?filter=7 returns only records from the last 7 days."""
        response = auth_client.get("/profile?filter=7")
        assert response.status_code == 200
        assert b"Recent" in response.data
        assert b"Mid" not in response.data
        assert b"Old" not in response.data
        assert b"8.0" in response.data
        assert b"7.0" not in response.data
        assert b"6.0" not in response.data

    def test_filter_14_days(self, auth_client, seeded_data):
        """Verify that ?filter=14 returns records from the last 14 days."""
        response = auth_client.get("/profile?filter=14")
        assert response.status_code == 200
        assert b"Recent" in response.data
        assert b"Mid" in response.data
        assert b"Old" not in response.data
        assert b"8.0" in response.data
        assert b"7.0" in response.data
        assert b"6.0" not in response.data

    def test_filter_30_days(self, auth_client, seeded_data):
        """Verify that ?filter=30 returns records from the last 30 days."""
        response = auth_client.get("/profile?filter=30")
        assert response.status_code == 200
        assert b"Recent" in response.data
        assert b"Mid" in response.data
        assert b"Old" not in response.data
        assert b"8.0" in response.data
        assert b"7.0" in response.data
        assert b"6.0" not in response.data

    def test_empty_state_graceful_handling(self, auth_client):
        """Verify that the page handles cases with no data in the selected range gracefully."""
        # No data seeded for this user in this specific test (seeded_data fixture not used)
        response = auth_client.get("/profile?filter=7")
        assert response.status_code == 200
        # The spec says: "No logs found for this period"
        assert b"No logs found" in response.data or b"No vitals found" in response.data or b"empty" in response.data.lower()

    def test_invalid_filter_defaults_to_all(self, auth_client, seeded_data):
        """Verify that an invalid filter value (e.g., ?filter=999) defaults to All Time."""
        response = auth_client.get("/profile?filter=999")
        assert response.status_code == 200
        assert b"Recent" in response.data
        assert b"Mid" in response.data
        assert b"Old" in response.data

    def test_ui_filter_dropdown_and_selection(self, auth_client):
        """Verify the filter dropdown is present and the current selection is marked as selected."""
        # Test for "7 days" selection
        response = auth_client.get("/profile?filter=7")
        assert response.status_code == 200
        # Check if dropdown exists (usually <select name="filter"> or similar)
        assert b'name="filter"' in response.data or b'id="filter"' in response.data
        # Check if the "7" option is selected
        assert b'value="7"' in response.data
        assert b'selected' in response.data
