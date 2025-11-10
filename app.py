import streamlit as st, re
from datetime import datetime
from utils.finance import get_stock_price
from utils.weather import get_weather
from utils.news import get_news
from utils.emailer import fetch_emails
from utils.calendarer import list_events, add_event

st.set_page_config(page_title="Agentic AI", page_icon="🧠", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your Agentic AI Assistant. I can check stocks, weather, news, email, and your calendar. How can I help today?"}
    ]

def parse(text):
    t = text.lower()
    if "stock" in t or re.search(r"\b[A-Z]{2,5}\b", t):
        ticker = re.findall(r"\b[A-Z]{2,5}\b", t)
        return ("stock", ticker[0] if ticker else "AAPL")
    if "weather" in t:
        city = t.split("in")[-1].strip() or "Boston"
        return ("weather", city)
    if "news" in t:
        topic = t.split("news")[-1].strip() or "world"
        return ("news", topic)
    if "email" in t or "inbox" in t:
        return ("email", None)
    if "schedule" in t or "meeting" in t:
        return ("add_event", t)
    if "my schedule" in t or "calendar" in t:
        return ("list_events", None)
    return ("unknown", t)

user = st.chat_input("Ask me anything...")

if user:
    st.session_state.messages.append({"role": "user", "content": user})
    kind, arg = parse(user)

    if kind == "stock": reply = get_stock_price(arg)
    elif kind == "weather": reply = get_weather(arg)
    elif kind == "news": reply = "\n".join(get_news(arg))
    elif kind == "email": reply = "\n".join(fetch_emails())
    elif kind == "list_events": reply = "\n".join(list_events())
    elif kind == "add_event": reply = add_event("Demo Meeting")
    else: reply = "I didn’t quite get that, but you can ask about stocks, weather, news, email, or calendar."

    st.session_state.messages.append({"role": "assistant", "content": reply})

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])
