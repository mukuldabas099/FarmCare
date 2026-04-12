"""
backend/routes/weather.py
Routes: /weather, /forecast, /set_location
"""
import threading
from flask import Blueprint, request, jsonify
from backend.utils.weather import weather_cache, weather_lock, fetch_weather

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather", methods=["GET"])
def weather_ep():
    with weather_lock:
        return jsonify(dict(weather_cache))


@weather_bp.route("/forecast", methods=["GET"])
def forecast_ep():
    with weather_lock:
        return jsonify({"forecast": weather_cache.get("forecast", [])})


@weather_bp.route("/set_location", methods=["POST"])
def set_location():
    data = request.json or {}
    lat  = data.get("lat")
    lon  = data.get("lon")
    if lat is None or lon is None:
        return jsonify({"error": "lat and lon required"}), 400
    with weather_lock:
        weather_cache["lat"] = float(lat)
        weather_cache["lon"] = float(lon)
    threading.Thread(target=fetch_weather, args=(float(lat), float(lon)), daemon=True).start()
    return jsonify({"status": "ok", "lat": lat, "lon": lon})
