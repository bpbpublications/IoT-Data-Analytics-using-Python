import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load the wind turbine data into a pandas DataFrame
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv',
parse_dates=['timestamps'])
sns.regplot(x='wind_speed', y='energy_output', data=df_wind_turbine)
plt.xlabel('Wind Speed')
plt.ylabel('Energy Output')
plt.title('Wind Speed vs Energy Output with Regression Line')
plt.show()
