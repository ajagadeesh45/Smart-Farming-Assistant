import pickle
import numpy as np

with open("models/price_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_price(commodity, min_p, max_p, year, month, day):
    data = np.array([[commodity, min_p, max_p, year, month, day]])
    pred = model.predict(data)
    return round(pred[0], 2)