import datetime
import json
from quart import Quart, request  # Replace Flask with Quart
import asyncio
from connections.redis import get_redis_client
from connections.gcs import get_gcs_client
from connections.mongodb import get_mongo_client  # Add this import
from filter import test_filter_campaigns

import os 
app = Quart(__name__)  # Replace Flask with Quart

# Initialize connections
mongo_collection = get_mongo_client()
redis_client = get_redis_client()
gcs_client = get_gcs_client()

### Input Request Json:
# {
#     "tenantId": "1234567890",
#     "broadcastId": "1234567890",
#     "startAtDate": "2024-01-01",
#     "endAtDate": "2024-01-01"
# }     
@app.route('/process', methods=['POST'])
async def process_data():
    request_json = request.get_json(silent=True)

    if request_json is None:
        return 'Invalid JSON', 400
    
    tenant_id = request_json.get('tenantId')
    if request_json.get('tenantId') is None:
        tenant_id = "*"

    start_at_date = request_json.get('startAtDate')
    if request_json.get('startAtDate') is None:
        start_at_date = datetime.now().strftime("%Y-%m-%d")

    end_at_date = request_json.get('endAtDate')
    if request_json.get('endAtDate') is None:
        end_at_date = datetime.now().strftime("%Y-%m-%d")

    broadcast_id = request_json.get('broadcastId')
    if request_json.get('broadcastId') is None:
        broadcast_id = "*"

    if tenant_id == "*" and start_at_date == "*" and end_at_date == "*":
        print("Reload all data")
    else:
        print("Reload data for tenantId: %s, broadcastId: %s, startAtDate: %s, endAtDate: %s", tenant_id, broadcast_id, start_at_date, end_at_date)

    # Prepare output for GCS
    output = {
        'message': 'Data processed successfully',
        'mongo_id': str(request_json.get('_id')),
        'redis_value': redis_client.get('last_insert_id').decode('utf-8')
    }

    # Store output in GCS
    # output_blob = gcs_bucket.blob('output.json')
    # output_blob.upload_from_string(json.dumps(output))

    return json.dumps(output), 200

@app.route('/health', methods=['GET'])
def health():
    mongodb_health_status = mongo_collection.health()
    redis_health_status = redis_client.ping()
    return json.dumps({'mongodb': mongodb_health_status, 'redis': redis_health_status}), 200

@app.route('/test', methods=['POST'])
def test():
    results = test_filter_campaigns()
    return json.dumps(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    test()