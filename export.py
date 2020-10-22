import coloredlogs
import logging
import requests
import json
import os
from pprint import pprint

GLOBAL_URL = "https://api.getpostman.com/"
COLLECTIONS_ENDPOINT = GLOBAL_URL + "collections/"
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def get_all_collections(client):
    response = client.get(COLLECTIONS_ENDPOINT)
    response.raise_for_status()
    return response.json()['collections']


def get_collection(client, uid):
    response = client.get(COLLECTIONS_ENDPOINT+uid)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    logger.info("Exporting user collections")

    api_key = None
    with open('postman-key', 'r') as keyfile:
        api_key = keyfile.read()

    with requests.Session() as client:
        client.headers.update({'X-Api-Key': api_key})
        user_collections = get_all_collections(client)
        for collection in user_collections:
            logger.debug(f"Retrieving collection {collection['name']}")
            complete_collection = get_collection(client, collection['id'])['collection']
            if not os.path.exists("./collections/"):
                os.mkdir("./collections/")
            with open(f"./collections/{collection['name']}.postman_collection.json", "w+") as collection_file:
                logger.info(f"Exporting collection {collection['name']}")
                collection_file.write(json.dumps(complete_collection))
