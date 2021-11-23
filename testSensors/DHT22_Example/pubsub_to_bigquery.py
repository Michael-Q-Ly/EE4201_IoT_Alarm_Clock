import json
import logging
import os
from flask import abort
from google.cloud import pubsub_v1
from google.cloud import bigquery
 
 
def bigquery_import(messages: list):
    client = bigquery.Client()
    rows_to_insert = []
    table = client.get_table(f"{os.environ.get('GCP_PROJECT')}.{os.environ.get('BQ_DATASET')}.{os.environ.get('BQ_TABLE')}")
    for msg in messages:
        rows_to_insert.append((msg.get("device_id"), msg.get("ts"), msg.get("temperature"), msg.get("humidity")))
 
    errors = client.insert_rows(table, rows_to_insert)
    if errors == []:
        logging.info("New rows have been added.")
    else:
        logging.error(errors)
 
 
def pull_sensor_data(batch_size):
    project_id = os.environ.get("GCP_PROJECT")
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, os.environ.get("SENSORS_PUBSUB_SUBSCRIPTION"))
 
    num_imports = 0
    while 1:
        response = subscriber.pull(subscription_path, max_messages=batch_size, return_immediately=True)
        if len(response.received_messages) == 0:
            break
 
        messages = []
        ack_ids = []
        for received_message in response.received_messages:
            iot_data = json.loads(
                (received_message.message.data).decode().replace("'", "\""))
            iot_data["device_id"] = received_message.message.attributes["deviceId"]
            logging.info(f"Received: {iot_data}")
            messages.append(iot_data)
            ack_ids.append(received_message.ack_id)
 
            subscriber.acknowledge(subscription_path, ack_ids)
 
        logging.info(
            f"Received and acknowledged {len(messages)} messages.")
 
        num_imports += len(messages)
        bigquery_import(messages)
 
    return num_imports
 
 
def request_handler(request):
    if not all(env_var in os.environ for env_var in ["GCP_PROJECT", "SENSORS_PUBSUB_SUBSCRIPTION", "BQ_DATASET", "BQ_TABLE"]):
        logging.error("Environment variables are incomplete! Aborting...")
        return abort(500)
    request_json = request.get_json()  # json is only available if the request's mime type was set to json
    if not request_json:
        request_json = json.loads(request.data)
    if request_json and "batchSize" in request_json:
        num_messages = pull_sensor_data(int(request_json["batchSize"]))
        return f"{num_messages} messaged imported into BigQuery"
 
    return abort(422)  # unprocessable entity
 
 
# for local testing from console, update the environment variables below
# and set the GOOGLE_APPLICATION_CREDENTIALS environment variable to
# the path of your service account info JSON file
if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "[PATH_TO_YOUR_SERVICE_KEY_JSON_FILE]"
    os.environ["GCP_PROJECT"] = "[YOUR_PROJECT_ID]"
    os.environ["SENSORS_PUBSUB_SUBSCRIPTION"] = "[YOUR_PUBSUB_TOPIC_NAME]"
    os.environ["BQ_DATASET"] = "[YOUR_IOT_BIGQUERY_DATASET_NAME]"
    os.environ["BQ_TABLE"] = "[YOUR_BIGQUERY_TABLE_NAME_WITHIN_THE_DATASET]"
 
    num_messages = pull_sensor_data(10)
    logging.info(f"Pulled and imported {num_messages} messages")
