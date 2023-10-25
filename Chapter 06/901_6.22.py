import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import matplotlib.pyplot as plt
# Select two columns for the Granger Causality Test
data_granger = data_external[['wind_speed_100', 'power_output_100']]
# Run the Granger Causality Test with a maximum lag of 5 time periods
maxlag = 5
granger_test_results = grangercausalitytests(data_granger, maxlag=maxlag, verbose=False)
# Print the p-values for each lag
for lag in range(1, maxlag+1):
    print(f'Lag {lag}: p-value = {granger_test_results[lag][0]["ssr_ftest"][1]:.3f}')
# Plot the lag plot for the Granger Causality Test
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
for i, var in enumerate(['wind_speed_100', 'power_output_100']):
    ax = axes[i]
    ax.set_title(f'Lag Plot for {var}')
    lag_plot(data_granger[var], ax=ax)
plt.tight_layout()
plt.show()
