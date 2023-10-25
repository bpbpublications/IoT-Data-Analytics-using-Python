import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Print the plot within the page
%matplotlib inline
# set seaborn theme
sns.set(style="white")

conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
cur = conn.cursor()
cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
data_external = pd.DataFrame(cur.fetchall(), columns=['id','rtc','year', 'month', 'day', 'hour', 'minute', 'temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 
     'wind_direction_80', 'wind_speed_100','wind_speed_120','wind_speed_80','pressure_200','pressure_100','pressure_0','power_output_80','power_output_100',
     'power_output_120'])
# Inspecting the percentages of Null values again
print(round(100*(data_external.isnull().sum()/len(data_external.index)), 2))
