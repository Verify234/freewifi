# --- splash.py ---
import streamlit as st
import datetime

def splash_page():
    st.title("📶 Welcome to Free WiFi")
    st.subheader("Please sign in to access internet")

    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    location = st.selectbox("Location", ["Store 1", "Store 2", "Store 3"])

    if st.button("Connect"):
        st.success("You're now connected! Enjoy browsing.")
        st.session_state["connected"] = True
        # Simulate data entry (in production: save to DB)
        with open("connection_logs.csv", "a") as f:
            f.write(f"{email},{phone},{location},{datetime.datetime.now()}\n")
