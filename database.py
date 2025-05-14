"""This is a base database file here we created collections"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Connect to MongoDB Atlas
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# Use your database and collections
db = client["pet_database"]
users_collection = db["users"]
pet_collection = db["pets"]
request_collection = db["requests"]
audit_log_collection= db["audit_log"]
def log_event(username, action, success=True, role=None, details=""):
    from datetime import datetime
    audit_log_collection.insert_one({
        "username": username,
        "action": action,
        "timestamp": datetime.now(),
        "success": success,
        "role": role,
        "details": details
    })
# Test connection: print one user
print(users_collection.find_one())
