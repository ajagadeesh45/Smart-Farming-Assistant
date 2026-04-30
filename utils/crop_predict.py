# utils/crop_predict.py

import pickle
import numpy as np
import os

# =========================
# LOAD MODEL (SAFE PATH)
# =========================

model_path = os.path.join("models", "Crop_recommendation_model.pkl")
encoder_path = os.path.join("models", "label_encoder.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(encoder_path, "rb") as f:
    label_encoder = pickle.load(f)

# =========================
# PREDICTION FUNCTION
# =========================

def recommend_crop(N, P, K, temperature, humidity, ph, rainfall):
    try:
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        
        prediction = model.predict(data)
        crop_name = label_encoder.inverse_transform(prediction)

        return crop_name[0]

    except Exception as e:
        return f"Prediction Error: {e}"