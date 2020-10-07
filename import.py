import coloredlogs
import json
import logging
import os
import os.path
import requests

GLOBAL_URL = "https://api.getpostman.com/"
COLLECTIONS_ENDPOINT = GLOBAL_URL + "collections/"
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def get_collection(client, uuid):
    response = client.get(COLLECTIONS_ENDPOINT+uuid)
    response.raise_for_status()
    return response.json()["collection"]


def update_collection(client, collection, uuid):
    logger.info(f"Updating collection with name {collection['info']['name']}")
    user_collection = get_collection(client, uuid)
    collection["item"] = merge_folders(collection["item"], user_collection["item"])
    response = client.put(COLLECTIONS_ENDPOINT+uuid, data=json.dumps({'collection': collection}))
    response.raise_for_status()


def merge_folders(new_folders, existing_folders):
    existing_dict = {f["name"]: f for f in existing_folders}
    new_dict = {f["name"]: f for f in new_folders}

    user_added_folders = []
    user_added_requests = []
    for name, folder_request in existing_dict.items():
        if not name in new_dict:
            if "item" in folder_request:
                user_added_folders.append(folder_request)
            else:
                user_added_requests.append(folder_request)

    common_requests = []
    common_folders = []
    remote_added_requests = []
    remote_added_folders = []
    for name, folder_request in new_dict.items():
        if "item" in folder_request:
            if not name in existing_dict:
                remote_added_folders.append(folder_request)
            else:
                common_folders.append(folder_request)
        else:
            if not name in existing_dict:
                remote_added_requests.append(folder_request)
            else:
                common_requests.append(folder_request)
    
    return [*common_folders, *remote_added_folders, *user_added_folders, *common_requests, *remote_added_requests, *user_added_requests]


def merge_requests(new_folder, existing_folder):
    new_requests = {r["name"]: r for r in new_folder}
    existing_requests = {r["name"]: r for r in existing_folder}


    user_added_requests = []
    for name, request in existing_requests.items():
        if not name in new_requests:
            user_added_requests.append(request)

    common_requests = []
    remote_added_requests = []
    for name, request in new_requests.items():
        if not name in existing_requests:
            remote_added_requests.append(request)
        else:
            common_requests.append(request)

    return [*common_requests, *remote_added_requests, *user_added_requests]
    

def create_collection(client, collection):
    logger.info(f"Creating new collection with name {collection['info']['name']}")
    response = client.post(COLLECTIONS_ENDPOINT, data=json.dumps({'collection': collection}))
    response.raise_for_status()


def get_user_collections(client):
    logger.info("Retrieving user collections")
    response = client.get(COLLECTIONS_ENDPOINT)
    if response.status_code == 200:
        return response.json()["collections"]
    else:
        response.raise_for_status()
        return []


def get_collections_to_import():
    logger.info("Retrieving collections in folder")
    base_path = './collections/'
    directory = os.listdir(base_path)
    result = []
    for element in directory:
        if os.path.isfile(os.path.join(base_path, element)) and element.endswith('.json'):
            with open(os.path.join(base_path, element), 'r') as f:
                result.append(json.load(f))
    return result
            

if __name__ == "__main__":
    logger.info("Importing Postman collections")

    api_key = None
    with open('postman-key', 'r') as keyfile:
        api_key = keyfile.read()

    with requests.Session() as client:
        client.headers.update({'X-Api-Key': api_key})
        collections = get_collections_to_import()
        user_collections = {collection["name"]: collection for collection in get_user_collections(client)}
        for collection in collections:
            if collection["info"]["name"] in user_collections:
                collection["info"]["_postman_id"] = user_collections[collection["info"]["name"]]["id"]
                update_collection(client, collection, collection["info"]["_postman_id"])
            else:
                collection["info"].pop("_postman_id")
                create_collection(client, collection)
