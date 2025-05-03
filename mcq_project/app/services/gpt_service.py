import json, time, os
from dotenv import load_dotenv
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  
)

def send_correction_prompt(original_q, retries=3, delay=2):
    question = original_q["question"]
    options = original_q["options"]
    answer = original_q["answer"]
    suggestions = original_q.get("validation", {}).get("suggestions", {})

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
  "answer": "A"
}}
"""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": PROMPT}],
                temperature=0.5,
                max_tokens=600
            )
            result = json.loads(response.choices[0].message.content.strip())
            result["revised"] = True
            return result
        except Exception as e:
            print(f"[GPT ERROR - Attempt {attempt+1}] {e}")
            time.sleep(delay)

    original_q["revised"] = False
    original_q["correction_error"] = f"Failed after {retries} attempts"
    return original_q
