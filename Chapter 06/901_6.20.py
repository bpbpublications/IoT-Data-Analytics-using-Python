import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load the wind turbine time series dataset
data = data_external[['rtc','power_output_100']]
# Compute the mean and standard deviation of the energy output
mean_energy_output = data['power_output_100'].mean()
std_energy_output = data['power_output_100'].std()
# Compute the noise threshold based on the mean and standard deviation of the energy output
noise_threshold = mean_energy_output + 3*std_energy_output
# Identify the noisy data points where the energy output exceeds the noise threshold
noisy_data = data[data['power_output_100'] > noise_threshold]
# Plot the noisy data points
plt.figure()
plt.plot(data['rtc'], data['power_output_100'], 'b-', label='Energy Output')
plt.plot(noisy_data['rtc'], noisy_data['power_output_100'], 'ro', label='Noisy Data')
plt.fill_between(data['rtc'], noise_threshold, data['power_output_100'], alpha=0.2, color='grey', label='Noise Threshold')
plt.title('Wind Turbine Time Series with Noisy Data Points')
plt.xlabel('timestamp')
plt.ylabel('power_output_100')
plt.legend()
plt.show()
