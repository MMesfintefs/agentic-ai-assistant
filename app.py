import streamlit as st
import yfinance as yf
import plotly.express as px
import requests, imaplib, email
from datetime import datetime
from duckduckgo_search import DDGS
from openai import OpenAI
import pandas as pd
import os

# --- Setup ---
st.set_page_config(page_title="Agentic AI Assistant", layout="wide")
st.title("🤖 Agentic AI Assistant")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Basic prompt input ---
prompt = st.chat_input("Ask me anything...")
if not prompt:
    st.stop()

st.chat_message("user").markdown(prompt)

# --- Core logic ---
response = ""
if "stock" in prompt.lower() or "price" in prompt.lower():
    try:
        words = prompt.split()
        ticker = next((w.upper() for w in words if w.isalpha() and len(w) <= 5), "AAPL")
        data = yf.Ticker(ticker).history(period="1mo")
        st.write(f"### {ticker} stock (last 1 month)")
        st.line_chart(data["Close"])
        latest = data["Close"].iloc[-1]
        response = f"{ticker} is currently trading at **${latest:.2f}**."
    except Exception as e:
        response = f"Could not fetch stock data. ({e})"

elif "news" in prompt.lower():
    try:
        q = " ".join(prompt.split()[1:]) or "latest"
        url = f"https://newsapi.org/v2/everything?q={q}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        articles = requests.get(url).json().get("articles", [])[:3]
        if not articles:
            response = "No news found."
        else:
            st.write("### 📰 Latest News")
            for a in articles:
                st.markdown(f"- [{a['title']}]({a['url']})")
            response = "Here are the top headlines."
    except Exception as e:
        response = f"Error fetching news: {e}"

elif "email" in prompt.lower():
    try:
        mail = imaplib.IMAP4_SSL(st.secrets["EMAIL_HOST"])
        mail.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_PASS"])
        mail.select("inbox")
        result, data = mail.search(None, 'ALL')
        ids = data[0].split()[-3:]
        for num in ids:
            _, msg_data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            st.write(f"**From:** {msg['From']}  |  **Subject:** {msg['Subject']}")
        response = "Fetched your recent emails."
    except Exception as e:
        response = f"Email access failed ({e})"

elif "calendar" in prompt.lower():
    response = "Calendar access placeholder. (Integrate Google Calendar API here.)"

else:
    try:
        chat = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        response = chat.choices[0].message.content
    except Exception as e:
        response = f"Error connecting to OpenAI: {e}"

# --- Output ---
with st.chat_message("assistant"):
    st.markdown(response)
