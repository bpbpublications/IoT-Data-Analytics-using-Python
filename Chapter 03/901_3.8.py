number_of_data = 25
sensor_data = 1
# Generate IoT simulation data for multiple sensors with
for id in range(number_of_data):
    for val in range(number_of_data):
        sensor_id = "sensor_" + str(id) # Assign sensor ID
        sensor_val = sensor_data + val #generate sensor value
        # Print the generated sensor id and values
        print(f"Sensor {sensor_id}: Sensor Value = {sensor_val} ")
