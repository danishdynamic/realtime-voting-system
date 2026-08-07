# infrastructure/db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Get the absolute path to the directory where THIS file (database.py) lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Define the database path relative to this file (e.g., puts it in the same folder)
DB_PATH = os.path.join(BASE_DIR, "polls.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"📡 DATABASE CONNECTION: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()