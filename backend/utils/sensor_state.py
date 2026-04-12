"""
backend/utils/sensor_state.py
Shared global sensor state used across all modules.
"""
import threading 

SK = ["temperature", "moisture", "ec", "ph", "nitrogen", "phosphorus", "potassium"]

latest = dict(
    temperature=None, moisture=None, ec=None, ph=None,
    nitrogen=None, phosphorus=None, potassium=None,
    timestamp="", raw_line="", read_count=0, error_count=0
)
lock = threading.Lock()
