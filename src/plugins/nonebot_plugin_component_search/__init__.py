from nonebot import get_driver, on_message, Bot, on_startswith
from .util import convert_image_to_bytes

from .config import Config
from nonebot.params import State
from nonebot.typing import T_State
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, MessageSegment, Message
from loguru import logger
from .util import send_image, check_is_sendable, double_check_message

from .calculator import Calculator
from typing import Optional
from .models import Weapon
global_config = get_driver().config

driver = get_driver()

calculator: Optional[Calculator] = None


@driver.on_startup
async def startup():
    global calculator
    calculator = Calculator()
    logger.opt(colors=True).info('<g>成功加载武器组件信息!</g>')


def is_weapon() -> Rule:
    async def _is_weapon(bot: Bot, event: Event, state: T_State = State()) -> bool:
        if isinstance(event, GroupMessageEvent) and event.get_plaintext():
            command = event.get_plaintext().replace('.', '', 1).strip()
            if command.startswith('武器'):
                state['weapon'] = command.strip().replace('武器', '')
                return True
            elif command.startswith('机炮'):
                state['weapon'] = command.strip().replace('机炮', '')
                return True
        return False


weapons_search = on_startswith('.', priority=100)


@weapons_search.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    text: str = event.get_plaintext().replace('.', '', 1).strip()
    if text:
        if text.startswith('武器'):
            pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.weapons))
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        elif text.startswith('量子') or text.startswith('跃迁'):
            pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.qdrives))
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        elif text.startswith('护盾'):
            pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.shields))
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        elif text.startswith('冷却器'):
            pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.coolers))
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        elif text.startswith('导弹'):
            pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.missiles))
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        elif text.startswith('电源') or text.startswith('发电机'):
            pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.power_plants))
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        elif text == '商店':
            pic = convert_image_to_bytes(calculator.generate_shop_item_pic())
            await bot.send(event, Message(MessageSegment.image(pic)))
            return
        item_list = calculator.get_match_items_by_name(text, 10)
        # matched_list: list[tuple[Weapon, float]] = [(item, ratio) for (item, ratio) in item_list if isinstance(
        # item, Weapon)]
        matched_list = item_list # not implemented yet
        if matched_list:
            checked_list = check_is_sendable(matched_list)
            if len(checked_list) == 1:
                await bot.send(event, MessageSegment.image(f'https://localhost/components/v2/{checked_list[0][0].data.ref}.png'))
            else:
                message = double_check_message(checked_list)
                await bot.send(event, Message(MessageSegment.text(message)))
                return
        else:
            await bot.send(event, '没有找到匹配的物品哦~')
    # pic = convert_image_to_bytes(calculator.generate_item_type_pic(calculator.weapons))
    # await bot.send(event, Message(MessageSegment.image(pic)))