from sqlalchemy.orm import Session

from repositories.entry_repository import create_entry as repo_create_entry
from repositories.entry_repository import list_entries as repo_list_entries


def create_entry(db: Session, content: str, type_: str, tags: list[str], sentiment_score: float = 0.0):
    # 1. Validate basic inputs (service layer is responsible for this)
    if not content or content.strip() == "":
        raise ValueError("Entry content cannot be empty.")

    if type_ not in ["note", "habit", "reflection"]:
        raise ValueError("Invalid entry type. Must be 'note', 'habit', or 'reflection'.")

    # 2. Clean tags
    tags = [t.strip().lower() for t in tags] if tags else []

    # 3. Delegate the creation to the repository
    return repo_create_entry(
        db=db,
        content=content,
        type_=type_,
        tags=tags,
        sentiment_score=sentiment_score,
    )


def list_entries(db: Session):
    return repo_list_entries(db)
