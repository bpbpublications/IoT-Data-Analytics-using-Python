import psycopg2
import pandas as pd
from MetricEngine import MetricEngine
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
def calculate_metrics_data():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
        # Read the timestamp of the last run from a separate table or file
    last_run_timestamp = '2023-03-11 11:39:35.922405'  # Replace with code to read the timestamp
    cur = conn.cursor()
    # Create the last run timetamp table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS metriczone.last_run_timestamp (
            
            rtc timestamp without time zone,
            job_id SERIAL PRIMARY KEY
            )
    ''')
    #select the latest record with the recent timestamp
    cur.execute("SELECT rtc FROM metriczone.last_run_timestamp ORDER BY job_id DESC LIMIT 1")
    result_timestamp = cur.fetchone()
    if result_timestamp is not None:
        last_run_timestamp = result_timestamp[0]
    print("last_run_timestamp ", last_run_timestamp)
    cur = conn.cursor()
    cur.execute("SELECT * FROM curatedzone.c_wind_turbine_data WHERE rtc > %s", (last_run_timestamp,))
    data = pd.DataFrame(cur.fetchall(), columns=['id','rtc', 'wind_speed', 'rpm', 'temp', 'pressure', 'energy_output', 'asset_id', 'serial_number'])
    # Calculate the metrics using the MetricEngine
    data_for_metrics = MetricEngine()
    metric_data = data_for_metrics.calculate_metrics(data)
    # Create the m_wind_turbine_metrics table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS metriczone.m_wind_turbine_metrics (
            id serial PRIMARY KEY,
            capacity_factor FLOAT,
            max_wind_speed FLOAT,
            min_wind_speed FLOAT,
            avg_wind_speed FLOAT,
            max_rpm FLOAT,
            min_rpm FLOAT,
            avg_rpm FLOAT,
            max_temperature FLOAT,
            min_temperature FLOAT,
            max_pressure FLOAT,
            min_pressure FLOAT,
            avg_pressure FLOAT,
            actual_energy_output FLOAT,
            max_energy_output FLOAT,
            mtbf FLOAT,
            mttr FLOAT,
            downtime FLOAT,
            hours_in_period FLOAT
        )
    ''')
    # Insert the calculated metric data into the m_wind_turbine_metrics table
    for i, row in metric_data.iterrows():
         cur.execute("""INSERT INTO metriczone.m_wind_turbine_metrics (capacity_factor, mtbf, mttr, downtime, max_wind_speed, min_wind_speed, avg_wind_speed, 
            max_rpm, min_rpm, avg_rpm, max_temperature, min_temperature, max_pressure, min_pressure, avg_pressure, max_energy_output, actual_energy_output, 
            hours_in_period ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s)
            """, (row['capacity_factor'], row['mtbf'], row['mttr'],row['downtime'],row['max_wind_speed'],row['min_wind_speed'],row['avg_wind_speed'],row['max_rpm'],
                row['min_rpm'],row['avg_rpm'],row['max_temperature'],row['min_temperature'],row['max_pressure'],row['min_pressure'],row['avg_pressure'],
                row['max_energy_output'],row['actual_energy_output'], row['hours_in_period']))
        conn.commit()
    # Update the timestamp of the last run to the current time
    cur.execute("INSERT INTO metriczone.last_run_timestamp (rtc) VALUES (%s) ON CONFLICT (job_id) DO UPDATE SET rtc = EXCLUDED.rtc", (datetime.now(),))
    conn.commit()
calculate_metrics_data()
