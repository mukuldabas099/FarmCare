"""
backend/utils/crop_data.py
All soil/crop/fertilizer mappings and ideal ranges.
"""

# ── Soil type → recommended crops ────────────────────────────
SOIL_CROP_MAP = {
    "Alluvial": [
        {"crop": "Rice",      "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Nov"},
        {"crop": "Wheat",     "season": "Rabi",   "season_hi": "रबी",    "months": "Nov–Apr"},
        {"crop": "Sugarcane", "season": "Annual", "season_hi": "वार्षिक", "months": "Year-round"},
        {"crop": "Pulses",    "season": "Annual", "season_hi": "वार्षिक", "months": "Year-round"},
        {"crop": "Mustard",   "season": "Rabi",   "season_hi": "रबी",    "months": "Oct–Mar"},
    ],
    "Black": [
        {"crop": "Cotton",    "season": "Kharif", "season_hi": "खरीफ",   "months": "May–Dec"},
        {"crop": "Soybean",   "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Oct"},
        {"crop": "Groundnut", "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Oct"},
        {"crop": "Wheat",     "season": "Rabi",   "season_hi": "रबी",    "months": "Nov–Apr"},
        {"crop": "Sugarcane", "season": "Annual", "season_hi": "वार्षिक", "months": "Year-round"},
    ],
    "Red": [
        {"crop": "Millets (Jowar/Bajra)", "season": "Kharif", "season_hi": "खरीफ", "months": "Jun–Oct"},
        {"crop": "Pulses",    "season": "Annual", "season_hi": "वार्षिक", "months": "Year-round"},
        {"crop": "Groundnut", "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Oct"},
        {"crop": "Cotton",    "season": "Kharif", "season_hi": "खरीफ",   "months": "May–Dec"},
    ],
    "Yellow": [
        {"crop": "Maize",     "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Oct"},
        {"crop": "Rice",      "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Nov"},
        {"crop": "Groundnut", "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Oct"},
        {"crop": "Pulses",    "season": "Annual", "season_hi": "वार्षिक", "months": "Year-round"},
    ],
    "Clay": [
        {"crop": "Rice",    "season": "Kharif", "season_hi": "खरीफ",   "months": "Jun–Nov", "note": "Best suited"},
        {"crop": "Cabbage", "season": "Rabi",   "season_hi": "रबी",    "months": "Oct–Mar"},
        {"crop": "Beans",   "season": "Annual", "season_hi": "वार्षिक", "months": "Year-round"},
    ],
}

# ── Ideal sensor ranges per crop ──────────────────────────────
CROP_IDEAL = {
    "Rice":      {"temperature":[20,35],"moisture":[55,80],"ec":[200,600],"ph":[5.5,7.0],"nitrogen":[80,120],"phosphorus":[40,60],"potassium":[80,120]},
    "Wheat":     {"temperature":[10,25],"moisture":[40,65],"ec":[200,700],"ph":[6.0,7.5],"nitrogen":[80,120],"phosphorus":[40,80],"potassium":[80,150]},
    "Cotton":    {"temperature":[25,35],"moisture":[35,65],"ec":[200,800],"ph":[6.0,8.0],"nitrogen":[60,100],"phosphorus":[30,60],"potassium":[60,100]},
    "Maize":     {"temperature":[18,32],"moisture":[40,65],"ec":[200,600],"ph":[5.8,7.0],"nitrogen":[80,140],"phosphorus":[40,80],"potassium":[80,140]},
    "Sugarcane": {"temperature":[20,38],"moisture":[55,75],"ec":[200,600],"ph":[6.0,8.0],"nitrogen":[80,150],"phosphorus":[40,80],"potassium":[80,150]},
    "Soybean":   {"temperature":[20,30],"moisture":[40,65],"ec":[200,500],"ph":[6.0,7.0],"nitrogen":[20,60], "phosphorus":[40,80],"potassium":[60,100]},
    "Groundnut": {"temperature":[25,35],"moisture":[40,60],"ec":[200,500],"ph":[5.5,7.0],"nitrogen":[20,60], "phosphorus":[40,80],"potassium":[40,80]},
    "Mustard":   {"temperature":[10,25],"moisture":[30,55],"ec":[200,600],"ph":[6.0,7.5],"nitrogen":[60,100],"phosphorus":[30,60],"potassium":[40,80]},
    "Pulses":    {"temperature":[15,30],"moisture":[30,55],"ec":[200,500],"ph":[6.0,7.5],"nitrogen":[20,50], "phosphorus":[30,70],"potassium":[40,80]},
    "Millets":   {"temperature":[25,35],"moisture":[25,50],"ec":[200,500],"ph":[6.0,7.5],"nitrogen":[40,80], "phosphorus":[20,50],"potassium":[40,80]},
    "Cabbage":   {"temperature":[10,22],"moisture":[45,65],"ec":[200,600],"ph":[6.0,7.5],"nitrogen":[80,140],"phosphorus":[40,80],"potassium":[80,120]},
    "Beans":     {"temperature":[15,28],"moisture":[40,60],"ec":[200,500],"ph":[6.0,7.5],"nitrogen":[20,60], "phosphorus":[30,70],"potassium":[60,100]},
}

