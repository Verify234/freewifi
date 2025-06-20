# --- automation.py ---
import streamlit as st
import pandas as pd
import os # Keep os import, though its usage will change slightly

# No need to import load_business_data from insights here if this section is ONLY for uploading and validating new files.
# If you also want to DISPLAY existing data from connection_logs in this dashboard, then you would import it.

def automation_controls():
    st.header("⚙️ Automation Settings")

    # Rule configuration (this section is fine)
    trigger = st.selectbox("When to trigger?", ["On Connect", "After X Minutes", "On Disconnect"])
    action = st.selectbox("Action", ["Send SMS", "Send Email", "Webhook Call"])
    content = st.text_area("Message Content", "Thanks for connecting to Free WiFi!")

    if st.button("Save Rule"):
        st.success(f"Rule saved: {trigger} → {action}")
        # In a real application, you would save this rule to a database or persistent storage
        # (e.g., Streamlit's connection to a database, or a more robust config management system).

    st.markdown("---")

    st.subheader("📤 Upload New Business Dataset for Validation")

    business_type = st.selectbox("Business Type", ["Boutique", "Business Cafe", "Hospital", "Restaurant", "Supermarket"])
    uploaded_file = st.file_uploader(f"Upload {business_type} CSV", type="csv")

    if uploaded_file:
        try:
            # --- FIX 1: Read directly from the uploaded file's buffer ---
            df = pd.read_csv(uploaded_file)

            # --- FIX 2: Apply the same column renaming logic for uploaded files ---
            if 'session_duration_minutes' in df.columns and 'duration' not in df.columns:
                df.rename(columns={'session_duration_minutes': 'duration'}, inplace=True)
                st.info("Renamed 'session_duration_minutes' to 'duration' for uploaded file validation.")

            # --- FIX 3: Define ALL expected columns including new metrics ---
            # These are the columns you expect in the uploaded CSV for full functionality
            expected_columns = {
                "timestamp",
                "device_type",
                "duration", # Now 'duration' is the target name after renaming
                "signal_strength_dBm",
                "data_used_MB",
                "peak_usage_hour"
            }

            if not expected_columns.issubset(df.columns):
                missing_cols = expected_columns - set(df.columns)
                st.error(f"Uploaded file is missing one or more required columns: {', '.join(missing_cols)}")
            else:
                st.success(f"✅ Uploaded file for {business_type} validated successfully!")
                st.info(f"{len(df)} records in the uploaded dataset.")
                st.dataframe(df.head())

                # Simulate further automation logic with the validated data
                st.info(f"🛠️ Automation Triggered for uploaded data: {trigger} → {action}\n\nMessage: {content}")

                # Example of processing the uploaded data (you can replace with your actual automation logic)
                st.subheader("Uploaded Data Summary (Example)")
                st.write(f"Average Duration: {df['duration'].mean():.2f} minutes")
                st.write(f"Average Data Used: {df['data_used_MB'].mean():.2f} MB")

        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")

    # You might want to display existing data from connection_logs here as well,
    # if so, you would call load_business_data from insights.py.
    # For example:
    # st.markdown("---")
    # st.subheader("Existing Datasets Status")
    # from insights import load_business_data
    # existing_df = load_business_data(business_type)
    # if existing_df is not None:
    #     st.write("Current data in 'connection_logs' for this business type:")
    #     st.dataframe(existing_df.head())
    # else:
    #     st.info("No existing dataset loaded for this business type from 'connection_logs'.")
