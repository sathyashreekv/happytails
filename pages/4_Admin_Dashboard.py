# import streamlit as st
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from bson.errors import InvalidId
# import os
# from PIL import Image
# from database import pet_collection, request_collection
# import time

# st.set_page_config(page_title="Admin Dashboard", layout="wide")
# st.title("🐾 Admin Dashboard")

# # --- Search & Filter --- #
# st.subheader("Search & Filter Pets")
# search_term = st.text_input("Search by Name, Breed, or Status")

# query = {"$or": [
#     {"name": {"$regex": search_term, "$options": "i"}},
#     {"breed": {"$regex": search_term, "$options": "i"}},
#     {"status": {"$regex": search_term, "$options": "i"}}
# ]} if search_term else {}

# pets = list(pet_collection.find(query))

# # --- Show all pets --- #
# st.markdown("### All Pets")
# if pets:
#     for pet in pets:
#         st.markdown(f"**Name:** {pet.get('name', '')} | **Breed:** {pet.get('breed', '')} | **Status:** {pet.get('status', 'available')}| **Next Vaccination:** {pet.get('next_vaccination', 'N/A')}")
# else:
#     st.info("No pets found.")

# # --- Edit or Delete Pet --- #
# st.subheader("✏️ Edit or Delete Pet")
# if pets:
#     pet_options = [f"{pet.get('name', 'Unnamed')} - {str(pet['_id'])}" for pet in pets]
#     selected_pet_str = st.selectbox("Select a pet to edit", pet_options)
#     selected_id = selected_pet_str.split(" - ")[-1]
#     selected_pet = pet_collection.find_one({"_id": ObjectId(selected_id)})

#     # Pre-filled form
#     name = st.text_input("Name", value=selected_pet.get("name", ""))
#     age = st.number_input("Age", value=selected_pet.get("age", 0), min_value=0)
#     breed = st.text_input("Breed", value=selected_pet.get("breed", ""))
#     health = st.text_area("Health Info", value=selected_pet.get("health", ""))
#     description = st.text_area("Description", value=selected_pet.get("description", ""))
#     status = st.selectbox("Status", ["available", "adopted", "pending"],
#                           index=["available", "adopted", "pending"].index(selected_pet.get("status", "available")))
#     import datetime

# # Convert to date object if exists
#     vaccination_date = selected_pet.get("next_vaccination")
#     if isinstance(vaccination_date, str):
#        try:
#            vaccination_date = datetime.datetime.strptime(vaccination_date, "%Y-%m-%d").date()
#        except:
#          vaccination_date = None

#      next_vaccination = st.date_input("Next Vaccination Date", value=vaccination_date or datetime.date.today())

#     # Show image
#     image_url = selected_pet.get("image", "")
#     if image_url:
#         st.image(image_url, width=200, caption="Current Image")

#     # Upload new image
#     uploaded_image = st.file_uploader("Upload New Image", type=["jpg", "jpeg", "png"])
#     if uploaded_image:
#         image_path = os.path.join("pet_images", uploaded_image.name)
#         os.makedirs("pet_images", exist_ok=True)
#         with open(image_path, "wb") as f:
#             f.write(uploaded_image.getbuffer())
#         image_url = image_path

#     # Update button
#     if st.button("Update Pet"):
#         if not name:
#             st.warning("Name is required.")
#         else:
#             update_fields = {
#                 "name": name,
#                 "age": age,
#                 "breed": breed,
#                 "health": health,
#                 "description": description,
#                 "status": status,
#                 "image": image_url,
#                 "next_vaccination": str(next_vaccination)
#             }
#             pet_collection.update_one({"_id": ObjectId(selected_id)}, {"$set": update_fields})
#             st.success("✅ Pet updated!")
#             st.rerun()

#     # Delete button
#     if st.button("❌ Delete Pet"):
#         pet_collection.delete_one({"_id": ObjectId(selected_id)})
#         st.warning("🗑️ Pet deleted!")
#         st.rerun()

# # --- Add New Pet Section --- #
# st.subheader("➕ Add New Pet")

# with st.form("add_pet"):
#     new_name = st.text_input("Pet Name")
#     new_age = st.number_input("Pet Age", min_value=0, step=1)
#     new_breed = st.text_input("Breed")
#     new_health = st.text_area("Health Info")
#     new_description = st.text_area("Description")
#     new_next_vaccination = st.date_input("Next Vaccination Date")
#     new_status = st.selectbox("Status", ["available", "adopted", "pending"])
#     new_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

#     submitted = st.form_submit_button("Add Pet")

