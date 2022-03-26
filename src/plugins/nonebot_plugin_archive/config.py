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
    # Your Config Here

    class Config:
        extra = "ignore"
        entry_modify_success = [
            "诶嘿嘿～词条编辑成功哦～",
            "词条编辑成功哟～",
            "Success～",
            "Succèss～",
            "词条录入成功...",
            "词条录入ing...\nSuccess...",
            "少女折寿中...\nSuccess!"
        ]
        entry_remove_success = [
            "诶嘿嘿～词条移除成功哦～",
            "词条移除成功哟～",
            "Success～",
            "Succèss～",
            "词条移除成功...",
            "词条移除ing...\nSuccess...",
            "少女折寿中...\nSuccess!"
        ]
        entry_not_legal = [
            "嗯...待移除的词条不匹配呢...",
            "数据库中没有匹配的条目呢～",
            "请小伙伴确认词条名是否正确哦～",
            "参数不合法(๑>◡<๑)"
        ]
        default_config = {
        }