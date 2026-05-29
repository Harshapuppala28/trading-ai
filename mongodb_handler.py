from pymongo import MongoClient

from datetime import datetime
from datetime import timedelta


client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["trading_ai"]

collection = db["patterns"]


def already_exists(
    pattern_name,
    timestamp
):

    current_time = datetime.strptime(
        timestamp,
        "%Y-%m-%d %H:%M:%S%z"
    )

    previous_time = (
        current_time - timedelta(minutes=30)
    )

    existing = collection.find_one({

        "pattern": pattern_name,

        "timestamp": {

            "$gte": str(previous_time),
            "$lte": timestamp
        }
    })

    if existing:
        return True

    return False


def save_pattern(
    pattern_name,
    latest,
    bullish_score,
    bearish_score,
    trend_15m,
    trend_1h,
    volume_spike,
    high_volatility
):

    timestamp = str(latest.name)

    if already_exists(
        pattern_name,
        timestamp
    ):

        print(
            f"⚠️ DUPLICATE SKIPPED: {pattern_name}"
        )

        return

    data = {

        "pattern": pattern_name,

        "price": float(
            latest['Close']
        ),

        "rsi": float(
            latest['RSI']
        ),

        "ema_9": float(
            latest['EMA_9']
        ),

        "ema_21": float(
            latest['EMA_21']
        ),

        "atr": float(
            latest['ATR']
        ),

        "bullish_score": bullish_score,

        "bearish_score": bearish_score,

        "trend_15m": trend_15m,

        "trend_1h": trend_1h,

        "volume_spike": volume_spike,

        "high_volatility": high_volatility,

        "result": "PENDING",

        "future_price": None,

        "timestamp": timestamp,

        "timeframe": "5m"
    }

    collection.insert_one(data)

    print(
        f"✅ SAVED TO MONGODB: {pattern_name}"
    )