# ── Improvement suggestions per parameter ─────────────────────
IMPROVE_SUGS = {
    "temperature": {
        "low":  "Soil temperature too low. Use plastic mulch or greenhouse covers to warm the soil.",
        "high": "Soil too hot. Apply organic mulch (straw/hay) to cool the surface."
    },
    "moisture": {
        "low":  "Moisture below ideal. Irrigate immediately. Consider drip irrigation for efficiency.",
        "high": "Over-watered. Reduce irrigation frequency. Improve drainage channels."
    },
    "ec": {
        "low":  "Low EC — soil lacks dissolved nutrients. Add NPK fertilizer as per recommendation.",
        "high": "High EC (salt stress). Leach soil with 2–3 deep irrigations using fresh water."
    },
    "ph": {
        "low":  "Acidic soil. Apply agricultural lime (CaCO₃) at 2–4 tonnes/hectare to raise pH.",
        "high": "Alkaline soil. Apply elemental sulfur (1–2 kg/100 sqm) or gypsum to lower pH."
    },
    "nitrogen": {
        "low":  "Nitrogen deficiency. Apply Urea (46-0-0) at 100–150 kg/ha or organic compost.",
        "high": "Excess nitrogen. Withhold N fertilizers. Apply potassium to balance."
    },
    "phosphorus": {
        "low":  "Phosphorus deficient. Apply DAP (18-46-0) at 100–125 kg/ha.",
        "high": "Phosphorus excess. Skip P fertilizers this season. Improve drainage."
    },
    "potassium": {
        "low":  "Potassium low. Apply MOP (Muriate of Potash, 0-0-60) at 50–100 kg/ha.",
        "high": "Excess potassium. Avoid K fertilizers this season."
    },
}

# ── Fertilizer info table ──────────────────────────────────────
FERT_INFO = {
    "Urea":      {"npk": "46-0-0",   "desc": "High nitrogen. Best for leafy/vegetative growth stages.",
                  "rate": "100–150 kg/ha", "when": "Basal at sowing + top-dress at tillering."},
    "DAP":       {"npk": "18-46-0",  "desc": "High phosphorus. Promotes strong root development.",
                  "rate": "100–125 kg/ha", "when": "Apply as basal dose before or at sowing."},
    "14-35-14":  {"npk": "14-35-14", "desc": "Balanced NPK, high P. Good for fruiting and flowering.",
                  "rate": "150–200 kg/ha", "when": "50% at sowing, 50% at vegetative stage."},
    "28-28":     {"npk": "28-28-0",  "desc": "Equal N-P. For soils deficient in both N and P.",
                  "rate": "120–175 kg/ha", "when": "Basal dose + top-dress at 30 days."},
    "17-17-17":  {"npk": "17-17-17", "desc": "Complete balanced NPK. Good for all crop growth stages.",
                  "rate": "150–200 kg/ha", "when": "Apply at sowing + top dress during growth."},
    "10-26-26":  {"npk": "10-26-26", "desc": "High P and K. Ideal for root crops and fruit development.",
                  "rate": "100–150 kg/ha", "when": "Apply at sowing or transplanting stage."},
    "20-20":     {"npk": "20-20-0",  "desc": "Balanced N-P fertilizer. Good for N and P deficient soils.",
                  "rate": "100–150 kg/ha", "when": "Basal application or top dressing."},
}

# ── Soil encoder mappings ─────────────────────────────────────
SOIL_MAP_FERT = {
    "black": "Black",        "black cotton": "Black",    "black soil": "Black",
    "clay": "Clayey",        "clayey": "Clayey",         "clay loam": "Clayey",
    "clayey soil": "Clayey",
    "loam": "Loamy",         "loamy": "Loamy",           "loam soil": "Loamy",
    "red": "Red",            "red laterite": "Red",      "red soil": "Red",
    "sandy": "Sandy",        "sandy soil": "Sandy",
    "alluvial": "Loamy",     "alluvial soil": "Loamy",
    "yellow": "Sandy",       "yellow soil": "Sandy",
}

CROP_TO_FERT = {
    "rice": "Paddy",        "wheat": "Wheat",        "maize": "Maize",
    "cotton": "Cotton",     "sugarcane": "Sugarcane", "soybean": "Pulses",
    "groundnut": "Ground Nuts", "mustard": "Oil seeds", "pulses": "Pulses",
    "millets": "Millets",   "cabbage": "Wheat",       "beans": "Pulses",
    "millets (jowar/bajra)": "Millets",
    "paddy": "Paddy",       "barley": "Barley",       "tobacco": "Tobacco",
}


def normalize_soil_for_fert(s: str) -> str:
    key = s.lower().strip()
    if key in SOIL_MAP_FERT:
        return SOIL_MAP_FERT[key]
    first = key.split()[0]
    return SOIL_MAP_FERT.get(first, "Loamy")


def map_crop_for_fert(crop_str: str, crop_fe=None) -> str:
    key = crop_str.lower().strip()
    if key in CROP_TO_FERT:
        return CROP_TO_FERT[key]
    if crop_fe is not None:
        classes_lower = {c.lower(): c for c in crop_fe.classes_}
        if key in classes_lower:
            return classes_lower[key]
    return "Wheat"
