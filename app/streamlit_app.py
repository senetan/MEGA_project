import streamlit as st
st.set_page_config(page_title="MEGA Predictor", layout="centered")

import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
import os
from datetime import datetime
from models import load_model, load_pipeline, load_target_scaler

# === Chargement des artefacts
model = load_model()
pipeline = load_pipeline()
scaler = load_target_scaler()

# === Titre
st.title("🔋 MEGA - Prédiction de la consommation énergétique")

st.markdown("Saisissez la date, l'heure et les productions par énergie pour estimer la consommation.")

# === Formulaire utilisateur

col1, col2 = st.columns(2)

with col1:
    date_input = st.date_input("📅 Date", datetime.today())
with col2:
    hour_input = st.number_input("🕐 Heure (0-23)", min_value=0, max_value=23, step=1)

# === Énergies (à adapter selon ton modèle)
energy_inputs = {}
st.subheader("⚡️ Production par source d'énergie")

energy_features = [
    "powerConsumptionBreakdown.nuclear",
    "powerConsumptionBreakdown.geothermal",
    "powerConsumptionBreakdown.biomass",
    "powerConsumptionBreakdown.coal",
    "powerConsumptionBreakdown.wind",
    "powerConsumptionBreakdown.solar",
    "powerConsumptionBreakdown.hydro",
    "powerConsumptionBreakdown.gas",
    "powerConsumptionBreakdown.oil"
]

for feature in energy_features:
    energy_inputs[feature] = st.number_input(f"{feature}", min_value=0.0, value=100.0, step=100.0)

# === Lancer la prédiction
if st.button("Prédire la consommation"):
    try:
        input_dict = {**energy_inputs}
        input_df = pd.DataFrame([input_dict])

        # Ajouter la colonne datetime
        datetime_str = f"{date_input.strftime('%Y-%m-%d')} {hour_input:02d}:00:00"
        input_df["datetime"] = pd.to_datetime(datetime_str)

        # Prétraitement et prédiction
        X = pipeline.transform(input_df)
        y_scaled = model.predict(X)
        y = scaler.inverse_transform(y_scaled.reshape(-1, 1))

        st.success(f"🔮 Consommation estimée : {y[0][0]:,.2f} MW")

    except Exception as e:
        st.error(f"❌ Erreur de prédiction : {str(e)}")
