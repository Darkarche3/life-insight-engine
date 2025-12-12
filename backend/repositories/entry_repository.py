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


def list_entries(
    db: Session,
    type_: str | None = None,
    limit: int | None = None,
    tag: str | None = None,
    search: str | None = None,
):
    query = db.query(EntryModel)

    if type_:
        query = query.filter(EntryModel.type == type_)

    if tag:
        tag = tag.strip().lower()
        query = query.filter(EntryModel.tags.like(f"%{tag}%"))

    if search:
        search = search.strip()
        if search:
            query = query.filter(EntryModel.content.ilike(f"%{search}%"))

    query = query.order_by(EntryModel.timestamp.desc())

    if limit:
        query = query.limit(limit)

    return query.all()
