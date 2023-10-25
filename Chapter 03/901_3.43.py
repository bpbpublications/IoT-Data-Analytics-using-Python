import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load the wind turbine data into a pandas DataFrame
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv',
parse_dates=['timestamps'])
plt.scatter(df_wind_turbine['wind_speed'], df_wind_turbine['energy_output'])
plt.xlabel('Wind Speed')
plt.ylabel('Energy Output')
plt.title('Wind Speed vs Energy Output Scatter Plot')
plt.show()
