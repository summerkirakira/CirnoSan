from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    class Config:
        extra = "ignore"
        cool_photo_not_find = [
            '诶？未找到舰船图片的说～',
            '摸摸摸～不存在的哦～',
            '请小伙伴检查输入的舰船是否正确哦～',
            '404 NOT FIND ',
            '过分...明明不存在的说！'
        ]
