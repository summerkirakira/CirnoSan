# import nonebot
from nonebot import get_driver, Bot, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from .config import Config, save_config_to_yaml, get_config, current_folder
from nonebot.rule import Rule
from .data_source import insert_new_row
import os

driver = get_driver()

if not os.path.exists(os.path.join(current_folder, "config.yaml")):
    save_config_to_yaml(Config.Config.default_record_dict)
config: dict = get_config()


def enabled_record_checker() -> Rule:
    async def _enabled_record_checker(bot: Bot, event: Event) -> bool:
        if isinstance(event, GroupMessageEvent):
            if int(bot.self_id) in config and \
                    event.group_id in config[int(bot.self_id)]:
                return True
            return False
        return False

    return Rule(_enabled_record_checker)


insert_message = on_message(priority=-1, rule=enabled_record_checker())


@insert_message.handle()
async def _insert_message(bot: Bot, event: Event):
    insert_message.block = False
    if isinstance(event, GroupMessageEvent):
        await insert_new_row(qq_id=event.sender.user_id, bot_id=int(bot.self_id), group=event.group_id,
                             text_message=str(event.get_message()), name=event.sender.nickname,
                             permission=event.sender.role)


