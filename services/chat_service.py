import os
from groq import Groq
from models import StudyPlan, StudySession, Subject
from datetime import date

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))


def build_system_prompt(plan):
    today = date.today()

    subjects = ", ".join(
        f"{s.name} ({s.difficulty_label})" for s in plan.subjects
    )

    today_sessions = [
        s for s in plan.sessions if s.date == today
    ]
    today_text = ""
    if today_sessions:
        today_text = "\nToday's sessions:\n" + "\n".join(
            f"- {s.subject.name if s.subject else 'General'}: {s.topic} ({s.duration_minutes}min)"
            for s in today_sessions
        )
    else:
        today_text = "\nNo sessions scheduled for today."

    return f"""You are StudyMind AI, a friendly and expert study assistant.

You are helping a student named {plan.user.name} prepare for their exam on {plan.exam_date.strftime('%B %d, %Y')} ({plan.days_until_exam} days away).

Their subjects: {subjects}
Overall progress: {plan.progress_percent}% complete
{today_text}

Your role:
- Answer questions about their subjects clearly and concisely
- Give study tips, memory techniques, and exam strategies
- Motivate and encourage them
- Help them understand difficult concepts
- Suggest how to use their remaining study time wisely
- Keep responses focused and practical — this is a study session, not an essay

Always be encouraging, clear, and to the point. Use examples when explaining concepts."""


def get_chat_response(plan_id, messages):
    plan = StudyPlan.query.get_or_404(plan_id)
    system_prompt = build_system_prompt(plan)

    groq_messages = [
        {"role": "system", "content": system_prompt}
    ] + messages

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        temperature=0.7,
        messages=groq_messages,
    )

    return response.choices[0].message.content


def get_quick_tips(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    subjects = [s.name for s in plan.subjects]

    prompt = f"""Give 3 quick, actionable study tips for a student studying {', '.join(subjects)} with {plan.days_until_exam} days until their exam.
Format as a simple numbered list. Keep each tip under 20 words. Be specific and practical."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=200,
        temperature=0.8,
        messages=[
            {"role": "system", "content": "You are a concise study advisor. Give short, practical tips only."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content