#     if submitted:
#         if not new_name:
#             st.warning("Name is required.")
#         else:
#             image_path = ""
#             if new_image:
#                 os.makedirs("pet_images", exist_ok=True)
#                 image_path = os.path.join("pet_images", new_image.name)
#                 with open(image_path, "wb") as f:
#                     f.write(new_image.getbuffer())

#             new_pet = {
#                 "name": new_name,
#                 "age": new_age,
#                 "breed": new_breed,
#                 "health": new_health,
#                 "description": new_description,
#                 "status": new_status,
#                 "image": image_path,
#                 "next_vaccination": str(new_next_vaccination),

#             }

#             pet_collection.insert_one(new_pet)
#             st.balloons()
#             st.success("🎉 New pet added!")
#             st.rerun()

# # --- Helper Function for Adoption Requests --- #
# def handle_adoption_request(req, pet_collection, request_collection):
#     pet = None
#     try:
#         pet_id = ObjectId(req["pet_id"]) if not isinstance(req["pet_id"], ObjectId) else req["pet_id"]
#         pet = pet_collection.find_one({"_id": pet_id})
#     except (InvalidId, TypeError, KeyError):
#         pass
#     pet_name = pet.get("name", "Unknown") if pet else "Unknown"

#     st.markdown(f"""
#     **Request ID:** {str(req["_id"])}  
#     **Pet:** {pet_name}  
#     **User:** {req.get("user_name", "N/A")}  
#     **Contact:** {req.get("email", "N/A")}  
#     **Status:** {req.get("status", "pending")}  
#     """)

#     accepted = req.get("status") == "accepted"
#     rejected = req.get("status") == "rejected"

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("✅ Accept", key=f"accept_{req['_id']}", disabled=accepted ):
#             request_collection.update_one({"_id": req["_id"]}, {"$set": {"status": "accepted"}})
#             if pet:
#                 pet_collection.update_one({"_id": pet["_id"]}, {"$set": {"status": "adopted"}})
#             st.toast(f"🎉 Adoption request for {pet_name} has been accepted!", icon="🎊")
#             st.rerun()

#     with col2:
#         if st.button("❌ Reject", key=f"reject_{req['_id']}", disabled=accepted or rejected):
#             request_collection.update_one({"_id": req["_id"]}, {"$set": {"status": "rejected"}})
#             st.toast(f"❌ Adoption request for {pet_name} has been rejected.")
#             st.rerun()

# # --- Adoption Request Management --- #
# st.subheader("📋 Adoption Requests")
# requests = list(request_collection.find())

# if requests:
#     for req in requests:
#         handle_adoption_request(req, pet_collection, request_collection)
# else:
#     st.info("No adoption requests found.")

import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os
from PIL import Image
from database import pet_collection, request_collection
import datetime

# Streamlit page config
st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🐾 Admin Dashboard")

# --- Search & Filter --- #
st.subheader("Search & Filter Pets")
search_term = st.text_input("Search by Name, Breed, or Status")

query = {"$or": [
    {"name": {"$regex": search_term, "$options": "i"}},
    {"breed": {"$regex": search_term, "$options": "i"}},
    {"status": {"$regex": search_term, "$options": "i"}}
]} if search_term else {}

pets = list(pet_collection.find(query))

# --- Show All Pets --- #
st.markdown("### All Pets")
if pets:
    for pet in pets:
        st.markdown(
            f"**Name:** {pet.get('name', '')} | "
            f"**Breed:** {pet.get('breed', '')} | "
            f"**Status:** {pet.get('status', 'available')} | "
            f"**Next Vaccination:** {pet.get('next_vaccination', 'N/A')}"
        )
else:
    st.info("No pets found.")

