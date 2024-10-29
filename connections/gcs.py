from google.cloud import storage
from common.config import GCS_BUCKET

def get_gcs_client():
    return storage.Client()
