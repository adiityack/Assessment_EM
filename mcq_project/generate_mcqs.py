

import json
import time
import os
from openai import OpenAI



from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  
)

# Prompt template
PROMPT = """
Generate 10 multiple-choice questions (MCQs) on the topic "Laws of Motion - Grade 9".
Each question should have:
- A clear question statement.
- Four answer options labeled A, B, C, D.
- One correct answer (only the label like "A", "B", etc.).
Format the response as a list of dictionaries like:
[
  {
    "question": "What is Newton's First Law also known as?",
    "options": {
      "A": "Law of Acceleration",
      "B": "Law of Inertia",
      "C": "Law of Action-Reaction",
      "D": "Law of Force"
    },
    "answer": "B"
  },
  ...
]
"""

def validate_question(q):
    return (
        isinstance(q, dict) and
        "question" in q and isinstance(q["question"], str) and
        "options" in q and isinstance(q["options"], dict) and
        len(q["options"]) == 4 and
        "answer" in q and q["answer"] in q["options"]
    )

def is_valid_output(data):
    return (
        isinstance(data, list) and
        len(data) == 10 and
        all(validate_question(q) for q in data)
    )

# Retry until valid
retries = 3
for attempt in range(retries):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": PROMPT}]
        )
        content = response.choices[0].message.content.strip()
        new_questions = json.loads(content)

        if is_valid_output(new_questions):
            # Load existing questions if file exists
            existing_questions = []
            if os.path.exists("questions.json"):
                with open("questions.json", "r") as f:
                    try:
                        existing_questions = json.load(f)
                        if not isinstance(existing_questions, list):
                            existing_questions = []
                    except json.JSONDecodeError:
                        existing_questions = []

            # Append new questions
            all_questions = existing_questions + new_questions

            # Save combined questions
            with open("questions.json", "w") as f:
                json.dump(all_questions, f, indent=2)
            print("New questions appended to questions.json")
            break
        else:
            raise ValueError("Invalid question format")
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < retries - 1:
            time.sleep(2)
        else:
            print("Failed to generate valid questions after 3 attempts.")


