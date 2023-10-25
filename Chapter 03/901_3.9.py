# Simulating IoT data for a manufcaturing equipment using while loop
i = 0
while i <= 25:
    # Simulate machine floor humidity, machine temperature and valve pressure from IoT sensors
    floor_humidity = 50 + i * 2
    machine_temperature = 25 + i
    valve_pressure = 150 + i * 10
    #print the results
    print("Floor Humidity: {}%, Temperature: {}°C, Valve Pressure: {}kPa".format(floor_humidity, machine_temperature, valve_pressure))
    i += 1
