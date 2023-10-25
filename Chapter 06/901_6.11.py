# Linearity testing using Pearson correlation coefficient for power output and wind speed
from scipy.stats import pearsonr, spearmanr
corr, p = pearsonr(data_external['power_output_100'], data_external['wind_speed_100'])
print('Pearson correlation coefficient between power output and wind speed:', corr)
print('p-value:', p)
