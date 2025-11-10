import json, os

def fetch_emails(max_results=5):
    mock_path = os.path.join(os.path.dirname(__file__), "../mock_email.json")
    try:
        with open(mock_path, "r") as f:
            data = json.load(f)
        return [f"📧 {m['subject']} — {m['snippet']}" for m in data[:max_results]]
    except Exception as e:
        return [f"Error reading mock email: {e}"]
