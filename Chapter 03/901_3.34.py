import pandas as pd
import numpy as np
# Load data into a pandas DataFrame
df = pd.read_csv('wind_turbine.csv', parse_dates=['timestamps'], index_col='timestamps')
# Calculate the moving average with a window size of 7 days
moving_avg = df['energy_output'].rolling(window='7D').mean()
# Print the moving average for the first 10 rows
print(moving_avg.head(10))
