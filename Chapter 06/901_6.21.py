import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
# Load the time series data
data = data_external[['rtc', 'power_output_100']]
# Perform ADF test
result = adfuller(data['power_output_100'])
# Print the test results
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))
# Plot the time series data with critical values
plt.plot(data.index, data['power_output_100'], color='blue', label='Power Output')
plt.axhline(y=result[4]['1%'], color='red', linestyle='-', label='1% Critical Value')
plt.axhline(y=result[4]['5%'], color='green', linestyle='-', label='5% Critical Value')
plt.axhline(y=result[4]['10%'], color='orange', linestyle='-', label='10% Critical Value')
plt.xlabel('Timestamp')
plt.ylabel('Power Output')
plt.title('ADF Test Results')
plt.legend()
plt.show()
