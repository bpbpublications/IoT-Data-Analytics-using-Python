import pandas as pd
import numpy as np
# Load data into a pandas DataFrame
df = pd.read_csv('wind_turbine.csv', parse_dates=['timestamps'], index_col='timestamps')
# Calculate the exponential moving average with a span of 7 days
exp_moving_avg = df['energy_output'].ewm(span=7).mean()
# Print the exponential moving average for the first 10 rows
print(exp_moving_avg.head(10))
