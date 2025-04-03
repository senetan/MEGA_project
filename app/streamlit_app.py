import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://api:8000/predict")

st.set_page_config(
    page_title="MEGA - Energy Consumption Prediction",
    page_icon="🔋",
    layout="centered"
)

st.title("🔋 MEGA - Energy Consumption Prediction")
st.markdown("Enter the date, hour, and energy production values to get a prediction.")

# User input form
with st.form("prediction_form"):
    date = st.date_input("📅 Date")
    hour = st.slider("🕐 Hour (0-23)", min_value=0, max_value=23, step=1)

    st.markdown("---")
    st.markdown("### ⚡️ Energy production by source")

    nuclear = st.number_input("Nuclear (MW)", min_value=0.0, value=100.0)
    geothermal = st.number_input("Geothermal (MW)", min_value=0.0, value=10.0)
    biomass = st.number_input("Biomass (MW)", min_value=0.0, value=100.0)
    coal = st.number_input("Coal (MW)", min_value=0.0, value=100.0)
    wind = st.number_input("Wind (MW)", min_value=0.0, value=100.0)
    solar = st.number_input("Solar (MW)", min_value=0.0, value=100.0)
    hydro = st.number_input("Hydropower (MW)", min_value=0.0, value=100.0)
    gas = st.number_input("Gas (MW)", min_value=0.0, value=100.0)
    oil = st.number_input("Oil (MW)", min_value=0.0, value=100.0)

    submitted = st.form_submit_button("🚀 Predict Consumption")

# Submission logic
if submitted:
    datetime_iso = datetime.combine(date, datetime.min.time()).replace(hour=hour).isoformat()

    payload = {
        "datetime": datetime_iso + "Z",
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

    st.markdown("📤 Payload sent to the API:")
    st.json(payload)

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        st.success(f"🎯 Predicted Carbon Intensity: {result['predicted_carbon_intensity']}")

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error: {http_err} - {response.text}")

    except Exception as err:
        st.error(f"Unexpected error: {err}")
