from flask import Blueprint, render_template, request, jsonify
from datetime import date, timedelta
from extensions import db
from models import StudyPlan, StudySession, User

tracker_bp = Blueprint("tracker", __name__, url_prefix="/dashboard")


@tracker_bp.route("/")
def all_plans():
    plans = StudyPlan.query.order_by(StudyPlan.created_at.desc()).all()
    return render_template("plan_list.html", plans=plans)


@tracker_bp.route("/<int:plan_id>")
def dashboard(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    today = date.today()

    # Sessions grouped by day
    all_sessions = (
        StudySession.query
        .filter_by(plan_id=plan_id)
        .order_by(StudySession.date)
        .all()
    )

    # Streak calculation
    streak = 0
    check_date = today
    while True:
        day_sessions = [s for s in all_sessions if s.date == check_date]
        if not day_sessions:
            break
        if all(s.completed for s in day_sessions):
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    # Subject progress
    subject_progress = {}
    for session in all_sessions:
        name = session.subject.name if session.subject else "General"
        if name not in subject_progress:
            subject_progress[name] = {"total": 0, "completed": 0, "minutes": 0}
        subject_progress[name]["total"] += 1
        subject_progress[name]["minutes"] += session.duration_minutes
        if session.completed:
            subject_progress[name]["completed"] += 1

    for name, data in subject_progress.items():
        data["percent"] = round(
            (data["completed"] / data["total"] * 100) if data["total"] > 0 else 0
        )

    # Weekly activity (last 7 days)
    weekly = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_sessions = [s for s in all_sessions if s.date == d]
        completed = sum(1 for s in day_sessions if s.completed)
        total = len(day_sessions)
        weekly.append({
            "date": d.strftime("%a"),
            "completed": completed,
            "total": total,
            "minutes": sum(s.duration_minutes for s in day_sessions if s.completed),
        })

    # Today's sessions
    today_sessions = [s for s in all_sessions if s.date == today]

    # Stats
    total_minutes = sum(s.duration_minutes for s in all_sessions if s.completed)
    total_sessions = len(all_sessions)
    completed_sessions = sum(1 for s in all_sessions if s.completed)
    missed_sessions = sum(1 for s in all_sessions if s.missed)

    return render_template(
        "dashboard.html",
        plan=plan,
        streak=streak,
        subject_progress=subject_progress,
        weekly=weekly,
        today_sessions=today_sessions,
        today=today,
        total_minutes=total_minutes,
        total_sessions=total_sessions,
        completed_sessions=completed_sessions,
        missed_sessions=missed_sessions,
    )


@tracker_bp.route("/<int:plan_id>/weekly-data")
def weekly_data(plan_id):
    today = date.today()
    all_sessions = StudySession.query.filter_by(plan_id=plan_id).all()
    weekly = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_sessions = [s for s in all_sessions if s.date == d]
        weekly.append({
            "date": d.strftime("%a"),
            "completed": sum(1 for s in day_sessions if s.completed),
            "total": len(day_sessions),
            "minutes": sum(s.duration_minutes for s in day_sessions if s.completed),
        })
    return jsonify(weekly)