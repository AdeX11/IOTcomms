import paho.mqtt.client as mqtt
# Define the MQTT Broker IP, port and TLS credentials
SERVER_ADDRESS = "localhost"
SERVER_PORT = 1883

# Define the topic to publish
TOPIC = "topic1"

# Connect to the MQTT broker
client = mqtt.Client(transport="tcp")
client.connect(SERVER_ADDRESS, SERVER_PORT)

# Publish a message
client.publish(TOPIC, "Hello World!")

# Disconnect from the MQTT broker
client.disconnect()