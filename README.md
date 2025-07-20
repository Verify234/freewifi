# 📡 AI-Powered Free WiFi Analytics App

Empowering Nigerian small businesses with real-time customer insights from free WiFi usage.

---

## 🧩 Problem Statement

In Nigeria, many small businesses—cafés, salons, kiosks, and lounges—offer free WiFi to customers. Yet, few have the tools to understand who’s connecting, when, and how often. This lack of insight leads to missed opportunities for customer retention and optimized services.

This project helps these businesses make smarter decisions using AI-powered analytics based on WiFi usage patterns.

---

## 📊 Features & Value Proposition

- **Customer Segmentation**: Clustering users based on session patterns, frequency, and duration.
- **Usage Analytics**: Track peak hours, repeat visitors, and session behaviors.
- **Visual Dashboard**: Streamlit-powered, mobile-friendly interface with clear graphs and insights.
- **Local Use Cases**: Designed with Nigerian businesses in mind—tailors, cafés, phone charging stations, and more.

---

## 🧠 Methodology

1. **Data Collection**: Simulated WiFi session logs (device IDs, connection times, durations).
2. **Data Cleaning**: Remove duplicates, fill in missing data, and standardize formats.
3. **EDA**: Discover trends—e.g., most active periods, average session length.
4. **Segmentation**: Apply clustering algorithms (e.g., KMeans) to categorize user behavior.
5. **Visualization**: Build dashboards for easy interpretation and business action.

---

## 📦 Dataset Overview

> *Note: This app uses simulated data for development purposes. You may upload your own WiFi session logs.*

- **Fields**: Timestamp, Device ID, Duration (mins), Frequency, Bandwidth
- **Source**: Simulated using `data_generator.py`
- **Size**: 500+ records for testing

---

## 🛠️ Tech Stack

| Component            | Purpose                        |
|---------------------|--------------------------------|
| Python              | Core language                  |
| Pandas, NumPy       | Data manipulation              |
| Scikit-learn        | Clustering & ML                |
| Matplotlib, Seaborn | Data Visualization             |
| Streamlit           | Web dashboard                  |

---

## 🔍 Key Insights

> What Nigerian small business owners can discover:

- Most users connect during lunchtime (12–2PM).
- 35% of devices are repeat visitors—potential loyal customers.
- Power users (long sessions) account for 60% of data volume.

> Future ideas: Predictive recommendations for loyalty programs or targeted discounts.

---

## 🚀 How to Use

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt


---
<img width="1366" height="764" alt="AI Dashboard" src="https://github.com/user-attachments/assets/912c19af-c359-4343-9b88-411376159423" />
<img width="1306" height="694" alt="Freewifi dashboard" src="https://github.com/user-attachments/assets/faf782c2-cec7-4b41-ba18-1332625aa0a9" />
