from fastapi import FastAPI

from db.base import engine, Base
from db import models

app = FastAPI()

# This line tells SQLAlchemy to create the tables in the database
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Life Insights Engine backend is running!"}