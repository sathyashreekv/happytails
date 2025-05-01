from bson import ObjectId
from database import pet_collection, request_collection

# PET FUNCTIONS
def get_all_pets(query={}):
    return list(pet_collection.find(query))

def get_pet_by_id(pet_id):
    return pet_collection.find_one({"_id": ObjectId(pet_id)})

def add_pet(pet_data):
    pet_collection.insert_one(pet_data)

def update_pet(pet_id, update_data):
    pet_collection.update_one({"_id": ObjectId(pet_id)}, {"$set": update_data})

def delete_pet(pet_id):
    pet_collection.delete_one({"_id": ObjectId(pet_id)})

# ADOPTION REQUEST FUNCTIONS
def get_all_requests():
    return list(request_collection.find())

# def update_request_status(request_id, status):
#     request_collection.update_one({"_id": ObjectId(request_id)}, {"$set": {"status": status}})

# def mark_pet_as_adopted(pet_id):
#     pet_collection.update_one({"_id": ObjectId(pet_id)}, {"$set": {"status": "adopted"}})


def mark_pet_as_adopted(pet_id):
    # Mark pet as unavailable and set status (optional)
    pet_collection.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": {"available": False, "status": "adopted"}}
    )

# --- ADOPTION REQUEST FUNCTIONS ---

def add_adoption_request(request_data):
    request_collection.insert_one(request_data)

def update_request_status(request_id, status):
    request_collection.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": status}}
    )

