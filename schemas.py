from typing import Union

from pydantic import BaseModel


class ScoreRecord(BaseModel):
    user: str
    score: Union[float, None] = None
