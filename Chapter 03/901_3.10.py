# Simple program to learn how to handle list using IoT sensor data
# Define some IoT sensor data as lists
machine_vibration = [0.1, 0.2, 0.3,0.4,0.5]
machine_pressure = [150, 155, 160, 165, 170]
# Print the data
print("Machine Vibration:", machine_vibration)
print("Machine Pressure:", machine_pressure)
# Accessing specific elements of a list using index value
print("Reading first element of Machine Vibration:", machine_vibration[0])
print("Reading first element of Machine Pressure:", machine_pressure[0])
# Modifying specific element of a list using index value
machine_vibration[0] = 0.150
machine_pressure[0] = 152.5
print("Modified Machine Vibration:", machine_vibration)
print("Modified Machine Pressure:", machine_pressure)
# Adding an element to a list using append function
machine_vibration.append(0.6)
machine_pressure.append(180)
print("New Machine Vibration:", machine_vibration)
print("New Machine Pressure:", machine_pressure)
# Removing an element from a list using pop function
machine_vibration.pop(0)
machine_pressure.pop(0)
print("After removing first element from Machine Vibration:", machine_vibration)
print("After removing first element from Machine Pressure:", machine_pressure)
