# --- config.py ---
import streamlit as st

def init_config():
    st.set_page_config(
        page_title="WiFi Analytics Dashboard",
        page_icon="📶",
        layout="wide",
        initial_sidebar_state="expanded"
    )
