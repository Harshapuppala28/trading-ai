from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017/"
)

db = client["trading_ai"]

collection = db["patterns"]

print("✅ MongoDB Connected Successfully")