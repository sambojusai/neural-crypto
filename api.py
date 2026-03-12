from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.predict import predict_price
from src.crypto_loader import load_crypto_data
from src.sentiment import get_crypto_sentiment
import uvicorn

app = FastAPI(
    title="NeuralCrypto API",
    description="AI-powered Crypto Price Prediction API using LSTM",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "Welcome to NeuralCrypto API!",
        "version": "1.0.0",
        "endpoints": [
            "/predict?symbol=bitcoin",
            "/sentiment?symbol=bitcoin",
            "/price?symbol=bitcoin"
        ]
    }


@app.get("/predict")
def predict(symbol: str = "bitcoin"):
    try:
        symbol = symbol.lower()
        if symbol not in ["bitcoin", "ethereum"]:
            raise HTTPException(
                status_code=400,
                detail="Symbol must be 'bitcoin' or 'ethereum'"
            )

        predicted_price = predict_price(symbol)
        df = load_crypto_data(symbol)
        current_price = df["close"].iloc[-1]
        direction = "UP" if predicted_price > current_price else "DOWN"
        change_pct = ((predicted_price - current_price) / current_price) * 100

        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "predicted_price": round(predicted_price, 2),
            "direction": direction,
            "change_percentage": round(change_pct, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/price")
def get_price(symbol: str = "bitcoin"):
    try:
        symbol = symbol.lower()
        if symbol not in ["bitcoin", "ethereum"]:
            raise HTTPException(
                status_code=400,
                detail="Symbol must be 'bitcoin' or 'ethereum'"
            )

        df = load_crypto_data(symbol)
        current_price = df["close"].iloc[-1]
        prev_price = df["close"].iloc[-2]
        change_pct = ((current_price - prev_price) / prev_price) * 100

        return {
            "symbol": symbol,
            "price": round(current_price, 2),
            "change_24h": round(change_pct, 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sentiment")
def get_sentiment(symbol: str = "bitcoin"):
    try:
        symbol = symbol.lower()
        if symbol not in ["bitcoin", "ethereum"]:
            raise HTTPException(
                status_code=400,
                detail="Symbol must be 'bitcoin' or 'ethereum'"
            )

        sentiment = get_crypto_sentiment(symbol)

        return {
            "symbol": symbol,
            "sentiment_score": sentiment["score"],
            "market_mood": sentiment["label"],
            "articles_analyzed": sentiment["total_analyzed"],
            "top_headlines": sentiment["headlines"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)