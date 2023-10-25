from kafka import KafkaConsumer
import psycopg2
import json

# Set up Kafka consumer
consumer = KafkaConsumer('wind-turbine-data', bootstrap_servers=['localhost:9092'])

# Set up Postgres connection
conn = psycopg2.connect(
    host="localhost",
    database="IoTDataLake",
    user="postgres",
    password=""
)
cur = conn.cursor()

# Create table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS rawzone.r_wind_turbine_data (
        id SERIAL PRIMARY KEY,
        rtc TIMESTAMP,
        wind_speed FLOAT,
        rpm FLOAT,
        temp FLOAT,
        pressure FLOAT,
        energy_output FLOAT,
        asset_id VARCHAR(20),
        serial_number VARCHAR(20)
    )
''')
conn.commit()

# Read data from Kafka topic and insert into Postgres
for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    header = data['header']
    asset_id = header['asset_id'][0]
    serial_number = header['serial_number']
    data = data['data'][0]
    rtc = data['rtc']
    wind_speed = data['wind_speed']
    rpm = data['rpm']
    temp = data['temp']
    pressure = data['pressure']
    energy_output = data['energy_output']
    cur.execute(f"INSERT INTO rawzone.r_wind_turbine_data (rtc, wind_speed, rpm, temp, pressure, energy_output, asset_id, serial_number) VALUES ('{rtc}', {wind_speed}, {rpm}, {temp}, {pressure}, {energy_output}, '{asset_id}', '{serial_number}')")
    conn.commit()
    print(f"Inserted data: {data}")

# Close Postgres connection
cur.close()
conn.close()
