import pandas as pd
# Read in the turbine data from the CSV file
turbine_data = pd.read_csv('wind_turbine.csv', parse_dates=["timestamps"])
# Print some basic statistics about the data
print("Basic statistics about the data:")
print(turbine_data.describe())
# Calculate the average energy output for each hour of the day
turbine_data["hour"] = turbine_data["timestamps"].dt.hour
hourly_energy_output = turbine_data.groupby("hour")["energy_output"].mean()
# Print the hourly energy output values
print("\nHourly energy output:")
print(hourly_energy_output)
# Calculate the correlation between wind speed and energy output
correlation = turbine_data["wind_speed"].corr(turbine_data["energy_output"])
# Print the correlation value
print("\nCorrelation between wind speed and energy output:")
print(correlation)
