# utils/weather_api.py

import requests

# -----------------------------
# Get location using IP
# -----------------------------
def get_location():
    try:
        res = requests.get("http://ip-api.com/json").json()
        city = res.get("city", "Chennai")
        lat = res.get("lat", 13.08)
        lon = res.get("lon", 80.27)
        return city, lat, lon
    except:
        return "Chennai", 13.08, 80.27


# -----------------------------
# Auto weather using location
# -----------------------------
def get_weather_auto():
    city, lat, lon = get_location()

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(url).json()

    weather = data["current_weather"]

    return city, weather["temperature"], weather["windspeed"]


# -----------------------------
# Old function (keep for safety)
# -----------------------------
def get_weather():
    city, temp, wind = get_weather_auto()
    return temp, wind, 0