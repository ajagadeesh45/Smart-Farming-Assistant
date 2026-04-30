import pickle, os
import numpy as np

_BASE = os.path.join(os.path.dirname(__file__), "..", "models")

with open(os.path.join(_BASE, "price_model.pkl"), "rb") as f:
    _price_model = pickle.load(f)

# Features: Commodity(int), Min Price, Max Price, Year, Month, Day
# Feature importance: MinPrice=33%, MaxPrice=67% — date has ~0 impact
# Strategy: derive min/max from user's single "today's price" input (±25%)

COMMODITY_IDX = {
    "Tomato": 0, "Potato": 1, "Onion": 2,
    "Rice":   3, "Wheat":  4, "Maize": 5,
}

# Typical Indian mandi price ranges (₹/quintal) — shown as hint to user
PRICE_RANGES = {
    "Tomato": (500,  3000),
    "Potato": (400,  2000),
    "Onion":  (400,  2500),
    "Rice":   (1500, 3500),
    "Wheat":  (1800, 3200),
    "Maize":  (900,  2200),
}

def predict_price(commodity: str, current_price: float) -> float:
    """
    Predict modal (fair market) price.
    Args:
        commodity     — crop name string  e.g. "Tomato"
        current_price — today's price the farmer sees (₹/qtl)
    Returns:
        predicted modal price (float, ₹/qtl)
    """
    import datetime
    today  = datetime.date.today()
    idx    = COMMODITY_IDX.get(commodity, 0)
    min_p  = round(current_price * 0.75)
    max_p  = round(current_price * 1.25)
    x      = np.array([[idx, min_p, max_p,
                        today.year, today.month, today.day]])
    return round(float(_price_model.predict(x)[0]), 2)
