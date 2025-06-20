def analytics_dashboard():
    st.title("📊 WiFi Usage Analytics")
    business_type = st.selectbox("Select Business Type", ["Restaurant", "Hospital", "Business Cafe", "Boutique", "Supermarket"])
    df = load_business_data(business_type)

    required_columns = {"timestamp", "device_type", "duration"}  # Define this early

    if df is not None:
        if not required_columns.issubset(df.columns):
            st.error("Uploaded file is missing required columns.")
            return  # Stop further processing

        st.success(f"Loaded {len(df)} records for {business_type}")
        st.dataframe(df.head())

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            fig = px.histogram(df, x="hour", nbins=24, title="Connections by Hour")
            st.plotly_chart(fig)

        if 'device_type' in df.columns:
            fig = px.pie(df, names="device_type", title="Device Type Distribution")
            st.plotly_chart(fig)
    else:
        st.warning("No data to display.")
