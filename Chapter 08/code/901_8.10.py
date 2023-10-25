import psycopg2
import pandas as pd
import datetime
# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
except:
    print("Unable to connect to the database")
# Query the wind turbine data from the curated zone of the data lake
try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
    wind_turbine_data = pd.DataFrame(cur.fetchall(), columns=['id', 'rtc', 'year', 'month', 'day', 'hour', 'minute', 
                                                              'temperature_100', 'temperature_120', 'temperature_80', 
                                                              'wind_direction_100', 'wind_direction_120', 
                                                              'wind_direction_80', 'wind_speed_100','wind_speed_120',
                                                              'wind_speed_80','pressure_200','pressure_100','pressure_0',
                                                              'power_output_80','power_output_100','power_output_120'])
    cur.close()
except:
    print("Unable to fetch wind turbine data")    
#Query the maint_threshold table for temperature threshold extracted from product manual
# Query the wind turbine data from the curated zone of the data lake
try:
    conn = psycopg2.connect(
    host="localhost",
    database="IoTDataLake",
    user="postgres",
    password=""
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM maintenancezone.maint_thresholds")
    maint_threshold_data = pd.DataFrame(cur.fetchall(), columns=['tag', 'threshold'])
    cur.close()
except:
    print("Unable to fetch maint threshold data")
# Define the threshold for temperature
threshold = 'temperature'
temperature_threshold = maint_threshold_data[maint_threshold_data['tag'] == threshold]['threshold'].iloc[0]
print(f"The temperature threshold is {temperature_threshold}")
# Identify the time periods when the temperature is above the threshold
high_temperature_periods = wind_turbine_data.loc[wind_turbine_data['temperature_100'] > temperature_threshold]
# Calculate the duration of each high-temperature period
high_temperature_periods['Duration'] = (high_temperature_periods['rtc'] - high_temperature_periods['rtc'].shift())
# Identify the time periods when maintenance should be performed
maintenance_periods = high_temperature_periods.loc[high_temperature_periods['Duration'] > pd.Timedelta('1 hour')]
# Create a maintenance record
if not maintenance_periods.empty: 
    maint_actual_start = None
    maint_actual_end = None
    maint_schedule_start = datetime.datetime.now() + datetime.timedelta(hours=2)
    maint_schedule_end = maint_schedule_start + datetime.timedelta(hours=2)
    reason = "Preventive Maintenance based on high temperature"
    vendor = "Wind Turbine Solutions"
    description = "Perform preventive maintenance to reduce wear and tear due to high temperature"
    assignee = "John Doe"
    status = "Open"
    equipment_location = "Wind Turbine #1"
    priority = "High" 
   # Insert the maintenance record into the Postgres database
    cur = conn.cursor()
    cur.execute("INSERT INTO maintenancezone.maintanence_rec (maint_actual_start, maint_schedule_start, maint_schedule_end, reason, vendor, description, assignee, status, equipment_location, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (maint_actual_start, maint_schedule_start, maint_schedule_end, reason, vendor, description, assignee, status, equipment_location, priority))
    conn.commit()
    print("Maintenance record inserted successfully")
    conn.close()
else:
    print("No maintenance required")
