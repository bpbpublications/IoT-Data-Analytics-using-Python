import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
# Load the wind turbine data with weekly frequency
wind_turbine_data = data_external[['rtc', 'wind_speed_100']]
# Set the timestamp column as the index of the DataFrame
wind_turbine_data.set_index("rtc", inplace=True)
# Perform seasonal decomposition on the wind speed data
decomposition = sm.tsa.seasonal_decompose(wind_turbine_data["wind_speed_100"], model="additive", freq=7)
# Get the seasonal and deseasonalized components of the wind speed data
seasonal_component = decomposition.seasonal
deseasonalized_wind_speed = decomposition.resid
# Create a new figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
# Plot the original wind speed data
ax1.plot(wind_turbine_data["wind_speed_100"])
ax1.set(title="Original Wind Speed Data")
