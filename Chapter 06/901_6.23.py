import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import kpss
# Load the time series data
data = data_external[['rtc', 'power_output_100']]
# Perform KPSS test
result = kpss(data['power_output_100'], regression='c')
# Print the test results
print('KPSS Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[3].items():
    print('\t%s: %.3f' % (key, value))
# Plot the time series data with critical values
plt.plot(data['rtc'], data['power_output_100'])
plt.axhline(y=result[3]['1%'], color='y', linestyle='-')
plt.axhline(y=result[3]['5%'], color='g', linestyle='-')
plt.axhline(y=result[3]['10%'], color='r', linestyle='-')
plt.xlabel('Timestamp')
plt.ylabel('Power Output')
plt.title('KPSS Test Results')
plt.show()
