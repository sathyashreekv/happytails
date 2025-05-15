import streamlit as st
import bcrypt
import random
import datetime
from twilio.rest import Client
import os

from database import users_collection as users_col  # MongoDB collection

# Load Twilio credentials
if "TWILIO_SID" in os.environ:
    sid = os.getenv("TWILIO_SID")
    auth = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_phone = os.getenv("TWILIO_PHONE")
else:
    sid = st.secrets["twilio"]["sid"]
    auth = st.secrets["twilio"]["auth"]
    twilio_phone = st.secrets["twilio"]["phone"]

client = Client(sid, auth)

# ----- Background Styling -----
st.set_page_config(page_title="HappyTails Auth", layout="wide")
st.markdown("""
<style>
.stApp { background-image: url("https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_1280.jpg");
          background-size: cover; background-position: center center; background-repeat: no-repeat; background-attachment: fixed; }
.center-wrap { display: flex; justify-content: center; align-items: center; height: 100vh; }
.form-container { backdrop-filter: blur(10px); background-color: rgba(255,255,255,0.15); padding: 3rem 2rem;
                 border-radius: 20px; max-width: 400px; width: 90%; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); color: white; }
h2 { text-align: center; color: white; }
.stTextInput>div>input, .stSelectbox>div>div>div { background-color: rgba(255,255,255,0.8); color: black; }
.stButton>button { background-color: #0066cc; color: white; font-weight: bold; border-radius: 10px; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# ----- State Initialization -----
for key in ["logged_in", "mode", "otp_sent", "generated_otp", "reset_user_id", "otp_start_time", "user", "role", "reset_phone"]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state.mode is None:
    st.session_state.mode = "Login"

st.markdown('<div class="center-wrap"><div class="form-container">', unsafe_allow_html=True)
st.markdown(f"<h2>{st.session_state.mode}</h2>", unsafe_allow_html=True)

# ----- Mode Switch -----
if st.session_state.mode in ["Login", "Sign Up"] and st.button("Switch to " + ("Sign Up" if st.session_state.mode == "Login" else "Login")):
    st.session_state.mode = "Sign Up" if st.session_state.mode == "Login" else "Login"
    st.rerun()

# ----- Login -----
if st.session_state.mode == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Login"):
            user = users_col.find_one({"username": username})
            if user and bcrypt.checkpw(password.encode(), user["password"]):
                st.success("✅ Logged in!")
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.role = user["role"]
                st.switch_page("pages/4_Admin_Dashboard.py" if user["role"] == "admin" else "pages/main.py")
            else:
                st.error("❌ Invalid username or password")
    with col2:
        if st.button("Forgot Password?"):
            st.session_state.mode = "Forgot"
            st.session_state.otp_sent = False
            st.rerun()

# ----- Sign Up -----
elif st.session_state.mode == "Sign Up":
    username = st.text_input("Create username")
    password = st.text_input("Create password", type="password")
    confirm = st.text_input("Confirm password", type="password")
    role = st.selectbox("Select role", ["user", "admin"])
    phone = st.text_input("Phone Number (with country code)")

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
                "role": role,
                "phone": phone
            })
            st.success("✅ Signed up successfully!")
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = role
            st.switch_page("pages/4_Admin_Dashboard.py" if role == "admin" else "pages/main.py")

# ----- Forgot Password Step 1 -----
elif st.session_state.mode == "Forgot" and not st.session_state.otp_sent:
    phone = st.text_input("Enter your registered phone number")
    if st.button("Send OTP"):
        user = users_col.find_one({"phone": phone})
        if not user:
            st.error("❌ No user found with this phone number")
        else:
            otp = str(random.randint(100000, 999999))
            try:
                message = client.messages.create(
                    body=f"HappyTails OTP: {otp}",
                    from_=twilio_phone,
                    to=phone
                )
                st.session_state.generated_otp = otp
                st.session_state.reset_user_id = user["_id"]
                st.session_state.reset_phone = phone
                st.session_state.otp_sent = True
                st.session_state.otp_start_time = datetime.datetime.now()
                st.success("✅ OTP sent via SMS")
            except Exception as e:
                st.error(f"❌ Failed to send SMS: {e}")

# ----- Forgot Password Step 2 -----
elif st.session_state.mode == "Forgot" and st.session_state.otp_sent:
    time_elapsed = (datetime.datetime.now() - st.session_state.otp_start_time).seconds
    time_remaining = max(0, 180 - time_elapsed)

    st.info(f"⏱️ OTP valid for: {time_remaining} seconds")

    if time_remaining <= 0:
        st.error("❌ OTP expired")
        st.session_state.otp_sent = False
        st.rerun()

    entered_otp = st.text_input("Enter OTP")
    new_pw = st.text_input("New Password", type="password")
    confirm_pw = st.text_input("Confirm Password", type="password")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Reset Password"):
            if entered_otp != st.session_state.generated_otp:
                st.error("❌ Incorrect OTP")
            elif new_pw != confirm_pw:
                st.error("❌ Passwords do not match")
            else:
                hashed_pw = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt())
                users_col.update_one({"_id": st.session_state.reset_user_id}, {"$set": {"password": hashed_pw}})
                st.success("✅ Password reset successful. Please login.")
                st.session_state.mode = "Login"
                st.session_state.otp_sent = False
                st.session_state.generated_otp = None
                st.rerun()
    with col2:
        if st.button("Resend OTP"):
            otp = str(random.randint(100000, 999999))
            try:
                message = client.messages.create(
                    body=f"HappyTails OTP: {otp}",
                    from_=twilio_phone,
                    to=st.session_state.reset_phone
                )
                st.session_state.generated_otp = otp
                st.session_state.otp_start_time = datetime.datetime.now()
                st.success("🔄 OTP resent via SMS")
            except Exception as e:
                st.error(f"❌ Failed to resend OTP: {e}")

st.markdown('</div></div>', unsafe_allow_html=True)
