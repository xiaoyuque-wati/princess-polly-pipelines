import os


REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
GCS_BUCKET = os.getenv('GCS_BUCKET', 'your-gcs-bucket-name')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'mt-prod-tenants')

