# postman-synchronizer
This project aim is to keep Postman data synchronized among team users. It is meant to manage the collections and environments in Git in order to keep track of the changes.
To effectively use this software, the advice is to fork this repository and work on your personal copy.

This is currently a WIP. Stay tuned for updates.

## Getting started
In order to use these scripts, you must have installed Python 3. If you have pipenv installed, you can just type 

`$ pipenv install -r requirements.txt`

and a virtual environment will be created with the dependencies installed.
To allow the scripts to connect with Postman through its API, you need to create a `postman-key` file in the root of the project. This file must contain
your Postman API key. It could have a form similar to the following one:

`PMAK-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

In order to obtain your key, follow this steps:
1. Go to [this](https://web.postman.co/workspaces?type=personal) link
2. Select the workspece where you want to apply the integration
3. Navigate into the "Integrations" tab.
4. Select the PostmanAPI integration.
5. Navigate into the options to find a "Generate API key" button
6. Insert data, confirm and save the key.

## Importing
You must put the collections in a "collections" folder in the root of the project.

To import the data just downloaded from Git, after the environment activation launch the following command:

`$ python import.py`

This command will take the collections and will merge their folders and requests with the current ones on the user workspace, so if a new request is created but not pushed from the user, it will remain on the workspace and won't be deleted.
