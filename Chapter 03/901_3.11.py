# Generate a simple IoT sensor data
floor_humidity = 40
machine_temperature = 30.5
valve_pressure = 100.5
# Creating a dictionary to store the IoT sensor data
machine_data = {
    "floor_humidity": floor_humidity,
    "machine_temperature": machine_temperature,
    "valve_pressure": valve_pressure
}
# Print the contents of the dictionary
print(machine_data)
# Access a specific value from the dictionary
print("Machine Temperature:", machine_data["machine_temperature"])
# Add a new key-value pair to the dictionary
machine_data["vibration"] = 0.5
print(machine_data)
# Update a value in the dictionary
machine_data["machine_temperature"] = 25.5
print(machine_data)
# Delete a key-value pair from the dictionary using del command
del machine_data["valve_pressure"]
print(machine_data)
