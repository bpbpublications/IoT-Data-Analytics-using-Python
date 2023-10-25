import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
# Connect to the database
conn = psycopg2.connect(
        host="localhost",
        database="IoTDataLake",
        user="postgres",
        password=""
    )
# Read the ABT into a Pandas dataframe
df = pd.read_sql_query("SELECT wind_speed_100, power_output_100, wind_direction_100, temperature_100, pressure_100, hour, day_of_week, month, season, wind_speed_range, power_output_range FROM analyticszone.wind_turbine_abt;", conn)

# Convert categorical columns to one-hot encoded dummy variables
df = pd.get_dummies(df, columns=['season', 'wind_speed_range', 'power_output_range'])
# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df.drop(['power_output_100'], axis=1),
    df['power_output_100'],
    test_size=0.2,
    random_state=42
)
# Train a linear regression model on the training set
Linearmodel = LinearRegression()
Linearmodel.fit(X_train, y_train)
# Predict power output for the training and test sets
y_train_prediction = Linearmodel.predict(X_train)
y_test_prediction = Linearmodel.predict(X_test)
# Plot the predicted values for the training and test sets
fig, ax = plt.subplots()
ax.scatter(y_train_pred, y_train, alpha=0.5, label='Predicted on Training Set')
ax.scatter(y_test_pred, y_test, alpha=0.5, label='Predicted on Test Set')
ax.set_xlabel('Predicted Power Output')
ax.set_ylabel('Actual Power Output')
ax.legend()
plt.show()
# Test the model on the test set and print the results
print(f"R^2 Score on Training: {model.score(X_train, y_train):.4f}")
print(f"R^2 Score on Test: {model.score(X_test, y_test):.4f}")
# Close the database connection
conn.close()