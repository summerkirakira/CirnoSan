from pydantic import BaseSettings
import os
import yaml

current_folder = os.path.dirname(__file__)


def get_config() -> dict:
    with open(os.path.join(current_folder, 'config.yaml'), "r", encoding='utf-8') as file:
        return yaml.safe_load(file.read())


def save_config_to_yaml(server_info):
    with open(os.path.join(current_folder, 'config.yaml'), 'w', encoding='utf-8') as f:
        f.write(yaml.dump(server_info, allow_unicode=True, sort_keys=False))


class Config(BaseSettings):

    class Config:
        extra = "ignore"
        default_config = {
            'sponsor_id': [2279981701, 751157294, 2053438632, 1741103316, 1535044994, 2835368897, 2213347911, 78057791,
                           1317246265, 154712316, 970037830, 2622820396, 1327291955, 744950835, 3288127992, 1760600684,
                           2437638506, 85902756],
            'enabled_groups': [463185812]
        }

