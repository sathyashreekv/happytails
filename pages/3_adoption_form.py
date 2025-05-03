# import streamlit as st
# from bson import ObjectId
# from database import pet_collection, request_collection


# # --- Streamlit page config ---
# st.set_page_config(page_title="Adopt a Pet", layout="wide")
# st.title("🐾 Adopt a Pet")
# st.markdown("Browse and adopt your new best friend!")


# # --- Search bar ---
# search_term = st.text_input("🔍 Search by name or breed")


# # --- Fetch available pets ---
# if search_term:
#     pets = pet_collection.find({
#         "$and": [
#             {"available": True},
#             {"$or": [
#                 {"name": {"$regex": search_term, "$options": "i"}},
#                 {"breed": {"$regex": search_term, "$options": "i"}}
#             ]}
#         ]
#     })
# else:
#     pets = pet_collection.find({"available": True})


# # --- Display pets ---
# for pet in pets:
#     unique_id = str(pet["_id"])
#     with st.container():
#         cols = st.columns([1, 2])
#         with cols[0]:
#             # st.image(pet.get("image", "https://placekitten.com/200/200"), width=250)
#             st.image(pet.get("image") or "https://placekitten.com/200/200", width=250)



#         with cols[1]:
#             st.subheader(pet["name"])
#             st.markdown(f"""
#                 - **Breed**: {pet['breed']}
#                 - **Age**: {pet['age']} years
#                 - **About**: {pet.get('description', 'No description available.')}
#             """)


#             if st.button(f"Adopt {pet['name']}", key=f"btn_{unique_id}"):
#                 with st.form(f"adopt_form_{unique_id}"):
#                     st.subheader(f"📝 Adoption Form for {pet['name']}")
#                     user_name = st.text_input("Your Full Name", key=f"name_{unique_id}")
#                     email = st.text_input("Email Address", key=f"email_{unique_id}")
#                     reason = st.text_area("Why do you want to adopt this pet?", key=f"reason_{unique_id}")
#                     submitted = st.form_submit_button("Submit Request")


#                 if submitted:
#                         if user_name and email and reason:
#                             try:
#                                 # Insert into adoption requests
#                                 request_collection.insert_one({
#                                     "pet_id": pet["_id"],
#                                     "pet_name": pet["name"],
#                                     "user_name": user_name,
#                                     "email": email,
#                                     "reason": reason,
#                                     "status": "pending"
#                                 })


#                                 # Mark the pet as unavailable
#                                 pet_collection.update_one(
#                                     {"_id": pet["_id"]},
#                                     {"$set": {"available": False}}
#                                 )


#                                 st.success(f"🎉 Your request to adopt {pet['name']} has                                                       been submitted!")
#                                 st.balloons()


#                             except Exception as e:
#                                 st.error("❌ Failed to submit adoption request.")
#                                 st.write(e)
#                         else:
#                             st.warning("Please fill all fields before submitting.")
 


# import streamlit as st
# from bson import ObjectId
# from database import pet_collection, request_collection

# # --- Streamlit page config ---
# st.set_page_config(page_title="Adopt a Pet", layout="wide")
# st.title("🐾 Adopt a Pet")
# st.markdown("Browse and adopt your new best friend!")

# # --- Search bar ---
# search_term = st.text_input("🔍 Search by name or breed")

# # --- Fetch available pets ---
# if search_term:
#     pets = pet_collection.find({
#         "$and": [
#             {"available": True},
#             {"$or": [
#                 {"name": {"$regex": search_term, "$options": "i"}},
#                 {"breed": {"$regex": search_term, "$options": "i"}}
#             ]}
#         ]
#     })
# else:
#     pets = pet_collection.find({"available": True})

# # --- Display pets ---
# for pet in pets:
#     unique_id = str(pet["_id"])
#     with st.container():
#         cols = st.columns([1, 2])
#         with cols[0]:
#             st.image(pet.get("image") or "https://placekitten.com/200/200", width=250)

