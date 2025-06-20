from sklearn.cluster import KMeans
import pandas as pd
import streamlit as st

def show_ai_insights():
    st.subheader("🤖 AI-Powered Insights")

    try:
        df = pd.read_csv("connection_logs/restaurant.csv")  # Or dynamic selection
        features = df.select_dtypes(include=['int64', 'float64'])

        if features.shape[0] < 2:
            st.warning("Not enough data for clustering. Need at least 2 records.")
            return

        n_clusters = min(3, features.shape[0])  # Adjust cluster count
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(features)

        df['Cluster'] = kmeans.labels_
        st.write("Clustered Insights:")
        st.dataframe(df.head())

    except Exception as e:
        st.error(f"AI Insight failed: {e}")
