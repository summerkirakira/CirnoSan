from nonebot import on_startswith, on_regex
from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, MessageSegment, Message
from .data_source import kaihei_message_process
from .config import current_folder, save_config_to_yaml
import os

from .config import get_config

driver = get_driver()

# kaihei_status_check = on_startswith('.开黑啦', priority=15)
kaihei_status_check = on_regex('^\.开黑|^\.kook|^\.语音', priority=15)


@kaihei_status_check.handle()
async def _kaihei_status_check(bot: Bot, event: Event):
    if isinstance(event, GroupMessageEvent):
        kaihei_info = await kaihei_message_process(event.group_id)
        message = [MessageSegment.text(kaihei_info)]
        await bot.send(event, Message(message))


@driver.on_startup
async def init():
    if not os.path.exists(os.path.join(current_folder, "config.yaml")):
        save_config_to_yaml({"kai_hei_api_url": {12345678: {"api_key": "", "invitation_link": ""}}})
