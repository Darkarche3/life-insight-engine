# Life Insights Engine

A full-stack personal logging and insights application.

Users can:
- Create structured life entries (notes, habits, reflections)
- Tag, search, and filter entries
- View recent entries in a clean web interface

The system is built with a clear separation between backend and frontend, allowing each to be developed and deployed independently.

---

## Architecture Overview

Frontend (React)
        ↓ HTTP (JSON)
Backend API (FastAPI)
        ↓
Service Layer (business logic)
        ↓
Repository Layer (database access)
        ↓
SQLite Database

---

## Running the Project Locally

### Prerequisites
- Python 3.10+
- Node.js 22.x
- npm

---

## Backend Setup (FastAPI)

From the project root:

    cd backend
    python -m venv venv
    venv\Scripts\activate        (Windows)
    source venv/bin/activate    (macOS/Linux)

    pip install -r requirements.txt
    uvicorn main:app --reload

Backend runs at:
    http://127.0.0.1:8000

API documentation:
    http://127.0.0.1:8000/docs

---

## Frontend Setup (React + Vite)

From the project root:

    cd frontend
    npm install
    npm run dev

Frontend runs at:
    http://localhost:5173

---

## Environment Variables

Create a file at:

    frontend/.env

With the following content:

    VITE_API_BASE=http://127.0.0.1:8000

This allows the frontend API URL to be changed easily when deploying.

---

## Database

- SQLite is used for local development
- Data is persisted in a .db file
- Database files are intentionally not committed to Git

---

## Key Design Decisions

- Business logic lives in the service layer
- Database logic lives in the repository layer
- The API layer handles HTTP concerns only
- Tags are stored as strings in the database and exposed as lists in the API
- Filtering and search are done at the database level for performance
- Frontend and backend are fully decoupled

---

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

Frontend:
- React
- Vite
- Fetch API
- Plain CSS

---

## Code Formatting and Consistency

Backend (Python):

    pip install black ruff
    black .
    ruff check .

Frontend (React):

    cd frontend
    npm install --save-dev prettier
    npx prettier --write .

---

## Future Improvements
- PostgreSQL support (JSONB tags)
- Authentication
- Analytics and insights endpoints
- Production deployment (Vercel + Render)

---

## Notes
- Backend and frontend can be deployed independently
- Environment variables control API endpoints
- This project is designed to be extended incrementally
