import statsmodels.api as sm
decomposition = sm.tsa.seasonal_decompose(data_external['power_output_100'], model='additive',freq=7)
fig = decomposition.plot()
plt.show()
