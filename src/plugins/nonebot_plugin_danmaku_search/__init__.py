from nonebot import get_driver
from .config import get_config
from .models import UserHistory
from typing import List, Optional
import httpx
from loguru import logger

from nonebot import get_driver, on_message, on_notice, on_startswith
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, MessageSegment, Message, Bot


async def get_user_history(uid: int, page_size: Optional[int] = None, page_num: Optional[int] = None, target: Optional[int] = None) -> UserHistory:
    async with httpx.AsyncClient(verify=False) as client:
        params = {
            "uid": uid,
            "pagesize": page_size,
            "pagenum": page_num,
            "target": target,
        }
        if not params["pagesize"]:
            del params["pagesize"]
        if not params["pagenum"]:
            del params["pagenum"]
        if not params["target"]:
            del params["target"]
        resp = (await client.get(f"https://danmaku.suki.club/api/search/user/detail", params=params)).json()
        return UserHistory.parse_obj(resp)


danmaku_search = on_startswith('.查入场', priority=30, block=True)


async def get_uid_by_name(name: str) -> int:
    try:
        url = "http://api.bilibili.com/x/web-interface/search/type"
        params = {"search_type": "bili_user", "keyword": name}
        async with httpx.AsyncClient(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Cookie": get_config()["bili_cookie"]
        }) as client:
            resp = await client.get(url, params=params, timeout=10)
            result = resp.json()
        for user in result["data"]["result"]:
            if user["uname"] == name:
                return user["mid"]
        return 0
    except (KeyError, IndexError, httpx.TimeoutException) as e:
        logger.warning(f"Error in get_uid_by_name({name}): {e}")
        return 0


def generate_message(user_history: UserHistory, limit: Optional[int] = None) -> str:
    return '\n'.join([str(data) for data in user_history.data.data])


@danmaku_search.handle()
async def _danmaku_search(bot: Bot, event: GroupMessageEvent):
    name_or_uid = event.get_plaintext().replace('.查入场', '').strip()
    if not name_or_uid.isdigit():
        uid = await get_uid_by_name(name_or_uid)
    else:
        uid = int(name_or_uid)
    if uid == 0:
        await danmaku_search.finish(Message('未找到该用户'))
    history: UserHistory = await get_user_history(uid, page_size=20)
    if history.code == 200:
        if not history.data:
            await danmaku_search.finish(f'未找到用户{uid}的入场记录')
        await danmaku_search.finish(Message(f"用户{uid}入场记录：\n{generate_message(history)}"))
    else:
        await danmaku_search.finish(Message(f"查询失败：{history.message}"))
