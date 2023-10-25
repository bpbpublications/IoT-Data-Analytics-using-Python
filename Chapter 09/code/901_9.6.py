import pandas as pd
import pickle
# Load the model from the file
with open('alert_model.pkl', 'rb') as f:
    model, scaler, thresholds = pickle.load(f)
# Define a function to predict alerts based on the input data
def predict_threshold(df, columns):
    # Standardize the input data
    input_data_scaled = scaler.transform(df[columns])
    # Make predictions using the model
    predictions = model.predict(input_data_scaled)
    # Check if each prediction is above or below threshold
    alerts = []
    for i in range(len(predictions)):
        if predictions[i] == 1:
            alerts.append(f"Row {i}: Above threshold")
        else:
            alerts.append(f"Row {i}: Below threshold")
    return alerts
# Example usage
input_data = pd.DataFrame({'temperature_100': [20],
                           'pressure_100': [1000],
                           'wind_speed_100': [10],
                           'power_output_100': [1500]})
# Select the columns to use for modeling
features = ['temperature_100', 'pressure_100', 'wind_speed_100', 'power_output_100']
alerts = predict_threshold(input_data, features)
for alert in alerts:
    print(alert)
