"""
FarmCare – Main Flask Application Entry Point (v4.0 Restructured)
=================================================================
Imports all route blueprints and starts the server.
"""

import os, json, threading, time, datetime, traceback
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

from flask import Flask, send_file, jsonify
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ── Load models (shared state) ────────────────────────────────
from backend.utils.model_loader import load_all_models, M
from backend.utils.sensor_state import latest, lock, SK
from backend.utils.logger       import init_log
from backend.utils.weather      import weather_thread_fn

load_all_models(BASE_DIR)
init_log(BASE_DIR)

# ── Register route blueprints ─────────────────────────────────
from backend.routes.sensor       import sensor_bp
from backend.routes.weather      import weather_bp
from backend.routes.soil         import soil_bp
from backend.routes.fertilizer   import fertilizer_bp
from backend.routes.optimize     import optimize_bp
from backend.routes.pdf          import pdf_bp
from backend.routes.datalog      import datalog_bp
from backend.routes.misc         import misc_bp
from backend.routes.crop_disease import crop_disease_bp

for bp in [sensor_bp, weather_bp, soil_bp, fertilizer_bp,
           optimize_bp, pdf_bp, datalog_bp, misc_bp, crop_disease_bp]:
    app.register_blueprint(bp)

# ── Try mandi routes ──────────────────────────────────────────
try:
    from backend.routes.mandi_routes import register_mandi_routes
    register_mandi_routes(app)
    _MANDI_OK = True
except ImportError:
    _MANDI_OK = False
    print("[Mandi] mandi_routes.py not found — mandi endpoints disabled")

# ── Firebase ──────────────────────────────────────────────────
import firebase_admin
from firebase_admin import credentials
FIREBASE_KEY = os.path.join(BASE_DIR, "config", "firebase_key.json")
FIREBASE_URL = "https://farmcare-52fd6-default-rtdb.asia-southeast1.firebasedatabase.app/"
firebase_initialized = False
if os.path.exists(FIREBASE_KEY):
    try:
        cred = credentials.Certificate(FIREBASE_KEY)
        firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_URL})
        firebase_initialized = True
        print("[Firebase] Connected ✓")
    except Exception as _fe:
        print(f"[Firebase] Failed: {_fe}")
else:
    print("[Firebase] config/firebase_key.json not found — cloud push disabled")

# ── MQTT subscriber ───────────────────────────────────────────
from backend.utils.mqtt_handler import mqtt_thread_fn, demo_thread
threading.Thread(target=mqtt_thread_fn, daemon=True).start()
threading.Thread(target=demo_thread,    daemon=True).start()

# ── Weather background thread ─────────────────────────────────
threading.Thread(target=weather_thread_fn, daemon=True).start()

# ── Serve main HTML ───────────────────────────────────────────
@app.route("/")
def index():
    return send_file(os.path.join(BASE_DIR, "templates", "index.html"))

@app.route("/<path:filename>")
def static_files(filename):
    filepath = os.path.join(BASE_DIR, "static", filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    # fallback: check root (legacy)
    root_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(root_path):
        return send_file(root_path)
    return "", 204


if __name__ == "__main__":
    print("=" * 62)
    print("  FarmCare  –  Soil Health Backend  (v4.0 Restructured)")
    print(f"  Soil Model : {'LOADED ✓' if 'soil_model' in M else 'MISSING — place soil_classifier.h5 in models/'}")
    print(f"  Fert Model : {'LOADED ✓' if 'fert_model' in M else 'MISSING — check models/*.pkl files'}")
    print(f"  Crop Dis.  : {'LOADED ✓' if 'disease_model' in M else 'MISSING — place crop_disease.h5 in models/'}")
    print(f"  Mandi API  : {'ENABLED ✓' if _MANDI_OK else 'DISABLED — backend/routes/mandi_routes.py missing'}")
    print(f"  Firebase   : {'ENABLED ✓' if firebase_initialized else 'DISABLED — config/firebase_key.json missing'}")
    print("  URL        : http://0.0.0.0:5000")
    print("=" * 62)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
