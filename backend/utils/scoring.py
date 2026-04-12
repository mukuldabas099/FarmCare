"""
backend/utils/scoring.py
Sensor thresholds, health score calculation, and improvement suggestions.
"""

THRESH = {
    "temperature": {"low": 10,  "high": 40,  "unit": "°C",    "opt": "15–35"},
    "moisture":    {"low": 20,  "high": 70,  "unit": "%",     "opt": "25–65"},
    "ec":          {"low": 200, "high": 800, "unit": "µS/cm", "opt": "200–800"},
    "ph":          {"low": 5.5, "high": 8.0, "unit": "pH",    "opt": "5.5–7.5"},
    "nitrogen":    {"low": 5,   "high": 140, "unit": "mg/kg", "opt": "40–120"},
    "phosphorus":  {"low": 5,   "high": 100, "unit": "mg/kg", "opt": "5–60"},
    "potassium":   {"low": 5,   "high": 205, "unit": "mg/kg", "opt": "15–120"},
}

SUGS = {
    "temperature_low":  "Soil too cold. Use mulching to retain warmth.",
    "temperature_high": "Soil temperature high. Apply organic mulch to cool surface.",
    "moisture_low":     "Moisture critically low. Irrigate immediately.",
    "moisture_high":    "Over-watered. Reduce irrigation. Improve drainage.",
    "ec_low":           "Low conductivity. Soil may lack dissolved nutrients.",
    "ec_high":          "High EC — salt stress. Leach soil with fresh water.",
    "ph_low":           "Acidic soil. Apply agricultural lime (CaCO₃) at 2–4 t/ha.",
    "ph_high":          "Alkaline soil. Apply elemental sulfur to lower pH.",
    "nitrogen_low":     "Nitrogen deficiency. Apply Urea (46-0-0) or organic compost.",
    "nitrogen_high":    "Excess nitrogen. Stop further N fertilization.",
    "phosphorus_low":   "Phosphorus deficient. Apply DAP (18-46-0).",
    "phosphorus_high":  "Phosphorus excess. Skip P fertilizers this season.",
    "potassium_low":    "Potassium deficient. Apply MOP (0-0-60).",
    "potassium_high":   "Excess potassium. Avoid further K applications.",
}


def classify(param, val):
    if val in (None, -1):
        return "error"
    t = THRESH.get(param)
    if not t:
        return "unknown"
    return "low" if val < t["low"] else "high" if val > t["high"] else "optimal"


def health_score(data):
    W = {"ph": 25, "nitrogen": 18, "moisture": 18,
         "phosphorus": 12, "potassium": 12, "temperature": 8, "ec": 7}
    tw = sum(W.values())
    sc = 0.0
    for p, w in W.items():
        val = data.get(p)
        if val in (None, -1):
            sc += w * 0.3
            continue
        t = THRESH[p]
        r = t["high"] - t["low"]
        if r == 0:
            sc += w
            continue
        mid = (t["low"] + t["high"]) / 2
        if t["low"] <= val <= t["high"]:
            sc += w * (1 - 0.25 * abs(val - mid) / (r / 2))
        else:
            excess = max(0, val - t["high"]) + max(0, t["low"] - val)
            sc += w * max(0, 1 - min(1.0, excess / (r * 0.5)))
    return round((sc / tw) * 100)


def safe(v, d):
    return d if v in (None, -1) else v


def get_sugs(data):
    s = []
    for p in THRESH:
        val = data.get(p)
        if val in (None, -1):
            continue
        st = classify(p, val)
        if st != "optimal" and f"{p}_{st}" in SUGS:
            s.append(SUGS[f"{p}_{st}"])
    return s or ["All soil parameters are within optimal range. ✓"]
