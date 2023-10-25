import pandas as pd
turbine_data = pd.read_csv('wind_turbine.csv', parse_dates=["timestamps"])
print(turbine_data)