# --- Edit or Delete Pet --- #
st.subheader("✏️ Edit or Delete Pet")
if pets:
    pet_options = [f"{pet.get('name', 'Unnamed')} - {str(pet['_id'])}" for pet in pets]
    selected_pet_str = st.selectbox("Select a pet to edit", pet_options)
    selected_id = selected_pet_str.split(" - ")[-1]
    selected_pet = pet_collection.find_one({"_id": ObjectId(selected_id)})

    # Pre-filled form
    name = st.text_input("Name", value=selected_pet.get("name", ""))
    age = st.number_input("Age", value=selected_pet.get("age", 0), min_value=0)
    breed = st.text_input("Breed", value=selected_pet.get("breed", ""))
    health = st.text_area("Health Info", value=selected_pet.get("health", ""))
    description = st.text_area("Description", value=selected_pet.get("description", ""))
    status = st.selectbox("Status", ["available", "adopted", "pending"],
                          index=["available", "adopted", "pending"].index(selected_pet.get("status", "available")))

    # Handle vaccination date
    vaccination_date = selected_pet.get("next_vaccination")
    if isinstance(vaccination_date, str):
        try:
            vaccination_date = datetime.datetime.strptime(vaccination_date, "%Y-%m-%d").date()
        except:
            vaccination_date = datetime.date.today()
    else:
        vaccination_date = datetime.date.today()

    next_vaccination = st.date_input("Next Vaccination Date", value=vaccination_date)

    # Show existing image
    image_url = selected_pet.get("image", "")
    if image_url and os.path.exists(image_url):
        st.image(image_url, width=200, caption="Current Image")

    # Upload new image
    uploaded_image = st.file_uploader("Upload New Image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        os.makedirs("pet_images", exist_ok=True)
        image_path = os.path.join("pet_images", uploaded_image.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        image_url = image_path

    # Update button
    if st.button("Update Pet"):
        if not name:
            st.warning("Name is required.")
        else:
            update_fields = {
                "name": name,
                "age": age,
                "breed": breed,
                "health": health,
                "description": description,
                "status": status,
                "image": image_url,
                "next_vaccination": str(next_vaccination)
            }
            pet_collection.update_one({"_id": ObjectId(selected_id)}, {"$set": update_fields})
            st.success("✅ Pet updated!")
            st.rerun()

    # Delete button
    if st.button("❌ Delete Pet"):
        pet_collection.delete_one({"_id": ObjectId(selected_id)})
        st.warning("🗑️ Pet deleted!")
        st.rerun()

# --- Add New Pet --- #
st.subheader("➕ Add New Pet")

with st.form("add_pet"):
    new_name = st.text_input("Pet Name")
    new_age = st.number_input("Pet Age", min_value=0, step=1)
    new_breed = st.text_input("Breed")
    new_health = st.text_area("Health Info")
    new_description = st.text_area("Description")
    new_next_vaccination = st.date_input("Next Vaccination Date")
    new_status = st.selectbox("Status", ["available", "adopted", "pending"])
    new_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    submitted = st.form_submit_button("Add Pet")

    if submitted:
        if not new_name:
            st.warning("Name is required.")
        else:
            image_path = ""
            if new_image:
                os.makedirs("pet_images", exist_ok=True)
                image_path = os.path.join("pet_images", new_image.name)
                with open(image_path, "wb") as f:
                    f.write(new_image.getbuffer())

            new_pet = {
                "name": new_name,
                "age": new_age,
                "breed": new_breed,
                "health": new_health,
                "description": new_description,
                "status": new_status,
                "image": image_path,
                "next_vaccination": str(new_next_vaccination),
            }

            pet_collection.insert_one(new_pet)
            st.balloons()
            st.success("🎉 New pet added!")
            st.rerun()

# --- Helper Function for Adoption Requests --- #
def handle_adoption_request(req, pet_collection, request_collection):
    pet = None
    try:
        pet_id = ObjectId(req["pet_id"]) if not isinstance(req["pet_id"], ObjectId) else req["pet_id"]
        pet = pet_collection.find_one({"_id": pet_id})
    except (InvalidId, TypeError, KeyError):
        pass
    pet_name = pet.get("name", "Unknown") if pet else "Unknown"

    st.markdown(f"""
    **Request ID:** {str(req["_id"])}  
    **Pet:** {pet_name}  
    **User:** {req.get("user_name", "N/A")}  
    **Contact:** {req.get("email", "N/A")}  
    **Status:** {req.get("status", "pending")}  
    """)

    accepted = req.get("status") == "accepted"
    rejected = req.get("status") == "rejected"

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Accept", key=f"accept_{req['_id']}", disabled=accepted):
            request_collection.update_one({"_id": req["_id"]}, {"$set": {"status": "accepted"}})
            if pet:
                pet_collection.update_one({"_id": pet["_id"]}, {"$set": {"status": "adopted"}})
            st.toast(f"🎉 Adoption request for {pet_name} has been accepted!", icon="🎊")
            st.rerun()

    with col2:
        if st.button("❌ Reject", key=f"reject_{req['_id']}", disabled=accepted or rejected):
            request_collection.update_one({"_id": req["_id"]}, {"$set": {"status": "rejected"}})
            st.toast(f"❌ Adoption request for {pet_name} has been rejected.")
            st.rerun()

# --- Adoption Request Management --- #
st.subheader("📋 Adoption Requests")
requests = list(request_collection.find())

if requests:
    for req in requests:
        handle_adoption_request(req, pet_collection, request_collection)
else:
    st.info("No adoption requests found.")
































