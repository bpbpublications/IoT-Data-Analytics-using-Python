import numpy as np
# Define a sample sensor data array with vibration and temperature readings
sensor_data = np.array([[10, 23], [11, 24], [12, 26], [13, 25], [14, 28]])
# Define a failure threshold for the vibration readings
vibration_threshold = 12
# Create a new array indicating whether each reading is normal or indicates a failure
failures = np.where(sensor_data[:,0] > vibration_threshold, 1, 0)
# Print a message for potential failure of machine 
print('Machine may breakdown as the vibration level crossed the threshold:', failures)
