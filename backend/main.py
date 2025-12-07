from fastapi import FastAPI
from db.base import engine, Base
from db import models

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Life Insights Engine backend is running!"}