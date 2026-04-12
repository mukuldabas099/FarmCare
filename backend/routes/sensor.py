"""
backend/routes/sensor.py
Routes: /sensor_data, /mqtt_status, /health
"""
from flask import Blueprint, jsonify
from backend.utils.sensor_state import latest, lock, SK
from backend.utils.scoring      import health_score
from backend.utils.mqtt_handler import mqtt_connected, MQTT_BROKER, MQTT_TOPIC

sensor_bp = Blueprint("sensor", __name__)


@sensor_bp.route("/sensor_data", methods=["GET"])
def sensor_data_ep():
    with lock:
        d = dict(latest)
    for k in SK:
        if d[k] is None:
            d[k] = -1
    d["health_score"] = health_score(d)
    return jsonify(d)


@sensor_bp.route("/mqtt_status", methods=["GET"])
def mqtt_status_ep():
    with lock:
        rc = latest.get("read_count", 0)
    return jsonify({
        "mqtt_connected":   mqtt_connected,
        "broker":           MQTT_BROKER,
        "topic":            MQTT_TOPIC,
        "readings_received": rc,
    })


@sensor_bp.route("/health", methods=["GET"])
def health_ep():
    from backend.utils.model_loader import M
    with lock:
        reads = latest["read_count"]
    return jsonify({
        "status":            "ok",
        "soil_model_loaded": "soil_model" in M,
        "fert_model_loaded": "fert_model" in M,
        "reads":             reads,
    })
