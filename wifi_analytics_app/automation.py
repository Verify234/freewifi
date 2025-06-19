from insights import connect_db
from datetime import datetime

def update_dwell_time():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE wifi_logs SET dwell_time = EXTRACT(EPOCH FROM (NOW()-first_visit))::INT
        WHERE "returning" = false
    """)
    conn.commit()
    cur.close()
    conn.close()
