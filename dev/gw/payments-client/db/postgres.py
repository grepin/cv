from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.AUTH_POSTGRES_USER}:{settings.AUTH_POSTGRES_PASSWORD}@{settings.AUTH_POSTGRES_HOST}:{settings.AUTH_POSTGRES_PORT}/{settings.AUTH_POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
