import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# Load the wind turbine data into a pandas dataframe
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv')
# Normalize data using MinMaxScaler
scaler = MinMaxScaler()
timestamps = df_wind_turbine['timestamps']
df_wind_turbine = df_wind_turbine.drop('timestamps', axis = 1)
df_wind_turbine_normalized = pd.DataFrame(scaler.fit_transform(df_wind_turbine), columns=df_wind_turbine.columns)
df_wind_turbine_normalized.insert(0,'timestamps',timestamps)
print(df_wind_turbine_normalized.describe())
df_wind_turbine_normalized.head() # Save the scaled data to a CSV file
df_wind_turbine_normalized.to_csv('wind_turbine_scaled.csv', index=False)
