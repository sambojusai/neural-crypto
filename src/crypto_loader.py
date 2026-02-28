import requests
import pandas as pd
import streamlit as st

# Symbol mapping for different APIs
COINGECKO_IDS = {
    "bitcoin": "bitcoin",
    "ethereum": "ethereum"
}

BINANCE_SYMBOLS = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT"
}


@st.cache_data(ttl=300)
def load_crypto_data(symbol):
    symbol = symbol.lower()

    # ------------------------------------------------
    # Step 1 — Fetch 90 days closing prices (CoinGecko)
    # ------------------------------------------------
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "90",
        "interval": "daily"
    }

    response = requests.get(url, params=params, timeout=20)

    if response.status_code == 429:
        raise Exception("CoinGecko rate limit reached. Please wait 1-2 minutes.")

    response.raise_for_status()
    data = response.json()

    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # ------------------------------------------------
    # Step 2 — Fetch REAL OHLC data from Binance
    # ------------------------------------------------
    try:
        binance_symbol = BINANCE_SYMBOLS.get(symbol, "BTCUSDT")

        binance_url = "https://api.binance.com/api/v3/klines"
        binance_params = {
            "symbol": binance_symbol,
            "interval": "1d",
            "limit": 90
        }

        binance_response = requests.get(
            binance_url,
            params=binance_params,
            timeout=20
        )
        binance_response.raise_for_status()
        klines = binance_response.json()

        # Binance returns: [timestamp, open, high, low, close, volume, ...]
        ohlc_df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close",
            "volume", "close_time", "quote_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])

        ohlc_df["timestamp"] = pd.to_datetime(ohlc_df["timestamp"], unit="ms")
        ohlc_df.set_index("timestamp", inplace=True)

        # Convert to float
        ohlc_df["open"] = ohlc_df["open"].astype(float)
        ohlc_df["high"] = ohlc_df["high"].astype(float)
        ohlc_df["low"] = ohlc_df["low"].astype(float)
        ohlc_df["close"] = ohlc_df["close"].astype(float)

        # Merge OHLC into main df
        df["open"] = ohlc_df["open"]
        df["high"] = ohlc_df["high"]
        df["low"] = ohlc_df["low"]

        # Fill any missing values
        df["open"] = df["open"].fillna(df["close"])
        df["high"] = df["high"].fillna(df["close"])
        df["low"] = df["low"].fillna(df["close"])

    except Exception:
        # Fallback — if Binance fails use close price
        df["open"] = df["close"]
        df["high"] = df["close"]
        df["low"] = df["close"]

    return df