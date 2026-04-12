"""
backend/routes/optimize.py
Route: /optimize_crop
"""
from flask import Blueprint, request, jsonify
from backend.utils.sensor_state import latest, lock, SK
from backend.utils.scoring      import classify, THRESH
from backend.utils.crop_data    import CROP_IDEAL, IMPROVE_SUGS

optimize_bp = Blueprint("optimize", __name__)


def optimize_crop(data: dict, crop_name: str) -> dict:
    ideal = CROP_IDEAL.get(crop_name)
    if not ideal:
        return {"error": f"No ideal data for crop '{crop_name}'"}

    params      = ["temperature","moisture","ec","ph","nitrogen","phosphorus","potassium"]
    comparison  = []
    suggestions = []
    all_optimal = True

    for p in params:
        val    = data.get(p)
        lo, hi = ideal[p]
        t      = THRESH[p]
        if val in (None, -1):
            comparison.append({"param": p, "value": "N/A",
                                "ideal": f"{lo}–{hi}", "unit": t["unit"], "status": "error"})
            continue
        if lo <= val <= hi:
            status = "optimal"
        elif val < lo:
            status = "low"
            all_optimal = False
            sug = IMPROVE_SUGS.get(p, {}).get("low", f"Increase {p}.")
            suggestions.append(f"🔻 {p.title()}: {val}{t['unit']} is below ideal ({lo}–{hi}). {sug}")
        else:
            status = "high"
            all_optimal = False
            sug = IMPROVE_SUGS.get(p, {}).get("high", f"Decrease {p}.")
            suggestions.append(f"🔺 {p.title()}: {val}{t['unit']} exceeds ideal ({lo}–{hi}). {sug}")

        comparison.append({
            "param": p, "value": val,
            "ideal": f"{lo}–{hi}", "unit": t["unit"], "status": status,
        })

    overall_match = round(
        sum(1 for c in comparison if c["status"] == "optimal") / len(params) * 100
    )
    return {
        "crop":            crop_name,
        "comparison":      comparison,
        "suggestions":     suggestions or ["✅ All parameters are within ideal range for this crop!"],
        "overall_match_pct": overall_match,
        "all_optimal":     all_optimal,
    }


@optimize_bp.route("/optimize_crop", methods=["POST"])
def optimize_crop_ep():
    try:
        d         = dict(request.json or {})
        crop_name = d.pop("crop_name", "Rice")
        with lock:
            snap = dict(latest)
        for k in SK:
            if k not in d or d[k] in (None, -1):
                d[k] = snap.get(k, -1)
        return jsonify(optimize_crop(d, crop_name))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
