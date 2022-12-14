from nonebot import on_command
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.params import ArgPlainText

from ...database import DB as db
from ...utils import get_type_id, handle_uid, permission_check, to_me, uid_check

dynamic_off = on_command("关闭动态", rule=to_me(), priority=5)
dynamic_off.__doc__ = """关闭动态 UID"""

dynamic_off.handle()(permission_check)

dynamic_off.handle()(handle_uid)

dynamic_off.got("uid", prompt="请输入要关闭动态的UID")(uid_check)


@dynamic_off.handle()
async def _(event: MessageEvent, uid: str = ArgPlainText("uid")):
    """根据 UID 关闭动态"""
    if await db.set_sub(
        "dynamic",
        False,
        uid=uid,
        type=event.message_type,
        type_id=await get_type_id(event),
    ):
        user = await db.get_user(uid=uid)
        assert user is not None
        await dynamic_off.finish(f"已关闭 {user.name}（{user.uid}）的动态推送")
    await dynamic_off.finish(f"UID（{uid}）未关注，请先关注后再操作")
