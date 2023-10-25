import pandas as pd
import pandas as pd
from scipy.stats import chi2_contingency
import psycopg2
# Define database connection parameters
host = 'localhost'
dbname = 'IoTDataLake'
user = 'postgres'
password = ""
# Define function to execute SQL query and return result as DataFrame
def execute_query(query):
    # Connect to database
    conn = psycopg2.connect(
        host=host,
        database=dbname,
        user=user,
        password=""
    )
    # Execute query and fetch result
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    # Get column names from cursor description
    col_names = [desc[0] for desc in cur.description]
    # Convert result to pandas DataFrame
    df = pd.DataFrame(result, columns=col_names)
    # Close cursor and database connection
    cur.close()
    conn.close()
    # Return DataFrame
    return df
# Load the wind turbine dataset from the curated zone of the data lake
df = execute_query('SELECT * FROM curatedzone.c_external_wind_turbine_data')
# assume df is your original DataFrame
stats = df.describe()
# reset the index of the stats DataFrame
stats.reset_index(inplace=True)
# create a list of descriptions
descriptions = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
# create a new DataFrame with descriptions as a column
stats_t = pd.DataFrame({'description': descriptions})
# merge the stats and stats_t DataFrames
stats_t = pd.concat([stats_t, stats], axis=1)
stats_t = stats_t.drop('index', axis=1)
# Change the data type of the "description" column to text
stats_t['description'] = stats_t['description'].astype(str)
table_name = "analyticszone.a_stats_wind_turbine"
#Connect to database
conn = psycopg2.connect(
        host=host,
        database=dbname,
        user=user,
        password=""
    )
# Create cursor object
cur = conn.cursor()                                     
# Create table query
create_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        metric_description TEXT,
        id DOUBLE PRECISION,
        temperature_100 DOUBLE PRECISION,
        temperature_120 DOUBLE PRECISION,
        temperature_80 DOUBLE PRECISION,
        wind_direction_100 DOUBLE PRECISION,
        wind_direction_120 DOUBLE PRECISION,
        wind_direction_80 DOUBLE PRECISION,
        wind_speed_100 DOUBLE PRECISION,
        wind_speed_120 DOUBLE PRECISION,
        wind_speed_80 DOUBLE PRECISION,
        pressure_200 DOUBLE PRECISION,
        pressure_100 DOUBLE PRECISION,
        pressure_0 DOUBLE PRECISION,
        power_output_80 DOUBLE PRECISION,
        power_output_100 DOUBLE PRECISION,
        power_output_120 DOUBLE PRECISION
    );
"""
79.	# Execute create table query
80.	cur.execute(create_query)
81.	# Commit the changes
82.	conn.commit()
83.	# Insert the transformed data into the a_basic_stats_wind_turbine table in the analytics zone of the data lake
84.	for i, row in stats_t.iterrows():
85.	    cur.execute(""INSERT INTO analyticszone.a_stats_wind_turbine (metric_description, id, temperature_100, temperature_120, temperature_80, wind_direction_100, "
    wind_direction_120, wind_direction_80, wind_speed_100, wind_speed_120, wind_speed_80, pressure_200, pressure_100, 
    pressure_0, power_output_80, power_output_100, power_output_120) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (row['description'], row['id'], row['temperature_100'], row['temperature_120'], row['temperature_80'],row['wind_direction_100'],row['wind_direction_120'],
    row['wind_direction_80'],row['wind_speed_100'], row['wind_speed_120'], row['wind_speed_80'], row['pressure_200'],
    row['pressure_100'], row['pressure_0'], row['power_output_80'], row['power_output_100'], row['power_output_120']  ))
    conn.commit()
cur.close()
conn.close()
# display the new DataFrame
print(stats_t)
