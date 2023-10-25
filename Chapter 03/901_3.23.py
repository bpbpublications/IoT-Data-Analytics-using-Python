import numpy as np
rand_sensor_data = np.random.rand(1000)
# Filtering the generated sensor data which has readings above 0.5
filtered_sensor_data = rand_sensor_data[rand_sensor_data <= 0.5]
# Let us look at the length of the filtered data along with the originally generated sensor
print("Sensor data before applying any filtering:", len(rand_sensor_data))
print("Sensor data after applying filtering:", len(filtered_sensor_data))
