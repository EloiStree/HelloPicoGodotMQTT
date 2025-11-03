A# pip install paho-mqtt

import os
import time
import threading
import uuid
import binascii
import random
import string

import paho.mqtt.client as mqtt

BROKER = "apint.ddns.net"
PORT = 1884  # Admin port
USERNAME = "admin"
PASSWORD = "..."
LISTEN_TOPIC = "game_input/iid"
PUBLISH_TOPICS = ["game_data/text", "game_data/bytes"]
PUBLISH_INTERVAL = 2  # seconds


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Admin connected to broker")
        client.subscribe(LISTEN_TOPIC, qos=0)
        print(f"Subscribed to {LISTEN_TOPIC}")
    else:
        print(f"Connection failed with rc={rc}")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload
    print(f"[RECEIVED] {topic}: {binascii.hexlify(payload).decode()}")
    


def on_disconnect(client, userdata, rc):
    print("Disconnected (rc=%s)" % rc)


def random_text():
    words = ["hello", "world", "admin", "test", "message", "random", "data", "info"]
    return " ".join(random.choices(words, k=random.randint(2, 5)))


def random_bytes():
    size = random.randint(8, 32)
    return os.urandom(size)


def publish_loop(client):
    try:
        while True:
            # Randomly choose topic
            topic = random.choice(PUBLISH_TOPICS)
            
            if topic == "game_data/text":
                payload = random_text()
                client.publish(topic, payload=payload, qos=0, retain=False)
                print(f"Published to {topic}: {payload}")
            else:  # game_data/bytes
                payload = random_bytes()
                client.publish(topic, payload=payload, qos=0, retain=False)
                print(f"Published to {topic}: {binascii.hexlify(payload).decode()}")
            
            time.sleep(PUBLISH_INTERVAL)
    except Exception as e:
        print(f"Publish loop error: {e}")


def main():
    client_id = f"admin-client-{uuid.uuid4().hex[:8]}"
    client = mqtt.Client(client_id=client_id)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    try:
        client.connect(BROKER, PORT, keepalive=60)
    except Exception as e:
        print("Could not connect to broker:", e)
        return

    client.loop_start()
    t = threading.Thread(target=publish_loop, args=(client,), daemon=True)
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping admin client...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
