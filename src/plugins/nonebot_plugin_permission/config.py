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
        default_config = {
            'enable_group': [901809142, 463185812, 956263332, 1047437620, 371361048, 950866616, 751505983, 903164626,
                             834365589, 956263332, 648884060, 966123127, 943264039, 39901318, 12312312],
            'ai_id': [2086868211, 934869815, 12345678],
            'black_list': [258760137, 1003726167, 1784558931]
        }
