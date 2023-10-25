import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import psycopg2
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
except:
    print("Unable to connect to the database")

# Query the wind turbine data from the curated zone of the data lake
try:
    cur = conn.cursor()
    cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
    wind_turbine_data = pd.DataFrame(cur.fetchall(), columns=['id', 'rtc', 'year', 'month', 'day', 'hour', 'minute', 
                                                              'temperature_100', 'temperature_120', 'temperature_80', 
                                                              'wind_direction_100', 'wind_direction_120', 
                                                              'wind_direction_80', 'wind_speed_100','wind_speed_120',
                                                              'wind_speed_80','pressure_200','pressure_100','pressure_0',
                                                              'power_output_80','power_output_100','power_output_120'])
    cur.close()
except:
    print("Unable to fetch wind turbine data")

# Split the data into training and testing sets
train, test = train_test_split(wind_turbine_data, test_size=0.2)

# Train a linear regression model on the training data
model = LinearRegression()
model.fit(train[['wind_speed_100', 'temperature_100', 'pressure_100']], train['power_output_100'])

# Predict the power output on the testing data
test['predicted_power_output'] = model.predict(test[['wind_speed_100', 'temperature_100', 'pressure_100']])

#finding MAE (Mean Absolute Error)
mae = mean_absolute_error(test['power_output_100'], test['predicted_power_output'])

# Set a threshold for the MAE to determine whether the wind turbine requires maintenance or not
threshold = 20

# Check if the MAE exceeds the threshold
if mae > threshold:
    print("The wind turbine requires maintenance.")
else:
    print("The wind turbine does not require maintenance.")
    
# Visualize the predicted vs actual power output on a scatter plot
colors = ['red' if p_actual > p_predicted else 'blue' for p_actual, p_predicted in zip(test['power_output_100'], test['predicted_power_output'])]
plt.scatter(test['power_output_100'], test['predicted_power_output'], color=colors)
plt.xlabel('Actual Power Output')
plt.ylabel('Predicted Power Output')
