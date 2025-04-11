import streamlit as st
import datetime
import requests
import math

# Streamlit page configuration
st.set_page_config(page_title="Optimize EV charging for carbon - Predicted carbon intensity :germany_flag:next week", page_icon="🌍", layout="centered")

# API URL
API_URL = "https://mega-api-2yzrud7e4q-od.a.run.app"

# Define the known last date of data (31/12/2023)
last_date = datetime.datetime(2025, 3, 15)

# Define the earliest valid date (1st January 2024)
earliest_valid_date = datetime.datetime(2025, 4, 11)

# Define the latest valid date (7th January 2024)
latest_valid_date = datetime.datetime(2025, 4, 18)

# Page title
st.title("Optimize EV charging for carbon - Predicted carbon intensity next week")
st.markdown("Welcome to the **Carbon Intensity Predictor** 🌱. Choose your energy parameters and get an instant forecast!")

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

# Calculate the difference in days between the selected date and the last known date (31/12/2023)
days_difference = (selected_date - last_date.date()).days
st.sidebar.write(f"📆 Days from 10/04/2025: {days_difference} days")

# Energy simulation based on the hour
def simulate_production(dt):
    """Returns an estimate of energy production at a given hour"""
    hour = dt.hour + dt.minute / 60

    # Very simple models based on the daily cycle
    solar = max(0, math.sin((hour - 6) / 12 * math.pi)) * 800  # Peak around noon
    wind = 3000 + 1500 * math.sin((hour / 24) * 2 * math.pi)   # Oscillation over 24 hours
    nuclear = 900  # stable
    geothermal = 100  # stable
    biomass = 200  # stable
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
