"""
backend/utils/model_loader.py
Loads all ML models (fertilizer .pkl files + soil .h5 model).
"""
import os, json
import joblib
import numpy as np

M = {}  # shared model dictionary


def load_all_models(base_dir: str):
    models_dir = os.path.join(base_dir, "models")

    # ── Fertilizer models (.pkl) ──────────────────────────────
    for key, fname in [
        ("fert_model", "fertilizer_model.pkl"),
        ("fert_le",    "fert_label_encoder.pkl"),
        ("soil_le",    "fert_soil_encoder.pkl"),
        ("crop_fe",    "fert_crop_encoder.pkl"),
    ]:
        path = os.path.join(models_dir, fname)
        if os.path.exists(path):
            M[key] = joblib.load(path)
            print(f"[Model] Loaded {fname} ✓")
        else:
            print(f"[Model] MISSING {fname}  (expected in models/)")

    # ── Soil classifier (.h5) ─────────────────────────────────
    soil_h5  = os.path.join(models_dir, "soil_classifier.h5")
    soil_map = os.path.join(models_dir, "soil_class_map.json")

    if os.path.exists(soil_h5):
        try:
            import tensorflow as tf
            M["soil_model"] = tf.keras.models.load_model(soil_h5, compile = False)
            print("[Model] Loaded soil_classifier.h5 ✓")
        except Exception as e:
            print(f"[Model] soil_classifier.h5 load error: {e}")
    else:
        print("[Model] soil_classifier.h5 NOT FOUND — place it in models/")

    if os.path.exists(soil_map):
        with open(soil_map) as f:
            M["soil_class_map"] = json.load(f)
        print(f"[Model] soil_class_map.json loaded ✓")
    else:
        M["soil_class_map"] = {"0": "Alluvial", "1": "Black", "2": "Clay", "3": "Red", "4": "Yellow"}
        print("[Model] Using default soil_class_map (5 classes)")

    # ── Crop Disease classifier (.h5) ────────────────────────────────
    disease_h5  = os.path.join(models_dir, "crop_disease.h5")
    disease_map = os.path.join(models_dir, "disease_class_map.json")

    if os.path.exists(disease_h5):
        try:
            import tensorflow as tf
            M["disease_model"] = tf.keras.models.load_model(disease_h5, compile=False)
            print("[Model] Loaded crop_disease.h5 ✓")
        except Exception as e:
            print(f"[Model] crop_disease.h5 load error: {e}")
    else:
        print("[Model] crop_disease.h5 NOT FOUND — place it in models/ (38-class PlantVillage model)")

    if os.path.exists(disease_map):
        with open(disease_map) as f:
            M["disease_class_map"] = json.load(f)
        print("[Model] disease_class_map.json loaded ✓")
    else:
        print("[Model] Using built-in DISEASE_CLASSES list for disease_class_map")
