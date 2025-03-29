from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import os
import joblib
import tensorflow as tf
from dotenv import load_dotenv
from google.cloud import bigquery, storage
import __main__

__main__.pd = pd
__main__.np = np

# Load environment variables
load_dotenv()

project_id = os.getenv("GCP_PROJECT")
bucket_name = os.getenv("BUCKET_NAME")
dataset_path = os.getenv("DATASET")
gac_key = os.getenv("GAC_KEY")

# Function to load dataset from BigQuery
def load_dataset_from_gcp():
    client = storage.Client.from_service_account_json(gac_key)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(dataset_path)  # Use dataset path from the .env file
    local_path = "/root/code/senetan/MEGA_project/raw_data_gcp/temp_dataset.csv"
    blob.download_to_filename(local_path)
    return pd.read_csv(local_path)

# Load model and pipeline
def load_model():
    return {
        "model": tf.keras.models.load_model(os.getenv("MODEL_PATH")),
        "features_pipeline": joblib.load(os.getenv("PIPELINE_PATH")),
        "target_scaler": joblib.load(os.getenv("TARGET_SCALER")),
    }

model = load_model()

# FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome on the MEGA API!"}

class PredictionInput(BaseModel):
    datetime: str = Field(..., example="2025-04-12T12:00:00.000Z")
    powerConsumptionBreakdown_nuclear: float = Field(..., example=50)
    powerConsumptionBreakdown_geothermal: float = Field(..., example=10)
    powerConsumptionBreakdown_biomass: float = Field(..., example=100)
    powerConsumptionBreakdown_coal: float = Field(..., example=200)
    powerConsumptionBreakdown_wind: float = Field(..., example=300)
    powerConsumptionBreakdown_solar: float = Field(..., example=20)
    powerConsumptionBreakdown_hydro: float = Field(..., example=400)
    powerConsumptionBreakdown_gas: float = Field(..., example=150)
    powerConsumptionBreakdown_oil: float = Field(..., example=30)

@app.post("/predict")
def predict(input_data: PredictionInput):
    data = input_data.model_dump()
    for key in list(data.keys()):
        if "powerConsumptionBreakdown_" in key:
            data[key.replace("_", ".")] = data.pop(key)
    sample_df = pd.DataFrame([data])
    sample_features = model["features_pipeline"].transform(sample_df)
    pred_scaled = model["model"].predict(sample_features)
    pred = model["target_scaler"].inverse_transform(pred_scaled)
    return {"predicted_carbon_intensity": f"{float(pred[0][0])} gCO2eq/kWh"}

# === Ajouts minimal pour Streamlit ===

def load_model_and_pipeline():
    """
    Fonction d'accès pour Streamlit : retourne le modèle, le pipeline et le scaler.
    """
    return model["model"], model["features_pipeline"], model["target_scaler"]

def predict_from_dict(input_data: dict):
    """
    Version Streamlit : prend un dictionnaire au lieu d'un objet Pydantic.
    """
    try:
        formatted_data = {
            key.replace("_", "."): value for key, value in input_data.items()
        }
        df = pd.DataFrame([formatted_data])
        X = model["features_pipeline"].transform(df)
        y_scaled = model["model"].predict(X)
        y_pred = model["target_scaler"].inverse_transform(y_scaled)
        return {
            "predicted_carbon_intensity": f"{float(y_pred[0][0]):.2f} gCO2eq/kWh"
        }
    except Exception as e:
        return {"error": str(e)}

# === Lancement de l'API ===

def main():
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))

if __name__ == "__main__":
    main()
