# --- ai_models.py ---
import os
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.express as px

def show_ai_insights():
    st.title("🧠 AI-Powered Insights")
    business_type = st.selectbox("Select Business Type for AI", ["Restaurant", "Hospital", "Business Cafe", "Boutique", "Supermarket"])
    filename = f"connection_logs_{business_type.lower().replace(' ', '_')}.csv"
    filepath = os.path.join("wifi_analytics_app", "connection_logs", filename)

    if not os.path.exists(filepath):
        st.error(f"🚫 File not found: {filepath}")
        return

    try:
        numeric_df = df.select_dtypes(include='number')

if numeric_df.shape[0] < 3 or numeric_df.shape[1] < 2:
    st.error("🚫 Not enough numeric data for clustering. Need at least 3 records and 2 numeric columns.")
    return


        X = df[numeric_cols].dropna()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        df['Cluster'] = kmeans.labels_

        st.success("✅ AI segmentation completed.")
        fig = px.scatter_matrix(df, dimensions=numeric_cols, color='Cluster', title='Customer Segmentation')
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"AI Insight failed: {e}")
