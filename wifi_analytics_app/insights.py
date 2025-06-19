import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime

def connect_db():
    return psycopg2.connect(
        host=st.secrets["PGHOST"],
        port=st.secrets["PGPORT"],
        user=st.secrets["PGUSER"],
        password=st.secrets["PGPASSWORD"],
        database=st.secrets["PGDATABASE"],
        sslmode="require"
    )

def load_data():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM wifi_logs", conn)
    conn.close()
    return df

def register_guest(email, phone, device_type):
    conn = connect_db()
    cur = conn.cursor()
    now = datetime.now()
    cur.execute("""
      INSERT INTO wifi_logs(device_id, device_type, first_visit, returning, dwell_time, email, phone)
      VALUES (%s,%s,%s,false,0,%s,%s)
    """, ("guest_device", device_type, now, email, phone))
    conn.commit()
    cur.close()
    conn.close()