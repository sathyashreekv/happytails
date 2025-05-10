""" This is main db function file where i have written crud operations functions """
from bson import ObjectId
from database import pet_collection, request_collection

"""PET FUNCTIONS:This function gets all list of all pets in pet's collection"""
def get_all_pets(query=None):
    if query is None:
       return list(pet_collection.find(query))
"""This function gets pets object id """
def get_pet_by_id(pet_id):
    return pet_collection.find_one({"_id": ObjectId(pet_id)})
"""This function adds a new pet's profile to pets collection(creation of pet profile)"""
def add_pet(pet_data):
    pet_collection.insert_one(pet_data)
"""This function updates the pet's profile """
def update_pet(pet_id, update_data):
    pet_collection.update_one({"_id": ObjectId(pet_id)}, {"$set": update_data})
"""This function helps in deletion of pet profile when a pet is adopted"""
def delete_pet(pet_id):
    pet_collection.delete_one({"_id": ObjectId(pet_id)})
"""ADOPTION REQUEST FUNCTIONS"""
def get_all_requests():
    return list(request_collection.find())
"""This function marks as a pet as adopted when a adoption request is accepted by admin"""
def mark_pet_as_adopted(pet_id):
    # Mark pet as unavailable and set status (optional)
    pet_collection.update_one(
        {"_id": ObjectId(pet_id)},
        {"$set": {"available": False, "status": "adopted"}}
    )
"""--- ADOPTION REQUEST FUNCTIONS ---"""
"""function to submit a adoption request"""
def add_adoption_request(request_data):
    request_collection.insert_one(request_data)
"""Function to udpate the request of users """
def update_request_status(request_id, status):
    request_collection.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"status": status}}
    )
