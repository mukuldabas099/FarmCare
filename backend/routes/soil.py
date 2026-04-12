"""
backend/routes/soil.py
Route: /predict_soil_crops  — image → soil type + crop recommendations
"""
import io, traceback
import numpy as np
from flask import Blueprint, request, jsonify
from PIL import Image

from backend.utils.crop_data  import SOIL_CROP_MAP
from backend.utils.model_loader import M

soil_bp = Blueprint("soil", __name__)


def _normalize_soil_label(label: str) -> str:
    """Map classifier label → SOIL_CROP_MAP key."""
    label = label.strip()
    if label in SOIL_CROP_MAP:
        return label
    lower = label.lower()
    mapping = {
        "alluvial": "Alluvial", "black": "Black",
        "clay": "Clay",         "clayey": "Clay",
        "red": "Red",           "yellow": "Yellow",
    }
    for prefix, canonical in mapping.items():
        if lower.startswith(prefix):
            return canonical
    return label


def get_soil_notes(soil_type: str) -> str:
    notes = {
        "Alluvial": "Fertile, fine-textured soil found near river plains. Excellent for most crops.",
        "Black":    "Clay-rich, high mineral content. Ideal for cotton and soybean.",
        "Red":      "Iron-oxide rich, often acidic and low in N/P. Apply lime and organic matter.",
        "Yellow":   "Slightly acidic, moderate fertility. Suitable for maize and groundnut.",
        "Clay":     "High clay content, excellent water retention. Best for rice.",
    }
    return notes.get(_normalize_soil_label(soil_type), "Soil analysis complete.")


def _colour_fallback(img_bytes: bytes) -> dict:
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((128, 128))
        arr = np.array(img, dtype=np.float32)
        r, g, b     = arr[:, :, 0].mean(), arr[:, :, 1].mean(), arr[:, :, 2].mean()
        brightness  = (r + g + b) / 3
        if r > 120 and g < 90:               label = "Red"
        elif brightness > 160:               label = "Alluvial"
        elif r < 75 and g < 75 and b < 75:   label = "Black"
        else:                                label = "Clay"
        crops = SOIL_CROP_MAP.get(label, [])
        return {"soil_type": label, "confidence": 60.0, "crops": crops,
                "notes": get_soil_notes(label),
                "model": "colour_fallback (model not loaded)",
                "all_classes": [{"label": label, "prob": 60.0}]}
    except Exception as e:
        return {"soil_type": "Alluvial", "confidence": 0, "crops": SOIL_CROP_MAP["Alluvial"],
                "notes": "Analysis failed", "model": "error", "error": str(e), "all_classes": []}


def predict_soil_from_image(img_bytes: bytes) -> dict:
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((224, 224))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)

        if "soil_model" in M:
            proba     = M["soil_model"].predict(arr, verbose=0)[0]
            class_map = M["soil_class_map"]
            top_idx   = int(np.argmax(proba))
            raw_label = class_map.get(str(top_idx), list(class_map.values())[top_idx])
            top_label = _normalize_soil_label(raw_label)
            confidence = round(float(proba[top_idx]) * 100, 1)

            all_probs = sorted([
                {"label":     _normalize_soil_label(class_map.get(str(i), str(i))),
                 "raw_label": class_map.get(str(i), str(i)),
                 "prob":      round(float(p) * 100, 1)}
                for i, p in enumerate(proba)
            ], key=lambda x: x["prob"], reverse=True)

            return {
                "soil_type":   top_label,
                "raw_label":   raw_label,
                "confidence":  confidence,
                "all_classes": all_probs,
                "crops":       SOIL_CROP_MAP.get(top_label, []),
                "notes":       get_soil_notes(top_label),
                "model":       "soil_classifier.h5",
            }
        else:
            return _colour_fallback(img_bytes)
    except Exception as e:
        print(f"[SoilML] Error: {e}")
        return _colour_fallback(img_bytes)


@soil_bp.route("/predict_soil_crops", methods=["POST"])
def predict_soil_crops_ep():
    try:
        if "soil_image" not in request.files:
            return jsonify({"error": "No soil_image file provided"}), 400
        img_bytes = request.files["soil_image"].read()
        return jsonify(predict_soil_from_image(img_bytes))
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500