from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    class Config:
        extra = "ignore"
        allow_search_player_key = [
            'id查询',
            'ID查询',
            '查询玩家',
            '玩家查询',
            'id'
        ]
