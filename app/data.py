import os
import pandas as pd
import logging
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Chemins configurables ===
LOCAL_DATA_PATH = os.getenv("DATA_PATH", "data/df_de_merged_update_timeline.csv")
GCP_BUCKET_NAME = os.getenv("BUCKET_NAME")
GCP_DATASET_PATH = os.getenv("DATASET")  # ex: "path/in/bucket/data.csv"
GCP_CREDENTIALS = os.getenv("GAC_KEY", "service-account-key.json")

# === Chargement local ===

def load_local_data(path: str = LOCAL_DATA_PATH) -> pd.DataFrame:
    try:
        logger.info(f"Chargement des données locales depuis {path}")
        df = pd.read_csv(path)
        logger.info(f"Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
        return df
    except Exception as e:
        logger.error(f"Erreur chargement local : {e}")
        raise

# === Chargement depuis GCP ===

def load_data_from_gcp(bucket_name: str = GCP_BUCKET_NAME,
                       blob_path: str = GCP_DATASET_PATH,
                       credentials_path: str = GCP_CREDENTIALS) -> pd.DataFrame:
    try:
        logger.info(f"Connexion à GCP - Bucket: {bucket_name}, Blob: {blob_path}")
        storage_client = storage.Client.from_service_account_json(credentials_path)
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_path)

        content = blob.download_as_bytes()
        df = pd.read_csv(pd.io.common.BytesIO(content))

        logger.info(f"Données chargées depuis GCP : {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Erreur chargement GCP : {e}")
        raise

# === Interface générique ===

def load_data(source: str = "local") -> pd.DataFrame:
    """
    source : 'local' ou 'gcp'
    """
    if source == "gcp":
        return load_data_from_gcp()
    return load_local_data()
