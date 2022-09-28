from pydantic import BaseModel
from typing import List, Optional
from enum import IntEnum
import time


class UserHistory(BaseModel):
    """用户历史记录"""
    code: int
    message: str

    class Data(BaseModel):
        class Data(BaseModel):
            class Channel(BaseModel):
                name: str
                isLiving: bool
                roomId: int
                faceUrl: str
                tags: List[str]
                totalLiveCount: int
                totalDanmakuCount: int
                totalIncome: int
                totalLiveSecond: int
                lastLiveDate: int

            class Live(BaseModel):
                liveId: str
                title: str
                area: Optional[str]
                parentArea: Optional[str]
                isFinish: bool
                coverUrl: str
                startDate: int
                stopDate: int
                danmakusCount: int
                totalIncome: int
                watchCount: int
                interactionCount: int

            class Danmaku(BaseModel):
                class Type(IntEnum):
                    TEXT = 0
                    GIFT = 1
                    FLEET = 2
                    SUPER_CHAT = 3
                    JOIN = 4
                name: str
                type: int
                uId: int
                sendDate: int
                price: int
                message: str

            channel: Channel
            live: Optional[Live]
            danmakus: List[Danmaku]

            def __str__(self):
                string: str = f"在主播: {self.channel.name} 的直播间:\n  "
                action_list: list[str] = []
                for danmaku in self.danmakus:
                    send_time: str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(danmaku.sendDate / 1000))
                    if danmaku.type == self.Danmaku.Type.TEXT:
                        action_list.append(f"在{send_time}发送了弹幕：{danmaku.message}")
                    elif danmaku.type == self.Danmaku.Type.GIFT:
                        action_list.append(f"在{send_time}赠送了礼物：{danmaku.message}")
                    elif danmaku.type == self.Danmaku.Type.FLEET:
                        action_list.append(f"在{send_time}赠送了{danmaku.message}")
                    elif danmaku.type == self.Danmaku.Type.SUPER_CHAT:
                        action_list.append(f"在{send_time}发送了SC：{danmaku.message}")
                    elif danmaku.type == self.Danmaku.Type.JOIN:
                        action_list.append(f"在{send_time}进入了直播间: {self.live.title}")
                string += "\n  ".join(action_list)
                return string
        data: List[Data]

    data: Data

