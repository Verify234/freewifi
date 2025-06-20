# --- app.py (Main entry point) ---
import streamlit as st
from auth import login_user
 from splash import splash_page
from insights import analytics_dashboard
from ai_models import show_ai_insights
from automation import automation_controls
from config import init_config

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
