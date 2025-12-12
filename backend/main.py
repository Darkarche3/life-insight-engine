from fastapi import FastAPI, Depends, HTTPException
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
    try:
        new_entry = create_entry(
            db=db,
            content=entry.content,
            type_=entry.type,
            tags=entry.tags,
            sentiment_score=entry.sentiment_score,
        )
    except ValueError as e:
        # Translate business-level error → HTTP 400
        raise HTTPException(status_code=400, detail=str(e))

    # Convert DB tags string -> list for the response
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
def api_list_entries(
    type: str | None = None,
    limit: int | None = None,
    tag: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    entries = list_entries(db, type_=type, limit=limit, tag=tag, search=search)

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
