import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
wind_turbine_data = data_external[['power_output_100']]
# perform stationary analysis
def stationary_analysis(wind_turbine_data ):
    # calculate rolling mean and standard deviation
    rolmean = wind_turbine_data .rolling(window=12).mean()
    rolstd = wind_turbine_data.rolling(window=12).std()
    # plot rolling statistics
    plt.plot(wind_turbine_data , color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    # perform Augmented Dickey-Fuller test
    print('Results of Augmented Dickey-Fuller Test:')
    adf_test = adfuller(wind_turbine_data['power_output_100'], autolag='AIC')
    adf_output = pd.Series(adf_test[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in adf_test[4].items():
        adf_output['Critical Value (%s)'%key] = value
    print(adf_output)
# perform non-stationary analysis
def non_stationary_analysis(wind_turbine_data):
    decomposition = seasonal_decompose(wind_turbine_data, model='additive', freq=12)
    # plot the decomposition
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1, figsize=(15,8))
    wind_turbine_data.plot(ax=ax1)
    ax1.set(title='Original Data')
    decomposition.trend.plot(ax=ax2)
    ax2.set(title='Trend Component')
    decomposition.seasonal.plot(ax=ax3)
    ax3.set(title='Seasonal Component')
    decomposition.resid.plot(ax=ax4)
    ax4.set(title='Residual Component')
    plt.tight_layout()
    plt.show()
# call the functions
stationary_analysis(wind_turbine_data)
non_stationary_analysis(wind_turbine_data)
