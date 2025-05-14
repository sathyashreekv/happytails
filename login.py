import streamlit as st
import bcrypt
import re
from database import users_collection as users_col, audit_log_collection as log_col  # assuming audit log collection exists

# Page config
st.set_page_config(page_title="HappyTails Auth", layout="wide")

# CSS Styling
st.markdown(""" 
    <style>
    .stApp {
        background-image: url("https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_1280.jpg");
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

# Centered container
st.markdown('<div class="center-wrap"><div class="form-container">', unsafe_allow_html=True)
st.markdown(f"<h2>{st.session_state.mode}</h2>", unsafe_allow_html=True)

# Mode Switch Button
if st.button("Switch to " + ("Sign Up" if st.session_state.mode == "Login" else "Login")):
    st.session_state.mode = "Sign Up" if st.session_state.mode == "Login" else "Login"
    st.rerun()

# =========================== LOGIN FORM ===========================
if st.session_state.mode == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    remember_me = st.checkbox("Remember Me")

    if st.button("Login"):
        user = users_col.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            st.success("✅ Logged in!")
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = user["role"]

            log_col.insert_one({"action": "login", "user": username})  # Log the login

            if user["role"] == "admin":
                st.switch_page("pages/4_Admin_Dashboard.py")
            else:
                st.switch_page("pages/main.py")
        else:
            st.error("❌ Invalid username or password")

# ========================== SIGN UP FORM ==========================
else:
    email = st.text_input("Email")
    username = st.text_input("Create username")
    password = st.text_input("Create password", type="password")
    confirm = st.text_input("Confirm password", type="password")
    role = st.selectbox("Select role", ["user", "admin"])

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def password_strength(pw):
        if len(pw) < 8:
            return "Weak (min 8 characters required)"
        if not re.search(r"[A-Z]", pw):
            return "Weak (add uppercase letter)"
        if not re.search(r"[a-z]", pw):
            return "Weak (add lowercase letter)"
        if not re.search(r"\d", pw):
            return "Weak (add a number)"
        if not re.search(r"[!@#\$%\^&\*]", pw):
            return "Weak (add a special character)"
        return "Strong"

    if password:
        st.info(f"🔐 Password Strength: {password_strength(password)}")

    if st.button("Sign Up"):
        if not is_valid_email(email):
            st.error("📧 Enter a valid email address")
        elif password != confirm:
            st.error("❌ Passwords do not match")
        elif users_col.find_one({"username": username}):
            st.error("🚫 Username already exists!")
        else:
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            users_col.insert_one({
                "email": email,
                "username": username,
                "password": hashed_pw,
                "role": role
            })
            st.success("✅ Signed up successfully!")
            log_col.insert_one({"action": "signup", "user": username})
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = role
            if role == "admin":
                st.switch_page("pages/4_Admin_Dashboard.py")
            else:
                st.switch_page("pages/main.py")

# Logout button if logged in
if st.session_state.get("logged_in", False):
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.success("👋 Logged out!")
        st.rerun()

st.markdown('</div></div>', unsafe_allow_html=True)
