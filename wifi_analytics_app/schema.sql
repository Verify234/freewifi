CREATE TABLE wifi_logs (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  device_id VARCHAR,
  device_type VARCHAR,
  location VARCHAR,
  first_visit TIMESTAMP,
  returning BOOLEAN,
  dwell_time INT,
  email VARCHAR,
  phone VARCHAR
);
cur.execute("""
    UPDATE wifi_logs 
    SET dwell_time = EXTRACT(EPOCH FROM (NOW()-first_visit))::INT
    WHERE "returning" = false
""")
DROP TABLE IF EXISTS wifi_logs;
