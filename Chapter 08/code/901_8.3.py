import json
import pandas as pd
from kafka import KafkaConsumer
# Kafka consumer setup
consumer = KafkaConsumer('wind-turbine-data', bootstrap_servers=['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))
# Create an empty Pandas DataFrame
columns = ['rtc', 'temperature_100', 'pressure_100', 'wind_speed_100', 'power_output_100']
df = pd.DataFrame(columns=columns)
# Consume data from Kafka topic
for message in consumer:
    data = message.value
    df = df.append(pd.json_normalize(data['data']), ignore_index=True)
    # Print the latest row of data
    print(df.tail(1))
