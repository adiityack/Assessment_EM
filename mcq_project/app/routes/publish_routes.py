from flask import Blueprint, jsonify, request
import os, json, time, requests, logging
from app.utils.file_loader import get_questions

publish_bp = Blueprint('publish', __name__)

@publish_bp.route('/', methods=['GET'])
def home():
    return "Flask server is running."

@publish_bp.route('/publish', methods=['POST'])
def publish_questions():
    questions = get_questions()
    if questions is None:
        return jsonify({"error": "questions.json not found"}), 404

    MOCK_API_URL = "https://httpbin.org/post"
    HEADERS = {"Authorization": "Bearer dummy_token"}

    success_count, failure_count = 0, 0

    for index, question in enumerate(questions, start=1):
        retries = 3
        while retries > 0:
            try:
                response = requests.post(
                    MOCK_API_URL,
                    headers=HEADERS,
                    json=question,
                    timeout=5
                )
                response.raise_for_status()
                logging.info(f"[SUCCESS] Q#{index}: Published. Status: {response.status_code}")
                success_count += 1
                break
            except requests.RequestException as e:
                retries -= 1
                logging.warning(f"[RETRY] Q#{index} - Retries left: {retries}, Error: {e}")
                time.sleep(1)
        else:
            logging.error(f"[FAILURE] Q#{index}: Failed after 3 attempts.")
            failure_count += 1

    return jsonify({
        "message": "Publishing completed.",
        "success_count": success_count,
        "failure_count": failure_count
    })
