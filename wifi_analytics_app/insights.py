# --- insights.py ---
import streamlit as st
import pandas as pd
import os

def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")
    st.write("Analytics dashboard content will be displayed here.")

def load_business_data(business_type):
    folder_path = "connection_logs"
    file_map = {
        "Restaurant": "restaurant.csv",
        "Hospital": "hospital.csv",
        "Business Cafe": "business_cafe.csv",
        "Boutique": "boutique.csv",
        "Supermarket": "supermarket.csv"
    }

    file_name = file_map.get(business_type)
    if not file_name:
        return None

    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None
