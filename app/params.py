import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

##################  VARIABLES  ##################
DATASET = os.environ.get("DATASET")
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
INSTANCE = os.environ.get("INSTANCE")
GAR_IMAGE = os.environ.get("GAR_IMAGE")
GAC_KEY = os.environ.get("GAC_KEY")
