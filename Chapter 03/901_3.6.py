# Define sensor data on humidity level of the environment
humidityLevel = 30.0
# Check the humidity level using conditional statements and prompt message accordingly
if humidityLevel > 70.0:
    print("Humidity level of the environment is too high, turn on your dehumidifier.")
elif humidityLevel < 40.0:
    print("Humidity level of the environment is too low, turn on your humidifier.")
else:
    print("Humidity of the environment is within normal level.")
