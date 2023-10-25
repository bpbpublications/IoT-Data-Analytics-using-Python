import pandas as pd
import numpy as np
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
# Keep only the relevant columns
wind_turbine_data = wind_turbine_data[["rtc", "wind_speed_100", "power_output_100",'wind_direction_100','temperature_100','pressure_100']]
# Convert the 'rtc' column to a datetime object
wind_turbine_data["rtc"] = pd.to_datetime(wind_turbine_data["rtc"])
# Set the 'rtc' column as the index
wind_turbine_data = wind_turbine_data.set_index("rtc")
# Create a new column for the hour of the day
wind_turbine_data["hour"] = wind_turbine_data.index.hour
# Create a new column for the day of the week
wind_turbine_data["day_of_week"] = wind_turbine_data.index.dayofweek
# Create a new column for the month of the year
wind_turbine_data["month"] = wind_turbine_data.index.month
# Create a new column for the season of the year
seasons = [(0, "winter"), (3, "spring"), (6, "summer"), (9, "fall")]
wind_turbine_data["season"] = pd.cut((wind_turbine_data.index.month % 12 + 3) // 3, bins=[s[0] for s in seasons] + [12], labels=[s[1] for s in seasons], right=False)
# Create a new column for the wind speed range
bins = [-np.inf, 3, 6, 9, 12, np.inf]
labels = ["<3", "3-6", "6-9", "9-12", ">12"]
wind_turbine_data["wind_speed_range"] = pd.cut(wind_turbine_data["wind_speed_100"], bins=bins, labels=labels)
# Create a new column for the power output range
bins = [-np.inf, 500, 1000, 1500, 2000, np.inf]
labels = ["<500", "500-1000", "1000-1500", "1500-2000", ">2000"]
wind_turbine_data["power_output_range"] = pd.cut(wind_turbine_data["power_output_100"], bins=bins, labels=labels)
# Define create table statement
create_table = """
CREATE TABLE analyticszone.wind_turbine_abt (
    wind_speed_100 FLOAT,
    power_output_100 FLOAT,
    wind_direction_100 FLOAT,
    temperature_100 FLOAT,
    pressure_100 FLOAT,
    hour INTEGER,
    day_of_week INTEGER,
    month INTEGER,
    season TEXT,
    wind_speed_range TEXT,
    power_output_range TEXT
);
"""

# drop and create table
cur.execute(f"DROP TABLE IF EXISTS analyticszone.wind_turbine_abt")
cur.execute(create_table)
conn.commit()
cur.close()
# Insert the data into the table
insert_cursor = conn.cursor()
abt_records = []
for index, row in wind_turbine_data.iterrows():
    value = (row['wind_speed_100'], row['power_output_100'], row['wind_direction_100'], row['temperature_100'],
             row['pressure_100'], row['hour'], row['day_of_week'], row['month'], row['season'],
             row['wind_speed_range'], row['power_output_range'])
    abt_records.append(value)

query = "INSERT INTO analyticszone.wind_turbine_abt VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
insert_cursor.executemany(query,  abt_records)
conn.commit()
insert_cursor.close()
conn.close()