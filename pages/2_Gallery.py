"""This is gallery file """
import streamlit as st
from database import pet_collection
st.set_page_config(page_title="Pet Gallery", layout="wide")
st.title("🐾 Pet Gallery")
# Fetch all pets (not just available ones)
all_pets = list(pet_collection.find({}))
if not all_pets:
    st.info("No pets found in the database.")
else:
    # Display pets in a 3-column grid
    cols = st.columns(3)
    for index, pet in enumerate(all_pets):
        with cols[index % 3]:
            st.markdown("---")
            image_url = pet.get("image") or 
            "https://cdn.pixabay.com/photo/2016/02/19/10/00/dog-1209113_960_720.jpg"
            st.image(image_url, use_container_width=True)
            st.markdown(f"### {pet['name']}")
            st.markdown(f"**Breed:** {pet['breed']}")
            st.markdown(f"**Age:** {pet['age']} years")
