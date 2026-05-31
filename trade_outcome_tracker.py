import os
import time
import ssl
from dotenv import load_dotenv
from pymongo import MongoClient

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
load_dotenv()

# ==========================================
# GET MONGO URI
# ==========================================
MONGO_URI = os.getenv("MONGO_URI")

# ==========================================
# CONNECT TO MONGODB ATLAS (With Robust SSL Context)
# ==========================================
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client = MongoClient(
    MONGO_URI, 
    ssl=True,
    ssl_context=ssl_context
)

db = client["trading_ai"]
collection = db["trade_history"]

print("✅ Trade Outcome Tracker Connected To MongoDB Atlas")

# ==========================================
# EVALUATE PENDING TRADES
# ==========================================
def evaluate_pending_trades():
    print("\n📊 Evaluating Pending Trades...")

    # INDENTATION FIXED: This entire block is now properly inside the function
    try:
        pending_trades = list(collection.find({
            "result": {
                "$exists": False
            }
        }))

        if not pending_trades:
            print("🔍 No pending trades to evaluate.")
            return

        for trade in pending_trades:
            print(f"🔍 Checking Trade: {trade.get('primary_pattern', trade.get('pattern', 'Unknown'))}")

            current_price = trade.get("future_price", trade.get("price"))
            entry_price = trade.get("price")
            
            if entry_price is None or current_price is None:
                print("⚠️ Skipping trade: Missing price data.")
                continue

            bullish_score = trade.get("bullish_score", 0)
            bearish_score = trade.get("bearish_score", 0)

            result = "LOSS"

            if bullish_score > bearish_score:
                if current_price > entry_price:
                    result = "WIN"
            elif bearish_score > bullish_score:
                if current_price < entry_price:
                    result = "WIN"

            collection.update_one(
                {"_id": trade["_id"]},
                {"$set": {"result": result}}
            )

            print(f"✅ Trade Updated: {result}")

    except Exception as e:
        print(f"❌ Trade Evaluation Error: {e}")