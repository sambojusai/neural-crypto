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

        model = load_model(model_path, compile=False)
        scaler = load_scaler(symbol)

        data = load_crypto_data(symbol)

        # Ensure we have enough data
        closes = data["close"].values
        if len(closes) < 61:
            raise ValueError(f"Not enough data: got {len(closes)}, need 61")

        # Take exactly 60 days
        last_60 = closes[-61:-1].reshape(-1, 1)
        last_60_scaled = scaler.transform(last_60)

        X_test = last_60_scaled.reshape(1, 60, 1)

        predicted_scaled = model.predict(X_test, verbose=0)
        predicted_price = scaler.inverse_transform(predicted_scaled)

        return float(predicted_price[0][0])

    except Exception as e:
        raise Exception(f"Prediction failed: {e}")