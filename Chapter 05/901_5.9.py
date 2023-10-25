import json
import random
import datetime
import time
import paho.mqtt.client as mqtt

# Function to generate simulated data
def generate_data():
    data = {}
    data['header'] = {}
    data['header']['asset_id'] = 'WT001',
    data['header']['serial_number'] = '12345'

    data['data'] = []
    current_time = datetime.datetime.now().replace(microsecond=0).isoformat()
    data_point = {}
    data_point['rtc'] = current_time
    data_point['temp'] = round(random.uniform(20, 30), 2)
    data_point['pressure'] = round(random.uniform(1000, 1100), 2)
    data_point['wind_speed'] = round(random.uniform(5, 15), 2)
    data_point['rpm'] = random.randint(1200, 1800)
    data_point['energy_output'] = random.randint(800, 1200)
    data['data'].append(data_point)
    return json.dumps(data)

# MQTT client setup
client = mqtt.Client()
client.connect("localhost", 1883)  # Connect to Mosquitto MQTT broker

# Main program loop to generate data every 1 second
while True:
    data = generate_data()
    print(data)
    client.publish("wind-turbine-data", data)
    time.sleep(1)
