# --- app.py (Main entry point) ---
import streamlit as st
import os

from auth import login_user
from splash import splash_page
from ai_models import show_ai_insights
from automation import automation_controls
from config import init_config
from insights import load_business_data, analytics_dashboard

# Set a modern background color (gradient or solid)
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #ece9f7 0%, #b9e4f4 100%);
    min-height: 100vh;
}
.login-container {
    background: white;
    padding: 2.5rem 2rem;
    border-radius: 1.25rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    max-width: 400px;
    margin: 5vh auto;
    animation: fadeIn 0.8s;
}
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(30px);}
    100% { opacity: 1; transform: translateY(0);}
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# ⚙️ Initialize config
init_config()

# --- Animated Login Page with Help Links ---
def animated_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.image("https://th.bing.com/th?q=FreeWifi+PNG+Password&w=120&h=120&c=1&rs=1&qlt=70&r=0&o=7&cb=1&pid=InlineBlock&rm=3&mkt=en-WW&cc=NG&setlang=en&adlt=moderate&t=1&mw=247", width=72)
    st.markdown("<h2 style='text-align:center;'>Welcome to FreeWiFi Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray;'>Please sign in to continue</p>", unsafe_allow_html=True)
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    login_btn = st.button("Login", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return username, password, login_btn

def unauthorized_access():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.error("Login failed. Need help? [Contact Support](mailto:support@yourdomain.com) or try again.", icon="🚫")
    st.button("Back to Login", use_container_width=True, key="retry_login")
    st.markdown("</div>", unsafe_allow_html=True)

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
elif user_type == "unauthorized":
    unauthorized_access()
else:
    # Show animated login by default if not logged in or session expired
    animated_login()

# 🎯 Optional: Standalone dashboard access
def main_dashboard():
    st.title("📡 Free WiFi Analytics Dashboard")
    business_type = st.selectbox("Select Business Type", ["Boutique", "Business Cafe", "Hospital", "Restaurant", "Supermarket"])
    df = load_business_data(business_type)
    if df is not None:
        st.success(f"{len(df)} records loaded for {business_type}")
        st.dataframe(df.head())
    else:
        st.warning("No data loaded.")
