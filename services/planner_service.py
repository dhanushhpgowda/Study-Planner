import os
import json
from datetime import date, timedelta
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

DIFFICULTY_WEIGHT = {1: 0.8, 2: 1.0, 3: 1.4}
SESSION_TYPES = {
    "study":     "Study",
    "revision":  "Revision",
    "mock_test": "Mock Test",
}


def build_prompt(subjects, exam_date, daily_hours, user_name):
    today = date.today()
    days_left = (exam_date - today).days
    subject_lines = "\n".join(
        f"- {s['name']} | difficulty: {s['difficulty_label']} | topics: {s.get('topics') or 'General'}"
        for s in subjects
    )
    return f"""You are an expert academic study planner. Create a detailed, personalized study schedule.

Student: {user_name}
Exam date: {exam_date.strftime('%B %d, %Y')}
Days available: {days_left}
Study hours per day: {daily_hours}

Subjects:
{subject_lines}

Rules:
1. Harder subjects get more total time across the schedule
2. Space out subjects — avoid studying the same subject more than 2 days in a row
3. Include short revision sessions every 3-4 days for earlier topics
4. Last 2 days before exam = revision and mock test only, no new topics
5. Each session should be 45-90 minutes max
6. Keep daily load within the {daily_hours} hours limit
7. Keep topic names SHORT — maximum 6 words
8. Keep tip text SHORT — maximum 10 words

Return ONLY a valid JSON array. No explanation, no markdown, just raw JSON.
Each item must have exactly these fields:
{{
  "day_number": 1,
  "date": "YYYY-MM-DD",
  "subject": "Subject Name",
  "topic": "Short topic name",
  "duration_minutes": 60,
  "session_type": "study",
  "tip": "Short tip here"
}}

Generate the full schedule for all {days_left} days."""


def generate_schedule(subjects, exam_date, daily_hours, user_name):
    prompt = build_prompt(subjects, exam_date, daily_hours, user_name)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=8000,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert study planner. "
                    "Always respond with valid JSON only. "
                    "No explanation, no markdown, no text before or after. "
                    "Just a raw JSON array. Keep topic names short (under 8 words). "
                    "Keep tip text short (under 12 words)."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown fences if present
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    # If JSON is cut off, try to salvage it
    if not raw.endswith("]"):
        last_brace = raw.rfind("}")
        if last_brace != -1:
            raw = raw[:last_brace + 1] + "]"

    sessions = json.loads(raw)
    return sessions


def sessions_to_db(sessions, plan, subjects_map):
    from models import StudySession
    from extensions import db

    db_sessions = []
    for s in sessions:
        subject_id = subjects_map.get(s["subject"].strip().lower())
        session_date = date.fromisoformat(s["date"])

        db_session = StudySession(
            plan_id=plan.id,
            subject_id=subject_id,
            day_number=s["day_number"],
            date=session_date,
            topic=s["topic"],
            duration_minutes=s["duration_minutes"],
            session_type=s.get("session_type", "study"),
            notes=s.get("tip", ""),
        )
        db_sessions.append(db_session)

    db.session.add_all(db_sessions)
    db.session.commit()
    return db_sessions


def get_today_sessions(plan):
    from models import StudySession
    today = date.today()
    return (
        StudySession.query
        .filter_by(plan_id=plan.id)
        .filter(StudySession.date == today)
        .all()
    )


def get_sessions_by_day(plan_id):
    from models import StudySession
    sessions = (
        StudySession.query
        .filter_by(plan_id=plan_id)
        .order_by(StudySession.day_number, StudySession.id)
        .all()
    )
    days = {}
    for s in sessions:
        days.setdefault(s.day_number, []).append(s)
    return days