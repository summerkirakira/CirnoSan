from nonebot import on_startswith, export
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, Message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import get_driver
from nonebot.params import State
from nonebot.rule import Rule
from .data_source import current_folder, SHIP_PIC_PATH, ship_alias, ship_list, pic_locate


from .config import Config
import os

global_config = get_driver().config
config = Config(**global_config.dict())


def is_ship_name() -> Rule:
    async def _ship_name_checker(bot: Bot, event: Event, state: T_State=State()) -> bool:
        input_name: str = event.get_plaintext().replace(' ', '').replace('.', '')
        state['ship_name'] = input_name
        if input_name in ship_list:
            return True
        else:
            for ship_name in ship_alias:
                for ship_alias_name in ship_alias[ship_name]:  # match ship alis name
                    if input_name == ship_alias_name:
                        state['ship_name'] = ship_name
                        return True
            return False

    return Rule(_ship_name_checker)


ship_info = on_startswith('.', rule=is_ship_name(), priority=15)


@ship_info.handle()
async def handle_ship_search(bot: Bot, event: MessageEvent, state: T_State=State()):
    with open(os.path.join(SHIP_PIC_PATH, f'{pic_locate(state["ship_name"])}.png'), 'rb') as f:
        ship_pic_bytes = f.read()
    picture = MessageSegment.image(ship_pic_bytes)
    await bot.send(event, Message(picture))


# Export something for other plugin
export = export()
export.ship_alias = ship_alias
export.ship_info_list = os.listdir(os.path.join(current_folder, 'ship_info_pic'))

