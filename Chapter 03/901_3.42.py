import pandas as pd
# Read in the turbine data CSV file
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv')
# Add a new column to the data indicating the hour of the day
df_wind_turbine['hour'] = pd.to_datetime(df_wind_turbine['timestamps']).dt.hour
# Aggregate the data by hour, taking the mean of each column for each hour
hourly_data = df_wind_turbine.groupby('hour').mean()
# Save the aggregated data to a new CSV file
hourly_data.to_csv('turbine_data_hourly.csv')
