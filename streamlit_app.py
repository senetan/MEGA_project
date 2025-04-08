import streamlit as st
import datetime
import requests
import math

# Streamlit page configuration
st.set_page_config(page_title="Carbon intensity Prediction", page_icon="🌍", layout="centered")

# API URL
API_URL = "https://mega-api-2yzrud7e4q-od.a.run.app"

# Page title
st.title("🌍 Carbon intensity Prediction")
st.markdown("Welcome to the **Carbon Intensity Predictor** 🌱. Choose your energy parameters and get an instant forecast!")

# Date and time selection
with st.expander("📅 Select Date and Time", expanded=True):
    col1, col2 = st.columns(2)

    # Date input
    with col1:

        date_input = st.date_input("Date", value=datetime.date.today())

    # Time input
    with col2:
        default_time = datetime.time(12, 0)
        time_input = st.time_input("Time", value=default_time)

    # Combiner date + heure
    datetime_obj = datetime.datetime.combine(date_input, time_input)
    datetime_input = datetime_obj.isoformat()
    st.markdown(f"🕒 Selected datetime (ISO 8601): `{datetime_input}`")

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
