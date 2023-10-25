import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
# Load the wind turbine data into a Pandas DataFrame
wind_turbine_data = data_external[['rtc','power_output_100']]
# Set the timestamp column as the index of the DataFrame
wind_turbine_data.set_index("rtc", inplace=True)
# Fit an ARIMA model to the data
model = sm.tsa.ARIMA(wind_turbine_data["power_output_100"], order=(1, 1, 1))
fitted_model = model.fit()
# Generate forecasts for the next month
forecasts = fitted_model.forecast(steps=720)
# Convert the forecasted dates to the same format as the original dates
last_date = wind_turbine_data.index[-1]
forecasted_dates = pd.date_range(last_date, periods=720+1, freq="H")[1:]
# Extract the forecasted values from the forecasts array
forecasted_values = forecasts[0]
# Create a new figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
# Plot the actual wind speed data and the forecasts
ax1.plot(wind_turbine_data["power_output_100"], label="Actual Power Output")
ax1.plot(forecasted_dates, forecasted_values, label="Forecasted Power Output", color="red")
ax1.set(title="Actual and Forecasted Power Output Data", ylabel="Power Output")
ax1.legend()
# Plot the residuals of the model
ax2.plot(fitted_model.resid)
ax2.set(title="Residuals of the ARIMA Model", ylabel="Residuals")
# Adjust the layout of the subplots
plt.tight_layout()
# Display the plot
plt.show()