#         with cols[1]:
#             st.subheader(pet["name"])
#             st.markdown(f"""
#                 - **Breed**: {pet['breed']}
#                 - **Age**: {pet['age']} years
#                 - **About**: {pet.get('description', 'No description available.')}
#             """)

#             with st.expander(f"🐶 Adopt {pet['name']}"):
#                 with st.form(f"adopt_form_{unique_id}"):
#                     st.subheader(f"📝 Adoption Form for {pet['name']}")
#                     user_name = st.text_input("Your Full Name", key=f"name_{unique_id}")
#                     email = st.text_input("Email Address", key=f"email_{unique_id}")
#                     reason = st.text_area("Why do you want to adopt this pet?", key=f"reason_{unique_id}")
#                     submitted = st.form_submit_button("Submit Request")

#                     if submitted:
#                         if user_name and email and reason:
#                             try:
#                                 # Insert into adoption requests
#                                 request_collection.insert_one({
#                                     "pet_id": pet["_id"],
#                                     "pet_name": pet["name"],
#                                     "user_name": user_name,
#                                     "email": email,
#                                     "reason": reason,
#                                     "status": "pending"
#                                 })

#                                 # Mark the pet as unavailable
#                                 pet_collection.update_one(
#                                     {"_id": pet["_id"]},
#                                     {"$set": {"available": False}}
#                                 )

#                                 st.success(f"🎉 Your request to adopt {pet['name']} has been submitted!")
#                                 st.balloons()
#                             except Exception as e:
#                                 st.error("❌ Failed to submit adoption request.")
#                                 st.write(e)
#                         else:
#                             st.warning("Please fill all fields before submitting.")






import streamlit as st
from bson import ObjectId
from database import pet_collection, request_collection

# --- Streamlit page config ---
st.set_page_config(page_title="Adopt a Pet", layout="wide")
st.title("🐾 Adopt a Pet")
st.markdown("Browse and adopt your new best friend!")

# --- Search bar ---
search_term = st.text_input("🔍 Search by name or breed")

# --- Fetch available pets ---
if search_term:
    pets = list(pet_collection.find({
        "$and": [
            {"available": True},
            {"$or": [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"breed": {"$regex": search_term, "$options": "i"}}
            ]}
        ]
    }))
else:
    pets = list(pet_collection.find({"available": True}))

# --- Show message if no pets found ---
if not pets:
    st.info("😿 No available pets found. Try adjusting your search.")

# --- Display pets ---
for pet in pets:
    unique_id = str(pet["_id"])
    with st.container():
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(pet.get("image") or "https://placekitten.com/200/200", width=250)

        with cols[1]:
            st.subheader(pet["name"])
            st.markdown(f"""
                - **Breed**: {pet['breed']}
                - **Age**: {pet['age']} years
                - **About**: {pet.get('description', 'No description available.')}
            """)

            with st.expander(f"🐶 Adopt {pet['name']}"):
                with st.form(f"adopt_form_{unique_id}"):
                    st.subheader(f"📝 Adoption Form for {pet['name']}")
                    user_name = st.text_input("Your Full Name", key=f"name_{unique_id}")
                    email = st.text_input("Email Address", key=f"email_{unique_id}")
                    reason = st.text_area("Why do you want to adopt this pet?", key=f"reason_{unique_id}")
                    submitted = st.form_submit_button("Submit Request")

                    if submitted:
                        if user_name and email and reason:
                            try:
                                # Insert into adoption requests
                                request_collection.insert_one({
                                    "pet_id": pet["_id"],
                                    "pet_name": pet["name"],
                                    "user_name": user_name,
                                    "email": email,
                                    "reason": reason,
                                    "status": "pending"
                                })

                                # Mark the pet as unavailable
                                pet_collection.update_one(
                                    {"_id": pet["_id"]},
                                    {"$set": {"available": False}}
                                )

                                st.success(f"🎉 Your request to adopt {pet['name']} has been submitted!")
                                st.balloons()
                                st.experimental_rerun()  # Force refresh
                            except Exception as e:
                                st.error("❌ Failed to submit adoption request.")
                                st.write(e)
                        else:
                            st.warning("Please fill all fields before submitting.")














