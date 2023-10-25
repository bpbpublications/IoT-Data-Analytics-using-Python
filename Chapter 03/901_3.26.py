import numpy as np
import datetime #This package has all datetime processing functions
import pandas as pd
from scipy import stats
# Set the random seed for reproducibility
np.random.seed(42)
# Define the number of data points to generate
num_rows = 1440 # This will generate 1440 rows of data
# Define the start and end dates for the data generation. This is required for time series analysis.
start_date = datetime.datetime(2023, 1, 1) #
end_date = datetime.datetime(2023, 1, 2)
# We simulate an IIOT equipment, wind turbine, for our simulation. Define the turbine parameters and their normal ranges
temperature_mean = 80
temperature_stddev = 10
pressure_mean = 30000
pressure_stddev = 5000
wind_speed_mean = 10
wind_speed_stddev = 5
rpm_mean = 1500
rpm_stddev = 250
energy_output_mean = 50
energy_output_stddev = 10

# Generate the data
timestamps = np.arange(start_date, end_date, dtype='datetime64[m]')
temperature = np.random.normal(temperature_mean, temperature_stddev, num_rows)
pressure = np.random.normal(pressure_mean, pressure_stddev, num_rows)/ 100 # Scale pressure by a factor of 100
wind_speed = np.random.normal(wind_speed_mean, wind_speed_stddev, num_rows)
rpm = np.random.normal(rpm_mean, rpm_stddev, num_rows)
# Create a linear relationship between wind speed and energy output with a coefficient of 0.3
energy_output = energy_output_mean + 0.3 * (wind_speed -
wind_speed_mean) + np.random.normal(0, energy_output_stddev, num_rows)
# Introduce missing values by randomly setting 10% of the energy output values to NaN
energy_output_mask = np.random.rand(num_rows) < 0.1
energy_output[energy_output_mask] = np.nan
# Introduce outliers by randomly setting 20% of the rpm values to be greater than 3 standard deviations from the mean
rpm_outliers = np.random.rand(num_rows) < 0.2
rpm[rpm_outliers] = np.random.normal(loc=3, scale=1,
size=rpm_outliers.sum()) * rpm_stddev + rpm_mean
# Create duplicate rows by randomly selecting 10% of the data points and replicating them
duplicates = np.random.choice(num_rows, int(num_rows * 0.1), replace=False)
timestamps = np.concatenate([timestamps, timestamps[duplicates]])
temperature = np.concatenate([temperature, temperature[duplicates]])
pressure = np.concatenate([pressure, pressure[duplicates]])
wind_speed = np.concatenate([wind_speed, wind_speed[duplicates]])
rpm = np.concatenate([rpm, rpm[duplicates]])
energy_output = np.concatenate([energy_output, energy_output[duplicates]])
# Combine the data into a single array
data_wind_turbine = pd.DataFrame({'timestamps': timestamps,
'temperature': temperature, 'pressure': pressure, 'wind_speed':
wind_speed, 'rpm': rpm, 'energy_output': energy_output})
# Save the data to a file
data_wind_turbine.to_csv('wind_turbine_with_issues.csv', index=False)
