import paho.mqtt.client as mqtt
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # Subscribe to the topic
    client.subscribe(TOPIC) 

# Define the callback for the incoming messages
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf8")
    print("Received message: %s" % message)


# Define the MQTT Broker IP, port and TLS credentials
SERVER_ADDRESS = "localhost"
SERVER_PORT = 1883

# Define the topic to subscribe
TOPIC = "topic1"

# Connect to the MQTT broker
client = mqtt.Client(transport="tcp")
client.on_message = on_message
client.on_connect = on_connect
# client.tls_set(ca_certs="localhost.crt")
# client.username_pw_set("username", "password")
client.connect(SERVER_ADDRESS, SERVER_PORT,60)


# Start the infinite loop
client.loop_forever()