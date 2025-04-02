import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib
import logging

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Exemple de configuration (à adapter selon ton projet)
NUMERICAL_FEATURES = ["feature_1", "feature_2"]
CATEGORICAL_FEATURES = ["feature_3"]

# === Pipeline de traitement ===

def build_preprocessing_pipeline():
    logger.info("Construction du pipeline de prétraitement...")

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, NUMERICAL_FEATURES),
        ("cat", categorical_pipeline, CATEGORICAL_FEATURES)
    ])

    return preprocessor

# === Entraîner et sauvegarder le pipeline ===

def fit_and_save_pipeline(df: pd.DataFrame, output_path: str = "models/features_pipeline.pkl"):
    try:
        logger.info("Entraînement du pipeline de prétraitement...")
        pipeline = build_preprocessing_pipeline()
        pipeline.fit(df)
        joblib.dump(pipeline, output_path)
        logger.info(f"Pipeline sauvegardé à {output_path}")
    except Exception as e:
        logger.error(f"Erreur entraînement/sauvegarde pipeline : {e}")
        raise

# === Charger le pipeline ===

def load_pipeline(path: str = "models/features_pipeline.pkl"):
    try:
        logger.info(f"Chargement du pipeline depuis {path}")
        return joblib.load(path)
    except Exception as e:
        logger.error(f"Erreur chargement pipeline : {e}")
        raise
