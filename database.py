# from pymongo import MongoClient
# from bson import ObjectId
# from pymongo import MongoClient
# import os

# client = MongoClient("mongodb://localhost:27017/pets")
# db = client["pet_database"]
# users_collection = db["users"]
# pet_collection = db["pets"]
# request_collection = db["requests"]


from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import gridfs

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

fs=gridfs.GridFS(db)

# Test connection: print one user
print(users_collection.find_one())
