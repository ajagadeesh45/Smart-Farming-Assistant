import pickle, os
import numpy as np

# Absolute path — works regardless of where you run streamlit from
_BASE = os.path.join(os.path.dirname(__file__), "..", "models")

with open(os.path.join(_BASE, "Crop_recommendation_model.pkl"), "rb") as f:
    _crop_model = pickle.load(f)
with open(os.path.join(_BASE, "label_encoder.pkl"), "rb") as f:
    _le = pickle.load(f)

SOIL_PRESETS = {
    "Red Soil":      (40, 35, 30, 6.0),
    "Black Soil":    (80, 45, 55, 7.2),
    "Sandy Soil":    (20, 18, 15, 5.8),
    "Loamy Soil":    (85, 42, 43, 6.5),
    "Clay Soil":     (60, 38, 50, 6.8),
    "Alluvial Soil": (90, 50, 60, 7.0),
}

WATER_PRESETS = {
    "High — Fully Irrigated":        (1.3, 2000),
    "Medium — Partial Irrigation":   (1.0, 1000),
    "Low — Rainfed Only":            (0.8,  400),
}

def recommend_crop(soil_type: str, water_avail: str,
                   temperature: float, humidity: float):
    """
    Returns top-3 list of (crop_name, confidence_pct).
    Inputs come from simple farmer UI + live weather.
    """
    N, P, K, ph = SOIL_PRESETS.get(soil_type, (60, 38, 40, 6.5))
    k_factor, base_rain = WATER_PRESETS.get(water_avail, (1.0, 1000))
    K_adj    = int(K * k_factor)
    x        = np.array([[N, P, K_adj, temperature, humidity, ph, base_rain]])
    proba    = _crop_model.predict_proba(x)[0]
    top3     = [(str(_le.classes_[i]), round(float(proba[i]) * 100, 1))
                for i in np.argsort(proba)[::-1][:3]]
    return top3
