import streamlit as st
import pandas as pd
import os

def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")
    st.write("Analytics dashboard content will be displayed here.")
    
def load_business_data(business_type):
    # Adjust filename to match your actual filenames
    filename = f"connection_logs_{business_type.lower().replace(' ', '_')}.csv"
    filepath = os.path.join("connection_logs", filename)

    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        raise FileNotFoundError(f"🚫 File not found: {filepath}")


