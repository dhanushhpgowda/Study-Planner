from flask import Blueprint, send_file, jsonify, render_template, redirect, url_for, flash
from models import StudyPlan
from extensions import db

export_bp = Blueprint("export", __name__, url_prefix="/plan")


@export_bp.route("/<int:plan_id>/export/pdf")
def export_pdf(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    from services.pdf_export import build_pdf
    buffer = build_pdf(plan)
    filename = f"{plan.title.replace(' ', '_')}_study_plan.pdf"
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


@export_bp.route("/<int:plan_id>/reschedule", methods=["POST"])
def reschedule(plan_id):
    from services.rescheduler import reschedule_missed
    result = reschedule_missed(plan_id)
    return jsonify(result)


@export_bp.route("/<int:plan_id>/export")
def export_page(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    from services.rescheduler import get_missed_sessions
    missed = get_missed_sessions(plan_id)
    return render_template("export.html", plan=plan, missed_count=len(missed))