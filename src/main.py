from fastapi import FastAPI
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from os import getenv
from fastapi.staticfiles import StaticFiles

load_dotenv()

DATABASE_URL = getenv('DB_CONNECTION')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define a function to get a database session.
def get_db():
    # Create a new session.
    db = SessionLocal()
    try:
        # Yield the session to the caller.
        yield db
    finally:
        # After the caller is done with the session, close it.
        db.close()

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")


from src.auth.views import router as auth_router
from src.post.views import router as posts_router

app.include_router(auth_router)
app.include_router(posts_router)


Base.metadata.create_all(bind=engine)
