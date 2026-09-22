# MediTrack ✚

A personal health journal that helps you log symptoms, medications, and daily
vitals — then spot patterns over time and walk into your next doctor's visit
with real data instead of vague recollections.

> **Learning project.** MediTrack is being built from Claude Code to utilize all the features and workflows of it. It is not a
> medical device and does not provide diagnosis.
---
## Why MediTrack

Most people can't accurately answer "how often did you have that headache last
month?" — memory is fuzzy, and symptom diaries are tedious. MediTrack makes
logging an entry take seconds, then surfaces the patterns that a single bad
day hides.

- **Log in seconds** — symptom, severity, notes, timestamp. Nothing more.
- **See the pattern** — weekly and monthly views of frequency, intensity, and clusters.
- **Share with your doctor** — clean, dated summaries for appointments.
---
## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Flask 3.x |
| Templating | Jinja2 |
| Database | SQLite (raw `sqlite3`, no ORM) |
| Frontend | Vanilla HTML / CSS / JS |
| Testing | pytest + pytest-flask |

---
## Project Structure

- `app.py`: Main application entry point and routing.
- `database/`: Database logic and schema management.
- `static/`: CSS, JS, and image assets.
- `templates/`: Jinja2 HTML templates.
- `.claude/`: Project-specific guidance, specs, and plans.

## Current Progress
- [x] Basic landing page and static routes.
- [x] Database layer implementation:
  - `users` table for account management.
  - `health_logs` table for symptom and medication tracking.
  - `vitals` table for biometric tracking.
  - Connection management via Flask `g` object.
  - Automated database initialization and seeding on startup.
- [x] User registration flow.
- [x] User authentication and session management.
- [x] Health log entry forms and storage.
- [ ] Vitals dashboard and visualization.
- [ ] Pattern detection and summary reports.
