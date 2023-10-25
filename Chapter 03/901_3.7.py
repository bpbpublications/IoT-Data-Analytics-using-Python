number_of_data = 25 #No of times we need the loop to run
sensor_data = 0 #Initial value of the data
increment_by = 2 #Increment by adding 2 to the initial value
for i in range(number_of_data):
    sensor_data += increment_by 
    print("Generated sensor data:", sensor_data)
