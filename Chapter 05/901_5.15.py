import psycopg2
import pandas as pd
from data_cleaning_engine import DataCleaningEngine
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from data_cleaning_engine import DataCleaningEngine


def clean_data():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
    # Initialize last run timestamp
    last_run_timestamp = '2023-03-11 11:39:35.922405'  # Replace with code to read the timestamp
    # Read the data inserted after the last run from the raw data table
    cur = conn.cursor()
    # Create the last run timetamp table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS curatedzone.last_run_timestamp (
            
            rtc timestamp without time zone,
            job_id SERIAL PRIMARY KEY
            )
    ''')
    #select the latest record with the recent timestamp
    cur.execute("SELECT rtc FROM curatedzone.last_run_timestamp ORDER BY job_id DESC LIMIT 1")
    result_timestamp = cur.fetchone()

    if result_timestamp is not None:

        last_run_timestamp = result_timestamp[0]

    print("last_run_timestamp ", last_run_timestamp)
   
    cur.execute("SELECT * FROM rawzone.r_wind_turbine_data WHERE rtc > %s", (last_run_timestamp,))
    data = pd.DataFrame(cur.fetchall(), columns=['id','rtc', 'wind_speed', 'rpm', 'temp', 'pressure', 'energy_output', 'asset_id', 'serial_number'])
    print("data " , data)
    # Clean the data using the DataCleaningEngine
    clean_engine = DataCleaningEngine()
    cleaned_data = clean_engine.clean_data(data)
    print(cleaned_data)

    # Create the c_wind_turbine_data table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS curatedzone.c_wind_turbine_data (
            id integer PRIMARY KEY,
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

    # Insert the cleaned data into the c_wind_turbine_data table
    for i, row in cleaned_data.iterrows():
        last_timestamp = row['rtc']
        cur.execute("""INSERT INTO curatedzone.c_wind_turbine_data (id, rtc, wind_speed, rpm, temp, pressure, energy_output, asset_id, serial_number) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['id'], row['rtc'], row['wind_speed'], row['rpm'], row['temp'],row['pressure'],row['energy_output'],row['asset_id'],row['serial_number']))

        conn.commit()

    # Update the timestamp of the last run to the current time
    cur.execute("INSERT INTO curatedzone.last_run_timestamp (rtc) VALUES (%s) ON CONFLICT (job_id) DO UPDATE SET rtc = EXCLUDED.rtc", (datetime.now(),))
    conn.commit()

# Create a scheduler that runs the clean_data function every 1 minute.
scheduler = BackgroundScheduler()
scheduler.add_job(clean_data, 'interval', minutes=1)

# Start the scheduler
scheduler.start()

# Keep the program running
while True:
    pass