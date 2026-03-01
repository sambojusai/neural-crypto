import streamlit as st
import plotly.graph_objects as go
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.crypto_loader import load_crypto_data
from src.predict import predict_price

st.set_page_config(
    page_title="NeuralCrypto - AI Price Predictor",
    layout="wide"
)

st.title("🧠 NeuralCrypto — AI Crypto Price Predictor")

# -------------------------------
# SELECT CRYPTO
# -------------------------------
crypto = st.selectbox(
    "Select Cryptocurrency",
    ["bitcoin", "ethereum"]
)

# -------------------------------
# LOAD DATA
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
prev_price = df["close"].iloc[-2]
price_change = live_price - prev_price
price_change_pct = (price_change / prev_price) * 100

st.metric(
    label=f"{crypto.capitalize()} Price (USD)",
    value=f"${live_price:,.2f}",
    delta=f"{price_change_pct:.2f}% vs yesterday"
)

# -------------------------------
# AI PREDICTION + METRICS
# -------------------------------
st.subheader("📈 AI Predicted Next-Day Price")

try:
    prediction = predict_price(crypto)

    # UP or DOWN indicator
    if prediction > live_price:
        direction = "📈 UP"
        color = "green"
    else:
        direction = "📉 DOWN"
        color = "red"

    # Calculate MAE and RMSE (naive baseline on last 30 days)
    naive_predictions = df["close"].shift(1).tail(30).dropna().values
    actual_for_naive = df["close"].tail(30).iloc[1:].values

    mae = mean_absolute_error(actual_for_naive, naive_predictions)
    rmse = np.sqrt(mean_squared_error(actual_for_naive, naive_predictions))

    # Show 3 columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🤖 Tomorrow's Prediction",
            value=f"${prediction:,.2f}"
        )
    with col2:
        st.metric(
            label="📊 MAE (Avg Error)",
            value=f"${mae:,.2f}"
        )
    with col3:
        st.metric(
            label="📉 RMSE (Error Score)",
            value=f"${rmse:,.2f}"
        )

    # Direction indicator
    st.markdown(f"### Market Direction: :{color}[{direction}]")

except Exception as e:
    st.error(f"Prediction error: {e}")

# -------------------------------
# CANDLESTICK CHART
# -------------------------------
st.subheader("📊 Price Movement — Last 90 Days (TradingView Style)")

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
        title=f"{crypto.capitalize()} — OHLC Candlestick Chart",
        xaxis_rangeslider_visible=False,
        height=500,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Candlestick error: {e}")

# -------------------------------
# LAST 60 DAYS LINE CHART
# -------------------------------
st.subheader("📉 Last 60 Days Closing Price")

history = df.tail(60)
st.line_chart(history["close"])

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This app is for educational purposes only. "
    "Not financial advice. Crypto markets are highly volatile."
)