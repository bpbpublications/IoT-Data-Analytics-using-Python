from autots import AutoTS
import pandas as pd
import matplotlib.pyplot as plt
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
                                                          'temperature_100', 'temperature_120', 'temperature_80', 
                                                          'wind_direction_100', 'wind_direction_120', 
                                                          'wind_direction_80', 'wind_speed_100','wind_speed_120',
                                                          'wind_speed_80','pressure_200','pressure_100','pressure_0',
                                                          'power_output_80','power_output_100','power_output_120'])
# Set the index to the timestamp column
wind_turbine_data.set_index('rtc', inplace=True)

# Specify the models to use
models = ['ARIMA', 'ETS']

# Fit AutoTS model with specified models
model = AutoTS(forecast_length=24, frequency='H', ensemble='weighted', max_generations=5, num_validations=2, model_list=models)
model.fit(wind_turbine_data['power_output_100'])
# Fit AutoTS model with Prophet
#model = AutoTS(forecast_length=24, frequency='H', ensemble='weighted', max_generations=5, num_validations=2)
#model.fit(df['power_output_100'])

# Make predictions
predictions = model.predict()

# Create a new figure with a bigger size
fig = plt.figure(figsize=(10, 6))

# Plot actual vs predicted
plt.plot(wind_turbine_data.index[-24:], wind_turbine_data['power_output_100'][-24:], label='Actual')
plt.plot(predictions.forecast.index[-24:], predictions.forecast[-24:], label='Predicted')
plt.legend()
plt.show()

