from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline
from MEGA_project_folder.utils import extract_time_energy_features
import tensorflow as tf
import pickle
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
PIPELINE_PATH = os.getenv("PIPELINE_PATH")
# Load the model and the pipeline
model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={'extract_time_energy_features': extract_time_energy_features}
)
with open(PIPELINE_PATH, 'rb') as file:
    model_and_pipeline = pickle.load(file)

features_pipeline = model_and_pipeline['features_pipeline']
target_scaler = model_and_pipeline['target_scaler']

# FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome on the MEGA API!"}

class PredictionInput(BaseModel):
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
    try:
        data = input_data.model_dump()
        mapping = {
        "powerConsumptionBreakdown_nuclear": "powerConsumptionBreakdown.nuclear",
        "powerConsumptionBreakdown_geothermal": "powerConsumptionBreakdown.geothermal",
        "powerConsumptionBreakdown_biomass": "powerConsumptionBreakdown.biomass",
        "powerConsumptionBreakdown_coal": "powerConsumptionBreakdown.coal",
        "powerConsumptionBreakdown_wind": "powerConsumptionBreakdown.wind",
        "powerConsumptionBreakdown_solar": "powerConsumptionBreakdown.solar",
        "powerConsumptionBreakdown_hydro": "powerConsumptionBreakdown.hydro",
        "powerConsumptionBreakdown_gas": "powerConsumptionBreakdown.gas",
        "powerConsumptionBreakdown_oil": "powerConsumptionBreakdown.oil"
        }

        for k, v in mapping.items():
            data[v] = data.pop(k)

    # Create a DataFrame from the input data
        sample_df = pd.DataFrame([data])
    # Transformation with the pipeline
        sample_features = features_pipeline.transform(sample_df)

    # Prediction with the model
        pred_scaled = model.predict(sample_features)
        pred = target_scaler.inverse_transform(pred_scaled)

        return {"predicted_carbon_intensity": f"{float(pred[0][0])} gCO2eq/kWh"}
    except Exception as e:
        return {"error": str(e)}

# Run Uvicorn
def main():
    uvicorn.run(app, host=os.getenv("API_HOST"), port=int(os.getenv("API_PORT")))


if __name__ == "__main__":
    main()
