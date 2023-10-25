import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
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

# Smooth the power output using a rolling window average with a window size of 24
wind_turbine_data['power_output_100_smoothed'] = wind_turbine_data['power_output_100'].rolling(window=24).mean()

# Split the data into training and test sets
train_size = int(len(wind_turbine_data) * 0.8)
train, test = wind_turbine_data.iloc[:train_size], wind_turbine_data.iloc[train_size:]

# Define the number of lags for the AR model
lags = 10

# Fit the AR model to the smoothed training data
ar_model = AutoReg(train['power_output_100_smoothed'].dropna(), lags=lags)
ar_fit = ar_model.fit()

# Generate predictions on the test set
predictions = ar_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)

# Calculate the root mean squared error (RMSE)
mse = mean_squared_error(test['power_output_100'], predictions)
rmse = np.sqrt(mse)
print('Test RMSE: %.3f' % rmse)

# Plot the actual and smoothed power output along with the predicted values
plt.plot(test.index, test['power_output_100'], label='Actual', color='blue')
plt.plot(wind_turbine_data.index, wind_turbine_data['power_output_100_smoothed'], label='Smoothed', color='green')
plt.plot(test.index, predictions, label='Predicted', color='red')
plt.xlabel('Time')
plt.ylabel('Power Output')
plt.legend()
plt.show()