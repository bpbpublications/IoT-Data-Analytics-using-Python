import pandas as pd
import numpy as np
# Load the wind turbine data into a pandas dataframe
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv')
print(df_wind_turbine.isnull().sum())
# Replace using mean
mean = df_wind_turbine['energy_output'].mean()
df_wind_turbine['energy_output'].fillna(mean, inplace=True)
print(df_wind_turbine.isnull().sum())
