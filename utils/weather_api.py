import requests

WX_DESC = {
    0:  ("Clear sky",        "☀️"),
    1:  ("Mainly clear",     "🌤️"),
    2:  ("Partly cloudy",    "⛅"),
    3:  ("Overcast",         "☁️"),
    45: ("Foggy",            "🌫️"),
    48: ("Icy fog",          "🌫️"),
    51: ("Light drizzle",    "🌦️"),
    53: ("Drizzle",          "🌦️"),
    55: ("Heavy drizzle",    "🌧️"),
    61: ("Slight rain",      "🌧️"),
    63: ("Moderate rain",    "🌧️"),
    65: ("Heavy rain",       "🌧️"),
    80: ("Slight showers",   "🌦️"),
    81: ("Showers",          "🌧️"),
    82: ("Heavy showers",    "⛈️"),
    95: ("Thunderstorm",     "⛈️"),
    99: ("Heavy thunderstorm","⛈️"),
}

def get_weather():
    """
    Fetch live weather — Chennai (13.08°N, 80.27°E) via Open-Meteo.
    Returns: (temperature, windspeed, weathercode, humidity, precip_prob)
    Falls back to typical Chennai values if network unavailable.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=13.08&longitude=80.27"
        "&current_weather=true"
        "&hourly=relativehumidity_2m,precipitation_probability"
        "&forecast_days=1"
    )
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        data        = resp.json()
        cw          = data["current_weather"]
        humidity    = data["hourly"]["relativehumidity_2m"][0]
        precip_prob = data["hourly"]["precipitation_probability"][0]
        return (cw["temperature"], cw["windspeed"],
                cw["weathercode"], humidity, precip_prob)
    except Exception:
        # Fallback: typical Chennai April values
        return 33.0, 14.0, 2, 68, 20

def wx_label(code: int):
    """Return (description_str, emoji_str) for a WMO weather code."""
    return WX_DESC.get(code, ("Partly cloudy", "⛅"))
