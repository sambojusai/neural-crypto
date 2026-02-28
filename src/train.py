import os
import argparse
import numpy as np

from src.crypto_loader import load_crypto_data
from src.preprocess import scale_data
from src.model_builder import build_model


def train_crypto(symbol="bitcoin", epochs=25):
    print(f"Loading data for {symbol}...")

    data = load_crypto_data(symbol)

    # Use only closing price
    prices = data["close"].values.reshape(-1, 1)

    # Scale data
    scaled, scaler = scale_data(prices, symbol)

    # Create sequences
    seq_length = 60
    X, y = [], []

    for i in range(seq_length, len(scaled)):
        X.append(scaled[i - seq_length:i])
        y.append(scaled[i])

    X, y = np.array(X), np.array(y)

    # Build model
    model = build_model((X.shape[1], 1))

    print("Training model...")
    model.fit(X, y, epochs=epochs, batch_size=32)

    # Save model
    os.makedirs("model", exist_ok=True)
    model.save(f"model/{symbol}_model.h5")



    print(f"Model trained and saved for {symbol}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", type=str, default="bitcoin")
    parser.add_argument("--epochs", type=int, default=25)
    args = parser.parse_args()

    train_crypto(args.symbol, args.epochs)
