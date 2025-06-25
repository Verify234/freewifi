# AI-Powered Free WiFi Analytics App

This app provides WiFi usage analytics and customer segmentation for small businesses using Streamlit and AI.

---

## 1. Problem Statement

Small businesses offering free WiFi often lack insights into customer behavior and usage patterns. This project aims to help businesses make data-driven decisions by providing analytics and customer segmentation based on WiFi usage data.

---

## 2. Dataset Used

- **Description**: (Describe the dataset here—e.g., anonymized logs from WiFi access points including timestamps, device IDs, session durations, and usage patterns.)
- **Source**: (Mention if it's real, simulated, or from a public source.)
- **Size & Features**: (Briefly list main columns/features.)

---

## 3. Methodology & Key Steps

1. **Data Collection**: Gathered WiFi usage logs from access points.
2. **Data Cleaning**: Removed duplicates, handled missing values, and standardized formats.
3. **Exploratory Data Analysis (EDA)**: Identified user trends, peak usage times, and session distributions.
4. **Customer Segmentation**: Applied clustering algorithms (e.g., KMeans) to segment users based on their WiFi usage patterns.
5. **Visualization**: Built interactive dashboards using Streamlit for business users.

---

## 4. Technologies & Libraries

- **Python**: Core programming language
- **Pandas, NumPy**: Data manipulation and analysis
- **Scikit-learn**: Machine learning and clustering
- **Matplotlib, Seaborn**: Data visualization
- **Streamlit**: Web app/dashboard development

---

## 5. Key Findings & Model Performance

- (Insert key insights, such as most common customer segments, peak usage times, or overall traffic trends.)
- (Provide any model metrics or clustering results, e.g., silhouette score for clustering.)

---

## 6. How to Run the Code

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2. **Run the Streamlit app**:
    ```bash
    streamlit run wifi_analytics_app/app.py
    ```
3. **Upload your WiFi usage data and explore the dashboard.**

---
