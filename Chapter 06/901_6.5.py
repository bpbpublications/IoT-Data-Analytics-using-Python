import psycopg2
import pandas as pd
from DataAnalyticsEngine import DataAnalyticsEngine
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
def analyze_data():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
        # Assign the timestamp
    last_run_timestamp = '2000-01-11 11:39:35.922405'  # Replace with code to read the timestamp
    # Read the data inserted after the last run from the curated data table
    cur = conn.cursor()
    # Create the last_run_timestamp table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS analyticszone.last_run_timestamp_wt (
            rtc timestamp without time zone,
            job_id SERIAL PRIMARY KEY
            )
    ''')
    cur.execute("SELECT rtc FROM analyticszone.last_run_timestamp_wt ORDER BY job_id DESC LIMIT 1")
    result_timestamp = cur.fetchone()
    if result_timestamp is not None:
        last_run_timestamp = result_timestamp[0]
    print("last_run_timestamp ", last_run_timestamp)
    cur = conn.cursor()
    cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data WHERE rtc > %s", (last_run_timestamp,))
    data = pd.DataFrame(cur.fetchall(), columns=['id','rtc','year', 'month', 'day', 'hour', 'minute', 'temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 
     'wind_direction_80', 'wind_speed_100','wind_speed_120','wind_speed_80','pressure_200','pressure_100','pressure_0','power_output_80','power_output_100',
     'power_output_120'])
    data_analyzer = DataAnalyticsEngine() #call the data analytical engine
    anlyzed_data = data_analyzer.analyze_data(data)
    print(anlyzed_data.head(5))
    # Create the a_external_wind_turbine_data table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS analyticszone.a_external_wind_turbine_data (
            wind_speed_to_power_output_ratio_100 FLOAT,
            wind_speed_to_power_output_ratio_120 FLOAT,
            wind_speed_to_power_output_ratio_80 FLOAT,
            wind_direction_wind_speed_ratio_100 FLOAT,
            wind_direction_wind_speed_ratio_120 FLOAT,
            wind_direction_wind_speed_ratio_80 FLOAT,
            wind_speed_to_pressure_ratio_100 FLOAT,
            wind_speed_to_pressure_ratio_120 FLOAT,
            wind_speed_to_pressure_ratio_80 FLOAT,
            temp_to_power_output_ratio_100 FLOAT,
            temp_to_power_output_ratio_120 FLOAT,
            temp_to_power_output_ratio_80 FLOAT,
            temp_wind_speed_ratio_100 FLOAT,
            temp_wind_speed_ratio_120 FLOAT,
            temp_wind_speed_ratio_80 FLOAT,
            wind_speed_to_power_output_corr_100 FLOAT,
            wind_speed_to_power_output_corr_120 FLOAT,
            wind_speed_to_power_output_corr_80 FLOAT,
            wind_direction_wind_speed_corr_100 FLOAT,
            wind_direction_wind_speed_corr_120 FLOAT,
            wind_direction_wind_speed_corr_80 FLOAT,
            temp_wind_speed_corr_100 FLOAT,
            temp_wind_speed_corr_120 FLOAT,
            temp_wind_speed_corr_80 FLOAT,
            temp_power_output_corr_100 FLOAT,
            temp_power_output_corr_120 FLOAT,
            temp_power_output_corr_80 FLOAT,
            pressure_wind_speed_corr_100 FLOAT,
            pressure_wind_speed_corr_120 FLOAT,
            pressure_wind_speed_corr_80 FLOAT,
            pressure_power_output_corr_100 FLOAT,
            pressure_power_output_corr_120 FLOAT,
            pressure_power_output_corr_80 FLOAT
        )
    ''')
    # Insert the analyzed data into the a_external_wind_turbine_data table in the analytical zone of the data lake
    for i, row in anlyzed_data.iterrows():
        cur.execute("""INSERT INTO analyticszone.a_external_wind_turbine_data (wind_speed_to_power_output_ratio_100 ,
            wind_speed_to_power_output_ratio_120 ,
            wind_speed_to_power_output_ratio_80 ,
            wind_direction_wind_speed_ratio_100 ,
            wind_direction_wind_speed_ratio_120 ,
            wind_direction_wind_speed_ratio_80 ,
            wind_speed_to_pressure_ratio_100 ,
            wind_speed_to_pressure_ratio_120 ,
            wind_speed_to_pressure_ratio_80 ,
            temp_to_power_output_ratio_100 ,
            temp_to_power_output_ratio_120 ,
            temp_to_power_output_ratio_80 ,
            temp_wind_speed_ratio_100 ,
            temp_wind_speed_ratio_120 ,
            temp_wind_speed_ratio_80 ,
            wind_speed_to_power_output_corr_100 ,
            wind_speed_to_power_output_corr_120 ,
            wind_speed_to_power_output_corr_80 ,
            wind_direction_wind_speed_corr_100 ,
            wind_direction_wind_speed_corr_120 ,
            wind_direction_wind_speed_corr_80 ,
            temp_wind_speed_corr_100 ,
            temp_wind_speed_corr_120 ,
            temp_wind_speed_corr_80 ,
            temp_power_output_corr_100 ,
            temp_power_output_corr_120 ,
            temp_power_output_corr_80 ,
            pressure_wind_speed_corr_100 ,
            pressure_wind_speed_corr_120 ,
            pressure_wind_speed_corr_80 ,
            pressure_power_output_corr_100 ,
            pressure_power_output_corr_120 ,
            pressure_power_output_corr_80 ) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s ,%s, %s, %s, %s, %s, 
            %s, %s, %s, %s,%s ,%s, %s)
            """, (row['wind_speed_to_power_output_ratio_100'], row['wind_speed_to_power_output_ratio_120'], row['wind_speed_to_power_output_ratio_80'], row['wind_direction_wind_speed_ratio_100'], 
             row['wind_direction_wind_speed_ratio_120'], row['wind_direction_wind_speed_ratio_80'],row['wind_speed_to_pressure_ratio_100'],
             row['wind_speed_to_pressure_ratio_120'],row['wind_speed_to_pressure_ratio_80'], row['temp_to_power_output_ratio_100'], 
             row['temp_to_power_output_ratio_120'], row['temp_to_power_output_ratio_80'], row['temp_wind_speed_ratio_100'], row['temp_wind_speed_ratio_120'], 
                row['temp_wind_speed_ratio_80'], row['wind_speed_to_power_output_corr_100'], row['wind_speed_to_power_output_corr_120'], 
                row['wind_speed_to_power_output_corr_80'], row['wind_direction_wind_speed_corr_100'],row['wind_direction_wind_speed_corr_120'],
                row['wind_direction_wind_speed_corr_80'], row['temp_wind_speed_corr_100'], row['temp_wind_speed_corr_120'],
                row['temp_wind_speed_corr_80'], row['temp_power_output_corr_100'], row['temp_power_output_corr_120'],
                row['temp_power_output_corr_80'],row['pressure_wind_speed_corr_100'], row['pressure_wind_speed_corr_120'],row['pressure_wind_speed_corr_80'],
                row['pressure_power_output_corr_100'],row['pressure_power_output_corr_120'], row['pressure_power_output_corr_80']  ))
        conn.commit()
    # Update the timestamp of the last run to the current time
    cur.execute("INSERT INTO analyticszone.last_run_timestamp_wt (rtc) VALUES (%s) ON CONFLICT (job_id) DO UPDATE SET rtc = EXCLUDED.rtc", (datetime.now(),))
    conn.commit()
analyze_data()
