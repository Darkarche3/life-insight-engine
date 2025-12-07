from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./life_insights.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

'''
This file sets up the entire foundation of your database system:

engine → connection to the SQLite file

SessionLocal → how your app talks to the DB

Base → the parent class for all ORM tables
'''