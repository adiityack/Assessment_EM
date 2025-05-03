
import pytest
from unittest.mock import patch, Mock
from fetch_mcq.main import fetch_questions

@patch("fetch_mcq.main.requests.post")
def test_fetch_questions(mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "Q1. Example MCQ"}}
        ]
    }
    mock_post.return_value = mock_response

    api_key = "fake-token"
    content = fetch_questions(api_key)

    assert content == "Q1. Example MCQ"
    mock_post.assert_called_once()
