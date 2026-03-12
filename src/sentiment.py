import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Your NewsAPI key - load from environment
from dotenv import load_dotenv
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CRYPTO_KEYWORDS = {
    "bitcoin": "bitcoin BTC crypto",
    "ethereum": "ethereum ETH crypto"
}


def fetch_news_headlines(symbol="bitcoin", num_articles=20):
    """Fetch latest crypto news headlines from NewsAPI"""
    try:
        query = CRYPTO_KEYWORDS.get(symbol, symbol)

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": num_articles,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        articles = response.json().get("articles", [])
        headlines = [a["title"] for a in articles if a["title"]]

        return headlines

    except Exception as e:
        print(f"News fetch error: {e}")
        return []


def analyze_sentiment(headlines):
    """
    Analyze sentiment of headlines using VADER
    Returns score between 0 and 1
    0 = Very Negative
    0.5 = Neutral
    1 = Very Positive
    """
    if not headlines:
        return 0.5  # neutral if no news

    scores = []
    for headline in headlines:
        score = analyzer.polarity_scores(headline)
        # compound score is between -1 and 1
        scores.append(score["compound"])

    # Average all scores
    avg_score = sum(scores) / len(scores)

    # Convert from (-1, 1) to (0, 1)
    normalized = (avg_score + 1) / 2

    return round(normalized, 4)


def get_crypto_sentiment(symbol="bitcoin"):
    """
    Main function — fetch news and return sentiment
    Returns:
        score: 0 to 1 (0=bearish, 1=bullish)
        label: Bullish / Bearish / Neutral
        headlines: list of headlines analyzed
    """
    headlines = fetch_news_headlines(symbol)
    score = analyze_sentiment(headlines)

    # Label based on score
    if score >= 0.6:
        label = "🟢 Bullish"
    elif score <= 0.4:
        label = "🔴 Bearish"
    else:
        label = "🟡 Neutral"

    return {
        "score": score,
        "label": label,
        "headlines": headlines[:5],  # return top 5 headlines
        "total_analyzed": len(headlines)
    }