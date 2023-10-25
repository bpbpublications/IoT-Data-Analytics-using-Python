import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error

# Split the data into training and test sets
train_size = int(len(wind_turbine_data) * 0.8)
train, test = wind_turbine_data.iloc[:train_size], wind_turbine_data.iloc[train_size:]

# Define the number of lags for the AR model
lags = 10

# Fit the AR model to the training data
ar_model = AutoReg(train['power_output_100'], lags=lags)
ar_fit = ar_model.fit()

# Generate predictions on the test set
predictions = ar_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)

# Calculate the root mean squared error (RMSE)
mse = mean_squared_error(test['power_output_100'], predictions)
rmse = np.sqrt(mse)
print('Test RMSE: %.3f' % rmse)

# Plot the predicted and actual values
plt.plot(test.index, test['power_output_100'], label='Actual')
plt.plot(test.index, predictions, label='Predicted')
plt.xlabel('Time')
plt.ylabel('Power Output')
plt.legend()
plt.show()