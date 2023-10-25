import psycopg2
import pandas as pd
# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
except Exception as e:
    print("Unable to connect to the database")
    print(e)

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
except Exception as e:
    print("Unable to fetch wind turbine data")
    print(e)

# Define the threshold for power output
threshold = 2000

# Calculate the moving average of the power output
rolling_avg = wind_turbine_data['power_output_100'].rolling(window=24).mean()

# Identify the time periods when the power output is below the threshold and the rolling average
low_power_periods = wind_turbine_data.loc[(wind_turbine_data['power_output_100'] < threshold) & (wind_turbine_data['power_output_100'] < rolling_avg)]

# Calculate the duration of each low-power period
low_power_periods['Duration'] = (low_power_periods['rtc'] - low_power_periods['rtc'].shift())

# Identify the time periods when maintenance should be performed
maintenance_periods = low_power_periods.loc[low_power_periods['Duration'] > pd.Timedelta('1 day')]

# Compute the start and end times of the maintenance period
maint_start = maintenance_periods['rtc'].min()
maint_end = maintenance_periods['rtc'].min() + pd.Timedelta('6 hours')

# Create a single maintenance record
maintenance_record = pd.DataFrame({
    'maint_actual_start': [maint_start],
    'maint_actual_end': [maint_end],
    'maint_schedule_start': [maint_start + pd.Timedelta('1 day')],
    'maint_schedule_end': [maint_end + pd.Timedelta('1 day')],
    'reason': ['Preventive Maintenance'],
    'vendor': ['ABC Company'],
    'description': ['Inspect and clean the turbine blades'],
    'assignee': ['John Doe'],
    'status': ['Scheduled'],
    'equipment_location': ['Turbine 1'],
    'priority': ['High']
})

# Insert the maintenance record into the maintenance table
try:
    cur = conn.cursor()
    cur.execute("INSERT INTO maintenancezone.maintanence_rec (maint_schedule_start, maint_schedule_end, reason, vendor, description, assignee, status, equipment_location, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (maintenance_record['maint_schedule_start'][0], maintenance_record['maint_schedule_end'][0], maintenance_record['reason'][0], maintenance_record['vendor'][0], maintenance_record['description'][0], maintenance_record['assignee'][0], maintenance_record['status'][0], maintenance_record['equipment_location'][0], maintenance_record['priority'][0]))
    # Commit
    conn.commit()
    print("Maintenance record inserted successfully")
except:
    print("Unable to insert maintenance record")
finally:
    # Close the cursor and connection
    cur.close()
    conn.close()
