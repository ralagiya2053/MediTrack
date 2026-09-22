---
description: Runs parallel security and quality code review for a specific MediTrack feature. Pass the spec name as argument e.g. /code-review-feature 03-login-and-logout
allowed-tools: Bash
---

Run the full code review pipeline for the feature specified in
$ARGUMENTS.

If no argument is provided, stop immediately and say:
"Please provide a spec name. Usage: /code-review-feature <spec-name>
e.g. /code-review-feature 03-login-and-logout"

If `.claude/specs/$ARGUMENTS.md` does not exist, stop immediately and
say:
"Spec file not found at .claude/specs/$ARGUMENTS.md. Please check the
spec name and try again."

---

## Pre-flight Check

Before invoking any subagents, collect the diff:
- Run `git diff` for unstaged changes
- Run `git diff --staged` for staged changes
- Combine both into a single diff

If both are empty, stop immediately and say:
"No changes detected. Implement the feature before running code
review."

---

## Step 1: Parallel Review

Invoke both subagents simultaneously with the same context.

**meditrack-security-reviewer** receives:
- The combined diff from the pre-flight check
- Spec file for context: `.claude/specs/$ARGUMENTS.md`
- Source files to reference: `app.py` and `database/` directory
- Instruction: Review only the changed code for security
  vulnerabilities. Do not comment on quality or style.
- MediTrack-specific reminders to include in the prompt:
    - This is a health app. Cross-user data leaks of health_logs or
      vitals are the highest-severity class of bug.
    - Every route that returns health data must filter by
      `session['user_id']`, not by a URL parameter.
    - The schema enforces CHECK constraints on `entry_type`
      ('symptom' | 'medication'), `severity` (1–10), and `metric`
      (the five allowed vitals metrics). Flag any code that could
      insert values outside these.
    - Passwords must be hashed with werkzeug; sessions must be
      cleared on login before setting new data.

**meditrack-quality-reviewer** receives:
- The combined diff from the pre-flight check
- Spec file for context: `.claude/specs/$ARGUMENTS.md`
- Source files to reference: `app.py`, `database/` directory, and
  `templates/` directory
- Instruction: Review only the changed code for quality, Flask best
  practices, and maintainability. Do not comment on security
  concerns.
- MediTrack-specific reminders to include in the prompt:
    - Symptom and metric names must match the fixed lists in the
      spec — do not invent new ones.
    - Templates must extend `base.html`, use `url_for()`, and not
      contain inline styles.
    - Slash-command scripts must use `sqlite3.connect(DATABASE)`, not
      `get_db()`.
    - Dates stored and displayed as `YYYY-MM-DD`.

Both subagents must run in parallel. Do not wait for one to finish
before starting the other.

---

## Step 2: Unified Report

Once both subagents have completed, combine their findings into a
single unified report. De-duplicate any overlapping findings — if both
agents flagged the same line for different reasons, merge them into
one finding with both perspectives noted.

Structure the combined report as:


---

## Step 3: Ask for Approval

After presenting the unified report, ask:

"Do you want me to implement the action plan now?"

Wait for explicit user confirmation before making any changes. Do not
touch any files until the user approves.

---

## Rules

- Do NOT edit any files before user approval
- Do NOT start one reviewer before the other — both must run in
  parallel
- Do NOT skip the pre-flight diff check
- Do NOT proceed if the spec file at `.claude/specs/$ARGUMENTS.md`
  does not exist — report it and stop
- If either subagent fails or returns no output, report it and do NOT
  present a partial review as complete