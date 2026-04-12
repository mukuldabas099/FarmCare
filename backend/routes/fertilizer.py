"""
backend/routes/fertilizer.py
Route: /predict_fertilizer
"""
import numpy as np
from flask import Blueprint, request, jsonify
from backend.utils.model_loader import M
from backend.utils.scoring      import safe
from backend.utils.crop_data    import FERT_INFO, normalize_soil_for_fert, map_crop_for_fert

fertilizer_bp = Blueprint("fertilizer", __name__)


def predict_fertilizer(data, soil_type: str, crop_type: str, hum_override=None):
    if "fert_model" not in M:
        return {"error": "fertilizer_model.pkl not found in models/"}

    soil_norm = normalize_soil_for_fert(soil_type)
    crop_norm = map_crop_for_fert(crop_type, M.get("crop_fe"))

    def enc(encoder, val):
        classes = list(encoder.classes_)
        return int(encoder.transform([val])[0]) if val in classes else 0

    soil_enc = enc(M["soil_le"], soil_norm)
    crop_enc = enc(M["crop_fe"], crop_norm)
    tmp  = safe(data.get("temperature"), 28)
    hum  = hum_override or safe(data.get("humidity"), 60)
    moi  = safe(data.get("moisture"),   42)
    n    = safe(data.get("nitrogen"),   80)
    k    = safe(data.get("potassium"), 120)
    p    = safe(data.get("phosphorus"), 50)

    X     = np.array([[tmp, hum, moi, soil_enc, crop_enc, n, k, p]])
    proba = M["fert_model"].predict_proba(X)[0]
    top3  = []
    for idx in np.argsort(proba)[::-1][:3]:
        fn   = M["fert_le"].classes_[idx]
        info = FERT_INFO.get(fn, {"npk": "—", "desc": "Standard fertilizer.",
                                   "rate": "As per test", "when": "At sowing."})
        top3.append({
            "name": fn, "npk": info["npk"],
            "confidence": round(proba[idx] * 100, 1),
            "description": info["desc"],
            "rate": info["rate"], "timing": info["when"]
        })
    return {
        "recommended":     top3[0],
        "alternatives":    top3[1:],
        "soil_type":       soil_norm,
        "crop_type_mapped": crop_norm,
    }


@fertilizer_bp.route("/predict_fertilizer", methods=["POST"])
def predict_fert_ep():
    try:
        d  = dict(request.json or {})
        st = d.pop("soil_type", "Loamy")
        ct = d.pop("crop_type", "Wheat")
        return jsonify(predict_fertilizer(d, st, ct))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
