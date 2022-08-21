import email
from io import BytesIO
from PIL import Image
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, MessageSegment, Message
from .models import ComponentData
from typing import Union


def convert_image_to_bytes(image: Image) -> bytes:
    output = BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()


async def send_image(bot: Bot, group_id: int, ref: str):
    await bot.call_api('send_group_msg', group_id=group_id, message=f"[CQ:image,file=https://biaoju.site/component/{ref}.png]")


def check_is_sendable(item_list: list[tuple[ComponentData, float]]) -> list[tuple[ComponentData, float]]:
    matched_list: list[tuple[ComponentData, float]] = []
    highest_ratio = 0
    for item, ratio in item_list:
        if ratio < highest_ratio:
            break
        if ratio >= 0.5:
            matched_list.append((item, ratio))
            highest_ratio = ratio
    return matched_list


def double_check_message(item_list: list[tuple[ComponentData, float]]) -> str:
    message: str = '小九不是很清楚你要找的是什么哦~\n请问你要找的是--\n'
    item_list: list[tuple[ComponentData, float]] = [(item, ratio) for item, ratio in item_list if ratio > 0.2]
    if not item_list:
        return '小九没有找到匹配的物品哦~请尝试使用更精确的中英文搜索哦～'
    for item, ratio in item_list:
        message += f'[{item.data.chineseTypeName}]{item.data.chineseName}\n'
    message = message[:-1]
    return message
    
