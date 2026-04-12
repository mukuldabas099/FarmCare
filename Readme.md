# 🌾 FarmCare

**FarmCare** is an AI-powered smart farming platform built with Flask that helps farmers monitor soil health, detect crop diseases, get fertilizer recommendations, and access live market prices — all from a single web dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Live Sensor Dashboard** | Real-time soil metrics (temperature, moisture, pH, EC, N/P/K) via MQTT from ESP32 sensors |
| 🌱 **Soil Type Classifier** | Upload a soil image → ML model identifies soil type (Alluvial, Black, Red, Clay, Yellow) and recommends suitable crops |
| 🦠 **Crop Disease Detection** | Upload a leaf photo → 38-class PlantVillage model diagnoses disease with causes, symptoms, treatment, and prevention tips |
| 💊 **Fertilizer Recommender** | Predicts the best fertilizer based on soil type, crop, and sensor data (NPK ratios, dosage, timing) |
| ⚙️ **Crop Optimizer** | Compares current sensor readings against crop-specific ideal ranges and suggests corrective actions |
| 🌦 **Weather Integration** | Current weather + 10-day forecast via OpenWeatherMap with smart irrigation advice |
| 📈 **Mandi Prices** | Live commodity market prices from India's AGMARKNET (data.gov.in) — price trends, best markets, top crops by state |
| 📄 **Soil Health Card PDF** | Generates a downloadable multi-page PDF report of soil health with Hindi font support |
| 📋 **Data Logger** | Logs all sensor readings to CSV and Firebase Realtime Database |
| 🌐 **Multilingual UI** | Frontend supports English and Hindi (Devanagari fonts bundled) |

---

## 🏗️ Project Structure

```
Farm/
├── app.py                        # Flask entry point — registers all blueprints
├── backend/
│   ├── routes/
│   │   ├── sensor.py             # /sensor — live sensor data endpoint
│   │   ├── soil.py               # /predict_soil_crops — soil image classifier
│   │   ├── crop_disease.py       # /predict_crop_disease — leaf disease detector
│   │   ├── fertilizer.py         # /predict_fertilizer — fertilizer recommender
│   │   ├── optimize.py           # /optimize_crop — crop parameter optimizer
│   │   ├── weather.py            # /weather, /forecast, /set_location
│   │   ├── mandi_routes.py       # /mandi/* — live mandi price APIs
│   │   ├── pdf.py                # /generate_pdf — soil health card generator
│   │   ├── datalog.py            # /datalog — sensor history log
│   │   └── misc.py               # Miscellaneous utility endpoints
│   └── utils/
│       ├── model_loader.py       # Loads all ML models at startup
│       ├── mqtt_handler.py       # MQTT subscriber + demo data generator
│       ├── weather.py            # OpenWeatherMap API integration
│       ├── scoring.py            # Sensor thresholds & health score logic
│       ├── sensor_state.py       # Shared in-memory sensor state
│       ├── logger.py             # CSV data logger
│       ├── crop_data.py          # Soil-crop mappings, fertilizer info, crop ideals
│       └── disease_data.py       # Disease info database (38 PlantVillage classes)
├── models/
│   ├── soil_classifier.h5        # TensorFlow model for soil type (224×224 RGB)
│   ├── crop_disease.h5           # TensorFlow model for crop disease (PlantVillage 38-class)
│   ├── fertilizer_model.pkl      # Scikit-learn fertilizer classifier
│   ├── fert_label_encoder.pkl    # Fertilizer label encoder
│   ├── fert_crop_encoder.pkl     # Crop feature encoder
│   └── fert_soil_encoder.pkl     # Soil type encoder
├── config/
│   └── firebase_key.json         # Firebase service account credentials
├── data/
│   ├── FertilizerData.csv        # Training reference data for fertilizers
│   ├── soil_data_log.csv         # Logged sensor readings
│   └── known_labels.json         # Known class labels
├── fonts/
│   ├── NotoSans-Regular.ttf      # UI fonts
│   └── NotoSansDevanagari-*.ttf  # Hindi fonts for PDF generation
├── static/
│   ├── css/                      # main.css, nav.css
│   ├── js/                       # core.js, main.js, lang.js (i18n)
│   └── pages/                    # HTML pages: dashboard, crops, soil, fertilizer, mandi, etc.
├── templates/
│   └── index.html                # Main SPA shell
├── download_hindi_fonts.py       # Script to download Noto Hindi fonts
└── hindi_pdf_patch.py            # Registers Hindi fonts for ReportLab PDF
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A running MQTT broker (e.g., [Mosquitto](https://mosquitto.org/)) on `localhost:1883`
- An ESP32 sensor publishing JSON to the `farmcare/sensors` topic (or use the built-in demo mode)

### Installation

```bash
# 1. Clone or extract the project
cd Farm

