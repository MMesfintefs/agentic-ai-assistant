import json
from datetime import datetime

def process_user_input(user_input):
    if not user_input:
        return "Say something first 😅"
    
    text = user_input.lower()

    if "hello" in text or "hi" in text:
        return "Hello there 👋 How can I help you today?"

    elif "email" in text:
        try:
            with open("mock_email.json") as f:
                emails = json.load(f)
            formatted = "\n\n".join(
                [f"📩 *{e['subject']}* — from {e['sender']} at {e['time']}" for e in emails]
            )
            return f"Here are your recent emails:\n\n{formatted}"
        except:
            return "Couldn't load your emails right now."

    elif "calendar" in text or "schedule" in text:
        try:
            with open("mock_calendar.json") as f:
                events = json.load(f)
            formatted = "\n".join([f"🗓️ {e['title']} — {e['time']}" for e in events])
            return f"Here’s your schedule:\n{formatted}"
        except:
            return "Couldn’t fetch your calendar at the moment."

    elif "date" in text:
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."

    else:
        return "I'm still learning that one 🤔. Try asking for stocks, emails, or your schedule."
