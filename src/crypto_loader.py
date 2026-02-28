import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)  # cache for 5 minutes
def load_crypto_data(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "90",
        "interval": "daily"
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code == 429:
        raise Exception("Rate limit exceeded. Please wait 1–2 minutes.")

    response.raise_for_status()
    data = response.json()

    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Create OHLC for candlestick
    df["open"] = df["close"]
    df["high"] = df["close"]
    df["low"] = df["close"]

    return df
