import os
import time
import random
import json
from datetime import datetime, timezone
from paho.mqtt import client as mqtt_client

BROKER_HOST = os.getenv("MQTT_HOST", "climit-mosquitto")
BROKER_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "sensoruser")
MQTT_PASS = os.getenv("MQTT_PASS", "Sensor!2026")
TOPIC = os.getenv("MQTT_TOPIC", "climit/site1/sensor1/temperature")

SENSOR_ID = int(os.getenv("SENSOR_ID", "1"))
BASE_TEMP = float(os.getenv("BASE_TEMP", "23.0"))


def connect_mqtt():
    client_id = f"simulator-{random.randint(0, 10000)}"

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect
    client.connect(BROKER_HOST, BROKER_PORT)
    return client


def generate_temperature(prev_value: float | None) -> float:
    if prev_value is None:
        prev_value = BASE_TEMP
    # petite variation random
    return round(prev_value + random.uniform(-0.3, 0.3), 2)


def run():
    client = connect_mqtt()
    client.loop_start()

    value = None

    try:
        while True:
            value = generate_temperature(value)
            timestamp = int(datetime.now(tz=timezone.utc).timestamp())

            payload = {
                "sensor_id": SENSOR_ID,
                "value": value,
                "unit": "C",
                "timestamp": timestamp,
            }

            msg_str = json.dumps(payload)
            result = client.publish(TOPIC, msg_str, qos=0, retain=False)
            status = result[0]
            if status == 0:
                print(f"Sent {msg_str} to {TOPIC}")
            else:
                print(f"Failed to send message: {status}")

            time.sleep(5)  # toutes les 5 secondes
    except KeyboardInterrupt:
        print("Stopping simulator")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run()
