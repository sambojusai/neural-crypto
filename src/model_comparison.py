import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model


def prepare_data(prices, seq_length=60):
    X, y = [], []
    for i in range(seq_length, len(prices)):
        X.append(prices[i - seq_length:i])
        y.append(prices[i])
    return np.array(X), np.array(y)


def run_model_comparison(df, symbol="bitcoin"):
    """
    Fairly compare LSTM vs Linear Regression vs Random Forest
    ALL models tested on SAME test data
    """
    # Get closing prices
    prices = df["close"].values.reshape(-1, 1)

    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(prices)

    # Prepare sequences
    seq_length = 60
    X, y = prepare_data(scaled.flatten(), seq_length)

    # Train/Test split — 80% train, 20% test
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Inverse transform actual test prices
    y_test_actual = scaler.inverse_transform(
        y_test.reshape(-1, 1)
    ).flatten()

    results = {}

    # ------------------------------------------------
    # Model 1 — Linear Regression
    # ------------------------------------------------
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_predictions = lr_model.predict(X_test)
    lr_pred_actual = scaler.inverse_transform(
        lr_predictions.reshape(-1, 1)
    ).flatten()

    results["Linear Regression"] = {
        "mae": round(mean_absolute_error(y_test_actual, lr_pred_actual), 2),
        "rmse": round(np.sqrt(mean_squared_error(y_test_actual, lr_pred_actual)), 2),
    }

    # ------------------------------------------------
    # Model 2 — Random Forest
    # ------------------------------------------------
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    rf_pred_actual = scaler.inverse_transform(
        rf_predictions.reshape(-1, 1)
    ).flatten()

    results["Random Forest"] = {
        "mae": round(mean_absolute_error(y_test_actual, rf_pred_actual), 2),
        "rmse": round(np.sqrt(mean_squared_error(y_test_actual, rf_pred_actual)), 2),
    }

    # ------------------------------------------------
    # Model 3 — LSTM (FAIR comparison on same test data)
    # ------------------------------------------------
    try:
        model_path = f"model/{symbol}_model.h5"
        lstm_model = load_model(model_path, compile=False)

        # Load saved scaler for this symbol
        import joblib
        scaler_path = f"model/{symbol}_scaler.pkl"
        lstm_scaler = joblib.load(scaler_path)

        # Run LSTM on same test sequences
        X_test_lstm = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
        lstm_predictions = lstm_model.predict(X_test_lstm, verbose=0)
        lstm_pred_actual = lstm_scaler.inverse_transform(
            lstm_predictions
        ).flatten()

        # Use same y_test_actual for fair comparison
        y_test_lstm = scaler.inverse_transform(
            y_test.reshape(-1, 1)
        ).flatten()

        results["LSTM (Deep Learning)"] = {
            "mae": round(mean_absolute_error(y_test_lstm, lstm_pred_actual), 2),
            "rmse": round(np.sqrt(mean_squared_error(y_test_lstm, lstm_pred_actual)), 2),
        }

    except Exception as e:
        # Fallback if model not found
        results["LSTM (Deep Learning)"] = {
            "mae": "N/A",
            "rmse": "N/A",
        }

    return results, y_test_actual