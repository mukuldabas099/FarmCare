"""
backend/routes/crop_disease.py
Route: /predict_crop_disease  — image → crop disease + cure solution
Uses the crop_disease.h5 model (PlantVillage 38-class classifier).
"""
import io, traceback
import numpy as np
from flask import Blueprint, request, jsonify
from PIL import Image

from backend.utils.disease_data import get_disease_info
from backend.utils.model_loader import M

crop_disease_bp = Blueprint("crop_disease", __name__)

# PlantVillage 38-class label list (standard order)
DISEASE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]


def _colour_fallback_disease(img_bytes: bytes) -> dict:
    """Simple colour-based fallback when model is not loaded."""
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((128, 128))
        arr = np.array(img, dtype=np.float32)
        r, g, b = arr[:, :, 0].mean(), arr[:, :, 1].mean(), arr[:, :, 2].mean()
        # Very rough heuristic
        if g > r and g > b:
            label = "Tomato___healthy"
        elif r > 130 and g < 100:
            label = "Tomato___Late_blight"
        elif r > g and b < 100:
            label = "Tomato___Early_blight"
        else:
            label = "Tomato___healthy"
        info = get_disease_info(label)
        return {
            "class_label": label,
            "confidence": 45.0,
            "is_healthy": info["disease"] is None,
            "crop": info["crop"],
            "disease": info["disease"],
            "emoji": info["emoji"],
            "severity": info["severity"],
            "cause": info["cause"],
            "symptoms": info["symptoms"],
            "solution": info["solution"],
            "prevention": info["prevention"],
            "model": "colour_fallback",
            "top5": [{"label": label, "confidence": 45.0}],
        }
    except Exception as e:
        info = get_disease_info("Tomato___healthy")
        return {
            "class_label": "Tomato___healthy",
            "confidence": 0,
            "is_healthy": True,
            "crop": "Tomato", "disease": None,
            "emoji": "🍅", "severity": "None",
            "cause": "", "symptoms": "Analysis failed",
            "solution": [], "prevention": "",
            "model": "error", "error": str(e), "top5": [],
        }


def predict_disease_from_image(img_bytes: bytes) -> dict:
    """Run crop disease prediction on uploaded image bytes."""
    try:
        # Auto-detect the model's expected input size — works for any trained model
        if "disease_model" in M:
            model_input = M["disease_model"].input_shape  # e.g. (None, 128, 128, 3)
            h, w = model_input[1], model_input[2]
        else:
            h, w = 224, 224  # fallback default

        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((w, h))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)

        if "disease_model" in M:
            proba = M["disease_model"].predict(arr, verbose=0)[0]
            # Use loaded class map if available, else use our DISEASE_CLASSES list
            class_map = M.get("disease_class_map", {str(i): c for i, c in enumerate(DISEASE_CLASSES)})

            top_idx   = int(np.argmax(proba))
            top_label = class_map.get(str(top_idx), DISEASE_CLASSES[top_idx] if top_idx < len(DISEASE_CLASSES) else "Unknown")
            confidence = round(float(proba[top_idx]) * 100, 1)

            # Top-5 predictions
            sorted_indices = np.argsort(proba)[::-1][:5]
            top5 = [
                {
                    "label": class_map.get(str(i), DISEASE_CLASSES[i] if i < len(DISEASE_CLASSES) else str(i)),
                    "confidence": round(float(proba[i]) * 100, 1),
                }
                for i in sorted_indices
            ]

            info = get_disease_info(top_label)
            return {
                "class_label": top_label,
                "confidence": confidence,
                "is_healthy": info["disease"] is None,
                "crop": info["crop"],
                "disease": info["disease"],
                "emoji": info["emoji"],
                "severity": info["severity"],
                "cause": info["cause"],
                "symptoms": info["symptoms"],
                "solution": info["solution"],
                "prevention": info["prevention"],
                "model": "crop_disease.h5",
                "top5": top5,
            }
        else:
            return _colour_fallback_disease(img_bytes)

    except Exception as e:
        print(f"[DiseaseML] Error: {e}")
        traceback.print_exc()
        return _colour_fallback_disease(img_bytes)


@crop_disease_bp.route("/predict_crop_disease", methods=["POST"])
def predict_crop_disease_ep():
    try:
        if "crop_image" not in request.files:
            return jsonify({"error": "No crop_image file provided"}), 400
        img_bytes = request.files["crop_image"].read()
        result = predict_disease_from_image(img_bytes)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500