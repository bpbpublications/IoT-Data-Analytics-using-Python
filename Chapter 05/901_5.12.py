from kafka import KafkaProducer
import paho.mqtt.client as mqtt
import json

# Define constants
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "wind-turbine-data"
KAFKA_BROKER_HOST = "localhost"
KAFKA_BROKER_PORT = 9092
KAFKA_TOPIC = "wind-turbine-data"

# Create a Kafka producer configuration
producer_config = {
    "bootstrap_servers": f"{KAFKA_BROKER_HOST}:{KAFKA_BROKER_PORT}",
    "value_serializer": lambda x: json.dumps(x).encode('utf-8')
}

# Create a Kafka producer instance
producer = KafkaProducer(**producer_config)

# Define the MQTT client callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    # Subscribe to the MQTT topic
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    # Parse the JSON message
    json_data = json.loads(msg.payload.decode())
    # Print the received message
    print(f"Received message: {json_data}")
    # Send the message to Kafka topic
    producer.send(KAFKA_TOPIC, json_data)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Disconnected from MQTT broker with result code {rc}")

# Create a MQTT client instance
client = mqtt.Client()
# Set the MQTT client callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the MQTT broker
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

# Start the MQTT loop
client.loop_forever()
