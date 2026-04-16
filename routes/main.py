from flask import Blueprint, render_template, request, jsonify, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/health")
def health():
    return {"status": "ok", "message": "Study Planner API is running"}


@main_bp.route("/notifications/test/<int:plan_id>", methods=["POST"])
def test_notification(plan_id):
    from models import StudyPlan
    from datetime import date
    from services.notifications import send_daily_reminder

    plan = StudyPlan.query.get_or_404(plan_id)
    today_sessions = [s for s in plan.sessions if s.date == date.today()]

    if not today_sessions:
        all_sessions = sorted(plan.sessions, key=lambda s: s.date)
        today_sessions = all_sessions[:3] if all_sessions else []

    success = send_daily_reminder(plan.user, plan, today_sessions)
    return jsonify({
        "success": success,
        "message": f"Test email sent to {plan.user.email}" if success else "Failed to send email. Check your MAIL settings in .env"
    })


@main_bp.route("/notifications/toggle/<int:user_id>", methods=["POST"])
def toggle_notifications(user_id):
    from models import User
    from extensions import db
    user = User.query.get_or_404(user_id)
    user.email_reminders = not user.email_reminders
    db.session.commit()
    return jsonify({
        "enabled": user.email_reminders,
        "message": f"Reminders {'enabled' if user.email_reminders else 'disabled'}"
    })