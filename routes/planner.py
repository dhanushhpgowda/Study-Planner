from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import date, datetime
from extensions import db
from models import User, StudyPlan, Subject, StudySession

planner_bp = Blueprint("planner", __name__, url_prefix="/plan")


@planner_bp.route("/new", methods=["GET"])
def new_plan():
    return render_template("plan_new.html", today=date.today().isoformat())


@planner_bp.route("/generate", methods=["POST"])
def generate():
    try:
        name        = request.form.get("name", "").strip()
        email       = request.form.get("email", "").strip()
        exam_date_s = request.form.get("exam_date", "")
        daily_hours = float(request.form.get("daily_hours", 4))
        plan_title  = request.form.get("plan_title", "My Study Plan").strip()

        subject_names       = request.form.getlist("subject_name[]")
        subject_difficulties = request.form.getlist("subject_difficulty[]")
        subject_topics      = request.form.getlist("subject_topics[]")

        if not name or not email or not exam_date_s or not subject_names:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("planner.new_plan"))

        exam_date = datetime.strptime(exam_date_s, "%Y-%m-%d").date()
        if exam_date <= date.today():
            flash("Exam date must be in the future.", "error")
            return redirect(url_for("planner.new_plan"))

        # Get or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.flush()

        # Create study plan
        plan = StudyPlan(
            user_id=user.id,
            title=plan_title,
            exam_date=exam_date,
            daily_hours=daily_hours,
        )
        db.session.add(plan)
        db.session.flush()

        # Create subjects
        subjects_data = []
        subjects_map  = {}
        diff_labels   = {1: "Easy", 2: "Medium", 3: "Hard"}

        for i, sname in enumerate(subject_names):
            sname = sname.strip()
            if not sname:
                continue
            diff   = int(subject_difficulties[i]) if i < len(subject_difficulties) else 2
            topics = subject_topics[i].strip() if i < len(subject_topics) else ""

            subj = Subject(
                plan_id=plan.id,
                name=sname,
                difficulty=diff,
                topics=topics,
            )
            db.session.add(subj)
            db.session.flush()

            subjects_map[sname.lower()] = subj.id
            subjects_data.append({
                "name": sname,
                "difficulty": diff,
                "difficulty_label": diff_labels.get(diff, "Medium"),
                "topics": topics,
            })

        db.session.commit()

        # Call Claude to generate schedule
        from services.planner_service import generate_schedule, sessions_to_db
        sessions_json = generate_schedule(subjects_data, exam_date, daily_hours, name)
        sessions_to_db(sessions_json, plan, subjects_map)

        flash(f"Your study plan is ready, {name}! 🎉", "success")
        return redirect(url_for("planner.view_plan", plan_id=plan.id))

    except ValueError as e:
        flash(f"Invalid input: {str(e)}", "error")
        return redirect(url_for("planner.new_plan"))
    except Exception as e:
        db.session.rollback()
        flash(f"Something went wrong while generating your plan: {str(e)}", "error")
        return redirect(url_for("planner.new_plan"))


@planner_bp.route("/<int:plan_id>")
def view_plan(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    from services.planner_service import get_sessions_by_day
    days = get_sessions_by_day(plan_id)
    today = date.today()
    return render_template("plan_view.html", plan=plan, days=days, today=today)


@planner_bp.route("/<int:plan_id>/session/<int:session_id>/complete", methods=["POST"])
def complete_session(plan_id, session_id):
    session = StudySession.query.get_or_404(session_id)
    session.mark_complete()
    db.session.commit()
    return jsonify({"status": "ok", "progress": StudyPlan.query.get(plan_id).progress_percent})


@planner_bp.route("/<int:plan_id>/session/<int:session_id>/miss", methods=["POST"])
def miss_session(plan_id, session_id):
    session = StudySession.query.get_or_404(session_id)
    session.mark_missed()
    db.session.commit()
    return jsonify({"status": "ok"})