from io import BytesIO
from PIL import Image, ImageFilter
import nonebot
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent, MessageSegment
from nonebot import get_driver
from lxml import etree
from dateutil.parser import parse
import datetime
import httpx
import time
import os

server_status = on_startswith(".服务器状态")

@server_status.handle()
async def _server_status(bot: Bot, event: GroupMessageEvent):
    await bot.send(event, Message(MessageSegment.image(resize_image(await get_server_status()))))


async def get_server_status() -> bytes:
    async with httpx.AsyncClient() as client:
        r = await client.get("https://image.thum.io/get/width/1200/crop/1200/https://status.robertsspaceindustries.com")
        return r.content


def resize_image(image_bytes: bytes) -> bytes:
    image = Image.open(BytesIO(image_bytes))
    image = image.crop((150, 5, 1050, 1200))
    output = BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()



