import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class HighScore(Base):
    __tablename__ = "highscore"

    game_id = Column(Integer, primary_key=True)
    user = Column(String, primary_key=True)
    score = Column(Float)
    ts = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
