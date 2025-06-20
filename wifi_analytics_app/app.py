# --- app.py (Main entry point) ---
import streamlit as st
from auth import login_user
from splash import splash_page
from insights import analytics_dashboard
from ai_models import show_ai_insights
from automation import automation_controls
from config import init_config
from insights import load_business_data

init_config()

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
            
def main_dashboard():
    st.title("📡 Free WiFi Analytics Dashboard")

    business_type = st.selectbox("Select Business Type", ["Restaurant", "Hospital", "Business Cafe", "Boutique", "Supermarket"])

    df = load_business_data(business_type)

    if df is not None:
        st.success(f"{len(df)} records loaded for {business_type}")
        st.dataframe(df.head())

        # AI Insights or analytics functions here
        # example: show_ai_insights(df)
    else:
        st.warning("No data loaded.")


