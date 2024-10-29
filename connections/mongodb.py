from pymongo import MongoClient
from common.config import MONGODB_URI, DATABASE_NAME


def get_mongo_client():
    mongo_client = MongoClient(MONGODB_URI)
    return mongo_client[DATABASE_NAME]
