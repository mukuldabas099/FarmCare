"""
backend/utils/logger.py
CSV data logging for sensor readings.
"""
import os, csv, datetime, threading

LOG_HEADERS = ["timestamp", "temperature", "moisture", "ec", "ph",
               "nitrogen", "phosphorus", "potassium", "health_score", "source"]

_LOG_FILE = None
_log_lock = threading.Lock()


def init_log(base_dir: str):
    global _LOG_FILE
    _LOG_FILE = os.path.join(base_dir, "data", "soil_data_log.csv")
    os.makedirs(os.path.dirname(_LOG_FILE), exist_ok=True)
    if not os.path.exists(_LOG_FILE):
        with open(_LOG_FILE, "w", newline="") as f:
            csv.writer(f).writerow(LOG_HEADERS)
        print(f"[Log] Created: {_LOG_FILE}")
    else:
        size = os.path.getsize(_LOG_FILE)
        with open(_LOG_FILE, "r") as f:
            rows = sum(1 for _ in f) - 1
        print(f"[Log] Existing log: {rows} rows ({size/1024:.1f} KB)")


def log_reading(data: dict, source: str = "sensor"):
    from backend.utils.scoring import health_score
    if _LOG_FILE is None:
        return
    try:
        row = [
            data.get("timestamp", datetime.datetime.now().isoformat()),
            data.get("temperature"), data.get("moisture"), data.get("ec"),
            data.get("ph"), data.get("nitrogen"), data.get("phosphorus"),
            data.get("potassium"), health_score(data), source
        ]
        with _log_lock:
            with open(_LOG_FILE, "a", newline="") as f:
                csv.writer(f).writerow(row)
    except Exception as e:
        print(f"[Log] Write error: {e}")


def get_log_file():
    return _LOG_FILE


def get_log_lock():
    return _log_lock
