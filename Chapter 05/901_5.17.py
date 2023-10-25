import psycopg2
import pandas as pd
from DataTransformationEngine import DataTransformationEngine
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def transform_data():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
        # Assign the timestamp
    last_run_timestamp = '2023-03-11 11:39:35.922405'  # Replace with code to read the timestamp
    # Read the data inserted after the last run from the curated data table
    cur = conn.cursor()
    # Create the last_run_timestamp table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transformationzone.last_run_timestamp (
            
            rtc timestamp without time zone,
            job_id SERIAL PRIMARY KEY
            )
    ''')
    cur.execute("SELECT rtc FROM transformationzone.last_run_timestamp ORDER BY job_id DESC LIMIT 1")
    result_timestamp = cur.fetchone()

    if result_timestamp is not None:

        last_run_timestamp = result_timestamp[0]

    print("last_run_timestamp ", last_run_timestamp)
    cur = conn.cursor()
    cur.execute("SELECT * FROM curatedzone.c_wind_turbine_data WHERE rtc > %s", (last_run_timestamp,))
    data = pd.DataFrame(cur.fetchall(), columns=['id','rtc', 'wind_speed', 'rpm', 'temp', 'pressure', 'energy_output', 'asset_id', 'serial_number'])
    data_transformer = DataTransformationEngine()
    transformed_data = data_transformer.transform_data(data)
    print(transformed_data.columns)
    # Create the t_wind_turbine_data table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transformationzone.t_wind_turbine_data (
            id integer PRIMARY KEY,
            rtc TIMESTAMP,
            wind_speed FLOAT,
            rpm FLOAT,
            temp FLOAT,
            pressure FLOAT,
            energy_output FLOAT,
            asset_id VARCHAR(20),
            serial_number VARCHAR(20),
            energy_output_per_rpm FLOAT,
            pressure_temp_ratio FLOAT,
            pressure_kPa FLOAT,
            energy_output_kWh FLOAT,
            pressure_str varchar(80)


        )
    ''')
    # Insert the transformed data into the t_wind_turbine_data table in the transformation zone of the data lake
    for i, row in transformed_data.iterrows():
        
        cur.execute("""INSERT INTO transformationzone.t_wind_turbine_data (id, rtc, wind_speed, rpm, temp, pressure, energy_output, asset_id, serial_number, 
            energy_output_per_rpm, pressure_temp_ratio, pressure_kPa, energy_output_kWh, pressure_str) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['id'], row['rtc'], row['wind_speed'], row['rpm'], row['temp'],row['pressure'],row['energy_output'],row['asset_id'],row['serial_number'], 
                row['energy_output_per_rpm'], row['pressure_temp_ratio'], row['pressure_kPa'], row['energy_output_kWh'], row['pressure_str'] ))
        conn.commit()
    # Update the timestamp of the last run to the current time
    cur.execute("INSERT INTO transformationzone.last_run_timestamp (rtc) VALUES (%s) ON CONFLICT (job_id) DO UPDATE SET rtc = EXCLUDED.rtc", (datetime.now(),))
    conn.commit()
# Create a scheduler that runs the transform_data function every 1 minute
scheduler = BackgroundScheduler()
scheduler.add_job(transform_data, 'interval', minutes=1)
# Start the scheduler
scheduler.start()
# Keep the program running
while True:
    pass