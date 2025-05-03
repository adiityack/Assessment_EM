import requests

def fetch_questions(api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Give 5 MCQs"}]
    }

    res = requests.post(url, json=payload, headers=headers, timeout=10)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]