from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

try:
    from config import Settings
except ImportError:
    from .config import Settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{Settings.database_username}:{Settings.database_password}@{Settings.database_hostname}:{Settings.database_port}/{Settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()