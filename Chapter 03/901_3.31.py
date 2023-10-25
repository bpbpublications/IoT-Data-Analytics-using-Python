import pandas as pd
turbine_data = pd.read_csv('wind_turbine.csv', parse_dates=["timestamps"])
turbine_data_with_issues = pd.read_csv('wind_turbine_with_issues.csv', parse_dates=["timestamps"])
combined_data = pd.merge(turbine_data, turbine_data_with_issues, on="timestamps")
print(combined_data)
