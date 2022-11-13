from pydantic import BaseModel


class Players(BaseModel):

    class Player(BaseModel):
        class Position(BaseModel):
            x: float
            y: float
            z: float
        name: str
        uuid: str
        position: Position

    players: list[Player]
