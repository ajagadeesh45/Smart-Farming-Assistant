import streamlit as st
import tempfile
import os
import pandas as pd

from utils.weather_api import get_weather_auto
from utils.crop_predict import recommend_crop
from utils.price_predict import predict_price
from utils.disease_predict import predict_disease

# =====================================
# CONFIG
# =====================================
st.set_page_config(page_title="Smart Farming", layout="wide")

# =====================================
# SESSION
# =====================================
if "page" not in st.session_state:
    st.session_state.page = "start"

if "username" not in st.session_state:
    st.session_state.username = ""

if "last_disease" not in st.session_state:
    st.session_state.last_disease = "No scan yet"

# =====================================
# 🎨 CLEAN UI
# =====================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Remove top padding */
.block-container {
    padding-top: 1rem;
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 80px 20px;
}

.hero h1 {
    font-size: 48px;
    color: #1b4332;
}

.hero p {
    font-size: 18px;
    color: #555;
}

/* Button */
.stButton > button {
    background: #2d6a4f;
    color: white;
    border-radius: 10px;
    height: 48px;
    font-size: 16px;
}

/* Cards */
.card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    text-align: center;
    transition: 0.2s;
}

.card:hover {
    transform: scale(1.03);
}

/* Section spacing */
.section {
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 🚀 START PAGE
# =====================================
if st.session_state.page == "start":

    st.markdown("""
    <div class="hero">
        <h1>🌾 Smart Farming Assistant</h1>
        <p>AI-powered platform for crop, price, weather & disease insights</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1,2,1])
    with col:
        if st.button("🚀 Get Started"):
            st.session_state.page = "name"
            st.rerun()

# =====================================
# 👤 NAME PAGE
# =====================================
elif st.session_state.page == "name":

    st.markdown("### 👋 Welcome")

    name = st.text_input("Enter your name")

    if st.button("Continue"):
        if name.strip():
            st.session_state.username = name
            st.session_state.page = "main"
            st.rerun()
        else:
            st.warning("Enter your name")

# =====================================
# 🌾 MAIN APP
# =====================================
elif st.session_state.page == "main":

    st.markdown(f"## 👋 Hello, {st.session_state.username}")

    option = st.sidebar.radio("Menu", [
        "Dashboard",
        "Weather",
        "Crop",
        "Price",
        "Disease"
    ])

    # =====================================
    # DASHBOARD
    # =====================================
    if option == "Dashboard":

        city, temp, wind = get_weather_auto()
        crop = recommend_crop(80, 40, 40, temp, 70, 6.5, 200)
        price = predict_price(1, 1000, 2000, 2026, 6, 15)

        st.markdown("### 📊 Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.markdown(f"<div class='card'>📍 {city}<br>🌡 {temp}°C</div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'>🌾 {crop}</div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='card'>💰 ₹ {price}</div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='card'>🍃 {st.session_state.last_disease}</div>", unsafe_allow_html=True)

    # =====================================
    # WEATHER
    # =====================================
    elif option == "Weather":

        city, temp, wind = get_weather_auto()

        st.markdown("### 🌦 Weather")

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='card'>📍 {city}</div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='card'>🌡 {temp} °C</div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='card'>💨 {wind} km/h</div>", unsafe_allow_html=True)

    # =====================================
    # CROP
    # =====================================
    elif option == "Crop":

        st.markdown("### 🌱 Crop Recommendation")

        col1, col2 = st.columns(2)

        soil = col1.selectbox("Soil", ["Red", "Black", "Clay", "Sandy", "Loamy"])
        water = col2.selectbox("Water", ["Low", "Medium", "High"])

        if st.button("Recommend"):
            crop = recommend_crop(80, 40, 40, 28, 70, 6.5, 200)
            st.success(crop)

    # =====================================
    # PRICE
    # =====================================
    elif option == "Price":

        st.markdown("### 💰 Price Prediction")

        price = predict_price(1, 1000, 2000, 2026, 6, 15)
        st.success(f"₹ {price}")

        df = pd.DataFrame({
            "Day": range(1, 11),
            "Price": [1200,1300,1250,1400,1500,1450,1600,1700,1650,1800]
        })

        st.line_chart(df.set_index("Day"))

    # =====================================
    # DISEASE
    # =====================================
    elif option == "Disease":

        st.markdown("### 🍃 Disease Detection")

        file = st.file_uploader("Upload Image")

        if file:
            st.image(file)

            if st.button("Detect"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(file.read())
                    path = tmp.name

                name, conf = predict_disease(path)
                st.session_state.last_disease = name

                st.success(name)
                os.remove(path)