# --- insights.py ---
import streamlit as st
import pandas as pd
import os

def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")
    st.write("Analytics dashboard content will be displayed here.")

import pandas as pd
import os

def load_business_data(business_type):
    filename = business_type.lower().replace(" ", "_") + ".csv"
    file_path = os.path.join("connection_logs", filename)

    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

