"""
backend/utils/weather.py
OpenWeather API integration — current weather + 10-day forecast.
"""
import threading, time, datetime
import requests as http_requests

WEATHER_API_KEY         = "4939cd6273d783a378ba9c28a3f4ccdb"
WEATHER_UPDATE_INTERVAL = 600  # seconds

weather_cache = {
    "temperature": None, "feels_like": None, "humidity": None,
    "description": None, "rain_expected": False, "rain_mm": 0.0,
    "wind_speed": None, "heat_wave": False, "advice": None,
    "city": None, "last_updated": None, "lat": None, "lon": None,
    "forecast": [],
}
weather_lock = threading.Lock()


def generate_weather_advice(w: dict, sensor: dict) -> str:
    moisture  = sensor.get("moisture", 50)
    if moisture in (None, -1): moisture = 50
    rain_mm   = w.get("rain_mm", 0.0)
    heat_wave = w.get("heat_wave", False)
    desc      = (w.get("description") or "").lower()
    if rain_mm >= 10:
        return f"🌧 Heavy rain expected ({rain_mm}mm) — skip irrigation today."
    if w.get("rain_expected") and rain_mm >= 2:
        return f"🌦 Rain expected ({rain_mm}mm) — hold irrigation for now."
    if heat_wave and moisture < 35:
        return "🔥 Heat wave + dry soil — irrigate immediately and add mulch."
    if heat_wave and moisture >= 35:
        return "🌡 Heat wave — increase irrigation frequency, monitor moisture closely."
    if "rain" in desc or "drizzle" in desc:
        return "🌧 Currently raining — pause irrigation. Re-check in 2 hours."
    if moisture < 25:
        return "💧 Soil moisture critically low — irrigate now."
    if 40 <= moisture <= 65:
        return "✅ Soil moisture optimal. No irrigation needed right now."
    return "📊 Monitor soil moisture. Irrigate if moisture drops below 30%."


def fetch_weather(lat: float, lon: float):
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return
    try:
        curr = http_requests.get(
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric", timeout=5).json()
        fore = http_requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&cnt=40", timeout=5).json()

        rain_mm, rain_expected = 0.0, False
        daily = {}
        for item in fore.get("list", []):
            day = item["dt_txt"].split(" ")[0]
            if day not in daily:
                daily[day] = {"temps": [], "rain": 0.0, "descs": []}
            daily[day]["temps"].append(item["main"]["temp"])
            daily[day]["rain"] += item.get("rain", {}).get("3h", 0.0)
            daily[day]["descs"].append(item["weather"][0]["description"])
            rain_mm += item.get("rain", {}).get("3h", 0.0)
        if rain_mm > 1.0:
            rain_expected = True

        forecast_list = []
        for day, v in sorted(daily.items())[:10]:
            forecast_list.append({
                "date":        day,
                "temp_min":    round(min(v["temps"]), 1),
                "temp_max":    round(max(v["temps"]), 1),
                "rain_mm":     round(v["rain"], 1),
                "description": max(set(v["descs"]), key=v["descs"].count).title(),
            })

        temp      = curr["main"]["temp"]
        heat_wave = temp >= 38.0

        from backend.utils.sensor_state import latest, lock
        with lock:
            sensor_snap = dict(latest)

        with weather_lock:
            weather_cache.update({
                "temperature":   round(temp, 1),
                "feels_like":    round(curr["main"]["feels_like"], 1),
                "humidity":      curr["main"]["humidity"],
                "description":   curr["weather"][0]["description"].title(),
                "rain_expected": rain_expected,
                "rain_mm":       round(rain_mm, 1),
                "wind_speed":    round(curr["wind"]["speed"] * 3.6, 1),
                "heat_wave":     heat_wave,
                "city":          curr.get("name", ""),
                "last_updated":  datetime.datetime.now().strftime("%H:%M"),
                "lat": lat, "lon": lon,
                "forecast": forecast_list,
            })
            weather_cache["advice"] = generate_weather_advice(weather_cache, sensor_snap)
        print(f"[Weather] {weather_cache['city']} | {weather_cache['temperature']}°C | "
              f"{weather_cache['description']}")
    except Exception as e:
        print(f"[Weather] Fetch error: {e}")


def weather_thread_fn():
    time.sleep(5)
    while True:
        with weather_lock:
            lat = weather_cache.get("lat")
            lon = weather_cache.get("lon")
        if lat is None:
            lat, lon = 28.6139, 77.2090
            with weather_lock:
                weather_cache["lat"] = lat
                weather_cache["lon"] = lon
        fetch_weather(lat, lon)
        time.sleep(WEATHER_UPDATE_INTERVAL)
