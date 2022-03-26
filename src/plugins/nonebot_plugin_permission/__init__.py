from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot import get_driver
import os
from .config import current_folder,get_config, save_config_to_yaml

from .config import Config

global_config = get_driver().config
if not os.path.exists(os.path.join(current_folder, "config.yaml")):
    save_config_to_yaml(Config.Config.default_config)
config: dict = get_config()

permission_check = on_message(priority=0)


@permission_check.handle()
async def message_permission(bot: Bot, event: MessageEvent):
    permission_check.block = False
    if int(bot.self_id) not in config['ai_id']:
        permission_check.block = True
        return
    if event.sender.user_id in config['black_list']:
        permission_check.block = True
        return
    if isinstance(event, GroupMessageEvent):
        if event.group_id not in config['enable_group']:
            permission_check.block = True
            return

