import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf


# Compute partial autocorrelation using the wind_turbine_data dataframe created earlier
fig, ax = plt.subplots()
plot_pacf(wind_turbine_data['power_output_100'], lags=20, method='ols', ax=ax)

# Plot partial autocorrelation
ax.set_title("Partial Autocorrelation of 'power_output_100'")
ax.set_xlabel("Lag")
ax.set_ylabel("Partial Autocorrelation")
plt.show()