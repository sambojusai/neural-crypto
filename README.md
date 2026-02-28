# 📈 Crypto Price Predictor (BTC & ETH)

A **Streamlit-based cryptocurrency price prediction web application** that uses a **deep learning LSTM model** to predict the **next-day price** of **Bitcoin (BTC)** and **Ethereum (ETH)**.

The app also displays **live prices**, **TradingView-style candlestick charts**, and **historical price trends** using real market data.

---

## 🚀 Features

- 🔥 **Live Bitcoin & Ethereum Price**
- 🤖 **AI-based Next-Day Price Prediction (LSTM)**
- 📊 **TradingView-style Candlestick Chart (Last 24 Hours)**
- 📉 **Last 60 Days Closing Price Chart**
- ⚡ Interactive **Streamlit Dashboard**
- ☁️ **Streamlit Cloud Deployable**

---

## 🧠 Machine Learning Model

- **Model Type:** LSTM (Long Short-Term Memory)
- **Framework:** TensorFlow / Keras
- **Input Window:** Last 60 days
- **Output:** Next-day closing price
- **Scaler:** MinMaxScaler (saved using Joblib)
- **Models:** Separate models for BTC and ETH

> ⚠️ This project is for **educational purposes only**.  
> It is **NOT financial advice**.

---
## 📂 Project Structure

crypto-price-predictor/
│
├── app.py # Streamlit frontend
├── requirements.txt # Python dependencies
│
├── model/
│ ├── bitcoin_model.h5 # Trained BTC model
│ ├── ethereum_model.h5 # Trained ETH model
│ └── scaler.pkl # Saved MinMaxScaler
│
├── src/
│ ├── init.py
│ ├── crypto_loader.py # Live & historical data loaders
│ ├── predict.py # Prediction logic
│ ├── preprocess.py # Scaling utilities
│ ├── model_builder.py # LSTM architecture
│ └── train.py # Model training script
│
├── .gitignore
└── README.md

yaml
Copy code

---

## 📊 Data Sources

- **Live Prices:** CoinGecko API  
- **Historical Prices:** CoinGecko  
- **Candlestick (OHLC):** Binance API  

---


This project is Streamlit Cloud ready.

Steps:
Push code to GitHub

Visit 👉 https://share.streamlit.io

Select:

Repository: crypto-price-predictor

Branch: main

Main file: app.py

Click Deploy

⚠️ Disclaimer
Cryptocurrency markets are highly volatile.
This application is built for learning and demonstration purposes only.

Do NOT use it for real trading or financial decisions.

👨‍💻 Author
Samboju Sai Charan
B.Tech – Artificial Intelligence
Crypto Price Prediction Project 🚀


