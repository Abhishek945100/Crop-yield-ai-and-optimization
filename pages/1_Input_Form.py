import streamlit as st
from src.weather_service import get_real_weather, get_live_environment
import requests
import random

st.markdown("""
<style>

/* Remove header */
header {visibility: hidden;}

/* Remove deploy + 3 dot */
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {display: none !important;}

/* Remove top gap */
.block-container {
    padding-top: 0rem !important;
}

/* Keep background same */
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #0b1f33 100%);
}

</style>
""", unsafe_allow_html=True)
# Cursor fix
st.markdown("""
<style>
div[data-baseweb="select"] * {
    cursor: pointer !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📥 Farmer Input Form")

# =========================
# 👨‍🌾 Farmer Profile
# =========================
st.subheader("👨‍🌾 Farmer Profile")

farmer_name = st.text_input("Farmer Name")
# =========================
# 🌍 Land Size with Unit Conversion
# =========================

land_unit = st.selectbox(
    "Select Land Unit",
    ["Acre", "Bigha"]
)

land_input = st.number_input("Enter Land Size", min_value=0.1)

# 🔄 Conversion to Acre
if land_unit == "Acre":
    land_size = land_input
else:
    # 1 Bigha = 0.62 Acre (approx)
    land_size = land_input * 0.62
    st.info(f"Converted Land Size (in Acre): {round(land_size, 2)}")


irrigation = st.selectbox("Irrigation", ["Low", "Medium", "High"])
budget = st.selectbox("Budget", ["Low", "Medium", "High"])

# =========================
# 🌾 Crop Season Selection
# =========================
st.subheader("🌾 Crop Season Selection")

season = st.selectbox("Crop Category", ["Rabi", "Kharif", "Zaid"])

crop_map = {
    "Rabi": ["wheat", "barley", "gram", "mustard"],
    "Kharif": ["rice", "maize", "cotton", "soybean"],
    "Zaid": ["watermelon", "muskmelon", "cucumber"]
}

previous_crop = st.radio(
    "Select Previous Crop",
    crop_map[season],
    horizontal=True
)

# =========================
# 🌦️ Environment
# =========================
st.subheader("🌦️ Environment")

city = st.text_input("🌍 Enter City", "Kanpur")

# =========================
# 🔥 ADD THIS BLOCK (STATE FIX)
# =========================

state_city_map = {
    "Punjab": ["Ludhiana", "Amritsar"],
    "Haryana": ["Karnal", "Hisar"],
    "Uttar Pradesh": ["Kanpur"],
    "Rajasthan": ["Jaipur", "Kota"],
    "Maharashtra": ["Nagpur"],
    "Tamil Nadu": ["Chennai"],
    "Karnataka": ["Bangalore", "Mysore"],
    "Madhya Pradesh": ["Indore", "Bhopal"],
    "Gujarat": ["Ahmedabad"],
    "Andhra Pradesh": ["Guntur"]
}

selected_state = None

for s, cities in state_city_map.items():
    if city.strip().title() in cities:
        selected_state = s
        break

# fallback if not detected
if selected_state is None:
    selected_state = "Uttar Pradesh"


rainfall = st.number_input("Rainfall (mm)", min_value=0.0)

weather_mode = st.radio(
    "Weather Input Mode",
    ["Manual", "Simulation", "Real API"],
    horizontal=True
)

# -------- WEATHER MODES --------
if weather_mode == "Real API":
    if city.strip() == "":
        st.warning("Please enter a valid city name")
        humidity, sunshine = 60.0, 6.0
    else:
        try:
            weather = get_real_weather(city)

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(weather.get("humidity", 60))
            )

            sunshine = st.number_input(
                "Sunshine (hours/day)",
                min_value=0.0,
                value=float(weather.get("sunshine", 6))
            )

            st.success("Weather fetched successfully")

        except:
            st.warning("API failed → using default values")
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
            sunshine = st.number_input("Sunshine (hours/day)", min_value=0.0, value=6.0)

elif weather_mode == "Simulation":

    # 🔥 Deterministic simulation 

    seed_str = f"{city}-{season}"
    random.seed(seed_str)

    def vary(val, pct=0.1):
        delta = val * pct
        return round(val + random.uniform(-delta, delta), 2)

    # Base values
    base_humidity = 65
    base_sunshine = 7

    # Season effect
    season_factor = {
        "Rabi": 0.8,
        "Kharif": 1.2,
        "Zaid": 1.0
    }

    sf = season_factor.get(season, 1.0)

    sim_humidity = vary(base_humidity * sf)
    sim_sunshine = max(4, vary(base_sunshine * sf))

    # ✅ IMPORTANT: use separate variables first
    humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=sim_humidity
    )

    sunshine = st.number_input(
    "Sunshine (hours/day)",
    min_value=1.0,
    max_value=12.0,
    value=float(sim_sunshine),   # 🔥 THIS LINE IS KEY
    step=0.1
)

# 🔥 Custom warning (like your UI)
    if sunshine > 12:
        st.error("⚠ Sunshine cannot exceed 12 hours/day")

else:
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0)
    sunshine = st.number_input("Sunshine (hours/day)", min_value=0.0,max_value=12.00)

# =========================
# 🌱 Soil Health
# =========================
st.subheader("🌱 Soil Health")

soil_mode = st.radio(
    "Soil Data Input Mode",
    ["Manual", "Simulated", "API"],
    horizontal=True
)

# -------- SOIL MODES --------
if soil_mode == "Manual":
    st.info("Enter soil values manually (based on soil testing reports)")

    nitrogen = st.number_input("Nitrogen (kg/acre)", min_value=0.0)
    phosphorus = st.number_input("Phosphorus (kg/acre)", min_value=0.0)
    potassium = st.number_input("Potassium (kg/acre)", min_value=0.0)
    ph = st.number_input("Soil pH (0–14 scale)", min_value=0.0, max_value=14.0)
    moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0)

elif soil_mode == "Simulated":
    st.info("Data generated using soil type + season + region")

    soil_type = st.selectbox(
        "Soil Type",
        ["Alluvial", "Black", "Red", "Laterite", "Desert", "Mountain"]
    )

    # 🔹 Base values
    soil_data = {
        "Alluvial": (50, 40, 35, 6.5, 30),
        "Black": (60, 35, 40, 7.0, 35),
        "Red": (45, 30, 25, 6.0, 25),
        "Laterite": (40, 25, 20, 5.5, 20),
        "Desert": (20, 15, 10, 7.5, 10),
        "Mountain": (35, 28, 22, 6.2, 18)
    }

    base = soil_data[soil_type]

    # 🔥 Deterministic seed (same input → same output)
    seed_str = f"{soil_type}-{season}-{city}"
    random.seed(seed_str)

    # 🔥 Controlled variation
    def vary(val, pct=0.1):
        delta = val * pct
        return round(val + random.uniform(-delta, delta), 2)

    # 🔥 Season impact
    season_factor = {
        "Rabi": 0.9,
        "Kharif": 1.1,
        "Zaid": 1.0
    }

    sf = season_factor[season]

    nitrogen = vary(base[0] * sf)
    phosphorus = vary(base[1] * sf)
    potassium = vary(base[2] * sf)
    ph = vary(base[3], 0.05)
    moisture = vary(base[4], 0.15)

    st.success(
        f"Estimated → N:{nitrogen}, P:{phosphorus}, K:{potassium}, pH:{ph}, Moisture:{moisture}"
    )

elif soil_mode == "API":
    st.info("Fetching soil data from API")

    try:
        response = requests.get("https://api.mocksoil.com/data", timeout=5)
        data = response.json()

        nitrogen = float(data.get("nitrogen", 50))
        phosphorus = float(data.get("phosphorus", 40))
        potassium = float(data.get("potassium", 30))
        ph = float(data.get("ph", 6.5))
        moisture = float(data.get("moisture", 30))

        st.success("Soil data fetched from API")

    except:
        st.warning("⚠ API failed → using default values")
        nitrogen, phosphorus, potassium, ph, moisture = 50.0, 40.0, 30.0, 6.5, 30.0

# =========================
# 💾 VALIDATION + STORE
# =========================

submit = st.button("Submit Data")

if submit:

    errors = []

    # 👨‍🌾 Farmer Profile
    if farmer_name.strip() == "":
        errors.append("Farmer Name is required")

    if land_size <= 0:
        errors.append("Land size must be greater than 0")

    # 🌾 Crop
    if previous_crop is None:
        errors.append("Select previous crop")

    # 🌦️ Environment
    if rainfall <= 0:
        errors.append("Rainfall must be greater than 0")

    if humidity <= 0:
        errors.append("Humidity must be greater than 0")

    if sunshine <= 0:
        errors.append("Sunshine must be greater than 0")

    # 🌱 Soil
    if soil_mode == "Manual":
        if nitrogen <= 0:
            errors.append("Nitrogen value required")
        if phosphorus <= 0:
            errors.append("Phosphorus value required")
        if potassium <= 0:
            errors.append("Potassium value required")

    #  SHOW ALL ERRORS
    if len(errors) > 0:
        for err in errors:
            st.error(f"{err}")

    # ✅ STORE DATA
    else:
        st.session_state["input_data"] = {
    "farmer_name": farmer_name,
    "land_size": land_size,
    "irrigation": irrigation,
    "budget": budget,
    "season": season,
    "previous_crop": previous_crop,

    # 🔥 ADD THESE 2 LINES
    "state": selected_state,
    "city": city,

    "rainfall": rainfall,
    "humidity": humidity,
    "sunshine": sunshine,
    "nitrogen": nitrogen,
    "phosphorus": phosphorus,
    "potassium": potassium,
    "ph": ph,
    "moisture": moisture
}
        st.success("✅ All data validated & saved successfully!")