def calculate_average_temperature(sensor_data):
    """
    This user-defined function returns the average temperature from a given list of sensor data.
    """
    total = 0
    count = 0
    for temperature in sensor_data:
        total += temperature # add temperature to the total
        count += 1 
    return total / count # return the average temperature to the calling program
#call the user-defined function to get average temperature
temperature_list = [20.5, 30.0, 25.0, 21.0, 25.0, 28.0, 30.5]
average_temp = calculate_average_temperature(temperature_list) #calling the user-defined function
print(f"Average temperature: {average_temp:.1f}°C")
