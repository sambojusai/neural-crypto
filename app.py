import pandas as pd
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

    # Calculate MAE and RMSE — fixed array sizes
    closes = df["close"].values
    actual_for_naive = closes[-29:]      # 29 values
    naive_predictions = closes[-30:-1]   # 29 values — same size!

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
# SENTIMENT ANALYSIS
# -------------------------------
st.subheader("📰 Market Sentiment Analysis")

try:
    from src.sentiment import get_crypto_sentiment
    sentiment = get_crypto_sentiment(crypto)

    # Sentiment score bar
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Sentiment Score",
            value=f"{sentiment['score']:.2f} / 1.0"
        )
    with col2:
        st.metric(
            label="Market Mood",
            value=sentiment['label']
        )
    with col3:
        st.metric(
            label="Articles Analyzed",
            value=f"{sentiment['total_analyzed']} news"
        )

    # Show headlines
    st.markdown("**📰 Latest News Headlines:**")
    for headline in sentiment['headlines']:
        st.markdown(f"• {headline}")

except Exception as e:
    st.warning(f"Sentiment unavailable: {e}")
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
# MODEL COMPARISON
# -------------------------------
st.subheader("🤖 Model Comparison Dashboard")

with st.expander("📊 Click to see Model Comparison Analysis"):
    try:
        from src.model_comparison import run_model_comparison

        with st.spinner("Running model comparison... this takes 30 seconds"):
            comparison_results, actual_prices = run_model_comparison(df)

        # Show comparison table
        st.markdown("### 📈 Performance Comparison (Lower is Better)")

        comparison_data = {
            "Model": [],
            "MAE ($)": [],
            "RMSE ($)": [],
            "Performance": []
        }

        for model_name, metrics in comparison_results.items():
            comparison_data["Model"].append(model_name)
            comparison_data["MAE ($)"].append(metrics["mae"])
            comparison_data["RMSE ($)"].append(metrics["rmse"])

        # Find best model
        maes = comparison_data["MAE ($)"]
        min_mae = min(maes)
        for mae in maes:
            if mae == min_mae:
                comparison_data["Performance"].append("🏆 Best")
            else:
                comparison_data["Performance"].append("📊 Compared")

        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)

        st.markdown("### 💡 Why LSTM Wins?")
        st.markdown("""
        - **Linear Regression** assumes prices follow a straight line — too simple for volatile crypto
        - **Random Forest** is better but doesn't understand time sequences
        - **LSTM** remembers patterns from 60 days of history — best for time series data
        """)

    except Exception as e:
        st.warning(f"Model comparison unavailable: {e}")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This app is for educational purposes only. "
    "Not financial advice. Crypto markets are highly volatile."
)