# --- insights.py ---
import os
import pandas as pd
import streamlit as st
import plotly.express as px

# 🔍 Load data based on business type
def load_business_data(business_type):
    filename = f"connection_logs_{business_type.lower().replace(' ', '_')}.csv"
    filepath = os.path.join("connection_logs", filename)

    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        st.error(f"🚫 File not found: {filepath}")
        return None

# 📊 Analytics dashboard

def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")

    business_type = st.selectbox("Select Business Type", [
        "Restaurant", "Hospital", "Business Cafe", "Boutique", "Supermarket"
    ])

    df = load_business_data(business_type)

    if df is not None:
        st.success(f"Loaded {len(df)} records for {business_type}")
        st.dataframe(df.head())

        if 'connection_time' in df.columns:
            df['connection_time'] = pd.to_datetime(df['connection_time'])
            df['hour'] = df['connection_time'].dt.hour
            fig = px.histogram(df, x='hour', nbins=24, title='Connections by Hour')
            st.plotly_chart(fig)

        if 'device_type' in df.columns:
            fig = px.pie(df, names='device_type', title='Device Types')
            st.plotly_chart(fig)
    else:
        st.warning("No data to display.")
