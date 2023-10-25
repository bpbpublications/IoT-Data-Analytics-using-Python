# Box Plot
import seaborn as sns
import pandas as pd
import numpy as np
# Load the wind turbine data into a pandas dataframe
df_wind_turbine = pd.read_csv('wind_turbine_with_issues.csv')
sns.boxplot(df_wind_turbine['rpm'])
