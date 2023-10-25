import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="IoTDataLake",
    user="postgres",
    password=""
)

# Query the analyticszone.a_predicted_power_output table and create a DataFrame
cur = conn.cursor()
cur.execute("SELECT rtc, actual, predicted FROM analyticszone.a_predicted_power_output")
results = cur.fetchall()

# Unpack the results into separate lists
timestamps = [r[0] for r in results]
actual_values = [r[1] for r in results]
predicted_values = [r[2] for r in results]

# Create a time series line plot
fig, ax1 = plt.subplots(figsize=(10, 5))


# Add scatter plot of actual vs predicted values
ax1 = ax1.twinx()
ax1.scatter(actual_values, predicted_values, color='red', label='Actual vs Predicted')
ax1.plot([min(actual_values), max(actual_values)], [min(actual_values), max(actual_values)], 'k--', label='Ideal')
ax1.set_ylabel('Predicted')
ax1.legend()

plt.show()