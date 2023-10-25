#Using numpy to generate 1000 random numbers with values 0 and 1
import numpy as np
rand_sensor_data = np.random.rand(1000)
print(rand_sensor_data[:10]) #print the first 10 numbers from the generated list
#perform some basic statistical analysis on the random data 
mean = np.mean(rand_sensor_data)
std_dev = np.std(rand_sensor_data)
variance = np.var(rand_sensor_data)
print("type is: ", type(rand_sensor_data))
# Print the result of statistical analsysis
print("Statistical Mean of the random sensor data:", mean)
print("Standard deviation of the random sensor data:", std_dev)
print("Variance in the random sensor data:", variance)
