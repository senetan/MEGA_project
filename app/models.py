import os
import numpy as np
import joblib
import tensorflow as tf
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Chemins des artefacts ===
MODEL_PATH = os.getenv("MODEL_PATH", "models/MEGA_model.keras")
PIPELINE_PATH = os.getenv("PIPELINE_PATH", "models/features_pipeline.pkl")
TARGET_SCALER_PATH = os.getenv("TARGET_SCALER", "models/target_scaler.pkl")

# === Chargement des artefacts ===

def load_model(model_path: str = MODEL_PATH):
    try:
        logger.info(f"Chargement du modèle depuis {model_path}")
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        logger.error(f"Erreur chargement modèle : {e}")
        raise

def load_pipeline(pipeline_path: str = PIPELINE_PATH):
    try:
        logger.info(f"Chargement du pipeline depuis {pipeline_path}")
        return joblib.load(pipeline_path)
    except Exception as e:
        logger.error(f"Erreur chargement pipeline : {e}")
        raise

def load_target_scaler(scaler_path: str = TARGET_SCALER_PATH):
    try:
        logger.info(f"Chargement du target scaler depuis {scaler_path}")
        return joblib.load(scaler_path)
    except Exception as e:
        logger.error(f"Erreur chargement scaler : {e}")
        raise

# === Fonction de prédiction ===

def predict(input_array: np.ndarray) -> float:
    """
    input_array : np.array de forme (1, n_features)
    Retourne une prédiction float déscalée.
    """
    try:
        model = load_model()
        pipeline = load_pipeline()
        scaler = load_target_scaler()

        logger.info(f"Input brut : {input_array}")
        processed = pipeline.transform(input_array)
        prediction_scaled = model.predict(processed)
        prediction = scaler.inverse_transform(prediction_scaled.reshape(-1, 1))

        return float(prediction[0][0])
    except Exception as e:
        logger.error(f"Erreur de prédiction : {e}")
        raise
