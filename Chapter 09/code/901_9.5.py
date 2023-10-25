import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import psycopg2
# Connect to datalake
conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
cur = conn.cursor()
# Query curated zone of the data lake for the wind turbine table and create a dataframe 
cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
wind_turbine_data = pd.DataFrame(cur.fetchall(), columns=['id', 'rtc', 'year', 'month', 'day', 'hour', 'minute', 
 'temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 'wind_direction_80', 'wind_speed_100','wind_speed_120', 'wind_speed_80','pressure_200','pressure_100','pressure_0', 'power_output_80','power_output_100','power_output_120'])
# Define the threshold values for each parameter
thresholds = {'temperature_100': 25, 'pressure_100': 1100, 'wind_speed_100': 15, 'power_output_100': 2000}
# Create a new column 'Above_Threshold' in the training dataset based on the threshold values
wind_turbine_data['Above_Threshold'] = np.where((wind_turbine_data['temperature_100'] > thresholds['temperature_100']) |
                                                (wind_turbine_data['pressure_100'] > thresholds['pressure_100']) |
                                                (wind_turbine_data['wind_speed_100'] > thresholds['wind_speed_100']) |
                                                (wind_turbine_data['power_output_100'] > thresholds['power_output_100']),
                                                1, 0)
# Select the columns to use for modeling
features = ['temperature_100', 'pressure_100', 'wind_speed_100', 'power_output_100']
# Split the data into training and testing sets
train_data = wind_turbine_data.sample(frac=0.8, random_state=42)
test_data = wind_turbine_data.drop(train_data.index)
# Standardize the data
scaler = StandardScaler()
scaler.fit(train_data[features])
train_data_scaled = scaler.transform(train_data[features])
test_data_scaled = scaler.transform(test_data[features])
# Build the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(train_data_scaled, train_data['Above_Threshold'])
# Save the model as a pickle file
with open('alert_model.pkl', 'wb') as f:
    pickle.dump((model, scaler, thresholds), f)
