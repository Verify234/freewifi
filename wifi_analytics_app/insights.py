import os
import pandas as pd
import streamlit as st
import plotly.express as px

def load_business_data(business_type):
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "connection_logs")
    formatted_business_type = business_type.lower().replace(" ", "_")
    file_name = f"connection_logs_{formatted_business_type}.csv"
    file_path = os.path.join(data_dir, file_name)
    # st.write(f"Attempting to load: {file_path}")  # Uncomment for debugging

    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"🚫 Error reading CSV file {file_path}: {e}")
            return None
    else:
        st.error(f"🚫 File not found: {file_path}. Please ensure it exists in your 'connection_logs' directory and the naming convention is correct.")
        return None

def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")
    business_type = st.selectbox(
        "Select Business Type",
        ["Boutique", "Business Cafe", "Hospital", "Restaurant", "Supermarket"]
    )
    df = load_business_data(business_type)

    if df is not None:
        required_columns = {"timestamp", "device_type", "duration"}
        # New metrics columns are optional
        new_metrics_columns = {"signal_strength_dBm", "data_used_MB", "session_duration_minutes", "peak_usage_hour"}

        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            st.error(f"Uploaded file is missing one or more required columns: {', '.join(missing_cols)}")
            return

        st.success(f"Loaded {len(df)} records for {business_type}")
        st.dataframe(df.head())

        # Time-based histogram
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        if 'hour' not in df:
            df['hour'] = df['timestamp'].dt.hour
        fig = px.histogram(df, x="hour", nbins=24, title="Connections by Hour")
        st.plotly_chart(fig)

        # Device type distribution pie chart
        fig = px.pie(df, names="device_type", title="Device Type Distribution")
        st.plotly_chart(fig)

        # Plots for optional metrics
        if 'signal_strength_dBm' in df.columns:
            fig_signal = px.histogram(df, x="signal_strength_dBm", title="Signal Strength Distribution (dBm)")
            st.plotly_chart(fig_signal)

        if 'data_used_MB' in df.columns:
            fig_data = px.histogram(df, x="data_used_MB", title="Data Usage Distribution (MB)")
            st.plotly_chart(fig_data)

        if 'session_duration_minutes' in df.columns:
            fig_session = px.histogram(df, x="session_duration_minutes", title="Session Duration (Minutes)")
            st.plotly_chart(fig_session)

        if 'peak_usage_hour' in df.columns:
            fig_peak = px.histogram(df, x="peak_usage_hour", nbins=24, title="Peak Usage Hours")
            st.plotly_chart(fig_peak)

    else:
        st.warning("No data to display or file not found.")
