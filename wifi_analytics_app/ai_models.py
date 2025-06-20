import streamlit as st
import pandas as pd
import numpy as np
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

    df = pd.DataFrame() # Initialize df to avoid UnboundLocalError in finally block

    try:
        df = pd.read_csv(file_path)
        st.success(f"Successfully loaded {len(df)} records from {business_type.replace('_', ' ').title()} dataset.")
        st.dataframe(df.head()) # Show first few rows of the loaded data

        # --- Data Preprocessing for AI Models ---
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
            st.info("Extracted 'hour_of_day', 'day_of_week', and 'is_weekend' from timestamp.")
        else:
            st.warning("`timestamp` column not found. Some time-based features will be unavailable for AI insights.")


        # --- Robust 'frequent_visitor' Handling ---
        # Prioritize existing column, then generate if needed
        if 'frequent_visitor' in df.columns:
            # Try to convert to numeric (0 for No/False, 1 for Yes/True)
            # This handles 'Yes'/'No', 'TRUE'/'FALSE', 0/1, or even non-standard text by making them NaN first
            df['frequent_visitor'] = df['frequent_visitor'].astype(str).str.lower().map({'yes': 1, 'true': 1, 'no': 0, 'false': 0}).fillna(0)
            st.info("Processed existing 'frequent_visitor' column to numeric (0/1).")
        else:
            # If 'frequent_visitor' column does not exist, synthetically generate it.
            # In a real scenario, this would be derived from unique user IDs and multiple visits.
            df['frequent_visitor'] = np.random.choice([0, 1], size=len(df), p=[0.7, 0.3]) # 0=New, 1=Returning
            st.info("Synthetically generated 'frequent_visitor' status (0=New, 1=Returning) for demonstration as it was not found.")
        # Ensure it's integer type
        df['frequent_visitor'] = df['frequent_visitor'].astype(int)


        # Define features for clustering
        # We need at least 2 numeric features to make a scatter plot for clustering visualization
        clustering_features = ['duration', 'hour_of_day', 'frequent_visitor']
        
        # Filter out features that don't exist in the current dataframe or are not suitable (e.g., all NaNs)
        available_clustering_features = []
        for feature in clustering_features:
            if feature in df.columns and pd.api.types.is_numeric_dtype(df[feature]) and not df[feature].isnull().all():
                available_clustering_features.append(feature)
            else:
                st.warning(f"Feature '{feature}' is not available, not numeric, or all NaN. It will be excluded from clustering.")

        # Ensure we have enough data and features for KMeans
        # Also, check if all selected features have non-zero variance (StandardScaler requirement if not 1 col)
        if len(df) >= 3 and len(available_clustering_features) >= 2:
            st.subheader("📊 Customer Segmentation using K-Means Clustering")
            st.write("""
            K-Means is an unsupervised learning algorithm that groups similar data points into clusters.
            Here, we're clustering customers based on their **`duration`**, **`hour_of_day`**, and **`frequent_visitor`** status.
            """)

            X_cluster = df[available_clustering_features].dropna()

            if X_cluster.empty:
                st.warning("No valid data for clustering after dropping missing values in selected features. Showing general insights instead.")
                raise ValueError("Insufficient data for clustering after cleaning.") # Jump to fallback

            # Check for constant features before scaling
            if X_cluster.shape[1] > 1 and (X_cluster.var() == 0).any():
                st.warning("Some selected clustering features have zero variance (all values are the same). Removing them for scaling.")
                X_cluster = X_cluster.loc[:, (X_cluster != X_cluster.iloc[0]).any()] # Keep only columns with variance

            if X_cluster.shape[1] < 2: # After removing constant columns, check again
                 st.warning("Not enough varying numeric features for clustering after cleaning. Showing general insights instead.")
                 raise ValueError("Insufficient varying features for clustering.")


            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_cluster)

            # Determine optimal K (elbow method would be used in real analysis)
            n_clusters = st.slider("Select Number of Clusters (K)", min_value=2, max_value=5, value=3, step=1)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10) # n_init is important for robustness
            kmeans.fit(X_scaled)
            df.loc[X_cluster.index, 'Cluster'] = kmeans.labels_.astype(int) # Assign clusters back to original df

            st.markdown(f"**Identified {n_clusters} Customer Clusters:**")
            st.write(df['Cluster'].value_counts().sort_index())

            st.write("### Cluster Characteristics & Marketing Strategies")
            # Calculate mean of original features for cluster interpretation
            cluster_centers_df = df.groupby('Cluster')[available_clustering_features].mean().round(2)
            st.dataframe(cluster_centers_df, use_container_width=True)

            st.write("Interpretation of clusters and suggested marketing actions:")

            for cluster_id in sorted(df['Cluster'].unique()):
                st.markdown(f"#### Cluster {cluster_id}")
                # Get actual cluster characteristics from the aggregated DataFrame
                cluster_info = cluster_centers_df.loc[cluster_id]
                
                # Check if the feature exists in the cluster_info before accessing
                avg_duration = cluster_info['duration'] if 'duration' in cluster_info.index else 'N/A'
                avg_hour = cluster_info['hour_of_day'] if 'hour_of_day' in cluster_info.index else 'N/A'
                freq_visitor_ratio = cluster_info['frequent_visitor'] * 100 if 'frequent_visitor' in cluster_info.index else 'N/A'
                
                st.write(f"- **Avg. Duration:** {avg_duration} mins")
                st.write(f"- **Avg. Visit Hour:** {int(avg_hour)}:00 (approx)" if isinstance(avg_hour, (int, float)) else f"- **Avg. Visit Hour:** {avg_hour}")
                st.write(f"- **Returning Visitors:** {freq_visitor_ratio:.0f}%" if isinstance(freq_visitor_ratio, (int, float)) else f"- **Returning Visitors:** {freq_visitor_ratio}")

                # Tailor marketing strategies based on cluster characteristics and business type
                if business_type == "restaurant":
                    if isinstance(avg_duration, (int, float)) and isinstance(freq_visitor_ratio, (int, float)):
                        if avg_duration > 60 and freq_visitor_ratio > 50:
                            st.markdown("- **Insight:** **'Leisurely Loyal Diners'**. High-value regulars who enjoy longer stays. Likely coming for full meals and the ambiance.")
                            st.markdown("- **Strategy:** Offer exclusive loyalty program perks, chef's special previews, or gather feedback for new menu items. Promote premium experiences.")
                        elif avg_duration < 30 and isinstance(avg_hour, (int, float)) and avg_hour >= 7 and avg_hour <= 10:
                            st.markdown("- **Insight:** **'Morning Rush Grab-and-Go'**. Quick visits early in the day, likely for coffee/breakfast on the run.")
                            st.markdown("- **Strategy:** Promote breakfast combos, quick service options, mobile ordering with pre-paid pick-up, or 'commuter deals'.")
                        elif avg_duration < 45 and isinstance(avg_hour, (int, float)) and avg_hour >= 12 and avg_hour <= 14:
                            st.markdown("- **Insight:** **'Lunch Break Speedsters'**. Visitors during peak lunch, value efficiency and specific meal deals.")
                            st.markdown("- **Strategy:** Promote special lunch menus, express service lines, online pre-ordering for lunch, or corporate lunch packages.")
                        else:
                            st.markdown("- **Insight:** **'Occasional Explorers'**. Diverse behavior, could be new or less frequent visitors exploring options.")
                            st.markdown("- **Strategy:** Generic welcome offers, encourage reviews/social media tags, or a 'first-time visitor' discount to incentivize return and gather more preference data.")
                    else:
                        st.markdown("- **Insight:** **'Varied Restaurant Patrons'**. Data limitations prevent more specific insights here. Focus on broad appeal.")
                        st.markdown("- **Strategy:** Promote popular dishes, happy hour specials, or weekend events to attract diverse segments.")

                elif business_type == "supermarket":
                    if isinstance(avg_duration, (int, float)) and isinstance(freq_visitor_ratio, (int, float)):
                        if avg_duration > 45 and freq_visitor_ratio > 60:
                            st.markdown("- **Insight:** **'Dedicated Main Shoppers'**. Spending significant time, likely doing weekly/bi-weekly large hauls for household needs.")
                            st.markdown("- **Strategy:** Loyalty points on bulk purchases, personalized coupons based on inferred shopping categories, home delivery service promotions, or family-sized bundles.")
                        elif avg_duration < 20 and isinstance(avg_hour, (int, float)) and avg_hour > 17:
                            st.markdown("- **Insight:** **'Evening Quick Stop'**. Short visits, likely grabbing a few specific items after work/school.")
                            st.markdown("- **Strategy:** Promote 'grab-and-go' meals, quick checkout lanes, discounts on convenience items or essentials (milk, bread, eggs).")
                        elif avg_duration >= 20 and avg_duration <= 45 and freq_visitor_ratio < 30:
                            st.markdown("- **Insight:** **'Occasional Browsers & Explorers'**. Visiting different sections, not necessarily frequent, but open to discovery.")
                            st.markdown("- **Strategy:** Highlight new arrivals, in-store tasting events, category-specific promotions (e.g., 'Discover our Organic Aisle'), or digital maps/guides to encourage exploration and repeat visits.")
                        else:
                            st.markdown("- **Insight:** **'General Supermarket Visitors'**. Broad appeal marketing required.")
                            st.markdown("- **Strategy:** Weekly flyers, general discounts on popular categories, or loyalty program sign-up incentives.")
                    else:
                        st.markdown("- **Insight:** **'Varied Supermarket Shoppers'**. Data limitations prevent more specific insights here. Focus on broad appeal.")
                        st.markdown("- **Strategy:** Promote overall value, essential items, and a pleasant shopping experience.")

                elif business_type == "hospital":
                    if isinstance(avg_duration, (int, float)) and avg_duration > 90 and freq_visitor_ratio < 20:
                        st.markdown("- **Insight:** **'Patient/Long-Term Visitor'**. Longer stays, likely patients or accompanying family members. Less frequent individual visits.")
                        st.markdown("- **Strategy:** Focus on comfort and support: promote on-site cafe services, comfortable waiting areas, information kiosks, or specialized patient support programs via WiFi portal.")
                    elif isinstance(avg_duration, (int, float)) and avg_duration < 30 and isinstance(avg_hour, (int, float)) and avg_hour >= 8 and avg_hour <= 17:
                        st.markdown("- **Insight:** **'Quick Visit/Appointment Holder'**. Shorter, daytime visits. Could be for appointments or quick check-ups.")
                        st.markdown("- **Strategy:** Optimize wait times, provide clear navigation/directions via WiFi portal, offer appointment reminders or pre-check-in features.")
                    else:
                        st.markdown("- **Insight:** **'General Hospital Visitors'**. Mixed purposes for visits.")
                        st.markdown("- **Strategy:** Promote general hospital services, health awareness campaigns, or visitor guidelines for a better experience.")

                elif business_type == "business_cafe":
                    if isinstance(avg_duration, (int, float)) and avg_duration > 60 and isinstance(avg_hour, (int, float)) and avg_hour >= 9 and avg_hour <= 17:
                        st.markdown("- **Insight:** **'Remote Worker/Meeting Point'**. Long stays during business hours, indicating use as a workspace or meeting venue.")
                        st.markdown("- **Strategy:** Promote stable WiFi, availability of power outlets, quiet zones, meeting room bookings, or loyalty programs for coffee/snack combos for extended stays.")
                    elif isinstance(avg_duration, (int, float)) and avg_duration < 30 and isinstance(avg_hour, (int, float)) and avg_hour >= 7 and avg_hour <= 9:
                        st.markdown("- **Insight:** **'Morning Commuter Grab'**. Quick morning visits before work.")
                        st.markdown("- **Strategy:** Promote speedy service, breakfast deals, pre-ordering via app, or loyalty for morning coffee purchases.")
                    else:
                        st.markdown("- **Insight:** **'General Cafe Patrons'**. Varied reasons for visiting.")
                        st.markdown("- **Strategy:** Promote daily specials, comfortable ambiance, or upcoming events.")

                elif business_type == "boutique":
                    if isinstance(avg_duration, (int, float)) and avg_duration > 40 and freq_visitor_ratio > 40:
                        st.markdown("- **Insight:** **'Loyal Fashion Browsers'**. Frequent visitors who spend significant time, likely exploring new collections and considering purchases.")
                        st.markdown("- **Strategy:** VIP invites to new collection launches, personalized style recommendations via email (if available), or exclusive discounts on preferred brands/styles.")
                    elif isinstance(avg_duration, (int, float)) and avg_duration < 20 and freq_visitor_ratio < 20:
                        st.markdown("- **Insight:** **'Quick Look Shoppers'**. Shorter visits, possibly just checking out a specific item or passing through.")
                        st.markdown("- **Strategy:** Highlight key new arrivals near the entrance, offer quick styling tips, or prompt for a quick feedback survey on current displays.")
                    else:
                        st.markdown("- **Insight:** **'General Boutique Visitors'**. Diverse interests.")
                        st.markdown("- **Strategy:** Showcase best-sellers, general seasonal promotions, or visual merchandising updates to attract broader attention.")
                
            # Visualization of Clusters (using Plotly for interactivity)
            if len(available_clustering_features) >= 2:
                st.subheader("Visualizing Customer Clusters")
                st.write(f"Scatter plot showing clusters based on '{available_clustering_features[0]}' and '{available_clustering_features[1]}'.")

                # Prepare hover_data: Start with clustering features
                plot_hover_data = available_clustering_features[:] # Make a copy of the list

                # Add a unique identifier to hover_data if it exists in the DataFrame
                if 'device_id' in df.columns:
                    plot_hover_data.append('device_id')
                elif 'Visitor ID' in df.columns: # As a fallback, though the error suggests this is not the case
                    plot_hover_data.append('Visitor ID')
                # No 'else' needed here, as we don't want to error if no ID column found for hover

                fig = px.scatter(df, x=available_clustering_features[0], y=available_clustering_features[1],
                                 color='Cluster', title='Customer Clusters (K-Means)',
                                 hover_data=plot_hover_data) # Use the dynamically prepared list
                st.plotly_chart(fig)
            else:
                st.warning("Not enough varying numeric features for a 2D scatter plot of clusters after cleaning.")

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
        st.error(f"An unexpected critical error occurred during AI Insights: {e}")
        st.info("Please verify your data files and column names for any inconsistencies.")
