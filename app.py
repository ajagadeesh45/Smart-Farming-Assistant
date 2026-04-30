# app.py
# Farmer-Friendly Professional Version

import streamlit as st
from utils.weather_api import get_weather
from utils.crop_predict import recommend_crop
from utils.price_predict import predict_price


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Smart Farming Assistant",
    page_icon="🌾",
    layout="centered"
)


# =====================================
# TITLE SECTION
# =====================================

st.title("🌾 Smart Farming Assistant")
st.subheader("AI-Powered Farming Support System 👨‍🌾")

st.write(
    "This smart assistant helps farmers with weather updates, "
    "future market price prediction, and crop recommendation."
)


# =====================================
# SIDEBAR MENU
# =====================================

option = st.sidebar.selectbox(
    "Choose Service",
    [
        "Weather Prediction",
        "Market Price Prediction",
        "Crop Recommendation"
    ]
)


# =====================================
# WEATHER PREDICTION
# =====================================

if option == "Weather Prediction":

    st.header("🌦 Weather Prediction")

    st.write("Check current weather conditions for better farming decisions.")

    if st.button("Check Current Weather"):

        temperature, windspeed, weathercode = get_weather()

        st.success(f"Current Temperature: {temperature} °C")
        st.success(f"Wind Speed: {windspeed} km/h")

        if temperature > 35:
            st.warning(
                "High temperature detected. Rainfall chances may be low. "
                "Avoid immediate sowing."
            )

        elif temperature > 28:
            st.info(
                "Moderate weather. Suitable for farming activities and crop planning."
            )

        else:
            st.success(
                "Cool weather. Good for cultivation and better rainfall possibility."
            )


# =====================================
# MARKET PRICE PREDICTION
# =====================================

elif option == "Market Price Prediction":

    st.header("💰 Market Price Prediction")

    st.write("Select your crop details to predict future selling price.")

    commodity_name = st.selectbox(
        "Select Crop",
        [
            "Tomato",
            "Potato",
            "Onion",
            "Rice",
            "Wheat",
            "Maize",
            "Cotton",
            "Sugarcane",
            "Banana",
            "Groundnut"
        ]
    )

    # Commodity mapping
    commodity_dict = {
        "Tomato": 1,
        "Potato": 2,
        "Onion": 3,
        "Rice": 4,
        "Wheat": 5,
        "Maize": 6,
        "Cotton": 7,
        "Sugarcane": 8,
        "Banana": 9,
        "Groundnut": 10
    }

    commodity = commodity_dict[commodity_name]

    min_price = st.number_input(
        "Current Minimum Market Price (₹)",
        min_value=0.0,
        value=1000.0
    )

    max_price = st.number_input(
        "Current Maximum Market Price (₹)",
        min_value=0.0,
        value=2000.0
    )

    st.subheader("Expected Selling Date")

    year = st.number_input(
        "Year",
        min_value=2024,
        max_value=2035,
        value=2026
    )

    month = st.selectbox(
        "Month",
        list(range(1, 13))
    )

    day = st.selectbox(
        "Day",
        list(range(1, 32))
    )

    if st.button("Predict Future Price"):

        predicted_price = predict_price(
            commodity,
            min_price,
            max_price,
            year,
            month,
            day
        )

        st.success(
            f"Predicted Future Price for {commodity_name}: ₹ {predicted_price}"
        )

        st.info(
            "This helps farmers decide the best time to sell their crops "
            "for better profit."
        )


# =====================================
# CROP RECOMMENDATION
# =====================================

elif option == "Crop Recommendation":

    st.header("🌱 Crop Recommendation")

    st.write("Enter soil and weather details to find the best crop.")

    N = st.number_input(
        "Nitrogen Level (N)",
        min_value=0,
        value=90
    )

    P = st.number_input(
        "Phosphorus Level (P)",
        min_value=0,
        value=42
    )

    K = st.number_input(
        "Potassium Level (K)",
        min_value=0,
        value=43
    )

    temperature = st.number_input(
        "Temperature (°C)",
        value=25.0
    )

    humidity = st.number_input(
        "Humidity (%)",
        value=80.0
    )

    ph = st.number_input(
        "Soil pH Value",
        value=6.5
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        value=200.0
    )

    if st.button("Recommend Best Crop"):

        crop_name = recommend_crop(
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        )

        st.success(
            f"Recommended Crop: {crop_name}"
        )

        st.info(
            "This recommendation is based on soil nutrients, rainfall, "
            "temperature, and environmental conditions."
        )


# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.caption("Smart Agriculture using AI | Final Year Project")