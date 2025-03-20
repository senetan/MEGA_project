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
    """
    Root endpoint of the API.

    This function is called when a user accesses the root of the API.
    It returns a welcome message.

    Returns:
        dict: A welcome message from the API.
    """
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
    """
    Make a carbon intensity prediction.

    This function takes the input data provided by the user, transforms
    it using the feature pipeline, and makes a prediction using the pre-trained model.
    It then returns the predicted carbon intensity in grams of CO2 per kWh.

    Args:
        input_data (PredictionInput): Input data containing energy consumption breakdown by source.

    Returns:
        dict: A dictionary containing the predicted carbon intensity in gCO2eq/kWh or an error message.
    """
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
    """
    Starts the FastAPI application with Uvicorn.

    This function runs the FastAPI application using the Uvicorn server,
    taking the host and port information from the environment variables.
    """
    uvicorn.run(app, host=os.getenv("API_HOST"), port=int(os.getenv("API_PORT")))


if __name__ == "__main__":
    main()
