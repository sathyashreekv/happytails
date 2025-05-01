
import streamlit as st
import pymongo
import bcrypt

from bson import ObjectId
from database import users_collection as users_col

# Page config
st.set_page_config(page_title="HappyTails Auth", layout="wide")

# CSS
st.markdown("""
    <style>
      
            
        .stApp {
        background-image:url("https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_1280.jpg");


        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
     .center-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .form-container {
            backdrop-filter: blur(10px);
            background-color: rgba(255, 255, 255, 0.15);
            padding: 3rem 2rem;
            border-radius: 20px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            color: white;
        }
        h2 {
            text-align: center;
            color: white;
        }
        .stTextInput>div>input, .stSelectbox>div>div>div {
            background-color: rgba(255,255,255,0.8);
            color: black;
        }
        .stButton>button {
            background-color: #0066cc;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "mode" not in st.session_state:
    st.session_state.mode = "Login"

# Toggle form
st.markdown('<div class="center-wrap"><div class="form-container">', unsafe_allow_html=True)
st.markdown(f"<h2>{st.session_state.mode}</h2>", unsafe_allow_html=True)

# Switch button
if st.button("Switch to " + ("Sign Up" if st.session_state.mode == "Login" else "Login")):
    st.session_state.mode = "Sign Up" if st.session_state.mode == "Login" else "Login"
    st.rerun()

# Login Form
if st.session_state.mode == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = users_col.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            st.success("✅ Logged in!")
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = user["role"]
            if user["role"] == "admin":
                st.switch_page("pages/4_Admin_Dashboard.py")
            else:
                st.switch_page("pages/main.py")
        else:
            st.error("❌ Invalid username or password")

# Signup Form
else:
    username = st.text_input("Create username")
    password = st.text_input("Create password", type="password")
    confirm = st.text_input("Confirm password", type="password")
    role = st.selectbox("Select role", ["user", "admin"])

    if st.button("Sign Up"):
        if password != confirm:
            st.error("❌ Passwords do not match")
        elif users_col.find_one({"username": username}):
            st.error("🚫 Username already exists!")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            users_col.insert_one({
                "username": username,
                "password": hashed_pw,
                "role": role
            })
            st.success("✅ Signed up successfully!")
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = role
            if role == "admin":
                st.switch_page("pages/4_Admin_Dashboard.py")
            else:
                st.switch_page("pages/main.py")

st.markdown('</div></div>', unsafe_allow_html=True)
