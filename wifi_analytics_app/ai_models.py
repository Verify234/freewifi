import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import os
import warnings
warnings.filterwarnings("ignore")

# Optional: For NLG summaries (template-based)
import random

sns.set_theme(style="whitegrid")

def load_business_data(business_type):
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "connection_logs")
    file_name = f"{business_type}.csv"
    file_path = os.path.join(data_dir, file_name)
    try:
        df = pd.read_csv(file_path)
        st.success(f"Loaded {len(df)} records from {business_type} dataset.")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def preprocess_data(df):
    # Rename for consistency
    if 'session_duration_minutes' in df.columns and 'duration' not in df.columns:
        df.rename(columns={'session_duration_minutes': 'duration'}, inplace=True)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df['hour_of_day'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    if 'frequent_visitor' in df.columns:
        df['frequent_visitor'] = (
            df['frequent_visitor'].astype(str).str.lower().map({'yes': 1, 'true': 1, 'no': 0, 'false': 0}).fillna(0).astype(int)
        )
    else:
        df['frequent_visitor'] = np.random.choice([0, 1], size=len(df), p=[0.7, 0.3])
    return df

def ai_customer_segmentation(df, business_type):
    # KMeans clustering
    clustering_features = ['duration', 'hour_of_day', 'frequent_visitor']
    features = [f for f in clustering_features if f in df.columns and pd.api.types.is_numeric_dtype(df[f])]
    df = df.dropna(subset=features)
    if len(df) < 3 or len(features) < 2:
        st.warning("Insufficient data/features for clustering.")
        return df
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])
    n_clusters = st.slider("Select number of clusters (K)", 2, 5, 3)
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)
    st.subheader("Customer Clusters")
    st.dataframe(df.groupby('Cluster')[features].mean().round(2))
    fig = px.scatter(df, x=features[0], y=features[1], color='Cluster', title='Customer Clusters', hover_data=features)
    st.plotly_chart(fig)
    return df

def ai_peak_time_prediction(df):
    st.subheader("Predicting Peak Hours/Days")
    if 'hour_of_day' in df.columns and 'timestamp' in df.columns:
        peak_hour = df['hour_of_day'].mode()[0]
        st.info(f"**Typical peak hour:** {peak_hour}:00")
        daily_counts = df['timestamp'].dt.date.value_counts().sort_index()
        peak_day = daily_counts.idxmax()
        st.info(f"**Busiest day:** {peak_day}")
        fig = px.bar(x=daily_counts.index, y=daily_counts.values, labels={'x':'Date', 'y':'Connections'}, title="Daily Connection Trend")
        st.plotly_chart(fig)
    else:
        st.warning("Insufficient time data for peak prediction.")

def ai_anomaly_detection(df):
    st.subheader("Anomaly Detection")
    if 'duration' in df.columns:
        model = IsolationForest(contamination=0.05)
        df['anomaly'] = model.fit_predict(df[['duration']].fillna(0))
        anomalies = df[df['anomaly'] == -1]
        st.write(f"Detected {len(anomalies)} anomalous sessions.")
        st.dataframe(anomalies[['duration', 'hour_of_day', 'frequent_visitor']])
    else:
        st.warning("No 'duration' feature for anomaly detection.")

def ai_churn_prediction(df):
    st.subheader("Churn Prediction (Likelihood User Won't Return)")
    if 'frequent_visitor' in df.columns and 'duration' in df.columns:
        # For demo: Predict "churn" as not frequent visitor with short duration
        df['churn_risk'] = ((df['frequent_visitor'] == 0) & (df['duration'] < 20)).astype(int)
        st.write("Sample churn risk (1 = high risk):")
        st.dataframe(df[['duration', 'frequent_visitor', 'churn_risk']].head())
        churn_rate = df['churn_risk'].mean() * 100
        st.info(f"Estimated churn risk in sample: {churn_rate:.1f}%")
    else:
        st.warning("Insufficient features for churn prediction.")

def ai_marketing_recommendations(df, business_type):
    st.subheader("Personalized Marketing Recommendations")
    # Example: simple rule-based for demonstration
    if 'Cluster' in df.columns:
        for c in sorted(df['Cluster'].unique()):
            group = df[df['Cluster'] == c]
            avg_duration = group['duration'].mean()
            freq_visitor_ratio = group['frequent_visitor'].mean() * 100
            if avg_duration > 60 and freq_visitor_ratio > 50:
                st.markdown(f"- **Cluster {c}: VIP/Loyal Customers**: Send loyalty rewards, exclusive offers.")
            elif avg_duration < 30:
                st.markdown(f"- **Cluster {c}: Quick Visitors**: Offer fast deals, express services, or grab-and-go promotions.")
            else:
                st.markdown(f"- **Cluster {c}: Diverse**: Use general promotions and survey for more info.")
    else:
        st.info("Cluster data unavailable for tailored marketing.")

def ai_time_series_forecasting(df):
    st.subheader("Time Series Forecasting")
    if 'timestamp' in df.columns:
        ts = df.set_index('timestamp').resample('D').size()
        if len(ts) > 7:
            try:
                model = ARIMA(ts, order=(1,1,1))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=7)
                st.line_chart(pd.concat([ts, forecast.rename('Forecast')]))
                st.write("Forecast for next 7 days:")
                st.dataframe(forecast.reset_index())
            except Exception as e:
                st.warning(f"Forecasting failed: {e}")
        else:
            st.warning("Not enough data for reliable time series forecasting.")
    else:
        st.warning("No timestamp data for time series analysis.")

def ai_nlg_summary(df, business_type):
    st.subheader("Automated Insight Summary")
    # Example: Template-based NLG (can be replaced with GPT/OpenAI API)
    if df.empty:
        st.info("No data to summarize.")
        return
    total = len(df)
    avg_duration = df['duration'].mean() if 'duration' in df.columns else None
    peak_hour = df['hour_of_day'].mode()[0] if 'hour_of_day' in df.columns else None
    freq_pct = df['frequent_visitor'].mean() * 100 if 'frequent_visitor' in df.columns else None
    msg = f"For your {business_type.replace('_', ' ').title()}, you had {total} WiFi sessions. "
    if avg_duration:
        msg += f"Average session lasted {avg_duration:.1f} minutes. "
    if peak_hour:
        msg += f"Peak usage was at {peak_hour}:00. "
    if freq_pct:
        msg += f"Returning visitors made up {freq_pct:.0f}% of all sessions."
    st.success(msg)

def show_ai_insights():
    st.header("🤖 AI-Powered Customer Insights: Advanced Analytics Suite")
    st.write("Select a business type and explore advanced, AI-driven insights for your WiFi analytics.")

    business_options = [
        "restaurant",
        "hospital",
        "business_cafe",
        "boutique",
        "supermarket"
    ]
    business_type = st.selectbox("Business Type", business_options)

    df = load_business_data(business_type)
    if df.empty:
        return
    df = preprocess_data(df)
    st.dataframe(df.head())

    # AI Features
    df = ai_customer_segmentation(df, business_type)
    ai_peak_time_prediction(df)
    ai_anomaly_detection(df)
    ai_churn_prediction(df)
    ai_marketing_recommendations(df, business_type)
    ai_time_series_forecasting(df)
    ai_nlg_summary(df, business_type)

# Streamlit entry point
#if __name__ == "__main__" or st._is_running_with_streamlit:
    #show_ai_insights()
