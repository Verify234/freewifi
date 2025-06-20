# --- ai_models.py (Updated AI Insight Logic with Sample Visualizations) ---

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def show_ai_insights():
    st.header("🤖 AI-Powered Customer Insights")

    business_options = [
        "restaurant",
        "hospital",
        "business_cafe",
        "boutique",
        "supermarket"
    ]
    business_type = st.selectbox("Select Business Type", business_options)

    file_path = f"connection_logs/{business_type}.csv"

    try:
        df = pd.read_csv(file_path)
        st.success(f"Loaded {len(df)} records from {business_type.title()} dataset")
        st.write(df.head())

        numeric_cols = df.select_dtypes(include='number')

        if len(df) >= 3 and numeric_cols.shape[1] >= 2:
            st.subheader("Clustering Users")
            X = numeric_cols.dropna()
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            df['Cluster'] = kmeans.labels_

            st.write("Cluster Labels:", df['Cluster'].value_counts())

            # Sample cluster scatter plot
            fig, ax = plt.subplots()
            ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=kmeans.labels_, cmap='viridis')
            ax.set_title("Customer Clusters")
            st.pyplot(fig)

        else:
            st.warning("🔍 Not enough numeric data for clustering. Showing simple analytics instead.")

            st.subheader("📈 Sample Visualizations")
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df['hour'] = df['timestamp'].dt.hour
                hourly_counts = df['hour'].value_counts().sort_index()

                st.write("### Connection Frequency by Hour")
                fig, ax = plt.subplots()
                hourly_counts.plot(kind='bar', ax=ax)
                ax.set_xlabel("Hour of Day")
                ax.set_ylabel("Connections")
                st.pyplot(fig)

            if 'device_type' in df.columns:
                device_counts = df['device_type'].value_counts()
                st.write("### Device Type Distribution")
                st.bar_chart(device_counts)

    except FileNotFoundError:
        st.error(f"🚫 File not found: {file_path}")
    except Exception as e:
        st.error(f"AI Insight failed: {e}")
