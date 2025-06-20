# --- ai_models.py ---
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def show_ai_insights():
    st.title("🧠 AI-Powered Customer Insights")

    # Simulate loading selected business type data from session
    if 'selected_business_type' in st.session_state:
        business_type = st.session_state['selected_business_type']
        filepath = f"connection_logs/connection_logs_{business_type.lower().replace(' ', '_')}.csv"

        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError:
            st.error(f"🚫 File not found: {filepath}")
            return

        st.subheader(f"Insights for {business_type}")
        st.write("Sample of data loaded:")
        st.dataframe(df.head())

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if len(numeric_cols) < 2:
            st.warning("⚠️ Not enough numeric columns for clustering. Displaying basic insights instead.")
            st.metric("Total Records", len(df))
            st.metric("Avg. Session Duration", round(df[numeric_cols[0]].mean(), 2) if numeric_cols else "N/A")
            return

        if df.shape[0] < 3:
            st.warning("⚠️ Not enough data points for clustering. Displaying descriptive insights.")
            for col in numeric_cols:
                st.metric(f"Average {col}", round(df[col].mean(), 2))
            return

        # Preprocess data
        X = df[numeric_cols].dropna()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Perform clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        df['cluster'] = clusters

        st.success("✅ AI segmentation complete")

        # Show cluster statistics
        st.write("### Cluster Summary")
        st.dataframe(df.groupby('cluster')[numeric_cols].mean().round(2))
    else:
        st.info("ℹ️ Please load a business type in the Analytics section first.")
