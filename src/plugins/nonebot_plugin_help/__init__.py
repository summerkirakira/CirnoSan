from nonebot import get_driver, on_startswith
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, MessageSegment, Message
from .generate_help_image import get_help


help_image = on_startswith('.帮助', priority=3, block=True)
command_image = on_startswith('.指令', priority=3, block=True)


@help_image.handle()
async def _help_image():
    await help_image.finish(Message(MessageSegment.image(await get_help())))


@command_image.handle()
async def _command_image():
    await command_image.finish(Message(MessageSegment.image(await get_help())))
