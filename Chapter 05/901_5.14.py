import json
import numpy as np
import pandas as pd

class DataCleaningEngine:
    def __init__(self):
        pass

    def clean_data(self, df):
        # Drop duplicate rows
        df = df.drop_duplicates()
        # Drop rows with missing values
        df = df.dropna()
        # # Convert string timestamps to datetime format
        df['rtc'] = pd.to_datetime(df['rtc'])
        # # # Clean data using additional rules
        # # # Remove leading/trailing whitespaces from all columns
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # # # Remove special characters from column names
        df.columns = df.columns.str.replace('[^a-zA-Z0-9_]', '')
        # # # Convert all string values to lowercase
        df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)     
        # # # drop rows which are empty
        df = df.dropna()
        # # # # Remove rows with data outside a certain range. They will create noise due to IoT Sensor malfunction
        df = df[(df['temp'] >= 10) & (df['temp'] <= 150)]
        df = df[(df['pressure'] >= 800) & (df['pressure'] <= 1200)]
        df = df[(df['wind_speed'] >= 0) & (df['wind_speed'] <= 200)]
        df = df[(df['rpm'] >= 0) & (df['rpm'] <= 3000)]
        df = df[(df['energy_output'] >= 0) & (df['energy_output'] <= 2000)]        
        return df
