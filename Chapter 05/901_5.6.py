import json
import psycopg2
# Connect to the PostgreSQL database
conn = psycopg2.connect(database="IoTDataLake", user="postgres", password="", host="localhost", port="5432")
# Open the JSON file and load the data
with open("gateway_reg.json", "r") as f:
    data = json.load(f)
# Loop through the devices and insert them into the database
for device in data["devices"]:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO rawzone.device_master (device_id, device_name, description, manufacturer, model, serial_number, asset_id, location_latitude, location_longitude, properties_measurement_interval, connectivity_protocol, connectivity_host, connectivity_port, connectivity_username, connectivity_password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """,
        (
            device["device_id"],
            device["device_name"],
            device["description"],
            device["manufacturer"],
            device["model"],
            device["serial_number"],
            device["asset_id"],
            device["location"]["latitude"],
            device["location"]["longitude"],
            device["properties"]["measurement_interval"],
            device["connectivity"]["protocol"],
            device["connectivity"]["host"],
            device["connectivity"]["port"],
            device["connectivity"]["username"],
            device["connectivity"]["password"]

        )
    )
    conn.commit()
# Close the database connection
conn.close()
