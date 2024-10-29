from pymongo import MongoClient
from common.config import MONGODB_URI
from common.config import DATABASE_NAME

def find_records_by_pagination(collection_name, query, last_id=None, page_size=1000):
    """
    Fetches paginated matching records from a MongoDB collection using cursor-based pagination.

    :param collection_name: Name of the collection
    :param query: MongoDB query dictionary
    :param last_id: ObjectId of the last document from previous page
    :param page_size: Number of records per page
    :return: List of matching records
    """
    campaign_mongodb_client = MongoClient(MONGODB_URI)

    # Access the database and collection
    collection = campaign_mongodb_client[DATABASE_NAME][collection_name]
    
    # Modify query to include _id comparison if last_id is provided
    if last_id:
        query = {"$and": [{"_id": {"$gt": last_id}}, query]}
    
    # Perform the query with limit
    results = collection.find(query).sort("_id", 1).limit(page_size)
    
    # Convert results to a list
    records = list(results)
    
    # Close the connection
    if campaign_mongodb_client:
        campaign_mongodb_client.close()
    
    return records

def find_all_matching_records(collection_name, query):
    all_results = []
    last_id = None
    
    while True:
        results = find_records_by_pagination(collection_name, query, last_id=last_id, page_size=1000)
        if not results:
            break
            
        all_results.extend(results)
        last_id = results[-1]["_id"]  # Get the last document's _id for next iteration
        
    return all_results
