from datetime import date, timedelta
from extensions import db
from models import StudySession, StudyPlan


def get_missed_sessions(plan_id):
    today = date.today()
    return (
        StudySession.query
        .filter_by(plan_id=plan_id, missed=False, completed=False)
        .filter(StudySession.date < today)
        .order_by(StudySession.date)
        .all()
    )


def reschedule_missed(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    today = date.today()

    # Get all uncompleted past sessions (missed ones)
    missed = get_missed_sessions(plan_id)
    if not missed:
        return {"rescheduled": 0, "message": "No missed sessions found."}

    # Get future sessions to understand existing load per day
    future_sessions = (
        StudySession.query
        .filter_by(plan_id=plan_id)
        .filter(StudySession.date >= today)
        .filter(StudySession.completed == False)
        .order_by(StudySession.date)
        .all()
    )

    # Build a map of date -> total minutes already scheduled
    daily_load = {}
    for s in future_sessions:
        d = s.date
        daily_load[d] = daily_load.get(d, 0) + s.duration_minutes

    max_daily_minutes = plan.daily_hours * 60
    rescheduled_count = 0

    # Mark all missed sessions as missed=True first
    for s in missed:
        s.missed = True

    db.session.flush()

    # For each missed session, find the next available day with capacity
    check_date = today
    for session in missed:
        placed = False
        attempts = 0

        while not placed and attempts < 60:
            current_load = daily_load.get(check_date, 0)
            if current_load + session.duration_minutes <= max_daily_minutes:
                # Create a new rescheduled session
                new_session = StudySession(
                    plan_id=plan_id,
                    subject_id=session.subject_id,
                    day_number=session.day_number,
                    date=check_date,
                    topic=session.topic + " (rescheduled)",
                    duration_minutes=session.duration_minutes,
                    session_type=session.session_type,
                    notes=f"Rescheduled from {session.date.strftime('%b %d')}",
                )
                db.session.add(new_session)
                daily_load[check_date] = current_load + session.duration_minutes
                rescheduled_count += 1
                placed = True
            else:
                check_date += timedelta(days=1)
                attempts += 1

    db.session.commit()

    return {
        "rescheduled": rescheduled_count,
        "message": f"Successfully rescheduled {rescheduled_count} missed session(s)."
    }