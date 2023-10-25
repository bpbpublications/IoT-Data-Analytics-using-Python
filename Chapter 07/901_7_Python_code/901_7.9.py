import pandas as pd
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import psycopg2

#Connect to datalake
conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )

cur = conn.cursor()
#Query curated zone of the data lake for the wind turbine table and create a dataframe 
cur.execute("SELECT * FROM curatedzone.c_external_wind_turbine_data")
wind_turbine_data= pd.DataFrame(cur.fetchall(), columns=['id','rtc','year', 'month', 'day', 'hour', 'minute', 'temperature_100', 'temperature_120', 'temperature_80', 'wind_direction_100', 'wind_direction_120', 
    	'wind_direction_80', 'wind_speed_100','wind_speed_120','wind_speed_80','pressure_200','pressure_100','pressure_0','power_output_80','power_output_100',
    	'power_output_120'])

# Convert the timestamp column to datetime
wind_turbine_data['rtc'] = pd.to_datetime(wind_turbine_data['rtc'])

# Select the relevant columns
wind_turbine_df = wind_turbine_data[['id', 'rtc', 'wind_speed_100', 'power_output_100']].head(10000)

# Set the index to the timestamp column
wind_turbine_df.set_index('rtc', inplace=True)

# Extract features using the "exhaustive" settings for feature calculation
extracted_features = extract_features(wind_turbine_df, column_id='id')

# Impute missing values
imputed_features = impute(extracted_features)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(imputed_features, wind_turbine_df['power_output_100'], test_size=0.2, random_state=42)

# Train a random forest regressor
rf = RandomForestRegressor()
rf.fit(X_train, y_train)

# Evaluate the model on the testing set
score = rf.score(X_test, y_test)
print('R^2 score:', score)

# Predict on the testing set
y_pred = rf.predict(X_test)

# Plot actual vs predicted values
plt.figure(figsize=(10, 5))
plt.plot(y_test, y_pred, 'o', label='Actual vs Predicted')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', label='Ideal')
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted Power Output')
plt.legend()
plt.show()

