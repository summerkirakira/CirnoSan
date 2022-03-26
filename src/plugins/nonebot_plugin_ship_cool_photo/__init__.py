from nonebot import get_driver, on_startswith
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.adapters.onebot.v11.message import MessageSegment
import nonebot
import random
import os
import json

from .config import Config

current_folder = os.path.dirname(__file__)  # get current folder absolute path
with open(os.path.join(current_folder, 'ImageInform.json'), "r", encoding='utf-8') as f:
    image_list = json.loads(f.read())

global_config = get_driver().config
config = Config(**global_config.dict())
export = nonebot.require("nonebot_plugin_ship_information")
message_export = nonebot.require("nonebot_plugin_cute_message")

ship_alias = export.ship_alias
ship_list = export.ship_info_list

COOL_PHOTO_PATH = os.path.join(current_folder, 'CoolPhotos')


def ship_name_checker(input_name) -> any:
    if input_name in ship_list:
        return input_name
    else:
        for ship_name in ship_alias:
            for ship_alias_name in ship_alias[ship_name]:  # match ship alis name
                if input_name == ship_alias_name:
                    return ship_name

        return None


def get_path(message):
    mString = message.replace(".色图", "").replace(' ', '')
    if mString:
        mString = mString.strip()
        if ship_name_checker(mString):
            name = ship_name_checker(mString)
            ship_photos = []
            for ship in image_list:
                if ship["model"]["name"] == name:
                    ship_photos.append(ship)
            if ship_photos:
                chosen_photo = random.choice(ship_photos)
                file_path = os.path.join(current_folder, 'CoolPhotos', chosen_photo["name"])
                return file_path
            else:
                return None
        return None
    else:
        return os.path.join(current_folder, 'CoolPhotos', random.choice(os.listdir(COOL_PHOTO_PATH)))


cool_photo = on_startswith('.色图', priority=14)


@cool_photo.handle()
async def _cool_photo(bot: Bot, event: Event):
    photo_path = get_path(event.get_plaintext())
    if photo_path:
        with open(os.path.join(photo_path), 'rb') as f:
            r = f.read()
        await bot.send(event, Message(MessageSegment.image(r)))
    else:
        await bot.send(event, Message(
            MessageSegment.text(random.choice(Config.Config.cool_photo_not_find) + random.choice(message_export.emoji))))

