import pandas as pd
turbine_data = pd.read_csv('wind_turbine.csv', parse_dates=["timestamps"])
high_wind_speed = turbine_data[turbine_data["wind_speed"] > 15]
print(high_wind_speed)
