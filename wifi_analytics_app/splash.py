import streamlit as st
from insights import register_guest

def splash_page():
    st.title("Welcome to Free WiFi")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    if st.button("Connect"):
        register_guest(email, phone, st.session_state.get("device_type", "unknown"))
        st.success("Connected!")
        st.stop()