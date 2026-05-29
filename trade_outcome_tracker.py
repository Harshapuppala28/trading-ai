import yfinance as yf

from pymongo import MongoClient


client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["trading_ai"]

collection = db["patterns"]

symbol = "GC=F"


def evaluate_pending_trades():

    pending_trades = collection.find({

        "result": "PENDING"
    })

    ticker = yf.Ticker(symbol)

    current_price = ticker.history(
        period="1d",
        interval="5m"
    )['Close'].iloc[-1]

    for trade in pending_trades:

        entry_price = trade['price']

        bullish_score = trade['bullish_score']

        bearish_score = trade['bearish_score']

        trade_id = trade['_id']

        result = "LOSS"

        if bullish_score > bearish_score:

            if current_price > entry_price:

                result = "WIN"

        elif bearish_score > bullish_score:

            if current_price < entry_price:

                result = "WIN"

        collection.update_one(

            {"_id": trade_id},

            {

                "$set": {

                    "future_price": float(current_price),

                    "result": result
                }
            }
        )

        print(
            f"Trade Updated: {result}"
        )


if __name__ == "__main__":

    evaluate_pending_trades()