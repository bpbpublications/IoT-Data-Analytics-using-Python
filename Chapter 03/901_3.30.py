import pandas as pd
turbine_data = pd.read_csv('wind_turbine.csv', parse_dates=["timestamps"])
hourly_data = turbine_data.groupby(turbine_data["timestamps"].dt.hour).mean()
print(hourly_data[["wind_speed", "energy_output"]])
