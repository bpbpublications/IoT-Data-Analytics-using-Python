import psycopg2
import pandas as pd
# Connect to PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
except:
    print("Unable to connect to database")

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
# Define the threshold for power output
threshold = 20
# Identify the time periods when the power output is below the threshold
low_power_periods = wind_turbine_data[wind_turbine_data['power_output_100'] < threshold]
# Calculate the duration of each low-power period
low_power_periods['Duration'] = low_power_periods['rtc'] - low_power_periods['rtc'].shift()
# Identify the time periods when corrective maintenance should be performed
corrective_maintenance_periods = low_power_periods[low_power_periods['Duration'] > pd.Timedelta('3 hour')]
# Insert a new record in the maintenance table for each corrective maintenance period
if len(corrective_maintenance_periods) > 0:
    maint_actual_start = corrective_maintenance_periods.iloc[0]['rtc']
    maint_actual_end = corrective_maintenance_periods.iloc[-1]['rtc'] + pd.Timedelta('1 hour')
    maint_schedule_start = maint_actual_start
    maint_schedule_end = maint_actual_end + pd.Timedelta('7 days')
    reason = 'Low power output'
    vendor = 'ABC Wind Turbine Services'
    description = 'Corrective maintenance for low power output'
    assignee = 'John Doe'
    status = 'Open'
    equipment_location = 'Wind turbine A'
    priority = 'High'
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO maintenancezone.maintanence_rec (maint_actual_start, maint_actual_end, maint_schedule_start, maint_schedule_end, reason, vendor, description, assignee, status, equipment_location, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (maint_actual_start, maint_actual_end, maint_schedule_start, maint_schedule_end, reason, vendor, description, assignee, status, equipment_location, priority))
        conn.commit()
        cur.close()
    except:
        print("Unable to insert maintenance record")
# Output the corrective maintenance periods
print(corrective_maintenance_periods[['rtc', 'power_output_100', 'Duration']])
# Close the database connection
conn.close()
