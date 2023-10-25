import pandas as pd
import numpy as np
# Load the wind turbine data into a pandas dataframe
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv')
print(df_wind_turbine.duplicated().sum())
df_wind_turbine = df_wind_turbine.drop_duplicates()
print(df_wind_turbine.duplicated().sum())
