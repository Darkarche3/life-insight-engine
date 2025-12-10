from typing import List
from sqlalchemy.orm import Session

from db.models import EntryModel

def create_entry(db: Session, content: str, type_: str, tags: list[str], sentiment_score: float = 0.0) -> EntryModel:
    tags_str = ",".join(tags) if tags else ""
    entry = EntryModel(
        content=content,
        type=type_,
        tags=tags_str,
        sentiment_score=sentiment_score,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def list_entries(db: Session) -> List[EntryModel]:
    return db.query(EntryModel).order_by(EntryModel.timestamp.desc()).all()
