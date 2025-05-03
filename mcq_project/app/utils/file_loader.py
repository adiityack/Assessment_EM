import os
import json

import os

QUESTION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'questions.json'))
print("Resolved path:", QUESTION_FILE_PATH)



def get_questions():
    if not os.path.exists(QUESTION_FILE_PATH):
        return None
    with open(QUESTION_FILE_PATH, 'r') as f:
        return json.load(f)

def save_questions(data):
    with open(QUESTION_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=2)
