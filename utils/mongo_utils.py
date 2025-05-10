from bson import ObjectId
from database import pet_collection, request_collection

# PET FUNCTIONS

def get_all_pets(query=None):
    """
    Retrieves a list of all pets from the pet collection based on the provided query.

    Args:
        query (dict): MongoDB query to filter the pets (default is None).

    Returns:
        list: A list of pet documents that match the query.
    """
    if query is None:
        query = {}  # Default to an empty query to return all pets
    return list(pet_collection.find(query))

def get_pet_by_id(pet_id):
    """
    Retrieves a pet's details by its unique ID.

    Args:
        pet_id (str): The unique ObjectId of the pet.

    Returns:
        dict: The pet document if found, or None if not found.
    """
    return pet_collection.find_one({"_id": ObjectId(pet_id)})

def add_pet(pet_data):
    """
    Adds a new pet profile to the pet collection.

    Args:
        pet_data (dict): The data to insert for the pet profile.
    """
    try:
        pet_collection.insert_one(pet_data)
    except Exception as e:
        print(f"Error inserting pet: {e}")

def update_pet(pet_id, update_data):
    """
    Updates the pet's profile with new data.

    Args:
        pet_id (str): The ID of the pet to update.
        update_data (dict): A dictionary containing the updated data.
    """
    try:
        pet_collection.update_one({"_id": ObjectId(pet_id)}, {"$set": update_data})
    except Exception as e:
        print(f"Error updating pet: {e}")

def delete_pet(pet_id):
    """
    Deletes a pet profile from the pet collection.

    Args:
        pet_id (str): The ID of the pet to delete.
    """
    try:
        pet_collection.delete_one({"_id": ObjectId(pet_id)})
    except Exception as e:
        print(f"Error deleting pet: {e}")

# ADOPTION REQUEST FUNCTIONS

def get_all_requests():
    """
    Retrieves all adoption requests from the request collection.

    Returns:
        list: A list of adoption request documents.
    """
    return list(request_collection.find())

def mark_pet_as_adopted(pet_id):
    """
    Marks a pet as adopted and unavailable in the pet collection.

    Args:
        pet_id (str): The ID of the pet to mark as adopted.
    """
    try:
        pet_collection.update_one(
            {"_id": ObjectId(pet_id)},
            {"$set": {"available": False, "status": "adopted"}}
        )
    except Exception as e:
        print(f"Error marking pet as adopted: {e}")

def add_adoption_request(request_data):
    """
    Adds an adoption request to the request collection.

    Args:
        request_data (dict): The data to insert for the adoption request.
    """
    try:
        request_collection.insert_one(request_data)
    except Exception as e:
        print(f"Error inserting adoption request: {e}")

def update_request_status(request_id, status):
    """
    Updates the status of an adoption request.

    Args:
        request_id (str): The ID of the adoption request to update.
        status (str): The new status to set for the adoption request.
    """
    try:
        request_collection.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": {"status": status}}
        )
    except Exception as e:
        print(f"Error updating request status: {e}")
