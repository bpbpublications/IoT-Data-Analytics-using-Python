import numpy as np
import datetime #This package has all datetime processing functions
import pandas as pd
# Set the random seed for reproducibility
np.random.seed(42)
# Define the number of data points to generate
num_rows = 1440 # This will generate 2000 rows of data
# Define the start and end dates for the data generation. This is required for time series analysis.
start_date = datetime.datetime(2023, 1, 1) #
end_date = datetime.datetime(2023, 1, 2)
# We simulate an IIOT equipment, wind turbine, for our simulation. Define the turbine parameters and their normal ranges
temperature_mean = 80
temperature_stddev = 10
pressure_mean = 300
pressure_stddev = 50
wind_speed_mean = 10
wind_speed_stddev = 5
rpm_mean = 1500
rpm_stddev = 250
energy_output_mean = 50
energy_output_stddev = 10
# Generate the data
timestamps = np.arange(start_date, end_date, dtype='datetime64[m]')
temperature = np.random.normal(temperature_mean, temperature_stddev, num_rows)
pressure = np.random.normal(pressure_mean, pressure_stddev, num_rows)
wind_speed = np.random.normal(wind_speed_mean, wind_speed_stddev, num_rows)
rpm = np.random.normal(rpm_mean, rpm_stddev, num_rows)
energy_output = np.random.normal(energy_output_mean, energy_output_stddev, num_rows)
# Combine the data into a single array
#data = np.column_stack((timestamps, temperature, pressure, wind_speed, rpm, energy_output))
# Save the data to a CSV file
data = pd.DataFrame({'timestamps': timestamps, 'temperature': temperature, 'pressure': pressure, 'wind_speed': wind_speed, 'rpm': rpm, 'energy_output': energy_output})
# Save the data to a CSV file using pandas and function ‘to_csv’
data.to_csv('wind_turbine.csv', index=False)
