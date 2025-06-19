# --- ai_models.py ---
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def show_ai_insights():
    st.header("🤖 AI-Powered Insights")
    try:
        df = pd.read_csv("connection_logs.csv", names=["email", "phone", "location", "timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["hour"] = df["timestamp"].dt.hour
        df["day"] = df["timestamp"].dt.dayofweek

        # Simple feature matrix
        X = df[["hour", "day"]]

        kmeans = KMeans(n_clusters=3)
        df["cluster"] = kmeans.fit_predict(X)

        st.subheader("Customer Segmentation")
        fig, ax = plt.subplots()
        scatter = ax.scatter(df["hour"], df["day"], c=df["cluster"], cmap="viridis")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Day of Week")
        st.pyplot(fig)

        st.success("AI segmentation complete. 3 clusters identified.")
    except Exception as e:
        st.error(f"AI Insight failed: {e}")
