import streamlit as st

USERS = {
    "admin": {"pw": "secretpw", "role": "admin"},
    "manager": {"pw": "managerpw", "role": "manager"},
}

def login_widget():
    st.sidebar.title("Login")
    u = st.sidebar.text_input("User")
    p = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign In"):
        if u in USERS and USERS[u]["pw"] == p:
            st.session_state.user = u
            st.session_state.role = USERS[u]["role"]
        else:
            st.sidebar.error("Login failed")