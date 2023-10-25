import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
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
data = wind_turbine_data[["rtc", "wind_speed_100", "power_output_100"]]

# Convert the 'rtc' column to a datetime object
data["rtc"] = pd.to_datetime(data["rtc"])

# Set the 'rtc' column as the index
data = data.set_index("rtc")

# Split the data into training and testing sets
train_size = int(len(data) * 0.8)
train_data = data.iloc[:train_size]
test_data = data.iloc[train_size:]

# Fit the ARIMA model
model = ARIMA(train_data["power_output_100"], exog=train_data["wind_speed_100"], order=(1, 1, 1))
model_fit = model.fit()

# Predict the power output for the test data
predictions = model_fit.predict(start=test_data.index[0], end=test_data.index[-1], exog=test_data["wind_speed_100"])

# Plot the actual and predicted power output
plt.plot(test_data.index, test_data["power_output_100"], label="Actual")
plt.plot(predictions.index, predictions, label="Predicted")
plt.legend()
plt.show()

# Evaluate the model's performance
mse = ((predictions - test_data["power_output_100"]) ** 2).mean()
print("ARIMA Test MSE:", mse)