import os
import time
import certifi

from dotenv import load_dotenv
from pymongo import MongoClient

# ==========================================

# LOAD ENV VARIABLES

# ==========================================

load_dotenv()

# ==========================================

# GET MONGO URI

# ==========================================

MONGO_URI = os.getenv(
"MONGO_URI"
)

# ==========================================

# CONNECT TO MONGODB ATLAS

# ==========================================

client = MongoClient(
    MONGO_URI, 
    tls=True, 
    tlsAllowInvalidCertificates=True
)

db = client["trading_ai"]

collection = db["trade_history"]

print(
"✅ Trade Outcome Tracker Connected To MongoDB Atlas"
)

# ==========================================

# EVALUATE PENDING TRADES

# ==========================================

def evaluate_pending_trades():


 print(
    "\n📊 Evaluating Pending Trades..."
 )

try:

    pending_trades = collection.find(
        {
            "result": {
                "$exists": False
            }
        }
    )

    for trade in pending_trades:

        print(
            f"🔍 Checking Trade: {trade.get('pattern')}"
        )

        current_price = trade.get(
            "future_price",
            trade.get("price")
        )

        entry_price = trade.get(
            "price"
        )

        bullish_score = trade.get(
            "bullish_score",
            0
        )

        bearish_score = trade.get(
            "bearish_score",
            0
        )

        result = "LOSS"

        if bullish_score > bearish_score:

            if current_price > entry_price:

                result = "WIN"

        elif bearish_score > bullish_score:

            if current_price < entry_price:

                result = "WIN"

        collection.update_one(

            {
                "_id": trade["_id"]
            },

            {
                "$set": {
                    "result": result
                }
            }

        )

        print(
            f"✅ Trade Updated: {result}"
        )

except Exception as e:

    print(
        f"❌ Trade Evaluation Error: {e}"
    )

