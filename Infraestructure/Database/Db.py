from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/uamitosca-database?client_encoding=utf8"

DATABASE_URL = {
    "database": "uamitosca-database",
    "drivername": "postgresql+psycopg2",
    "username": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432",
    "query": {"client_encoding": "utf8"}
}

engine = create_engine(URL(**DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
