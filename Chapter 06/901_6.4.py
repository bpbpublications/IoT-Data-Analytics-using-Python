import json
import numpy as np
import pandas as pd

class DataAnalyticsEngine:
    def __init__(self):
        pass


    def analyze_data(self, df):
        # Check if all required columns are present in the DataFrame
        required_cols = ['id', 'rtc','temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 
        'wind_direction_80', 'wind_speed_100', 'wind_speed_120', 'wind_speed_80', 'pressure_200', 'pressure_100', 'pressure_0', 'power_output_80', 
        'power_output_100', 'power_output_120']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise KeyError(f"{missing_cols} not in index")
    
        #Wind Speed to Power Output ratio calculation
        df['wind_speed_to_power_output_ratio_120'] = df['wind_speed_120'] / df['power_output_120']
        df['wind_speed_to_power_output_ratio_100'] = df['wind_speed_100'] / df['power_output_100']
        df['wind_speed_to_power_output_ratio_80'] = df['wind_speed_80'] / df['power_output_80']

        # Wind direction to Wind speed Ratio
        df['wind_direction_wind_speed_ratio_120'] = df['wind_direction_120'] / df['wind_speed_120']
        df['wind_direction_wind_speed_ratio_100'] = df['wind_direction_100'] / df['wind_speed_100']
        df['wind_direction_wind_speed_ratio_80'] = df['wind_direction_80'] / df['wind_speed_80']

        # Wind Speed to Pressure Ratio
        df['wind_speed_to_pressure_ratio_120'] = df['wind_speed_120'] / df['pressure_200']
        df['wind_speed_to_pressure_ratio_100'] = df['wind_speed_100'] / df['pressure_100']
        df['wind_speed_to_pressure_ratio_80'] = df['wind_speed_80'] / df['pressure_0']

        # Temperature to Power Output ratio
        df['temp_to_power_output_ratio_120'] = df['temperature_120'] / df['power_output_120']
        df['temp_to_power_output_ratio_100'] = df['temperature_100'] / df['power_output_100']
        df['temp_to_power_output_ratio_80'] = df['temperature_80'] / df['power_output_80']

        # Temperature to Wind Speed ratio
        df['temp_wind_speed_ratio_120'] = df['temperature_120'] / df['wind_speed_120']
        df['temp_wind_speed_ratio_100'] = df['temperature_100'] / df['wind_speed_100']
        df['temp_wind_speed_ratio_80'] = df['temperature_80'] / df['wind_speed_80']

        # Correlation between Wind Speed and Power Output
        df['wind_speed_to_power_output_corr_120'] = df['wind_speed_120'].corr(df['power_output_120'])
        df['wind_speed_to_power_output_corr_100'] = df['wind_speed_100'].corr(df['power_output_100'])
        df['wind_speed_to_power_output_corr_80'] = df['wind_speed_80'].corr(df['power_output_80'])

        # Correlation between Wind Direction and Wind Speed
        df['wind_direction_wind_speed_corr_120'] = df['wind_direction_120'].corr(df['wind_speed_120'])
        df['wind_direction_wind_speed_corr_100'] = df['wind_direction_100'].corr(df['wind_speed_100'])
        df['wind_direction_wind_speed_corr_80'] = df['wind_direction_80'].corr(df['wind_speed_80'])

        # Correlation between Temperature and Wind Speed 
        df['temp_wind_speed_corr_120'] = df['temperature_120'].corr(df['wind_speed_120'])
        df['temp_wind_speed_corr_100'] = df['temperature_100'].corr(df['wind_speed_100'])
        df['temp_wind_speed_corr_80'] = df['temperature_80'].corr(df['wind_speed_80'])

        # Correlation between Temperature and Power Output 
        df['temp_power_output_corr_120'] = df['temperature_120'].corr(df['power_output_120'])
        df['temp_power_output_corr_100'] = df['temperature_100'].corr(df['power_output_100'])
        df['temp_power_output_corr_80'] = df['temperature_80'].corr(df['power_output_80'])

        # Correlation between Pressure and Wind Speed
        df['pressure_wind_speed_corr_120'] = df['pressure_200'].corr(df['wind_speed_120'])
        df['pressure_wind_speed_corr_100'] = df['pressure_100'].corr(df['wind_speed_100'])
        df['pressure_wind_speed_corr_80'] = df['pressure_0'].corr(df['wind_speed_80'])

        # Correlation between Pressure and Power Output
        df['pressure_power_output_corr_120'] = df['pressure_200'].corr(df['power_output_120'])
        df['pressure_power_output_corr_100'] = df['pressure_100'].corr(df['power_output_100'])
        df['pressure_power_output_corr_80'] = df['pressure_0'].corr(df['power_output_80'])

        return df
