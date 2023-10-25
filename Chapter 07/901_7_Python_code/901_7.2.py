import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import psycopg2

#Connect to datalake
conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )

cur = conn.cursor()
#Query curated zone of the data lake for the wind turbine table and create a dataframe 
cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
wind_turbine_data= pd.DataFrame(cur.fetchall(), columns=['id','rtc','year', 'month', 'day', 'hour', 'minute', 'temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 
    	'wind_direction_80', 'wind_speed_100','wind_speed_120','wind_speed_80','pressure_200','pressure_100','pressure_0','power_output_80','power_output_100',
    	'power_output_120'])

# Define the maximum lag value to consider
max_lag = 10

# Create a list to store the correlation coefficients for each lag value
corrs = []

# Calculate the correlation coefficients for each lag value up to max_lag
for lag in range(1, max_lag+1):
    # Create a new dataframe with lagged values
    cols_to_lag = ['power_output_100', 'wind_speed_100']
    for i in range(1, lag+1):
        for col in cols_to_lag:
            wind_turbine_data[col + '(t-' + str(i) + ')'] = wind_turbine_data[col].shift(i)

    # Drop rows with NaN values
    df_lagged = wind_turbine_data.dropna()

    # Calculate the correlation matrix
    corr_matrix = df_lagged.corr()

    # Extract the correlation coefficient between the power output at time t and time t-lag
    corr = corr_matrix.loc['power_output_100', 'power_output_100(t-' + str(lag) + ')']

    # Append the correlation coefficient to the list of correlations
    corrs.append(corr)

# Plot the correlation coefficients for each lag value
plt.plot(range(1, max_lag+1), corrs)
plt.xlabel('Lag')
plt.ylabel('Correlation Coefficient')
plt.show()