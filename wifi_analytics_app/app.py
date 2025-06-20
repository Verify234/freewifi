# --- app.py (Main entry point) ---
import streamlit as st
import os

from auth import login_user
from splash import splash_page
from ai_models import show_ai_insights
from automation import automation_controls
from config import init_config
from insights import load_business_data, analytics_dashboard

# ⚙️ Initialize config
init_config()

# 🔐 Authentication
user_type = login_user()

if user_type == "guest":
    splash_page()

elif user_type == "admin":
    st.sidebar.title("Admin Dashboard")
    tab = st.sidebar.radio("Navigate", ["Analytics", "AI Insights", "Automation"])

    if tab == "Analytics":
        analytics_dashboard()

    elif tab == "AI Insights":
        show_ai_insights()

    elif tab == "Automation":
        automation_controls()

else:
    st.warning("Unauthorized access.")


# 🎯 Optional: Standalone dashboard access
def main_dashboard():
    st.title("📡 Free WiFi Analytics Dashboard")

    business_type = st.selectbox("Select Business Type", ["Boutique", "Business Cafe", "Hospital", "Restaurant", "Supermarket"])

    df = load_business_data(business_type)

    if df is not None:
        st.success(f"{len(df)} records loaded for {business_type}")
        st.dataframe(df.head())

        # Optional: AI insight preview
        # show_ai_insights(df)
    else:
        st.warning("No data loaded.")
