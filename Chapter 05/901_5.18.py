import pandas as pd
class MetricEngine:
    def __init__(self, rated_capacity=2000):
        self.rated_capacity = rated_capacity # kW
    def calculate_metrics(self, df):
        # Calculate the metrics
        if len(df) > 1:
            total_runtime = (df["rtc"].iloc[-1] - df["rtc"].iloc[0]).total_seconds() / 3600 # hours
        else:
            total_runtime = 0
        downtime = 0 # hours
        num_failures = 0
        for index, row in df.iterrows():
            if pd.isna(row["energy_output"]):
                downtime += 10 / 60 # Assuming 10 mins to repair
                num_failures += 1
            elif row["energy_output"] == 0:
                downtime += 10 # Assuming 10 hours to repair
                num_failures += 1
        if num_failures > 0:
            mtbf = total_runtime / num_failures
            mttr = downtime / num_failures
        else:
            mtbf = 0
            mttr = 0
         capacity_factor = (df["energy_output"].sum() / (24 * 1000 * 4.32 * self.rated_capacity)) * 100
         if len(df['rtc']) > 0:
            hours_in_period = (max(df['rtc']) - min(df['rtc'])).total_seconds() / 3600
        else:
            hours_in_period = 0
 
        max_wind_speed = df['wind_speed'].max()
        min_wind_speed = df['wind_speed'].min()
        avg_wind_speed = df['wind_speed'].mean()
        max_rpm = df['rpm'].max()
        min_rpm = df['rpm'].min()
        avg_rpm = df['rpm'].mean()
        max_temperature = df['temp'].max()
        min_temperature = df['temp'].min()
        avg_temperature = df['temp'].mean()
        max_pressure = df['pressure'].max()
        min_pressure = df['pressure'].min()
        avg_pressure = df['pressure'].mean()
        max_energy_output = df['energy_output'].max()
        actual_energy_output = df['energy_output'].sum()
        if len(df) > 0:
            df_new = pd.DataFrame({
                'capacity_factor': [capacity_factor],
                'mtbf': [mtbf],
                'mttr': [mttr],
                'downtime': [downtime],
                'max_wind_speed': [max_wind_speed],
                'min_wind_speed': [min_wind_speed],
                'avg_wind_speed': [avg_wind_speed],
                'max_rpm': [max_rpm],
                'min_rpm': [min_rpm],
                'avg_rpm': [avg_rpm],
                'max_temperature': [max_temperature],
                'min_temperature': [min_temperature],
                'avg_temperature': [avg_temperature],
                'max_pressure': [max_pressure],
                'min_pressure': [min_pressure],
                'avg_pressure': [avg_pressure],
                'max_energy_output': [max_energy_output],
                'actual_energy_output': [actual_energy_output],
                'hours_in_period': [hours_in_period]
            })
        else:
            df_new = pd.DataFrame()
        return df_new
