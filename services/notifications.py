from flask_mail import Message
from extensions import mail
from models import StudyPlan, StudySession, User
from datetime import date


def build_daily_email(user, plan, today_sessions):
    total_minutes = sum(s.duration_minutes for s in today_sessions)
    hours = total_minutes // 60
    mins  = total_minutes % 60

    subject_list = ""
    for s in today_sessions:
        subj  = s.subject.name if s.subject else "General"
        stype = s.session_type.replace("_", " ").title()
        subject_list += f"""
        <tr>
          <td style="padding:10px 16px;border-bottom:1px solid #1e1e2e;font-size:14px;color:#f0eee8;">{subj}</td>
          <td style="padding:10px 16px;border-bottom:1px solid #1e1e2e;font-size:14px;color:#9896a0;">{s.topic}</td>
          <td style="padding:10px 16px;border-bottom:1px solid #1e1e2e;font-size:14px;color:#f5a623;text-align:center;">{s.duration_minutes}m</td>
          <td style="padding:10px 16px;border-bottom:1px solid #1e1e2e;font-size:14px;color:#9896a0;text-align:center;">{stype}</td>
        </tr>"""

    days_left = (plan.exam_date - date.today()).days
    progress  = plan.progress_percent

    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#0a0a0f;font-family:'Helvetica Neue',Arial,sans-serif;">
  <div style="max-width:600px;margin:0 auto;padding:32px 16px;">

    <!-- HEADER -->
    <div style="text-align:center;margin-bottom:32px;">
      <div style="display:inline-block;background:rgba(245,166,35,0.12);border:1px solid rgba(245,166,35,0.3);border-radius:12px;padding:12px 20px;">
        <span style="color:#f5a623;font-size:20px;font-weight:800;letter-spacing:-0.02em;">◈ StudyMind</span>
      </div>
    </div>

    <!-- HERO -->
    <div style="background:#111118;border:1px solid #1e1e2e;border-radius:20px;padding:32px;margin-bottom:20px;text-align:center;">
      <div style="font-size:36px;margin-bottom:8px;">📚</div>
      <h1 style="color:#f0eee8;font-size:26px;font-weight:800;margin:0 0 8px;letter-spacing:-0.02em;">
        Good morning, {user.name}!
      </h1>
      <p style="color:#9896a0;font-size:15px;margin:0 0 24px;">
        Here's your study agenda for today — {date.today().strftime('%A, %B %d')}
      </p>

      <!-- STATS ROW -->
      <div style="display:flex;justify-content:center;gap:0;border:1px solid #1e1e2e;border-radius:12px;overflow:hidden;margin-bottom:0;">
        <div style="flex:1;padding:16px;background:#1e1e2e;text-align:center;border-right:1px solid #0a0a0f;">
          <div style="font-size:22px;font-weight:800;color:#f5a623;">{days_left}</div>
          <div style="font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;margin-top:4px;">Days left</div>
        </div>
        <div style="flex:1;padding:16px;background:#1e1e2e;text-align:center;border-right:1px solid #0a0a0f;">
          <div style="font-size:22px;font-weight:800;color:#8b7cf6;">{progress}%</div>
          <div style="font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;margin-top:4px;">Progress</div>
        </div>
        <div style="flex:1;padding:16px;background:#1e1e2e;text-align:center;">
          <div style="font-size:22px;font-weight:800;color:#2dd4bf;">{hours}h {mins}m</div>
          <div style="font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;margin-top:4px;">Today's load</div>
        </div>
      </div>
    </div>

    <!-- TODAY'S SCHEDULE -->
    <div style="background:#111118;border:1px solid #1e1e2e;border-radius:20px;overflow:hidden;margin-bottom:20px;">
      <div style="padding:20px 24px;border-bottom:1px solid #1e1e2e;">
        <h2 style="color:#f0eee8;font-size:16px;font-weight:700;margin:0;">Today's sessions</h2>
      </div>
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="background:#0a0a0f;">
            <th style="padding:10px 16px;text-align:left;font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;">Subject</th>
            <th style="padding:10px 16px;text-align:left;font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;">Topic</th>
            <th style="padding:10px 16px;text-align:center;font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;">Time</th>
            <th style="padding:10px 16px;text-align:center;font-size:11px;color:#5a5862;text-transform:uppercase;letter-spacing:0.06em;font-weight:600;">Type</th>
          </tr>
        </thead>
        <tbody>{subject_list}</tbody>
      </table>
    </div>

    <!-- CTA -->
    <div style="text-align:center;margin-bottom:20px;">
      <a href="http://localhost:5000/plan/{plan.id}"
         style="display:inline-block;background:#f5a623;color:#0a0a0f;font-weight:800;font-size:15px;
                padding:14px 32px;border-radius:12px;text-decoration:none;letter-spacing:-0.01em;">
        Open my study plan →
      </a>
    </div>

    <!-- MOTIVATIONAL QUOTE -->
    <div style="background:rgba(139,124,246,0.08);border:1px solid rgba(139,124,246,0.2);border-radius:16px;padding:20px;text-align:center;margin-bottom:20px;">
      <p style="color:#8b7cf6;font-size:14px;font-style:italic;margin:0;">
        "Success is the sum of small efforts, repeated day in and day out."
      </p>
    </div>

    <!-- FOOTER -->
    <div style="text-align:center;padding:16px;">
      <p style="color:#5a5862;font-size:12px;margin:0;">
        StudyMind · You're receiving this because you enabled daily reminders.<br/>
        Exam: {plan.exam_date.strftime('%B %d, %Y')} · Plan: {plan.title}
      </p>
    </div>

  </div>
</body>
</html>"""

    return html


def send_daily_reminder(user, plan, today_sessions):
    if not today_sessions:
        return False

    html_body = build_daily_email(user, plan, today_sessions)

    msg = Message(
        subject=f"📚 StudyMind — Today's Study Plan ({date.today().strftime('%b %d')})",
        recipients=[user.email],
        html=html_body,
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[Email Error] Failed to send to {user.email}: {e}")
        return False


def send_reminders_for_all_plans(app):
    with app.app_context():
        today = date.today()
        plans = StudyPlan.query.filter_by(is_active=True).all()
        sent  = 0

        for plan in plans:
            if plan.days_until_exam < 0:
                continue

            today_sessions = [
                s for s in plan.sessions
                if s.date == today and not s.completed and not s.missed
            ]

            if plan.user.email_reminders:
                success = send_daily_reminder(plan.user, plan, today_sessions)
                if success:
                    sent += 1

        print(f"[Scheduler] Sent {sent} reminder email(s) for {today}")
        return sent