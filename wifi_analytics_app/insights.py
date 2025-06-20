# --- insights.py ---
import os
import pandas as pd
import streamlit as st
import plotly.express as px

def load_business_data(business_type):
    # Get the directory where the current script (insights.py) is located
    current_dir = os.path.dirname(__file__)

    # Define the subdirectory where your connection logs are stored
    # Assuming 'connection_logs' is a folder at the same level as insights.py
    data_dir = os.path.join(current_dir, "connection_logs")

    # Correctly format the business_type to match your actual filenames
    # e.g., "Boutique" -> "boutique.csv"
    formatted_business_type = business_type.lower().replace(" ", "_")

    # *** FIX IS HERE: Remove 'connection_logs_' prefix from filename construction ***
    file_name = f"{formatted_business_type}.csv"

    # Construct the full file path
    file_path = os.path.join(data_dir, file_name)

    st.write(f"Attempting to load: {file_path}") # This line is for debugging, you can remove it later

    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"🚫 Error reading CSV file {file_path}: {e}")
            return None
    else:
        st.error(f"🚫 File not found: {file_path}. Please ensure it exists in your 'connection_logs' directory and the naming convention is correct.")
        return None

# The rest of your insights.py file remains the same
def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")
    business_type = st.selectbox(
        "Select Business Type",
        ["Boutique", "Business Cafe", "Hospital", "Restaurant", "Supermarket"]
    )
    df = load_business_data(business_type)

    if df is not None:
        required_columns = {"timestamp", "device_type", "duration"}
        new_metrics_columns = {"signal_strength_dBm", "data_used_MB", "session_duration_minutes", "peak_usage_hour"}
        all_required_columns = required_columns.union(new_metrics_columns)

        if not all_required_columns.issubset(df.columns):
            missing_cols = all_required_columns - set(df.columns)
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

        if 'signal_strength_dBm' in df.columns:
            fig_signal = px.histogram(df, x="signal_strength_dBm", title="Signal Strength Distribution (dBm)")
            st.plotly_chart(fig_signal)
    else:
        st.warning("No data to display or file not found.")
