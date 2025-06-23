# --- auth.py ---
import streamlit as st

# In a real app, integrate Firebase/Auth0 or OAuth (Google/Facebook)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "guest": {"password": "guest123", "role": "guest"}
}

def login_user():
    with st.sidebar:
        st.title("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = USERS.get(username)
            if user and user["password"] == password:
                st.session_state["user"] = username
                st.session_state["role"] = user["role"]
                st.success(f"Logged in as {username}")
                return user["role"]
            else:
                st.error("Invalid credentials")
    return st.session_state.get("role")
