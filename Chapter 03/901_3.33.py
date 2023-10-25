import pandas as pd
import numpy as np
# Load data into a pandas DataFrame
df = pd.read_csv('wind_turbine.csv', parse_dates=['timestamps'], index_col='timestamps')
# Calculate summary statistics
print("Minimum power:", np.min(df['energy_output']))
print("Maximum power:", np.max(df['energy_output']))
print("Mean power:", np.mean(df['energy_output']))
print("Standard deviation of power:", np.std(df['energy_output']))
print("Correlation between wind speed and energy:", np.corrcoef(df['wind_speed'], df['energy_output'])[0, 1])
