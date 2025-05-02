import os
import json
import time
from flask import Flask, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import logging





# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

# Automatically determine the path of questions.json in the same directory as the app
QUESTION_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'questions.json')

def send_correction_prompt(original_q, retries=3, delay=2):
    """
    Function to send a question with validation issues to GPT for correction.
    """
    question = original_q["question"]
    options = original_q["options"]
    answer = original_q["answer"]
    suggestions = original_q.get("validation", {}).get("suggestions", {})

    # Prompt to ask GPT to correct the question
    PROMPT = f"""
You are an expert MCQ editor. The following question has validation issues such as grammar errors, duplicate options, or answer mismatches.

Please fix the question according to the provided suggestions, while keeping the core concept the same.

---

Original Question: {question}

Options:
{json.dumps(options, indent=2)}

Answer: {answer}

Validation Suggestions:
{json.dumps(suggestions, indent=2)}

---

Return the corrected version strictly in this JSON format:
{{
  "question": "...",
  "options": {{
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "answer": "A"  // valid option key
}}
"""

    # Retry logic for handling failures
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": PROMPT}],
                temperature=0.5,
                max_tokens=600
            )
            content = response.choices[0].message.content.strip()
            new_question = json.loads(content)
            new_question["revised"] = True
            return new_question
        except Exception as e:
            print(f"[GPT ERROR - Attempt {attempt+1}] {e}")
            time.sleep(delay)

    # If all attempts fail
    original_q["revised"] = False
    original_q["correction_error"] = f"Failed after {retries} attempts"
    return original_q

@app.route('/review', methods=['POST'])
def review_questions():
    """
    API endpoint to process a batch of questions, send faulty ones for correction,
    and return the corrected list of questions.
    """
    # Check if the questions.json file exists in the directory
    if not os.path.exists(QUESTION_FILE_PATH):
        return jsonify({"error": "questions.json file not found in the current directory"}), 404

    # Load the questions from the JSON file
    with open(QUESTION_FILE_PATH, 'r') as f:
        data = json.load(f)

    # List to store the updated questions
    revised_questions = []

    # Loop through the questions and process them
    for question in data:
        if question["validation"]["status"] == "Failed":
            # If validation failed, send the question to GPT for correction
            corrected_question = send_correction_prompt(question)
            revised_questions.append(corrected_question)
        else:
            # If the question is valid, mark it as not revised
            question["revised"] = False
            revised_questions.append(question)

    # Update the questions.json with the revised questions
    with open(QUESTION_FILE_PATH, 'w') as f:
        json.dump(revised_questions, f, indent=2)

    # Return a success response
    return jsonify({"message": "Questions have been reviewed and updated", "questions": revised_questions})

#newnewnew




if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
