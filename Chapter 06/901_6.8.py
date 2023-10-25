#Using the Box plot will help us understand the outliers
plt.figure(figsize=(18,6))
plt.title('Distribution of wind_speed_100 ')
sns.boxplot(y=data_external.wind_speed_100)