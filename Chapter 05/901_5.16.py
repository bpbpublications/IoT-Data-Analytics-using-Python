import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

class DataTransformationEngine:
    def __init__(self):
        pass
    
    def transform_data(self, df):
        # Check if all required columns are present in the DataFrame
        required_cols = ['rtc', 'temp', 'pressure', 'wind_speed', 'rpm', 'energy_output']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise KeyError(f"{missing_cols} not in index")   
        
        # # # Normalize the value column
        df['wind_speed'] = (df['wind_speed'] - df['wind_speed'].mean()) / df['wind_speed'].std()
        df['temp'] = (df['temp'] - df['temp'].mean()) / df['temp'].std()
        # # Remove columns with low variance
        numeric_cols = df.select_dtypes(include=np.number).columns
        variances = df[numeric_cols].var()
        cols_to_drop = variances[variances < 0.01].index
        df = df.drop(cols_to_drop, axis=1)

        # Create a new column 'energy_output_per_rpm' which represents energy output per rpm
        df['energy_output_per_rpm'] = df['energy_output'] / df['rpm']
        
        # Apply a rolling mean to the 'energy_output_per_rpm' column
        df['energy_output_per_rpm'] = df['energy_output_per_rpm'].rolling(window=3).mean()

        # Create a new column 'pressure_temp_ratio' which represents the ratio of pressure to temperature
        df['pressure_temp_ratio'] = df['pressure'] / df['temp']

        # Apply a rolling median to the 'pressure_temp_ratio' column
        df['pressure_temp_ratio'] = df['pressure_temp_ratio'].rolling(window=3).median()

        #Unit conversion for pressure: Convert the pressure values from Pascals (Pa) to kilopascals (kPa) and add a new column pressure_kPa to the DataFrame.
        df['pressure_kPa'] = df['pressure'] / 1000

        #Unit conversion for energy_output: Convert the energy output values from joules (J) to kilowatt-hours (kWh) and add a new column energy_output_kWh to the DataFrame.
        df['energy_output_kWh'] = df['energy_output'] / 3600000

        #Format conversion for pressure: Convert the pressure values to a string with two decimal places and add a new column pressure_str to the DataFrame.
        df['pressure_str'] = df['pressure'].apply(lambda x: '{:.2f}'.format(x))

        
        return df
        
