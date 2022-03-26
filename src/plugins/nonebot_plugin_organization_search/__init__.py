from io import BytesIO

import nonebot
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, GroupMessageEvent, MessageSegment
from .config import name_dict
import httpx
import asyncio
from PIL import Image

get_organization = on_startswith('.舰队查询')


@get_organization.handle()
async def _get_organization(bot: Bot, event: GroupMessageEvent):
    organization_name = event.get_plaintext().replace('.舰队查询', '').strip()
    if not organization_name:
        await bot.send(event, '请输入舰队名称哦～')
        return
    if organization_name in name_dict:
        organization_name = name_dict[organization_name]
    await bot.send(event, MessageSegment.image(await request_organization_pic(organization_name)))


async def request_organization_pic(organization: str) -> bytes:
    async with httpx.AsyncClient() as client:
        is_get = False
        while not is_get:
            resp = await client.get(f'https://image.thum.io/get/width/1200/allowJPG/https://robertsspaceindustries.com/orgs/{organization}', timeout=100.0)
            image = Image.open(BytesIO(resp.content))
            image = image.convert('RGB')
            r, g, b = image.getpixel((200, 0))
            if r == g == b == 255:
                is_get = False
                await asyncio.sleep(5)
            else:
                is_get = True
        return resize_image(resp.content)


def resize_image(image_bytes: bytes) -> bytes:
    image = Image.open(BytesIO(image_bytes))
    image = image.crop((0, 120, 1200, 1100))
    output = BytesIO()
    image.save(output, format='PNG')
    return output.getvalue()

