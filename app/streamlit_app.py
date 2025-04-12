import streamlit as st
import datetime
import requests
import math
from PIL import Image
from datetime import timedelta

# Streamlit page configuration
st.set_page_config(
    page_title="Optimize EV charging for carbon - Predicted carbon intensity :germany_flag:next week",
    page_icon="🌍",
    layout="centered"
)

# API URL
API_URL = "https://mega-api-2yzrud7e4q-od.a.run.app"

# ✨ Set dynamic datetime boundaries
now = datetime.datetime.now()
earliest_valid_date = (now + datetime.timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
latest_valid_date = (now + datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)

# Page title
st.title("Make EVs Great Again (MEGA) tool: optimize for carbon")
st.markdown("Welcome to the **EV charging Carbon Intensity Predictor** 🌱. Choose a day and time next week and get an instant forecast!")

st.sidebar.markdown("## 📅 Select Date and Time")

# Date input in sidebar
selected_date = st.sidebar.date_input(
    "Date",
    value=earliest_valid_date.date(),
    min_value=earliest_valid_date.date(),
    max_value=latest_valid_date.date()
)

# Time input in sidebar
selected_time = st.sidebar.time_input(
    "Time",
    value=datetime.time(12, 0)
)

# Combine into a datetime object
datetime_obj = datetime.datetime.combine(selected_date, selected_time)
datetime_input = datetime_obj.isoformat()

st.sidebar.markdown(f"🕒 Selected datetime (ISO 8601): `{datetime_input}`")

# Energy simulation based on the hour
def simulate_production(dt):
    hour = dt.hour + dt.minute / 60
    solar = max(0, math.sin((hour - 6) / 12 * math.pi)) * 800
    wind = 3000 + 1500 * math.sin((hour / 24) * 2 * math.pi)
    nuclear = 900
    geothermal = 100
    biomass = 200
    coal = 400 + 100 * math.sin((hour / 24) * 2 * math.pi + 1)
    hydro = 300 + 100 * math.cos((hour / 24) * 2 * math.pi)
    gas = 250 + 50 * math.sin((hour / 24) * 2 * math.pi + 2)
    oil = 50 + 20 * math.sin((hour / 24) * 2 * math.pi + 3)

    return {
        "powerConsumptionBreakdown_nuclear": nuclear,
        "powerConsumptionBreakdown_geothermal": geothermal,
        "powerConsumptionBreakdown_biomass": biomass,
        "powerConsumptionBreakdown_coal": coal,
        "powerConsumptionBreakdown_wind": wind,
        "powerConsumptionBreakdown_solar": solar,
        "powerConsumptionBreakdown_hydro": hydro,
        "powerConsumptionBreakdown_gas": gas,
        "powerConsumptionBreakdown_oil": oil,
    }

st.markdown("---")

# Predict button for carbon intensity
if st.button("🔮 Predict Carbon Intensity"):
    with st.spinner("⏳ Sending request to the prediction API..."):
        energy_data = simulate_production(datetime_obj)
        energy_data["datetime"] = datetime_input
        try:
            response = requests.post(f"{API_URL}/predict", json=energy_data)

            if response.text:
                result = response.json()
                predicted_value = float(result["predicted_carbon_intensity"].split()[0])
                st.success(f"🌱 Predicted Carbon Intensity: {predicted_value:.2f} gCO₂eq/kWh")
            else:
                st.error("Empty response received from the API.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to get prediction: {e}")
        except ValueError:
            st.error("Error decoding JSON or parsing prediction.")

# ✨ Smart Pick Section: Show top 5 greenest hours (once per session)
@st.cache_data
def get_best_low_carbon_slots():
    best_slots = []
    current = earliest_valid_date

    while current < latest_valid_date:
        if 6 <= current.hour < 22:
            energy_data = simulate_production(current)
            energy_data["datetime"] = current.isoformat()

            try:
                response = requests.post(f"{API_URL}/predict", json=energy_data)
                if response.ok and response.text:
                    result = response.json()
                    predicted_value = float(result["predicted_carbon_intensity"].split()[0])
                    best_slots.append((current, predicted_value))
            except:
                pass
        current += timedelta(hours=1)

    best_slots.sort(key=lambda x: x[1])
    return best_slots[:5]

st.markdown("### ⚡ Smart Pick: Best Charging Times This Week")

top_5 = get_best_low_carbon_slots()
for dt, val in top_5:
    st.markdown(f"✅ **{dt.strftime('%A %d %B – %H:%M')}** → {val:.2f} gCO₂eq/kWh")

# QR Code
qr_img = Image.open("app/streamlit_qr.png")
st.image(qr_img, caption="Scan to open this app on your phone 📱")

# Google Slides presentation
st.markdown("### 📽️ MEGA Project Presentation")

st.markdown("""
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vTeb2weY1ffOABXNc2SJUpXyxNNTJ0GDX3g8CfEPOIwYipc1MCAfI-8m6b9LQgbtw/pubembed?start=true&loop=false&delayms=3000"
frameborder="0" width="100%" height="600" scrolling="no" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
""", unsafe_allow_html=True)
