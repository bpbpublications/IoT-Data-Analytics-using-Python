data_filtered = data_external.loc[:, ['month','day','hour','minute','temperature_100', 'wind_direction_100', 'wind_speed_100', 'pressure_100','power_output_100']]
plt.figure(figsize = (16,10))
sns.heatmap(data_filtered.corr(),annot = True)
