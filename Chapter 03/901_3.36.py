import pandas as pd
import numpy as np
# Load data into a pandas DataFrame
df = pd.read_csv('wind_turbine.csv', parse_dates=['timestamps'], index_col='timestamps')
# Calculate autocorrelation with a lag of 1 day
autocorr = np.corrcoef(df['energy_output'][1:], df['energy_output'][:-1])[0, 1]
# Print the autocorrelation
print("Autocorrelation (lag=1):", autocorr)
