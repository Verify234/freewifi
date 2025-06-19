import random
from datetime import datetime
import psycopg2

def generate_fake_data():
    device_types = ['Android', 'iOS', 'Windows', 'Mac']
    locations = ['Entrance', 'Aisle 1', 'Aisle 2', 'Checkout', 'Waiting Area']

    data = {
        'timestamp': datetime.now(),
        'device_type': random.choice(device_types),
        'location': random.choice(locations),
        'device_id': f"device_{random.randint(1000, 9999)}"
    }
    return data

def insert_into_postgres(data):
    conn = psycopg2.connect(
        host="localhost", database="wifi_analytics", user="your_user", password="your_password"
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO wifi_logs (timestamp, device_type, location, device_id)
        VALUES (%s, %s, %s, %s)
    """, (data['timestamp'], data['device_type'], data['location'], data['device_id']))
    conn.commit()
    cur.close()
    conn.close()

# Example usage
data = generate_fake_data()
insert_into_postgres(data)
