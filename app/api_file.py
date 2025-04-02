from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import os
import joblib
import tensorflow as tf
from dotenv import load_dotenv
from google.cloud import bigquery,storage
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
        "model": tf.keras.models.load_model(
            os.getenv("MODEL_PATH"),
        ),
        "features_pipeline": joblib.load(os.getenv("PIPELINE_PATH")),
        "target_scaler": joblib.load(os.getenv("TARGET_SCALER")),
    }

model= load_model()

# FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome on the MEGA API!"}

class PredictionInput(BaseModel):
    """
    Input data model for carbon intensity prediction.

    This model defines the structure of the data that the user must provide
    to make a prediction via the API. It includes different energy sources
    and the date/time at which the prediction should be made.

    Attributes:
        datetime (str): The date and time of the prediction in ISO 8601 format.
        powerConsumptionBreakdown_nuclear (float): Nuclear energy consumption.
        powerConsumptionBreakdown_geothermal (float): Geothermal energy consumption.
        powerConsumptionBreakdown_biomass (float): Biomass energy consumption.
        powerConsumptionBreakdown_coal (float): Coal energy consumption.
        powerConsumptionBreakdown_wind (float): Wind energy consumption.
        powerConsumptionBreakdown_solar (float): Solar energy consumption.
        powerConsumptionBreakdown_hydro (float): Hydroelectric energy consumption.
        powerConsumptionBreakdown_gas (float): Gas energy consumption.
        powerConsumptionBreakdown_oil (float): Oil energy consumption.
    """
    datetime: str = Field(
        ...,
        example="2025-04-12T12:00:00.000Z"
    )
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

    # Rename keys to match the model's expected format
    for key in list(data.keys()):
        if "powerConsumptionBreakdown_" in key:
                data[key.replace("_", ".")] = data.pop(key)

    # Prepare data
    sample_df = pd.DataFrame([data])
    sample_features = model["features_pipeline"].transform(sample_df)

    # Prediction
    pred_scaled = model["model"].predict(sample_features)
    pred = model["target_scaler"].inverse_transform(pred_scaled)


    return {"predicted_carbon_intensity": f"{float(pred[0][0])} gCO2eq/kWh"}

def main():
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))

if __name__ == "__main__":
    main()
