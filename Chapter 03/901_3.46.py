import pandas as pd
import plotly.express as px
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv',
parse_dates=['timestamps'])
fig = px.scatter_matrix(df_wind_turbine, dimensions=['wind_speed', 'rpm', 'temperature', 'pressure',  'energy_output'])
fig.update_layout(title='Wind Turbine Scatter Plot')
fig.show()
