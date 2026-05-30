import os

from dotenv import load_dotenv

from pymongo import MongoClient


# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# MONGODB URI
# ==========================================

MONGO_URI = os.getenv(
    "MONGO_URI"
)


# ==========================================
# CONNECT TO MONGODB ATLAS
# ==========================================

client = MongoClient(MONGO_URI)

db = client["trading_ai"]

collection = db["trade_history"]


print(
    "✅ Connected to MongoDB Atlas"
)


# ==========================================
# SAVE PATTERN
# ==========================================

def save_pattern(data):

    try:

        collection.insert_one(data)

        print(
            "✅ Pattern Saved To MongoDB"
        )

    except Exception as e:

        print(
            f"❌ MongoDB Save Error: {e}"
        )