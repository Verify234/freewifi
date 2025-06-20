# --- ai_models.py (Updated AI Insight Logic with Sample Visualizations) ---



import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

from sklearn.preprocessing import StandardScaler

import os # <--- ADD THIS IMPORT



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



    # --- FIX IS HERE: Robust Path Construction ---

    current_dir = os.path.dirname(__file__)

    data_dir = os.path.join(current_dir, "connection_logs")

    file_name = f"{business_type}.csv" # Assuming your files are named e.g., restaurant.csv, boutique.csv

    file_path = os.path.join(data_dir, file_name)

    # --- END FIX ---



    st.write(f"Attempting to load for AI insights: {file_path}") # For debugging



    try:

        df = pd.read_csv(file_path)

        st.success(f"Loaded {len(df)} records from {business_type.title()} dataset for AI Insights")

        st.write(df.head())



        # Ensure required columns for AI are present and handle renaming

        # This mirrors the logic in insights.py to ensure 'duration' is available if 'session_duration_minutes' exists

        if 'session_duration_minutes' in df.columns and 'duration' not in df.columns:

            df.rename(columns={'session_duration_minutes': 'duration'}, inplace=True)

            st.info("Renamed 'session_duration_minutes' to 'duration' for AI compatibility.")



        numeric_cols = df.select_dtypes(include='number')



        # Filter out timestamp if it's treated as numeric but not for clustering

        if 'timestamp' in numeric_cols.columns:

            numeric_cols = numeric_cols.drop(columns=['timestamp'])

        if 'hour' in numeric_cols.columns: # If 'hour' was derived from timestamp and is numeric

            numeric_cols = numeric_cols.drop(columns=['hour'])

        # Add any other columns you don't want to use for clustering (e.g., 'Cluster' if you re-run this)

        if 'Cluster' in numeric_cols.columns:

            numeric_cols = numeric_cols.drop(columns=['Cluster'])





        # Ensure enough numeric columns remaining for clustering

        if len(df) >= 3 and numeric_cols.shape[1] >= 2:

            st.subheader("Clustering Users")

            X = numeric_cols.dropna()



            if X.empty:

                st.warning("No valid numeric data after dropping NaNs for clustering.")

                st.subheader("📈 Sample Visualizations (Fallback)")

                # Fallback visualizations if clustering data is insufficient

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

                return



            scaler = StandardScaler()

            X_scaled = scaler.fit_transform(X)



            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

            kmeans.fit(X_scaled)

            df['Cluster'] = kmeans.labels_



            st.write("Cluster Labels:", df['Cluster'].value_counts())



            # Sample cluster scatter plot - ensure X_scaled has at least 2 columns

            if X_scaled.shape[1] >= 2:

                fig, ax = plt.subplots()

                ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=kmeans.labels_, cmap='viridis')

                ax.set_title("Customer Clusters (First Two Numeric Features)")

                ax.set_xlabel(X.columns[0]) # Label with original column names

                ax.set_ylabel(X.columns[1])

                st.pyplot(fig)

            else:

                st.warning("Not enough numeric columns for 2D scatter plot after scaling.")



        else:

            st.warning("🔍 Not enough numeric data for clustering (need at least 3 rows and 2 numeric columns). Showing simple analytics instead.")



            st.subheader("📈 Sample Visualizations (Fallback)")

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

        st.error(f"🚫 File not found: {file_path}. Please ensure it exists in your 'connection_logs' directory and the naming convention is correct.")

    except Exception as e:

        st.error(f"AI Insight failed: {e}")
