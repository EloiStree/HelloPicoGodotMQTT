import paho.mqtt.client as mqtt
import json
import threading
import time
import random

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("game_data/text")
        client.subscribe("game_data/bytes")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    
    if topic == "game_data/text":
        try:
            text_data = payload.decode('utf-8')
            print(f"Text data: {text_data}")
        except UnicodeDecodeError:
            print("Failed to decode text message")
    
    elif topic == "game_data/bytes":
        print(f"Bytes data: {payload}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

def send_random_bytes(client):
    while True:
        try:
            # Generate random bytes between 4-16 bytes
            byte_length = random.randint(4, 20)
            random_bytes = bytes([random.randint(0, 255) for _ in range(byte_length)])
            
            # Publish to game_input/iid
            client.publish("game_input/iid", random_bytes)
            print(f"Sent {byte_length} random bytes: {random_bytes.hex()}")
            
            # Wait 1 second before sending next message
            time.sleep(1)
        except Exception as e:
            print(f"Error sending bytes: {e}")
            break

# Create MQTT client
client = mqtt.Client()

# Set client name
client_id = f"python_client_{random.randint(1000, 9999)}"
client._client_id = client_id.encode('utf-8')
print(f"Client ID: {client_id}")
# Set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to broker
try:
    client.connect("apint.ddns.net", 1883, 60)
    
    # Start the background thread for sending random bytes
    sender_thread = threading.Thread(target=send_random_bytes, args=(client,))
    sender_thread.daemon = True
    sender_thread.start()
    
    client.loop_forever()
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
except Exception as e:
    print(f"Error: {e}")
