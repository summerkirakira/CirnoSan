from nonebot import get_driver
from nonebot import get_driver, on_message, Bot, on_startswith
from nonebot.adapters.onebot.v11 import Bot, Event, Message, GroupMessageEvent
from .config import default_entries, save_config_to_yaml, current_folder, get_config

import os
global_config = get_driver().config


if not os.path.exists(os.path.join(current_folder, "config.yaml")):
    save_config_to_yaml(default_entries)
config: dict = get_config()

get_default_entries = on_startswith('.', priority=30, block=True)


@get_default_entries.handle()
async def _get_default_entries(bot: Bot, event: GroupMessageEvent):
    key = event.get_plaintext().replace('.', '').strip()
    if key in config:
        await bot.call_api('send_group_msg', message=config[key], group_id=event.group_id)
        return
    get_default_entries.block = False


