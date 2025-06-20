# --- insights.py ---
import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    try:
        df = pd.read_csv("connection_logs.csv", names=["email", "phone", "location", "timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
    except:
        return pd.DataFrame(columns=["email", "phone", "location", "timestamp"])

def analytics_dashboard():
    st.header("📊 WiFi Analytics Dashboard")
    df = load_data()

    if df.empty:
        st.warning("No data available yet.")
        return

    st.metric("Total Connections", len(df))
    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date

    st.subheader("Connections by Hour")
    fig = px.histogram(df, x="hour", nbins=24)
    st.plotly_chart(fig)

    st.subheader("Connections Over Time")
    daily = df.groupby("date").size().reset_index(name="count")
    st.line_chart(daily.set_index("date"))

    st.download_button("Download Logs", df.to_csv(index=False), "wifi_logs.csv")
