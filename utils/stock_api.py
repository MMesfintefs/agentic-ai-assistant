import yfinance as yf
import plotly.express as px
import pandas as pd

def get_stock_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1mo")
        if data.empty:
            return "No stock data found.", None
        
        last_price = data["Close"].iloc[-1]
        first_price = data["Close"].iloc[0]
        change = ((last_price - first_price) / first_price) * 100

        info = f"**{ticker.upper()}** — Current Price: ${last_price:.2f} | Change: {change:.2f}% (1M)"
        chart = px.line(data, x=data.index, y="Close", title=f"{ticker.upper()} - Last 1 Month Trend")

        return info, chart
    except Exception as e:
        return f"Error fetching stock data: {e}", None
