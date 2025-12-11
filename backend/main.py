from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.base import engine, Base, SessionLocal
from db import models
from services.entry_service import create_entry, list_entries
from schemas.entry_schema import EntryCreate, EntryResponse
from typing import List


app = FastAPI()

# This line tells SQLAlchemy to create the tables in the database
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Life Insights Engine backend is running!"}


@app.post("/entries", response_model=EntryResponse)
def api_create_entry(entry: EntryCreate, db: Session = Depends(get_db)):
    new_entry = create_entry(
        db=db,
        content=entry.content,
        type_=entry.type,
        tags=entry.tags,
        sentiment_score=entry.sentiment_score
    )

    # Convert DB string tags -> list[str] for the response
    tags_list = new_entry.tags.split(",") if new_entry.tags else []

    return EntryResponse(
        id=new_entry.id,
        timestamp=new_entry.timestamp,
        content=new_entry.content,
        type=new_entry.type,
        tags=tags_list,
        sentiment_score=new_entry.sentiment_score,
    )


@app.get("/entries", response_model=List[EntryResponse])
def api_list_entries(db: Session = Depends(get_db)):
    entries = list_entries(db)
    response_entries = []
    for e in entries:
        tags_list = e.tags.split(",") if e.tags else []
        response_entries.append(
            EntryResponse(
                id=e.id,
                timestamp=e.timestamp,
                content=e.content,
                type=e.type,
                tags=tags_list,
                sentiment_score=e.sentiment_score,
            )
        )

    return response_entries
