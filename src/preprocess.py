import os
import joblib
from sklearn.preprocessing import MinMaxScaler

MODEL_DIR = "model"


def save_scaler(scaler, symbol):
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"{symbol}_scaler.pkl")
    joblib.dump(scaler, path)


def load_scaler(symbol):
    path = os.path.join(MODEL_DIR, f"{symbol}_scaler.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Scaler not found for {symbol}")
    return joblib.load(path)


def scale_data(data, symbol):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(data)
    save_scaler(scaler, symbol)
    return scaled, scaler