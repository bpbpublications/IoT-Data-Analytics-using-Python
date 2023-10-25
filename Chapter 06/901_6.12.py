import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Print the plot within the page
%matplotlib inline
# set seaborn theme
sns.set(style="white")
conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
cur = conn.cursor()
cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
data_external = pd.DataFrame(cur.fetchall(), columns=['id','rtc','year', 'month', 'day', 'hour', 'minute', 'temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 
     'wind_direction_80', 'wind_speed_100','wind_speed_120','wind_speed_80','pressure_200','pressure_100','pressure_0','power_output_80','power_output_100',
     'power_output_120'])
def plot_df(new_data, x, y, title="", xlabel='Time', ylabel='Power Output', dpi=100):
    # Resample the data to a 15-minute interval
    resampled_data = new_data.set_index('rtc').resample('15T').sum().reset_index()
    # Create a datetime index for the resampled data
    resampled_data['datetime'] = pd.to_datetime(resampled_data['rtc'])
    # Plot the resampled data
    plt.figure(figsize=(15,4), dpi=dpi)
    plt.plot(resampled_data['datetime'], resampled_data[y], color='blue')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()
plot_df(data_external, x=data_external['rtc'], y='power_output_100', title='Trend and Seasonality of power output (15-minute interval)')
