"""
backend/utils/disease_data.py
Disease information: solutions, causes, and prevention for each crop disease class.
Compatible with PlantVillage dataset class names.
"""

# Maps class label → rich disease info dict
DISEASE_INFO = {
    # ── Apple ──────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "crop": "Apple", "disease": "Apple Scab",
        "emoji": "🍎",
        "severity": "High",
        "cause": "Fungal infection by Venturia inaequalis. Spreads via wind and rain.",
        "symptoms": "Olive-green or brown spots on leaves and fruit; scabby lesions.",
        "solution": [
            "Apply fungicides (captan, mancozeb) at early leaf stage",
            "Remove and destroy fallen leaves to reduce fungal spores",
            "Prune trees for better air circulation",
            "Use resistant apple varieties when replanting",
        ],
        "prevention": "Spray fungicide during wet spring weather. Keep orchard floor clean.",
    },
    "Apple___Black_rot": {
        "crop": "Apple", "disease": "Black Rot",
        "emoji": "🍎",
        "severity": "High",
        "cause": "Fungus Botryosphaeria obtusa. Enters via wounds and dead wood.",
        "symptoms": "Brown rotting areas on fruit; purple spots on leaves with frog-eye pattern.",
        "solution": [
            "Remove mummified fruits and dead wood immediately",
            "Apply copper-based fungicide sprays",
            "Prune infected branches 10–15 cm below visible symptoms",
            "Maintain tree vigor with proper fertilization",
        ],
        "prevention": "Avoid wounding trees during pruning. Remove cankers early.",
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple", "disease": "Cedar Apple Rust",
        "emoji": "🍎",
        "severity": "Medium",
        "cause": "Fungus Gymnosporangium juniperi-virginianae; requires cedar/juniper hosts.",
        "symptoms": "Bright orange-yellow spots on upper leaf surface; tube-like structures underneath.",
        "solution": [
            "Apply myclobutanil or propiconazole fungicide at pink bud stage",
            "Remove nearby cedar/juniper trees if feasible",
            "Plant rust-resistant apple cultivars",
            "Continue fungicide sprays through petal fall",
        ],
        "prevention": "Avoid planting apple near cedar trees. Spray preventively in spring.",
    },
    "Apple___healthy": {
        "crop": "Apple", "disease": None,
        "emoji": "🍎", "severity": "None",
        "cause": "", "symptoms": "No disease detected — plant appears healthy.",
        "solution": ["Continue regular monitoring", "Maintain proper irrigation and nutrition"],
        "prevention": "Keep orchard clean, prune annually, monitor for pests.",
    },

    # ── Blueberry ──────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "crop": "Blueberry", "disease": None,
        "emoji": "🫐", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Regular watering and mulching", "Annual fertilization with acidic fertilizer"],
        "prevention": "Maintain soil pH 4.5–5.5. Monitor for pests.",
    },

    # ── Cherry ─────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry", "disease": "Powdery Mildew",
        "emoji": "🍒",
        "severity": "Medium",
        "cause": "Fungus Podosphaera clandestina. Thrives in warm, dry conditions.",
        "symptoms": "White powdery coating on young leaves, shoots, and fruit.",
        "solution": [
            "Spray sulfur-based or potassium bicarbonate fungicide",
            "Apply neem oil solution weekly during active growth",
            "Remove heavily infected leaves and shoots",
            "Improve air circulation by pruning",
        ],
        "prevention": "Avoid overhead irrigation. Plant resistant varieties.",
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry", "disease": None,
        "emoji": "🍒", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Regular pruning", "Balanced fertilization"],
        "prevention": "Monitor for pests and fungal issues in spring.",
    },

    # ── Corn / Maize ───────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn / Maize", "disease": "Gray Leaf Spot",
        "emoji": "🌽",
        "severity": "High",
        "cause": "Fungus Cercospora zeae-maydis. Favored by warm, humid weather.",
        "symptoms": "Rectangular gray-tan lesions parallel to leaf veins.",
        "solution": [
            "Apply strobilurin or triazole fungicide at tasseling stage",
            "Rotate crops — do not plant corn in same field continuously",
            "Use resistant hybrids",
            "Till crop residue to reduce inoculum",
        ],
        "prevention": "Crop rotation every 2 years. Choose resistant varieties.",
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn / Maize", "disease": "Common Rust",
        "emoji": "🌽",
        "severity": "Medium",
        "cause": "Fungus Puccinia sorghi. Spreads through airborne spores.",
        "symptoms": "Brick-red to brown pustules scattered on both leaf surfaces.",
        "solution": [
            "Apply mancozeb or propiconazole at early rust stages",
            "Plant resistant maize hybrids",
            "Early planting to avoid peak rust pressure",
            "Monitor fields weekly during growing season",
        ],
        "prevention": "Use certified rust-resistant seeds. Scout fields regularly.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn / Maize", "disease": "Northern Leaf Blight",
        "emoji": "🌽",
        "severity": "High",
        "cause": "Fungus Exserohilum turcicum. Cool, moist conditions favor spread.",
        "symptoms": "Long, elliptical gray-green to tan lesions on leaves.",
        "solution": [
            "Apply fungicides (pyraclostrobin, propiconazole) before tasseling",
            "Use resistant hybrid varieties",
            "Rotate with non-host crops (soybean, wheat)",
            "Deep till infected residues",
        ],
        "prevention": "Plant early. Use resistant hybrids. Rotate crops annually.",
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn / Maize", "disease": None,
        "emoji": "🌽", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Maintain proper nitrogen levels", "Regular scouting"],
        "prevention": "Crop rotation and resistant varieties.",
    },

    # ── Grape ─────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "crop": "Grape", "disease": "Black Rot",
        "emoji": "🍇",
        "severity": "High",
        "cause": "Fungus Guignardia bidwellii. Spreads in warm, wet weather.",
        "symptoms": "Tan/brown circular lesions on leaves; black shriveled 'mummies' on fruit.",
        "solution": [
            "Apply captan, mancozeb, or myclobutanil from bud break",
            "Remove mummified berries and infected leaves",
            "Ensure good canopy ventilation through pruning",
            "Continue sprays until veraison (color change)",
        ],
        "prevention": "Remove mummies over winter. Spray preventively in spring.",
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape", "disease": "Esca / Black Measles",
        "emoji": "🍇",
        "severity": "High",
        "cause": "Complex fungal disease involving Phaeomoniella and Phaeoacremonium spp.",
        "symptoms": "Tiger-stripe pattern on leaves; black spots in berry flesh; apoplexy (sudden wilting).",
        "solution": [
            "No curative treatment exists — manage to slow spread",
            "Remove and destroy infected wood and canes",
            "Protect pruning wounds with fungicide paste or sealant",
            "Avoid large pruning wounds; prune in dry weather",
        ],
        "prevention": "Prune during dry conditions. Apply wound protectants immediately.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape", "disease": "Leaf Blight (Isariopsis)",
        "emoji": "🍇",
        "severity": "Medium",
        "cause": "Fungus Pseudocercospora vitis. Wet, humid conditions promote spread.",
        "symptoms": "Angular brown spots on older leaves; premature defoliation.",
        "solution": [
            "Apply copper-based fungicide or mancozeb sprays",
            "Remove infected leaves to reduce spore load",
            "Improve row orientation for better air circulation",
        ],
        "prevention": "Maintain vine vigor. Avoid over-irrigation.",
    },
    "Grape___healthy": {
        "crop": "Grape", "disease": None,
        "emoji": "🍇", "severity": "None",
        "cause": "", "symptoms": "Vine appears healthy.",
        "solution": ["Regular canopy management", "Balanced fertilization"],
        "prevention": "Annual pruning and preventive fungicide schedule.",
    },

    # ── Orange ─────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange", "disease": "Huanglongbing (Citrus Greening)",
        "emoji": "🍊",
        "severity": "Critical",
        "cause": "Bacteria Candidatus Liberibacter asiaticus, spread by Asian citrus psyllid.",
        "symptoms": "Yellow shoots; blotchy mottling of leaves; small, misshapen bitter fruit.",
        "solution": [
            "No cure — infected trees must be removed and destroyed",
            "Control psyllid vectors with systemic insecticides (imidacloprid)",
            "Use certified disease-free nursery stock for replanting",
            "Report outbreaks to local agriculture department",
        ],
        "prevention": "Purchase certified clean planting material. Control psyllid population.",
    },

    # ── Peach ─────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "crop": "Peach", "disease": "Bacterial Spot",
        "emoji": "🍑",
        "severity": "High",
        "cause": "Bacteria Xanthomonas arboricola pv. pruni. Spreads via rain splash.",
        "symptoms": "Water-soaked spots on leaves that turn angular and dark; fruit cracking.",
        "solution": [
            "Apply copper bactericide sprays from petal fall",
            "Avoid overhead irrigation to reduce spread",
            "Prune out infected branches",
            "Apply zinc sprays during dormancy",
        ],
        "prevention": "Use resistant varieties. Apply copper sprays preventively.",
    },
    "Peach___healthy": {
        "crop": "Peach", "disease": None,
        "emoji": "🍑", "severity": "None",
        "cause": "", "symptoms": "Tree is healthy.",
        "solution": ["Annual dormant pruning", "Balanced fertilization"],
        "prevention": "Scout regularly; spray preventive copper in late dormancy.",
    },

    # ── Bell Pepper ────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper", "disease": "Bacterial Spot",
        "emoji": "🫑",
        "severity": "High",
        "cause": "Bacteria Xanthomonas campestris pv. vesicatoria. Warm, rainy conditions.",
        "symptoms": "Water-soaked spots on leaves; raised scabby spots on fruit.",
        "solution": [
            "Apply copper hydroxide + mancozeb sprays",
            "Remove and destroy infected plant parts",
            "Use disease-free certified seeds or transplants",
            "Rotate peppers with non-solanaceous crops",
        ],
        "prevention": "Use resistant varieties. Avoid working in wet fields.",
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper", "disease": None,
        "emoji": "🫑", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Regular watering", "Stake plants for support"],
        "prevention": "Use disease-free seeds. Rotate crops every 2–3 years.",
    },

    # ── Potato ─────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "crop": "Potato", "disease": "Early Blight",
        "emoji": "🥔",
        "severity": "Medium",
        "cause": "Fungus Alternaria solani. Attacks older leaves first.",
        "symptoms": "Concentric ring target-like brown spots on lower leaves.",
        "solution": [
            "Spray chlorothalonil or mancozeb every 7–10 days",
            "Remove infected lower leaves",
            "Ensure adequate potassium — deficiency worsens blight",
            "Avoid wetting foliage during irrigation",
        ],
        "prevention": "Use certified seed tubers. Rotate crops. Maintain plant nutrition.",
    },
    "Potato___Late_blight": {
        "crop": "Potato", "disease": "Late Blight",
        "emoji": "🥔",
        "severity": "Critical",
        "cause": "Oomycete Phytophthora infestans. The cause of Irish Potato Famine.",
        "symptoms": "Water-soaked dark lesions on leaves, spreading rapidly; white mold under humid conditions; tuber rot.",
        "solution": [
            "Apply metalaxyl + mancozeb or cymoxanil fungicide immediately",
            "Destroy infected plants and haulm — do not compost",
            "Harvest tubers quickly when infection is detected",
            "Use certified blight-free seed potatoes next season",
        ],
        "prevention": "Plant resistant varieties (Sarpo Mira). Scout fields every 3 days in humid weather.",
    },
    "Potato___healthy": {
        "crop": "Potato", "disease": None,
        "emoji": "🥔", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Proper hilling", "Consistent irrigation"],
        "prevention": "Use certified seed. Rotate with cereals every 3 years.",
    },

    # ── Raspberry ─────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "crop": "Raspberry", "disease": None,
        "emoji": "🍓", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Annual cane removal after fruiting", "Mulching"],
        "prevention": "Ensure good drainage. Scout for cane blight.",
    },

    # ── Soybean ────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "crop": "Soybean", "disease": None,
        "emoji": "🌿", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Maintain proper row spacing", "Apply balanced fertilizer"],
        "prevention": "Rotate with corn or wheat. Monitor for aphids.",
    },

    # ── Squash ─────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "crop": "Squash", "disease": "Powdery Mildew",
        "emoji": "🎃",
        "severity": "Medium",
        "cause": "Fungi Podosphaera xanthii and Erysiphe cichoracearum. Dry, warm days.",
        "symptoms": "White powdery coating on leaves and stems; yellowing and premature leaf drop.",
        "solution": [
            "Spray potassium bicarbonate or neem oil solution",
            "Apply sulfur-based fungicide preventively",
            "Remove heavily infected plant parts",
            "Improve air circulation — thin plants if overcrowded",
        ],
        "prevention": "Plant resistant varieties. Avoid excessive nitrogen. Ensure spacing.",
    },

    # ── Strawberry ─────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry", "disease": "Leaf Scorch",
        "emoji": "🍓",
        "severity": "Medium",
        "cause": "Fungus Diplocarpon earlianum. Wet, mild conditions favor disease.",
        "symptoms": "Small dark purple spots on leaves; edges turn reddish-brown (scorched look).",
        "solution": [
            "Apply captan or myclobutanil fungicide at first sign",
            "Remove old and infected leaves after harvest",
            "Avoid overhead irrigation",
            "Ensure good bed drainage",
        ],
        "prevention": "Renovate beds after harvest. Use straw mulch to reduce splash.",
    },
    "Strawberry___healthy": {
        "crop": "Strawberry", "disease": None,
        "emoji": "🍓", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy.",
        "solution": ["Regular runner management", "Mulch beds to reduce splash"],
        "prevention": "Renovate after harvest. Use certified plants.",
    },

    # ── Tomato ─────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "crop": "Tomato", "disease": "Bacterial Spot",
        "emoji": "🍅",
        "severity": "High",
        "cause": "Bacteria Xanthomonas spp. Spread by water splash and contaminated tools.",
        "symptoms": "Water-soaked spots on leaves turning dark; scabby raised spots on fruit.",
        "solution": [
            "Apply copper-based bactericide (copper hydroxide) every 7 days",
            "Remove infected plant debris",
            "Use disease-free transplants from certified nursery",
            "Avoid working in fields when plants are wet",
        ],
        "prevention": "Use resistant varieties. Disinfect tools with bleach solution.",
    },
    "Tomato___Early_blight": {
        "crop": "Tomato", "disease": "Early Blight",
        "emoji": "🍅",
        "severity": "Medium",
        "cause": "Fungus Alternaria solani. Common in warm, humid conditions.",
        "symptoms": "Target-like brown rings on older leaves; stem lesions at soil level.",
        "solution": [
            "Apply chlorothalonil, mancozeb, or copper fungicide",
            "Remove infected lower leaves immediately",
            "Stake plants and mulch to reduce soil splash",
            "Water at base — avoid wetting leaves",
        ],
        "prevention": "Mulch soil, rotate crops, use resistant varieties.",
    },
    "Tomato___Late_blight": {
        "crop": "Tomato", "disease": "Late Blight",
        "emoji": "🍅",
        "severity": "Critical",
        "cause": "Phytophthora infestans. Spreads rapidly in cool, wet weather.",
        "symptoms": "Large, irregular dark water-soaked patches on leaves; greasy white mold; brown fruit rot.",
        "solution": [
            "Apply metalaxyl + mancozeb or copper fungicide immediately",
            "Remove and bag all infected material — do not compost",
            "Destroy crop if infection is severe",
            "Plan rotation — avoid tomato/potato next year in same field",
        ],
        "prevention": "Scout in cool wet weather. Apply preventive fungicide. Use resistant varieties (Mountain Magic).",
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato", "disease": "Leaf Mold",
        "emoji": "🍅",
        "severity": "Medium",
        "cause": "Fungus Passalora fulva. Common in high humidity greenhouses.",
        "symptoms": "Pale green-yellow spots on upper leaf surface; olive-green velvety mold underneath.",
        "solution": [
            "Apply copper fungicide or mancozeb",
            "Improve ventilation in greenhouses",
            "Reduce humidity by watering in the morning",
            "Remove infected leaves promptly",
        ],
        "prevention": "Maintain humidity below 85%. Use resistant varieties.",
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato", "disease": "Septoria Leaf Spot",
        "emoji": "🍅",
        "severity": "Medium",
        "cause": "Fungus Septoria lycopersici. Wet conditions trigger spread.",
        "symptoms": "Numerous small circular spots with dark borders and gray centers on leaves.",
        "solution": [
            "Apply chlorothalonil or mancozeb fungicide",
            "Remove and discard infected foliage",
            "Mulch around plants to prevent soil splash",
            "Stake plants for improved air flow",
        ],
        "prevention": "Crop rotation. Mulching. Avoid overhead watering.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato", "disease": "Spider Mite Infestation",
        "emoji": "🍅",
        "severity": "Medium",
        "cause": "Two-spotted spider mite Tetranychus urticae. Dry, hot conditions.",
        "symptoms": "Fine stippling on leaves; bronze discoloration; webbing under leaves.",
        "solution": [
            "Spray with insecticidal soap or neem oil solution",
            "Apply miticide (abamectin, spiromesifen) if severe",
            "Increase humidity and irrigate properly",
            "Introduce predatory mites (Phytoseiulus persimilis) for biological control",
        ],
        "prevention": "Monitor plants weekly. Avoid dusty conditions. Conserve natural enemies.",
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato", "disease": "Target Spot",
        "emoji": "🍅",
        "severity": "Medium",
        "cause": "Fungus Corynespora cassiicola. Warm, wet tropical/subtropical conditions.",
        "symptoms": "Dark brown spots with concentric rings (target pattern) on leaves and fruit.",
        "solution": [
            "Apply azoxystrobin or chlorothalonil fungicide",
            "Improve field drainage and plant spacing",
            "Remove infected leaves",
            "Avoid late evening irrigation",
        ],
        "prevention": "Rotate crops. Use wider plant spacing. Avoid excessive nitrogen.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato", "disease": "Yellow Leaf Curl Virus (TYLCV)",
        "emoji": "🍅",
        "severity": "Critical",
        "cause": "Tomato Yellow Leaf Curl Virus, transmitted by whitefly (Bemisia tabaci).",
        "symptoms": "Upward curling and yellowing of leaves; stunted growth; reduced fruit set.",
        "solution": [
            "Control whitefly vector with imidacloprid or thiamethoxam systemic insecticide",
            "Remove and destroy infected plants immediately",
            "Use reflective silver mulch to repel whiteflies",
            "Erect insect-proof netting in nurseries",
        ],
        "prevention": "Plant resistant/tolerant varieties. Control whitefly populations.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato", "disease": "Tomato Mosaic Virus (ToMV)",
        "emoji": "🍅",
        "severity": "High",
        "cause": "Tomato Mosaic Virus (ToMV). Transmitted mechanically via hands and tools.",
        "symptoms": "Mosaic light-dark green patterns on leaves; leaf distortion; reduced fruit quality.",
        "solution": [
            "No cure — remove and destroy infected plants",
            "Disinfect tools and hands with soap or bleach solution",
            "Control aphid vectors with insecticides",
            "Use virus-free transplants only",
        ],
        "prevention": "Use resistant varieties (TM-2 gene). Disinfect tools between plants.",
    },
    "Tomato___healthy": {
        "crop": "Tomato", "disease": None,
        "emoji": "🍅", "severity": "None",
        "cause": "", "symptoms": "Plant is healthy — no disease detected.",
        "solution": ["Maintain regular watering schedule", "Support plants with stakes"],
        "prevention": "Rotate crops, use certified seeds, scout weekly.",
    },
}


def get_disease_info(class_label: str) -> dict:
    """
    Returns disease info for a given class label.
    Falls back to a generic response if label not found.
    """
    info = DISEASE_INFO.get(class_label)
    if info:
        return info
    # Try partial match
    for key, val in DISEASE_INFO.items():
        if class_label.lower() in key.lower():
            return val
    # Generic fallback
    parts = class_label.split("___")
    crop = parts[0].replace("_", " ") if parts else "Unknown Crop"
    disease = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown Disease"
    return {
        "crop": crop, "disease": disease,
        "emoji": "🌿", "severity": "Unknown",
        "cause": "Details not available for this class.",
        "symptoms": "Refer to agricultural extension office for diagnosis.",
        "solution": [
            "Consult your local Krishi Vigyan Kendra (KVK)",
            "Send samples to plant disease diagnostic lab",
            "Apply broad-spectrum copper-based fungicide as precaution",
        ],
        "prevention": "Use certified seeds. Practice crop rotation. Monitor fields regularly.",
    }
