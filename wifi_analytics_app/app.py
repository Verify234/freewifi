import streamlit as st
from splash import splash_page
from auth import login_widget
from automation import update_dwell_time
from insights import load_data

login_widget()
if "user" not in st.session_state:
    st.stop()
    
st.title("WiFi Analytics Dashboard")
st.autorefresh(interval=5000)

df = load_data()
st.dataframe(df)

if st.session_state.get("role") == "admin":
    if st.button("Download CSV"):
        csv = df.to_csv(index=False)
        st.download_button("Download", csv, file_name="wifi_data.csv")

    if st.button("Trigger Webhook"):
        import requests
        r = requests.post(st.secrets["WEBHOOK_URL"], json=df.to_dict(orient="records"))
        st.success(f"Webhook triggered! Status: {r.status_code}")
