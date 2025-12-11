from sqlalchemy.orm import Session

from repositories.entry_repository import create_entry as repo_create_entry
from repositories.entry_repository import list_entries as repo_list_entries


ALLOWED_TYPES = {"note", "habit", "reflection"}

def create_entry(db: Session, content: str, type_: str, tags: list[str], sentiment_score: float = 0.0):
    # 1. Content must not be empty
    if not content or content.strip() == "":
        raise ValueError("Entry content cannot be empty.")

    # 2. Type must be valid
    if type_ not in ALLOWED_TYPES:
        raise ValueError(f"Invalid entry type. Must be one of: {', '.join(ALLOWED_TYPES)}")

    # 3. Sentiment must be between 0 and 1
    if not (0.0 <= sentiment_score <= 1.0):
        raise ValueError("Sentiment score must be between 0 and 1.")

    # 4. Normalize tags
    normalized_tags = []
    if tags:
        seen = set()
        for t in tags:
            cleaned = t.strip().lower()
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                normalized_tags.append(cleaned)

    # 5. Save to repository
    return repo_create_entry(
        db=db,
        content=content,
        type_=type_,
        tags=normalized_tags,
        sentiment_score=sentiment_score,
    )



def list_entries(db: Session, type_: str | None = None, limit: int | None = None):
    return repo_list_entries(db=db, type_=type_, limit=limit)
