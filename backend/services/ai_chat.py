import os
from typing import List
from google import genai
from sqlalchemy.orm import Session
from db.models import EntryModel


def _load_entries(db: Session, limit: int = 25) -> List[EntryModel]:
    return (
        db.query(EntryModel)
        .order_by(EntryModel.timestamp.desc())
        .limit(limit)
        .all()
    )


def _build_context(entries: List[EntryModel]) -> str:
    lines = []
    for e in reversed(entries):
        lines.append(
            f"- [id={e.id}] [{e.timestamp.strftime('%Y-%m-%d %H:%M')}] "
            f"(type={e.type}, sentiment={e.sentiment_score}, tags={e.tags}): {e.content}"
        )
    return "\n".join(lines)


def chat_with_journal(db: Session, question: str, limit: int = 25) -> dict:
    entries = _load_entries(db, limit=limit)
    if not entries:
        return {"answer": "There are no journal entries yet.", "mode": "no_data"}

    api_key = os.getenv("GEMINI_API_KEY")
    context = _build_context(entries)

    # Demo-safe fallback
    if not api_key:
        return {
            "answer": (
                "AI mode is disabled (no GEMINI_API_KEY). "
                "Based on your recent entries, you appear to be focused on projects, "
                "self-improvement, and reflection."
            ),
            "mode": "fallback",
        }

    # ✅ New Gemini client (non-deprecated)
    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a helpful assistant that answers questions using the user's journal entries.

Use ONLY the entries below as your source of truth.
If you are unsure, say you are unsure.


ENTRIES:
{context}

USER QUESTION:
{question}

Provide:
A short direct answer or 2–4 bullet points of evidence from the entries whichever is more appropriate.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return {
        "answer": response.text,
        "mode": "gemini",
    }
