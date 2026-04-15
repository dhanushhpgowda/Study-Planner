from flask import Blueprint, render_template, request, jsonify
from models import StudyPlan

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/<int:plan_id>")
def chat_page(plan_id):
    plan = StudyPlan.query.get_or_404(plan_id)
    return render_template("chat.html", plan=plan)


@chat_bp.route("/<int:plan_id>/message", methods=["POST"])
def send_message(plan_id):
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    from services.chat_service import get_chat_response
    reply = get_chat_response(plan_id, messages)
    return jsonify({"reply": reply})


@chat_bp.route("/<int:plan_id>/tips", methods=["GET"])
def quick_tips(plan_id):
    from services.chat_service import get_quick_tips
    tips = get_quick_tips(plan_id)
    return jsonify({"tips": tips})