# 2. Install Python dependencies
pip install flask flask-cors paho-mqtt firebase-admin tensorflow \
            scikit-learn joblib pillow reportlab requests numpy pandas

# 3. (Optional) Download Hindi fonts for PDF generation
python download_hindi_fonts.py

# 4. Add your API keys (see Configuration below)

# 5. Run the server
python app.py
```

The server starts at **http://0.0.0.0:5000**

---

## ⚙️ Configuration

### API Keys

| Service | File / Env Var | Where to Get |
|---|---|---|
| **OpenWeatherMap** | `backend/utils/weather.py` → `WEATHER_API_KEY` | [openweathermap.org](https://openweathermap.org/api) |
| **data.gov.in (Mandi)** | `backend/routes/mandi_routes.py` → `DATAGOV_API_KEY` or `DATAGOV_API_KEY` env var | [data.gov.in](https://data.gov.in) → My Account → API Keys |
| **Firebase** | `config/firebase_key.json` | Firebase Console → Project Settings → Service Accounts |

### MQTT

By default, FarmCare connects to a local MQTT broker at `localhost:1883` and subscribes to the topic `farmcare/sensors`.

Expected JSON payload from the ESP32:
```json
{
  "temperature": 24.5,
  "moisture": 45.0,
  "ec": 350,
  "ph": 6.5,
  "nitrogen": 80,
  "phosphorus": 50,
  "potassium": 120
}
```

> **Demo Mode:** If no MQTT data is received, FarmCare automatically generates realistic simulated sensor data so the dashboard remains functional.

---

## 🤖 ML Models

| Model | File | Framework | Description |
|---|---|---|---|
| Soil Classifier | `soil_classifier.h5` | TensorFlow/Keras | Classifies soil images into 5 types (224×224 input) |
| Crop Disease Detector | `crop_disease.h5` | TensorFlow/Keras | 38-class PlantVillage leaf disease classifier |
| Fertilizer Recommender | `fertilizer_model.pkl` | Scikit-learn | Predicts top-3 fertilizers from soil/crop/NPK data |

All models are loaded at startup via `backend/utils/model_loader.py`. If a model file is missing, a colour-heuristic fallback is used automatically.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main web UI |
| `GET` | `/sensor` | Latest sensor readings |
| `POST` | `/predict_soil_crops` | Soil type from image (`multipart: soil_image`) |
| `POST` | `/predict_crop_disease` | Disease from leaf image (`multipart: crop_image`) |
| `POST` | `/predict_fertilizer` | Fertilizer recommendation (JSON body) |
| `POST` | `/optimize_crop` | Crop-specific parameter analysis (JSON body) |
| `GET` | `/weather` | Current weather data |
| `GET` | `/forecast` | 10-day weather forecast |
| `POST` | `/set_location` | Update weather location (`{"lat": ..., "lon": ...}`) |
| `GET` | `/mandi/prices` | Mandi prices (`?commodity=Wheat&state=Punjab`) |
| `GET` | `/mandi/best_markets` | Best markets for a commodity |
| `GET` | `/mandi/monthly_trend` | Monthly price trend |
| `GET` | `/mandi/top_crops` | Top traded crops by state |
| `GET` | `/mandi/commodities` | List of available commodities |
| `GET` | `/mandi/states` | List of Indian states |
| `POST` | `/generate_pdf` | Generate soil health card PDF |
| `GET` | `/datalog` | View historical sensor data |

---

## 🔥 Firebase Integration

When `config/firebase_key.json` is present, FarmCare pushes live sensor readings and health scores to Firebase Realtime Database at:

```
farmcare-52fd6-default-rtdb.asia-southeast1.firebasedatabase.app/farmcare/latest
```

---

## 🌍 Multilingual Support

The frontend includes a language switcher (`static/js/lang.js`) supporting English and Hindi. Hindi PDF generation is handled via bundled Noto Devanagari fonts using ReportLab.

---

## 📦 Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **ML:** TensorFlow / Keras, Scikit-learn, joblib
- **IoT:** Paho MQTT (ESP32 integration)
- **Cloud:** Firebase Admin SDK (Realtime Database)
- **Weather:** OpenWeatherMap API
- **Market Data:** data.gov.in AGMARKNET API
- **PDF:** ReportLab
- **Frontend:** Vanilla HTML/CSS/JS (multi-page SPA)

---

## 📄 License

This project is intended for educational and agricultural research purposes.
