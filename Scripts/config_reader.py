import json
import os

import yaml

CONFIG_FILENAME = "config.yml"
SECRET_FILENAME = "secret.yml"

config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), CONFIG_FILENAME
)

secret_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), SECRET_FILENAME
)

try:
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    raise Exception(
        "Configuration file not found. Please make sure the config.yml file is in the Main Folder."
    )
except yaml.YAMLError:
    raise Exception(
        "Error parsing the configuration file. Invalid YAML format. Please make sure the config.yml is formatted correctly."
    )

try:
    with open(secret_path, encoding="utf-8") as f:
        secret = yaml.safe_load(f)
except FileNotFoundError:
    raise Exception(
        "Configuration file not found. Please create the secret.yml file is in the Main Folder."
    )
except yaml.YAMLError:
    raise Exception(
        "Error parsing the configuration file. Invalid YAML format. Please make sure the secret.yml is formatted correctly."
    )


class Paths:
    root_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    logs_folder = os.path.join(root_folder, "logs")


class Bot:
    token = secret["BOT TOKEN"]
    server = config["Server"]["server_id"]
    owner_id = config["Owner"]["owner_id"]


class Roles:
    roles_lookup = config["roles"]


class InvalidConfigError(Exception):
    pass


def validate():
    """
    Function to check validity of config on startup
    """

    roles_dict = Roles.roles_lookup

    # Check if the dictionary is empty
    if not roles_dict:
        raise InvalidConfigError("The 'roles' in the config is empty.")

    # Check for duplicate role IDs
    seen_role_ids = set()
    for role_id in roles_dict.keys():
        if role_id in seen_role_ids:
            raise InvalidConfigError(f"Duplicate role ID found: {role_id}.")
        seen_role_ids.add(role_id)
