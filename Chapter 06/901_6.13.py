def plot_df(wind_speed_df, x, y, title="", xlabel='rtc', ylabel='Wind Speed', dpi=100):
    plt.figure(figsize=(15,4), dpi=dpi)
    decomposition = sm.tsa.seasonal_decompose(y, model='additive', freq=30) # perform seasonal decomposition
    trend = decomposition.trend # extract trend component
    seasonal = decomposition.seasonal # extract seasonal component
    plt.plot(x, y, color='yellow', label='Original Data') # plot original data in gray
    plt.plot(x, trend, color='blue', label='Trend') # plot trend component in blue
    plt.plot(x, seasonal, color='red', label='Seasonality') # plot seasonal component in red
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.legend()
    plt.show()
plot_df(data_external, x=data_external['rtc'], y=data_external['wind_speed_100'], title='Trend and Seasonality of wind speed')
