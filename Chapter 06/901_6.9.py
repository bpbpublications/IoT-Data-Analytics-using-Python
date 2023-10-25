# Visual inspection of linearity using scatter plot for wind speed and power output
sns.scatterplot(data=data_external, x='wind_speed_100', y='power_output_100')
plt.show()