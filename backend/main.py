from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import engine, Base, SessionLocal
from db.models import EntryModel
from services.entry_service import create_entry, list_entries
from schemas.entry_schema import EntryCreate, EntryResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from datetime import datetime, timedelta


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/insights/summary")
def insights_summary(db: Session = Depends(get_db)):
    # last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    total_entries = db.query(func.count(EntryModel.id)).scalar() or 0

    avg_sentiment_7d = (
        db.query(func.avg(EntryModel.sentiment_score))
        .filter(EntryModel.timestamp >= seven_days_ago)
        .scalar()
    )

    avg_sentiment_today = (
        db.query(func.avg(EntryModel.sentiment_score))
        .filter(EntryModel.timestamp >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))
        .scalar()
    )

    return {
        "total_entries": int(total_entries),
        "avg_sentiment_7d": float(avg_sentiment_7d) if avg_sentiment_7d is not None else None,
        "avg_sentiment_today": float(avg_sentiment_today) if avg_sentiment_today is not None else None,
    }
