import pandas as pd
import numpy as np
def above_threshold(df, column, threshold):
    '''
    Function to check if the given column is above the threshold
    '''
    if df[column].max() > threshold:
        alert_msg = f"{column} is above the threshold of {threshold}"
        return alert_msg
    else:
        return None
def below_threshold(df, column, threshold):
    '''
    Function to check if the given column is below the threshold
    '''
    if df[column].min() < threshold:
        alert_msg = f"{column} is below the threshold of {threshold}"
        return alert_msg
    else:
        return None
def continuous_threshold(df, column, threshold, duration):
    '''
    Function to check if the given column is above the threshold continuously for the given duration
    '''
    continuous_count = 0
    for value in df[column]:
        if value > threshold:
            continuous_count += 1
        else:
            continuous_count = 0
        if continuous_count >= duration:
            alert_msg = f"{column} is continuously above the threshold of {threshold} for {duration} minutes"
            return alert_msg
    return None
# Example usage
wind_turbine_data = pd.DataFrame({'temperature_100': [30, 25, 30],
                           'pressure_100': [2000, 1100, 1200],
                           'wind_speed_100': [30, 15, 20],
                           'power_output_100': [1500, 2000, 2500]})
# Alert for wind speed above 25 m/s
alert1 = above_threshold(wind_turbine_data, 'wind_speed_100', 25)
if alert1:
    print(alert1)
# Alert for power output below 1000 kW
alert2 = below_threshold(wind_turbine_data, 'power_output_100', 1000)
if alert2:
    print(alert2)
# Alert for wind speed continuously above 20 m/s for 5 minutes
alert3 = continuous_threshold(wind_turbine_data, 'wind_speed_100', 20, 5)
if alert3:
    print(alert3)
