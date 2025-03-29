# === app.py ===

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# ✅ Doit être ici AVANT toute commande st.
st.set_page_config(page_title="MEGA - Prédiction CO2", layout="centered")

# Ajout du dossier contenant la logique
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "MEGA_project_folder")))

from MEGA_project_folder.api_file import load_model_and_pipeline, predict_from_dict as api_predict

# === Titre ===
st.title("🌍 MEGA — Prédiction d’intensité carbone")
st.markdown("Bienvenue dans l’interface de prédiction du projet **MEGA**.\nRemplis les champs ci-dessous et clique sur **Prédire** pour obtenir l’intensité carbone prévue.")

# === Chargement du modèle et pipeline ===
@st.cache_resource
def load_assets():
    return load_model_and_pipeline()

model, pipeline, scaler = load_assets()

# === Formulaire utilisateur ===
st.header("📝 Données d’entrée")

with st.form(key="prediction_form"):
    datetime = st.text_input("Date & Heure (format ISO)", value="2025-04-12T12:00:00.000Z")

    st.subheader("⚡ Répartition de la consommation énergétique (en MW)")
    col1, col2, col3 = st.columns(3)
    with col1:
        nuclear = st.number_input("Nucléaire", value=50.0)
        geothermal = st.number_input("Géothermie", value=10.0)
        biomass = st.number_input("Biomasse", value=100.0)
    with col2:
        coal = st.number_input("Charbon", value=200.0)
        wind = st.number_input("Éolien", value=300.0)
        solar = st.number_input("Solaire", value=20.0)
    with col3:
        hydro = st.number_input("Hydraulique", value=400.0)
        gas = st.number_input("Gaz", value=150.0)
        oil = st.number_input("Pétrole", value=30.0)

    submit_button = st.form_submit_button(label="🔮 Prédire")

# === Prédiction ===
if submit_button:
    input_data = {
        "datetime": datetime,
        "powerConsumptionBreakdown_nuclear": nuclear,
        "powerConsumptionBreakdown_geothermal": geothermal,
        "powerConsumptionBreakdown_biomass": biomass,
        "powerConsumptionBreakdown_coal": coal,
        "powerConsumptionBreakdown_wind": wind,
        "powerConsumptionBreakdown_solar": solar,
        "powerConsumptionBreakdown_hydro": hydro,
        "powerConsumptionBreakdown_gas": gas,
        "powerConsumptionBreakdown_oil": oil
    }

    with st.spinner("Prédiction en cours..."):
        prediction_result = api_predict(input_data)
        if "error" in prediction_result:
            st.error(f"❌ Erreur : {prediction_result['error']}")
        else:
            st.success(f"✅ Intensité carbone prédite : {prediction_result['predicted_carbon_intensity']}")
