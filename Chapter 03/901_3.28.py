import pandas as pd
turbine_data = pd.read_csv('wind_turbine.csv', parse_dates=["timestamps"])
wind_speed = turbine_data["wind_speed"]
print(wind_speed)
