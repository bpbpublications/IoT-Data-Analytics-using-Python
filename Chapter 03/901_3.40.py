from scipy import stats
import numpy as np
import pandas as pd
# Load the wind turbine data into a pandas dataframe
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv')
z = np.abs(stats.zscore(df_wind_turbine['rpm']))
print(z)
print(np.where(z > 3))
df_wind_turbine = df_wind_turbine[z<3]
z = np.abs(stats.zscore(df_wind_turbine['rpm']))
print(z)
print(np.where(z > 3))

