from pymongo import MongoClient
from config import Config

# MongoDB connection
try:
    client = MongoClient(Config.MONGO_URI)
    db = client.get_database()
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    db = None