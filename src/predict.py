import os
import numpy as np
import tensorflow as tf

from tensorflow.keras.models import load_model
from src.crypto_loader import load_crypto_data
from src.preprocess import load_scaler

tf.keras.backend.clear_session()


def predict_price(symbol="bitcoin"):
    try:
        symbol = symbol.lower()

        model_path = f"model/{symbol}_model.h5"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found for {symbol}")

        # Load model (SAFE)
        model = load_model(model_path, compile=False)

        # Load scaler
        scaler = load_scaler(symbol)

        # Load historical data
        data = load_crypto_data(symbol)
        if len(data) < 60:
            raise ValueError("Not enough historical data")

        # Use last 60 close prices
        last_60 = data["close"].tail(60).values.reshape(-1, 1)
        last_60_scaled = scaler.transform(last_60)

        X_test = last_60_scaled.reshape(1, 60, 1)

        # Predict
        predicted_scaled = model.predict(X_test, verbose=0)
        predicted_price = scaler.inverse_transform(predicted_scaled)

        return float(predicted_price[0][0])

    except Exception as e:
        raise Exception(f"Prediction failed: {e}")