import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
#Print the plot within the page
%matplotlib inline

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

# Compute autocorrelation
autocorr = wind_turbine_data['power_output_100'].autocorr()

# Plot autocorrelation
fig, ax = plt.subplots(figsize=(12, 6))
pd.plotting.autocorrelation_plot(wind_turbine_data['power_output_100'], ax=ax)
ax.set_title(f"Autocorrelation of 'power_output_100' (Lag-1 autocorrelation: {autocorr:.2f})")
plt.show()