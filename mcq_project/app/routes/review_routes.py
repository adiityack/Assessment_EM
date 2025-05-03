from flask import Blueprint, jsonify
import os, json
from app.utils.file_loader import get_questions, save_questions
from app.services.gpt_service import send_correction_prompt

review_bp = Blueprint('review', __name__)

@review_bp.route('/review', methods=['POST'])
def review_questions():
    questions = get_questions()
    if questions is None:
        return jsonify({"error": "questions.json file not found"}), 404

    revised_questions = []
    for q in questions:
        if q.get("validation", {}).get("status") == "Failed":
            revised = send_correction_prompt(q)
            revised_questions.append(revised)
        else:
            q["revised"] = False
            revised_questions.append(q)

    save_questions(revised_questions)

    return jsonify({
        "message": "Questions have been reviewed and updated",
        "questions": revised_questions
    })
