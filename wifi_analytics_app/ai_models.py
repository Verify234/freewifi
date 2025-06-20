# --- ai_models.py ---
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import os

def show_ai_insights():
    st.title("🧠 AI-Powered Insights")

    business_type = st.selectbox("Select Business Type", [
        "Restaurant", "Hospital", "Business Cafe", "Boutique", "Supermarket"
    ])

    filename = f"connection_logs_{business_type.lower().replace(' ', '_')}.csv"
    filepath = os.path.join("connection_logs", filename)

    if not os.path.exists(filepath):
        st.error(f"🚫 File not found: {filepath}")
        return

    try:
        df = pd.read_csv(filepath)

        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if len(numeric_cols) < 2:
            st.warning("Insufficient numeric features for clustering.")
            return

        X = df[numeric_cols].dropna()

        if len(X) < 3:
            st.warning("Not enough data samples for clustering. Minimum 3 required.")
            return

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        df['Cluster'] = kmeans.labels_

        st.success("AI segmentation completed.")
        fig = px.scatter_matrix(df, dimensions=numeric_cols, color='Cluster', title='Customer Segmentation')
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"AI Insight failed: {e}")
