import streamlit as st
import plotly.graph_objects as go

from src.crypto_loader import load_crypto_data
from src.predict import predict_price

st.set_page_config(
    page_title="Crypto Price Prediction",
    layout="wide"
)

st.title("🚀 Crypto Price Prediction (BTC & ETH)")

# -------------------------------
# SELECT CRYPTO
# -------------------------------
crypto = st.selectbox(
    "Select Cryptocurrency",
    ["bitcoin", "ethereum"]
)

# -------------------------------
# LOAD DATA ONCE (CRITICAL FIX)
# -------------------------------
try:
    df = load_crypto_data(crypto)
except Exception as e:
    st.error(e)
    st.warning("⚠️ CoinGecko rate limit reached. Please wait 1–2 minutes and refresh.")
    st.stop()

# -------------------------------
# LIVE PRICE
# -------------------------------
st.subheader("🔥 Live Price")

live_price = df["close"].iloc[-1]
st.metric(
    label=f"{crypto.capitalize()} Price (USD)",
    value=f"${live_price:,.2f}"
)

# -------------------------------
# AI PREDICTION
# -------------------------------
st.subheader("📈 AI Predicted Next-Day Price")

try:
    prediction = predict_price(crypto)
    st.success(f"Predicted Price: ${prediction:,.2f}")
except Exception as e:
    st.error(e)

# -------------------------------
# CANDLESTICK CHART
# -------------------------------
st.subheader("📊 Today's Price Movement (TradingView Style)")

try:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"]
            )
        ]
    )

    fig.update_layout(
        title=f"{crypto.capitalize()} Price",
        xaxis_rangeslider_visible=False,
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Candlestick error: {e}")

# -------------------------------
# LAST 60 DAYS
# -------------------------------
st.subheader("📉 Last 60 Days Closing Price")

history = df.tail(60)
st.line_chart(history["close"])
