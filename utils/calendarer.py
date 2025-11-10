import json, os
from datetime import datetime

def list_events():
    mock_path = os.path.join(os.path.dirname(__file__), "../mock_calendar.json")
    try:
        with open(mock_path, "r") as f:
            data = json.load(f)
        return [f"📅 {e['date']} — {e['title']}" for e in data]
    except Exception as e:
        return [f"Error reading mock calendar: {e}"]

def add_event(title="Demo Meeting"):
    # Simulate success
    return f"✅ '{title}' scheduled on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
