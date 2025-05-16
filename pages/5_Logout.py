import streamlit as st

st.set_page_config(page_title="Logout", layout="wide")

st.title("🔒 Logout")

if "logged_in" in st.session_state and st.session_state.logged_in:
    st.success(f"👋 Logged out {st.session_state.user}")
    st.session_state.clear()
    st.markdown("Redirecting to login...")
    st.switch_page("login.py")
else:
    st.warning("⚠️ You are not logged in.")

