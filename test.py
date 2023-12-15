

import paho.mqtt.client as mqtt

SERVER_ADDRESS = "localhost"
SERVER_PORT = 5892

client = mqtt.Client(transport="tcp")
client.tls_set(ca_certs="localhost.crt")
client.connect(SERVER_ADDRESS, SERVER_PORT)
client.loop_forever()

 

import paho.mqtt.client as mqtt

# Define the MQTT Broker IP, port and TLS credentials
SERVER_ADDRESS = "localhost"
SERVER_PORT = 5892

# Define the topic to subscribe
TOPIC = ""

# Connect to the MQTT broker
client = mqtt.Client(transport="tcp")
client.tls_set(ca_certs="localhost.crt")
client.connect(SERVER_ADDRESS, SERVER_PORT)

# Define the callback for the incoming messages
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print("Received message: %s" % message)

client.on_message = on_message

# Subscribe to the topic
client.subscribe(TOPIC)

# Start the infinite loop
client.loop_forever()

 

# Define the MQTT Broker IP, port and TLS credentials
SERVER_ADDRESS = "localhost"
SERVER_PORT = 5892

# Define the topic to publish
TOPIC = "topic1"

# Connect to the MQTT broker
client = mqtt.Client(transport="tcp")
client.tls_set(ca_certs="localhost")
client.connect(SERVER_ADDRESS, SERVER_PORT)

# Publish a message
client.publish(TOPIC, "Hello World!")

# Disconnect from the MQTT broker
client.disconnect()