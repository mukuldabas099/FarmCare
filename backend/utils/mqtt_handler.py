"""
backend/utils/mqtt_handler.py
MQTT subscriber that receives sensor data from ESP32.
Demo thread generates fake data when ESP32 is offline.
"""
import json, time, datetime, random, threading
import paho.mqtt.client as mqtt_client

from backend.utils.sensor_state import latest, lock, SK
from backend.utils.logger       import log_reading

MQTT_BROKER    = "localhost"
MQTT_PORT      = 1883
MQTT_TOPIC     = "farmcare/sensors"
MQTT_CLIENT_ID = "farmcare_pi_subscriber"

mqtt_connected = False


def on_mqtt_connect(client, userdata, flags, rc):
    global mqtt_connected
    if rc == 0:
        mqtt_connected = True
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Connected. Subscribed to '{MQTT_TOPIC}'")
    else:
        mqtt_connected = False
        print(f"[MQTT] Connection failed, rc={rc}. Retrying...")


def on_mqtt_message(client, userdata, msg):
    global latest
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        if not any(k in payload for k in SK):
            return
        payload["timestamp"] = datetime.datetime.now().isoformat()
        payload.setdefault("read_count", 0)
        payload.setdefault("error_count", 0)
        payload.setdefault("raw_line", msg.payload.decode())
        with lock:
            latest.update(payload)
            latest["read_count"] = latest.get("read_count", 0) + 1
        log_reading(latest, "mqtt")

        # Push to Firebase if available
        try:
            from firebase_admin import db as firebase_db
            from backend.utils.scoring import health_score
            firebase_db.reference("farmcare/latest").set(
                {k: latest.get(k) for k in SK + ["timestamp"]}
                | {"health_score": health_score(latest)})
        except Exception:
            pass
    except Exception as e:
        print(f"[MQTT] Parse error: {e}")


def on_mqtt_disconnect(client, userdata, rc):
    global mqtt_connected
    mqtt_connected = False
    print(f"[MQTT] Disconnected (rc={rc}). Will auto-reconnect.")


def mqtt_thread_fn():
    client = mqtt_client.Client(
        client_id=MQTT_CLIENT_ID,
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION1
    )
    client.on_connect    = on_mqtt_connect
    client.on_message    = on_mqtt_message
    client.on_disconnect = on_mqtt_disconnect
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            client.loop_forever()
        except Exception as e:
            print(f"[MQTT] Cannot reach broker: {e}. Retrying in 5s...")
            time.sleep(5)


def demo_thread():
    """Generates fake sensor data when ESP32 is offline."""
    base = dict(temperature=24.5, moisture=45.0, ec=350,
                ph=6.50, nitrogen=80, phosphorus=50, potassium=120)
    count = 0
    while True:
        time.sleep(3)
        count += 1
        with lock:
            if latest.get("read_count", 0) > 0:
                continue  # real data is flowing
        d = {k: round(v + random.uniform(-3, 3), 2) for k, v in base.items()}
        d.update(
            ph=round(max(4.5, min(9.0, d["ph"])), 2),
            moisture=round(max(0, min(100, d["moisture"])), 1),
            temperature=round(max(10, min(50, d["temperature"])), 1),
            timestamp=datetime.datetime.now().isoformat(),
            raw_line="demo", read_count=count, error_count=0
        )
        with lock:
            latest.update(d)
        log_reading(latest, "demo")
