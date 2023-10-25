import pandas as pd
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

# Calculate moving average of power output
window_size = 24 # choose window size
rolling_avg = wind_turbine_data['power_output_100'].rolling(window_size).mean()

# Plot original data and moving average
plt.plot(wind_turbine_data['rtc'], wind_turbine_data['power_output_100'], label='Original Data')
plt.plot(wind_turbine_data['rtc'], rolling_avg, label='Moving Average')

# Set plot labels and legend
plt.xlabel('Time')
plt.ylabel('Power Output')
plt.title('Original Data vs. Moving Average')
plt.legend()

# Show the plot
plt.show()