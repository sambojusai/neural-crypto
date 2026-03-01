# 🧠 NeuralCrypto — AI Crypto Price Predictor

![Python](https://img.shields.io/badge/Python-3.11-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)
![License](https://img.shields.io/badge/License-MIT-green)

A **deep learning web application** that predicts the next-day price of **Bitcoin (BTC)** and **Ethereum (ETH)** using an **LSTM neural network**, built with TensorFlow/Keras and deployed via Streamlit.

> ⚠️ This project is for **educational purposes only** and is NOT financial advice.

---

## 🚀 Live Demo

👉 **[Coming Soon — Streamlit Cloud](#)**

---

## ✨ Features

- 🔥 **Live BTC & ETH Prices** — fetched in real-time via CoinGecko API
- 🤖 **AI Next-Day Price Prediction** — powered by LSTM deep learning model
- 📊 **Real Candlestick Charts** — OHLC data from Binance API
- 📉 **60-Day Historical Price Trend** — interactive line chart
- ⚡ **Fast & Responsive** — built with Streamlit, cached API calls

---

## 🧠 Machine Learning Architecture

| Component | Details |
|---|---|
| Model Type | LSTM (Long Short-Term Memory) |
| Framework | TensorFlow / Keras |
| Input | Last 60 days of closing prices |
| Output | Next-day predicted closing price |
| Optimizer | Adam |
| Loss Function | Mean Squared Error (MSE) |
| Regularization | Dropout (0.2) |
| Scaler | MinMaxScaler (0–1 normalization) |

### Why LSTM?
Crypto prices are **sequential and time-dependent**. LSTM networks are specifically designed to learn long-term patterns in sequential data, making them more suitable than traditional models like ARIMA for volatile, non-linear time series like cryptocurrency prices.

---

## 📂 Project Structure

```
neural-crypto/
│
├── app.py                  # Streamlit frontend dashboard
├── requirements.txt        # Python dependencies
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── crypto_loader.py    # CoinGecko + Binance API integration
│   ├── predict.py          # Prediction pipeline
│   ├── preprocess.py       # MinMaxScaler utilities
│   ├── model_builder.py    # LSTM architecture definition
│   └── train.py            # Model training script
│
└── model/                  # Saved models (not tracked in git)
    ├── bitcoin_model.h5
    ├── ethereum_model.h5
    ├── bitcoin_scaler.pkl
    └── ethereum_scaler.pkl
```

---

## 📊 Data Sources

| Data | Source | Details |
|---|---|---|
| Live Price | CoinGecko API | Real-time USD price |
| Historical Prices | CoinGecko API | 90 days daily closing |
| OHLC Candlestick | Binance API | Real open/high/low/close |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Deep Learning:** TensorFlow, Keras
- **Frontend:** Streamlit
- **Data Processing:** NumPy, Pandas, Scikit-learn
- **Visualization:** Plotly
- **APIs:** CoinGecko, Binance

---

## ⚙️ Run Locally

**1. Clone the repository:**
```bash
git clone https://github.com/sambojusai/neural-crypto.git
cd neural-crypto
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Train the models:**
```bash
python -m src.train --symbol bitcoin --epochs 25
python -m src.train --symbol ethereum --epochs 25
```

**5. Run the app:**
```bash
streamlit run app.py
```

Open 👉 `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to 👉 [share.streamlit.io](https://share.streamlit.io)
3. Select repository: `neural-crypto`
4. Set main file: `app.py`
5. Click **Deploy** ✅

---

## 👨‍💻 Author

**Samboju Sai Charan**
B.Tech — Artificial Intelligence
📧 [sambojusaicharan0@gmail.com]
🔗 [https://www.linkedin.com/in/samboju-saicharan-674aa436b/](#) | [GitHub](https://github.com/sambojusai)

---

## ⚠️ Disclaimer

Cryptocurrency markets are highly volatile. This application is built purely for **learning and demonstration** purposes. Do **NOT** use predictions for real trading or financial decisions.
