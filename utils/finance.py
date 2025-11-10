import yfinance as yf

def get_stock_price(ticker, period="3mo"):
    t = yf.Ticker(ticker)
    hist = t.history(period=period)
    if hist.empty:
        return f"No data found for {ticker}"
    price = hist["Close"].iloc[-1]
    return f"{ticker.upper()} current price: ${price:.2f}"
