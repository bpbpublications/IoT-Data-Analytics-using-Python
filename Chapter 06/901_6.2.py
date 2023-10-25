import pandas as pd
import numpy as np
import psycopg2
# Read the CSV file which is downloaded and renamed
df = pd.read_csv('wind_data_new.csv', skiprows=6)
# Convert the time columns to a datetime object and add a new column called rtc
df['rtc'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute']])
cols = list(df.columns)
cols.remove('rtc')
cols = ['rtc'] + cols
df = df[cols]
# Define the constants
rho = 1.225 # Air density at sea level (kg/m^3)
d = 150 # Diameter of the rotor (m)
r = d/2 # Radius of the rotor (m)
A = np.pi*r**2 # Swept area of the rotor (m^2)
Cp = 0.38 # Power coefficient of the turbine
# Calculate wind speed at hub height 80m
df['Wind Speed at 80m (m/s)'] = df['Wind Speed at 80m (m/s)']*np.log(80/0.1)/np.log(120/0.1)
# Calculate wind speed at hub height 100m
df['Wind Speed at 100m (m/s)'] = df['Wind Speed at 100m (m/s)']*np.log(80/0.1)/np.log(120/0.1)
# Calculate wind speed at hub height 120m
df['Wind Speed at 120m (m/s)'] = df['Wind Speed at 120m (m/s)']*np.log(80/0.1)/np.log(120/0.1)
# Calculate the power output for 80m, 100m and 120m
df['Power Output at 80m (kW)'] = 0.5*rho*A*Cp*(df['Wind Speed at 80m (m/s)']*1000/3600)**3
df['Power Output at 100m (kW)'] = 0.5*rho*A*Cp*(df['Wind Speed at 100m (m/s)']*1000/3600)**3
df['Power Output at 120m (kW)'] = 0.5*rho*A*Cp*(df['Wind Speed at 120m (m/s)']*1000/3600)**3

# Set up database connection
conn = psycopg2.connect(database="IoTDataLake", user="postgres", password="", host="localhost", port="5432")
cur = conn.cursor()
# Create wind turbine data table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS curatedzone.c_external_wind_turbine_data (
        id SERIAL PRIMARY KEY,
        rtc TIMESTAMP NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        hour INTEGER NOT NULL,
        minute INTEGER NOT NULL,
        temperature_100 FLOAT,
        temperature_120 FLOAT,
        temperature_80 FLOAT,
        wind_direction_100 FLOAT,
        wind_direction_120 FLOAT,
        wind_direction_80 FLOAT,
        wind_speed_100 FLOAT,
        wind_speed_120 FLOAT,
        wind_speed_80 FLOAT,
        pressure_200 FLOAT,
        pressure_100 FLOAT,
        pressure_0 FLOAT,
        power_output_80 FLOAT,
        power_output_100 FLOAT,
        power_output_120 FLOAT
    )
""")
59.	# Insert the transformed data into the c_external_wind_turbine_data table in the curated zone of the data lake
60.	for i, row in df.iterrows():
61.	 cur.execute(""INSERT INTO curatedzone.c_external_wind_turbine_data (rtc, year, month, day, hour, minute, temperature_100, temperature_120, "
 temperature_80, wind_direction_100, wind_direction_120, wind_direction_80, wind_speed_100, wind_speed_120, wind_speed_80, pressure_200, pressure_100, pressure_0,
  power_output_80, power_output_100, power_output_120) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s, %s, %s)
    """, (row['rtc'], row['Year'], row['Month'], row['Day'],row['Hour'],row['Minute'], row['Temperature at 100m (C)'],row['Temperature at 120m (C)'],
     row['Temperature at 80m (C)'], row['Wind Direction at 100m (Degrees)'], row['Wind Direction at 120m (Degrees)'], row['Wind Direction at 80m (Degrees)'], 
     row['Wind Speed at 100m (m/s)'], row['Wind Speed at 120m (m/s)'], row['Wind Speed at 80m (m/s)'], row['Pressure at 200m (atm)'], row['Pressure at 100m (atm)'],
     row['Pressure at 0m (atm)'], row['Power Output at 80m (kW)'], row['Power Output at 100m (kW)'], row['Power Output at 120m (kW)'] ))
 conn.commit()
cur.close()
conn.close()
