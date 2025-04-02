from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import tensorflow as tf
import os
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Chargement des chemins depuis l'environnement ou valeurs par défaut ===
MODEL_PATH = os.getenv("MODEL_PATH", "models/MEGA_model.keras")
PIPELINE_PATH = os.getenv("PIPELINE_PATH", "models/features_pipeline.pkl")
TARGET_SCALER_PATH = os.getenv("TARGET_SCALER", "models/target_scaler.pkl")

# === Chargement des artefacts ===
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    pipeline = joblib.load(PIPELINE_PATH)
    target_scaler = joblib.load(TARGET_SCALER_PATH)
    logger.info("Modèle, pipeline et scaler chargés avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement des artefacts : {e}")
    raise

# === Initialisation de l'application FastAPI ===
app = FastAPI(
    title="MEGA API",
    description="API de prédiction pour le projet MEGA",
    version="1.0"
)

# === Schéma de données d'entrée (à adapter à ton pipeline réel) ===
class InputData(BaseModel):
    feature_1: float
    feature_2: float
    feature_3: float
    # 🔁 Ajoute tous les features nécessaires ici

# === Route d'accueil ===
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API MEGA 🚀"}

# === Route de prédiction ===
@app.post("/predict")
def predict(data: InputData):
    try:
        input_dict = data.dict()
        logger.info(f"Données reçues pour prédiction : {input_dict}")

        # Mise en forme et traitement
        input_array = np.array([list(input_dict.values())])
        processed_input = pipeline.transform(input_array)
        prediction_scaled = model.predict(processed_input)
        prediction = target_scaler.inverse_transform(prediction_scaled.reshape(-1, 1))

        return {"prediction": float(prediction[0][0])}
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne lors de la prédiction.")
