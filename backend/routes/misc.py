"""
backend/routes/misc.py
Routes: /get_translations, /cloud_status
"""
from flask import Blueprint, jsonify

misc_bp = Blueprint("misc", __name__)

TRANSLATIONS = {
    "en": {
        "app_title": "FarmCare", "app_subtitle": "Intelligent Soil Health Monitor",
        "live_readings": "Live Sensor Readings", "trend_history": "Trend History (last 20 readings)",
        "soil_health": "Soil Health Summary", "health_score": "Health Score",
        "weather_title": "Live Weather & Irrigation Advice",
        "soil_image_title": "Soil Type Detection (AI Model)",
        "upload_soil": "Upload Soil Photo for AI Analysis",
        "crop_recommend": "Recommended Crops for Your Soil",
        "crop_optimize_title": "Crop Optimization", "select_crop": "Select Your Crop",
        "fertilizer_title": "Fertilizer Recommendation",
        "pdf_title": "Generate Soil Health Card (PDF)",
        "farmer_name": "Farmer Name", "email": "Email",
        "address": "Address / Village", "location": "Location (Lat Lng)",
        "khasra": "Khasra Number", "farm_size": "Farm Size (sqft)",
        "generate_pdf": "Generate Soil Health Card",
        "connect": "Connect", "demo_mode": "Demo Mode",
        "optimal": "Optimal", "low": "Low", "high": "High",
        "critical": "Critical", "marginal": "Marginal",
        "excellent": "Excellent — Soil is in perfect condition",
        "good": "Good — Soil needs minor attention",
        "poor": "Poor — Soil health is critical",
        "historical_data": "Historical Data Log",
        "download_csv": "Download CSV", "clear_log": "Clear Log",
        "forecast_title": "10-Day Weather Forecast",
        "suggestions": "Soil Improvement Suggestions",
        "mandi_title": "Mandi Price Intelligence — AGMARKNET",
        "detecting": "Detecting soil type…", "analyzing": "Analyzing…",
        "suitable_crops": "Suitable Crops",
    },
    "hi": {
        "app_title": "फार्मकेयर", "app_subtitle": "बुद्धिमान मृदा स्वास्थ्य मॉनिटर",
        "live_readings": "लाइव सेंसर रीडिंग", "trend_history": "ट्रेंड इतिहास (अंतिम 20 रीडिंग)",
        "soil_health": "मृदा स्वास्थ्य सारांश", "health_score": "स्वास्थ्य स्कोर",
        "weather_title": "लाइव मौसम और सिंचाई सलाह",
        "soil_image_title": "मृदा प्रकार पहचान (AI मॉडल)",
        "upload_soil": "AI विश्लेषण के लिए मिट्टी की फोटो अपलोड करें",
        "crop_recommend": "आपकी मिट्टी के लिए अनुशंसित फसलें",
        "crop_optimize_title": "फसल अनुकूलन", "select_crop": "अपनी फसल चुनें",
        "fertilizer_title": "उर्वरक अनुशंसा",
        "pdf_title": "मृदा स्वास्थ्य कार्ड (PDF) बनाएं",
        "farmer_name": "किसान का नाम", "email": "ईमेल",
        "address": "पता / गाँव", "location": "स्थान (अक्षांश देशांतर)",
        "khasra": "खसरा नंबर", "farm_size": "खेत का आकार (वर्ग फुट)",
        "generate_pdf": "मृदा स्वास्थ्य कार्ड बनाएं",
        "connect": "कनेक्ट करें", "demo_mode": "डेमो मोड",
        "optimal": "अनुकूल", "low": "कम", "high": "अधिक",
        "critical": "गंभीर", "marginal": "सीमांत",
        "excellent": "उत्कृष्ट — मिट्टी बिल्कुल सही है",
        "good": "अच्छा — थोड़ा ध्यान चाहिए", "poor": "खराब — मिट्टी स्वास्थ्य गंभीर",
        "historical_data": "ऐतिहासिक डेटा लॉग",
        "download_csv": "CSV डाउनलोड करें", "clear_log": "लॉग साफ़ करें",
        "forecast_title": "10 दिन का मौसम पूर्वानुमान",
        "suggestions": "मृदा सुधार सुझाव",
        "mandi_title": "मंडी मूल्य इंटेलिजेंस — AGMARKNET",
        "detecting": "मृदा प्रकार पहचाना जा रहा है…", "analyzing": "विश्लेषण हो रहा है…",
        "suitable_crops": "उपयुक्त फसलें",
    }
}


@misc_bp.route("/get_translations", methods=["GET"])
def get_translations():
    return jsonify(TRANSLATIONS)


@misc_bp.route("/cloud_status", methods=["GET"])
def cloud_status():
    try:
        import firebase_admin
        initialized = firebase_admin._apps  # non-empty if initialized
        return jsonify({"firebase": bool(initialized)})
    except Exception:
        return jsonify({"firebase": False})
