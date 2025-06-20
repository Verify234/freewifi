import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns # For better aesthetics and more plot types
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import plotly.express as px # For interactive plots

# Set Seaborn style for better aesthetics
sns.set_theme(style="whitegrid")

def show_ai_insights():
    st.header("🤖 AI-Powered Customer Insights: A Data Scientist's Deep Dive")
    st.write("""
    This section showcases how a data scientist would leverage advanced AI techniques to transform raw WiFi connection logs into actionable marketing intelligence.
    We'll move beyond simple metrics to uncover hidden customer segments and predict future behaviors.
    """)

    business_options = [
        "restaurant",
        "hospital",
        "business_cafe",
        "boutique",
        "supermarket"
    ]
    business_type = st.selectbox("Select Business Type to Analyze", business_options)

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "connection_logs")
    file_name = f"{business_type}.csv"
    file_path = os.path.join(data_dir, file_name)

    # For debugging
    st.info(f"Attempting to load data from: `{file_path}` for AI insights.")

    try:
        df = pd.read_csv(file_path)
        st.success(f"Successfully loaded {len(df)} records from {business_type.replace('_', ' ').title()} dataset.")
        st.dataframe(df.head()) # Show first few rows of the loaded data

        # Data Preprocessing for AI Models
        # Ensure 'duration' column is available for clustering
        if 'session_duration_minutes' in df.columns and 'duration' not in df.columns:
            df.rename(columns={'session_duration_minutes': 'duration'}, inplace=True)
            st.info("💡 Renamed 'session_duration_minutes' to 'duration' for consistent AI model input.")

        # Convert timestamp to datetime and extract features
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df['hour_of_day'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek # Monday=0, Sunday=6
            df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

        # Feature Engineering: Example of 'Return Visitor'
        # For a simple demo, we'll assign randomly or based on existing 'frequent_visitor'
        if 'frequent_visitor' not in df.columns and 'Visitor ID' in df.columns:
             # This is a conceptual assignment. In real-world, it'd be based on unique visitor IDs across multiple visits.
            df['frequent_visitor'] = np.random.choice([0, 1], size=len(df), p=[0.7, 0.3]) # 0=New, 1=Returning
            st.info("Synthetically generated 'frequent_visitor' status for demonstration.")
        elif 'frequent_visitor' in df.columns and df['frequent_visitor'].dtype == 'object':
            df['frequent_visitor'] = df['frequent_visitor'].apply(lambda x: 1 if x.lower() == 'yes' else 0)


        # Define features for clustering
        # We need at least 2 numeric features to make a scatter plot for clustering visualization
        clustering_features = ['duration', 'hour_of_day', 'frequent_visitor']
        
        # Filter out features that don't exist in the current dataframe
        available_clustering_features = [f for f in clustering_features if f in df.columns]

        # Convert potentially categorical string columns to numeric for clustering if necessary
        # Example: 'gender' or 'device_type' would need One-Hot Encoding in a real scenario
        # For simplicity, we'll assume our chosen features are numeric or converted.

        # Ensure we have enough data and features for KMeans
        if len(df) >= 3 and len(available_clustering_features) >= 2:
            st.subheader("📊 Customer Segmentation using K-Means Clustering")
            st.write("""
            K-Means is an unsupervised learning algorithm that groups similar data points into clusters.
            Here, we're clustering customers based on their **`duration`**, **`hour_of_day`**, and **`frequent_visitor`** status.
            """)

            X_cluster = df[available_clustering_features].dropna()

            if X_cluster.empty:
                st.warning("No valid data for clustering after dropping missing values in selected features. Showing general insights instead.")
                raise ValueError("Insufficient data for clustering.") # Jump to fallback

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_cluster)

            # Determine optimal K (elbow method would be used in real analysis)
            # For this demo, let's stick to a reasonable number, e.g., 3 or 4 clusters
            n_clusters = st.slider("Select Number of Clusters (K)", min_value=2, max_value=5, value=3, step=1)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10) # n_init is important for robustness
            kmeans.fit(X_scaled)
            df.loc[X_cluster.index, 'Cluster'] = kmeans.labels_.astype(int) # Assign clusters back to original df

            st.markdown(f"**Identified {n_clusters} Customer Clusters:**")
            st.write(df['Cluster'].value_counts().sort_index())

            st.write("### Cluster Characteristics & Marketing Strategies")
            cluster_centers_df = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=available_clustering_features)
            cluster_centers_df['Cluster'] = cluster_centers_df.index
            st.dataframe(cluster_centers_df.set_index('Cluster').round(2), use_container_width=True)

            st.write("Interpretation of clusters and suggested marketing actions:")

            for cluster_id in sorted(df['Cluster'].unique()):
                st.markdown(f"#### Cluster {cluster_id}")
                avg_duration = df[df['Cluster'] == cluster_id]['duration'].mean().round(1)
                avg_hour = df[df['Cluster'] == cluster_id]['hour_of_day'].mean().round(1)
                freq_visitor_ratio = df[df['Cluster'] == cluster_id]['frequent_visitor'].mean().round(2) * 100

                st.write(f"- **Avg. Duration:** {avg_duration} mins")
                st.write(f"- **Avg. Visit Hour:** {int(avg_hour)}:00 (approx)")
                st.write(f"- **Returning Visitors:** {freq_visitor_ratio:.0f}%")

                # Tailor marketing strategies based on cluster characteristics and business type
                if business_type == "restaurant":
                    if avg_duration > 60 and freq_visitor_ratio > 50:
                        st.markdown("- **Insight:** **'Leisurely Loyal Diners'**. These are your high-value, regulars who spend quality time. Likely coming for full meals.")
                        st.markdown("- **Strategy:** Offer exclusive loyalty program perks, chef's special previews, or feedback requests for menu development.")
                    elif avg_duration < 30 and avg_hour >= 7 and avg_hour <= 10:
                        st.markdown("- **Insight:** **'Morning Rush Grab-and-Go'**. Quick visits, likely for coffee/breakfast.")
                        st.markdown("- **Strategy:** Promote breakfast combos, quick service options, mobile ordering, or pre-paid pick-up.")
                    elif avg_duration < 45 and avg_hour >= 12 and avg_hour <= 14:
                        st.markdown("- **Insight:** **'Lunch Break Speedsters'**. Visitors during peak lunch, want efficiency.")
                        st.markdown("- **Strategy:** Lunch specials, express menus, online pre-ordering, or 'skip-the-queue' benefits.")
                    else:
                        st.markdown("- **Insight:** **'General Explorers'**. Diverse behavior, could be new or occasional.")
                        st.markdown("- **Strategy:** Generic welcome offers, encourage reviews, or a 'first-time visitor' discount to incentivize return.")
                elif business_type == "supermarket":
                    if avg_duration > 45 and freq_visitor_ratio > 60:
                        st.markdown("- **Insight:** **'Dedicated Main Shoppers'**. Spending significant time, likely doing weekly/bi-weekly large hauls.")
                        st.markdown("- **Strategy:** Loyalty points on bulk purchases, personalized coupons based on past purchases (if inferred), or home delivery services.")
                    elif avg_duration < 20 and avg_hour > 17:
                        st.markdown("- **Insight:** **'Evening Quick Stop'**. Short visits, likely grabbing a few items after work.")
                        st.markdown("- **Strategy:** Promote 'grab-and-go' meals, quick checkout lanes, or discounts on convenience items.")
                    elif avg_duration >= 20 and avg_duration <= 45 and freq_visitor_ratio < 30:
                        st.markdown("- **Insight:** **'Occasional Browsers'**. Exploring different sections, not necessarily frequent.")
                        st.markdown("- **Strategy:** Highlight new arrivals, in-store events, or category-specific promotions to encourage exploration and repeat visits.")
                    else:
                        st.markdown("- **Insight:** **'General Shoppers'**. Mixed behavior, broad appeal marketing.")
                        st.markdown("- **Strategy:** Weekly flyers, general discounts, or in-store sampling to attract diverse interests.")
                # Add more business-specific strategies for hospital, business_cafe, boutique

            # Visualization of Clusters (using Plotly for interactivity)
            if len(available_clustering_features) >= 2:
                st.subheader("Visualizing Customer Clusters")
                fig = px.scatter(df, x=available_clustering_features[0], y=available_clustering_features[1],
                                 color='Cluster', title='Customer Clusters (K-Means)',
                                 hover_data=['duration', 'hour_of_day', 'frequent_visitor'])
                st.plotly_chart(fig)
            else:
                st.warning("Not enough numeric features for a 2D scatter plot of clusters.")

        else:
            st.warning("🔍 Insufficient data or numeric features for robust clustering. Showing general analytics instead.")
            raise ValueError("Insufficient data for clustering.") # Will jump to fallback visualizations

    except (FileNotFoundError, ValueError) as e: # Catch ValueError from insufficient data too
        st.error(f"🚫 Error loading or processing data for AI Insights: {e}")
        st.write("Please ensure the CSV file exists and contains relevant numeric data.")

        # --- Fallback Visualizations (General Analytics) ---
        st.subheader("📈 General WiFi Analytics Visualizations (Fallback)")
        st.write("Even without advanced AI, basic analytics provide valuable insights:")

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df['hour_of_day'] = df['timestamp'].dt.hour # Ensure 'hour_of_day' is always available if timestamp exists

            # Plot 1: Connection Frequency by Hour (Bar Chart)
            st.write("#### Connection Frequency by Hour")
            hourly_counts = df['hour_of_day'].value_counts().sort_index()
            fig_hourly, ax_hourly = plt.subplots(figsize=(10, 5))
            sns.barplot(x=hourly_counts.index, y=hourly_counts.values, ax=ax_hourly, palette='viridis')
            ax_hourly.set_title("WiFi Connections by Hour of Day")
            ax_hourly.set_xlabel("Hour of Day")
            ax_hourly.set_ylabel("Number of Connections")
            st.pyplot(fig_hourly)

            # Plot 2: Daily Connection Trends (Line Chart if enough data)
            if not df['timestamp'].empty:
                daily_counts = df.set_index('timestamp').resample('D').size()
                if len(daily_counts) > 1: # Only plot line if more than one day
                    st.write("#### Daily Connection Trend")
                    fig_daily, ax_daily = plt.subplots(figsize=(10, 5))
                    ax_daily.plot(daily_counts.index, daily_counts.values, marker='o')
                    ax_daily.set_title("Daily WiFi Connection Trend")
                    ax_daily.set_xlabel("Date")
                    ax_daily.set_ylabel("Number of Connections")
                    plt.xticks(rotation=45)
                    st.pyplot(fig_daily)

        if 'device_type' in df.columns:
            # Plot 3: Device Type Distribution (Pie Chart)
            st.write("#### Device Type Distribution")
            device_counts = df['device_type'].value_counts()
            fig_device = px.pie(names=device_counts.index, values=device_counts.values,
                                 title='Distribution of Device Types')
            st.plotly_chart(fig_device)

        if 'duration' in df.columns:
            # Plot 4: Distribution of Session Durations (Histogram)
            st.write("#### Distribution of Session Durations")
            fig_duration = px.histogram(df, x='duration', nbins=20,
                                        title='Distribution of WiFi Session Durations',
                                        labels={'duration': 'Session Duration (minutes)'})
            st.plotly_chart(fig_duration)

    except Exception as e:
        st.error(f"An unexpected error occurred during AI Insights: {e}")
        st.info("Please check the data files and column names.")
