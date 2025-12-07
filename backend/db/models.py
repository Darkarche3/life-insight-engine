from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

from .base import Base

class EntryModel(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)
    tags = Column(String, default="")
    sentiment_score = Column(Float, default=0.0)
