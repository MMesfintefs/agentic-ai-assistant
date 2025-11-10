import requests, streamlit as st

def get_weather(city):
    key = st.secrets["OPENWEATHER_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    r = requests.get(url).json()
    if "main" in r:
        temp = r["main"]["temp"]
        cond = r["weather"][0]["description"]
        return f"{city.title()}: {temp}°C, {cond}"
    return "Weather data unavailable."
