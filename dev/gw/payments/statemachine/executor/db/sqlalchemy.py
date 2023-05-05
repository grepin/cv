from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


def initsa():
    engine = create_engine(
        "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            settings.AUTH_POSTGRES_USER,
            settings.AUTH_POSTGRES_PASSWORD,
            settings.AUTH_POSTGRES_HOST,
            settings.AUTH_POSTGRES_PORT,
            settings.AUTH_POSTGRES_DB
        ),
        isolation_level="SERIALIZABLE",
        client_encoding="utf8",
        poolclass=NullPool
    )
    session = sessionmaker(
        autocommit=False,
        bind=engine
    )

    return engine, session
