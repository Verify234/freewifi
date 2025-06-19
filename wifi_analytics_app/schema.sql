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
