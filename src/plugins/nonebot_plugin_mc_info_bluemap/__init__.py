from nonebot import get_driver
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment, Message
from nonebot import on_startswith, on_message
from nonebot.matcher import Matcher, Bot
import httpx
from .models import Players

server_status = on_startswith(msg=".mc", ignorecase=True, priority=15)


@server_status.handle()
async def _server_status(bot: Bot, event: GroupMessageEvent):
    with httpx.Client() as client:
        try:
            r = client.get("http://mc.kirakira.vip:6353/maps/overworld/live/players")
            players: Players = Players.parse_raw(r.text)
            text: str = f"服务器地址: mc.kirakira.vip:25581\n网页地图: mc.kirakria.vip:6353\n当前服务器在线人数：{len(players.players)}人\n"
            text += "\n".join([f"{player.name}({int(player.position.x)},{int(player.position.y)},{int(player.position.z)})" for player in players.players])
            text += "\n\n欢迎来找小九玩哦～"
            await server_status.finish(Message(MessageSegment.text(text)))
        except Exception as e:
            pass


