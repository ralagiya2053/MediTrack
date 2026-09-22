from app import app
from flask import url_for

with app.test_request_context():
    try:
        print(f"URL for edit_vital: {url_for('edit_vital', id=1)}")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
