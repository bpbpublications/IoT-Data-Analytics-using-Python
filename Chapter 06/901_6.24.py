import pandas as pd
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
# Load the time series data
data = data_external[['rtc', 'power_output_100']]
# Extract the power output column
power_output = data['power_output_100']
# Run the Phillips-Perron test
pp_test = ts.adfuller(power_output, regression='ct')
# Print the test results
print('Phillips-Perron Test Results:')
print('ADF Statistic:', pp_test[0])
print('p-value:', pp_test[1])
print('Critical Values:')
for key, value in pp_test[4].items():
    print('\t%s: %.3f' % (key, value))
# Plot the time series data with critical values
plt.plot(data['rtc'], power_output, label='Power Output')
plt.axhline(y=pp_test[4]['1%'], color='y', linestyle='--', label='1% Critical Value')
plt.axhline(y=pp_test[4]['5%'], color='g', linestyle='--', label='5% Critical Value')
plt.axhline(y=pp_test[4]['10%'], color='r', linestyle='--', label='10% Critical Value')
plt.legend()
plt.title('Phillips-Perron Test Results')
plt.xlabel('Timestamp')
plt.ylabel('Power Output')
plt.show()
