import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv', parse_dates=['timestamps'])
bins = [0, 5, 10, 15, 20, 25]
labels = ['0-5', '5-10', '10-15', '15-20', '20-25']
df_wind_turbine['wind_speed_range'] = pd.cut(df_wind_turbine['wind_speed'], bins=bins, labels=labels,
include_lowest=True)
grouped = df_wind_turbine.groupby('wind_speed_range').mean().reset_index()
plt.bar(grouped['wind_speed_range'], grouped['energy_output'])
plt.xlabel('Wind Speed Range (m/s)')
plt.ylabel('Mean Energy Output (kW)')
plt.title('Mean Energy Output by Wind Speed Range')
plt.show()
