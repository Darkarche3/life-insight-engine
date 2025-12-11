from pydantic import BaseModel
from datetime import datetime
from typing import List


class EntryCreate(BaseModel):
    content: str
    type: str
    tags: List[str] = []
    sentiment_score: float = 0.0


class EntryResponse(BaseModel):
    id: int
    timestamp: datetime
    content: str
    type: str
    tags: List[str]
    sentiment_score: float

    class Config:
        orm_mode = True
