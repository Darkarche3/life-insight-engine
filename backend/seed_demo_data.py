from datetime import datetime, timedelta

from db.base import SessionLocal, engine
from db.models import EntryModel
from db.base import Base


def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)


def seed():
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(EntryModel).count()
        if existing >= 3:
            print(f"Already have {existing} entries. No seeding needed.")
            return

        now = datetime.utcnow()

        demo_entries = [
            # 5 days ago — Classkick product / AI idea
            EntryModel(
                content=(
                    "Thought about building a lightweight AI assistant for Classkick that helps "
                    "teachers quickly spot patterns in student confusion during a lesson. "
                    "Instead of replacing teacher judgment, the system would summarize where "
                    "students are struggling in real time so teachers can intervene earlier "
                    "and more effectively."
                ),
                type="reflection",
                tags="classkick,education,ai,product",
                sentiment_score=0.75,
                timestamp=now,
            ),
            # 2 days ago — habit entry
            EntryModel(
                content="Did a solid gym session and felt stronger than last week.",
                type="habit",
                tags="gym,health",
                sentiment_score=0.85,
                timestamp=now - timedelta(days=2),
            ),
            # Today — reflection
            EntryModel(
                content=(
                    "Felt a bit overwhelmed today, but breaking tasks down into smaller steps "
                    "made things feel more manageable."
                ),
                type="reflection",
                tags="mindset,planning",
                sentiment_score=0.55,
                timestamp= now - timedelta(days=5),
            ),
        ]

        db.add_all(demo_entries)
        db.commit()
        print("Seeded 3 demo entries with varied dates.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
