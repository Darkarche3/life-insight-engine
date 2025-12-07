# Domain Model (Version 1)

This document defines the main entities in the Life Insights Engine.
These are the “things” the system cares about.

---

## Entry

Represents one piece of information I record about my day.

- **id**: integer  
- **timestamp**: datetime  
- **content**: string  
- **type**: one of `"note"`, `"habit"`, `"reflection"`  
- **tags**: list of strings  
- **sentiment_score**: float (range: -1 to 1)

---

## Tag

Represents a simple category attached to entries.

- **id**: integer  
- **name**: string

---

## Notes

- `Entry` is the core entity in the system.
- `Tag` exists only to help categorize entries.
- Weekly insights will NOT be stored as a database table.  
  They will be **computed** from entries.
