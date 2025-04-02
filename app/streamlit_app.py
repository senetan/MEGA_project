import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from app.models import load_model_and_scalers
from app.preproc import preprocess_data  # À adapter selon ton fichier
from app.params import FEATURES  # Liste de variables en entrée si existante

# Configuration de la page
st.set_page_config(
    page_title="MEGA Predictor",
    page_icon="🤖",
    layout="centered"
)

st.title("💡 MEGA Project — Prédiction intelligente")

# Chargement des assets ML
@st.cache_resource
def load_assets():
    model, pipeline, target_scaler = load_model_and_scalers()
    return model, pipeline, target_scaler

model, pipeline, target_scaler = load_assets()

# UI — Saisie utilisateur
st.subheader("Entrez les données à prédire")
user_input = {}

for feature in FEATURES:
    val = st.text_input(f"{feature}", "")
    user_input[feature] = val

# Bouton de prédiction
if st.button("Prédire"):
    try:
        # Convertir l'entrée en DataFrame
        input_df = pd.DataFrame([user_input])

        # Prétraitement
        X = preprocess_data(input_df, pipeline)

        # Prédiction
        prediction = model.predict(X)
        prediction = target_scaler.inverse_transform(prediction.reshape(-1, 1))[0][0]

        # Affichage
        st.success(f"🎯 Prédiction du modèle : **{prediction:.2f}**")

    except Exception as e:
        st.error(f"❌ Erreur lors de la prédiction : {e}")
