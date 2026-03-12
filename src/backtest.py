import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import joblib
import os


def run_backtest(df, symbol="bitcoin", initial_capital=10000):
    """
    Backtest the LSTM model on historical data
    Simulates trading based on model predictions
    """
    try:
        # Load model and scaler
        model_path = f"model/{symbol}_model.h5"
        scaler_path = f"model/{symbol}_scaler.pkl"

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found for {symbol}")

        model = load_model(model_path, compile=False)
        scaler = joblib.load(scaler_path)

        # Get closing prices
        closes = df["close"].values
        dates = df.index

        # We need at least 60 days for prediction + 30 days for testing
        if len(closes) < 90:
            raise ValueError("Not enough data for backtesting")

        # Use last 30 days for backtesting
        backtest_days = 30
        seq_length = 60

        predictions = []
        actuals = []
        backtest_dates = []

        # For each day in backtest period, predict and compare
        start_idx = len(closes) - backtest_days

        for i in range(backtest_days - 1):
            # Get 60 days before current position
            idx = start_idx + i
            if idx < seq_length:
                continue

            # Prepare input sequence
            sequence = closes[idx - seq_length:idx].reshape(-1, 1)
            scaled_seq = scaler.transform(sequence)
            X = scaled_seq.reshape(1, seq_length, 1)

            # Predict
            pred_scaled = model.predict(X, verbose=0)
            pred_price = scaler.inverse_transform(pred_scaled)[0][0]

            # Actual next day price
            actual_price = closes[idx]

            predictions.append(pred_price)
            actuals.append(actual_price)
            backtest_dates.append(dates[idx])

        # Calculate results
        predictions = np.array(predictions)
        actuals = np.array(actuals)

        # Direction accuracy
        pred_directions = np.diff(predictions) > 0
        actual_directions = np.diff(actuals) > 0
        direction_accuracy = np.mean(pred_directions == actual_directions) * 100

        # Simulate trading
        capital = initial_capital
        position = 0
        trades = []

        for i in range(len(predictions) - 1):
            pred_direction = predictions[i + 1] > predictions[i]
            actual_return = (actuals[i + 1] - actuals[i]) / actuals[i]

            if pred_direction:  # Model says BUY
                profit = capital * actual_return
                capital += profit
                trades.append({
                    "date": backtest_dates[i],
                    "action": "BUY",
                    "return": round(actual_return * 100, 2),
                    "profit": round(profit, 2)
                })
            else:  # Model says SELL/HOLD
                trades.append({
                    "date": backtest_dates[i],
                    "action": "HOLD",
                    "return": 0,
                    "profit": 0
                })

        total_return = ((capital - initial_capital) / initial_capital) * 100
        winning_trades = len([t for t in trades if t["profit"] > 0])
        total_trades = len([t for t in trades if t["action"] == "BUY"])

        return {
            "direction_accuracy": round(direction_accuracy, 1),
            "total_return": round(total_return, 2),
            "final_capital": round(capital, 2),
            "initial_capital": initial_capital,
            "winning_trades": winning_trades,
            "total_trades": total_trades,
            "trades": trades[-10:],  # Last 10 trades
            "predictions": predictions.tolist(),
            "actuals": actuals.tolist(),
            "dates": [str(d) for d in backtest_dates]
        }

    except Exception as e:
        raise Exception(f"Backtest failed: {e}")